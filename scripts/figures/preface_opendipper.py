#!/usr/bin/env python3
"""Native evidence mounting: retain screenshot pixels, add hand-drawn surround."""
import argparse, base64, hashlib, html, io, json
from pathlib import Path
import cairosvg
from PIL import Image, ImageChops
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[2]
F=ROOT/'textbook/assets/figures'
S=F/'sources'
p=argparse.ArgumentParser()
p.add_argument('--global-screenshot',required=True)
p.add_argument('--galaxy-screenshot',required=True)
p.add_argument('--global-mount',required=True)
p.add_argument('--galaxy-mount',required=True)
p.add_argument('--font',required=True)
p.add_argument('--qa-dir',required=True)
args=p.parse_args()
font=TTFont(args.font); glyphs=font.getGlyphSet(); cmap=font.getBestCmap()

def text(value,x,y,size,color='#1D2433'):
    cursor=0; parts=[]; scale=size/font['head'].unitsPerEm
    for ch in value:
        assert ord(ch) in cmap,ch
        name=cmap[ord(ch)]; pen=SVGPathPen(glyphs); glyphs[name].draw(pen)
        parts.append(f'<path d="{pen.getCommands()}" transform="translate({cursor} 0)"/>')
        cursor+=glyphs[name].width
    return f'<g aria-label="{html.escape(value,quote=True)}" fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">'+''.join(parts)+'</g>'

def uri(path):return 'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode()

sha='dcfcb8367ed8d883613e854cc36cd3c718e94df5'
records=[]; provenance=[]
for number,key,title,original,mount,box,steps in [
 ('0-4','global','OpenDipper 全球观测：从分布追问口径',args.global_screenshot,args.global_mount,(92,174,1816),[
  ('① 选对象','先看图层与统计对象'),('② 读分布','再看地图、气泡与图例'),('③ 查口径','核对时间、来源和模拟标记')]),
 ('0-5','galaxy','OpenDipper 开源星系：从连线追问证据',args.galaxy_screenshot,args.galaxy_mount,(162,208,1708),[
  ('① 认对象','节点代表哪类对象？'),('② 问关系','关系来自哪条记录？'),('③ 留边界','连线不自动等于依赖')])
]:
    original=Path(original); mount=Path(mount)
    source=S/f'OpenDipper_{key}_user-snapshot_2026-10-29.webp'
    frame=S/f'OpenDipper_{key}_handdrawn-mount_v01.webp'
    raw=Image.open(original).convert('RGB')
    raw.save(source,'WEBP',lossless=True,method=6)
    assert ImageChops.difference(raw,Image.open(source).convert('RGB')).getbbox() is None
    Image.open(mount).convert('RGB').save(frame,'WEBP',quality=86,method=6)
    x,y,w=box; h=raw.height*w/raw.width
    body=[f'<image x="0" y="0" width="2000" height="1660" preserveAspectRatio="none" href="{uri(frame)}"/>',
          text(f'图 {number}　{title}',100,95,43),
          f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{uri(source)}"/>']
    for i,(heading,explanation) in enumerate(steps):
        left=[265,800,1330][i]
        body += [text(heading,left,1425,36),
                 f'<path d="M{left} 1441 Q{left+85} 1436 {left+170} 1440" fill="none" stroke="{["#5146D9","#3F958D","#F27A59"][i]}" stroke-width="4"/>',
                 text(explanation,left,1494,26,'#4B5360')]
    body.append(text('真实界面截图 · 手绘装帧导读',655,1584,24,'#656577'))
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1660" viewBox="0 0 2000 1660" role="img"><title>'+html.escape(f'图 {number}　{title}')+'</title>'+''.join(body)+'</svg>\n'
    stem=f'AIOS101_Fig-00-0{number[-1]}_opendipper-{key}_v01'
    (F/(stem+'.svg')).write_text(svg)
    rendered=cairosvg.svg2png(bytestring=svg.encode(),output_width=2000,output_height=1660)
    webp=F/(stem+'.webp')
    Image.open(io.BytesIO(rendered)).convert('RGB').save(webp,'WEBP',quality=92,method=6)
    qa=Path(args.qa_dir);qa.mkdir(parents=True,exist_ok=True)
    (qa/f'preface-{number}.png').write_bytes(rendered)
    records.append(dict(id=number,title=title,file=webp.name,width=2000,height=1660,bytes=webp.stat().st_size,
        originalBytes=original.stat().st_size,insertion='序言 / 从全球地图与开源星系，学习观察与判断',
        alt=('OpenDipper 全球观测真实界面：左侧选择对象图层，中间查看地图和图例，右侧核对指标、来源与观察期。原图的模拟标签保留；外围为手绘装帧。' if key=='global' else 'OpenDipper 开源星系真实界面：左侧是开源软件仓库网络，右侧是模型、数据等对象的网络。导读提示辨认节点类型、核对关系记录并保留结论边界；外围为手绘装帧。'),
        displayWidth=920,sourceUrls=['https://www.x-lab.info/open-dipper/'+('#ecosystem' if key=='galaxy' else ''),f'https://github.com/X-lab2017/open-dipper/blob/{sha}/docs/'+('OPEN_GALAXY.md' if key=='galaxy' else 'DATA_EVIDENCE.md')],
        kind='annotated-screenshot',revision='2026-10-29',zoomFile=stem+'.svg',staticSnapshot=True,
        originalFile=source.relative_to(F).as_posix(),
        zoomHint='图题和导读为矢量文字，界面保留原始截图。下方可打开原始截图核对细节。',
        sourceRecord='sources/preface-opendipper-2026-10-29.md'))
    provenance.append(dict(id=number,attachment=original.name,originalSHA256=hashlib.sha256(original.read_bytes()).hexdigest(),
        screenshot=source.name,screenshotBytes=source.stat().st_size,dimensions=list(raw.size),decodedPixelsIdentical=True,
        screenshotSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),mountOriginal=mount.name,mount=frame.name,mountBytes=frame.stat().st_size,
        figureBytes=webp.stat().st_size,svgBytes=(F/(stem+'.svg')).stat().st_size))
current=json.loads((F/'manifest.json').read_text())
current=[r for r in current if r['id'] not in {'0-4','0-5'}]
current[1:1]=records
(F/'manifest.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
(S/'preface-opendipper-manifest.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(provenance,ensure_ascii=False,indent=2))
