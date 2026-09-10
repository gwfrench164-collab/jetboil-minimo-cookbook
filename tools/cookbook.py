#!/usr/bin/env python3
"""Offline recipe validation and deterministic audit/index generation."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BEGIN GENERATED OFFICIAL RECIPE -->'
END = '<!-- END GENERATED OFFICIAL RECIPE -->'

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('YAML mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def read_recipe(path):
    text = path.read_text(encoding='utf-8')
    parts = re.split(r'^---[ \t]*\r?$', text, maxsplit=2, flags=re.M)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('expected opening and closing YAML frontmatter delimiters')
    data = yaml.load(parts[1], Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    return data, parts[2]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('reference escapes repository')
    return path

def canonical_url(value):
    u = urlsplit(value)
    return u.netloc.lower() + unquote(u.path).rstrip('/')

def render_official(data):
    o = data['official_recipe']
    lines = [START, '## Official Recipe', '',
             f"Source: [{o['source_title']}]({data['source']['source_url']})", '',
             'Published wording from the recorded source extract; only markup and outer whitespace are normalized.', '',
             '### Ingredients', '']
    lines += ['- ' + x for x in o['ingredients_exact']]
    if o['tools_exact']:
        lines += ['', '### Tools', ''] + ['- ' + x for x in o['tools_exact']]
    lines += ['', '### Instructions', '']
    for i, text in enumerate(o['instructions_exact'], 1):
        for group in o['instruction_groups']:
            if group['before_step'] == i:
                lines += ['#### ' + group['text'], '']
        lines += [f'{i}. {text}', '']
    if o['featured_products_exact']:
        lines += ['### Featured Recommended Products', ''] + ['- '+x for x in o['featured_products_exact']] + ['']
    lines += [END]
    return '\n'.join(lines)

def inspect(root):
    schema = json.loads((root / 'schemas/recipe.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    records, issues = [], []
    seen = {k:{} for k in ['id','title','url','content']}
    paths = sorted((root / '01_Recipes').rglob('*.md'))
    if not paths:
        issues.append(('ERROR','01_Recipes','empty_collection','No recipes found'))
    for path in paths:
        rel = path.relative_to(root).as_posix()
        def issue(level, code, message): issues.append((level,rel,code,message))
        try:
            data, body = read_recipe(path)
        except (ValueError, yaml.YAMLError, OSError) as exc:
            issue('ERROR','parse',str(exc)); continue
        errors = sorted(validator.iter_errors(data), key=lambda e:str(list(e.path)))
        for err in errors:
            issue('ERROR','schema',f"{'.'.join(map(str,err.path)) or 'root'}: {err.message}")
        record = {'path':rel,'data':data,'verified':False}
        records.append(record)
        if errors:
            continue
        s, c = data['source'], data['recipe_card']
        keyvals = {'id':data['id'],'title':re.sub(r'\W+','',data['title'].casefold()),
                   'content':json.dumps([c['ingredients'],c['instructions']],sort_keys=True)}
        if s['source_url']:
            keyvals['url'] = canonical_url(s['source_url'])
        for kind,key in keyvals.items():
            if key in seen[kind]:
                issue('ERROR','duplicate_'+kind,f'matches {seen[kind][key]}')
                issues.append(('ERROR',seen[kind][key],'duplicate_'+kind,f'matches {rel}'))
            seen[kind][key] = rel
        if [x['step'] for x in c['instructions']] != list(range(1,len(c['instructions'])+1)):
            issue('ERROR','step_order','Instruction numbers must be consecutive from 1')
        for group in data.get('official_recipe',{}).get('instruction_groups',[]):
            if group['before_step'] > len(data['official_recipe']['instructions_exact']):
                issue('ERROR','instruction_group','Group points beyond last instruction')
        if s['source_url']:
            u = urlsplit(s['source_url'])
            if u.scheme != 'https' or not u.hostname or u.username or u.password:
                issue('ERROR','source_url','Expected absolute HTTPS URL without credentials')
        if s['type'] == 'official_jetboil_recipe':
            if s['publisher'].casefold() != 'jetboil':
                issue('ERROR','publisher','Official recipe publisher must be Jetboil')
            if not s['source_url']:
                issue('WARNING','missing_source_url','Official source URL not yet identified')
            else:
                u = urlsplit(s['source_url'])
                if u.hostname != 'jetboil.johnsonoutdoors.com' or not re.match(r'^/(us|ca/en-ca)/recipes/[^/]+/?$',u.path):
                    issue('ERROR','official_domain','Official recipe needs a Jetboil recipe detail URL')
            if not data.get('audit'):
                issue('WARNING','source_unreviewed','Official content has not been source-audited')
        elif s['publisher'] != 'internal':
            issue('ERROR','publisher','Derived field systems must identify publisher as internal')
        if 'official_jetboil' in data.get('tags',[]) and s['type'] != 'official_jetboil_recipe':
            issue('ERROR','provenance_tag','Derived recipe tagged official')
        audit = data.get('audit',{})
        claims = (s.get('source_verified') is True or data['recipe_status'].get('official_recipe_verified') is True)
        verified_status = audit.get('status') in ('verified_cached','verified_live')
        if claims and not verified_status:
            issue('ERROR','unsupported_verified_claim','Verified flag requires a verified audit and evidence')
        if verified_status:
            before = len(issues)
            if data.get('schema_version') != 2:
                issue('ERROR','audit_schema','Audited recipes must use schema_version 2')
            try:
                snapshot_path = safe_path(root,audit['evidence_file'])
                blob = snapshot_path.read_bytes()
                if digest(blob) != audit['snapshot_sha256']:
                    raise ValueError('Snapshot checksum mismatch')
                snapshot = json.loads(blob)
                if snapshot['source_url'] != s['source_url']:
                    raise ValueError('Snapshot source URL mismatch')
                if snapshot['official_recipe'] != data.get('official_recipe'):
                    raise ValueError('Official content differs from source snapshot')
                if snapshot['accessed_on'] != audit['checked_on'] or snapshot['retrieval_method'] != audit['method'] or snapshot['live_check'] != audit['live_check']:
                    raise ValueError('Audit metadata differs from source snapshot')
                evidence = safe_path(root,snapshot['evidence_file']).read_bytes()
                if digest(evidence) != snapshot['evidence_sha256']:
                    raise ValueError('Source extract checksum mismatch')
                if date.fromisoformat(audit['checked_on']) > date.today():
                    raise ValueError('Audit date is in the future')
                if audit['status'] == 'verified_live' and (audit['method'] != 'direct_official_page' or audit['live_check'] != 'verified'):
                    raise ValueError('Live verification requires direct retrieval evidence')
                if audit['status'] == 'verified_cached' and audit['method'] != 'indexed_official_page':
                    raise ValueError('Cached verification requires indexed retrieval evidence')
                o=data['official_recipe']
                if s.get('source_verified') is not True or data['recipe_status'].get('official_recipe_verified') is not True:
                    raise ValueError('Verification flags disagree with audit status')
                if c.get('equipment') != o['tools_exact']:
                    raise ValueError('Card tools differ from official tools list')
                if c.get('servings') is not None or any(c.get(k) for k in ['yield','prep_time','cook_time','total_time']):
                    raise ValueError('Current source snapshot has no standalone serving/yield/time metadata')
                if s.get('official_title') != o['source_title'] or data['title'] != o['source_title'] or c['title'] != o['source_title']:
                    raise ValueError('Official titles disagree')
                if c.get('content_basis') != 'official_recipe':
                    raise ValueError('Audited card must identify its content basis')
                if c['ingredients'] != [{'source_text':x} for x in o['ingredients_exact']] or [x['text'] for x in c['instructions']] != o['instructions_exact']:
                    raise ValueError('Recipe card differs from official text; regenerate it')
                expected = render_official(data)
                if body.count(START)!=1 or body.count(END)!=1 or expected not in body:
                    raise ValueError('Rendered official section differs; regenerate it')
                for heading in ['## MiniMo Adaptation','## Field-Tested Variations','## Proposed Variations']:
                    if heading not in body:
                        raise ValueError('Missing section '+heading)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                issue('ERROR','audit_evidence',str(exc))
            record['verified'] = len(issues)==before
        # Check actual Markdown links, never manufacture ingredient/technique relationships.
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',body):
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) and not target.startswith('#'):
                target = unquote(target.split('#',1)[0])
                if target and not (path.parent / target).exists():
                    issue('ERROR','broken_link',target)
    # A failed schema/duplicate/link check must never appear as verified in the tracker.
    bad = {x[1] for x in issues if x[0]=='ERROR'}
    for rec in records:
        if rec['path'] in bad: rec['verified']=False
    return records, sorted(issues)

def report_files(records,issues):
    official=[r for r in records if r['data'].get('source',{}).get('type')=='official_jetboil_recipe']
    verified=sum(r['verified'] for r in official)
    lines=['# Recipe Accuracy Audit Tracker','','Generated by `python tools/build_project_audit.py`. Do not edit manually.','',
           f'{len(records)} recipe files; {len(official)} labeled official Jetboil; {len(records)-len(official)} derived. {verified} official recipes verified against recorded source text.','',
           '“Verified (indexed)” means compared with indexed official-page text, not a fresh live-site capture. Editorial review does not mean field-tested or comprehensive.','',
           '| Recipe | Source audit | Checked | MiniMo review | Field tests |','|---|---|---|---|---|']
    for r in official:
        d=r['data'];a=d.get('audit',{})
        status=('Verified (indexed)' if a.get('status')=='verified_cached' else 'Verified (live)') if r['verified'] else 'Pending / invalid evidence'
        lines.append(f"| [{d.get('title',r['path'])}](../{r['path']}) | {status} | {a.get('checked_on','—')} | {d.get('minimo_adaptation',{}).get('status','pending')} | {len(d.get('field_tested_variations',{}).get('entries',[]))} |")
    lines += ['', '## Outstanding checks','']
    if issues:
        lines += ['| Severity | File | Check | Detail |','|---|---|---|---|']
        for level,path,code,msg in issues:
            lines.append(f"| {level} | {path} | {code} | {msg.replace('|','/').replace(chr(10),' ')} |")
    else: lines += ['None.']
    index=['# Recipe Index','','Generated by `python tools/build_project_audit.py`. Audit status: [Recipe Accuracy Audit Tracker](Recipe_Accuracy_Audit_Tracker.md).','']
    groups={}
    for r in records:groups.setdefault(Path(r['path']).parts[1],[]).append(r)
    for group,rs in sorted(groups.items()):
        index += ['## '+group.replace('_',' '),'']
        for r in rs:
            d=r['data']; source=d.get('source',{}).get('type','invalid')
            index.append(f"- [{d.get('title',r['path'])}](../{r['path']}) — {source}; {'source verified' if r['verified'] else 'not source verified'}")
        index+=['']
    summary={'recipe_count':len(records),'official_count':len(official),'verified_count':verified,'derived_count':len(records)-len(official),'issues':[dict(zip(['severity','path','code','message'],i)) for i in issues],'recipes':[{'path':r['path'],'id':r['data'].get('id'),'source_verified':r['verified'],'audit':r['data'].get('audit',{}).get('status','pending')} for r in records]}
    return {'08_Index/Recipe_Accuracy_Audit_Tracker.md':'\n'.join(lines)+'\n','08_Index/recipe-index.md':'\n'.join(index).rstrip()+'\n','08_Index/recipe-audit.json':json.dumps(summary,indent=2,ensure_ascii=False)+'\n'}

def main(default='validate'):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--baseline',type=Path,help='Known warning list; fail on new or obsolete entries')
    p.add_argument('--strict',action='store_true',help='Treat audit backlog warnings as failures')
    p.add_argument('--check',action='store_true',help='For report generation: check outputs without changing files')
    args=p.parse_args();root=args.root.resolve()
    try: records,issues=inspect(root)
    except (OSError,ValueError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1
    if default=='provenance':
        codes={'parse','schema','missing_source_url','source_unreviewed','publisher','source_url','official_domain','unsupported_verified_claim','audit_evidence','audit_schema','provenance_tag','duplicate_url'}
        issues=[i for i in issues if i[2] in codes]
    failed=any(x[0]=='ERROR' or args.strict for x in issues)
    if args.baseline:
        try:
            baseline=json.loads(args.baseline.read_text())
            expected={tuple(x) for x in baseline['known_warnings']}
            actual={(x[1],x[2]) for x in issues if x[0]=='WARNING'}
            for key in sorted(actual-expected):print('NEW WARNING: '+': '.join(key));failed=True
            for key in sorted(expected-actual):print('OBSOLETE BASELINE: '+': '.join(key));failed=True
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print('ERROR reading warning baseline: '+str(exc));failed=True
    if default=='report':
        if failed:
            print('Cannot generate or verify reports while validation fails.',file=sys.stderr)
        else:
            for rel,content in report_files(records,issues).items():
                path=root/rel
                if args.check:
                    if not path.exists() or path.read_text()!=content:
                        print('STALE: '+rel);failed=True
                else:
                    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
    for level,path,code,msg in issues:print(f'{level} {path} [{code}]: {msg}')
    print(f'{len(records)} recipes; {sum(i[0]=="ERROR" for i in issues)} errors; {sum(i[0]=="WARNING" for i in issues)} warnings')
    return int(failed)

if __name__=='__main__':sys.exit(main())
