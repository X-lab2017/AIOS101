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
assert sum(s['html'].count('textbook-diagram') for key in ('CH01', 'CH02', 'CH03', 'CH04', 'CH05', 'CH06') for s in data['units'][key]['sections']) == 31
assert len(data['worksheets']) == 4
print('PASS: canonical full text, stable sections, source digests, safe rendering, Mermaid fallbacks and internal appendix links')

# Figure delivery: exact IDs, portable Pages paths, reserved geometry and safe input.
from course_markdown import image_path
from html.parser import HTMLParser
class Images(HTMLParser):
    def __init__(self):
        super().__init__(); self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img': self.images.append(dict(attrs))
figures = json.loads((root/'textbook/assets/figures/manifest.json').read_text())
assert len(figures) == 44 and len({f['id'] for f in figures}) == 44
for ch, count in [('CH01', 4), ('CH02', 4), ('CH03', 8), ('CH04', 9), ('CH05', 9), ('CH06', 10)]:
    parser = Images()
    for sec in data['units'][ch]['sections']: parser.feed(sec['html'])
    assert len(parser.images) == count, ch
    for image in parser.images:
        assert image['alt'] and int(image['width']) > 0 and int(image['height']) > 0
        assert image['loading'] == 'lazy'
        assert (root/'dist'/image['src']).is_file()
    raw = (root/'dist/resources'/f'{ch}.md').read_text()
    assert raw.count('![图 ') == count and 'https://raw.githubusercontent.com/' in raw
for target in ['javascript:evil.webp', '//evil.test/a.webp', '../../../private.webp', '../assets/figures/../../private.webp', 'https://evil.test/a.webp']:
    assert image_path(target, source) is None
assert '<script>' not in render('<details onclick="evil()">\n<script>evil()</script>', source, commit, {})
assert sum(s['html'].count('<details class="figure-relations">') for ch in ('CH01','CH02','CH03','CH04','CH05','CH06') for s in data['units'][ch]['sections']) == 31
print('PASS: 44 registered images, dimensions, local assets, portable downloads, 31 folded fallbacks and unsafe image rejection')

# Decision-node labels and branches must survive the text fallback.
decision = render('```mermaid\nflowchart TD\n A["开始"] --> D{"继续？"}\n D -->|否| E["结束"]\n```', source, commit, {})
assert "继续？" in decision and "开始" in decision and "结束" in decision and "否" in decision

# Labeled dotted edges carry essential leakage and context-limit boundaries.
dotted = render('```mermaid\nflowchart LR\n X["近重复测试样本"] -. "不当泄漏" .-> T["训练集"]\n```', source, commit, {})
assert '<span class="diagram-label">不当泄漏</span>' in dotted
assert '<span class="diagram-node">近重复测试样本</span>' in dotted and '⇢' in dotted

# Every current figure gets a captioned zoom page. Main reading never loads SVGs.
import re
for f in figures:
    page = (root/'dist/figures'/ (f['id']+'.html')).read_text()
    assert f'data-width="{f["width"]}"' in page
    assert 'data-scale="fit"' in page and 'data-scale="2"' in page
    assert 'maximum-scale' not in page and 'user-scalable=no' not in page
    assert '<p class="figure-caption">图 '+f['id']+'　' in page
    if f.get('zoomFile'):
        assert '<svg' in page and (root/'dist/textbook/assets/figures'/f['zoomFile']).is_file()
    assert (root/'textbook/assets/figures'/f['file']).stat().st_size == f['bytes']
for ch in range(1,7):
    path = next((root/'textbook/chapters').glob(f'CH{ch:02}-*.md'))
    raw = path.read_text()
    blocks=re.findall(r'!\[图 (\d+-\d+)　[^\]]+\]\([^)]+\)[\s\S]*?<details>\n<summary>结构关系与 Mermaid 源码</summary>\n\n```mermaid\n([\s\S]*?)```',raw)
    # Match each block to the immediately preceding figure (real-material figures
    # between structural ones must not be associated with a later Mermaid block).
    for match in re.finditer(r'```mermaid\n([\s\S]*?)```',raw):
        number=re.findall(r'!\[图 (\d+-\d+)　',raw[:match.start()])[-1]
        assert match[1].strip() == (root/'textbook/assets/figures/mermaid'/f'Fig-{number}.mmd').read_text().strip(),number
    assert not any(old in raw for old in ['正式绘制可用','真实截图占位'])
assert (root/'dist/figure-fonts/figure-sans.woff').is_file()
print('PASS: 44 captioned zoom pages, source parity and labeled dotted edges')
