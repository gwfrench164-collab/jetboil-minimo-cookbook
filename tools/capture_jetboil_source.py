#!/usr/bin/env python3
"""Capture a candidate from official HTML; never mark a recipe verified or overwrite it."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

HOST='jetboil.johnsonoutdoors.com'

def extract(html):
    soup=BeautifulSoup(html,'html.parser')
    h1=soup.find('h1')
    if h1 is None:raise ValueError('No recipe title; blocked or changed page. No source accepted.')
    title=h1.get_text().strip()
    out=dict(source_title=title,ingredients_exact=[],instructions_exact=[],instruction_groups=[],tools_exact=[],featured_products_exact=[])
    section=None; started=False
    names={'ingredients':'ingredients_exact','instructions':'instructions_exact','tools':'tools_exact','featured recommended products':'featured_products_exact'}
    for el in h1.find_all_next():
        if el.name in ['h1','h2','h3','h4','h5','h6']:
            text=el.get_text().strip();name=text.rstrip(':').lower()
            if name in names:section=names[name];started=True
            elif section=='instructions_exact' and el.name in ('h4','h5','h6'):
                out['instruction_groups'].append({'before_step':len(out['instructions_exact'])+1,'text':text})
            elif started:break
        elif el.name=='p' and section=='instructions_exact' and el.get_text().strip():
            # Some source pages use paragraphs as timing group labels.
            out['instruction_groups'].append({'before_step':len(out['instructions_exact'])+1,'text':el.get_text().strip()})
        elif el.name=='li' and section:
            # Stop after the recipe, before related articles and site navigation.
            if el.find_parent(['nav','footer']):break
            text=el.get_text().strip()
            if text:out[section].append(text)
        elif started and el.get_text().strip().startswith('Tagged'):
            break
    if not out['ingredients_exact'] or not out['instructions_exact']:
        raise ValueError('Missing ingredients/instructions; blocked or changed page. No source accepted.')
    if any(g['before_step']>len(out['instructions_exact']) for g in out['instruction_groups']):
        raise ValueError('Unexpected trailing instruction text; review page structure manually')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('url');p.add_argument('--html',type=Path,help='HTML saved from this URL in your browser')
    p.add_argument('--output',type=Path,required=True,help='New directory outside the canonical audit snapshots')
    a=p.parse_args();u=urlsplit(a.url)
    if u.scheme!='https' or u.hostname!=HOST or u.username or u.password or not re.match(r'^/(us|ca/en-ca)/recipes/[^/]+/?$',u.path):p.error('An official Jetboil recipe detail URL is required')
    try:
        if a.output.exists():raise ValueError('Output directory exists; choose a new one to preserve evidence')
        if a.html:html=a.html.read_bytes()
        else:
            with urlopen(Request(a.url,headers={'User-Agent':'MiniMoCookbookSourceCheck/1.0'}),timeout=30) as response:
                if urlsplit(response.url).hostname!=HOST:raise ValueError('Unexpected redirect host')
                html=response.read(5_000_001)
        if len(html)>5_000_000:raise ValueError('Page too large')
        official=extract(html)
        snapshot={'source_url':a.url,'accessed_on':date.today().isoformat(),'retrieval_method':'direct_official_page','live_check':'verified','normalization':'HTML markup removed and outer whitespace trimmed. Review list grouping and word boundaries before accepting.','evidence_file':'source.html','evidence_sha256':hashlib.sha256(html).hexdigest(),'official_recipe':official}
        a.output.mkdir(parents=True);(a.output/'source.html').write_bytes(html)
        (a.output/'candidate.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
        print('Candidate only: '+str(a.output/'candidate.json')+'; compare and review before accepting.')
    except Exception as exc:
        print('Source capture failed: '+str(exc));return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
