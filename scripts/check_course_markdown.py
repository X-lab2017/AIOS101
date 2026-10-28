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
mermaid = render('```mermaid\nflowchart LR\n A["开放"] -->|仍需文档| B["复用"]\n C["协作"] -.-> B\n```', source, commit, {})
assert 'textbook-diagram' in mermaid and '开放' in mermaid and '复用' in mermaid
assert '仍需文档' in mermaid and '→' in mermaid and '⇢' in mermaid
assert '<summary>查看 Mermaid 图源码</summary>' in mermaid
unsafe_mermaid = render('```mermaid\nflowchart LR\n A["<img src=x>"] --> B["结果"]\n```', source, commit, {})
assert '<img src=x>' not in unsafe_mermaid and '&lt;img src=x&gt;' in unsafe_mermaid
assert '#/learn/APP-A' in ''.join(s['html'] for s in data['units']['CH01']['sections'])
assert sum(s['html'].count('textbook-diagram') for key in ('CH01', 'CH02', 'CH03', 'CH04', 'CH05') for s in data['units'][key]['sections']) == 17
assert len(data['worksheets']) == 4
print('PASS: canonical full text, stable sections, source digests, safe rendering, Mermaid fallbacks and internal appendix links')
