#!/usr/bin/env python3
"""Compile the entire Markdown knowledge base into SQLite and an offline browser."""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from cookbook import ROOT, inspect, read_recipe

FOLDERS={'01_Recipes':'recipe','02_Techniques':'technique','03_Ingredients':'ingredient','04_Components':'component','05_Pantry_Modules':'pantry'}
RELATIONS={'related_recipes':'recipe','recipes_used_in':'recipe','linked_recipes':'recipe','used_in_recipes':'recipe','related_ingredients':'ingredient','linked_ingredients':'ingredient','related_techniques':'technique','linked_techniques':'technique','related_pantry_modules':'pantry','pantry_modules':'pantry','components_used_in':'component','linked_components':'component','substitutions':'ingredient','ingredients':'ingredient'}

def norm(value):return re.sub(r'[^\w]+',' ',str(value).casefold()).strip()
def textify(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,default=str)
def recipe_line(line):
    if 'source_text' in line:return line['source_text']
    parts=[str(line.get(k,'')) for k in ['amount','unit','item'] if line.get(k) not in ('',None)]
    out=' '.join(parts)
    extra=[str(line[k]) for k in ['preparation','notes'] if line.get(k)]
    return out+(' ('+'; '.join(extra)+')' if extra else '')

def unique_json(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate JSON field: '+key)
        result[key]=value
    return result

def apply_connection_reviews(root,entities,relationships):
    path=root/'08_Index/connection_reviews.json'
    if not path.exists():return []
    document=json.loads(path.read_text(),object_pairs_hook=unique_json)
    schema=json.loads((root/'schemas/connection-reviews.schema.json').read_text())
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(document))
    if errors:raise ValueError('Invalid connection review: '+errors[0].message)
    records={e['key']:e for e in entities}
    lookup=defaultdict(list)
    for link in relationships:lookup[(link['origin'],link['field'],link['label'])].append(link)
    seen=set()
    for review in document['reviews']:
        identity=tuple(review[k] for k in ('origin','field','label'))
        if identity in seen:raise ValueError('Duplicate connection review: '+str(identity))
        seen.add(identity)
        if len(lookup[identity])!=1:raise ValueError('Review must identify exactly one existing connection: '+str(identity))
        for side in ('origin','target'):
            record=records.get(review[side])
            if not record or record['sha256']!=review[side+'_sha256']:
                raise ValueError('Connection review needs renewal after record change: '+review[side])
        link=lookup[identity][0]
        link['original_match']={k:link[k] for k in ('target_kind','target','candidates','status','basis')}
        link.update(target=review['target'],target_kind=records[review['target']]['kind'],candidates=[review['target']],status='resolved',basis='reviewed_connection',review=review)
    return document['reviews']

