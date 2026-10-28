const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  ExternalHyperlink,
  FootnoteReferenceRun,
  Header,
  Footer,
  HeadingLevel,
  ImageRun,
  PageNumber,
  PageOrientation,
  Packer,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableLayoutType,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require("docx");

const outputPath = process.argv[2];
if (!outputPath) throw new Error("Missing output path");

const root = path.resolve(__dirname, "..");
const screenshotPath = path.join(root, "textbook", "assets", "preface", "opendipper-open-galaxy-20261027.jpg");
const GREEN = "285B4B";
const GOLD = "A17B32";
const OCHRE = "945E47";
const BLUE = "526F82";
const INK = "23332E";
const MUTED = "63716B";
const LIGHT = "DCE4E0";
const bodyFont = { ascii: "Aptos", hAnsi: "Aptos", eastAsia: "宋体", cs: "Aptos" };
const headingFont = { ascii: "Aptos Display", hAnsi: "Aptos Display", eastAsia: "微软雅黑", cs: "Aptos" };

function run(text, options = {}) {
  return new TextRun({ text, font: bodyFont, size: 24, color: INK, ...options });
}

function body(text, options = {}) {
  return new Paragraph({
    style: "BodyText",
    children: [run(text)],
    ...options,
  });
}

function heading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    children: [new TextRun({ text, font: headingFont, size: 32, bold: true, color: GREEN })],
  });
}

function small(text, options = {}) {
  return new Paragraph({
    alignment: options.alignment || AlignmentType.LEFT,
    spacing: { after: options.after === undefined ? 80 : options.after, line: 260 },
    children: [run(text, { size: options.size || 18, color: options.color || MUTED, bold: options.bold })],
  });
}

function linkedText(label, url) {
  return new ExternalHyperlink({
    link: url,
    children: [new TextRun({ text: label, style: "Hyperlink", size: 18, font: bodyFont })],
  });
}

function footnoteParagraph(children) {
  return new Paragraph({ spacing: { after: 80, line: 240 }, children });
}

const header = new Header({
  children: [
    new Paragraph({
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LIGHT, space: 5 } },
      spacing: { after: 80 },
      children: [
        new TextRun({ text: "AI 开源通识　｜　序言", font: headingFont, size: 17, color: GREEN }),
        new TextRun({ text: "　　　　　　　　　专家评审稿 · v0.2", font: headingFont, size: 16, color: MUTED }),
      ],
    }),
  ],
});

const footer = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: LIGHT, space: 5 } },
      children: [
        new TextRun({ text: "AIOS101　·　", font: headingFont, size: 16, color: MUTED }),
        new TextRun({ children: [PageNumber.CURRENT], font: headingFont, size: 16, color: MUTED }),
      ],
    }),
  ],
});

const portraitPage = {
  size: { width: 11906, height: 16838, orientation: PageOrientation.PORTRAIT },
  margin: { top: 1250, right: 1300, bottom: 1250, left: 1300, header: 560, footer: 560 },
};

const landscapePage = {
  size: { width: 16838, height: 11906, orientation: PageOrientation.LANDSCAPE },
  margin: { top: 650, right: 800, bottom: 650, left: 800, header: 350, footer: 350 },
};

