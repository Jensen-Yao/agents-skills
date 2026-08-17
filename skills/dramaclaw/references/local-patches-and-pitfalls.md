# DramaClaw 本机修复记录与已知坑（防上游更新覆盖）

> 维护对象：`F:\DramaClaw`（SuperTale Community Edition / DramaClaw，v1.3.2，commit 起点 `5ae9c3f9`）
> 最后更新：2026-08-16
> 目的：上游仓库更新（`git pull`）可能覆盖本地修复。本文件 + git 本地提交 + skill 目录补丁包三重保存，供恢复。
> 恢复流程见文末。

---

## 一、已修复的代码缺陷（若复现，说明补丁被覆盖）

> 本地 git 提交（2026-08-16，基于上游 `5ae9c3f9`，分支 `local-fixes`）：
> `af808b8b fix(config)` · `6d2306d9 fix(runners)` · `88f386d3 fix(generators)` ·
> `9b295dcf fix(audio)` · `622406c6 fix(video)` · `81a0bbdd chore(scripts)` ·
> `2fd4b969 wip(此前会话改动)`。完整补丁包：本 skill `patches/dramaclaw-local-fixes.patch`。

### 1. 模型选择回退到 LingShan-G2 → NewAPI 503（最关键）
- **症状**：草图/渲染任务报 `[Sketch Image] provider=newapi, model=LingShan-G2` → `503 model_not_found`；项目明明配置了 `newapi_agnes_image2_flash`。
- **根因**：项目注册表 `state/local/projects.db` 把 state_dir 指到 `output\<project>`，但 `load_project_config(username, project)` 仍读旧路径 `state/local/<project>/project_config.json`；那份旧配置缺少 `sketch_image_selection` / `render_image_selection`，于是回退到默认 `newapi_gpt_image2` → NewAPI 默认模型 LingShan-G2（无渠道）。
- **修复**：`src/novelvideo/project_config.py` 新增 `_registry_state_dir_for()` / `_overlay_registry_state_dir_config()`，`load_project_config` 加载后叠加注册表 state_dir 的规范配置（21 个调用点一次性受益）。
- **验证**：`load_project_config("local","nogenshikkaku")` 返回 `sketch_image_selection='newapi_agnes_image2_flash'`；草图/首帧任务日志显示 `model=agnes-image-2.1-flash`。

### 2. Agnes 图片模型强制输出多格拼图/故事板
- **症状**：1x1 请求仍返回 2x2/3x4 拼图、带 Panel 标签文字、三联卡片；场景 reverse 图为上下双联图；图生图带参考图时更严重。
- **根因**：Agnes `agnes-image-2.1-flash` 对 storyboard/grid 词汇和附加参考图有强多格偏置。
- **修复**：
  - `src/novelvideo/generators/prompt_builder.py`：`SketchModeStrategy` 对 1x1 单幅使用精简单面板提示词（`single_panel` 分支 + `layout_block`）。
  - `src/novelvideo/generators/nanobanana_grid.py`：新增 `_agnes_single_panel_sketch_prompt()` / `_agnes_single_panel_render_prompt()`；1x1 草图与渲染在 Agnes 下走纯文本（不附场景/角色/草图参考图），避免拼图。
- **遗留**：渲染阶段仍偶发三联卡片式构图；这是模型能力限制，如需精修再单张重渲染。

### 3. Windows 文件锁竞态（WinError 32）
- **症状**：并行草图/渲染任务随机失败 `PermissionError: [WinError 32] 另一个程序正在使用此文件`，且 inline runner 异常曾带崩整个 API 进程。
- **修复**：
  - `src/novelvideo/generators/pool_indexer.py`：`_replace_with_retry()` / `_copy2_with_retry()`（15 次 × 0.5s）。
  - `src/novelvideo/ports/local/tasks.py`：`_run_inline` 包 try/except，任务异常不再传播到事件循环。

