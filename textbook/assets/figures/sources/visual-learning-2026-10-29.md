# 自学教材图版修订：制作与来源

日期：2026-10-29。插画为 AI 辅助概念表达；精确数字与关系由可编辑矢量生成，不以插画冒充实测或实际界面。

## 图 0-3　一次回答背后的工作

- 目的：区分回答的可见出口与形成模型、组织服务、核对改进的工作。
- 输入：课程已批准的图 1-2，仅作媒介、纸色与笔触参考；不复制其中历史人物。
- 方法：内置 imagegen；原始输出 `exec-33d8d195-276d-4c06-80f7-dd45d5a71a3e.png`；网页 WebP 质量 88，保留像素尺寸。
- 边界：假想工作场景；不是产品架构、真实实验室照片或训练执行证据。没有新增第三方照片素材。
- 验看：人物动作、纸本物件与三类工作的区分可读；不含需要核实的生成数字或项目标识。

### 最终绘制提示

```text
Use case: illustration-story.
Asset type: conceptual editorial illustration for the preface of AIOS101, a serious self-study university textbook for all majors.
Primary request: Make an intelligent, inviting technology-publication illustration with the visual metaphor "a simple AI answer unfolds into the human work behind it." It should teach a beginner that the visible chat product is only an entrance to a larger world of forming models, assembling services, and checking/improving them.
Input image 1 is STYLE REFERENCE ONLY: emulate its precise colored-pencil and graphite drawing, warm ivory book paper, restrained indigo, muted teal, coral accents and editorial collage craft. Do NOT copy its portraits, historic names, dates or text.
Composition: landscape 3:2. One large unfolded paper book on a real university studio desk, not a tiled infographic. A modest upright laptop screen in the foreground left shows only two simple empty chat bubbles. Its screen frame opens like a hinged paper doorway, revealing a coherent miniature cutaway workshop that extends right and upward across the open book. Three visibly different, easy-to-recognize activities: at the left-back, a researcher sorts paper data cards beside a realistic modest server/computer and a matrix-like parameter sheet; in the center-back, a developer connects a compact computing module to a plain interface and an open reference book; on the right, two students inspect a printed answer against dated source documents, one using a pencil to mark a discrepancy while another revises a shared document. Realistic books, paper, computers, magnifier, folders. Human craftsmanship and collaboration are the point; no humanoid AI, no brain, no floating magic particle networks. Work areas share one continuous physical scene, not three boxed cards, not a rigid process diagram.
The illustration is a visual metaphor, not a literal software architecture or a historical photograph. No arrows, data plots, fabricated code or fabricated logos. No readable text, numbers, figure number, title or watermark anywhere: leave unobtrusive blank paper space along the bottom 12% for separate precise typesetting. Use gentle diffuse daylight, highly legible silhouettes and purposeful details; no clutter, no empty decorative planets. Sophisticated and playful, appropriate for a professionally published Chinese textbook.
```

## 图 3-1　AI 开源生态的四个观察维度

- 方法：内置 imagegen，图 1-2 仅作笔触参考；原始输出 `exec-c999a96e-84c8-471f-8495-579599e22d62.png`。保留 1536×1024 像素，WebP 质量 88。
- 边界：资料、人物和线索为概念插画，不冒充项目截图、具体人物或依赖证据。四个中文词人工核对无误。

### 最终绘制提示

```text
Use case: stylized-concept.
Asset type: figure 3-1 editorial conceptual illustration in AIOS101, a university textbook on AI and open source for all majors.
Primary request: Illustrate four lenses for studying one open-source AI project: assets, relationships, people, rules. The metaphor is an archivist's open evidence case, NOT a software dependency graph. Four aspects of the SAME project should be evident, rather than four disconnected products.
Input image 1 is style reference only: retain sophisticated colored-pencil/graphite editorial illustration on warm ivory paper, indigo, muted teal and coral accents. No historic portraits or copied words.
Composition: landscape 3:2, almost overhead view, like a beautifully arranged natural-history field notebook but populated with real-world computing and documentary objects. One large indigo archival folder opens diagonally across the center, containing a compact model matrix sheet, a modest code notebook, source documents and small file tabs. Around it are four distinct observational tools, asymmetrically balanced: upper left a magnifying glass reveals the texture and separateness of model/data/document cards; upper right several threads connect document tabs to other clearly separate folders, with a question-tag reminding us that links require interpretation; lower left human hands from different contributors pass a correction sheet with a pencil and compare a previous revision; lower right a brass key rests on a large permission document beside a dated revision notebook. Everything belongs to a single coherent still-life on a reading table. No floating UI, no rounded infographic boxes, no robot, no brain, no neon network, no fake technical dashboard.
Only four large readable Chinese labels, integrated as restrained marginal pencil annotations: “资产”, “关系”, “参与者”, “规则”. Exactly these labels and no other readable text, no dates, no numerical data, no title or figure number. The relationships are purely conceptual threads with no arrowheads, not actual measured dependencies. Leave soft ivory breathing room around edges. Professional publication quality, tactile and thoughtful, amusingly investigative, visually different from a classroom scene or history portraits.
```

