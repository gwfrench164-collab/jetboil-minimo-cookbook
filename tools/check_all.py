#!/usr/bin/env python3
"""Run all offline checks with the current Python environment; never rewrite outputs."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def commands():
    return [
        ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['tools/validate_recipes.py', '--baseline', 'tools/audit_backlog.json'],
        ['tools/check_provenance.py', '--baseline', 'tools/audit_backlog.json'],
        ['tools/render_recipes.py'],
        ['tools/build_project_audit.py', '--check'],
        ['tools/build_database.py', '--check'],
    ]

def main():
    failed = []
    for args in commands():
        print('\nChecking: ' + ' '.join(args), flush=True)
        if subprocess.run([sys.executable, *args], cwd=ROOT).returncode:
            failed.append(' '.join(args))
    print('\n' + ('FAILED: ' + '; '.join(failed) if failed else 'All offline checks passed.'))
    return int(bool(failed))

if __name__ == '__main__':
    raise SystemExit(main())
