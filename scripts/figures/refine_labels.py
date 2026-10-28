"""Revise SVG labels and routing without regenerating source evidence pixels."""
from drawing import *

changes={
 '04-01':{'参数位于训练之后。':'训练形成或更新参数。','它不是第四份输入材料。':'训练也使用初始或已有参数。','结构关系依照正文 Mermaid；图中符号为概念示意，不对应具体硬件或模型内部实现。':'图中突出训练形成或更新的数值状态；符号为概念示意，不对应具体硬件。','四类要素共同进入训练过程；参数是学习结果。模型运行还需配置与代码等条件。':'训练使用初始或已有参数，并据数据更新；模型运行还需配置与代码等条件。'},
 '05-06':{'M550 1265H220V625H300':'M800 1320V1345H30V625H300','x="1325" y="530"':'x="1300" y="700"'},
 '05-08':{'正文七步顺序保持不变；补充文字用于解释每一步需要留下的证据。':'每一步保留可核查证据，使评价条件与结论对应。'},
 '06-03':{'x="310" y="780"':'x="310" y="830"','x="555" y="565"':'x="300" y="565"','x="555" y="608"':'x="300" y="608"'},
 '06-07':{'x="70" y="1145"':'x="235" y="1145"'},
}
for n,edits in changes.items():
    target=F/'vector'/f'AIOS101_Fig-{n}_v02.svg'
    source=target if target.exists() else F/'vector'/f'AIOS101_Fig-{n}_v01.svg'
    svg=source.read_text()
    for old,new in edits.items():
        assert old in svg or new in svg, (n,old)
        svg=svg.replace(old,new)
    target.write_text(svg)
    image=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=3200))).convert('RGB')
    image.resize((1600,round(image.height/2)),Image.Resampling.LANCZOS).save(F/f'AIOS101_Fig-{n}_v02.webp',quality=90)
print('Revised five labels/routing diagrams.')
