#!/usr/bin/env python3
"""Build the printable AIOS101 review book from canonical Markdown sources."""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
from pathlib import Path

import fitz
from PIL import Image as PILImage
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    LongTable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    TableStyle,
    XPreformatted,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK = ROOT / "textbook"
OUTPUT = ROOT / "deliverables" / "AI开源通识_序言与前六章_图文评审版_2026-10-29.pdf"
ASSET_DIR = ROOT / "deliverables" / ".review-book-assets"
REPORT = ROOT / "deliverables" / "AI开源通识_序言与前六章_排版核验.json"
PAGE_W, PAGE_H = A4
LEFT = 25 * mm
RIGHT = 22 * mm
TOP = 24 * mm
BOTTOM = 22 * mm
BODY_W = PAGE_W - LEFT - RIGHT

PAPER = HexColor("#F6F3EB")
INK = HexColor("#1D2433")
INDIGO = HexColor("#5146D9")
INDIGO_DARK = HexColor("#30288F")
CORAL = HexColor("#F27A59")
LAVENDER = HexColor("#E7E3FC")
TEAL = HexColor("#3F958D")
MUTED = HexColor("#656577")
RULE = HexColor("#CEC9DD")
LIGHT = HexColor("#F5F5F5")
LINK = HexColor("#4438B7")

CHAPTERS = [
    TEXTBOOK / "chapters" / "CH01-why-ai-open-source-literacy.md",
    TEXTBOOK / "chapters" / "CH02-open-source-mechanisms.md",
    TEXTBOOK / "chapters" / "CH03-ai-open-source-ecosystem.md",
    TEXTBOOK / "chapters" / "CH04-data-to-models.md",
    TEXTBOOK / "chapters" / "CH05-training-to-inference.md",
    TEXTBOOK / "chapters" / "CH06-model-to-agents.md",
]
PREFACE = TEXTBOOK / "preface.md"
APPENDIX = TEXTBOOK / "appendices" / "APP-A-repository-snapshots.md"


