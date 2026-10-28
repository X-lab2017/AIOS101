"""Build quiet, directly linkable large-figure readers from the canonical captions."""
import html
import json
import re
from pathlib import Path
from course_markdown import inline

def build_figure_pages(root, out, commit):
    folder=out/'figures'; folder.mkdir(exist_ok=True)
    records=json.loads((root/'textbook/assets/figures/manifest.json').read_text())
    for record in records:
        number=record['id']; chapter='CH'+number.split('-')[0].zfill(2)
        path=next((root/'textbook/chapters').glob(chapter+'-*.md'))
        caption=re.search(r'^图 '+re.escape(number)+r'　(.+)$',path.read_text(),re.M)
        if not caption: raise ValueError('Missing figure caption '+number)
        title='图 '+number+'　'+record['title']
        source=path.relative_to(root).as_posix()
        image_path='textbook/assets/figures/'+record['file']
        vector=record.get('zoomFile')
        if vector:
            svg=(root/'textbook/assets/figures'/vector).read_text()
            # Only curated, self-contained repository SVGs are included inline.
            if re.search(r'<script|<foreignObject|\bon\w+\s*=|(?:href|url)=["\']https?:',svg,re.I):
                raise ValueError('Non-local SVG content '+vector)
            svg=re.sub(r'<\?xml[^>]*>|<!DOCTYPE[^>]*>', '',svg)
            media=svg
        else:
            media='<img src="../'+image_path+'" alt="'+html.escape(record.get('alt',title),quote=True)+'" width="'+str(record['width'])+'" height="'+str(record['height'])+'">'
        page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+html.escape(title)+''' · AIOS101</title>
<link rel="stylesheet" href="../figure-viewer.css?v='''+commit+'''"></head><body>
<header><a href="../#/learn/'''+chapter+'''">← 返回第'''+number.split('-')[0]+'''章</a><span>AIOS101 · X-lab</span></header>
<main><h1>'''+html.escape(title)+'''</h1><div class="figure-controls" role="group" aria-label="图片缩放">
<button type="button" data-scale="fit" aria-pressed="true">适应屏幕</button>
<button type="button" data-scale="1" aria-pressed="false">原尺寸</button>
<button type="button" data-scale="2" aria-pressed="false">放大 2 倍</button>
<span id="zoom-status" role="status">适应屏幕</span></div>
<p class="view-hint">放大后可在图内横向、纵向滑动。'''+('此图使用矢量文字。' if vector else '此图保留原图像素；密集材料可结合下方来源核对。')+'''</p>
<div class="figure-stage" tabindex="0" role="region" aria-label="可滚动的大图" data-width="'''+str(record['width'])+'''">'''+media+'''</div>
<p class="figure-caption">图 '''+number+'　'+inline(caption[1],source,commit,{})+'''</p>
<p class="figure-download"><a href="../'''+image_path+'''" download>下载 WebP</a>'''+(' · <a href="../textbook/assets/figures/'+vector+'" download>下载 SVG</a>' if vector else '')+'''</p>
</main><script src="../figure-viewer.js?v='''+commit+'''"></script></body></html>'''
        (folder/(number+'.html')).write_text(page)
    print(f'Built {len(records)} captioned large-figure pages')
