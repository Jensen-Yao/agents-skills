# 🧠 Agents Skills · 智能体技能库

<div align="center">

**个人 Agent 技能库 —— 140+ 个 SKILL.md 技能，桌面端与手机端共用**<br>
*Personal agent skills library — 140+ SKILL.md skills shared across desktop and mobile*

[![Skills](https://img.shields.io/badge/skills-140-blue.svg)](#-技能索引-skill-index)
[![SKILL.md](https://img.shields.io/badge/format-SKILL.md-purple.svg)](#-技能格式-skill-format)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![DSH](https://img.shields.io/badge/DeepSeek%20Harness-4D6BFE.svg)](https://github.com/deepseek-ai/deepseek-harness)

</div>

---

## 📖 这是什么 · What is this

本仓库是个人 Agent 技能集合：每个技能是一个目录，内含一份 `SKILL.md`（YAML frontmatter + 专家指令正文）。当任务描述命中某个技能的 `description` 时，Agent 按需加载该技能，获取完整指令。

*This repository is a personal collection of agent skills. Each skill is a directory containing a `SKILL.md` (YAML frontmatter + expert instructions). When a task description matches a skill's `description`, the agent loads it on demand.*

## 🏗 技能加载架构 · Skill Loading Architecture

技能由 DeepSeek Harness 的技能系统（`@deepseek-ai/dsh-skill-filesystem`）从多个根目录按优先级加载：

*Skills are loaded by the DeepSeek Harness skill system (`@deepseek-ai/dsh-skill-filesystem`) from multiple roots by rank:*

```
┌────────────────────────────────────────────┐
│  技能根目录 · Skill roots (by rank)         │
├────────────────────────────────────────────┤
│ 1. <项目>/.dsh/skills     项目级 · project  │
│ 2. <项目>/.agents/skills  项目级 · project  │
│ 3. 自定义目录 · custom dirs                │
│ 4. ~/.dsh/skills          用户级 · user     │
│ 5. ~/.agents/skills       用户级 · user     │
│ 6. 内置技能 · bundled skills               │
└────────────────────────────────────────────┘
         │  按需发现 + 热加载 · discovery + hot reload (directory watcher)
         ▼
   Agent（桌面 / 手机 Termux）· Agent (desktop / mobile Termux)
```

- 本仓库内容部署于 `~/.agents/skills/`（用户级 agents 根）。*This repo deploys to `~/.agents/skills/` (user-level agents root).*
- 同一套技能**桌面端与手机端通用**；手机端同步后 harness 的热加载 watcher 会自动发现新技能，无需重启。*The same skills work on both desktop and mobile; the harness watcher hot-reloads new skills without restart.*

## 📄 技能格式 · Skill Format

```
skills/<技能名 · skill name>/
└── SKILL.md
    ├── frontmatter: name + description（触发条件，描述"何时使用" / when to use）
    └── 正文 · body: 该领域的专家级指令 · expert instructions
```

示例 · *Example*（`apple-design`）：

```yaml
---
name: apple-design
description: Apple's approach to interface design and fluid, physical motion... Use when building or reviewing gesture-driven UI...
---
# Apple Design
...
```

## 🗂 技能索引 · Skill Index

共 **140** 个技能，按类分组；**在线检索版**：https://jensen-yao.github.io/agents-skills/ （支持关键词搜索与分类筛选）。
*140 skills, grouped by category. Searchable online at the link above.*

### 框架与平台 · framework  (13)

- **`autogpt`** — 
- **`crewai`** — 
- **`dspy`** — 
- **`guidance`** — 
- **`instructor`** — 
- **`langchain`** — 
- **`langsmith`** — 
- **`mlflow`** — 
- **`outlines`** — 
- **`phoenix`** — 
- **`swanlab`** — 
- **`tensorboard`** — 
- **`weights-and-biases`** — 

### 评估与基准 · eval  (3)

- **`bigcode-evaluation-harness`** — 
- **`lm-evaluation-harness`** — 
- **`nemo-evaluator`** — 

### 数据与检索 · data  (11)

- **`chroma`** — 
- **`faiss`** — 
- **`nemo-curator`** — 
- **`nnsight`** — 
- **`pinecone`** — 
- **`pyvene`** — 
- **`qdrant`** — 
- **`ray-data`** — 
- **`sentencepiece`** — 
- **`sentence-transformers`** — 
- **`transformer-lens`** — 

### 工具与CLI · tool  (33)

- **`0-autoresearch-skill`** — 
- **`a-evolve`** — 
- **`alibabacloud-find-skills`** — 
- **`audiocraft`** — 
- **`blip-2`** — 
- **`cli-anything`** — 
- **`cli-creator`** — 
- **`clip`** — 
- **`dramaclaw`** — 
- **`hatch-pet`** — 
- **`huggingface-tokenizers`** — 
- **`imagegen`** — 
- **`image-gen-fuck`** — 
- **`karpathy-guidelines`** — 
- **`lambda-labs`** — 
- **`libreoffice-local-install`** — 
- **`llava`** — 
- **`ml-training-recipes`** — 
- **`modal`** — 
- **`officecli`** — 
- **`playwright`** — 
- **`pytorch-fsdp2`** — 
- **`pytorch-lightning`** — 
- **`ray-train`** — 
- **`saelens`** — 
- **`segment-anything`** — 
- **`skypilot`** — 
- **`stable-diffusion`** — 
- **`tensorrt-llm`** — 
- **`visiomaster`** — 
- **`whisper`** — 
- **`windows-deployment-cli-locations`** — 
- **`winui-app`** — 

### 研究与写作 · research  (5)

- **`brainstorming-research-ideas`** — 
- **`creative-thinking-for-research`** — 
- **`ml-paper-writing`** — 
- **`presenting-conference-talks`** — 
- **`systems-paper-writing`** — 

### 学术文献 · academic  (19)

- **`cnki-advanced-search`** — 
- **`cnki-download`** — 
- **`cnki-export`** — 
- **`cnki-journal-index`** — 
- **`cnki-journal-search`** — 
- **`cnki-journal-toc`** — 
- **`cnki-navigate-pages`** — 
- **`cnki-paper-detail`** — 
- **`cnki-parse-results`** — 
- **`cnki-researcher`** — 
- **`cnki-search`** — 
- **`scholar-ppt-cn`** — 
- **`sci-extract`** — 
- **`sci-figure`** — 
- **`sci-html`** — 
- **`sci-ppt`** — 
- **`sci-review`** — 
- **`sci-search`** — 
- **`sci-zotero`** — 

### 安全与对齐 · safety  (4)

- **`bugbounty-workflow`** — 
- **`constitutional-ai`** — 
- **`nemo-guardrails`** — 
- **`prompt-guard`** — 

### 设计与前端 · design  (12)

- **`academic-plotting`** — 
- **`animation-vocabulary`** — 
- **`apple-design`** — 
- **`app-shell-ui`** — 
- **`chinese-plot-labels`** — 
- **`drawio-skill`** — 
- **`emil-design-eng`** — 
- **`find-animation-opportunities`** — 
- **`improve-animations`** — 
- **`pick-ui-library`** — 
- **`prototype`** — 
- **`review-animations`** — 

### 训练与推理 · ml  (39)

- **`accelerate`** — 
- **`awq`** — 
- **`axolotl`** — 
- **`bitsandbytes`** — 
- **`deepspeed`** — 
- **`flash-attention`** — 
- **`gguf`** — 
- **`gptq`** — 
- **`grpo-rl-training`** — 
- **`hqq`** — 
- **`knowledge-distillation`** — 
- **`litgpt`** — 
- **`llama-cpp`** — 
- **`llama-factory`** — 
- **`llamaguard`** — 
- **`llamaindex`** — 
- **`long-context`** — 
- **`mamba`** — 
- **`megatron-core`** — 
- **`miles`** — 
- **`model-merging`** — 
- **`model-pruning`** — 
- **`moe-training`** — 
- **`nanogpt`** — 
- **`openpi`** — 
- **`openrlhf`** — 
- **`openvla-oft`** — 
- **`peft`** — 
- **`rwkv`** — 
- **`sglang`** — 
- **`simpo`** — 
- **`slime`** — 
- **`speculative-decoding`** — 
- **`torchforge`** — 
- **`torchtitan`** — 
- **`trl-fine-tuning`** — 
- **`unsloth`** — 
- **`verl`** — 
- **`vllm`** — 

### 机器人 · robotics  (1)

- **`cosmos-policy`** — 

## 📲 同步到设备 · Sync to Devices

**桌面端 · Desktop（Claude Code 等）**

```bash
git clone https://github.com/Jensen-Yao/agents-skills.git ~/.agents/skills
```

**手机端 · Mobile（Termux 中的 DeepSeek Harness）**

```bash
# 在 Termux 中 · inside Termux
git clone https://github.com/Jensen-Yao/agents-skills.git ~/.agents/skills
# 或增量更新 · or incremental update
cd ~/.agents/skills && git pull
```

放置后无需重启：harness 的技能 watcher 会自动发现；也可在 App「关于 → 存储位置」中查看/编辑「技能目录」。*No restart needed — the skill watcher picks up changes automatically; you can also browse/edit the skills directory in the app's Storage page.*

## 📄 License

[MIT](LICENSE) —— 技能内容版权归各自作者 · *skill content copyright belongs to their respective authors.*