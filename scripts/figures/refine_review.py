"""Regenerate the revised precise diagrams; Pillow and CairoSVG required.

Source: canonical CH04–CH06 and the Apache-2.0 attributed excerpt below.
Run from any directory: python3 scripts/figures/refine_review.py
"""
from drawing import *

def node(x,y,w,lines,kind='normal',h=110):
    fill,stroke={'normal':('white','#D7D3C9'),'model':('#EEEAFB',purple),'result':('#E1EFEB',teal),'decision':('#FFF0E7',coral)}[kind]
    s=box(x,y,w,h,fill,stroke,20)
    for i,t in enumerate(lines): s+=txt(x+24,y+(h-(len(lines)-1)*34)/2+9+i*34,t,26,ink,600 if i==0 else 400)
    return s

def edge(d,label='',x=0,y=0):
    return line(d,purple,True)+(txt(x,y,label,22,teal) if label else '')

# Training steps, epoch counting and checkpoint saving are separate operations.
b=txt(60,175,'一个 epoch 是完整处理一轮训练集；检查点按保存策略记录状态。',26,teal)
b+=box(60,220,1480,360,'#EDF3EE',teal)+txt(90,270,'一轮训练中的批次顺序（简化）',28,teal,600)
for x,ls in [(90,['批次 1','一次迭代']),(610,['批次 2','一次迭代']),(1130,['后续批次','直至本轮处理完成'])]: b+=node(x,330,380,ls)
b+=edge('M470 385H610')+edge('M990 385H1130')+txt(90,505,'此处按“一批一次更新”说明。',24)+txt(90,545,'实际可采用梯度累积等安排。',24)
b+=edge('M1320 440V670')+node(1050,670,490,['本轮结束；是否继续？'],'decision')
b+=edge('M1295 780V920','是',1320,860)+node(1050,920,490,['进入下一轮','重复上方批次顺序'],'result')
b+=edge('M1540 725H1570V1165H1540','否',1500,1100)+node(1050,1110,490,['结束本次训练'],'result')
b+=edge('M800 440V630H420V670','到达设定保存步骤',445,610)
b+=node(60,670,720,['保存检查点','参数及相关训练状态'],'model')
b+=edge('M420 780V980')+node(60,980,720,['用于恢复、比较或后续适配','不自动等于最佳模型'],'result')
b+=txt(60,1320,'保存不要求等到一轮结束，也不意味着训练必须停止。',30,purple,600)
save('4-6','批次、迭代、训练轮次与检查点',b,['检查点保存由训练配置决定；可按步骤、轮次等策略触发。','图示区分批次处理、轮次计数和状态保存，不规定所有框架的实现细节。'],h=1520)

# Two independent filters on the same illustrative distribution.
b=txt(60,175,'教学示意 · 前文“今天的天气很” · 不是实际天气或模型运行结果',25,coral,600)
b+=box(60,220,740,700,'white')+txt(90,275,'同一候选分布',30,purple,600)
for i,(t,p) in enumerate([('晴朗',.55),('寒冷',.25),('温暖',.12),('潮湿',.05),('安静',.03)]):
    y=335+i*105; b+=txt(90,y+32,t,28)+box(220,y,700*p,50,purple,purple,4)+txt(245+700*p,y+35,f'{p:.2f}',26)
b+=txt(90,865,'五项概率合计 1.00',24)
b+=node(920,220,620,['top-k＝2','保留前两项：晴朗、寒冷'],'result',h=180)
b+=txt(945,450,'按候选数量截取',26,teal,600)
b+=node(920,560,620,['top-p＝0.90','保留前三项：晴朗、寒冷、温暖'],'decision',h=180)
b+=txt(945,790,'0.55＋0.25＋0.12＝0.92 ≥ 0.90',24,coral,600)+txt(945,840,'按累计概率达到或超过阈值截取',24)
b+=edge('M800 365H860V310H920')+edge('M800 680H860V650H920')
b+=box(60,1020,1480,180,'#EEEAFB',purple)+txt(90,1076,'两种方法独立对照，再在各自保留的集合内采样。',30,purple,600)+txt(90,1130,'数字只描述候选分配；高概率不保证事实正确。',26)
save('5-3','生成 top-k 与 top-p 的简化对照',b,['top-k 按候选数量保留；top-p 按累计概率保留达到阈值的最小集合。','第六章的检索 top-k 则表示文档候选片段数量，两者对象不同。'],h=1400)

