---
name: local-models
description: "Operate this machine's locally hosted AI models and model services on demand: CosyVoice3 TTS (配音/旁白/克隆), local embeddings bge-m3, Ollama models (gemma3:4b), musicgen-small (音乐生成), and LM Studio models. Use whenever the user mentions 本地模型, 本地配音, 本地TTS, CosyVoice, 11436, 11435, bge-m3, ollama, gemma, 本地音乐生成, musicgen, LM Studio, or asks to generate speech/music/embeddings with local models. IMPORTANT: use these resources only when a task actually needs them — do not load heavy models or start services speculatively."
---

# 本机本地模型（按需使用）

> 适用机器：本 Windows 工作站。所有模型与代码集中在 `D:\Desktop\模型管理`。
> 铁律：**只在任务真正需要本地模型时才使用**。不要为了"准备着"去启动服务、加载模型或安装依赖——8GB 显存共享，多个大模型不能同时常驻。

## 资源总览（先判断用哪个，再动手）

| 能力 | 服务/入口 | 端口 | 状态 | 何时用 |
|---|---|---|---|---|
| 中文配音/旁白/声线克隆 | CosyVoice3-0.5B（GPU） | 11436 | 常驻看门狗，**模型懒加载**（首次请求约 30s） | 需要本地 TTS 配音时 |
| 文本嵌入（1024 维） | bge-m3 / llama-server | 11435 | 常驻 | 需要本地 embedding 时 |
| 本地对话 LLM | Ollama `gemma3:4b` | 11434 | 应用常驻，模型按需加载 | 需要免费本地聊天/轻量文本任务时 |
| 音乐生成 | musicgen-small（模型已下载，**运行库未装**） | — | 未部署 | 任务明确要生成音乐时再装 |
| 其他 GGUF 模型 | LM Studio（模型在 `C:\Users\18052\.lmstudio\extensions`） | 由 LM Studio 管理 | 按需 | 需要 LM Studio 生态时 |

- GPU：`NVIDIA RTX 5060 Laptop`（8GB 显存）。torch 2.7.1+cu128 装在 `D:\Desktop\模型管理\venv`（详见同目录 `README-torch.md`）。
- 任何"加载失败/版本不对"类问题，先读 `D:\Desktop\模型管理\README-torch.md` 和 `F:\DramaClaw\LOCAL-PATCHES.md`。

## 1. CosyVoice3-0.5B 配音（最常用）

- 服务：OpenAI 兼容 `POST http://127.0.0.1:11436/v1/audio/speech`；看门狗 `D:\Desktop\模型管理\service\watchdog_tts.py`（崩溃自动重启，日志 `D:\Desktop\模型管理\tts-server.log`）。
- **使用前先探活**（不要重复启动）：
  ```powershell
  Invoke-WebRequest -Uri 'http://127.0.0.1:11436/health' -UseBasicParsing -TimeoutSec 5
  ```
  若不可达（如机器重启后）：
  ```powershell
  Start-Process 'D:\Desktop\模型管理\venv\Scripts\python.exe' -ArgumentList '-u','D:\Desktop\模型管理\service\watchdog_tts.py' -WindowStyle Hidden
  ```
- 请求体：
  ```json
  {"model":"index-tts-2","input":"要合成的文本","metadata":{"audio_url":"data:audio/wav;base64,<参考音频>"}}
  ```
  - 有 `audio_url` → 零样本声线克隆；没有 → 用默认示例音色。
  - **内部约定**：prompt_text 必须含 `<|endofprompt|>`（服务端已处理，不要"修复"）。
  - 返回 `audio/mpeg`（mp3 字节）。
- 单句验证脚本：`D:\Desktop\模型管理\service\test_tts.py`（输出 `D:\Desktop\模型管理\test_output.wav`）。
- 性能：fp32 RTF≈1.5（30s 音频约 45s）；想省显存/加速可设环境变量 `COSYVOICE_FP16=1` 后重启服务（未长期验证）。
- 显存告警：CosyVoice3 常驻约 3-5GB 显存。若要跑别的大模型，先停它：
  ```powershell
  Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'watchdog_tts|tts_server' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
  ```

## 2. bge-m3 嵌入（11435）

