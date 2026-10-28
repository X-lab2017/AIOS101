#!/usr/bin/env python3
"""Check the built course contract and relative assets before a Pages deploy."""
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
data = json.loads((OUT/'content.json').read_text())
assert [c['id'] for c in data['chapters']] == [f'CH{i:02d}' for i in range(1, 13)]
assert data['preface'] == (ROOT/'textbook/preface.md').read_text(), 'Preface differs from canonical source'
assert re.fullmatch(r'[0-9a-f]{40}', data['sourceCommit'])
for chapter in data['chapters']:
    if 'sourcePath' in chapter:
        assert (ROOT/chapter['sourcePath']).is_file(), chapter['id']
        assert chapter['sourceStatus'] == 'draft', 'Source existence must not imply approval'
        for item in chapter['worksheets']:
            assert item['id'].startswith('ACT-'+chapter['id']+'-')
            assert (ROOT/item['path']).is_file(), item['path']

# Resolve literal references as if hosted under a repository subpath.
base = 'https://example.test/AIOS101/'
checked = set()
for filename in ['index.html', 'styles.css', 'brand.css', 'app.js', 'brand.js']:
    text = (OUT/filename).read_text()
    refs = re.findall(r'''(?:src|href)=["']([^"']+)["']''', text)
    refs += re.findall(r'''url\(["']?([^)'"\s]+)''', text)
    for ref in refs:
        if '${' in ref or ref.startswith(('#', 'https:', 'http:', 'data:', 'mailto:')):
            continue
        url = urlparse(urljoin(base+filename, ref))
        assert url.path.startswith('/AIOS101/'), f'Resource escapes Pages subpath: {ref}'
        path = OUT/unquote(url.path.removeprefix('/AIOS101/'))
        assert path.is_file(), f'Missing resource: {filename} -> {ref}'
        checked.add(path)
for theme in ['light', 'dark']:
    for path in [f'assets/logo-{theme}.svg', f'assets/full-logo-{theme}.svg', f'assets/course/logo-{theme}.svg', f'assets/course/mark-{theme}.svg']:
        assert (OUT/path).is_file(), path
with zipfile.ZipFile(OUT/'assets/course/aios101-identity-kit-v0.1.zip') as archive:
    assert archive.testzip() is None, 'Corrupt identity asset package'
assert (OUT/'.nojekyll').is_file()
print(f'PASS: 12 chapter IDs, canonical preface, draft sources, {len(checked)} static references, theme assets and ZIP')