# Separate retrieval, model and execution lanes; paired arrows never share a rail.
b=node(480,200,640,['人：目标、约束、授权与核验'],'decision')
b+=node(480,480,640,['任务编排与状态'],'model')
b+=edge('M670 310V480','目标与权限',485,410)+edge('M950 480V310','结果与待确认项',980,410)
b+=node(60,810,440,['外部文档与数据'])+node(60,1060,440,['检索器与索引'])
b+=node(580,1060,510,['模型：生成回答、','计划或调用请求'],'model')+node(1190,810,350,['工具与外部程序'])
b+=edge('M280 920V1060','建索引',305,1005)
b+=edge('M480 535H30V1115H60')+txt(65,725,'编排发起检索',23,teal)
b+=edge('M500 1115H580')+txt(80,1240,'检索片段 → 模型上下文证据',25,teal)
b+=edge('M710 590V1060','组织上下文',540,720)
b+=edge('M960 1060V590','回答／计划／调用请求',975,990)
b+=edge('M1120 520H1355V810')+txt(1140,675,'经权限检查后执行',22,teal)
b+=edge('M1540 865H1570V420H1120V480')+txt(1180,380,'执行结果或错误',22,teal)
save('6-1','从模型到任务系统的基本组成',b,['检索证据进入上下文；模型提出调用请求，外部程序承担实际执行。','这是角色关系示意，不表示某款产品的实际架构；资料、模型参数与工具结果不能混同。'],h=1440)

# Human approval comes before execution; denial is an explicit terminal branch.
b=node(60,205,760,['提出任务：目标、资料范围与权限'],'model')
b+=edge('M440 315V395')+node(60,395,760,['资料与权限是否必要且合适？'],'decision')
b+=node(1040,395,500,['停止或缩小范围','不执行该动作'],'decision')+edge('M820 450H1040','否',900,425)
b+=edge('M440 505V585','是',470,555)+node(60,585,760,['准备上下文与拟执行动作','尚未执行工具'])
b+=edge('M440 695V775')+node(60,775,760,['敏感数据、对外影响','或不可逆动作？'],'decision')
b+=node(1040,775,500,['展示动作、输入与后果','请求人工决定'],'decision')+edge('M820 830H1040','是',905,805)
b+=edge('M1290 885V975')+node(1040,975,500,['是否获准？'],'decision')
b+=edge('M1540 1030H1570V450H1540','否：拒绝则不执行',1165,665)
b+=edge('M1290 1085V1160H820','是',1315,1145)
b+=edge('M440 885V1135','否',470,1015)+node(60,1135,760,['执行前技术检查','输入、参数、权限与预算'],'decision')
b+=edge('M820 1220H980V1325H1040','未通过',840,1298)+node(1040,1270,500,['停止并说明原因','不执行该动作'],'decision')
b+=edge('M440 1245V1365','通过',470,1318)+node(60,1365,760,['执行获准的步骤'])
b+=edge('M440 1475V1555')+node(60,1555,760,['核验结果、证据与停止条件'])
b+=edge('M440 1665V1745')+node(60,1745,760,['任务完成且证据充分？'],'decision')
b+=edge('M820 1800H1040','否',905,1775)+node(1040,1745,500,['在约束内决定继续或停止','保留未完成事项'],'decision')
b+=edge('M440 1855V1955','是',470,1915)+node(60,1955,760,['交付结果、来源、日志与责任说明'],'result')
b+=txt(1060,1975,'继续须重新经过检查。',25,purple,600)+txt(1060,2025,'批准不能绕过技术约束。',24)
save('6-10','人机协作中的关键检查点',b,['准备动作、人工决定、技术检查和实际执行按先后区分；拒绝后不执行该动作。','人工确认不是唯一防线；每轮继续均受权限、预算、日志和停止条件约束。'],h=2260)

# Source excerpts remain literal; only whitespace, selection and annotations change.
excerpts=json.loads((F/'sources/agent-book-tool-excerpts.json').read_text())
b=txt(60,174,'固定原文代码字段节选 · 仅展示天气分支 · 省略时间分支与重复历史',24,coral,600)
y=220
for title,code,meaning in excerpts['panels']:
    lines=code.splitlines(); h=130+len(lines)*37
    b+=box(60,y,1480,h,'white')+txt(90,y+49,title,29,teal,600)
    for i,t in enumerate(lines): b+=f'<text x="95" y="{y+104+i*37}" font-family="DejaVu Sans Mono, monospace" font-size="25" fill="{ink}" xml:space="preserve">{escape(t)}</text>'
    b+=txt(85,y+h+46,meaning,25,purple,600)
    y+=h+110
b+=txt(60,y+20,'原教材时间、天气为预设教学内容；本图不表示实时查询或实际运行。',26,coral)
save('6-6','一次工具调用的消息与执行角色',b,['来源：李博杰《深入理解 AI Agent》第二章，固定提交 dbc046eb896ac4e39aa19c7774c8bf49583b89a6。','Apache License 2.0；从原文选取字段并换行排版，非原网页截图；省略字段不构成完整可执行请求。'],h=y+230)
print('Rebuilt five revised figures.')
