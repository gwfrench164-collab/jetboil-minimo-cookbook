import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_database import apply_connection_reviews, collect, unique_json

class ConnectionReviews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=collect(ROOT)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'08_Index').mkdir();(self.root/'schemas').mkdir()
        shutil.copy(ROOT/'schemas/connection-reviews.schema.json',self.root/'schemas')
        self.doc=json.loads((ROOT/'08_Index/connection_reviews.json').read_text())
        self.entities=copy.deepcopy(self.data['entities'])
        self.links=copy.deepcopy(self.data['relationships'])
        for link in self.links:
            if 'original_match' in link:
                link.update(link.pop('original_match'));link.pop('review',None)
    def apply(self):
        (self.root/'08_Index/connection_reviews.json').write_text(json.dumps(self.doc))
        return apply_connection_reviews(self.root,self.entities,self.links)
    def test_review_keeps_original_and_selects_documented_target(self):
        self.apply()
        for link in self.links:
            if 'review' in link:
                self.assertEqual(link['target'],link['review']['target'])
                self.assertIn(link['original_match']['status'],('unresolved','ambiguous'))
    def test_changed_evidence_rejected(self):
        key=self.doc['reviews'][0]['target']
        next(e for e in self.entities if e['key']==key)['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'renewal'):self.apply()
    def test_duplicate_decision_rejected(self):
        self.doc['reviews'].append(self.doc['reviews'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate connection'):self.apply()
    def test_unknown_field_rejected(self):
        self.doc['reviews'][0]['guessed']=True
        with self.assertRaisesRegex(ValueError,'Invalid connection'):self.apply()
    def test_missing_connection_rejected(self):
        self.doc['reviews'][0]['label']='nonexistent'
        with self.assertRaisesRegex(ValueError,'exactly one'):self.apply()
    def test_invalid_date_rejected(self):
        self.doc['reviews'][0]['reviewed_on']='2026-99-99'
        with self.assertRaisesRegex(ValueError,'Invalid connection'):self.apply()
    def test_duplicate_json_field_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate JSON'):json.loads('{"x":1,"x":2}',object_pairs_hook=unique_json)
    def test_numeric_collisions_are_not_guessed(self):
        for link in self.data['relationships']:
            if link['label'] in ('ingredient-0002','technique-0003'):
                self.assertEqual(link['status'],'ambiguous');self.assertIsNone(link['target'])
