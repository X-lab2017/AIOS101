from pathlib import Path
from html import escape
import json
import re
import shutil
import yaml
from PIL import Image
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "AIOS101-3h"
PAGES = OUT / "pages"
MEDIA = OUT / "media"
FIG = ROOT / "textbook" / "assets" / "figures"
W, H = 960, 540

C = {
    "paper": "#F6F3EB", "ink": "#1D2433", "indigo": "#5146D9",
    "coral": "#F27A59", "lavender": "#E7E3FC", "teal": "#3F958D",
    "muted": "#656577", "line": "#DCD9E1", "white": "#FFFFFF",
    "softcoral": "#FBE7DE", "softteal": "#E0EFEA", "softgray": "#ECE9E1",
}
FONT = {"latin": "QuattrocentoSans", "ea": "MiSans"}

for directory in (PAGES, MEDIA):
    directory.mkdir(parents=True, exist_ok=True)
for p in PAGES.glob("*.page"):
    p.unlink()

manifest = json.loads((FIG / "manifest.json").read_text(encoding="utf-8"))
meta = {x["id"]: x for x in manifest}
used_figs = [
    "1-1", "1-2", "1-3", "1-4", "2-1", "2-2", "2-3", "2-4",
    "3-1", "3-2", "3-3", "3-4", "3-5", "3-8", "4-1", "4-2",
    "4-3", "4-4", "4-5", "4-7", "5-1", "5-2", "5-3", "5-5",
    "5-6", "5-8", "5-9", "6-1", "6-2", "6-4", "6-5", "6-6",
    "6-7", "6-8", "6-9", "6-10",
]
fig_files = {}
for fid in used_figs:
    src = FIG / meta[fid]["file"]
    dst = MEDIA / f"fig-{fid.replace('-', '_')}.jpg"
    with Image.open(src) as im:
        if im.mode != "RGB":
            bg = Image.new("RGB", im.size, "white")
            if im.mode == "RGBA":
                bg.paste(im, mask=im.getchannel("A"))
            else:
                bg.paste(im.convert("RGB"))
            im = bg
        im.save(dst, "JPEG", quality=94, optimize=True, progressive=True, subsampling=0)
    fig_files[fid] = f"media/{dst.name}"

for name in ("logo-dark", "logo-light"):
    doc = fitz.open(ROOT / "site" / "assets" / "course" / f"{name}.svg")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=True)
    pix.save(MEDIA / f"{name}.png")

slides = []

def rect(x, y, w, h, color, name="rect", radius=False, line=None):
    return {"elementId": name, "elementType": "shape", "bounds": [x, y, w, h],
            "shapeName": "roundRect" if radius else "rect",
            "fill": {"type": "solid", "color": color},
            **({"border": line} if line else {"border": {"width": 0, "color": color}})}

def line(x1, y1, x2, y2, color=None, width=1, name="line", arrow=False):
    # Thin filled rectangles render consistently as rules in both editor and export.
    color = color or C["line"]
    bounds = [x1, y1, max(1, x2-x1), width] if y1 == y2 else [x1, y1, width, max(1, y2-y1)]
    return rect(*bounds, color, name)

def text(x, y, w, h, value, size=20, color=None, bold=False, align="left",
         valign="top", lh=1.25, name="text", wrap=True):
    return {"elementId": name, "elementType": "text", "bounds": [x, y, w, h],
            "content": {"text": value, "fontSize": size, "fontFamily": FONT,
                        "color": color or C["ink"], "bold": bold, "lineHeight": lh,
                        "align": [align, valign], "wrap": wrap}}

def rich(x, y, w, h, paragraphs, size=20, color=None, lh=1.35, name="rich"):
    value = "\n".join(f"<p>{p}</p>" for p in paragraphs)
    return text(x, y, w, h, value, size, color, False, "left", "top", lh, name)

def image(path, x, y, w, h, name="image", mode="contain"):
    return {"elementId": name, "elementType": "image", "bounds": [x, y, w, h],
            "src": path, "fit": {"mode": mode}}

def footer(n, source="", dark=False):
    color = "#C8C8D4" if dark else C["muted"]
    items = [line(56, 508, 904, 508, "#4C5260" if dark else C["line"], 1, "footer-rule")]
    if source:
        items.append(text(56, 514, 770, 16, source, 9, color, name="source", wrap=False))
    items.append(text(852, 512, 52, 18, f"{n:02d} / 62", 10, color, align="right", name="page-no", wrap=False))
    return items

def header(title, n, section="", kicker=None, source=""):
    items = []
    if section:
        items.append(text(56, 24, 600, 18, section, 10, C["indigo"], bold=True, name="section", wrap=False))
    items.append(text(56, 56, 848, 72, title, 30, C["ink"], bold=True, lh=1.14, name="title"))
    if kicker:
        items.append(text(56, 124, 848, 30, kicker, 15, C["muted"], name="kicker"))
    items += footer(n, source)
    return items

