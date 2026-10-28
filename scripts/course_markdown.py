"""Small, escaped Markdown renderer for the repository's textbook subset."""
import hashlib
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import quote, urlsplit


def section_id(title):
    return 's-' + hashlib.sha1(title.encode()).hexdigest()[:10]


def destination(target, source, commit, routes):
    target = html.unescape(target.strip())
    if target.startswith('#'):
        return target
    parsed = urlsplit(target)
    if parsed.scheme:
        return target if parsed.scheme in ('http', 'https', 'mailto') else '#'
    if target.startswith('//'):
        return '#'
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), parsed.path))
    if path in routes:
        return '#/learn/' + routes[path]
    if path.startswith('../'):
        return '#'
    return 'https://github.com/X-lab2017/AIOS101/blob/' + commit + '/' + quote(path) + ('#' + parsed.fragment if parsed.fragment else '')


def inline(text, source, commit, routes):
    tokens = []
    def hold(value):
        tokens.append(value)
        return '\x00' + str(len(tokens)-1) + '\x00'
    text = re.sub(r'`([^`]+)`', lambda m: hold('<code>' + html.escape(m[1]) + '</code>'), text)
    def link(m):
        url = destination(m[2], source, commit, routes)
        label = html.escape(m[1])
        attrs = ' target="_blank" rel="noopener noreferrer"' if url.startswith(('http:', 'https:')) else ''
        return hold('<a href="' + html.escape(url, quote=True) + '"' + attrs + '>' + label + '</a>')
    text = re.sub(r'!?\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    for i, value in enumerate(tokens):
        text = text.replace('\x00' + str(i) + '\x00', value)
    return text


def image_path(target, source):
    """Only repository-owned raster figures may be embedded in the reader."""
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return None
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), parsed.path))
    if path.startswith('textbook/assets/figures/') and path.endswith('.webp'):
        return path
    return None


def figure_image(label, target, source):
    path = image_path(target, source)
    if not path:
        return '<p>' + html.escape(label) + '</p>'
    root = Path(__file__).resolve().parents[1]
    records = json.loads((root/'textbook/assets/figures/manifest.json').read_text())
    record = next((r for r in records if r['file'] == posixpath.basename(path)), None)
    if not record or not (root/path).is_file():
        raise ValueError('Unregistered or missing figure: ' + path)
    url = html.escape(quote(path), quote=True)
    viewer = 'figures/' + record['id'] + '.html'
    alt = html.escape('图 '+record['id']+'　'+record['title']+'。'+record.get('alt', ''), quote=True)
    display_width = max(520, min(920, int(record.get('displayWidth', 780))))
    return ('<figure class="textbook-figure" id="fig-' + record['id'] + '" style="max-width:' + str(display_width) + 'px"><a class="figure-open" href="' + viewer +
            '" target="_blank" rel="noopener noreferrer" aria-label="' + alt + ' · 查看大图 / Open full size">' +
            '<img src="' + url + '" alt="' + alt + '" width="' + str(record['width']) +
            '" height="' + str(record['height']) + '" loading="lazy" decoding="async"></a>' +
            '<figcaption><a href="' + viewer + '" target="_blank" rel="noopener noreferrer">放大查看 ↗</a></figcaption></figure>')


def mermaid_block(code):
    """Render the textbook's simple node/edge subset as an accessible fallback."""
    nodes = {}; edges = []
    for raw in code.splitlines():
        line = raw.strip()
        # Mermaid permits labels between the two halves of a dotted arrow.
        # Normalize that form so the accessible relationship list keeps the edge.
        line = re.sub(r'-\.\s*"([^"]*)"\s*\.->', r'-.->|\1|', line)
        node = re.fullmatch(r'([A-Za-z]\w*)\s*[\[{]"([^"]*)"[\]}]', line)
        if node:
            nodes[node[1]] = node[2]; continue
        edge = re.fullmatch(r'([A-Za-z]\w*)(?:[\[{]"([^"]*)"[\]}])?\s*(-\.->|---|-->)\s*(?:\|([^|]*)\|\s*)?([A-Za-z]\w*)(?:[\[{]"([^"]*)"[\]}])?', line)
        if edge:
            if edge[2]: nodes[edge[1]] = edge[2]
            if edge[6]: nodes[edge[5]] = edge[6]
            edges.append((edge[1], edge[5], edge[3], edge[4] or ''))
    if not edges:
        return '<pre><code>' + html.escape(code) + '</code></pre>'
    relations = []
    for start, end, arrow, label in edges:
        symbol = {'-.->': '⇢', '---': '—'}.get(arrow, '→')
        relation = '<span class="diagram-arrow">' + symbol + '</span>'
        if label:
            relation += '<span class="diagram-label">' + html.escape(label) + '</span>'
        relations.append('<li><span class="diagram-node">' + html.escape(nodes.get(start, start)) + '</span>' + relation + '<span class="diagram-node">' + html.escape(nodes.get(end, end)) + '</span></li>')
    source = html.escape(code)
    return '<div class="textbook-diagram" role="group" aria-label="结构关系图"><ul class="diagram-relations">' + ''.join(relations) + '</ul><details class="diagram-source"><summary>查看 Mermaid 图源码</summary><pre><code>' + source + '</code></pre></details></div>'


