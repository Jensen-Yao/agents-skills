---
name: dramaclaw
description: "Operate, inspect, configure, troubleshoot, and continue DramaClaw projects according to the official workflow. Use whenever the user mentions DramaClaw, NovelVideo, 虾导, 虾料, 虾塘, 虾镜, 虾画, 虾格, 虾条, CLI/API/Web project synchronization, model or storage configuration, characters, identities, portraits, scenes, props, voices, episodes, Beats, scripts, sketches, first frames, audio, video, composition, project status, resume/continue, or asks to generate/fix a DramaClaw production. Enforces asset, image, and review gates before downstream generation."
---

# DramaClaw

Follow the product manual and the repository's official skill. Treat the current source tree and live API responses as the authority for implementation details; treat the manual as the authority for production order and review boundaries.

## Start Every DramaClaw Task

1. Locate the active repository and project. On this machine the usual repository is `F:\DramaClaw`, but verify when paths or sessions differ.
2. Inspect the current source, CLI help, API routes, configuration, and project status before choosing commands. Do not infer endpoints or state from chat history.
3. Read [product-manual.md](references/product-manual.md) for production workflow, confirmation gates, 虾画 write-back, 3GS, 虾格, and quality checks.
4. Read [official-skill.md](references/official-skill.md) and the matching official reference only when API, async, update, resume, or delivery details are needed.
5. Read [local-patches-and-pitfalls.md](references/local-patches-and-pitfalls.md) whenever this machine's local fixes could be involved: model selection (Agnes/DeepSeek/embedding), sketch/render generation, audio/TTS, video backend, canvas projections, service startup, or after an upstream `git pull`. This file records every local code fix plus re-apply instructions so upstream updates do not silently overwrite them.
6. If copied documentation conflicts with the checked-out source, follow the current source and report the mismatch. Never invent a compatibility workaround.

## Local Machine Constraints (F:\DramaClaw)

