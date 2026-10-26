---
name: ppt-router
description: "Sole automatic routing entry for presentation and slide tasks. Use when the user asks to create, generate, rebuild, beautify, restyle, template, or fill any presentation, PPT, PPTX, 幻灯片, 演示文稿, slide deck, courseware, 课件, 答辩, 汇报, defense, seminar, or talk. Loads exactly one specialist — ppt-master, scholar-ppt-cn, sci-ppt, or presenting-conference-talks — or defers to the harness's native presentation skill. Never produces slides by itself."
---

# PPT Router

Single routing entry for presentation work. Select **exactly one** specialist per execution; never load two presentation skills together.

## Routing table

| Need | Skill |
|---|---|
| Chinese academic paper/thesis/report → PPT rebuild, with per-slide planning tables, reusable visual families, and editable output | `scholar-ppt-cn` |
| Slides from a paper PDF: thesis defense, seminar report, literature presentation; automatic figure extraction, LaTeX formula rendering, bilingual layouts | `sci-ppt` |
| General editable-PPTX workflow: generate decks, reconstruct page visuals, Brand/Style/Layout/Deck workspaces, native template fill, beautify finished files, narration/animation, narrated self-running video | `ppt-master` |
| Conference oral/spotlight/invited-talk deck from a finished paper: Beamer LaTeX PDF plus editable PPTX with speaker notes and talk script | `presenting-conference-talks` |

## Harness-native presentation skills

When running in a harness that ships a native presentation skill (for example ZCode `presentations:pptx` or the Codex presentation skill), prefer the native skill for straightforward create/edit requests. Use the specialists above only for their specific strengths: Chinese academic rebuilds (`scholar-ppt-cn`), defense/seminar decks from PDFs (`sci-ppt`), narrated video and template workspaces (`ppt-master`), talk scripts and Beamer output (`presenting-conference-talks`).

## Tie-breaks

- 中文论文/毕业论文转 PPT → `scholar-ppt-cn`; 英文会议宣讲 → `presenting-conference-talks`; 答辩/组会汇报 → `sci-ppt`; 通用生成/美化/模板填充 → `ppt-master`.
- When two rows fit, pick the one matching the output format the user named; if still ambiguous, ask one short question instead of guessing.
