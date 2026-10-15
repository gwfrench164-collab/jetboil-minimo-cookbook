#!/usr/bin/env python3
"""Opt-in live source candidates, breakfast first. Never modify recipe audit status."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from cookbook import ROOT, read_recipe
from capture_jetboil_source import extract, validate_url


def queue(root, category=None):
    rows = []
    for path in (root / '01_Recipes').rglob('*.md'):
        data, _ = read_recipe(path)
        if data.get('source', {}).get('type') != 'official_jetboil_recipe':
            continue
        group = path.relative_to(root / '01_Recipes').parts[0]
        if category and group != category:
            continue
        rows.append((group, path, data))
    return sorted(rows, key=lambda row: (row[0] != 'Breakfast', row[0], row[1].name))


def probe(url, directory):
    validate_url(url)
    with urlopen(Request(url, headers={'User-Agent': 'MiniMoCookbookSourceCheck/1.0'}), timeout=20) as response:
        validate_url(response.url)
        html = response.read(5_000_001)
        status = response.status
    if len(html) > 5_000_000:
        raise ValueError('Page too large')
    # Retain failed page bodies as evidence, too; HTTP 200 is not verification.
    directory.mkdir()
    (directory / 'response.html').write_bytes(html)
    evidence = {'http_status': status, 'sha256': hashlib.sha256(html).hexdigest()}
    try:
        official = extract(html)
    except ValueError as exc:
        return dict(evidence, outcome='unavailable', detail=str(exc))
    (directory / 'candidate.json').write_text(json.dumps({'source_url': url, 'official_recipe': official}, indent=2) + '\n')
    return dict(evidence, outcome='candidate_needs_review')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--category', help='Exact folder name, e.g. Breakfast')
    parser.add_argument('--output', type=Path, required=True, help='New directory for attempt log and responses')
    args = parser.parse_args()
    rows = queue(args.root, args.category)
    if not rows:
        parser.error('No official recipes matched; check category spelling')
    args.output.mkdir(parents=True, exist_ok=False)
    results = []
    for _, path, data in rows:
        url = data['source'].get('source_url')
        row = {'recipe': str(path.relative_to(args.root)), 'source_url': url,
               'attempted_at_utc': datetime.now(timezone.utc).isoformat()}
        if not url:
            row.update(outcome='missing_url', detail='Source URL discovery required; no URL guessed')
        else:
            try:
                row.update(probe(url, args.output / path.stem))
            except Exception as exc:
                row.update(outcome='unavailable', detail=str(exc))
        results.append(row)
        (args.output / 'attempts.json').write_text(json.dumps(results, indent=2) + '\n')
        print(row['recipe'] + ': ' + row['outcome'], flush=True)
    return int(any(row['outcome'] != 'candidate_needs_review' for row in results))

if __name__ == '__main__':
    raise SystemExit(main())
