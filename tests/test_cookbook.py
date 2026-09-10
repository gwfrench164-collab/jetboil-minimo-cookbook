import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from cookbook import inspect,read_recipe,report_files,digest,UniqueLoader
from render_recipes import synchronize
from capture_jetboil_source import extract

class RecipeChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ['schemas','01_Recipes','06_Source_Research']:
            shutil.copytree(ROOT/name,self.root/name)
        self.path=self.root/'01_Recipes/Breakfast/quinoa-breakfast-bowl.md'
    def issues(self):return inspect(self.root)[1]
    def codes(self):return {i[2] for i in self.issues()}
    def mutate(self,fn):
        d,body=read_recipe(self.path);fn(d)
        self.path.write_text('---\n'+yaml.safe_dump(d,sort_keys=False,allow_unicode=True)+'---\n'+body)
    def test_repository_has_no_errors(self):
        self.assertFalse([i for i in self.issues() if i[0]=='ERROR'])
        records,_=inspect(self.root)
        self.assertEqual(sum(r['verified'] for r in records),7)
    def test_duplicate_yaml_keys_fail_in_nested_mapping(self):
        text=self.path.read_text().replace('  publisher: JetBoil','  publisher: JetBoil\n  publisher: internal')
        self.path.write_text(text);self.assertIn('parse',self.codes())
    def test_unknown_nested_field(self):
        self.mutate(lambda d:d['recipe_card'].update(instrutions=[]))
        self.assertIn('schema',self.codes())
    def test_wrong_boolean_type(self):
        self.mutate(lambda d:d['recipe_status'].update(collected='true'))
        self.assertIn('schema',self.codes())
    def test_missing_required_field(self):
        self.mutate(lambda d:d.pop('id'));self.assertIn('schema',self.codes())
    def test_duplicate_id(self):
        self.mutate(lambda d:d.update(id='recipe-0009'));self.assertIn('duplicate_id',self.codes())
    def test_duplicate_normalized_url(self):
        self.mutate(lambda d:d['source'].update(source_url='https://jetboil.johnsonoutdoors.com/us/recipes/french-toast/?tracking=x#top'))
        self.assertIn('duplicate_url',self.codes())
    def test_impostor_domain(self):
        self.mutate(lambda d:d['source'].update(source_url='https://jetboil.johnsonoutdoors.com.example.org/us/recipes/quinoa'))
        self.assertIn('official_domain',self.codes())
    def test_official_text_drift(self):
        self.mutate(lambda d:d['official_recipe']['ingredients_exact'].append('invented ingredient'))
        self.assertIn('audit_evidence',self.codes())
    def test_rendered_text_drift(self):
        d,body=read_recipe(self.path)
        self.path.write_text(self.path.read_text().replace('### Ingredients','### Changed ingredients'))
        self.assertIn('audit_evidence',self.codes())
    def test_card_text_drift(self):
        self.mutate(lambda d:d['recipe_card']['instructions'][0].update(text='invented step'))
        self.assertIn('audit_evidence',self.codes())
    def test_evidence_tampering(self):
        d,_=read_recipe(self.path);p=self.root/d['audit']['evidence_file'];p.write_text(p.read_text()+' ')
        self.assertIn('audit_evidence',self.codes())
    def test_evidence_path_escape(self):
        self.mutate(lambda d:d['audit'].update(evidence_file='../outside.json'))
        self.assertIn('audit_evidence',self.codes())
    def test_cached_cannot_claim_live(self):
        self.mutate(lambda d:d['audit'].update(status='verified_live'))
        self.assertIn('audit_evidence',self.codes())
    def test_unsupported_verified_flag(self):
        self.path=self.root/'01_Recipes/Breakfast/savory-oatmeal-bowl.md'
        self.mutate(lambda d:d['source'].update(source_verified=True))
        self.assertIn('unsupported_verified_claim',self.codes())
    def test_field_test_requires_evidence(self):
        self.mutate(lambda d:d['field_tested_variations']['entries'].append({'description':'tested'}))
        self.assertIn('schema',self.codes())
    def test_invalid_step_order(self):
        self.mutate(lambda d:d['recipe_card']['instructions'][0].update(step=3))
        self.assertIn('step_order',self.codes())
    def test_report_deterministic(self):
        records,issues=inspect(self.root)
        self.assertEqual(report_files(records,issues),report_files(records,issues))
        report=json.loads(report_files(records,issues)['08_Index/recipe-audit.json'])
        self.assertEqual(report['verified_count'],7);self.assertEqual(report['official_count'],33)
    def test_invalid_recipe_not_reported_verified(self):
        self.mutate(lambda d:d['official_recipe']['instructions_exact'].append('invented'))
        records,issues=inspect(self.root)
        report=json.loads(report_files(records,issues)['08_Index/recipe-audit.json'])
        self.assertEqual(report['verified_count'],6)
    def test_renderer_idempotent(self):
        d,body=read_recipe(self.path);text=synchronize(d,body);self.path.write_text(text)
        self.assertEqual(text,synchronize(*read_recipe(self.path)))
    def test_strict_provenance_exit_code(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/check_provenance.py'),'--root',str(self.root),'--strict'],capture_output=True)
        self.assertEqual(result.returncode,1)
    def test_report_check_detects_staleness(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/build_project_audit.py'),'--root',str(self.root),'--check'],capture_output=True)
        self.assertEqual(result.returncode,1);self.assertIn(b'STALE',result.stdout)
    def test_empty_collection_fails(self):
        shutil.rmtree(self.root/'01_Recipes');self.assertIn('empty_collection',self.codes())

class SourceCapture(unittest.TestCase):
    def test_challenge_is_not_recipe(self):
        with self.assertRaises(ValueError):extract('<html><h1>Security check</h1><p>Complete CAPTCHA</p></html>')
    def test_preserves_groups_inline_links_and_punctuation(self):
        html='<h1>Sample</h1><h4>Ingredients</h4><ul><li>1 cup <a>oats</a></li></ul><h4>Instructions</h4><p>The Night Before</p><ul><li>Soak.</li></ul><p>In the Morning</p><ol><li>Heat, then stir!</li></ol><h5>Featured Recommended Products</h5><ul><li>MiniMo</li></ul><div>Tagged Breakfast</div><ul><li>Ignore footer</li></ul>'
        d=extract(html);self.assertEqual(d['ingredients_exact'],['1 cup oats']);self.assertEqual(d['instructions_exact'],['Soak.','Heat, then stir!']);self.assertEqual(d['featured_products_exact'],['MiniMo']);self.assertEqual(d['instruction_groups'][1]['before_step'],2)
    def test_partial_page_fails(self):
        with self.assertRaises(ValueError):extract('<h1>Sample</h1><h4>Ingredients</h4><ul><li>oats</li></ul>')

if __name__=='__main__':unittest.main()
