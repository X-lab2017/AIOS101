#!/usr/bin/env python3
"""Regenerate outlined AIOS101 brand SVGs. Design-time only: fontTools required."""
import argparse
import html
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site/assets/course'
P = json.loads((OUT / 'tokens.json').read_text())['colors']
parser = argparse.ArgumentParser()
parser.add_argument('--latin-font', required=True, help='Original SpaceGrotesk[wght].ttf from the pinned upstream')
parser.add_argument('--cjk-font', required=True, help='Local Noto Sans CJK SC Bold OTF; not bundled')
args = parser.parse_args()
latin = instantiateVariableFont(TTFont(args.latin_font), {'wght': 700}, inplace=False)
cjk = TTFont(args.cjk_font)


def letters(text, x, y, size, color, font=latin, spacing=0):
    glyphs, cmap, pen = font.getGlyphSet(), font.getBestCmap(), []
    scale = size / font['head'].unitsPerEm
    cursor = 0
    for char in text:
        name = cmap.get(ord(char), '.notdef')
        path = SVGPathPen(glyphs)
        glyphs[name].draw(path)
        pen.append(f'<path d="{path.getCommands()}" transform="translate({cursor:.3f} 0)"/>')
        cursor += glyphs[name].width + spacing / scale
    return f'<g fill="{color}" transform="translate({x} {y}) scale({scale:.7f} {-scale:.7f})">'+''.join(pen)+'</g>', cursor*scale


def txt(text, x, y, size, color=None, chinese=False, spacing=0):
    return letters(text, x, y, size, color or P['ink'], cjk if chinese else latin, spacing)[0]


def mark(x=0, y=0, size=128, variant='light'):
    shapes = ['8,26 58,50 58,100 8,76', '58,50 26,68 26,104 58,86', '26,68 62,88 62,122 26,104', '120,26 70,50 70,100 120,76', '70,50 102,68 102,104 70,86', '102,68 66,88 66,122 102,104']
    colors = ['#5146D9','#30288F','#DCD6FF','#DCD6FF','#5146D9','#30288F'] if variant!='dark' else ['#9D92FF','#6254D9','#EAE5FF','#EAE5FF','#9D92FF','#6254D9']
    start = f'<g transform="translate({x} {y}) scale({size/128})">'
    if variant in ('black','white'):
        color=P['ink'] if variant=='black' else '#FFFFFF'
        page='M8 26L58 50V86L62 88V122L26 104V84L8 76Z M28 68L55 53V56L30 70V102L28 101Z'
        return start+f'<g fill="{color}" fill-rule="evenodd"><path d="{page}"/><path d="{page}" transform="translate(128 0) scale(-1 1)"/><rect x="56" y="6" width="16" height="16"/></g></g>'
    return start+''.join(f'<polygon points="{s}" fill="{c}"/>' for s,c in zip(shapes,colors))+f'<rect x="56" y="6" width="16" height="16" fill="{P["coral"]}"/></g>'


def lockup(x=0,y=0,width=720,variant='light'):
    ink='#FFFFFF' if variant in ('dark','white') else P['ink']
    accent=('#B4AAFF' if variant=='dark' else P['indigo']) if variant not in ('white','black') else ink
    first, tw=letters('AIOS',184,109,105,ink)
    return f'<g transform="translate({x} {y}) scale({width/720})">'+mark(4,10,154,variant)+first+txt('101',184+tw,109,105,accent)+txt('AI 开源通识',186,151,31,ink,True)+'</g>'


