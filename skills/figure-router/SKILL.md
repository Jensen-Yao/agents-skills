---
name: figure-router
description: "Sole automatic routing entry for creating scientific and technical figures, charts, and diagrams. Use when the user asks to 绘图, 画图, 作图, draw, design, or polish 论文图, 架构图, 流程图, 示意图, 数据图表, figures, charts, diagrams, architecture/flowchart/ER/sequence diagrams, or publication graphics for a paper, thesis, or report. Loads exactly one creator — academic-plotting, ccf-visual-composer, diagram-design, or drawio-skill — and routes PDF figure extraction to sci-figure. Never draws by itself."
---

# Figure Router

Single routing entry for figure and diagram creation. Select **exactly one** creator per execution; extracting existing figures out of a PDF goes to `sci-figure`.

## Routing table

| Need | Skill |
|---|---|
| Publication data charts from experiment results (auto chart-type selection, matplotlib/seaborn) or ML architecture diagrams derived from a paper-section description | `academic-plotting` |
| Branded diagram families — architecture, flowchart, sequence, state machine, ER, timeline, swimlane, Gantt, Sankey, Wardley map, and more — rendered as polished HTML | `diagram-design` |
| An editable `.drawio`/diagrams.net file, or converting code/IaC/SQL/API schemas into diagrams; Mermaid/PlantUML when diagrams-as-code suffices | `drawio-skill` |
| Figure rendering or redesign inside a CCFA pipeline (`ccfa.yaml` or `ccf-*` context): scientific visual tables, biological data, GPT Image 2 generation, editable SVG/PDF/PPTX output | `ccf-visual-composer` |
| Extracting existing figures/sub-figures from a paper PDF (截取文献图片, 提取子图, Extended Data, Scheme) | `sci-figure` |

## Tie-breaks

Decide by the output format the user wants:

- Editable `.drawio` file → `drawio-skill`
- Polished HTML render for docs/reports → `diagram-design`
- matplotlib/PDF data chart from experiment numbers → `academic-plotting`
- Inside a CCFA research pipeline → `ccf-visual-composer`
- Pulling a figure out of an existing PDF → `sci-figure`

When the user just says 画个架构图 with no format preference, prefer `diagram-design` for web/report use and `drawio-skill` when they will keep editing the diagram afterwards. Ask one short question only when genuinely ambiguous.