def register_fonts() -> None:
    regular = os.environ.get("DAIMON_CJK_FONT_REGULAR")
    bold = os.environ.get("DAIMON_CJK_FONT_BOLD")
    if not regular or not bold:
        raise RuntimeError("Managed CJK fonts are unavailable")
    pdfmetrics.registerFont(TTFont("DaimonCJK", regular))
    pdfmetrics.registerFont(TTFont("DaimonCJK-Bold", bold))
    pdfmetrics.registerFontFamily(
        "DaimonCJK",
        normal="DaimonCJK",
        bold="DaimonCJK-Bold",
        italic="DaimonCJK",
        boldItalic="DaimonCJK-Bold",
    )


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "BookBody",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=10.5,
            leading=18,
            textColor=INK,
            alignment=TA_JUSTIFY,
            wordWrap="CJK",
            firstLineIndent=21,
            spaceAfter=5,
            allowWidows=0,
            allowOrphans=0,
        ),
        "lead": ParagraphStyle(
            "BookLead",
            parent=base["Normal"],
            fontName="DaimonCJK-Bold",
            fontSize=10.8,
            leading=18.5,
            textColor=INDIGO_DARK,
            alignment=TA_JUSTIFY,
            wordWrap="CJK",
            leftIndent=10,
            rightIndent=10,
            spaceBefore=5,
            spaceAfter=9,
        ),
        "chapter": ParagraphStyle(
            "BookChapter",
            parent=base["Heading1"],
            fontName="DaimonCJK-Bold",
            fontSize=21,
            leading=31,
            textColor=INK,
            wordWrap="CJK",
            spaceBefore=5 * mm,
            spaceAfter=11 * mm,
            keepWithNext=True,
        ),
        "section": ParagraphStyle(
            "BookSection",
            parent=base["Heading2"],
            fontName="DaimonCJK-Bold",
            fontSize=14.5,
            leading=22,
            textColor=INDIGO_DARK,
            wordWrap="CJK",
            spaceBefore=8 * mm,
            spaceAfter=3.5 * mm,
            keepWithNext=True,
        ),
        "subsection": ParagraphStyle(
            "BookSubsection",
            parent=base["Heading3"],
            fontName="DaimonCJK-Bold",
            fontSize=11.5,
            leading=18,
            textColor=INK,
            wordWrap="CJK",
            spaceBefore=5 * mm,
            spaceAfter=2 * mm,
            keepWithNext=True,
        ),
        "part": ParagraphStyle(
            "PartTitle",
            parent=base["Heading1"],
            fontName="DaimonCJK-Bold",
            fontSize=25,
            leading=38,
            textColor=INDIGO_DARK,
            alignment=TA_LEFT,
            wordWrap="CJK",
            spaceAfter=10 * mm,
        ),
        "part_body": ParagraphStyle(
            "PartBody",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=12,
            leading=23,
            textColor=MUTED,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "BookBullet",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=10.3,
            leading=17.5,
            textColor=INK,
            wordWrap="CJK",
            leftIndent=20,
            firstLineIndent=-12,
            spaceAfter=3,
        ),
        "number": ParagraphStyle(
            "BookNumber",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=10.3,
            leading=17.5,
            textColor=INK,
            wordWrap="CJK",
            leftIndent=25,
            firstLineIndent=-20,
            spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "BookQuote",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=10,
            leading=17.5,
            textColor=INDIGO_DARK,
            wordWrap="CJK",
            leftIndent=18,
            rightIndent=12,
            borderColor=INDIGO,
            borderWidth=0,
            borderPadding=0,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "BookCaption",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=8.8,
            leading=14,
            textColor=MUTED,
            alignment=TA_CENTER,
            wordWrap="CJK",
            spaceBefore=2.5 * mm,
            spaceAfter=5 * mm,
        ),
        "table": ParagraphStyle(
            "BookTable",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=8.4,
            leading=13,
            textColor=INK,
            wordWrap="CJK",
            spaceAfter=0,
        ),
        "table_head": ParagraphStyle(
            "BookTableHead",
            parent=base["Normal"],
            fontName="DaimonCJK-Bold",
            fontSize=8.5,
            leading=13,
            textColor=INK,
            wordWrap="CJK",
            spaceAfter=0,
        ),
        "code": ParagraphStyle(
            "BookCode",
            parent=base["Code"],
            fontName="DaimonCJK",
            fontSize=8,
            leading=12,
            textColor=INK,
            backColor=LIGHT,
            borderPadding=6,
            leftIndent=5,
            rightIndent=5,
            spaceBefore=3 * mm,
            spaceAfter=4 * mm,
        ),
        "toc_title": ParagraphStyle(
            "TOCTitle",
            parent=base["Heading1"],
            fontName="DaimonCJK-Bold",
            fontSize=24,
            leading=34,
            textColor=INK,
            spaceAfter=12 * mm,
        ),
        "title_small": ParagraphStyle(
            "TitleSmall",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=11,
            leading=18,
            textColor=INDIGO,
            alignment=TA_CENTER,
            spaceAfter=16 * mm,
        ),
        "title_main": ParagraphStyle(
            "TitleMain",
            parent=base["Title"],
            fontName="DaimonCJK-Bold",
            fontSize=34,
            leading=46,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=6 * mm,
        ),
        "title_sub": ParagraphStyle(
            "TitleSub",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=15,
            leading=25,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=5 * mm,
        ),
        "note": ParagraphStyle(
            "BookNote",
            parent=base["Normal"],
            fontName="DaimonCJK",
            fontSize=9.5,
            leading=17,
            textColor=MUTED,
            wordWrap="CJK",
            spaceAfter=4 * mm,
        ),
    }


