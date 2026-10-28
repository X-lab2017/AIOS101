"""Security and fidelity checks for the textbook renderer, no dependencies."""
import hashlib
import json
from pathlib import Path
from course_markdown import destination, render, section_id

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'dist/content.json').read_text())
assert set(data['units']) >= {'PREFACE', 'CH01', 'CH02', 'APP-A'}
for key, unit in data['units'].items():
    raw = (root / unit['sourcePath']).read_text()
    assert unit['markdown'] == raw, key
    assert unit['digest'] == hashlib.sha256(raw.encode()).hexdigest()
    assert len({s['id'] for s in unit['sections']}) == len(unit['sections'])
    for section in unit['sections']:
        assert section['markdown'] and section['html']
        assert section['id'] == 'opening' or section['id'] == section_id(section['title'])
    assert (root / 'dist/resources' / (key + '.md')).is_file()
commit = data['sourceCommit']
source = 'textbook/chapters/CH01-why-ai-open-source-literacy.md'
routes = {'textbook/appendices/APP-A-repository-snapshots.md': 'APP-A'}
assert destination('../appendices/APP-A-repository-snapshots.md', source, commit, routes) == '#/learn/APP-A'
for url in ['javascript:alert(1)', 'data:text/html,payload', '//untrusted.test']:
    assert destination(url, source, commit, {}) == '#'
rendered = render('<script>alert(1)</script>\n\n[x](javascript:evil)\n\n| 列 |\n|---|\n| **证据** |', source, commit, {})
assert '<script>' not in rendered and 'href="javascript:' not in rendered
assert '<th scope="col">列</th>' in rendered and '<strong>证据</strong>' in rendered
assert '&lt;script&gt;' in rendered
assert '#/learn/APP-A' in ''.join(s['html'] for s in data['units']['CH01']['sections'])
assert len(data['worksheets']) == 4
print('PASS: canonical full text, stable sections, source digests, safe rendering and internal appendix links')
