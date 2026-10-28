# 构建、检查与素材生成

## 日常编辑

```bash
python scripts/figures/catalog.py --write
python scripts/sync_status.py --write
python scripts/check_all.py
```

统一检查使用 Python 3.10+ 与 Node.js 18+，只用标准库；CI 使用 Python 3.12 与 Node.js 22。它校验品牌包、状态清单、构建、正文／图版、链接、阅读界面、旧数据兼容与脚本语法。`dist/` 为临时生成目录。

`catalog.py` 生成图版索引，`sync_status.py` 生成当前状态中的版本与图数。不要手改自动生成区；不带 `--write` 时只检查是否过时。

## 按需生成，不属于普通构建

| 工具 | 用途与环境 |
|---|---|
| `generate_course_brand.py`、`package_course_brand.py` | 品牌生产与固定包校验；生产需字体与图形依赖，日常仅运行 `--check` |
| `figures/self_study.py` | 第四至六章可复算教学图；依赖 Pillow、CairoSVG、字体和共享绘图模块 |
| `figures/preface_opendipper.py --help` | 原始截图、手绘外框与矢量导读合成；依赖 Pillow、CairoSVG、fontTools 和中文字体 |
| `figures/refine_review.py`、`refine_labels.py`、`optimize_gosd.py`、`subset_font.py` | 历次图版修订与字体处理；按来源记录使用其对应输入，不批量重跑覆盖新图 |
| `create_review_book_pdf.py --help` | PDF 导出；依赖 ReportLab、PyMuPDF、Pillow、pypdf 及脚本要求的中文字体环境变量；输出后必须重新验看 |
| `create_aios101_3h_deck.py` | 历史授课稿生成；需要其专用课件工具及输入，尚未适配当前图版 |

来源、提示、固定版本和历史输入见 `textbook/assets/figures/`。环境相关生成器不在 Pages CI 重跑；已提交并核验的图件供普通构建复用。若缺少输入或字体应如实记录，不伪造已重现。

已删除两个旧序言 Word 脚本及其专用 npm 依赖：它们固定了旧正文／旧版式，不能生成当前教材。恢复方法见维护记录。
