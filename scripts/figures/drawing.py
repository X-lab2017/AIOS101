from pathlib import Path
from html import escape
import cairosvg,re,json,io
from PIL import Image
R=Path(__file__).resolve().parents[2]; F=R/'textbook/assets/figures'
ink='#1D2433'; purple='#5146D9'; teal='#327F78'; coral='#D15F43'; paper='#F6F3EB'
def txt(x,y,s,z=24,c=ink,w=400):return f'<text x="{x}" y="{y}" font-size="{z}" fill="{c}" font-weight="{w}">{escape(s)}</text>'
def box(x,y,w,h,fill='white',stroke='#D7D3C9',rx=16):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def line(d,c=purple,arrow=False,dashed=False):return f'<path d="{d}" stroke="{c}" stroke-width="3" fill="none" '+('marker-end="url(#arrow)" ' if arrow else '')+('stroke-dasharray="8 6"' if dashed else '')+'/>'
def dot(x,y,r=7,c=purple):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def grid(x,y,learned=False):
 s=''
 for a in range(4):
  for b in range(4):s+=box(x+b*23,y+a*23,17,17,(['#5146D9','#9F97E8','#DDD9F9','#327F78'][(a*3+b*5)%4] if learned else paper),purple,2)
 return s

def save(num,title,body,notes,h=1100):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{h}" viewBox="0 0 1600 {h}" font-family="Noto Sans CJK SC, sans-serif" role="img"><title>图 {num} {escape(title)}</title><desc>{escape("；".join(notes))}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{purple}"/></marker></defs><rect width="1600" height="{h}" fill="{paper}"/>'+txt(60,49,'AIOS101   /   X-lab   /   '+{'4':'从数据到模型','5':'从训练到推理','6':'从模型到智能体'}[num[0]],18,purple,600)+txt(60,112,'图 '+num+'  '+title,40,ink,700)+body+line(f'M60 {h-130}H1540','#CCC8BE')
 for i,n in enumerate(notes):s+=txt(60,h-91+i*30,n,20,'#565E69')
 s+='</svg>';name='AIOS101_Fig-'+num.replace('-','-0',1).zfill(5)+'_v01'
 name='AIOS101_Fig-'+ '-'.join(v.zfill(2) for v in num.split('-'))+'_v02'
 (F/'vector'/(name+'.svg')).write_text(s)
 im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=3200))).convert('RGB')
 im.resize((1600,h),Image.Resampling.LANCZOS).save(F/(name+'.webp'),quality=90)
 return name
