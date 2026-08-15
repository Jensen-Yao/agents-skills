# 2026-05-28 箭头拓扑审查与重建闭环增强

本轮优化目标是把“箭头指向/箭头拓扑”从渲染后审查问题前移到第一版 scene authoring 前的硬约束，并把视觉审查结果稳定映射到下一轮 scene 修改目标。

## 发现的问题

在局部拓扑复杂、连接语义强的图形里，很多复刻失败不是 Visio 画不出箭头，而是第一版 scene 没有先锁定原图箭头事实，后续审查也难以把问题精确传回可编辑字段：

- 局部连接关系密集，整体看起来相似但实际端点或路径错误；
- 原图是水平/垂直/折线路径，scene 写成 `route: "auto"` 或宽泛 `straight` 后发生漂移；
- 原图是边界、端口、汇合点或分叉点输出，scene 直接连到组件中心；
- 多分支汇合/分叉没有 junction/bus，导致语义链路断裂；
- 内部组件连线没有暴露在 `edges[]` 中，原有 arrow-plan 机制无法覆盖；
- reviewer 能发现“箭头不对”，但下一轮 LLM 不稳定知道应该修改哪个 edge、motif 或字段。

## 修改内容

- 在 `SKILL.md` 中新增 strict replica 的 arrow-inventory pass：先从原图生成 `metadata.arrow_plan`，再写 scene edge。
- 在 `references/scene-schema.md` 中新增 `metadata.arrow_plan` 结构、edge 的 `arrow_plan_id` 绑定规则，以及 `nodes[].motif_edges[]` 内部连线声明。
- 在 `docs/workflow.md` 中把 Arrow Inventory 放进 scene authoring loop。
- 在 `references/review-contract.md` 中要求视觉 review 尽量引用 `arrow_plan` 的箭头 id，而不是泛泛描述“箭头不对”。
- 在 `scripts/make_review_assets.py` 中从 `metadata.arrow_plan` 自动生成 topology checklist。
- 在 `scripts/review_findings_to_repair_plan.py` 中保留 `checklist_refs`，并生成 `arrow_plan_repair_targets`，把 arrow id 映射到 scene edge、motif binding 和可编辑字段。
- 在 `scripts/prepare_regeneration_packet.py` 中把 topology checklist、visual checklist、checklist validation 和 arrow repair targets 放入 packet 和 Markdown prompt。
- 在 `scripts/scene_validate.py` 中新增 Arrow Plan Gate：
  - strict exact 场景缺少 `metadata.arrow_plan` 会报错；
  - `arrow_plan` 中的确定箭头必须有 edge 通过 `arrow_plan_id` 绑定；
  - source-visible edge 在 exact 场景中不能没有 `arrow_plan_id`；
  - `arrow_plan_id` 默认不能被多条 edge 复用，除非明确声明 multi-segment source arrow；
  - local motif 可以强制要求暴露内部 `motif_edges`；
  - `feedback` / `loss_backprop` 必须使用 `dashed_feedback_path`；
  - `boundary_handoff` / `frame_output` 必须使用 `boundary_port` 或 `boundary_arrow`；
  - `merge` / `fan_in` 必须汇入 junction/merge bus；
  - `fork` / `fan_out` 必须从 junction/merge bus 发出；
  - `loop_update` 必须用连续 `loop_arrow`；
  - `straight_horizontal` / `straight_vertical` / `orthogonal` 等 route shape 会检查实际 route 是否违背轴向约束。
- 在 `tests/test_public_release_smoke.py` 中新增两个 smoke tests：
  - 接受正确绑定的水平 arrow plan；
  - 拒绝声明为水平但实际渲染为斜线的箭头。

## 能力提升

这次更新把箭头问题从“PNG 出来后再肉眼找错”提前为“第一版 scene 必须满足原图箭头事实”。后续视觉 review 可以逐条检查 `A001`、`A002` 等箭头，而不是只给宽泛建议；下一轮重建也能看到具体要修的 edge、motif 和字段。

## 验证

- `python -m compileall -q scripts tests sync_to_skill.py`：通过
- `python -m pytest -q`：通过，`5 passed`
- 当前 `13` 个 example scene 全部通过 `scene_validate.py`
- 本机路径/隐私关键词扫描未发现残留