def add(kind, title, elements, section="", kicker=None, source="", dark=False, page_type="content"):
    n = len(slides) + 1
    if kind == "custom":
        els = elements + footer(n, source, dark)
    else:
        els = header(title, n, section, kicker, source) + elements
    slides.append({"title": title, "pageType": page_type,
                   "background": {"type": "solid", "color": C["ink"] if dark else C["paper"]},
                   "elements": els})

def bullets(items, x=56, y=164, w=848, row_h=61, size=20, accent=None, numbered=False):
    els = []
    accent = accent or C["indigo"]
    for i, item in enumerate(items):
        yy = y + i * row_h
        if numbered:
            els.append(text(x, yy, 42, 36, f"{i+1:02d}", 16, accent, bold=True, name=f"n{i}", wrap=False))
            tx = x + 48
        else:
            els.append(rect(x+3, yy+10, 9, 9, accent, f"dot{i}"))
            tx = x + 28
        if isinstance(item, tuple):
            head, body = item
            value = f"<p><strong>{escape(head)}</strong>　{escape(body)}</p>"
        else:
            value = f"<p>{escape(item)}</p>"
        els.append(text(tx, yy, w-(tx-x), row_h-4, value, size, C["ink"], lh=1.3, name=f"item{i}"))
        if i < len(items)-1:
            els.append(line(tx, yy+row_h-6, x+w, yy+row_h-6, C["line"], 1, f"sep{i}"))
    return els

