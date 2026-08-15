# 2026-05-27 发布准备更新

本次更新面向下一个公开 release，重点是把 Visiomaster 从“能把 scene 渲染成 Visio”推进到“能围绕原图、复刻图和视觉审查形成可复现的重建闭环”。

## 相比上一个 release 的主要差异

- 增加源图暂存流程：用 `stage_source_image.py` 记录原图副本和 SHA-256，避免后续审查只依赖聊天记录、截图记忆或旧输出。
- 增加 review bundle 流程：用 `make_review_assets.py` 统一生成审查 manifest 和模板，明确本轮原图、复刻 PNG、scene 和 round 信息。
- 增加双图视觉审查合同：`review-contract.md` 和 `reviewer-two-image-prompt.md` 要求视觉 LLM 同时看原图和复刻 PNG，并输出具体差异、影响等级、focus region 和 checklist 引用。
- 增加 checklist gate：`review_checklist_gate.py` 检查视觉审查是否真的包含拓扑清单、视觉清单、失败项引用，而不是泛泛写“还需要优化”。
- 增加 review findings 到 rebuild brief 的转换：`review_findings_to_repair_plan.py` 把视觉问题转成下一轮整图重建输入。
- 增加 regeneration packet：`prepare_regeneration_packet.py` 将原图路径、当前复刻图、审查摘要和重建提示整理成下一轮 authoring 包。
- 增加 no-op gate：`round_noop_gate.py` 用于发现“只改了元数据、弱样式字段或渲染 PNG 没变化”的无效迭代。
- 强化严格复刻约束：`SKILL.md` 明确要求复杂图从原图视觉 inventory 和 source-pixel region plan 开始，不能把旧 scene 修一修就当作新版 skill 能力验证。
- 强化 renderer/validator/audit 对字体、公式、复杂箭头、局部区域、边界端口、loss/feedback 类组件的约束。

## 清理内容

本次发布副本不包含本机临时输出和大批测试产物：

- `tmp_*` 临时 scene、audit 和导出目录
- `regressions/` 下的大量 PNG/SVG/VSDX/crop/overlay 调试输出
- Python `__pycache__`
- 带有本机绝对路径的旧内部更新记录

这些内容只适合本地调试，不适合作为公开 release 源码上传。

## 发布前注意

- 公开仓库中的命令示例统一使用 `python`，不绑定作者本机 Python 路径。
- 严格复刻仍然需要视觉 LLM 或人工审查。Python gate 只负责流程、结构和证据完整性，不能替代视觉质量判断。
- Windows + Microsoft Visio 桌面版 + `pywin32` 仍是渲染 `.vsdx` 的核心依赖。
- 不同 Visio/Office 版本、系统语言、字体安装情况可能影响导出结果。

## 后续可继续优化

- 扩展更多可复用论文图组件模板。
- 提升字体/公式自动归一化和 no-wrap 文本保护。
- 增加更多不依赖 Visio COM 的单元测试，覆盖 review/rebuild 合同和 scene schema。
- 建立一组可公开授权的多图视觉评测样例，用于比较不同版本的复刻能力。
