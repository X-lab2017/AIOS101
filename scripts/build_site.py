#!/usr/bin/env python3
"""Build the static review site from canonical course sources; standard library only."""
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
if OUT.exists():
    for child in OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
shutil.copytree(ROOT / 'site', OUT, dirs_exist_ok=True)
course = (ROOT / 'specs/course-spec.md').read_text()
constitution = (ROOT / 'CONSTITUTION.md').read_text()
rows = re.findall(r'^\| (CH\d\d) \| (.*?) \| (.*?) \| (.*?) \|$', course, re.M)
if [r[0] for r in rows] != [f'CH{i:02d}' for i in range(1, 13)]:
    raise SystemExit('Invalid course chapter matrix')
questions = re.findall(r'^\| 第 \d+ 章 \| .*? \| (.*?) \| .*? \|$', constitution, re.M)
english = ['Why AI and open source literacy?', 'Openness, reuse and collaboration', 'The AI open source ecosystem', 'From data to models', 'Inference, systems and evaluation', 'Retrieval, tools and agents', 'How open is a model?', 'From public to reproducible', 'Investigating ecosystems with data', 'From participation to contribution', 'Creating responsibly with open AI', 'Projects, review and continued contribution']
chapters = [dict(id=r[0], title=r[1], en=english[i], part=i//3, outcomes=r[2], evidence=r[3], question=questions[i], status='planned') for i,r in enumerate(rows)]
for chapter in chapters:
    sources = list((ROOT/'textbook/chapters').glob(chapter['id']+'-*.md'))
    if len(sources) > 1:
        raise SystemExit('Ambiguous canonical source for '+chapter['id'])
    if sources:
        chapter['sourcePath'] = sources[0].relative_to(ROOT).as_posix()
        chapter['sourceStatus'] = 'draft'
        version = re.search(r'^> 版本：(.*)$', sources[0].read_text(), re.M)
        chapter['sourceVersion'] = version.group(1).strip() if version else ''
        chapter['worksheets'] = []
        for worksheet in sorted((ROOT/'activities/student').glob('ACT-'+chapter['id']+'-*.md')):
            title = worksheet.read_text().splitlines()[0].removeprefix('# 学生任务单：')
            chapter['worksheets'].append(dict(id=worksheet.stem, path=worksheet.relative_to(ROOT).as_posix(), title=title))
source_commit = os.environ.get('GITHUB_SHA', '63c4f86e7e963a2cc7a36127707b126a92f37b1c')
if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
    raise SystemExit('Invalid source commit')
content = dict(version='0.3.0-preview', date='2026-10-28', sourceCommit=source_commit, brandCommit='373d61f0d6e334f0b85af0dd5d8ef9b9095bcc37', chapters=chapters, preface=(ROOT/'textbook/preface.md').read_text(), sources=(ROOT/'specs/source-register.md').read_text(), websiteSpec=(ROOT/'specs/website-spec.md').read_text(), activitySpec=(ROOT/'specs/website-activities.md').read_text())
(OUT/'content.json').write_text(json.dumps(content, ensure_ascii=False))
(OUT/'resources').mkdir()
for src, name in [('specs/website-spec.md','website-spec.md'),('specs/website-activities.md','website-activities.md'),('textbook/preface.md','preface.md'),('specs/course-identity-spec.md','course-identity-spec.md')]:
    text = (ROOT/src).read_text()
    def public_link(match):
        label, target = match.groups()
        if '://' in target or target.startswith('#'):
            return match.group(0)
        resolved = (ROOT/src).parent.joinpath(target).resolve().relative_to(ROOT)
        url = 'https://github.com/X-lab2017/AIOS101/blob/main/' + quote(resolved.as_posix())
        return f'[{label}]({url})'
    (OUT/'resources'/name).write_text(re.sub(r'\[([^\]]+)\]\(([^)]+)\)', public_link, text))
(OUT/'.nojekyll').write_text('')
print(f'Built {len(chapters)} planned chapters, full preface and 3 review specifications into {OUT}')
