#!/usr/bin/env python3
"""Synchronize audited cards and their marked Markdown projection; never edit sources."""
import argparse
import re
from pathlib import Path
import yaml
from cookbook import ROOT, START, END, read_recipe, render_official

def synchronize(data,body):
    o=data['official_recipe'];c=data['recipe_card']
    c['ingredients']=[{'source_text':x} for x in o['ingredients_exact']]
    c['instructions']=[{'step':i,'text':x} for i,x in enumerate(o['instructions_exact'],1)]
    c['title']=o['source_title'];c['equipment']=o['tools_exact'];c['content_basis']='official_recipe'
    if body.count(START)!=1 or body.count(END)!=1:
        raise ValueError('Expected exactly one generated official block')
    body=re.sub(re.escape(START)+'.*?'+re.escape(END),lambda _:render_official(data),body,flags=re.S)
    return '---\n'+yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=110)+'---\n'+body.lstrip('\n')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--write',action='store_true');a=p.parse_args();stale=False
    for path in sorted((a.root/'01_Recipes').rglob('*.md')):
        data,body=read_recipe(path)
        if data.get('schema_version')!=2:continue
        text=synchronize(data,body)
        if text!=path.read_text():
            if a.write:path.write_text(text,encoding='utf-8');print('Updated '+str(path.relative_to(a.root)))
            else:stale=True;print('STALE '+str(path.relative_to(a.root)))
    return int(stale)

if __name__=='__main__':raise SystemExit(main())
