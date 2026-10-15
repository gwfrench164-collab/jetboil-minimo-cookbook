import json
import hashlib
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_all
from capture_jetboil_source import validate_url
from cookbook import report_files
from probe_sources import probe

class MaintenanceTests(unittest.TestCase):
    def test_url_rejects_non_recipe_redirects_and_impostors(self):
        for url in ['http://jetboil.johnsonoutdoors.com/us/recipes/x',
                    'https://jetboil.johnsonoutdoors.com/support',
                    'https://jetboil.johnsonoutdoors.com.evil.org/us/recipes/x',
                    'https://user@jetboil.johnsonoutdoors.com/us/recipes/x',
                    'https://jetboil.johnsonoutdoors.com:444/us/recipes/x']:
            with self.subTest(url=url), self.assertRaises(ValueError):validate_url(url)
        validate_url('https://jetboil.johnsonoutdoors.com/us/recipes/quinoa-breakfast-bowl')

    def test_http_200_challenge_is_retained_but_never_verified(self):
        class Response:
            url = 'https://jetboil.johnsonoutdoors.com/us/recipes/test'
            status = 200
            def __enter__(self):return self
            def __exit__(self, *args):pass
            def read(self, size):return b'<html><script src="/_Incapsula_Resource"></script></html>'
        with tempfile.TemporaryDirectory() as tmp, patch('probe_sources.urlopen', return_value=Response()):
            out=Path(tmp)/'attempt'
            result=probe(Response.url,out)
            self.assertEqual(result['outcome'],'unavailable')
            self.assertTrue((out/'response.html').exists())
            self.assertFalse((out/'candidate.json').exists())

    def test_reports_distinguish_cached_live_invalid_and_derived(self):
        def record(name, status, valid=True, source='official_jetboil_recipe'):
            return {'path':f'01_Recipes/{name}.md','verified':valid,'data':{'title':name,'source':{'type':source},'audit':{'status':status}}}
        rows=[record('Beverages/live','verified_live'),record('Breakfast/cached','verified_cached'),
              record('Breakfast/invalid','verified_live',False), record('Other/derived','pending',False,'derived_field_system')]
        files=report_files(rows,[])
        summary=json.loads(files['08_Index/recipe-audit.json'])
        self.assertEqual((summary['live_verified_count'],summary['indexed_only_count'],summary['live_pending_count']),(1,1,2))
        queue=files['08_Index/Recipe_Accuracy_Audit_Tracker.md'].split('## Live audit queue')[1].split('## Outstanding')[0]
        self.assertIn('Breakfast/cached',queue)
        self.assertIn('Breakfast/invalid',queue)
        self.assertNotIn('Beverages/live',queue)
        self.assertNotIn('Other/derived',queue)

    def test_runner_continues_after_failure_and_returns_failure(self):
        with patch('check_all.subprocess.run') as run, redirect_stdout(io.StringIO()):
            run.return_value.returncode=1
            self.assertEqual(check_all.main(),1)
            self.assertEqual(run.call_count,len(check_all.commands()))

    def test_retained_attempt_evidence_matches_checksums(self):
        root=Path(__file__).resolve().parents[1]
        for log in (root/'06_Source_Research/JetBoil/attempts').glob('*/attempts.json'):
            for row in json.loads(log.read_text()):
                if 'sha256' not in row:continue
                evidence=log.parent/Path(row['recipe']).stem/'response.html'
                self.assertEqual(hashlib.sha256(evidence.read_bytes()).hexdigest(),row['sha256'])

    def test_runner_success(self):
        with patch('check_all.subprocess.run') as run, redirect_stdout(io.StringIO()):
            run.return_value.returncode=0
            self.assertEqual(check_all.main(),0)
            self.assertTrue(all(c.args[0][0]==sys.executable for c in run.call_args_list))

if __name__=='__main__':unittest.main()
