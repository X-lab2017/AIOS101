#!/usr/bin/env python3
"""AIOS101 仓库基础结构与 Markdown 静态检查（仅使用标准库）。"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "CONSTITUTION.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "README.md",
    "specs/README.md",
    "specs/course-spec.md",
    "specs/chapter-spec-template.md",
    "specs/activity-spec-template.md",
    "specs/content-evidence-spec.md",
    "specs/assessment-spec.md",
    "specs/presentation-spec.md",
    "specs/acceptance-spec.md",
    "specs/collaboration-spec.md",
    "specs/source-register.md",
    "specs/decision-record-template.md",
    "specs/change-request-template.md",
)

REQUIRED_SECTIONS = {
    "specs/course-spec.md": (
        "3. 学习成果框架",
        "4. 十二章对齐矩阵",
        "5. 内容层次规格",
        "6. 课程学习证据集",
        "7. 综合项目规格",
        "10. 课程级验收条件",
    ),
    "specs/chapter-spec-template.md": (
        "1. 章节定位",
        "2. 学习成果与评价对齐",
        "6. 章节活动清单",
        "7. 教材与讲义规格",
        "8. 评价设计",
        "11. 验收条件",
    ),
    "specs/activity-spec-template.md": (
        "1. 活动定位",
        "4. 安全、伦理与开放要求",
        "5. 活动流程",
        "6. 分层任务",
        "8. 学习证据与提交包",
        "9. 评价量规",
        "11. 活动验收",
    ),
    "specs/content-evidence-spec.md": (
        "3. 信息类型与证据要求",
        "4. 来源规范",
        "5. 数据与图表规范",
        "6. 技术与复现规范",
        "7. AI 辅助内容生产",
        "8. 许可与署名",
    ),
    "specs/assessment-spec.md": (
        "2. 学习成果与评价证据",
        "4. 通用四级量规",
        "6. 团队与个人评价",
        "7. AI 使用与学术诚信",
        "10. 评价验收清单",
    ),
    "specs/presentation-spec.md": (
        "2. 单一事实来源与产物关系",
        "3. 教材规范",
        "4. 讲义规范",
        "9. 可及性与多语言",
        "11. 展现验收清单",
    ),
    "specs/acceptance-spec.md": (
        "2. 就绪定义（Definition of Ready）",
        "3. 完成定义（Definition of Done）",
        "4. 质量门禁",
        "6. 问题等级与发布规则",
        "7. 验收记录模板",
        "8. 发布检查",
    ),
    "specs/collaboration-spec.md": (
        "2. 角色与责任",
        "3. 标准工作流程",
        "4. AI 协作者的强制规则",
        "5. 变更级别",
        "7. 评审要求",
        "9. 冲突处理",
    ),
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def relative_name(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def extract_link_destination(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split(maxsplit=1)[0] if target else ""


def main() -> int:
    errors: list[str] = []
    checked_links = 0

    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"缺少必需文件：{name}")

    markdown_files = sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.relative_to(ROOT).parts
    )
    markdown_text: dict[str, str] = {}

    for path in markdown_files:
        name = relative_name(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"无法读取 {name}：{exc}")
            continue
        markdown_text[name] = text

        for line_number, line in enumerate(text.splitlines(), start=1):
            if line != line.rstrip(" \t"):
                errors.append(f"{name}:{line_number} 存在行尾空格或制表符")

        for match in LINK_RE.finditer(text):
            destination = extract_link_destination(match.group(1))
            if not destination or destination.startswith("#"):
                continue

            parsed = urlsplit(destination)
            if parsed.scheme or destination.startswith("//"):
                continue

            relative_path = unquote(parsed.path)
            if not relative_path or Path(relative_path).is_absolute():
                continue

            checked_links += 1
            resolved = (path.parent / relative_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{name} 的相对链接越出仓库：{destination}")
                continue
            if not resolved.exists():
                line_number = text.count("\n", 0, match.start()) + 1
                errors.append(f"{name}:{line_number} 链接目标不存在：{destination}")

    for name, sections in REQUIRED_SECTIONS.items():
        text = markdown_text.get(name)
        if text is None:
            continue
        for section in sections:
            if not re.search(rf"^## {re.escape(section)}\s*$", text, re.MULTILINE):
                errors.append(f"{name} 缺少必要章节：## {section}")

    course_text = markdown_text.get("specs/course-spec.md")
    if course_text is not None:
        matrix_match = re.search(
            r"^## 4\. 十二章对齐矩阵\s*$(.*?)(?=^## 5\.)",
            course_text,
            re.MULTILINE | re.DOTALL,
        )
        if matrix_match is None:
            errors.append("specs/course-spec.md 无法定位十二章对齐矩阵")
        else:
            actual = re.findall(r"^\| (CH\d{2}) \|", matrix_match.group(1), re.MULTILINE)
            expected = [f"CH{number:02d}" for number in range(1, 13)]
            if actual != expected:
                errors.append(
                    "specs/course-spec.md 章节编号必须按 CH01—CH12 完整顺序排列；"
                    f"当前为：{', '.join(actual) or '无'}"
                )

    if errors:
        print(f"检查失败，共发现 {len(errors)} 个问题：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"检查通过：{len(markdown_files)} 个 Markdown 文件，{checked_links} 个相对链接。")
    print("必需文件、核心章节与 CH01—CH12 顺序均符合要求。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