const mainChildren = [
  new Paragraph({
    spacing: { before: 120, after: 360 },
    children: [new TextRun({ text: "序言　从一次提问，看见一个开放的世界", font: headingFont, size: 42, bold: true, color: INK })],
  }),
  new Paragraph({
    spacing: { after: 320, line: 360 },
    children: [run("你可能从未下载过一个 AI 模型，却很可能已经使用过 AI。", { size: 28, bold: true, color: GREEN })],
  }),
  body("在 DeepSeek 这样的 AI 大模型工具中输入一个问题，片刻之后，一段回答便出现在屏幕上。我们可以让它解释概念、协助阅读、修改文字、生成图片或分析数据。输入框、按钮和回答，构成了大多数人直接感知的 AI。"),
  body("但在这次简单的提问背后，大模型究竟是什么？它由哪些材料和技术塑造，为什么会给出这样的回答？它的能力如何被检验，局限又由谁说明？当工具出现错误、不再适用或无法满足我们的需要时，我们能否进一步检查、改进，甚至参与它的建设？"),
  body("工具的简洁把复杂技术折叠到了界面之后，也可能使我们把一次回答当成 AI 的全部。事实上，我们看见的是一个服务的出口，尚未看见支撑这次回答的大模型、数据、代码、算力、评测与协作者。"),
  body("这个看不见的世界并非无法接近。只要沿着一次回答向上游追问，技术系统的轮廓就会逐渐显现，我们也会从工具的使用者，开始成为技术的理解者。"),
  body("这些问题，构成了本书的起点。"),
  heading("一次提问，如何连接一个世界"),
  body("要理解日常使用的 AI 工具，可以沿着它背后的 AI 成果“供应链”向上游走去。"),
  body("这里的供应链，不只是商品从工厂到商店的过程，而是一个 AI 成果被生产、组合、分发和维护所经历的环节。数据经过选择、加工与标注，成为训练材料；算法、代码和算力共同塑造模型；模型被打包、发布，再与检索、推理和应用工具组合，进入具体任务；评测、文档、版本与许可证，帮助人们判断它做了什么、怎样使用以及能否继续修改；维护者和使用者则在长期互动中发现问题、修补缺陷、创造新的用途。"),
  body("沿着这条链条，我们会遇见代码仓库、数据集、模型文件、开发框架、评测结果和技术文档，也会遇见开发者、研究者、社区维护者、企业、高校、基金会以及无数普通使用者。AI 因而不再只是人机对话框里的答案，而是一个由技术资产、人的劳动和社会协作共同构成的系统。"),
  body("供应链帮助我们追踪“一个成果怎样到来”，生态则帮助我们理解“众多成果与参与者怎样共同演化”。在生态视野中，我们不仅关心依赖关系，也关心知识如何传播、贡献如何得到回应、项目如何维护、价值由谁创造并由谁分享。供应链是进入生态的一条路径，却不是生态的全部。"),
  body("开源，使这些原本容易被遮蔽的环节有了被看见的可能。"),
  heading("开源：让理解、验证与共同创造发生"),
  body("开源当然意味着开放源代码，但对于 AI 通识教育，它的意义远不止于此。"),
  body("开放的数据、代码、模型材料、文档、评测和协作记录，可以成为学习者直接观察的对象。我们不必只接受“这个模型很强大”的结论，还可以进一步询问：它在哪些任务上接受了评测？评测使用了什么数据？公开的是最终权重，还是也包含了理解训练过程所需的材料？别人能否在相同条件下重复这一结果？所谓“开放”，究竟允许我们做什么？"),
  body("这样，学习便从记住结论转向检查结论，从观看演示转向形成证据。"),
  body("开放还允许复用。学习者可以站在已有成果之上，修改一个变量、比较两个版本、补充一份说明、复现一个实验，而不必每次都从零开始。复用不是简单照搬，而是理解前人工作的过程，也是新创造得以发生的起点。"),
  body("更重要的是，开源把学习带入一种共同工作的方式。一份清楚的错误报告、一处文档修订、一组经过核验的数据、一项翻译、一次评测和一段代码，都可能改善他人正在使用的成果。学习不再只是为自己积累知识，也可以为共同体留下有用的东西。"),
  body("在长期的计算机科学普及教育和开源实践中，我越来越确信：教育的本质不仅是理解已有世界，更是获得创造新事物的能力。开源恰好把这两种追求连接起来。它打开技术的黑盒，也打开参与创造的大门；它让知识可以被查验，也让个人能够与他人一起，把想法变成公共成果。"),
  body("这也是本书选择以开源作为 AI 通识教育核心的原因。"),
  body("对于中国学习者而言，开源还意味着一种双向参与：我们不仅可以获取和使用全球成果，也能够把来自中国教育、科研、产业与社会生活的真实问题转化为开放作品，在共同改进中贡献自己的知识与经验。理解全球生态与建设中国生态，不是彼此分离的任务，而是同一学习过程的两个方向。"),
  heading("从一片开源星系，学习观察与判断"),
  body("看见生态并不容易。项目、模型、数据集和开发者分散在不同平台，信息不断更新，名称、版本与关系纷繁复杂。为了把这些问题转化为可观察、可讨论的学习对象，本书将在多个章节中使用“开源北斗”（OpenDipper）作为数据观测与证据探究工具。"),
  new Paragraph({
    style: "BodyText",
    children: [
      run("我们可以借助全球观测，了解开发者、项目、模型和生态活动在不同地域的分布；借助 AI 雷达，围绕具体任务发现软件、模型与数据候选；借助开源星系，观察项目之间已经记录的关系，整理自己的研究对象；还可以从资料阅读走向知识整理和证据报告，并进一步把问题、纠错与改进带回开放社区。"),
      new FootnoteReferenceRun(1),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    keepNext: true,
    spacing: { before: 180, after: 100 },
    children: [
      new ImageRun({
        type: "jpg",
        data: fs.readFileSync(screenshotPath),
        transformation: { width: 590, height: 405 },
        altText: {
          title: "OpenDipper 开源星系界面",
          description: "左侧为探索与筛选区，中间为代码星系，右侧为模型、数据集与应用 Space 组成的模型星系。",
          name: "OpenDipper 开源星系实景截图",
        },
      }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 220, line: 260 },
    children: [
      run("图 0-1　OpenDipper 开源星系界面。节点与连线用于探索项目及模型之间的记录关系，不直接代表软件依赖或质量排名。项目发布截图，应用版本 1.6.0，截图日期：2026-10-27；截图日期不等于数据观察期。原始 JPEG 未编辑，仅限专家评审，正式出版前复核授权。", { size: 17, color: MUTED }),
      new FootnoteReferenceRun(4),
    ],
  }),
  new Paragraph({
    style: "BodyText",
    children: [
      run("但工具不会自动给出正确答案。地图上的一条连线，可能表示共享贡献者，而不表示软件依赖；节点的大小和位置，也不必然代表质量或重要性。开源星系的设计特意区分记录关系与推断关系，并提醒使用者不要将共享贡献者或发布方路径直接解释为依赖链。"),
      new FootnoteReferenceRun(2),
    ],
  }),
  new Paragraph({
    style: "BodyText",
    children: [
      run("同样，下载量只是特定平台和时间范围内的获取信号，排名只在既定指标和样本中成立，公开可下载也不等于拥有完整开源材料与许可。不同数据可能具有不同观察期、统计对象和覆盖范围；缺失的数据应保持为未知，而不能随意当成零。"),
      new FootnoteReferenceRun(3),
    ],
  }),
  body("因此，OpenDipper 在本书中不是替我们作判断的“答案机器”，而是一间训练观察与判断的实验室。我们使用它，不是为了追逐更大的数字或更炫目的图，而是学习提出好问题、核对证据、说明边界，并把新的发现转化为可复核的知识。"),
  heading("一门面向所有大学生的 AI 通识课"),
  body("人工智能正在成为许多学科共同面对的基础性变化。无论学习文学、历史、教育、经济、管理、法律、新闻、艺术，还是数学、物理、生命科学与工程技术，我们都可能使用 AI、评价 AI 的成果，或参与决定它如何进入学习、工作与社会生活。"),
  body("因此，AI 通识教育不能只属于计算机专业，也不应变成少数熟练掌握工具者的专属能力。"),
  body("本书不要求你预先学习机器学习，不要求你编写过复杂程序，也不要求拥有昂贵的计算设备。你需要带来的，是基本的数字素养、对现实世界的好奇，以及愿意追问和动手验证的态度。"),
  body("对于没有编程经验的读者，书中提供无代码或低代码的探究路径。你仍然需要观察、比较、核查和解释，而不是只观看教师操作。对于有技术基础的读者，进阶挑战会进入实现、部署、评估与系统优化，但这些内容不会成为所有人理解核心概念的门槛。"),
  body("通识也不意味着浅尝辄止。我们减少的是不必要的先修知识，而不是思考的严谨性；我们避免的是工具复杂度造成的障碍，而不是证据、责任与创造的要求。"),
  body("本书也不会把开源描绘成没有代价的理想世界。开放可能伴随许可证误用、隐私泄露、安全风险和偏见传播；公开代码不保证项目得到良好维护，允许复用也不自动产生公共价值。正因为这些问题真实存在，我们才需要学习如何判断开放程度、如何核验结论、如何尊重他人劳动，以及如何负责任地发布自己的成果。"),
  heading("四篇十二章：从使用走向创造"),
  body("全书以“使用—理解—探究—贡献—创造”为学习主线，分为四篇。图 0-2 将这条主线、四篇十二章、三层学习路径与综合成果放在同一视野中，帮助我们在进入具体章节之前先看见全书结构。"),
];

const parts = [
  {
    number: "01",
    title: "认识开源",
    subtitle: "智能时代的共同创造",
    color: GREEN,
    chapters: [
      ["CH01", "智能时代为什么需要 AI 开源通识"],
      ["CH02", "开源的本质：开放、复用、协作与公共价值"],
      ["CH03", "AI 开源生态全景：数据、模型、代码、工具链与社区"],
    ],
  },
  {
    number: "02",
    title: "理解 AI",
    subtitle: "从模型黑盒到开放系统",
    color: GOLD,
    chapters: [
      ["CH04", "从数据到模型：智能如何形成"],
      ["CH05", "从训练到推理：AI 系统如何运行与评估"],
      ["CH06", "从模型到智能体：检索、工具与人机协作"],
    ],
  },
  {
    number: "03",
    title: "探究证据",
    subtitle: "开放程度、可复现性与生态影响",
    color: OCHRE,
    chapters: [
      ["CH07", "开放到什么程度：模型材料、许可证与开放分级"],
      ["CH08", "从公开到可复现：版本、文档、评测与开放科学"],
      ["CH09", "用数据理解生态：供给、网络、影响力与公共价值"],
    ],
  },
  {
    number: "04",
    title: "共同创造",
    subtitle: "从开放参与到负责任发布",
    color: BLUE,
    chapters: [
      ["CH10", "从参与到贡献：开源社区协作、治理与评价"],
      ["CH11", "用开源创造 AI：项目设计、系统集成与负责任发布"],
      ["CH12", "从学习者到创造者：综合项目、公开答辩与持续贡献"],
    ],
  },
];

function mapParagraph(text, options = {}) {
  return new Paragraph({
    alignment: options.alignment || AlignmentType.LEFT,
    spacing: { before: options.before || 0, after: options.after === undefined ? 70 : options.after, line: options.line || 220 },
    keepNext: options.keepNext,
    children: [new TextRun({ text, font: headingFont, size: options.size || 17, bold: options.bold, color: options.color || INK })],
  });
}

function partCell(part) {
  const children = [
    mapParagraph(part.number, { size: 23, bold: true, color: part.color, after: 30 }),
    mapParagraph(part.title, { size: 26, bold: true, color: part.color, after: 45 }),
    mapParagraph(part.subtitle, { size: 16, color: MUTED, after: 170 }),
  ];
  for (const [code, title] of part.chapters) {
    children.push(mapParagraph(code, { size: 14, bold: true, color: part.color, after: 25, keepNext: true }));
    children.push(mapParagraph(title, { size: 17, color: INK, after: 145, line: 225 }));
  }
  return new TableCell({
    width: { size: 3750, type: WidthType.DXA },
    verticalAlign: VerticalAlign.TOP,
    margins: { top: 140, bottom: 110, left: 170, right: 170 },
    shading: { type: ShadingType.CLEAR, fill: "FAFBFA", color: "auto" },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 18, color: part.color },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
      left: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
      right: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
    },
    children,
  });
}

