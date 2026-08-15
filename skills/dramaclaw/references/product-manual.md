# DramaClaw Product Manual Summary

Source: `https://neo-flying.feishu.cn/docx/T2UgdVA4Fo1A5KxCh0vckDz3nTg`

Reviewed in detail on August 14, 2026. The source page reported its latest modification as August 14.

## Core Model

DramaClaw has two production paths:

- **Mainline**: `虾料 -> 虾塘 -> 虾镜 -> 合成`. Best for beginners, standardized production, progress tracking, and ordinary shots.
- **Free canvas**: `虾画`. Best for directors and teams working on difficult shots, asset finalization, advanced media operations, 360, and director-world work.

Most formal projects should use the mixed model: ordinary shots in 虾镜, difficult shots in 虾画, then explicitly write approved 虾画 results back to the mainline.

`虾格` manages project visual style. `虾导` reads status, checks missing prerequisites, and recommends the next operation. `虾条` shows background task status, progress, logs, errors, results, cancellation, and cleanup.

## First Episode Workflow

1. Create a project.
2. Import an existing novel or script through 虾料.
3. Verify text, chapters, project type, style, ethnicity, and episode estimate.
4. Establish the project style in 虾格.
5. Build character, scene, prop, and voice assets in 虾塘.
6. Plan episodes in 虾镜, then plan identities, scenes, and props for the target episode.
7. Generate and review the episode script/Beats.
8. For every Beat, proceed through copy, sketch, render/first frame, audio, and video.
9. Compose/export only after all required shots are ready.

Do not begin with video generation. Errors in copy, characters, scenes, props, or first frames propagate downstream and become more expensive to repair.

## 虾料

- Select project type, visual style, and ethnicity before import; project type locks after import.
- Import `txt`, `md`, `docx`, or pasted text.
- Clean chapter headings and content before import.
- After import, verify word count, chapter recognition, estimated episode count, and project configuration.
- If chapters are wrong, normalize the source headings and re-import rather than manually compensating throughout the project.

## 虾塘 Assets

All downstream production depends on confirmed assets. 虾塘 contains characters, scenes, props, and voices.

### Characters

- Extract automatically or create manually.
- Record name, aliases, role, gender, age, body, appearance, and face prompt.
- A face prompt should cover age, face shape, features, hair, and temperament; clothing alone is insufficient.
- Generate or upload a portrait and retain the approved version.
- Create identities/outfits for story periods, roles, ages, or wardrobe changes.
- Character means who the person is; identity means the stage-specific appearance.
- Upload, record, trim, and assign voices as needed.

### Scenes

- Build from story analysis or create manually.
- Record name, type, environment prompt, and narrative description.
- Core recurring scenes need a source image. Add a reverse image for reverse-angle continuity.
- Use a 360 panorama or director world for frequently reused spaces.
- A scene variant/plate represents the same location at another time or story state and should inherit its spatial structure.

### Props

- Create from episode analysis or manually.
- Record name, type, owner, and visual prompt.
- Generate or upload a reference image.
- Select appearing props in the Beat so sketch, render, and video stages can reference them.

### Voices

- Third-person projects require a project narrator voice.
- First-person projects require the narrator protagonist and that character's voice.
- Missing narrator or character voices block bulk dubbing and dialogue generation.

## Director World And 3GS

Director world and 3GS solve spatial continuity, actor placement, prop placement, and camera selection for recurring scenes.

Recommended order:

1. Prepare scene source and optional reverse/360 assets.
2. Open or generate the director world.
3. Place characters, props, or placeholders.
4. Choose camera, FOV, roll, pitch, and yaw.
5. Export a pure background or director composite/control image.
6. Use that control image for the Beat sketch.
7. Produce the first frame and then video.

The manual describes this as progressively reducing uncertainty: 3D fixes spatial layout, the 2D control image fixes composition, the sketch fixes action/staging, and the first frame fixes final appearance and lighting.

## 虾镜

虾镜 is the principal production workspace: episode list -> single-episode workspace -> script, shots, and composition. Shot work is divided into copy, sketch, render/first frame, audio, and video.

### Episode Planning

- If no episodes exist, generate them from the chapter structure.
- Review source line count, Beat count, planned identities, scenes, props, and script state.
- Plan identities, scenes, and props before entering production because missing assets affect script and shot generation.

### Script Stage

- Verify the source text and saved storyboard source.
- Narrated productions may use AI rewriting with target line count and per-line length.
- Premium productions may generate from the original working copy.
- Generate the script or line-by-line Beats only after asset planning.
- Review dialogue/narration, speaker, visual description, scene, variant, identities, and props.

### Copy Stage

Copy fields affect sketch, dubbing, first frame, and video prompts. Check:

- dialogue/narration and audio type;
- correct speaker or narrator;
- scene, variant/plate, and time;
- visual action, composition, emotion, and environment;
- appearing identities and props.

Fix errors here before generating downstream media.

### Sketch Stage

- The sketch establishes composition, actor placement, action, and camera direction, not final visual quality.
- Generate only after copy and references are correct.
- Regenerate, upload, pose-edit, crop, select a background, or use a director control image when needed.
- Enter 虾画 for deeper work on difficult Beats.
- Approve whether the shot communicates clearly before worrying about lighting and materials.

### Render / First Frame

The first frame is the formal visual reference used by video generation. Confirm:

- face matches portrait/identity references;
- outfit matches the selected identity;
- scene, lighting, and period are continuous;
- required props appear in sensible locations;
- no stray text, watermark, or incorrect marking appears;
- composition leaves room for the intended motion.