## 图 4-1、4-5、4-6：可复算的教学图

- 作者绘制的原生 SVG；生成程序 `scripts/figures/self_study.py 4`，不使用生成图像绘制数字或曲线。
- 内容依据本书 4.2、4.4 节；输入 2、目标 6、损失 (2w−6)² 的曲线与四个表格点完全对应。w=2→2.5 仅作更新示意，不声明具体优化器或学习率。
- 批次图严格按 100/10=10、两轮 20 次绘制；第 4 和 13 步保存为教学设定。
- 图 4-1 参数格子无实际数值或实验含义。新图无新增第三方素材；WebP 质量 91，SVG 用于放大。

## 图 5-1、5-2、5-3：容量、文本增长与候选筛选

原生 SVG 由 `scripts/figures/self_study.py 5` 生成；无新增外部素材。容量图使用正文假设 1000−780=220；候选图使用 0.55/0.25/0.12/0.05/0.03，归一化比例由这些数字直接计算。文本纸带是假想分词与输出，不声称来自真实模型；普通推理参数不变。WebP 质量 91；SVG 中保留文字以便放大。

## 图 6-3、6-7：相关性、适用性与反馈分支

原生 SVG 由 `scripts/figures/self_study.py 6` 绘制。6-3 采用正文完全假想的两份活动通知（9 月 10 日/延期至 9 月 15 日）；示意距离不是嵌入实测，颜色不代表自动判定新通知有效。6-7 的反馈条件来自 6.6.1 节，分支、权限与停止边界与正文对应。无新增外部素材，WebP 质量 91，SVG 用于放大。

## 图 6-4　检索增强生成：带着资料作答

- 方法：内置 imagegen；图 1-2 仅作纸色、媒介与笔触参考。原始输出 `exec-52cd4804-403d-483f-a0d4-594e2449fd47.png`，保留 1536×1024 像素，WebP 质量 88。
- 边界：假想图书馆场景；人物、资料与屏幕均不是真实项目材料。书架、选页、桌面、逐项核对分别帮助理解外部资料、检索、上下文和引用核验。精确流程仍由正文及 Mermaid 表述。
- 验看：三张带来源标记的资料页与屏幕标记可区分；库与桌面分离；未生成技术数字、品牌标志或虚假引用。

### 最终绘制提示

```text
Use case: illustration-story. Create a sophisticated conceptual editorial illustration for AIOS101, a university self-study textbook, using a real-world visual metaphor for retrieval-augmented generation: "bring the relevant pages to the writing desk, do not move the entire library into the writer's head." Input image is a STYLE reference only: warm ivory paper, excellent colored pencil/graphite drawing, restrained indigo, muted teal, coral accents. Do not copy historical portraits or words.
Landscape 3:2, spacious architectural cutaway of a beautiful ordinary university library reading room. Clear large silhouettes and purposeful details, not a grid of boxes. At far left a tall curved bookshelf full of plain bound documents; at its foot an open wooden card-catalog drawer and a small university librarian in side profile comparing a plain question slip with catalog cards. In the middle she selects JUST THREE separate excerpt sheets with colored edge tabs and blank source labels, carrying them on a small wheeled book trolley toward the right. Several other documents remain visibly on the shelf. On the right foreground a large uncluttered reading desk: the three excerpt pages are spread open next to the original question slip, each keeps its tab and source label. A realistic laptop on that desk shows a single blank answer-page shape with three tiny colored reference markers matching the papers. A real human reader standing beside the desk points between one sentence-line on that output and one specific source page, visibly checking support. Behind the desk a modest closed computer tower remains a separate object, with no flow of paper into it. The desk is the metaphor for temporary context, the external shelves remain separate and independently changeable.
This is a conceptual scene, not a real product UI or a literal software architecture. No network diagrams, no arrows, no human brain, no robots, no mystical floating words, no fake screenshots, no fabricated citations or logos. NO readable text, numbers, titles, figure number or watermark anywhere. The laptop and papers contain only minimal neutral pencil strokes. Keep the central three excerpt pages and the comparing gesture visually unmistakable. Generous ivory negative space, elegant varying scale between architectural shelves and human-scale papers, subtle daylight. Professional, interesting, calm and didactic.
```