class BookmarkFlowable(Flowable):
    def __init__(self, name: str, title: str | None = None, level: int = 2):
        super().__init__()
        self.name = name
        self.title = title
        self.level = level
        self.width = 0
        self.height = 0

    def wrap(self, avail_width, avail_height):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.name)
        if self.title:
            self.canv.addOutlineEntry(self.title, self.name, level=self.level, closed=False)


class LearningMap(Flowable):
    """A printable vector map derived only from the approved four-part outline."""

    def __init__(self, width=BODY_W, height=122 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        c.setFont("DaimonCJK-Bold", 10)
        c.setFillColor(INK)
        c.drawString(0, h - 12, "学习主线")
        stages = ["使用", "理解", "探究", "贡献", "创造"]
        gap = 5 * mm
        box_w = (w - gap * 4) / 5
        y = h - 34
        for i, label in enumerate(stages):
            x = i * (box_w + gap)
            c.setFillColor(LAVENDER if i % 2 == 0 else PAPER)
            c.setStrokeColor(INDIGO)
            c.rect(x, y, box_w, 17, fill=1, stroke=1)
            c.setFillColor(INDIGO_DARK)
            c.setFont("DaimonCJK-Bold", 9.5)
            c.drawCentredString(x + box_w / 2, y + 5, label)
            if i < 4:
                c.setStrokeColor(CORAL)
                c.line(x + box_w + 1, y + 8.5, x + box_w + gap - 1, y + 8.5)
        c.setFillColor(INK)
        c.setFont("DaimonCJK-Bold", 10)
        c.drawString(0, h - 58, "四篇十二章")
        parts = [
            ("第一篇　认识开源", "第 1—3 章", "开放 · 复用 · 协作 · 生态"),
            ("第二篇　理解 AI", "第 4—6 章", "数据 · 模型 · 推理 · 智能体"),
            ("第三篇　探究证据", "第 7—9 章", "开放度 · 复现 · 生态数据"),
            ("第四篇　共同创造", "第 10—12 章", "贡献 · 项目 · 负责任发布"),
        ]
        top = h - 78
        row_h = 49
        for i, (title, chapters, terms) in enumerate(parts):
            yy = top - i * (row_h + 8) - row_h
            c.setFillColor(PAPER if i % 2 == 0 else LIGHT)
            c.setStrokeColor(RULE)
            c.rect(0, yy, w, row_h, fill=1, stroke=1)
            c.setFillColor(INDIGO if i < 3 else TEAL)
            c.rect(0, yy, 5, row_h, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("DaimonCJK-Bold", 10.5)
            c.drawString(14, yy + 29, title)
            c.setFillColor(MUTED)
            c.setFont("DaimonCJK", 9)
            c.drawRightString(w - 12, yy + 29, chapters)
            c.drawString(14, yy + 11, terms)
        c.restoreState()


class RepositoryMap(Flowable):
    def __init__(self, width=BODY_W, height=64 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.saveState()
        c.setFillColor(PAPER)
        c.setStrokeColor(INDIGO)
        c.rect(0, 0, w, h, fill=1, stroke=1)
        c.setFillColor(INDIGO_DARK)
        c.setFont("DaimonCJK-Bold", 11)
        c.drawCentredString(w / 2, h - 22, "公开仓库：文件、历史与协作记录")
        items = [
            ("README", "项目入口"),
            ("LICENSE", "使用条件"),
            ("提交与发布", "固定版本"),
            ("Issue", "问题讨论"),
            ("Pull Request", "变更评审"),
        ]
        gap = 4 * mm
        bw = (w - 20 - gap * 4) / 5
        yy = 30
        for i, (name, note) in enumerate(items):
            xx = 10 + i * (bw + gap)
            c.setFillColor(colors.white)
            c.setStrokeColor(RULE)
            c.rect(xx, yy, bw, 68, fill=1, stroke=1)
            c.setFillColor(INK)
            c.setFont("DaimonCJK-Bold", 8.5)
            c.drawCentredString(xx + bw / 2, yy + 43, name)
            c.setFillColor(MUTED)
            c.setFont("DaimonCJK", 8)
            c.drawCentredString(xx + bw / 2, yy + 22, note)
        c.setFillColor(MUTED)
        c.setFont("DaimonCJK", 8.5)
        c.drawCentredString(w / 2, 13, "公开可见只是观察起点；开放许可、固定版本与协作过程需要分别核查。")
        c.restoreState()


class ReviewBookDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and hasattr(flowable, "_toc_level"):
            level = flowable._toc_level
            text = flowable._toc_text
            key = flowable._bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


def svg_to_png(source: Path, target: Path, scale=2.0) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(stream=source.read_bytes(), filetype="svg")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    pix.save(target)
    doc.close()
    return target


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    logo = ASSET_DIR / "course-logo.png"
    canvas.drawImage(str(logo), 24 * mm, PAGE_H - 45 * mm, width=88 * mm, height=22 * mm, mask="auto")
    canvas.setFillColor(CORAL)
    canvas.rect(24 * mm, PAGE_H - 72 * mm, 9 * mm, 2.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("DaimonCJK-Bold", 35)
    canvas.drawString(24 * mm, PAGE_H - 103 * mm, "AI 开源通识")
    canvas.setFillColor(INDIGO)
    canvas.setFont("DaimonCJK", 14)
    canvas.drawString(25 * mm, PAGE_H - 117 * mm, "AI & Open Source Literacy")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.8)
    canvas.line(24 * mm, PAGE_H - 130 * mm, PAGE_W - 24 * mm, PAGE_H - 130 * mm)
    canvas.setFillColor(INK)
    canvas.setFont("DaimonCJK-Bold", 19)
    canvas.drawString(24 * mm, PAGE_H - 151 * mm, "序言与前六章")
    canvas.setFillColor(MUTED)
    canvas.setFont("DaimonCJK", 11)
    canvas.drawString(24 * mm, PAGE_H - 164 * mm, "图文评审版 · 专家评审样书")

    x0, y0 = 26 * mm, 45 * mm
    ww, hh = 155 * mm, 57 * mm
    canvas.setFillColor(LAVENDER)
    canvas.setStrokeColor(colors.transparent)
    canvas.saveState()
    canvas.translate(x0, y0)
    p = canvas.beginPath()
    p.moveTo(0, hh * 0.70)
    p.lineTo(ww * 0.48, hh)
    p.lineTo(ww * 0.48, hh * 0.16)
    p.lineTo(0, 0)
    p.close()
    canvas.drawPath(p, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    p = canvas.beginPath()
    p.moveTo(ww, hh * 0.70)
    p.lineTo(ww * 0.52, hh)
    p.lineTo(ww * 0.52, hh * 0.16)
    p.lineTo(ww, 0)
    p.close()
    canvas.drawPath(p, fill=1, stroke=0)
    canvas.setFillColor(CORAL)
    canvas.rect(ww * 0.485, hh * 0.92, ww * 0.03, hh * 0.16, fill=1, stroke=0)
    canvas.restoreState()
    canvas.setFillColor(INK)
    canvas.setFont("DaimonCJK-Bold", 10.5)
    canvas.drawString(24 * mm, 23 * mm, "X-lab AI 出品")
    canvas.setFillColor(MUTED)
    canvas.setFont("DaimonCJK", 9.5)
    canvas.drawRightString(PAGE_W - 24 * mm, 23 * mm, "2026 年 10 月")
    canvas.restoreState()


def draw_body_page(canvas, doc):
    canvas.saveState()
    canvas.setTitle("AI 开源通识：序言与前六章（图文评审版）")
    canvas.setAuthor("X-lab AI")
    canvas.setSubject("AI 开源通识教材专家评审样书")
    if doc.page >= 4:
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT, PAGE_H - 15 * mm, PAGE_W - RIGHT, PAGE_H - 15 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("DaimonCJK", 8)
        canvas.drawString(LEFT, PAGE_H - 12 * mm, "AI 开源通识")
        canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 12 * mm, "序言与前六章 · 图文评审版")
        canvas.drawCentredString(PAGE_W / 2, 11 * mm, str(doc.page))
    canvas.restoreState()


def plain_text(markdown: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", markdown)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    return html.unescape(text)


def inline_markup(text: str, source: Path) -> str:
    placeholders: dict[str, str] = {}

    def stash(value: str) -> str:
        key = f"@@PH{len(placeholders)}@@"
        placeholders[key] = value
        return key

    text = html.escape(text, quote=False)

    def code_repl(match):
        return stash(f'<font color="#4438B7">{match.group(1)}</font>')

    text = re.sub(r"`([^`]+)`", code_repl, text)

    def link_repl(match):
        label, target = match.group(1), match.group(2)
        if target.startswith(("https://", "http://")):
            return stash(f'<a href="{html.escape(target, quote=True)}" color="#4438B7">{label}</a>')
        resolved = (source.parent / target).resolve()
        anchors = {
            APPENDIX.resolve(): "appendix-a",
            PREFACE.resolve(): "preface",
            **{p.resolve(): f"chapter-{i}" for i, p in enumerate(CHAPTERS, 1)},
        }
        if resolved in anchors:
            return stash(f'<a href="#{anchors[resolved]}" color="#4438B7">{label}</a>')
        return label

    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    def figure_repl(match):
        number = match.group(1)
        return stash(f'<a href="#fig-{number}" color="#1D2433">图 {number}</a>')

    text = re.sub(r"图\s+([1-6]-[0-9]+|0-[12]|A-1)(?![0-9-])", figure_repl, text)
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def make_heading(text: str, style: ParagraphStyle, toc_level: int | None, bookmark: str) -> Paragraph:
    p = Paragraph(f'<a name="{bookmark}"/>{inline_markup(text, ROOT)}', style)
    if toc_level is not None:
        p._toc_level = toc_level
        p._toc_text = plain_text(text)
        p._bookmark = bookmark
    return p


def image_flowable(path: Path, max_height=150 * mm) -> Image:
    print_path = path
    if path.suffix.lower() == ".webp":
        print_path = ASSET_DIR / "print-images" / f"{path.stem}.jpg"
        print_path.parent.mkdir(parents=True, exist_ok=True)
        if not print_path.exists() or print_path.stat().st_mtime < path.stat().st_mtime:
            with PILImage.open(path) as source_image:
                source_image = source_image.convert("RGB")
                if source_image.width > 2000:
                    target_height = round(source_image.height * 2000 / source_image.width)
                    source_image = source_image.resize((2000, target_height), PILImage.Resampling.LANCZOS)
                source_image.save(print_path, "JPEG", quality=91, subsampling=0, optimize=True)
    with PILImage.open(print_path) as im:
        width, height = im.size
    scale = min(BODY_W / width, max_height / height)
    result = Image(str(print_path), width=width * scale, height=height * scale)
    result.hAlign = "CENTER"
    return result


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip().replace(r"\|", "|") for cell in stripped.split("|")]


def visual_length(text: str) -> int:
    return sum(2 if ord(ch) > 127 else 1 for ch in plain_text(text))


def make_table(rows: list[list[str]], source: Path, styles) -> LongTable:
    columns = max(len(row) for row in rows)
    normalized = [row + [""] * (columns - len(row)) for row in rows]
    lengths = []
    for col in range(columns):
        longest = max(visual_length(row[col]) for row in normalized)
        lengths.append(max(3.0, min(10.0, longest ** 0.5)))
    total = sum(lengths)
    widths = [BODY_W * weight / total for weight in lengths]
    data = []
    for r, row in enumerate(normalized):
        style = styles["table_head"] if r == 0 else styles["table"]
        data.append([Paragraph(inline_markup(cell, source), style) for cell in row])
    table = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 0.65, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 1.2, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


class MarkdownRenderer:
    def __init__(self, styles):
        self.styles = styles
        self.figure_ids: list[str] = []
        self.table_count = 0
        self.chapter_count = 0

    def render(self, source: Path, anchor: str, chapter: bool = True) -> list[Flowable]:
        lines = source.read_text(encoding="utf-8").splitlines()
        story: list[Flowable] = []
        i = 0
        in_details = False
        heading_count = 0
        while i < len(lines):
            raw = lines[i]
            line = raw.strip()
            if "<details>" in line:
                in_details = True
                i += 1
                continue
            if in_details:
                if "</details>" in line:
                    in_details = False
                i += 1
                continue
            if not line:
                i += 1
                continue
            if line.startswith("#"):
                match = re.match(r"^(#{1,3})\s+(.+)$", line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2)
                    heading_count += 1
                    if level == 1:
                        style = self.styles["chapter"]
                        story.append(make_heading(text, style, 0, anchor))
                        if chapter:
                            self.chapter_count += 1
                    elif level == 2:
                        bookmark = f"{anchor}-s{heading_count}"
                        story.append(make_heading(text, self.styles["section"], 1, bookmark))
                    else:
                        bookmark = f"{anchor}-s{heading_count}"
                        story.append(make_heading(text, self.styles["subsection"], None, bookmark))
                    i += 1
                    continue
            if re.match(r"^>\s*(版本|状态|对应规格|用途)：", line):
                i += 1
                continue
            if line == ">":
                i += 1
                continue
            if line.startswith(">"):
                quote = re.sub(r"^>\s?", "", line)
                story.append(Paragraph(inline_markup(quote, source), self.styles["quote"]))
                i += 1
                continue
            if line.startswith("```"):
                language = line[3:].strip()
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1
                import textwrap
                wrapped_lines = []
                for code_line in code_lines:
                    wrapped_lines.extend(textwrap.wrap(
                        code_line,
                        width=96,
                        replace_whitespace=False,
                        drop_whitespace=False,
                        break_long_words=True,
                        break_on_hyphens=False,
                    ) or [""])
                code = "\n".join(wrapped_lines)
                story.append(XPreformatted(html.escape(code), self.styles["code"]))
                continue
            image_match = re.match(r"^!\[([^]]*)\]\(([^)]+)\)$", line)
            if image_match:
                alt, target = image_match.groups()
                path = (source.parent / target).resolve()
                number_match = re.search(r"图\s+([0-9A-Z]+-[0-9]+)", alt)
                if number_match:
                    number = number_match.group(1)
                    self.figure_ids.append(number)
                    story.append(BookmarkFlowable(f"fig-{number}"))
                story.append(image_flowable(path))
                i += 1
                continue
            if line.startswith("图 0-1") and "图片占位" in line:
                path = TEXTBOOK / "assets" / "figures" / "AIOS101_Fig-03-08_opendipper-open-galaxy_v01.webp"
                story.append(BookmarkFlowable("fig-0-1"))
                story.append(image_flowable(path, max_height=138 * mm))
                story.append(Paragraph("图 0-1　OpenDipper 开源星系界面。", self.styles["caption"]))
                i += 1
                continue
            if line.startswith("图 0-2") and "图片占位" in line:
                story.append(BookmarkFlowable("fig-0-2"))
                story.append(LearningMap())
                story.append(Paragraph("图 0-2　《AI 开源通识》全书学习地图。", self.styles["caption"]))
                i += 1
                continue
            if line.startswith("图 A-1") and "图片占位" in line:
                story.append(BookmarkFlowable("fig-A-1"))
                story.append(RepositoryMap())
                story.append(Paragraph("图 A-1　公开仓库中的 README、许可、版本与协作入口。", self.styles["caption"]))
                i += 1
                continue
            caption_match = re.match(r"^图\s+([0-9A-Z]+-[0-9]+)　", line)
            if caption_match:
                story.append(Paragraph(inline_markup(line, source), self.styles["caption"]))
                i += 1
                continue
            if line.startswith("|"):
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    table_lines.append(lines[i].strip())
                    i += 1
                rows = [split_table_row(item) for item in table_lines]
                rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]
                story.append(Spacer(1, 2 * mm))
                story.append(make_table(rows, source, self.styles))
                story.append(Spacer(1, 4 * mm))
                self.table_count += 1
                continue
            bullet = re.match(r"^[-*]\s+(.+)$", line)
            if bullet:
                story.append(Paragraph("•　" + inline_markup(bullet.group(1), source), self.styles["bullet"]))
                i += 1
                continue
            numbered = re.match(r"^(\d+)\.\s+(.+)$", line)
            if numbered:
                story.append(Paragraph(numbered.group(1) + ".　" + inline_markup(numbered.group(2), source), self.styles["number"]))
                i += 1
                continue
            if re.fullmatch(r"\*\*.+\*\*", line):
                story.append(Paragraph(inline_markup(line, source), self.styles["lead"]))
            else:
                story.append(Paragraph(inline_markup(line, source), self.styles["body"]))
            i += 1
        return story


def add_part(story, number: str, title: str, description: str, anchor: str, styles):
    story.append(PageBreak())
    story.append(Spacer(1, 48 * mm))
    story.append(Paragraph(f"PART {number}", styles["title_small"]))
    story.append(make_heading(f"第{number}篇　{title}", styles["part"], 0, anchor))
    story.append(Paragraph(description.replace("\n", "<br/>"), styles["part_body"]))


def build_book() -> dict:
    register_fonts()
    styles = make_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    svg_to_png(ROOT / "site" / "assets" / "course" / "logo-light.svg", ASSET_DIR / "course-logo.png", 2.0)

    frame = Frame(LEFT, BOTTOM, BODY_W, PAGE_H - TOP - BOTTOM, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = ReviewBookDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="AI 开源通识：序言与前六章（图文评审版）",
        author="X-lab AI",
        subject="AI 开源通识教材专家评审样书",
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[Frame(0, 0, PAGE_W, PAGE_H, id="cover-frame")], onPage=draw_cover),
        PageTemplate(id="body", frames=[frame], onPage=draw_body_page),
    ])

    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    story: list[Flowable] = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]
    story.extend([
        Spacer(1, 38 * mm),
        Paragraph("AIOS101 · OPEN FOLIO", styles["title_small"]),
        Paragraph("AI 开源通识", styles["title_main"]),
        Paragraph("AI & Open Source Literacy", styles["title_sub"]),
        Spacer(1, 12 * mm),
        Paragraph("序言与前六章", styles["title_sub"]),
        Paragraph("图文评审版 · 专家评审样书", styles["title_sub"]),
        Spacer(1, 65 * mm),
        Paragraph("X-lab AI 出品", styles["title_sub"]),
        Paragraph("2026 年 10 月", styles["title_sub"]),
        PageBreak(),
        Paragraph("版本与使用说明", styles["chapter"]),
        Paragraph("本稿依据 AIOS101 仓库中的教材正本排版，用于课程内容、结构、图文呈现与教学适用性评审，不作为正式出版定稿。", styles["body"]),
        Paragraph("本册收录序言、第一篇（第 1—3 章）、第二篇（第 4—6 章）及附录 A。全书规划中的第 7—12 章不收录于本册。", styles["body"]),
        Spacer(1, 4 * mm),
    ])
    versions = [
        ["内容", "版本", "内容", "版本"],
        ["序言", "v0.4", "第 1 章", "v0.6"],
        ["第 2 章", "v0.6", "第 3 章", "v0.3"],
        ["第 4 章", "v0.3", "第 5 章", "v0.4"],
        ["第 6 章", "v0.3", "附录 A", "v0.1"],
    ]
    story.append(make_table(versions, ROOT / "README.md", styles))
    story.extend([
        Paragraph(f"正文来源提交：{source_commit}", styles["note"]),
        Paragraph("视觉基线：AIOS101 Visual Baseline v1.0.0（Open Folio／开卷）。封面沿用课程标志与品牌色，版式按 A4 印刷调整。", styles["note"]),
        Paragraph("打印建议：A4、双面、彩色、实际大小或适合可打印区域。黑白打印前请抽查截图与结构图的辨识度。", styles["note"]),
        Paragraph("版权与素材边界：正文和图版仍处于评审状态；第三方素材的正式出版授权、署名与修改说明须在出版前逐项复核。", styles["note"]),
        PageBreak(),
        Paragraph("本册目录", styles["toc_title"]),
    ])
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC0", fontName="DaimonCJK-Bold", fontSize=10.5, leading=19, leftIndent=0, firstLineIndent=0, textColor=INK, spaceBefore=3),
        ParagraphStyle("TOC1", fontName="DaimonCJK", fontSize=9.2, leading=16, leftIndent=16, firstLineIndent=0, textColor=MUTED),
    ]
    toc.dotsMinLevel = 0
    story.append(toc)

    renderer = MarkdownRenderer(styles)
    story.append(PageBreak())
    story.extend(renderer.render(PREFACE, "preface", chapter=False))
    add_part(story, "一", "认识开源：智能时代的共同创造", "第 1 章　智能时代为什么需要 AI 开源通识\n第 2 章　开源的本质：开放、复用、协作与公共价值\n第 3 章　AI 开源生态全景：数据、模型、代码、工具链与社区", "part-1", styles)
    for index, path in enumerate(CHAPTERS[:3], 1):
        story.append(PageBreak())
        story.extend(renderer.render(path, f"chapter-{index}"))
    add_part(story, "二", "理解 AI：从模型黑盒到开放系统", "第 4 章　从数据到模型：智能如何形成\n第 5 章　从训练到推理：AI 系统如何运行与评估\n第 6 章　从模型到智能体：检索、工具与人机协作", "part-2", styles)
    for index, path in enumerate(CHAPTERS[3:], 4):
        story.append(PageBreak())
        story.extend(renderer.render(path, f"chapter-{index}"))
    story.append(PageBreak())
    story.extend(renderer.render(APPENDIX, "appendix-a", chapter=False))

    manifest = json.loads((TEXTBOOK / "assets" / "figures" / "manifest.json").read_text(encoding="utf-8"))
    expected_figures = {entry["id"] for entry in manifest}
    actual_figures = set(renderer.figure_ids)
    missing = sorted(expected_figures - actual_figures)
    extra = sorted(actual_figures - expected_figures)
    if missing or extra or len(renderer.figure_ids) != len(expected_figures):
        raise RuntimeError(f"Figure parity failed: missing={missing}, extra={extra}, count={len(renderer.figure_ids)}")
    if renderer.chapter_count != 6:
        raise RuntimeError(f"Expected six chapters, got {renderer.chapter_count}")

    doc.multiBuild(story)
    reader = PdfReader(str(OUTPUT))
    page_count = len(reader.pages)
    all_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    required = ["AI 开源通识", "第 1 章", "第 2 章", "第 3 章", "第 4 章", "第 5 章", "第 6 章", "附录 A"]
    absent = [text for text in required if text not in all_text]
    if absent:
        raise RuntimeError(f"PDF text verification failed: {absent}")
    result = {
        "output": str(OUTPUT),
        "sourceCommit": source_commit,
        "pages": page_count,
        "chapters": renderer.chapter_count,
        "chapterFigures": len(renderer.figure_ids),
        "prefaceAndAppendixFigures": 3,
        "tables": renderer.table_count,
        "bytes": OUTPUT.stat().st_size,
        "requiredTextMissing": absent,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    build_book()