def collect(root):
    recipe_checks,check_issues=inspect(root)
    errors=[i for i in check_issues if i[0]=='ERROR']
    if errors:raise ValueError('Recipe validation failed: '+str(errors[:5]))
    verified={r['path']:r['verified'] for r in recipe_checks}
    entities=[];issues=[]
    for folder,kind in FOLDERS.items():
        for p in sorted((root/folder).rglob('*.md')):
            raw=p.read_text(encoding='utf-8');path=p.relative_to(root).as_posix()
            if raw.lstrip().startswith('---'):
                d,body=read_recipe(p)
            else:
                d={};body=raw
            heading=re.search(r'^#\s+(.+)$',body,re.M)
            title=d.get('title') or d.get('canonical_name') or d.get('name') or (heading.group(1) if heading else p.stem.replace('-',' ').title())
            source=d.get('source',{})
            if not isinstance(source,dict):source={'original':source}
            status='reference'
            if kind=='recipe':
                status='verified_cached' if verified.get(path) and d.get('audit',{}).get('status')=='verified_cached' else 'verified_live' if verified.get(path) else 'derived' if source.get('type')=='derived_field_system' else 'unreviewed'
            entity={'key':path,'kind':kind,'id':d.get('id'),'title':str(title),'category':p.parent.name.replace('_',' ') if kind=='recipe' else kind,'status':status,'source':source,'metadata':d,'body':body.strip(),'sha256':hashlib.sha256(raw.encode()).hexdigest()}
            if kind=='recipe':
                c=d['recipe_card'];o=d.get('official_recipe')
                entity['ingredients']=[{'position':i,'text':recipe_line(x),'item':x.get('item'),'amount':x.get('amount'),'unit':x.get('unit'),'basis':'official_transcription' if o else 'legacy_record'} for i,x in enumerate(c['ingredients'],1)]
                entity['instructions']=[{'position':i,'text':x['text']} for i,x in enumerate(c['instructions'],1)]
                entity['groups']=o.get('instruction_groups',[]) if o else []
                # These labels preserve exactly what the source/card says; not inferred compatibility.
                entity['equipment']=c.get('equipment',[])
                entity['featured_products']=o.get('featured_products_exact',[]) if o else []
            entities.append(entity)
            if not entity['id']:issues.append({'kind':'missing_id','record':path,'detail':'Stable path used; original has no ID.'})
    lookup=defaultdict(set);ids=defaultdict(list)
    for e in entities:
        ids[(e['kind'],e['id'])].append(e['key'])
        terms=[e['id'],e['title'],Path(e['key']).stem]+e['metadata'].get('aliases',[])
        for term in terms:
            if isinstance(term,str) and term:lookup[(e['kind'],norm(term))].add(e['key'])
    for (kind,ident),paths in sorted(ids.items(),key=str):
        if ident and len(paths)>1:issues.append({'kind':'duplicate_id','record':', '.join(paths),'detail':str(ident)+' is shared; ID links remain ambiguous.'})
    relationships=[]
    def add(origin,field,kind,target,basis):
        if not isinstance(target,str) or not target.strip():return
        candidates=sorted(lookup[(kind,norm(target))]);status='resolved' if len(candidates)==1 else 'ambiguous' if candidates else 'unresolved'
        relationships.append({'origin':origin,'field':field,'target_kind':kind,'label':target,'target':candidates[0] if len(candidates)==1 else None,'candidates':candidates,'status':status,'basis':basis})
    for e in entities:
        for field,kind in RELATIONS.items():
            value=e['metadata'].get(field,[])
            if isinstance(value,str):value=[value]
            if isinstance(value,list):
                for target in value:add(e['key'],field,kind,target,'explicit_record_reference')
        if e['kind']=='recipe':
            for line in e['ingredients']:
                # Only exact existing names/aliases. No fuzzy matching or ingredient inventions.
                if line.get('item'):add(e['key'],'ingredient_line:'+str(line['position']),'ingredient',line['item'],'exact_ingredient_name')
    reviews=apply_connection_reviews(root,entities,relationships)
    # Review flags are data, not silent deletions or fabricated link targets.
    counts=Counter(e['kind'] for e in entities)
    payload={'schema_version':1,'counts':dict(sorted(counts.items())),'verified_recipes':sum(e['status'].startswith('verified') for e in entities),'entities':entities,'relationships':relationships,'issues':issues,'connection_reviews':reviews}
    payload['recipe_audit_counts']=dict(sorted(Counter(e['status'] for e in entities if e['kind']=='recipe').items()))
    payload['content_sha256']=hashlib.sha256(textify(payload).encode()).hexdigest()
    return payload

