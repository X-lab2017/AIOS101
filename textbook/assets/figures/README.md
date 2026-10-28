# 教材图版：当前交付与维护

**[当前图号与图题索引](INDEX.md)是交付入口**；正文的规范图注和 [manifest.json](manifest.json)共同确定身份、文件和插入位置。版本与数量见[当前状态](../../../docs/STATUS.md)，不在多处手写计数。

## 修改一幅图

先说明它帮助读者理解什么，再决定保留、重绘、补充或退出正文。同步正文图题与图注、manifest、压缩 WebP、可用矢量和描述性 alt；结构图同步相应 Mermaid 文件和正文折叠源码。运行：

```bash
python scripts/figures/catalog.py --write
python scripts/sync_status.py --write
python scripts/check_all.py
```

手绘科技出版风格延续暖纸白、墨蓝、靛蓝、青绿和少量珊瑚橙；具体画法服从教学任务，不把所有图做成同一套框图。精确关系和数值必须可以核对，概念隐喻标明适用边界。真实材料不可生成式改写。

## 来源与授权边界

- [人物肖像参考](portrait-sources.md)：GNU／Linux／开源历史人物，原照片不随本仓库分发。
- [第四至第六章材料来源](ch04-ch06-sources.md)：固定论文、README、规范及其截图边界。
- [自学版图版修订与提示](sources/visual-learning-2026-10-29.md)：概念插画、可复算图与制作方法。
- [OpenDipper 双图来源](sources/preface-opendipper-2026-10-29.md)：原始截图、无损核对、手绘装帧与矢量导读。
- [全课来源登记](../../../specs/source-register.md)：事实、版本与核验状态。

DeepSeek 固定 README 不冻结外部模型文件；AIInfra Issue #386 与 PR #364 是独立证据；GOSD 分类不是依赖，下载量不是能力排名；OpenDipper 的记录、推断、模拟、采集期和界面日期分别说明。

维护者授权的仓库与 Pages 评审不改变第三方许可。正式出版素材条件与课程统一许可尚需维护者确定，保留原署名和来源。

## 当前资产与历史输入

- `manifest.json`：当前正文图。Pages 仅发布其 `file`、`zoomFile`、`originalFile` 指向的资产。
- `INDEX.md`：自动生成的统一图号、题名、位置与链接。
- `retired.json`：4-8、5-4、6-9 的退出原因，历史文件可查；0-1、0-2、A-1 为更早撤销的规划号，同样不复用。
- `vector/`、`mermaid/`、`sources/`：当前及历史可编辑源、证据和生成输入。清单外文件可能仍用于重现，不可按“未发布”自动删除。
- [历史制作记录](../../../docs/history/figure-production.md)与[第二篇初版绘制要求](../../../docs/history/ch04-ch06-figure-brief.md)：保留过程，不用于判断当前图数或题名。

网页压缩图、放大源和原图用途不同。先在正文中看阅读节奏，再在放大页看细节；仅上传大图并不能保证手机阅读清晰。