def svg(w,h,content,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>{content}</svg>\n'


def write(name,w,h,content,title):
    (OUT/name).write_text(svg(w,h,content,title))


def motif(w,h,part=0):
    a,b,c,d=P['indigo'],P['lavender'],P['coral'],P['teal']
    if part==0:
        body=f'<polygon points="0,{h*.16} {w*.5},{h*.42} {w*.5},{h} 0,{h*.72}" fill="{a}"/><polygon points="{w},{h*.16} {w*.5},{h*.42} {w*.5},{h} {w},{h*.72}" fill="{b}"/><circle cx="{w*.5}" cy="{h*.2}" r="{w*.11}" fill="{c}"/>'
    elif part==1:
        body=''.join(f'<polygon points="{w*.12},{h*(.14+i*.18)} {w*.56},{h*(.04+i*.18)} {w*.88},{h*(.2+i*.18)} {w*.44},{h*(.3+i*.18)}" fill="{[a,b,"#B5ACF5"][i%3]}"/>' for i in range(4))+f'<path d="M{w*.5} {h*.1}V{h*.95}" stroke="{c}" stroke-width="{w*.027}" stroke-dasharray="12 13"/>'
    elif part==2:
        body=f'<path d="M0 {h*.9}H{w*.3}V{h*.58}H{w*.65}V{h*.22}H{w}" fill="none" stroke="{a}" stroke-width="{w*.045}"/>'+''.join(f'<rect x="{w*x}" y="{h*y}" width="{w*.13}" height="{w*.13}" fill="{color}"/>' for x,y,color in [(.235,.51,b),(.585,.145,c),(.035,.8,a)])
    else:
        body=f'<path d="M0 {h*.15}C{w*.5} {h*.15},{w*.2} {h*.7},{w*.5} {h*.7}S{w*.7} {h*.15},{w} {h*.15}" fill="none" stroke="{d}" stroke-width="{w*.075}"/><path d="M0 {h*.46}C{w*.33} {h*.46},{w*.25} {h*.76},{w*.5} {h*.76}S{w*.75} {h*.46},{w} {h*.46}" fill="none" stroke="{a}" stroke-width="{w*.075}"/><rect x="{w*.43}" y="{h*.64}" width="{w*.14}" height="{w*.14}" fill="{c}"/>'
    return body


OUT.mkdir(parents=True,exist_ok=True)
for variant in ('light','dark','black','white'):
    write(f'mark-{variant}.svg',128,128,mark(variant=variant),'AIOS101 开卷图形标')
    write(f'logo-{variant}.svg',720,180,lockup(variant=variant),'AIOS101 · AI 开源通识')
write('favicon.svg',64,64,'<rect width="64" height="64" rx="14" fill="#5146D9"/><path d="M9 21L29 31V54L9 44Z M55 21L35 31V54L55 44Z" fill="#FFFFFF"/><rect x="28" y="9" width="8" height="8" fill="#F27A59"/>','AIOS101')
write('avatar.svg',512,512,'<rect width="512" height="512" rx="100" fill="#1D2433"/>'+mark(105,45,302,'dark')+txt('AIOS101',87,435,78,'#FFFFFF'),'AIOS101 课程头像')
write('hero-folio.svg',600,600,mark(60,35,480),'开卷：折叠书页与问题方块')

names=['认识开源','理解 AI','探究证据','共同创造']
en=['DISCOVER OPENNESS','UNDERSTAND AI','INVESTIGATE EVIDENCE','CREATE TOGETHER']
for i,name in enumerate(names):
    top=f'<rect width="600" height="800" fill="{P["paper"]}"/>'+mark(34,25,54)+txt('AIOS101',102,65,31)+txt(f'0{i+1}',40,153,52,P['indigo'] if i%2==0 else '#C4573A')+f'<path d="M134 137H560" stroke="#CEC9DD"/>'+txt(name,40,237,63,chinese=True)+txt(en[i],44,280,17,spacing=1.4)
    art=f'<g transform="translate(0 330)">{motif(600,435,i)}</g>'
    write(f'cover-part-{i+1}.svg',600,800,top+art+txt('AI & OPEN SOURCE LITERACY',36,782,13),'AIOS101 · '+name+'篇封面')

social=f'<rect width="1200" height="630" fill="{P["paper"]}"/>'+lockup(55,52,620)+txt('打开知识，',65,357,67,chinese=True)+txt('一起创造。',65,444,67,chinese=True)+txt('AI & OPEN SOURCE LITERACY',68,550,20,spacing=1.6)+mark(797,120,330)
write('social-card.svg',1200,630,social,'AIOS101 课程社交预览')

# The v0.1 identity-board.svg is historical; do not overwrite it.
# Metadata and releases are maintained separately; generation never rewrites approval.
print(f'Generated 16 production SVG assets in {OUT}; review differences, then package a new baseline version.')