- The local repo carries uncommitted-by-upstream fixes. Before any `git pull`, see `F:\DramaClaw\LOCAL-PATCHES.md`; prefer `git fetch && git rebase origin/main` over `git pull --ff-only`, and re-run the self-check list after updating.
- **Prefer `uv` for this project** (user directive, 2026-08-16): use `uv run novelvideo ...` for CLI commands and `uv sync` for dependency management. uv is configured on this machine (Aliyun mirror + only-system + timeouts in `%APPDATA%\uv\uv.toml` and user env vars; see the local fixes ledger). Note: a first real `uv sync` may rewrite `uv.lock` metadata and remove pip from `.venv` — both harmless. Exception: the long-running API server stays on the direct venv exe under the watchdog (no `uv run` wrapper for server processes).
- The DramaClaw API on 8780 runs under a watchdog (`F:\DramaClaw\state\run-api-watchdog.cmd`, copy in this skill's `scripts/`); it auto-restarts and injects the ffmpeg PATH. Kill the watchdog cmd process itself (not just the child python) to reload changed startup environment.
- 虾画 canvases are per-user: the UI opens `user_local_17cvc3s` (personal canvas for username `local`), NOT `default`. Write mainline projections to the personal canvas (or the canvas named by the `?canvas=` URL param), otherwise the UI shows an empty board.
- PowerShell console is GBK: never pass Chinese payloads inline; write JSON/py to UTF-8 files and run them with the venv python.
- Port 5173 belongs to another app (HandStar); the DramaClaw frontend usually runs on 5174.

## Production Order

Use this order unless the user is explicitly doing isolated experimentation in 虾画:

`虾料文本 -> 虾格风格 -> 虾塘资产 -> 虾镜剧集规划 -> 脚本/Beat -> 草图 -> 渲染图/首帧 -> 音频 -> 视频 -> 合成`

Never start normal production with direct text-to-video or image-to-video when required upstream assets and review gates are incomplete.

### Required Gates

Treat generated, selected, written back, and confirmed as different states. A task result is not user approval.

1. **Text gate**: verify imported content, chapters, project type, style, ethnicity, word count, and episode estimate.
2. **Style gate**: select or create 虾格, verify style instructions and avoid instructions, then apply it to the project before bulk visual generation.
3. **Asset gate**: build and confirm required character portraits, identities/outfits, voices, scene references/variants, and prop references in 虾塘.
4. **Episode planning gate**: plan identities, scenes, and props before generating the episode script.
5. **Copy gate**: verify each Beat's dialogue/narration, speaker, visual description, scene/variant/time, identities, and props.
6. **Sketch gate**: confirm composition, staging, action, camera direction, and color binding. Do not judge final lighting here.
7. **First-frame gate**: confirm face, outfit, scene, props, lighting, text artifacts, and suitability as the video's visual anchor.
8. **Audio gate**: confirm voice assignment, text, clarity, emotion, and duration.
9. **Video gate**: confirm movement, character consistency, scene continuity, camera motion, and audio relationship for every Beat.
10. **Composition gate**: compose only when every required Beat is ready and resolution/subtitle settings are correct.

If the user asks to continue, read actual pipeline and task state, identify the earliest incomplete gate, and advance only the corresponding next operation. Do not silently treat missing review as approval.

## 虾画 Rules

- Use 虾镜 for ordinary repeatable shots. Use 虾画 for difficult shots, asset finalization, advanced image/video processing, 360, and director-world work.
- Start from a mainline projection or Beat/asset context when possible so references remain traceable.
- Treat all 虾画 outputs as candidates. They do not become official assets until explicitly written back to a named target slot.
- Before write-back, show or inspect the candidate, target slot, and impact scope. Obtain explicit approval when replacing a global character, scene, or prop asset because it may affect multiple Beats.
- After a write-back, re-read the mainline state. Do not assume a canvas candidate automatically synchronized.
- Keep 3-5 candidates for important shots when useful; preserve node connections so generation provenance remains visible.

## Director World And 3GS

- Use scene variants for the same location at different times or story states.
- Use source/reverse images, 360 panoramas, director world, or 3GS for recurring spaces and continuity-sensitive shots.
- Preferred order: scene source -> director world/3GS -> place people and props -> choose camera -> export control image -> sketch -> first frame -> video.
- Use 3D for spatial layout, a 2D control image for composition, the sketch for action, and the first frame for final visual finish.
- Do not rebuild the same recurring room independently for every shot when a stable world or panorama exists.

## CLI, API, And Web State

- Inspect `uv run novelvideo --help` and relevant subcommand help before using the CLI. Prefer existing project commands over ad hoc scripts.
- Ensure CLI writes to the same canonical project/API state that the web frontend reads. Do not create a parallel hidden workflow that leaves 虾镜, 虾塘, 虾条, or 虾画 empty.
- Before a write, read pipeline status and relevant queued/running tasks. Do not duplicate an active async task.
- After starting an async task, report its real task ID/status and stop or wait according to the official async contract. Do not call downstream stages merely because submission succeeded.
- Use the repository's current routes and schemas. Read [official-api-reference.md](references/official-api-reference.md), [official-pipeline-details.md](references/official-pipeline-details.md), and source routes when uncertain.
- Keep provider keys out of logs, replies, tracked files, and commits. Read secrets only from the user-designated local files or environment.

## Failure Handling

- On a 4xx/5xx response, `ok:false`, missing prerequisite, queue-full response, or failed task, stop downstream writes and surface the actual error plus the specific missing gate.
- Diagnose the earliest wrong artifact. Fix copy before sketch, sketch before first frame, first frame before video, and audio before composition.
- Do not solve inconsistent faces by repeatedly regenerating video. Repair portrait/identity/face prompts first.
- Do not solve scene drift by random rerolls. Repair scene references, variants, 360, or director-world controls first.
- Do not solve missing props only in the video prompt. Add the prop asset and select it in the Beat.

## Reference Map

- Product workflow and manual summary: [product-manual.md](references/product-manual.md)
- Official complete skill: [official-skill.md](references/official-skill.md)
- Initialization: [official-playbook-init.md](references/official-playbook-init.md)
- Episode production: [official-playbook-episode.md](references/official-playbook-episode.md)
- Resume/continuation: [official-playbook-resume.md](references/official-playbook-resume.md)
- API routes: [official-api-reference.md](references/official-api-reference.md)
- Pipeline details: [official-pipeline-details.md](references/official-pipeline-details.md)
- Async tasks: [official-async-tasks.md](references/official-async-tasks.md)
- Read behavior: [official-read-behavior.md](references/official-read-behavior.md)
- Update behavior and editable fields: [official-update-behavior.md](references/official-update-behavior.md), [official-editable-fields.md](references/official-editable-fields.md)
- Delivery boundaries: [official-delivery-boundaries.md](references/official-delivery-boundaries.md)
- Manual/automatic modes: [official-run-modes.md](references/official-run-modes.md)
- Local fixes ledger, pitfalls, and post-update re-apply guide: [local-patches-and-pitfalls.md](references/local-patches-and-pitfalls.md)
