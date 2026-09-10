#!/usr/bin/env python3
"""Show official-source drift without modifying either file. Exit 1 means changed."""
import argparse,difflib,json
from pathlib import Path
from cookbook import read_recipe

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('recipe',type=Path);p.add_argument('candidate',type=Path);a=p.parse_args()
    d,_=read_recipe(a.recipe);candidate=json.loads(a.candidate.read_text())
    if d['source']['source_url']!=candidate['source_url']:p.error('Candidate URL does not match recipe')
    old=json.dumps(d['official_recipe'],ensure_ascii=False,indent=2).splitlines(True)
    new=json.dumps(candidate['official_recipe'],ensure_ascii=False,indent=2).splitlines(True)
    diff=list(difflib.unified_diff(old,new,fromfile='Recorded official recipe',tofile='Candidate official recipe'))
    print(''.join(diff) if diff else 'No official text changes found.')
    raise SystemExit(bool(diff))