DDL='''
PRAGMA foreign_keys=ON;
CREATE TABLE entities (key TEXT PRIMARY KEY, kind TEXT NOT NULL, legacy_id TEXT, title TEXT NOT NULL, category TEXT, audit_status TEXT NOT NULL, source_json TEXT NOT NULL, metadata_json TEXT NOT NULL, body TEXT NOT NULL, content_sha256 TEXT NOT NULL);
CREATE INDEX entity_kind ON entities(kind);
CREATE INDEX entity_legacy_id ON entities(legacy_id);
CREATE TABLE ingredient_lines (recipe_key TEXT REFERENCES entities(key), position INTEGER, original_text TEXT NOT NULL, item TEXT, amount TEXT, unit TEXT, basis TEXT NOT NULL, PRIMARY KEY(recipe_key,position));
CREATE TABLE instructions (recipe_key TEXT REFERENCES entities(key), position INTEGER, original_text TEXT NOT NULL, PRIMARY KEY(recipe_key,position));
CREATE TABLE relationships (relationship_id INTEGER PRIMARY KEY, origin_key TEXT NOT NULL REFERENCES entities(key), field TEXT NOT NULL, target_kind TEXT NOT NULL, original_label TEXT NOT NULL, target_key TEXT REFERENCES entities(key), status TEXT NOT NULL CHECK(status IN ('resolved','ambiguous','unresolved')), candidates_json TEXT NOT NULL, basis TEXT NOT NULL);
CREATE INDEX relationships_origin ON relationships(origin_key);
CREATE INDEX relationships_target ON relationships(target_key);
CREATE TABLE connection_reviews (origin_key TEXT REFERENCES entities(key), field TEXT, original_label TEXT, target_key TEXT REFERENCES entities(key), reviewed_on TEXT, rationale TEXT, evidence_json TEXT, PRIMARY KEY(origin_key,field,original_label));
CREATE TABLE review_issues (kind TEXT, record TEXT, detail TEXT);
CREATE TABLE equipment_mentions (entity_key TEXT REFERENCES entities(key), context TEXT, position INTEGER, original_text TEXT NOT NULL, PRIMARY KEY(entity_key,context,position));
CREATE TABLE build_info (schema_version INTEGER, content_sha256 TEXT);
CREATE VIEW recipes AS SELECT * FROM entities WHERE kind='recipe';
CREATE VIEW ingredients AS SELECT * FROM entities WHERE kind='ingredient';
CREATE VIEW techniques AS SELECT * FROM entities WHERE kind='technique';
CREATE VIEW pantry_modules AS SELECT * FROM entities WHERE kind='pantry';
CREATE VIEW components AS SELECT * FROM entities WHERE kind='component';
'''

def write_sqlite(payload,path):
    db=sqlite3.connect(path)
    try:
        db.executescript(DDL)
        for e in payload['entities']:
            db.execute('INSERT INTO entities VALUES (?,?,?,?,?,?,?,?,?,?)',(e['key'],e['kind'],e['id'],e['title'],e['category'],e['status'],textify(e['source']),textify(e['metadata']),e['body'],e['sha256']))
            for x in e.get('ingredients',[]):db.execute('INSERT INTO ingredient_lines VALUES (?,?,?,?,?,?,?)',(e['key'],x['position'],x['text'],x['item'],None if x['amount'] is None else str(x['amount']),x['unit'],x['basis']))
            for x in e.get('instructions',[]):db.execute('INSERT INTO instructions VALUES (?,?,?)',(e['key'],x['position'],x['text']))
        for e in payload['entities']:
            for context,values in [('recipe_card.equipment',e.get('equipment',[])),('official_recipe.featured_products',e.get('featured_products',[])),('equipment',e['metadata'].get('equipment',[]))]:
                if isinstance(values,str):values=[values]
                if isinstance(values,list):
                    for i,value in enumerate(values,1):
                        if isinstance(value,str):db.execute('INSERT INTO equipment_mentions VALUES (?,?,?,?)',(e['key'],context,i,value))
        for x in payload['relationships']:db.execute('INSERT INTO relationships(origin_key,field,target_kind,original_label,target_key,status,candidates_json,basis) VALUES (?,?,?,?,?,?,?,?)',(x['origin'],x['field'],x['target_kind'],x['label'],x['target'],x['status'],textify(x['candidates']),x['basis']))
        for x in payload.get('connection_reviews',[]):
            db.execute('INSERT INTO connection_reviews VALUES (?,?,?,?,?,?,?)',(x['origin'],x['field'],x['label'],x['target'],x['reviewed_on'],x['rationale'],textify(x)))
        for x in payload['issues']:db.execute('INSERT INTO review_issues VALUES (?,?,?)',(x['kind'],x['record'],x['detail']))
        db.execute('INSERT INTO build_info VALUES (?,?)',(1,payload['content_sha256']));db.commit()
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
    finally:db.close()