Direct text-to-video without a key frame is prone to style drift. The first frame anchors visual style, lighting, face, clothes, scene, props, and the video's starting state.

### Audio

Check voice assignment, dialogue/narration text, emotion, clarity, and duration. A missing voice is an unmet prerequisite, not a reason to continue silently to video.

### Video

- Choose a model compatible with available reference materials.
- Verify people, scene, props, first frame, audio, and other references.
- Configure generation mode, duration, resolution, aspect ratio, and advanced settings.
- Review or optimize the video prompt.
- Preview the result and check movement, people, scene, camera motion, and audio relationship.

### Composition

- Enter composition only when every required shot is ready.
- The composition page identifies Beats missing sketches, audio, or video.
- Select the correct horizontal/vertical resolution and subtitle option.
- Subtitle composition can fail if the local subtitle plugin is unavailable.
- Compose the episode or export a ZIP only after readiness checks.

## 虾画

虾画 is a visual production workspace, not merely an image generator. It supports uploaded resources, text, image, video, audio, script, 360, 3D/director-world, grouping, multi-version grids, mainline contexts, and skill nodes.

### Candidate And Write-Back Boundary

- Uploaded or generated canvas media remains a candidate by default.
- A candidate does not overwrite the mainline automatically.
- Explicit write-back can target character portraits/identities, scene source/360/director assets, prop references, Beat sketches, Beat render/first frames, Beat video, selected background, or director control image.
- Before write-back, inspect the thumbnail, target slot, overwrite warning, and impact scope.
- Character, scene, and prop changes are global and may affect multiple Beats. Beat sketch/first-frame/video writes usually affect only the current shot.
- After mainline assets change, synchronize or refresh canvas projections.

### Recommended Uses

- Repair one Beat: load Beat context -> add background/sketch/director composite -> generate several candidates -> approve -> write back to the Beat sketch.
- Finalize an identity: portrait/reference -> multi-view or image generation -> upscale/relight/inpaint -> approve -> write back identity.
- Build scene 360: source/reverse -> 2:1 panorama candidate -> inspect space -> write back scene 360.
- Build a video candidate: prepare first frame and references -> choose image-to-video, first/last-frame, or multi-reference mode -> generate -> approve -> write back Beat video.
- Team production: start from mainline projection, group candidates by asset or stage, preserve node links, compare 3-5 important candidates, and let the director approve write-back.

## 虾格

- A style can include a UI label, style instructions, avoid instructions, tags, and structured JSON.
- Presets are normally read-only; custom styles can be created, edited, or deleted.
- A reference image can be analyzed to propose style parameters.
- Apply the selected style to the project before bulk generation.

## 虾导

Use 虾导 to query actual project progress, task state, missing assets, incomplete shots, and the recommended next step. It is available as a standalone project page and as a context-aware panel in 虾画.

## 虾条

- Task states include submitting, queued, waiting, starting, running, completed, failed, and cancelled.
- Running tasks expose step and progress.
- Expanded tasks expose logs, errors, and results.
- Use task navigation to return to the relevant page.
- Running tasks may be cancelled; terminal tasks may be deleted; completed tasks may be cleared.
- When a page appears to have no result, check 虾条 before resubmitting.

## Team And Individual Practice

- Mainline pipeline mode suits new teams and standardized narrated productions.
- Free-canvas collaboration suits premium productions and experienced art/video teams.
- Mixed mode suits most formal projects: 虾塘 stabilizes assets, 虾镜 tracks progress and composition, 虾画 handles creative and difficult work.
- Individuals should test with a short chapter, keep the first episode's Beat count manageable, establish the protagonist portrait/core identities/core scenes/default voice first, and diagnose the faulty stage instead of rerolling blindly.

## Quality Checklist

| Stage | Required check | Pass condition |
|---|---|---|
| 虾料 | text, chapters, project type | complete text, sensible chapters/config |
| 角色 | portrait, identity, aliases, voice | stable protagonists; important roles complete |
| 场景 | source, reverse, 360, director world, variants | enough references; same-place states use variants |
| 道具 | reusable key props and images | important props can be selected in Beats |
| 脚本 | Beats, speaker, scene, variant, identity, props | coherent story and correct assignments |
| 草图 | composition, staging, action, color binding | shot is readable and positions are correct |
| 首帧 | face, outfit, scene, props, artifacts | usable as the video's visual anchor |
| 音频 | voice, text, duration, clarity | no missing voices; speech is intelligible |
| 视频 | action, camera, consistency, audio relation | each shot is usable |
| 合成 | all shots, subtitles, resolution | final episode previews and exports correctly |

## Common Diagnosis

- Unstable face: unify portrait, identity image, and face prompt before regenerating shots.
- Inconsistent recurring scene: add source/reverse/360/director world and use variants for different states.
- Missing prop: select it in Beat copy and provide its reference image.
- Good sketch but wrong first frame: inspect identity/scene/prop references and background anchor; refine in 虾画 if needed.
- Wrong video motion: fix the first frame action foundation or video prompt before regenerating.
- Composition disabled: locate Beats missing audio or video and complete them.
- 虾画 result absent from mainline: it is still a candidate; explicitly write it back to the correct slot.
- Task appears stuck: inspect 虾条 status, progress, logs, and error before retrying.

The governing principle is: `text -> assets -> script -> shots -> video -> final episode`. The product is designed for stable staged production, not for clicking every generation action at once.