- 服务：llama-server 常驻，模型 `F:\DramaClaw\runtime\models\bge-m3.gguf`，1024 维，OpenAI 兼容。
- 用一次：
  ```powershell
  $body = '{"model":"bge-m3","input":"要向量化的文本"}'
  Invoke-RestMethod -Uri 'http://127.0.0.1:11435/v1/embeddings' -Method Post -ContentType 'application/json' -Body $body
  ```
- 若没在跑（重启后），启动命令见 `F:\DramaClaw\启动 DramaClaw.cmd`（内含 11435 守卫）；独立启动：
  ```powershell
  Start-Process 'C:\Users\18052\AppData\Local\Programs\Ollama\lib\ollama\llama-server.exe' -ArgumentList '--model','F:\DramaClaw\runtime\models\bge-m3.gguf','--alias','bge-m3','--host','127.0.0.1','--port','11435','--embeddings','--no-webui','--ctx-size','8192','--batch-size','8192','--ubatch-size','8192','--pooling','cls','--log-disable' -WindowStyle Hidden
  ```

## 3. Ollama（11434，gemma3:4b）

- 模型库在 `D:\Desktop\模型管理\ollama\models`（`E:\Ollama\Models` 是指向它的 junction；用户环境变量 `OLLAMA_MODELS` 已设置）。
- 服务：Ollama app 常驻（重启机器后需打开一次 Ollama 应用，或手动 `Start-Process 'C:\Users\18052\AppData\Local\Programs\Ollama\ollama.exe' -ArgumentList 'serve' -WindowStyle Hidden`）。
- **按需使用**：
  ```powershell
  ollama run gemma3:4b "提示词"      # 一次性问答
  ollama ps                            # 看当前加载了哪些模型
  ollama stop gemma3:4b                # 用完卸载，释放内存
  ```
- 单次 API 调用（模型未加载时会自动加载，用完建议 stop）：
  ```powershell
  $body = '{"model":"gemma3:4b","prompt":"...","stream":false}'
  Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -ContentType 'application/json' -Body $body
  ```

## 4. musicgen-small（音乐生成，未部署）

- 模型文件：`D:\Desktop\模型管理\models\musicgen-small`（已下载）。
- **运行库未装**。只有任务明确要求"生成音乐"时才部署（用独立 venv，别污染 CosyVoice 环境）：
  ```powershell
  uv venv 'D:\Desktop\模型管理\venv-musicgen' --python 'D:\Python\Python312\python.exe'
  uv pip install --python 'D:\Desktop\模型管理\venv-musicgen\Scripts\python.exe' 'audiocraft' 'torch==2.7.1+cu128' --find-links 'https://mirrors.aliyun.com/pytorch-wheels/cu128/'
  # 用 audiocraft 加载本地模型目录即可（musicgen-small）
  ```
- 注意：musicgen 与 CosyVoice 同抢 8GB 显存，**不同时跑**；用完停止/退出进程。

## 5. LM Studio 模型

- 模型目录：`C:\Users\18052\.lmstudio\models`（junction → `D:\Desktop\模型管理\lmstudio\models`，当前为空）；实际引擎/模型在 `C:\Users\18052\.lmstudio\extensions`。
- 使用方式：打开 LM Studio 应用走其 GUI/本地 server；没有命令行直用约定，别自行猜测接口。任务需要时再启动应用。

## 通用注意

- 本机 PowerShell 控制台是 GBK：**传中文一律走 UTF-8 文件或 Python 脚本**。
- 装依赖一律 `uv`（已配阿里云镜像、禁下载解释器）：`uv pip install --python <venv>\Scripts\python.exe <pkg>`。
- 用系统 Python 3.12：`D:\Python\Python312\python.exe`；`D:\Python\Python314` 的 torch 是 CPU 版。
- 服务/模型状态速查：
  ```powershell
  foreach ($p in 11434,11435,11436,3000,8780,5174) { $c = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object LocalPort -eq $p; "{0}: {1}" -f $p, $(if ($c) {'up'} else {'down'}) }
  ```
- 详细坑与背景：`D:\Desktop\模型管理\README-torch.md`、`F:\DramaClaw\LOCAL-PATCHES.md`。