def outputs(root,payload):
    encoded=json.dumps(payload,ensure_ascii=False,separators=(',',':'),default=str)
    # JSON is inert data, not executable HTML, including user-authored source text.
    safe=encoded.replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    template=(root/'app/library.html').read_text()
    assert template.count('/*__LIBRARY_DATA__*/')==1
    html=template.replace('/*__LIBRARY_DATA__*/',safe)
    rs=Counter(x['status'] for x in payload['relationships'])
    report=['# Connected database status','','Generated by `python tools/build_database.py`.','','## Imported records','']
    report += [f'- {k}: {v}' for k,v in payload['counts'].items()]
    report += ['',f"Total: {len(payload['entities'])}. Source-verified recipes: {payload['verified_recipes']} (see recipe audit for cached/live distinction).",'', '## Connections','']+[f'- {k}: {v}' for k,v in sorted(rs.items())]
    report += ['', '## Recipe source review', ''] + [f'- {status}: {count}' for status,count in payload['recipe_audit_counts'].items()]
    report += ['',f"Documented connection corrections: {len(payload.get('connection_reviews',[]))}. Original fields and labels remain preserved.",'']
    report += ['','Connections are copied from explicit references or matched by exact ingredient name/alias. Resolved means one record matches, not that the culinary relationship was independently verified. Ambiguous references have no chosen target. All source files and conflicting records are retained.','','## Identifier issues','']
    report += [f"- {x['kind']}: `{x['record']}` - {x['detail']}" for x in payload['issues']]
    report += ['','## Pending connections','']+[f"- `{x['origin']}` / `{x['field']}`: {x['label']} ({x['status']})" for x in payload['relationships'] if x['status']!='resolved']
    return {'Open Cookbook.html':html,'output/database/library.json':json.dumps(payload,ensure_ascii=False,indent=2,default=str)+'\n','08_Index/Database_Status.md':'\n'.join(report)+'\n'}

def logical_database(path):
    with sqlite3.connect(path.as_uri()+"?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Database integrity check failed")
        return list(db.iterdump())

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--check',action='store_true');a=p.parse_args();root=a.root.resolve()
    try:
        data=collect(root);files=outputs(root,data)
        with tempfile.TemporaryDirectory() as tmp:
            dbpath=Path(tmp)/'cookbook.sqlite';write_sqlite(data,dbpath)
            if a.check:
                stale=[rel for rel,content in files.items() if not (root/rel).exists() or (root/rel).read_text()!=content]
                target=root/'output/database/cookbook.sqlite'
                if not target.exists() or logical_database(target)!=logical_database(dbpath):stale.append('output/database/cookbook.sqlite')
                if stale:raise ValueError('Stale generated outputs: '+', '.join(stale))
            else:
                # Build and validate everything before replacing any existing output.
                for rel,content in files.items():
                    target=root/rel;target.parent.mkdir(parents=True,exist_ok=True)
                    with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as f:f.write(content.encode());temp=f.name
                    os.replace(temp,target)
                target=root/'output/database/cookbook.sqlite';target.parent.mkdir(parents=True,exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as f:f.write(dbpath.read_bytes());temp=f.name
                os.replace(temp,target)
        print(f"Database ready: {len(data['entities'])} records; {len(data['relationships'])} recorded connections.")
        return 0
    except (OSError,ValueError,sqlite3.Error,yaml.YAMLError) as exc:print('Build failed: '+str(exc));return 1
if __name__=='__main__':raise SystemExit(main())
