const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  Header,
  HeadingLevel,
  Packer,
  PageNumber,
  Paragraph,
  TextRun,
} = require("docx");

const outputPath = process.argv[2];
if (!outputPath) throw new Error("Usage: node create_preface_clean_docx.js /absolute/path/output.docx");

const sourcePath = path.resolve(__dirname, "..", "textbook", "preface.md");
const markdown = fs.readFileSync(sourcePath, "utf8");
const GREEN = "315C4D";
const INK = "26332E";
const MUTED = "6B7570";
const LIGHT = "D9E1DD";
const bodyFont = { ascii: "Aptos", hAnsi: "Aptos", eastAsia: "宋体", cs: "Aptos" };
const headingFont = { ascii: "Aptos Display", hAnsi: "Aptos Display", eastAsia: "微软雅黑", cs: "Aptos" };

const run = (text, options = {}) => new TextRun({
  text,
  font: bodyFont,
  size: 24,
  color: INK,
  ...options,
});

const para = (children, options = {}) => new Paragraph({
  spacing: { after: 150, line: 360 },
  ...options,
  children: Array.isArray(children) ? children : [children],
});

const bodyPara = (text, options = {}) => para(run(text), {
  alignment: AlignmentType.JUSTIFIED,
  indent: { firstLine: 480 },
  widowControl: true,
  ...options,
});

const headingPara = (text) => para(
  run(text, { font: headingFont, size: 30, bold: true, color: GREEN }),
  {
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    spacing: { before: 330, after: 150, line: 320 },
  },
);

const captionPara = (text) => para(
  run(text, { font: headingFont, size: 21, color: MUTED }),
  {
    alignment: AlignmentType.CENTER,
    spacing: { before: 150, after: 210, line: 280 },
    keepLines: true,
  },
);

const lines = markdown.split(/\r?\n/);
const titleLine = lines.find((line) => line.startsWith("# "));
if (!titleLine) throw new Error("The Markdown source has no level-one title");
const title = titleLine.slice(2).trim();

const children = [
  para(run(title, { font: headingFont, size: 42, bold: true, color: INK }), {
    spacing: { before: 100, after: 110, line: 400 },
  }),
  para(run("《AI 开源通识》序言 · v0.3 · 内容评审稿", { font: headingFont, size: 20, color: MUTED }), {
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LIGHT, space: 12 } },
    spacing: { after: 330, line: 280 },
  }),
];

let bodyCount = 0;
for (const rawLine of lines) {
  const line = rawLine.trim();
  if (!line || line.startsWith(">") || line.startsWith("# ")) continue;
  if (line.startsWith("## ")) {
    children.push(headingPara(line.slice(3).trim()));
    continue;
  }
  const numbered = line.match(/^\d+\.\s+(.+)$/);
  if (numbered) {
    children.push(para(run(numbered[1]), {
      numbering: { reference: "starting-questions", level: 0 },
      spacing: { after: 110, line: 340 },
    }));
    continue;
  }
  if (/^图 0-[12]　/.test(line)) {
    children.push(captionPara(line));
    continue;
  }
  bodyCount += 1;
  if (bodyCount === 1) {
    children.push(para(run(line, { size: 28, bold: true, color: GREEN }), {
      spacing: { after: 240, line: 380 },
    }));
  } else if (line.startsWith("愿这本书帮助你")) {
    children.push(para(run(line, { size: 26, bold: true, color: GREEN }), {
      spacing: { before: 200, after: 160, line: 380 },
    }));
  } else {
    children.push(bodyPara(line));
  }
}

const header = new Header({
  children: [para(
    run("AI 开源通识　｜　序言 v0.3　｜　内容评审稿", { font: headingFont, size: 16, color: MUTED }),
    {
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LIGHT, space: 5 } },
      spacing: { after: 80, line: 240 },
    },
  )],
});

const footer = new Footer({
  children: [para(new TextRun({
    children: [PageNumber.CURRENT],
    font: headingFont,
    size: 16,
    color: MUTED,
  }), {
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 0, line: 240 },
  })],
});

const doc = new Document({
  creator: "AIOS101 课程建设",
  title: "AI 开源通识：序言 v0.3 清爽内容评审稿",
  subject: "面向所有大学生的 AI 通识课教材序言内容评审",
  description: "完整序言纯文本评审版，仅保留图号与图题占位。",
  keywords: "AI 通识教育, 开源, 序言, 内容评审, AIOS101",
  features: { updateFields: false },
  styles: {
    default: {
      document: {
        run: { font: bodyFont, size: 24, color: INK, language: { eastAsia: "zh-CN" } },
      },
    },
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
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1250, right: 1350, bottom: 1250, left: 1350, header: 560, footer: 560 },
        pageNumbers: { start: 1 },
      },
    },
    headers: { default: header },
    footers: { default: footer },
    children,
  }],
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`Created ${outputPath} (${buffer.length} bytes)`);
});
