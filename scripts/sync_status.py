#!/usr/bin/env python3
"""Derive the handoff's version/figure table from canonical repository inputs."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BEGIN GENERATED BASELINE -->'
END = '<!-- END GENERATED BASELINE -->'


def baseline():
    figures = json.loads((ROOT/'textbook/assets/figures/manifest.json').read_text())
    paths = [('PREFACE', 'textbook/preface.md', '0')]
    for n in range(1, 13):
        matches = sorted((ROOT/'textbook/chapters').glob(f'CH{n:02}-*.md'))
        if len(matches) > 1:
            raise ValueError(f'Multiple canonical files: CH{n:02}')
        if matches:
            paths.append((f'CH{n:02}', matches[0].relative_to(ROOT).as_posix(), str(n)))
    paths.append(('APP-A', 'textbook/appendices/APP-A-repository-snapshots.md', 'A'))
    lines = [START, '', '## 正本版本与图版（自动核对）', '',
             '| 单元 | 正文版本 | 当前图数 | 唯一正本 |', '|---|---|---|---|']
    for label, path, prefix in paths:
        raw = (ROOT/path).read_text()
        version = re.search(r'^> 版本：(.+)$', raw, re.M)
        if not version:
            raise ValueError('Missing source version: '+path)
        count = sum(f['id'].split('-')[0] == prefix for f in figures)
        lines.append(f'| {label} | {version[1].strip()} | {count} | [{Path(path).name}](../{path}) |')
    mermaid = sum((ROOT/path).read_text().count('```mermaid') for _, path, _ in paths)
    vectors = sum(bool(f.get('zoomFile')) for f in figures)
    lines += ['', f'合计 **{len(paths)} 个阅读单元、{len(figures)} 幅正文图、{vectors} 幅 SVG 放大版、{mermaid} 份折叠 Mermaid 源码**。', '', END]
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    path = ROOT/'docs/STATUS.md'
    raw = path.read_text()
    if raw.count(START) != 1 or raw.count(END) != 1:
        raise SystemExit('Missing or duplicate baseline markers')
    expected = re.sub(re.escape(START)+r'.*?'+re.escape(END), lambda _: baseline(), raw, flags=re.S)
    if args.write:
        path.write_text(expected)
    elif raw != expected:
        raise SystemExit('Handoff baseline is stale; run python scripts/sync_status.py --write')
    print('PASS: handoff versions and figure counts match canonical sources')
