"""Exact, editable teaching figures for the self-study visual review.

Run from the repository: python3 scripts/figures/self_study.py 4
All numbers in these figures are teaching examples, not experiment results.
"""
from pathlib import Path
from html import escape
import io,json,re,sys
import cairosvg
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
F=ROOT/'textbook/assets/figures'
INK='#1D2433'; PURPLE='#5146D9'; TEAL='#327F78'; CORAL='#C65D43'; PAPER='#F6F3EB'; GRAY='#626876'
def text(x,y,s,size=28,color=INK,weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill='white',stroke='#D7D3C9',rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def path(d,color=PURPLE,arrow=False,dash=False,width=3):
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="9 7"' if dash else '')+'/>'
def circle(x,y,r,color=PURPLE):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
def title(n):
    return next(x['title'] for x in json.loads((F/'manifest.json').read_text()) if x['id']==n)
def save(n,v,body,notes,alt,h=1000):
    label=title(n); name='AIOS101_Fig-'+ '-'.join(x.zfill(2) for x in n.split('-'))+f'_v{v:02d}'
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{h}" viewBox="0 0 1600 {h}" font-family="Noto Sans CJK SC, sans-serif" role="img"><title>图 {n}　{escape(label)}</title><desc>{escape(alt)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{PURPLE}"/></marker></defs>'+rect(0,0,1600,h,PAPER,PAPER,0)
    svg+=text(64,51,'AIOS101  /  X-lab  /  自学教材',21,PURPLE,600)+text(64,116,f'图 {n}　{label}',39,INK,700)+body
    svg+=path(f'M64 {h-129}H1536','#CBC7BF',width=2)
    for i,s in enumerate(notes):svg+=text(64,h-83+i*35,s,24,GRAY)
    svg+='</svg>'
    (F/'vector'/f'{name}.svg').write_text(svg)
    im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=2400))).convert('RGB')
    im.resize((1600,h),Image.Resampling.LANCZOS).save(F/f'{name}.webp',quality=91)
    m=json.loads((F/'manifest.json').read_text());rec=next(x for x in m if x['id']==n);old=rec['file']
    rec.update(file=f'{name}.webp',width=1600,height=h,bytes=(F/f'{name}.webp').stat().st_size,alt=alt,vector=f'vector/{name}.svg',zoomFile=f'vector/{name}.svg',revision='2026-10-29',sourceRecord='sources/visual-learning-2026-10-29.md')
    rec.pop('originalBytes',None)
    (F/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    p=next((ROOT/'textbook/chapters').glob('CH'+n.split('-')[0].zfill(2)+'-*.md'));s=p.read_text().replace(old,rec['file']);s=re.sub(r'^!\[图 '+re.escape(n)+r'　[^\]]+\]',lambda _:f'![图 {n}　{alt}]',s,flags=re.M);p.write_text(s)
    print(n,name,rec['bytes'])

def chapter4():
    # A workbench: the structure stays a scaffold; the colored numeric state changes.
    b=text(64,180,'材料、计算形式、更新规则与资源，怎样在同一个过程中相遇？',29,TEAL)
    b+=text(90,259,'数据',34,PURPLE,700)+text(90,300,'按任务组织的样本',27)
    for i in range(3):
        b+=rect(102+i*17,350+i*15,260,130,'#FFFFFF','#AAA1DE',3)
        b+=path(f'M{125+i*17} {381+i*15}h200 M{125+i*17} {410+i*15}h140','#AAA1DE')
    b+=text(90,573,'目标与学习算法',34,TEAL,700)+text(90,617,'比较差距，决定怎样更新',26)
    for i,length in enumerate([170,110,205]):
        b+=path(f'M108 {665+i*39}h235',TEAL,width=2)+circle(108+length,665+i*39,9,TEAL)
    b+=path('M410 415H550V460H620',arrow=True)+path('M410 678H550V550H620',arrow=True)
    b+=rect(620,293,430,380,'#EFECFA',PURPLE,8)+text(654,341,'模型结构：组织计算',31,PURPLE,700)
    # Grid as a schematic state, never labeled as actual weights.
    for row in range(4):
        for col in range(4):b+=rect(675+col*43,385+row*43,31,31,['#C8C2EC','#E0DCF4','#A79DDE'][(row+col)%3],PURPLE,2)
    b+=text(874,424,'初始参数',27)+text(874,469,'或已有参数',27)+text(654,614,'训练：反复计算与调整',30,PURPLE,600)
    b+=path('M1050 480H1185',arrow=True)+text(1095,449,'更新',26,PURPLE)
    b+=rect(1202,330,300,318,'white',PURPLE,8)+text(1230,384,'更新后的参数',31,PURPLE,700)
    for row in range(4):
        for col in range(4):b+=rect(1266+col*40,414+row*40,29,29,[PURPLE,TEAL,'#C6BFE9','#9ABCB7'][(row*3+col*2)%4],PURPLE,2)
    b+=text(1230,607,'学习留下的数值状态',24)
    b+=rect(620,731,430,111,'#E5F0EB',TEAL,8)+text(650,777,'算力与软件环境',31,TEAL,700)+text(650,818,'支持上述计算实际执行',26)
    b+=path('M835 731V680',TEAL,True)+path('M1050 650H1120V717H1350V654',TEAL,dash=True)
    b+=text(1180,775,'结构与参数共同构成',27)+text(1180,818,'可运行模型的核心',27,TEAL,600)
    save('4-1',3,b,['结构规定怎样计算；参数是计算中可被训练调整的数值。','参数格子仅作示意，不表示真实权重；训练结果还受数据与设置影响。'],'数据和学习规则进入训练工作台，模型结构容纳初始或已有参数，算力与软件环境支持计算。训练改变参数状态，结构与参数共同构成可运行模型的核心。',1020)

    # Worked example plus an exact quadratic, not a decorative descending curve.
    b=text(64,177,'同一个样本：输入 2，目标 6；预测＝2×w；损失＝（预测−6）的平方。',28,TEAL)
    for x,w,pred,loss,c,tag in [(64,2,4,4,PURPLE,'更新前'),(846,2.5,5,1,TEAL,'一次示意更新后')]:
        b+=rect(x,220,690,226,'white',c,8)+text(x+29,264,tag,27,c,700)
        b+=text(x+29,323,f'w＝{w}   →   预测 {pred}',43,c,700)
        b+=text(x+29,384,f'与目标差 {pred-6}   →   损失 {loss}',34)
    b+=path('M765 327H833',arrow=True)
    b+=text(64,506,'把正文的四组参数放到同一张图里',29,INK,600)
    X=lambda w:160+(w-1.8)/2.4*590
    Y=lambda loss:897-loss/6*320
    b+=path('M160 562V897H770',GRAY,width=2)+text(72,567,'损失',25,GRAY)+text(710,942,'参数 w',25,GRAY)
    for loss in [0,1,4]:b+=path(f'M160 {Y(loss)}H750','#D6D3CE',width=1)+text(139,Y(loss)+8,loss,23,GRAY,anchor='end')
    points=[(1.8+i*2.4/100) for i in range(101)]
    b+=path('M'+'L'.join(f'{X(w):.2f} {Y((2*w-6)**2):.2f}' for w in points),PURPLE,width=4)
    for w in [2,2.5,3,4]:
        loss=(2*w-6)**2;b+=circle(X(w),Y(loss),9,TEAL if w in [2.5,3] else PURPLE)+text(X(w),929,w,24,anchor='middle')
        if w!=3:b+=text(X(w)+14,Y(loss)-16,f'({w}, {loss:g})',24,TEAL if w==2.5 else PURPLE)
    b+=text(160,977,'w＝3 时，这个样本的损失为 0。',24,TEAL)
    b+=text(875,551,'更新依据来自哪里？',31,INK,700)
    for i,(name,desc) in enumerate([('反向传播','计算损失对参数的梯度'),('优化器','依据梯度及设置更新参数'),('下一批样本','用更新后的参数继续计算')]):
        y=622+i*117;b+=circle(893,y-10,16,PURPLE)+text(893,y-2,i+1,20,'white',600,anchor='middle')+text(927,y,name,29,PURPLE,600)+text(927,y+43,desc,26)
        if i<2:b+=path(f'M893 {y+26}v52',PURPLE,width=2)
    b+=text(875,970,'一步的改善，不代表所有样本都变好。',26,CORAL)
    assert [(2*w-6)**2 for w in [2,2.5,3,4]]==[4,1,0,4]
    save('4-5',2,b,['数值沿用正文的乘法玩具模型；w＝2 → 2.5 是教学设定，并非执行某个优化器的实测轨迹。','曲线对应这一个样本；它说明“更大”未必“更好”，不代表真实大模型的损失地形。'],'输入2、目标6的乘法模型中，参数从2示意更新为2.5，预测从4变5，平方损失从4变1。精确曲线同时标出参数3的损失0和参数4的损失4；反向传播计算梯度，优化器执行更新，再进入下一批样本。',1130)

    # Exact batch/epoch accounting, with checkpoints deliberately inside epochs.
    b=text(64,180,'100 个样本 ÷ 每批 10 个＝每轮 10 批；本例每批执行一次参数更新。',29,TEAL)
    for epoch,y in [(1,300),(2,570)]:
        c=PURPLE if epoch==1 else TEAL
        b+=text(64,y+51,f'第 {epoch} 轮',35,c,700)+text(64,y+94,'1 个 epoch',26,c)
        b+=path(f'M285 {y-35}H1506',c,width=2)+text(290,y-63,'同一训练集再处理一轮' if epoch==2 else '完整处理一次训练集',27,c)
        for i in range(10):
            x=290+i*121;b+=rect(x,y,104,117,'#EEEBFA' if epoch==1 else '#E4EFEB',c,5)+text(x+52,y+43,f'批 {i+1}',25,c,600,anchor='middle')+text(x+52,y+88,'10 样本',22,INK,anchor='middle')+text(x+52,y+157,str((epoch-1)*10+i+1),24,GRAY,anchor='middle')
        b+=text(64,y+156,'累计更新',24,GRAY)
        step=4 if epoch==1 else 13; i=(step-1)%10;x=290+i*121+52
        b+=circle(x,y+175,7,CORAL)+path(f'M{x} {y+175}v29h80',CORAL,width=2)+text(x+91,y+213,f'更新 {step} 后保存检查点',24,CORAL)
    b+=text(64,848,'两轮合计：20 次更新',33,PURPLE,700)+text(650,848,'保存位置由策略决定，不必等到轮次结束。',28)
    assert 100//10==10 and 2*100//10==20
    save('4-6',3,b,['每个小格是一批，不是一个样本；示意未采用梯度累积等安排。','每轮可重新打乱样本顺序；图中批号仅用于计数。检查点不自动等于最佳模型。'],'100个样本，每批10个，每批一次更新。第一轮10批对应累计更新1至10，第二轮对应11至20。检查点示意保存在更新4和13之后，均在轮次内部；检查点不等于最佳模型。',1020)

if __name__=='__main__':
    {'4':chapter4}[sys.argv[1]]()