function pathCell(title, description, color) {
  return new TableCell({
    width: { size: 5000, type: WidthType.DXA },
    margins: { top: 90, bottom: 80, left: 140, right: 140 },
    shading: { type: ShadingType.CLEAR, fill: "F3F6F4", color: "auto" },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
      left: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
      right: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
    },
    children: [
      new Paragraph({
        spacing: { after: 30 },
        children: [
          new TextRun({ text: title + "　", font: headingFont, size: 17, bold: true, color }),
          new TextRun({ text: description, font: bodyFont, size: 16, color: INK }),
        ],
      }),
    ],
  });
}

const mapChildren = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 70 },
    children: [new TextRun({ text: "图 0-2　《AI 开源通识》全书学习地图", font: headingFont, size: 34, bold: true, color: INK })],
  }),
  mapParagraph("以 AI 为学习对象，以开源为认识论、方法论和实践方式", { alignment: AlignmentType.CENTER, size: 17, color: MUTED, after: 130 }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 5, color: LIGHT, space: 8 } },
    children: [new TextRun({ text: "使用　→　理解　→　探究　→　贡献　→　创造", font: headingFont, size: 34, bold: true, color: GREEN })],
  }),
  new Table({
    width: { size: 15000, type: WidthType.DXA },
    columnWidths: [3750, 3750, 3750, 3750],
    layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: parts.map(partCell), cantSplit: true })],
  }),
  mapParagraph("三层学习路径", { size: 17, bold: true, color: GREEN, before: 130, after: 60, keepNext: true }),
  new Table({
    width: { size: 15000, type: WidthType.DXA },
    columnWidths: [5000, 5000, 5000],
    layout: TableLayoutType.FIXED,
    rows: [new TableRow({ children: [
      pathCell("核心通识", "全体学习者建立共同语言", GREEN),
      pathCell("探究实践", "无代码／低代码均可进入", GOLD),
      pathCell("进阶挑战", "面向有编程或系统基础者", BLUE),
    ], cantSplit: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 140, after: 80 },
    children: [
      new TextRun({ text: "综合项目方向　", font: headingFont, size: 17, bold: true, color: MUTED }),
      new TextRun({ text: "开放证据审计　·　生态数据研究　·　开源作品创造", font: headingFont, size: 19, bold: true, color: GREEN }),
    ],
  }),
  mapParagraph("学习证据：AI 开源生态图 · 开放度核查档案 · 最小探究记录 · 数据探究简报 · 贡献档案 · 综合项目发布包", { alignment: AlignmentType.CENTER, size: 15, color: MUTED, after: 50 }),
  mapParagraph("结构依据：课程宪法 v0.1、课程总规格 v0.1。本页为 Word 原生表格与文字，可直接编辑。", { alignment: AlignmentType.CENTER, size: 13, color: MUTED, after: 0 }),
];

const finalChildren = [
  body("第一篇“认识开源：智能时代的共同创造”，从为什么学习 AI 开源通识开始，讨论开放、复用、协作与公共价值，并建立数据、模型、代码、工具链与社区相互连接的整体图景。"),
  body("第二篇“理解 AI：从模型黑盒到开放系统”，沿着数据到模型、训练到推理、模型到智能体的路径，理解智能如何形成、系统如何运行，以及 AI 如何通过检索和工具进入真实任务。我们的目标不是记住全部技术细节，而是建立能够继续学习的基本心智模型。"),
  body("第三篇“探究证据：开放程度、可复现性与生态影响”，进一步追问一个模型究竟开放到什么程度，一项结论如何被他人重复，以及如何用数据研究全球与中国 AI 开源的发展。我们将学习辨认版本、材料、许可和评测证据，也将学习面对图表与排名时核对统计口径和结论边界。"),
  body("第四篇“共同创造：从开放参与到负责任发布”，把视线转向真实社区与个人作品。我们将学习提出问题、参与讨论、接受评审、完成贡献，并将开放模型、数据和工具组合为可复用、可评估、可维护的成果。"),
  body("这四篇不是彼此分离的知识板块，而是一条逐步展开的学习道路：先能看懂，继而能够验证；先学会与他人协作，继而让自己的成果成为他人继续创造的起点。"),
  heading("我们将怎样学习"),
  body("本书每章都从问题开始，通过概念建构、真实开源对象分析、探究实践和证据表达，形成完整的学习闭环。你不仅会读到概念，还会留下自己的学习产物。"),
  body("这些产物可能是一张 AI 开源生态图、一份具体模型版本的开放度核查档案、一份记录失败与解释的最小实验笔记、一份说明指标口径的数据探究简报，也可能是一份包含公开反馈的贡献档案。到课程后期，你将把这些经验汇聚为一个综合项目：可以审计一个开放项目的证据，可以研究一片生态，也可以创造一件对他人有用的开源作品。"),
  body("我们不以代码行数衡量贡献，也不以工具操作的熟练程度代替理解。文档、数据、评测、翻译、设计、讨论和代码，只要能够回应真实需要并接受检验，都是有价值的工作。"),
  body("在学习过程中，你也可以使用 AI 协助阅读、分析、编程和写作。但 AI 生成的内容不能代替你的判断。重要的来源需要回查，关键的结果需要核验，使用了他人的材料需要说明，AI 的帮助也应按课程要求披露。真正需要培养的，不是得到一个看似完整答案的速度，而是知道答案从何而来、在何处可能出错的能力。"),
  heading("你的第一个问题，就是起点"),
  body("开始阅读第一章之前，不妨先留下三个不计分的答案："),
  new Paragraph({ style: "ListParagraph", children: [run("我最近使用或最关注的一个 AI 成果是什么？")] }),
  new Paragraph({ style: "ListParagraph", children: [run("我最想打开它的哪一个黑盒？")] }),
  new Paragraph({ style: "ListParagraph", children: [run("如果有机会改进它，我愿意贡献什么？")] }),
  body("现在不必急着给出完整或正确的回答。随着学习推进，你可以重新回到这三个问题，观察自己的理解如何改变，也看看最初的好奇会把自己带向哪里。"),
  body("智能时代真正重要的，不只是少数人造出更强的 AI，也包括更多人能够理解它、质疑它、改进它，并共同决定它应当服务于怎样的未来。"),
  new Paragraph({
    spacing: { before: 180, after: 260, line: 380 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: GOLD, space: 12 } },
    children: [run("愿这本书帮助你从一次提问看见一个开放的世界，也帮助你在这个世界中留下自己的创造。", { size: 27, bold: true, color: GREEN })],
  }),
  heading("资料来源与版本说明"),
  body("本稿引用来源详见页下脚注 1—4。在线材料用于事实核查与课程设计，具体功能、数据与界面可能继续演化。正式出版时应重新核验时效性内容，并保留相应版本或快照。"),
  body("除图 0-1 按来源登记用于本次专家评审外，本稿未复制 OpenDipper 项目的其他图片、代码、数据或品牌素材；图 0-1 使用原始 JPEG，未作编辑，正式出版前需复核素材使用授权。"),
  small("版本：v0.2　｜　状态：专家评审稿　｜　对应规格：PREFACE-00　｜　版本日期：2026-10-28", { after: 0 }),
];

