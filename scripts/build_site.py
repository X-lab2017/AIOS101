#!/usr/bin/env python3
"""Build the learning companion from canonical Markdown. Standard library only."""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from course_markdown import unit, destination, image_path
from figure_pages import build_figure_pages

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'dist'
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(ROOT/'site', OUT)
shutil.copytree(ROOT/'textbook/assets/figures', OUT/'textbook/assets/figures')
commit = os.environ.get('GITHUB_SHA') or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
if not re.fullmatch(r'[0-9a-f]{40}', commit): raise SystemExit('Invalid source commit')
# Keep content and styles on the same release even when a reader has cached an older visit.
index = (OUT/'index.html').read_text()
index = re.sub(r'((?:src|href)="[^"?]+\.(?:js|css))"', lambda m: m[1]+'?v='+commit+'"', index)
(OUT/'index.html').write_text(index)
app = (OUT/'app.js').read_text().replace("fetch('content.json')", "fetch('content.json?v="+commit+"')")
(OUT/'app.js').write_text(app)
course = (ROOT/'specs/course-spec.md').read_text()
constitution = (ROOT/'CONSTITUTION.md').read_text()
rows = re.findall(r'^\| (CH\d\d) \| (.*?) \| (.*?) \| (.*?) \|$', course, re.M)
if [r[0] for r in rows] != [f'CH{i:02d}' for i in range(1,13)]: raise SystemExit('Invalid chapter matrix')
questions = re.findall(r'^\| 第 \d+ 章 \| .*? \| (.*?) \| .*? \|$', constitution, re.M)
english = ['Why AI and open source literacy?', 'Openness, reuse and collaboration', 'The AI open source ecosystem', 'From data to models', 'Inference, systems and evaluation', 'Retrieval, tools and agents', 'How open is a model?', 'From public to reproducible', 'Investigating ecosystems with data', 'From participation to contribution', 'Creating responsibly with open AI', 'Projects, review and continued contribution']
paths = {'PREFACE':ROOT/'textbook/preface.md','APP-A':ROOT/'textbook/appendices/APP-A-repository-snapshots.md'}
chapters = []
for i,r in enumerate(rows):
    c = dict(id=r[0],title=r[1],en=english[i],part=i//3,outcomes=r[2],evidence=r[3],question=questions[i],status='planned',worksheets=[])
    found = list((ROOT/'textbook/chapters').glob(c['id']+'-*.md'))
    if len(found)>1: raise SystemExit('Ambiguous source '+c['id'])
    if found:
        paths[c['id']] = found[0]; c['status']='available'; c['sourceStatus']='draft'; c['sourcePath']=found[0].relative_to(ROOT).as_posix()
    for p in sorted((ROOT/'activities/student').glob('ACT-'+c['id']+'-*.md')):
        c['worksheets'].append({'id':p.stem,'title':p.read_text().splitlines()[0].removeprefix('# 学生任务单：'),'path':p.relative_to(ROOT).as_posix()})
    chapters.append(c)
routes = {p.relative_to(ROOT).as_posix():key for key,p in paths.items()}
units = {key:unit(p,ROOT,commit,routes,key) for key,p in paths.items()}
for c in chapters:
    if c['id'] in units:c['sourceVersion']=units[c['id']]['version']
worksheets = {}
for p in sorted((ROOT/'activities/student').glob('ACT-CH0[12]-*.md')):
    worksheets[p.stem] = {'path':p.relative_to(ROOT).as_posix(),'markdown':p.read_text()}
glossary = []
for key,u in units.items():
    for sec in u['sections']:
        if sec['title']=='关键术语':
            for term,meaning in re.findall(r'^- \*\*(.+?)\*\*：(.+)$',sec['markdown'],re.M):glossary.append({'term':term,'meaning':meaning,'unit':key,'section':sec['id']})
figure_records=json.loads((ROOT/'textbook/assets/figures/manifest.json').read_text())
content = dict(figureCount=len(figure_records),version='0.7.0-self-study',date='2026-10-29',sourceCommit=commit,visualVersion='1.0.0',brandCommit='373d61f0d6e334f0b85af0dd5d8ef9b9095bcc37',chapters=chapters,units=units,worksheets=worksheets,glossary=glossary,preface=units['PREFACE']['markdown'],sources=(ROOT/'specs/source-register.md').read_text())
(OUT/'content.json').write_text(json.dumps(content,ensure_ascii=False),encoding='utf-8')
(OUT/'resources').mkdir()
resources = [(u['sourcePath'],key+'.md') for key,u in units.items()] + [(v['path'],key+'.md') for key,v in worksheets.items()] + [('specs/'+x+'.md',x+'.md') for x in ['website-spec','website-activities','learning-experience-spec','course-identity-spec','source-register']]
for path,name in resources:
    raw = (ROOT/path).read_text()
    # Downloads point to the matching source commit, independent of local app routes.
    def download_link(m):
        image = image_path(m[3], path) if m[1] else None
        url = 'https://raw.githubusercontent.com/X-lab2017/AIOS101/'+commit+'/'+image if image else destination(m[3],path,commit,{})
        return m[1]+'['+m[2]+']('+url+')'
    raw = re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)', download_link, raw)
    (OUT/'resources'/name).write_text(raw,encoding='utf-8')
# Historical download path remains valid; Windows treats these names as one file.
legacy_preface = OUT/'resources/preface.md'
if not legacy_preface.exists() or not os.path.samefile(OUT/'resources/PREFACE.md', legacy_preface):
    shutil.copyfile(OUT/'resources/PREFACE.md', legacy_preface)
(OUT/'.nojekyll').write_text('')
build_figure_pages(ROOT, OUT, commit)
print(f'Built {len(units)} complete reading units, {len(worksheets)} worksheets and {len(chapters)} course chapters')