def fig_slide(title, fid, section, points, source="", image_side="left", caption=True):
    els = []
    ix, tx = (56, 570) if image_side == "left" else (382, 56)
    iw, tw = 486, 334
    els.append(rect(ix, 162, iw, 318, C["white"], "image-field", line={"width": 1, "color": C["line"]}))
    els.append(image(fig_files[fid], ix+8, 170, iw-16, 302, "figure"))
    els += bullets(points, tx, 170, tw, max(63, 290//len(points)), 18)
    if caption:
        els.append(text(ix+8, 484, iw-16, 16, f"图 {fid}　{meta[fid]['title']}", 10, C["muted"], name="caption", wrap=False))
    add("fig", title, els, section, source=source)

def full_fig(title, fid, section, note, source=""):
    els = [rect(56, 148, 848, 326, C["white"], "image-field", line={"width": 1, "color": C["line"]}),
           image(fig_files[fid], 64, 154, 832, 314, "figure"),
           text(56, 480, 848, 22, f"图 {fid}　{meta[fid]['title']}｜{note}", 11, C["muted"], name="caption")]
    add("fig", title, els, section, source=source)

def compare(title, columns, section, bottom=None, source=""):
    els = []
    gap = 20
    cw = (848 - gap*(len(columns)-1)) / len(columns)
    for i, (head, body, color) in enumerate(columns):
        x = 56 + i*(cw+gap)
        els.append(text(x, 164, cw, 44, head, 23, color, bold=True, name=f"head{i}"))
        els.append(line(x, 214, x+cw, 214, color, 3, f"rule{i}"))
        els.append(text(x, 232, cw, 198, body, 19, C["ink"], lh=1.38, name=f"body{i}"))
    if bottom:
        els.append(rect(56, 444, 848, 42, C["lavender"], "takeaway"))
        els.append(text(72, 451, 816, 28, bottom, 17, C["indigo"], bold=True, valign="middle", name="takeaway-text"))
    add("compare", title, els, section, source=source)

def practice(title, task, steps, output, minutes="3 分钟", section="课堂互动"):
    els = [text(56, 154, 110, 24, minutes, 13, C["coral"], bold=True, name="time", wrap=False),
           text(56, 190, 848, 64, task, 25, C["ink"], bold=True, lh=1.22, name="task")]
    els += bullets(steps, 56, 278, 580, 55, 18, C["coral"], numbered=True)
    els.append(rect(674, 274, 230, 158, C["softcoral"], "output-field"))
    els.append(text(694, 294, 190, 24, "完成标准", 15, C["coral"], bold=True, name="output-label"))
    els.append(text(694, 330, 190, 82, output, 18, C["ink"], lh=1.32, name="output"))
    add("practice", title, els, section, page_type="content")

def chapter(nch, title, question, goals, part):
    n = len(slides)+1
    els = [text(56, 38, 300, 22, part, 11, "#B4AAFF", bold=True, name="part", wrap=False),
           text(56, 93, 180, 92, f"{nch:02d}", 78, C["coral"], bold=True, name="chapter-no", wrap=False),
           text(240, 102, 664, 88, title, 34, C["white"], bold=True, lh=1.15, name="chapter-title"),
           line(56, 212, 904, 212, "#4C5260", 1, "chapter-rule"),
           text(56, 242, 848, 66, question, 25, C["white"], bold=True, lh=1.25, name="question")]
    for i, goal in enumerate(goals):
        y = 338 + i*48
        els.append(text(56, y, 36, 28, f"0{i+1}", 13, "#B4AAFF", bold=True, name=f"gno{i}", wrap=False))
        els.append(text(104, y-2, 800, 36, goal, 18, "#E4E3EB", name=f"goal{i}"))
    add("custom", title, els, dark=True, page_type="chapter")

def break_page(number, next_title):
    n = len(slides)+1
    els = [text(56, 72, 848, 24, f"第 {number} 次休息", 14, "#B4AAFF", bold=True, name="break-label"),
           text(56, 142, 848, 88, "休息 10 分钟", 52, C["white"], bold=True, name="break-title"),
           text(56, 260, 848, 34, "离开屏幕，也让问题沉淀一下。", 22, "#D8D8E2", name="break-note"),
           line(56, 340, 904, 340, "#4C5260", 1, "break-rule"),
           text(56, 372, 848, 56, f"回来后：{next_title}", 24, C["coral"], bold=True, name="next")]
    add("custom", "休息 10 分钟", els, dark=True)

# 01—04 开场
n = 1
els = [image("media/logo-light.png", 56, 38, 200, 50, "logo"),
       text(56, 138, 848, 72, "AI 开源通识", 54, C["white"], bold=True, name="cover-title"),
       text(56, 226, 848, 44, "打开黑盒，理解智能，共同创造", 28, "#D8D8E2", name="cover-subtitle"),
       line(56, 306, 904, 306, "#4C5260", 1, "cover-rule"),
       text(56, 338, 848, 32, "全校通识授课｜序言与第 1—6 章", 19, C["coral"], bold=True, name="cover-scope"),
       text(56, 392, 848, 28, "180 分钟 · 真实案例 · 四次互动 · 无需编程先修", 17, "#C8C8D4", name="cover-meta"),
       text(56, 470, 848, 20, "AIOS101 · 课程讲义 v0.1 · 2026-10-29", 11, "#A8A8B8", name="cover-version")]
slides.append({"title": "AI 开源通识", "pageType": "cover", "background": {"type": "solid", "color": C["ink"]}, "elements": els})

practice("当 AI 给出答案，你看见了什么？",
         "回想一次使用 DeepSeek 等 AI 工具的经历：除了答案，你还能指出哪些内部过程？",
         ["独立写下：你能直接观察到的两件事", "再写下：你只能推测、无法直接确认的一件事", "与邻座比较：哪些证据能把推测变成判断"],
         "一条观察＋一个待核查问题", "2 分钟", "开场互动")

compare("今天不是学更多按钮，而是获得四种能力", [
    ("辨认", "分清模型、产品、系统与开放材料。\n\n知道自己在观察什么。", C["indigo"]),
    ("解释", "说明训练、推理、检索与工具调用怎样衔接。\n\n不停在名词。", C["indigo"]),
    ("核查", "追问对象、版本、配置、样本、许可与证据。\n\n不把宣传当结论。", C["teal"]),
    ("设计", "组合开放组件，加入权限、评价和人工节点。\n\n让创造可复用。", C["coral"]),
], "课程学习成果", "最终目标：从“会得到答案”走向“能解释、会验证、可创造”。")

compare("180 分钟：从开放认识到任务系统", [
    ("开场＋第 1—2 章", "10＋20＋25 分钟\n\n为什么开源\n开放、复用与协作", C["indigo"]),
    ("第 3—4 章", "25＋25 分钟\n\n生态全景\n智能如何形成", C["indigo"]),
    ("第 5—6 章", "25＋25 分钟\n\n运行与评价\n检索、工具与智能体", C["teal"]),
    ("收束", "5 分钟\n\n六章主线\n课后核查行动", C["coral"]),
], "学习路线", "两次休息各 10 分钟；第 22、41 页为休息页。")

# 第 1 章
chapter(1, "智能时代为什么需要\nAI 开源通识", "会使用 AI，为什么还不等于理解 AI？",
        ["分清模型、产品与 AI 系统", "用开放材料把黑盒变成学习对象"], "第一篇｜认识开源")
fig_slide("同一个 AI 工具，允许我们站在三种位置", "1-1", "第 1 章｜学习位置",
          [("使用", "得到结果，完成任务"), ("理解", "追问机制、条件与边界"), ("创造", "复用、修改并贡献新成果")])
compare("模型、产品、系统：三个层次不能混称", [
    ("模型", "结构＋参数等核心资产\n\n接收输入并计算输出\n\n例：某个固定版本的模型", C["indigo"]),
    ("AI 产品", "面向使用者的完整服务\n\n包含界面、规则、功能与运营\n\n例：DeepSeek 等工具", C["teal"]),
    ("AI 系统", "模型与数据、引擎、检索、工具、服务和人共同作用\n\n强调运行关系", C["coral"]),
], "第 1 章｜基本对象", "看到产品界面，不等于看到了模型；下载模型，也不等于获得整个产品。")
full_fig("软件开源为 AI 开放提供了方法与历史基础", "1-2", "第 1 章｜历史坐标",
         "GNU 提出自由软件目标；Linux 展示分布式协作；OSI 推动开源定义与许可传播。",
         "教材图 1-2；历史坐标用于理解脉络，不是完整开源史。")
fig_slide("打开 AI 黑盒，需要观察六类材料", "1-3", "第 1 章｜开放材料",
          [("有什么", "数据、代码、模型、文档、评测、协作记录"), ("怎么用", "分别支持理解、运行、比较、核查与贡献"), ("别混淆", "公开一种材料，不代表全部开放")])
full_fig("一份 README 能证明什么，又不能证明什么？", "1-4", "第 1 章｜真实证据",
         "固定提交 0cf7856 让全班阅读同一份文档；可核查声明，不等于全部训练细节已经公开。",
         "DeepSeek-R1 固定 README（0cf78561f1d51c84a21b2190626b21116d5c68bb，MIT License）。")
practice("判断练习｜公开可见，就是开放吗？",
         "某模型页面写着“可直接下载，禁止商用与再分发，训练数据未公开”。你能作出哪些判断？",
         ["能下载：只说明获得某项结果的入口存在", "限制条件：需要继续读许可，不能统称“自由使用”", "训练未公开：不能把可下载写成可复现完整训练"],
         "把“事实、许可、未知”分成三栏", "3 分钟", "第 1 章｜课堂互动")
compare("本章反馈｜用四个问题替代一句“它开源”", [
    ("对象", "具体是模型、数据集、代码，还是在线产品？", C["indigo"]),
    ("版本", "哪一个发布版本或固定提交？阅读日期是什么？", C["indigo"]),
    ("材料", "权重、数据、代码、文档、评测与记录公开了哪些？", C["teal"]),
    ("许可", "允许使用、修改、再分发和商用吗？有何条件？", C["coral"]),
], "第 1 章｜核查方法", "能下载 ≠ 能修改 ≠ 能再分发 ≠ 能完整复现。")

# 第 2 章
chapter(2, "开源的本质：开放、复用、\n协作与公共价值", "开源为什么不只是一份“免费代码”？",
        ["说清公开可见与开放授权的区别", "从 Issue、PR 与维护记录辨认共同创造"], "第一篇｜认识开源")
fig_slide("四个环节，把开放材料变成共同创造", "2-1", "第 2 章｜开源机制",
          [("开放", "材料可被观察与获取"), ("复用", "在许可条件下修改与再发布"), ("协作", "问题、修改与评审形成循环"), ("公共价值", "成果被他人学习、验证和继续建设")])
compare("公开可见与开放授权，是两个维度", [
    ("公开可见", "网页和源码能被阅读\n\n回答：看不看得到？\n\n不自动授予复制、修改或再分发权。", C["indigo"]),
    ("开放授权", "许可证明确允许的行为与条件\n\n回答：可以怎样做？\n\n需要保留版权、许可或署名等要求。", C["teal"]),
], "第 2 章｜开放判断", "免费阅读不等于没有权利边界；“网上能找到”也不是许可证明。")
fig_slide("Issue 与 PR：从提出问题到修改成果", "2-2", "第 2 章｜协作入口",
          [("Issue", "报告问题、提出建议、补充上下文"), ("PR", "提交一组可评审的修改"), ("平台", "国际案例用 GitHub；国内实践可用 AtomGit"), ("共同点", "公开讨论、版本记录与反馈")])
full_fig("真实社区记录要按各自证据阅读", "2-3", "第 2 章｜AIInfra",
         "Issue #386 与 PR #364 是独立记录，不能拼接成同一修复故事。",
         "AIInfra Issue #386（2026-10-28 读取时开放）；PR #364（2025-12-22 合并，b97c038）。")
compare("贡献不等于代码量，维护也不只是合并", [
    ("多样贡献", "文档与翻译\n数据与评测\n设计与教学\n问题报告与讨论\n代码与工具", C["indigo"]),
    ("维护劳动", "复现问题与澄清需求\n评审兼容性与风险\n处理重复与冲突\n版本发布与长期回应", C["teal"]),
], "第 2 章｜参与方式", "有价值的贡献让公共成果更准确、更可用、更容易继续维护。")
fig_slide("公共价值不靠口号，需要五类证据", "2-4", "第 2 章｜公共价值",
          [("可获得", "能否找到并使用"), ("可理解", "文档是否支持学习"), ("可复用", "许可与材料是否允许继续建设"), ("可协作", "反馈和贡献是否被回应"), ("可持续", "维护、版本与治理是否清楚")])
practice("评价练习｜这是一条有效贡献吗？",
         "某同学提交 PR：“这个项目太复杂，请全面重写。”没有环境、位置、修改说明或测试。",
         ["先判断：问题是否具体，修改是否可评审", "再补充：复现步骤、影响对象与最小修改", "最后回应：根据评审意见修订，并说明未覆盖事项"],
         "把笼统意见改成一条可评审贡献", "3 分钟", "第 2 章｜课堂互动")
compare("本章反馈｜协作质量看四个证据", [
    ("上下文", "问题发生在哪个版本、什么材料、什么使用情境？", C["indigo"]),
    ("最小行动", "他人能否复现问题或审查这组修改？", C["indigo"]),
    ("公开反馈", "谁提出了什么意见，贡献者怎样回应？", C["teal"]),
    ("维护结果", "合并、关闭、待处理或仍需证据？不作过度推断。", C["coral"]),
], "第 2 章｜协作核查", "好的协作不是“我说完了”，而是“别人能够接着做”。")

break_page(1, "第 3 章｜AI 开源生态全景")

# 第 3 章
chapter(3, "AI 开源生态全景：数据、模型、\n代码、工具链与社区", "一个 AI 成果由哪些开放要素构成，它们怎样连接？",
        ["从资产、活动、关系与影响四个维度看生态", "读懂生态图，同时保留统计与证据边界"], "第一篇｜认识开源")
fig_slide("生态不是项目名单，而是四个观察维度", "3-1", "第 3 章｜生态框架",
          [("资产", "数据、模型、代码、文档"), ("活动", "开发、评测、分发、使用"), ("关系", "依赖、派生、协作、治理"), ("影响", "学习、创新、公共价值与风险")])
compare("供应链与生态：相关，但不是同一张图", [
    ("供应链视角", "追踪一个成果从哪里来\n\n关注输入、加工、依赖、发布与责任\n\n适合问：这个模型由什么构成？", C["indigo"]),
    ("生态视角", "观察多主体怎样共同演化\n\n关注协作、复用、派生、治理与影响\n\n适合问：谁与谁怎样连接？", C["teal"]),
], "第 3 章｜观察视角", "一条连线必须说明关系类型；节点靠近不自动代表依赖或因果。")
full_fig("Agent Infra：围绕任务执行与智能体系统", "3-2", "第 3 章｜GOSD 2026",
         "86 个精选项目、12 类；观察窗口 2025-03—2026-08。",
         "GOSD 2026 完整评审版（2026-10-22）：145 个精选项目的子集，不是全球普查；图中位置不表示依赖。")
full_fig("Model Infra：围绕模型开发、训练与运行", "3-3", "第 3 章｜GOSD 2026",
         "59 个精选项目、13 类；与 Agent Infra 共同构成 145 个精选项目。",
         "GOSD 2026 完整评审版（2026-10-22）：分类用于观察技术供给，不等同于市场份额或完整排名。")
fig_slide("同样是“连接”，证据含义可以完全不同", "3-4", "第 3 章｜关系辨析",
          [("功能", "在系统中承担什么角色"), ("依赖", "运行或构建需要什么"), ("派生", "从哪个上游继续训练或修改"), ("分发", "通过什么渠道获得"), ("协作与治理", "谁参与、谁决定、怎样维护")])
full_fig("DeepSeek-R1：把资产和关系放在同一张图上", "3-5", "第 3 章｜真实项目",
         "读取模型、权重、文档、许可与形成关系；未公开的信息仍保留为未知。",
         "DeepSeek-R1 固定 README（0cf7856）；依据公开材料绘制，不补写未披露关系。")
full_fig("OpenDipper：用数据观察协作，而不是凭热度印象", "3-8", "第 3 章｜数据工具",
         "先确认指标、时间与项目范围，再解释星系与榜单。",
         "OpenDipper 开源星系界面；工具用于证据探究，图中位置与大小须按页面图例解释。")
practice("生态练习｜为一个校园 AI 工具画最小生态图",
         "选择“校园资料问答”或你熟悉的 AI 工具，画出它真正需要的开放要素。",
         ["列资产：模型、资料、代码、界面与文档", "画关系：用箭头标注检索、调用、依赖或维护", "标边界：哪些关系有证据，哪些只是你的推测"],
         "≥5 个节点＋≥4 条有名称的关系＋1 个未知项", "4 分钟", "第 3 章｜课堂互动")

# 第 4 章
chapter(4, "从数据到模型：智能如何形成", "资料怎样经过训练，变成能够生成回答的模型？",
        ["区分数据、结构、算法、参数与算力", "用预测、损失和参数更新解释最小训练循环"], "第二篇｜理解 AI")
fig_slide("模型能力不是某一个要素单独带来的", "4-1", "第 4 章｜形成要素",
          [("数据", "学习所依据的材料"), ("结构", "组织计算与参数"), ("算法", "依据目标调整参数"), ("算力", "让计算实际发生"), ("参数", "学习过程留下的数值状态")])
full_fig("FineWeb：训练数据是处理出来的，不是原料堆", "4-2", "第 4 章｜数据配方",
         "96 个 Common Crawl 快照，经提取、过滤、去重等处理形成约 15 万亿 token。",
         "FineWeb 论文 v2（2024-10-31）；token 按 GPT-2 分词统计，不表示其他模型使用 FineWeb。")
full_fig("读消融曲线：改变一个环节，保留结论边界", "4-3", "第 4 章｜FineWeb 消融",
         "17.1 亿参数模型上的特定对照；比较数据处理条件，不是所有模型的普遍排名。",
         "FineWeb 论文 v2 图 9（CC BY 4.0）；课程未独立复算。")
fig_slide("token、候选分布与损失：训练目标怎样落地", "4-4", "第 4 章｜下一 token 预测",
          [("token", "词、词的一部分、汉字或其他片段"), ("候选分布", "模型对下一片段的相对可能性分配"), ("损失", "预测与训练文本实际后续之间的差距"), ("注意", "图中数字为教学示意，不是事实正确率")])
full_fig("一次训练迭代：误差信号怎样推动参数更新", "4-5", "第 4 章｜训练循环",
         "样本 → 预测 → 损失 → 梯度 → 更新；普通推理没有这个参数更新循环。",
         "教材图 4-5；最小闭环省略数据调度、并行计算与监测等工程环节。")
compare("预训练、后训练、蒸馏：回答不同问题", [
    ("预训练", "在广泛数据上形成基础能力。\n\n常见目标：下一 token 预测。\n\n产物常称基座模型。", C["indigo"]),
    ("后训练", "继续适配指令、偏好与任务。\n\nSFT 学示范；RL 依据奖励信号调整行为。", C["teal"]),
    ("蒸馏", "利用已有模型产生的样本或信号训练另一模型。\n\n不是简单复制参数。", C["coral"]),
], "第 4 章｜形成阶段", "真实项目可组合多种路线；术语不能替代具体训练说明。")
full_fig("DeepSeek-R1：公开说明中的形成路径", "4-7", "第 4 章｜真实模型",
         "R1-Zero 与 R1 路线不同；六个蒸馏模型同时有样本来源与微调基础两类上游。",
         "DeepSeek-R1 固定 README（0cf7856）；仅呈现公开概述，不补写数据量、奖励设计或训练时长。")
practice("情境练习｜测试题“见过”之后，分数还说明什么？",
         "一套校园植物识别测试题被网站转载，其中近重复图片进入了训练集；测试准确率仍然很高。",
         ["指出问题：测试材料不当进入训练，独立性被削弱", "提出检查：来源、时间、近重复与划分规则", "改写结论：不能仅凭高分宣称能识别所有新场景"],
         "一句风险判断＋两项核查证据", "3 分钟", "第 4 章｜课堂互动")

break_page(2, "第 5 章｜从训练到推理")

# 第 5 章
chapter(5, "从训练到推理：AI 系统\n如何运行与评估", "同一个模型为什么给出不同回答，我们凭什么评价？",
        ["分清上下文、生成配置与运行系统", "用任务、样本、指标和失败记录形成有限结论"], "第二篇｜理解 AI")
fig_slide("模型实际看到什么：上下文不是一句提示", "5-1", "第 5 章｜上下文",
          [("输入", "系统提示、历史对话、用户材料和任务"), ("容量", "上下文通常同时容纳输入与新输出"), ("上限", "最大生成长度只限制新输出"), ("边界", "支持长上下文不等于每次都会输出很长")])
full_fig("预填充与解码：先处理输入，再逐步生成", "5-2", "第 5 章｜推理循环",
         "新 token 加入后续上下文，直到结束；普通推理使用参数而不更新参数。",
         "教材图 5-2；解码指生成输出序列，不是解密密文。")
fig_slide("温度、top-k、top-p 分别改变什么？", "5-3", "第 5 章｜生成策略",
          [("温度", "调整候选分布的集中程度"), ("top-k", "按固定数量保留候选"), ("top-p", "按累计概率保留最小候选集合"), ("别误读", "top-p＝0.95 不是 95% 正确率")])
full_fig("真实生成建议：先读项目条件，不背“万能参数”", "5-5", "第 5 章｜DeepSeek-R1",
         "项目建议温度 0.5—0.7、推荐 0.6，并建议多次测试取平均。",
         "DeepSeek-R1 固定 README（0cf7856）；项目建议不自动适用于所有模型，课程未据此运行模型。")
fig_slide("一次回答还经过哪些系统层？", "5-6", "第 5 章｜推理系统",
          [("模型与配置", "影响内容与资源需求"), ("推理引擎", "执行计算、管理状态与请求"), ("服务与硬件", "排队、路由、内存与计算环境"), ("网络与客户端", "传输与呈现"), ("结论", "慢或错不能只归因于模型")])
full_fig("评价从任务开始，而不是从分数开始", "5-8", "第 5 章｜最小评价",
         "任务 → 样本 → 基线 → 指标 → 配置 → 重复与失败 → 有限结论。",
         "教材图 5-8；基线可以是现有流程、简单规则、人工结果或另一模型。")
add("metrics", "真实评测数字，只能支持有限结论", [
    text(56, 150, 848, 26, "DeepSeek-R1 固定 README｜项目自报，课程未独立复算", 14, C["coral"], bold=True, name="evidence-label"),
    *[item for i, (name, value, metric) in enumerate([
        ("AIME 2024", "79.8", "pass@1"), ("MATH-500", "97.3", "pass@1"),
        ("SimpleQA", "30.1", "Correct"), ("C-SimpleQA", "63.7", "Correct"),
        ("LiveCodeBench", "65.9", "pass@1-COT")]) for item in [
        text(56+i*172, 196, 154, 26, name, 15, C["muted"], bold=True, name=f"mname{i}"),
        text(56+i*172, 230, 154, 58, value, 42, C["indigo"], bold=True, name=f"mvalue{i}", wrap=False),
        text(56+i*172, 292, 154, 24, metric, 13, C["muted"], name=f"mmetric{i}", wrap=False)]],
    line(56, 338, 904, 338, C["line"], 1, "metric-rule"),
    text(56, 360, 848, 52, "生成设置：最大生成长度 32,768 token；需采样的基准使用温度 0.6、top-p 0.95，每题生成 64 个回答估计 pass@1。", 17, C["ink"], name="settings"),
    rect(56, 432, 848, 46, C["softcoral"], "boundary"),
    text(72, 440, 816, 30, "不同任务、样本与指标不能横向相减，也不能合成“能力点”。", 18, C["coral"], bold=True, name="boundary-text")
], "第 5 章｜真实评测", source="DeepSeek-R1 固定 README（0cf7856）；数字为项目自报。")
practice("对照练习｜怎样比较两种生成配置？",
         "研究生成温度对“AIInfra 新生导言”的影响。请设计一个无需编写代码的对照方案。",
         ["固定对象：模型版本、完整提示、top-p、长度与运行环境", "只改变预先声明的温度；每个条件重复生成", "记录准确性、必要信息、可读性、截断与失败"],
         "一张变量表＋统一评价标准＋失败栏", "4 分钟", "第 5 章｜课堂互动")

# 第 6 章
chapter(6, "从模型到智能体：检索、\n工具与人机协作", "AI 怎样从“会回答”走向“能完成任务”？",
        ["分清检索片段、模型请求与工具实际执行", "设计有权限、有停止、有证据的低风险流程"], "第二篇｜理解 AI")
fig_slide("模型不是整个任务系统", "6-1", "第 6 章｜系统组成",
          [("模型", "生成回答、计划或调用请求"), ("检索", "从外部资料找到候选片段"), ("工具", "由外部程序执行查询、计算或读写"), ("状态与人", "保存进度、设定权限并核验")])
full_fig("RAG 第一步：把长资料切成可回查的证据块", "6-2", "第 6 章｜资料准备",
         "固定 AIInfra README 被教学性切分；保留标题、小节、版本与原文位置。",
         "AIInfra 固定 README（b97c038）；切分与候选次序为教学设计，不是产品实测。")
full_fig("RAG：检索片段进入上下文，不等于重新训练", "6-4", "第 6 章｜检索增强生成",
         "查资料与写回答相连；来源可更新、可回查，也可能切错、漏检或误读。",
         "教材图 6-4；top-k 在这里指文档片段，不是生成时的候选 token。")
fig_slide("工具调用：提出请求与真正执行是两件事", "6-5", "第 6 章｜工具调用",
          [("模型", "生成工具名称与输入参数"), ("编排", "检查格式、权限和任务状态"), ("外部程序", "获准后才实际执行"), ("返回", "结果、错误或超时进入后续上下文")])
full_fig("读工具消息：谁在说话，谁已经行动？", "6-6", "第 6 章｜消息顺序",
         "工具定义 → assistant 调用请求 → tool 返回结果；天气字段是预设教学内容。",
         "李博杰《深入理解 AI Agent》固定第 2 章（dbc046e，Apache-2.0）；节选与换行重排，不是完整可执行请求。")
full_fig("智能体循环：观察、规划、行动、反馈与停止", "6-7", "第 6 章｜任务循环",
         "会停止、会求助、会保留未完成事项，也是系统能力。",
         "教材图 6-7；工作流可包含智能体环节，停止条件从任务开始就应存在。")
full_fig("模拟轨迹：真实材料不等于真实执行", "6-8", "第 6 章｜新生导览",
         "人工发现“仓库体积”被误写为“模型大小”；最后只是“假设写入成功”。",
         "教学模拟轨迹，未发生真实文件写入；不得把模拟状态当作实测结果。")
full_fig("MCP 提供共同连接约定，但不自动保证安全", "6-9", "第 6 章｜协议与边界",
         "输入校验、权限、超时、日志与敏感操作确认，仍需具体系统落实。",
         "MCP 2025-06-18 工具规范与安全原则（MIT License）；课程未实现或运行 MCP。")
practice("设计练习｜给智能体加上必要的“刹车”",
         "为“根据公开课程资料生成学习卡，并保存到指定草稿目录”设计低风险流程。",
         ["限定范围：只读公开资料，只写指定草稿目录", "设置节点：保存前显示路径、内容与影响，由人确认", "写出停止：无新证据、连续失败或达到步数上限"],
         "一张流程图：资料＋工具＋人工确认＋停止条件", "4 分钟", "第 6 章｜课堂互动")

# 61—62 综合
compare("六章连成一条主线：从开放材料到可检查行动", [
    ("认识开源", "第 1—3 章\n\n对象与材料\n开放与协作\n资产与生态关系", C["indigo"]),
    ("理解 AI", "第 4—6 章\n\n训练形成参数\n推理生成输出\n检索与工具推进行动", C["teal"]),
    ("贯穿方法", "对象与版本\n配置与过程\n证据与边界\n权限与责任", C["coral"]),
], "综合回顾", "使用—理解—探究—贡献—创造：开源让每一步都有可观察、可核查的入口。")

n = len(slides)+1
els = [image("media/logo-light.png", 56, 38, 200, 50, "logo"),
       text(56, 122, 848, 56, "课后，用四步核查一个 AI 对象", 34, C["white"], bold=True, name="final-title")]
for i, (head, body) in enumerate([
    ("选定对象与版本", "一个模型、数据集、仓库或智能体流程"),
    ("收集材料与许可", "区分公开事实、项目主张与未知项"),
    ("记录配置与证据", "保留样本、过程、失败和结论边界"),
    ("形成可复用产物", "一张核查表、一幅生态图或一个低风险流程"),
]):
    y = 208 + i*54
    els.append(text(56, y, 40, 28, f"0{i+1}", 15, C["coral"], bold=True, name=f"final-n{i}", wrap=False))
    els.append(text(110, y-3, 220, 32, head, 19, C["white"], bold=True, name=f"final-h{i}"))
    els.append(text(342, y-2, 562, 32, body, 17, "#D8D8E2", name=f"final-b{i}"))
els += [line(56, 438, 904, 438, "#4C5260", 1, "final-rule"),
        text(56, 458, 848, 28, "github.com/X-lab2017/AIOS101", 17, "#B4AAFF", bold=True, name="repo", wrap=False),
        text(700, 482, 204, 20, "谢谢参与 · 继续共同创造", 12, "#C8C8D4", align="right", name="thanks", wrap=False)]
slides.append({"title": "课后四步核查行动", "pageType": "final", "background": {"type": "solid", "color": C["ink"]}, "elements": els})

assert len(slides) == 62, len(slides)
# Four main interactions: opening, ecosystem, generation comparison and agent design.
# The three shorter chapter checks remain in the deck as quick formative questions.
for page_no in (11, 20, 40):
    for element in slides[page_no-1]["elements"]:
        if element.get("elementId") == "section":
            element["content"]["text"] = element["content"]["text"].replace("课堂互动", "快速思考")
for i, slide in enumerate(slides, 1):
    # Element ids are deliberately stable and page-local.
    path = PAGES / f"{i:02d}.page"
    page = {k: v for k, v in slide.items() if k != "title"}
    path.write_text(yaml.safe_dump(page, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

presentation = {
    "version": "v2", "title": "AI 开源通识｜3 小时全校授课课件", "size": [W, H],
    "customFonts": [
        {"family": "MiSans", "src": "https://statics.kimi.ai/neo-design-static/p-font/MiSans.ttf"},
        {"family": "QuattrocentoSans", "src": "https://statics.kimi.ai/neo-design-static/p-font/QuattrocentoSans.ttf"},
    ],
    "theme": {"colors": C, "textStyles": {
        "title": {"fontSize": 30, "fontFamily": FONT, "color": "$ink", "bold": True, "lineHeight": 1.15},
        "body": {"fontSize": 19, "fontFamily": FONT, "color": "$ink", "lineHeight": 1.35},
    }},
    "pages": [f"pages/{i:02d}.page" for i in range(1, 63)],
}
(OUT / "AIOS101_3h.pptd").write_text(yaml.safe_dump(presentation, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")

index = ["# AIOS101 3 小时授课课件", "", "- 62 页，180 分钟，覆盖序言与第 1—6 章。", "- 两次休息各 10 分钟；四次主要课堂互动。", "- 主文件：`AIOS101_3h.pptd`；页面与媒体均在本目录内。", "- 正文来源：`textbook/chapters/`；图表来源与边界见教材图注。", "- 生成脚本：`scripts/create_aios101_3h_deck.py`。", "- 校验：`kimi-slides check slides/AIOS101-3h --level keep`。", "- 截图：`kimi-slides screenshot slides/AIOS101-3h -o slides/AIOS101-3h-screenshots`。", "", "## 教学时间", "", "| 页码 | 内容 | 分钟 |", "|---|---|---:|", "| 1—4 | 开场与学习路线 | 10 |", "| 5—12 | 第 1 章 | 20 |", "| 13—21 | 第 2 章 | 25 |", "| 22 | 休息 | 10 |", "| 23—31 | 第 3 章 | 25 |", "| 32—40 | 第 4 章 | 25 |", "| 41 | 休息 | 10 |", "| 42—50 | 第 5 章 | 25 |", "| 51—60 | 第 6 章 | 25 |", "| 61—62 | 综合与课后行动 | 5 |", "", "本课件为授课评审版，不替代教材完整解释；模型数据与社区记录按页面标注的版本、日期和证据边界使用。", ""]
(OUT / "README.md").write_text("\n".join(index), encoding="utf-8")
print(f"Created {len(slides)} pages, {len(list(MEDIA.iterdir()))} media files at {OUT}")
