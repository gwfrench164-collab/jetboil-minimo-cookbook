"""Regression checks for lossless compilation and conservative connections."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_database import collect, outputs, write_sqlite, logical_database, FOLDERS
from cookbook import read_recipe

class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=collect(ROOT)

    def test_every_source_record_is_preserved(self):
        paths={p.relative_to(ROOT).as_posix() for folder in FOLDERS for p in (ROOT/folder).rglob('*.md')}
        self.assertEqual(paths,{e['key'] for e in self.data['entities']})
        for e in self.data['entities']:
            raw=(ROOT/e['key']).read_text()
            if raw.lstrip().startswith('---'):
                metadata,body=read_recipe(ROOT/e['key'])
                self.assertEqual(e['metadata'],metadata)
                self.assertEqual(e['body'],body.strip())
            else:
                self.assertEqual(e['body'],raw.strip())

    def test_official_lines_are_exact(self):
        checked=0
        for e in self.data['entities']:
            o=e['metadata'].get('official_recipe')
            if o:
                checked+=1
                self.assertEqual([x['text'] for x in e['ingredients']],o['ingredients_exact'])
                self.assertEqual([x['text'] for x in e['instructions']],o['instructions_exact'])
        self.assertGreater(checked,0)

    def test_uncertain_links_do_not_choose_targets(self):
        statuses=set()
        keys={e['key'] for e in self.data['entities']}
        for r in self.data['relationships']:
            statuses.add(r['status'])
            if r['status']=='resolved':
                self.assertEqual(r['candidates'],[r['target']])
                self.assertIn(r['target'],keys)
            else:
                self.assertIsNone(r['target'])
                if r['status']=='ambiguous':self.assertGreater(len(r['candidates']),1)
                else:self.assertEqual(r['candidates'],[])
        self.assertEqual(statuses,{'resolved','ambiguous','unresolved'})
        self.assertTrue(any(x['kind']=='duplicate_id' for x in self.data['issues']))

    def test_sqlite_integrity_and_full_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'a.sqlite';q=Path(temp)/'b.sqlite'
            write_sqlite(self.data,p);write_sqlite(self.data,q)
            self.assertEqual(logical_database(p),logical_database(q))
            with sqlite3.connect(p) as db:
                rows=db.execute('SELECT key,metadata_json FROM entities').fetchall()
                self.assertEqual(len(rows),len(self.data['entities']))
                expected={e['key']:json.loads(json.dumps(e['metadata'],default=str)) for e in self.data['entities']}
                for key,metadata in rows:self.assertEqual(json.loads(metadata),expected[key])
                self.assertGreater(db.execute('SELECT count(*) FROM equipment_mentions').fetchone()[0],0)
                self.assertFalse(db.execute('PRAGMA foreign_key_check').fetchall())

    def test_embedded_data_cannot_close_script(self):
        data=copy.deepcopy(self.data)
        attack='</script><script>alert(1)</script>&'
        data['entities'][0]['body']=attack
        html=outputs(ROOT,data)['Open Cookbook.html']
        self.assertNotIn(attack,html)
        start='<script id="library-data" type="application/json">'
        embedded=html.split(start,1)[1].split('</script>',1)[0]
        self.assertEqual(json.loads(embedded)['entities'][0]['body'],attack)

    def test_recipe_audit_counts_exclude_reference_records(self):
        counts=self.data['recipe_audit_counts']
        self.assertEqual(sum(counts.values()),self.data['counts']['recipe'])
        self.assertNotIn('reference',counts)
        for status,count in counts.items():
            self.assertEqual(count,sum(e['kind']=='recipe' and e['status']==status for e in self.data['entities']))
        self.assertEqual(counts.get('verified_cached',0)+counts.get('verified_live',0),self.data['verified_recipes'])

    def test_output_is_reproducible(self):
        self.assertEqual(outputs(ROOT,self.data),outputs(ROOT,collect(ROOT)))

if __name__=='__main__':unittest.main()