def render(text, source, commit, routes):
    lines = text.splitlines(); result = []; i = 0
    fmt = lambda value: inline(value, source, commit, routes)
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line == '<details>' and i+1 < len(lines) and lines[i+1].strip() == '<summary>结构关系与 Mermaid 源码</summary>':
            block = []; i += 2
            while i < len(lines) and lines[i].strip() != '</details>':
                block.append(lines[i]); i += 1
            result.append('<details class="figure-relations"><summary>结构关系与 Mermaid 源码</summary>' + render('\n'.join(block), source, commit, routes) + '</details>')
            i += 1; continue
        picture = re.fullmatch(r'!\[([^\]]+)\]\(([^)]+)\)', line)
        if picture:
            result.append(figure_image(picture[1], picture[2], source)); i += 1; continue
        if line.startswith('```'):
            language = line[3:].strip().lower(); code = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            source_code = '\n'.join(code)
            result.append(mermaid_block(source_code) if language == 'mermaid' else '<pre><code>' + html.escape(source_code) + '</code></pre>'); i += 1; continue
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            level = min(6, max(2, len(heading[1])))
            result.append(f'<h{level}>' + fmt(heading[2]) + f'</h{level}>'); i += 1; continue
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i+1]):
            cells = lambda row: [fmt(x.strip()) for x in row.strip().strip('|').split('|')]
            header = cells(line); i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i])); i += 1
            result.append('<div class="reading-table" tabindex="0" role="region" aria-label="可横向滚动的表格 / Scrollable table"><table><thead><tr>' + ''.join('<th scope="col">'+x+'</th>' for x in header) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'); continue
        if line.startswith('>'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                block.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            result.append('<blockquote>'+render('\n'.join(block), source, commit, routes)+'</blockquote>'); continue
        match = re.match(r'^(?:([-*])|(\d+)\.)\s+(.+)', line)
        if match:
            ordered = bool(match[2]); tag = 'ol' if ordered else 'ul'; items = []
            while i < len(lines):
                item = re.match(r'^(?:([-*])|(\d+)\.)\s+(.+)', lines[i].strip())
                if not item or bool(item[2]) != ordered: break
                items.append('<li>'+fmt(item[3])+'</li>'); i += 1
            result.append('<'+tag+'>'+''.join(items)+'</'+tag+'>'); continue
        if re.fullmatch(r'[-*_]{3,}', line):
            result.append('<hr>'); i += 1; continue
        paragraph = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,6} |>|\||[-*] |\d+\. |```)', lines[i].strip()):
            paragraph.append(lines[i].strip()); i += 1
        # Canonical captions use an ideographic space after the figure ID.
        # A prose paragraph such as “图 0-4 展示……” is ordinary body text.
        cls = ' class="figure-caption"' if re.match(r'^图 \d+-\d+　', line) else ''
        result.append('<p'+cls+'>'+fmt('\n'.join(paragraph))+'</p>')
    return '\n'.join(result)


def unit(path, root, commit, routes, unit_id):
    raw = path.read_text(encoding='utf-8'); relative = path.relative_to(root).as_posix()
    title = raw.splitlines()[0].removeprefix('# ').strip()
    version = re.search(r'^> 版本：(.+)', raw, re.M)
    status = re.search(r'^> 状态：(.+)', raw, re.M)
    body = re.sub(r'^# .+\n(?:\s*\n|>[^\n]*\n)*', '', raw, count=1)
    chunks = re.split(r'^## (.+)\n', body, flags=re.M)
    sections = []
    if chunks[0].strip(): sections.append({'title':'从这里开始', 'id':'opening', 'markdown':chunks[0].strip()})
    for i in range(1, len(chunks), 2):
        sections.append({'title':chunks[i].strip(),'id':section_id(chunks[i].strip()),'markdown':chunks[i+1].strip()})
    for section in sections:
        section['html'] = render(section['markdown'], relative, commit, routes)
    return {'id':unit_id,'title':title,'version':version[1].strip() if version else '', 'status':status[1].strip() if status else '阅读支架', 'sourcePath':relative, 'digest':hashlib.sha256(raw.encode()).hexdigest(),'markdown':raw,'sections':sections, 'minutes':max(3,round(len(re.sub(r'\s+', '', body))/350))}