const doc = new Document({
  creator: "AIOS101 课程建设",
  title: "AI 开源通识：序言 v0.2 专家评审稿",
  subject: "面向所有大学生的 AI 通识课教材序言",
  description: "从一次 AI 提问进入模型供应链与开源生态，含 OpenDipper 实景截图与全书学习地图。",
  keywords: "AI 通识教育, 开源, OpenDipper, AIOS101",
  styles: {
    default: {
      document: { run: { font: bodyFont, size: 24, color: INK, language: { eastAsia: "zh-CN" } } },
    },
    paragraphStyles: [
      {
        id: "BodyText",
        name: "Body Text",
        basedOn: "Normal",
        next: "BodyText",
        run: { font: bodyFont, size: 24, color: INK },
        paragraph: {
          alignment: AlignmentType.JUSTIFIED,
          indent: { firstLine: 480 },
          spacing: { after: 150, line: 360 },
          widowControl: true,
        },
      },
      {
        id: "ListParagraph",
        name: "List Paragraph",
        basedOn: "BodyText",
        next: "ListParagraph",
        numbering: undefined,
        paragraph: {
          indent: { left: 720, firstLine: 0, hanging: 0 },
          spacing: { after: 100, line: 340 },
          numbering: { reference: "starting-questions", level: 0 },
        },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "starting-questions",
      levels: [{
        level: 0,
        format: "decimal",
        text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    }],
  },
  footnotes: {
    1: { children: [footnoteParagraph([
      run("X-lab：OpenDipper 项目中文说明，固定提交 8fa36b5，应用版本 1.16.1，读取日期：2026-10-28。用于说明模块、教学入口及“公开可下载不等于开源”等边界。来源登记：SRC-2026-001。", { size: 18 }),
      linkedText("固定来源", "https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/README.zh-CN.md"),
    ])] },
    2: { children: [footnoteParagraph([
      run("X-lab：Open Galaxy／开源星系契约，固定提交 8fa36b5，发布实现 1.5.1，读取日期：2026-10-28。用于说明记录关系、推断关系与软件依赖链之间的区别。来源登记：SRC-2026-002。", { size: 18 }),
      linkedText("固定来源", "https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/OPEN_GALAXY.md"),
    ])] },
    3: { children: [footnoteParagraph([
      run("X-lab：OpenShare and GOSD observed evidence，固定提交 8fa36b5，读取日期：2026-10-28。用于说明数据来源、独立观察时钟、覆盖范围、分母及缺失值处理原则。来源登记：SRC-2026-003。", { size: 18 }),
      linkedText("固定来源", "https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/DATA_EVIDENCE.md"),
    ])] },
    4: { children: [footnoteParagraph([
      run("X-lab：OpenDipper 开源星系浅色实景截图及截图说明，固定提交 8fa36b5，应用版本 1.6.0，截图日期：2026-10-27，读取日期：2026-10-28。来源登记：SRC-2026-004。根应用许可未选定，本稿仅限专家评审。", { size: 18 }),
      linkedText("截图", "https://raw.githubusercontent.com/X-lab2017/open-dipper/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/assets/opendipper-1.6.0-galaxy-light-20261027.jpg"),
      run("；", { size: 18 }),
      linkedText("说明", "https://github.com/X-lab2017/open-dipper/blob/8fa36b5d19f9bdc01fe1505f153c19b3c499c712/docs/assets/README.md"),
    ])] },
  },
  sections: [
    {
      properties: { page: portraitPage },
      children: [
        new Paragraph({ spacing: { before: 1050, after: 260 }, children: [new TextRun({ text: "AIOS101 · 教材建设", font: headingFont, size: 20, bold: true, color: GREEN, characterSpacing: 30 })] }),
        new Paragraph({ spacing: { after: 130 }, children: [new TextRun({ text: "AI 开源通识", font: headingFont, size: 64, bold: true, color: INK })] }),
        new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "序　言", font: headingFont, size: 40, bold: true, color: GREEN })] }),
        new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 18, color: GOLD, space: 16 } },
          spacing: { before: 180, after: 250 },
          children: [new TextRun({ text: "从一次提问，看见一个开放的世界", font: headingFont, size: 31, color: INK })],
        }),
        new Paragraph({ spacing: { after: 120 }, children: [run("面向所有大学生的 AI 通识课", { size: 25, color: MUTED })] }),
        new Paragraph({ spacing: { after: 850, line: 340 }, children: [run("以 AI 为学习对象，以开源为认识论、方法论和实践方式", { size: 22, color: MUTED })] }),
        new Table({
          width: { size: 9000, type: WidthType.DXA },
          columnWidths: [9000],
          rows: [new TableRow({ children: [new TableCell({
            width: { size: 9000, type: WidthType.DXA },
            margins: { top: 230, bottom: 230, left: 260, right: 260 },
            shading: { type: ShadingType.CLEAR, fill: "F1F5F2", color: "auto" },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
              bottom: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
              left: { style: BorderStyle.SINGLE, size: 16, color: GREEN },
              right: { style: BorderStyle.SINGLE, size: 4, color: LIGHT },
            },
            children: [
              small("专家评审稿 · v0.2", { size: 23, bold: true, color: GREEN, after: 110 }),
              small("评审重点：通识定位 · 导入逻辑 · 内容准确性 · 地图可读性", { size: 20, color: INK, after: 90 }),
              small("2026 年 10 月", { size: 18, color: MUTED, after: 0 }),
            ],
          })] })],
        }),
      ],
    },
    {
      properties: { page: { ...portraitPage, pageNumbers: { start: 1 } }, headers: { default: header }, footers: { default: footer } },
      children: mainChildren,
    },
    {
      properties: { page: landscapePage, headers: { default: header }, footers: { default: footer } },
      children: mapChildren,
    },
    {
      properties: { page: portraitPage, headers: { default: header }, footers: { default: footer } },
      children: finalChildren,
    },
  ],
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`Created ${outputPath} (${buffer.length} bytes)`);
});