### 4. 临时文件时间戳秒级重名（WinError 2）
- **症状**：同秒提交的并行任务共用 `tmp_YYYYMMDDHHMMSS_panel_01_raw.png`，互相覆盖后 rename 找不到文件。
- **修复**：`src/novelvideo/task_backend/runners/sketch.py`、`render.py` 时间戳改为 `%Y%m%d%H%M%S%f`（微秒）。

### 5. 音频阶段无渠道必失败
- **症状**：`audio/generate` 走 NewAPI `index-tts-2`，本地无该渠道 → 503；且 Beat 11/12（父亲对白）报"角色声线缺失"。
- **修复**：
  - `src/novelvideo/generators/indextts2_fal.py`：NewAPI 失败且错误含 404/503/not found/channel 时回退 Edge TTS（`zh-CN-YunjianNeural`/`zh-CN-YunxiNeural`）。
  - 数据侧：为"父亲"角色生成参考声线 `assets/characters/父亲/voice.mp3` 并写入 characters 表（`reference_audio_path` + sha256）。

### 6. 视频接口 500 / 无 ffprobe
- **症状**：`POST /episodes/1/beats/{n}/video` 500，日志 `FileNotFoundError: ffprobe`。
- **修复**：ffmpeg 9.0.1 静态构建位于 `F:\DramaClaw\runtime\ffmpeg\ffmpeg-9.0.1-essentials_build\bin\`；启动脚本与看门狗把该目录加入 PATH。

### 7. Agnes 视频不是可选视频后端
- **修复**：`src/novelvideo/config.py` `NEWAPI_VIDEO_MODELS` 加入 `agnes-video-v2.0`、`NEWAPI_VIDEO_DURATION_BOUNDS` 加入 `agnes-video-v2.0:4-12`；`src/novelvideo/generators/video_generator.py` 加显示标签。使用 `video_backend="newapi_agnes-video-v2.0"`（Agnes 图生视频，结果 URL 解析分支此前会话已加在 video_generator.py）。

### 8. 启动脚本中文乱码 / 无端口保护
- **症状**：`启动 DramaClaw.cmd` 以 UTF-8 保存，cmd.exe 按 GBK 解析导致 `if exist "...启动 NewAPI.cmd"` 永远为假；双击启动不拉起 NewAPI。
- **修复**：该 .cmd 重写为 GBK(936) 编码；API 启动加 `netstat` 端口占用检查。`启动 NewAPI.cmd` 为纯 ASCII，无此问题。

### 9. 此前会话的其余改动（保留性提交，未逐一审计）
`src/novelvideo/cli.py`（直出 Agnes 视频模式、TTS 超时降级、镜头复用）、`api/routes/*`（scenes/props/tasks 读 state_dir、任务管理器导入修正）、`task_backend/runners/character_image.py`/`prop_reference.py`/`scene_reference.py`/`script.py`（统一 state_dir）、`generators/scene_reference_images.py`（reverse 图提示词硬约束）、`generators/tts_generator.py`、`generators/video_generator.py`（Agnes 视频协议/Referer/结果解包）、`api/schemas.py`、`frontend/pnpm-workspace.yaml`、`frontend/src/routeTree.gen.ts`、`tests/test_newapi_image_gateway.py`、`tests/test_seedance2_request.py`。详见 git 本地提交历史（分支 `main` 本地领先 origin/main 的提交）。

---

## 二、已知坑（非代码 bug，但会表现为"前后端不连通"）

1. **双画布**：虾画 UI 默认打开"个人画布" `user_<用户名slug>_<fnv1a-base36>`（本机 `local` → `user_local_17cvc3s`），而投影 API 不校验目标画布。**投影必须写到该个人画布**（或 URL `?canvas=` 指定的画布），写 `default` 界面看不到。算法见 `frontend/src/features/freezone/projections.ts` `personalCanvasIdForUsername()`（FNV-1a、`Math.imul`、无符号 base36）。
2. **双配置目录**：注册表 `state_dir=F:\DramaClaw\output\<project>` 是权威，但历史代码读 `state\local\<project>`。改配置要确认写到哪份文件；最好通过 API 设置页保存。
3. **前端双存储**：设置页（模型/媒体存储）同时写浏览器 localStorage 与后端数据库（显示"来源: database"）；排查时两边都要看。
4. **端口冲突**：5173 常被用户的其他软件（HandStar）占用，Vite 自动跳 5174。前端实际端口以进程命令行/监听为准。
5. **控制台 GBK**：从 PowerShell 调 API 传中文参数会变问号；一律用 UTF-8 文件传 body 或 Python 脚本。
6. **浅克隆无标签**：前端 `git describe` 失败会回退显示版本 1.0.0；`git fetch --tags` 可修。
7. **NewAPI 未启动**：点"初始化"超时 120s = 3000 端口没有 NewAPI。用 `启动 NewAPI.cmd` 或看门狗拉起；管理员登录 `http://127.0.0.1:3000`（root / 见 `state\newapi_admin_credentials.txt`）。
8. **CLI 捷径**：早期会话用 CLI 绕过主线（Beat 直出视频）导致 Web 全空。**必须走官方工作流**：虾料→虾格→虾塘资产→剧集规划→脚本→草图→首帧→音频→视频→合成；CLI 改动必须写入 Web 同一份项目状态（`output\<project>\data.db` + `freezone\canvases\*.json`）。
9. **Agnes 模型行为**：场景图易出现人物、reverse 图易复用 master 构图或双联拼图；生成后必须人工/视觉验收，不合格就用裁剪候选写回或改提示词重做，不要盲目重试。
10. **前端旧标签页缓存空状态**：后端数据补齐后，旧打开的页面不自动刷新，需 Ctrl+F5 硬刷新；判断"UI 缺数据"前先硬刷新 + 直接查 API（`GET /episodes/{n}`、`/episodes/{n}/beats`、`/episodes/{n}/script`）。已知小 bug：合成页时长显示（曾显示 4:01，实际成片 55s）来自旧元数据，与成片实际时长不一致，待修。
11. **NewAPI 模型路由表（abilities）可能被"保存映射"写错渠道**：症状为 `/v1/embeddings` 500 `not implemented`（实际路由到了 DeepSeek 渠道）。2026-08-16 已修：`state\newapi\one-api.db` 的 `abilities` 表中 `DC-cognee-embedding` 的 `channel_id=2` 行删除，只保留 channel 3（llama-server bge-m3）；改库后需重启 NewAPI。**自检**：`POST http://127.0.0.1:3000/v1/embeddings {"model":"DC-cognee-embedding","input":"测试"}` 应返回 1024 维。同理检查所有 `GROUP BY model HAVING COUNT(DISTINCT channel_id)>1` 的模型。

## 五、模型配置清单（2026-08-16 审计）

**已配置（管线在用，全部实测可用）**：文本理解/生成 18 个 DC-*-LLM 槽（17 业务槽 + DC-cognee-LLM）→ DeepSeek `deepseek-v4-flash`（NewAPI 渠道 #2，2026-08-16 全量核对并实测 `DC-hermes-LLM` 重定向到 `deepseek-v4-flash` 成功）；视觉理解 4 槽（DC-video-prompt-optimizer-LLM / DC-video-identity-detector-LLM / DC-freezone-vision-LLM / DC-style-analyzer-LLM）→ Agnes `agnes-2.5-flash`（渠道 #1）；嵌入 DC-cognee-embedding → 本地 bge-m3（llama-server 11435，渠道 #3，1024 维，已从渠道 #2 的模型列表与映射中清掉残留）；图片 agnes-image-2.1-flash；视频 agnes-video-v2.0；媒体中转阿里云 OSS。

**未配置（均为可选替代，不影响当前生产）**：官方渠道 relayclaw（无 DC Key）；openrouter/volcengine/openai/midjourney 供应商渠道（无 Key）；音频 index-tts-2 / LingShan-MU-11（无渠道，实际走 Edge TTS 兜底）；图片 LingShan-G2 / LingShan-NB-2、视频 seedance 全系 / happyhorse-1.0（无渠道，由 Agnes 覆盖）。`agnes-image-2.0-flash` 已于 2026-08-16 从 settings.db 媒体映射、NewAPI 渠道模型列表和 abilities 路由表三处移除（Agnes 账户无此模型），只保留 `agnes-image-2.1-flash`。**小瑕疵**：设置页 Embedding 配置记录的 provider 误标为 deepseek（功能不受影响，仅显示）。

---

## 三、服务运维速查（本机）

| 服务 | 端口 | 启动方式 |
|---|---|---|
| DramaClaw API | 8780 | `F:\DramaClaw\state\run-api-watchdog.cmd`（看门狗，崩溃自动重启，已注入 ffmpeg PATH；副本存于本 skill 的 `scripts/`） |
| 前端 | 5174 | `F:\DramaClaw\启动 DramaClaw.cmd`（双击；GBK 编码） |
| NewAPI | 3000 | `F:\DramaClaw\启动 NewAPI.cmd` / `runtime\new-api.exe`（SQLite 数据 `state\newapi\one-api.db`） |
| 嵌入服务 | 11435 | llama-server（bge-m3，NewAPI `DC-openai` 渠道 → `DC-cognee-embedding`） |
| 本地 TTS | 11436 | CosyVoice3-0.5B（`D:\Desktop\模型管理`，Python 看门狗 `service\watchdog_tts.py`，OpenAI 兼容 `/v1/audio/speech`；DramaClaw 经 `INDEXTTS2_PROVIDER=local` 直连，参考音频 data:URL 克隆，失败回退 Edge TTS） |

- **本地 TTS 细节（2026-08-16 部署）**：模型 `D:\Desktop\模型管理\CosyVoice3-0.5B`（Fun-CosyVoice3-0.5B 全量，GPU torch 2.7.1+cu128 装在其独立 venv `D:\Desktop\模型管理\venv`，注意该 venv 需 `setuptools<81` 提供 pkg_resources、需 pyarrow、pyworld 用 stub）；推理要点：**CosyVoice3 零样本的 prompt_text 必须含 `<|endofprompt|>` 标记**，前端传参考音频**文件路径**而非张量；当前 fp32（`COSYVOICE_FP16=1` 可试 fp16），RTF≈1.5（8GB 显存 RTX 5060）。
- **模型目录整理（2026-08-16）**：`D:\Desktop\模型管理` 根目录的散装 Python 包（transformers/tokenizers/httpx 等 58 项）移入 `pylibs\`（若其他项目依赖原导入路径需加 `pylibs` 到 sys.path）；`musicgen-small` 移入 `models\`；Ollama 模型从 `E:\Ollama\Models` 迁至 `ollama\models`（原路径留 junction + 用户环境变量 `OLLAMA_MODELS` 已指新路径）；LM Studio 的 `C:\Users\18052\.lmstudio\models` 为空（其模型实际在 `.lmstudio\extensions`，未动），已建空 junction。用户自己的 `skills`、`promote`（文档）、快捷方式未动。

- Python 环境：`F:\DramaClaw\.venv`（Python 3.12，`D:\Python\Python312`）。**用户规则（2026-08-16）：优先用 uv**——CLI 用 `uv run novelvideo ...`，依赖管理用 `uv sync`。uv 已配置可用：`%APPDATA%\uv\uv.toml` 设阿里云镜像 `index-url` + `python-preference="only-system"` + `python-downloads="never"`，用户环境变量 `UV_HTTP_TIMEOUT=60`/`UV_CONNECT_TIMEOUT=15`/`UV_RETRIES=5`；`uv sync --dry-run` 实测 42s 解析 238 包。注意：首次真实 `uv sync` 会规范化 `uv.lock` 元数据并移除 .venv 里的 pip（无害）。例外：长驻 API 服务仍由看门狗直接跑 `.venv\Scripts\novelvideo.exe`（服务进程不走 uv run 包装层）。
- 依赖已装全：`pip check` 通过；曾用国内镜像 + `uv.lock` 导出精确版本安装（详见 requirements.runtime.txt）。
- NewAPI 运行令牌 `dramaclaw-ce-runtime` 已设不限额度。
- **队列并发（2026-08-16，用户要求"不设上限"，在 `.env` 里）**：项目级准入全部队列 `ST_PROJECT_MAX_ACTIVE_*_TASKS=0`、`ST_PROJECT_USER_MAX_ACTIVE_*_TASKS=0`（代码中 ≤0 = 无限制），`/tasks/limits` 显示 `limit=null`；CE 全局执行槽全部改为 20（default/video/world/ffmpeg 的 `ST_CE_GLOBAL_MAX_ACTIVE_*_TASKS=20`）。**界面没有修改入口**——纯环境变量控制，改 `.env` 后重启 8780（看门狗自动拉起）。若上游限流（429），把对应 `ST_PROJECT_USER_MAX_ACTIVE_*_TASKS` 或 `ST_CE_GLOBAL_MAX_ACTIVE_*_TASKS` 改回正整数/小值即可。
- 模型配置：Agnes（文本/图像/视频，渠道 `DC-agnes`）、DeepSeek（纯文本 `DC-*-LLM`，渠道 `DC-deepseek`）、嵌入 bge-m3（渠道 `DC-openai`）。密钥文件：`D:\Desktop\bot\api\agnes\for Dramaclaw.txt`、`D:\Desktop\bot\api\deepseekapi.txt`、`D:\Desktop\bot\api\阿里云通行密钥.txt`。

---

## 四、上游更新后的恢复流程

1. **先备份当前工作区状态**：
   ```powershell
   cd F:\DramaClaw
   git stash -u   # 或先提交（见下）
   ```
   推荐做法：本地修复已按逻辑拆成 git 提交（`git log origin/main..HEAD`），更新用 **rebase** 而不是 merge/pull --ff-only：
   ```powershell
   git fetch origin
   git rebase origin/main
   ```
   冲突文件按本文件"一"清单逐条核对；补丁包 `patches/dramaclaw-local-fixes.patch`（本 skill 目录）可整体重放：`git apply --3way <patch>`（失败时逐文件手动合并）。
2. **症状自检清单**（更新后逐项跑）：
   - [ ] `F:\DramaClaw\.venv\Scripts\python.exe -c "from novelvideo.project_config import load_project_config; print(load_project_config('local','nogenshikkaku').get('sketch_image_selection'))"` 输出 `newapi_agnes_image2_flash`
   - [ ] 提交一个 1x1 草图：任务日志 `model=agnes-image-2.1-flash`，成图为单幅（非拼图）
   - [ ] `POST .../episodes/1/audio/generate` 不再报"声线缺失"，且无 503（Edge 兜底可用）
   - [ ] `POST .../beats/1/video` 返回 `ok:true`（ffprobe 在 PATH）
   - [ ] 并行 3 个草图任务无 WinError 2/32
   - [ ] `启动 DramaClaw.cmd` 为 GBK 编码且能拉起 NewAPI
   - [ ] 8780 崩溃后看门狗自动拉起（杀进程观察 10 秒）
3. **画布/数据自检**：`GET /freezone/canvases/user_local_17cvc3s` 有节点；`GET /pipeline/status?episode=1` 的 episode_status 全 true；成片 `output\nogenshikkaku\videos\episodes\ep001_final.mp4` 存在。
