# 2026-05-29 Rounded Orthogonal Connector 更新

本轮优化目标是补齐“圆角折线连接曲线”的专门组件，避免在硬折线、全局 smooth 曲线和多点台阶折线之间反复摇摆。

## 发现的问题

很多论文图和 AI 生成流程图里的连接线不是自由曲线，而是正交路径加圆角拐弯：

- 主体线段仍然横平竖直；
- 每个 90 度拐角是固定半径圆角；
- 箭头头只在最后终点；
- 不能用 Catmull-Rom / smooth 曲线整体拟合，否则直线段会被拉弯或出现波浪。

## 修改内容

- 新增 edge 类型：`rounded_orthogonal_connector`。
- 新增 renderer：`rounded_orthogonal_path`。
- `scene_to_visio.py` 新增 `rounded_orthogonal_points()`：
  - 输入正交折线路径；
  - 对每个 90 度拐角按 `corner_radius_in` / `corner_radius_px` 生成确定性四分之一圆弧采样点；
  - 保留直线段语义，不使用全局 smooth 拟合；
  - 箭头头保留在最终路径终点。
- `scene_to_visio.py` 支持 `route: "rounded_orthogonal"`，并在像素坐标场景里把 `corner_radius_px` 缩放为 `corner_radius_in`。
- `scene_validate.py` 支持 `rounded_orthogonal` route，并对 `rounded_orthogonal_connector` 做基础检查：
  - 不应包含 diagonal segment；
  - 应至少有一个 90 度拐角；
  - 应显式设置圆角半径。
- `references/scene-schema.md` 增加使用示例和规则说明。
- `SKILL.md` 增加 authoring 规则：圆角正交连接器不要用 `smooth` 曲线替代。
- `metadata.arrow_plan.route_shape` 增加 `rounded_orthogonal`，严格模式会要求它绑定到 `rounded_orthogonal_connector` 或 `route: "rounded_orthogonal"`。
- `references/visio-component-map.md` 和 `references/reviewer-two-image-prompt.md` 增加路线形态审查提示，避免视觉审查只看箭头方向而忽略“硬折/圆角/smooth”的差异。
- 新增 `templates/examples/rounded_orthogonal_connector.scene.json`，作为严格合同下的最小示例。
- `tests/test_public_release_smoke.py` 增加 renderer 算法、像素半径缩放和 scene validate 覆盖。

## 能力提升

这次更新让 Visiomaster 可以表达“圆角正交连接线”这一类常见论文/流程图连接器。它和 `loop_arrow`、`curved_arrow` 的定位不同：

- `rounded_orthogonal_connector`：横平竖直的正交线，只把拐角圆滑化；
- `loop_arrow` / `curved_arrow`：真正的连续曲线或外圈循环箭头；
- `lane_arrow`：硬直角或纯水平/垂直短连接。

## 验证

- `python -m compileall -q scripts tests sync_to_skill.py`：通过
- `python -m pytest -q`：通过，`7 passed`
- 当前 `14` 个 example scene 全部通过 `scene_validate.py`
- 本机路径/隐私关键词扫描未发现残留
