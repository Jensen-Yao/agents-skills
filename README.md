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

共 **140** 个技能，按类分组；**点击技能名查看完整 SKILL.md**；在线检索版（关键词搜索 + 分类筛选）：https://jensen-yao.github.io/agents-skills/
*140 skills grouped by category. Click a skill name to view its full SKILL.md; searchable online at the link above.*

### 学术文献 (19)

- [**`cnki-advanced-search`**](skills/cnki-advanced-search/SKILL.md) — 
- [**`cnki-download`**](skills/cnki-download/SKILL.md) — 
- [**`cnki-export`**](skills/cnki-export/SKILL.md) — 
- [**`cnki-journal-index`**](skills/cnki-journal-index/SKILL.md) — 
- [**`cnki-journal-search`**](skills/cnki-journal-search/SKILL.md) — 
- [**`cnki-journal-toc`**](skills/cnki-journal-toc/SKILL.md) — 
- [**`cnki-navigate-pages`**](skills/cnki-navigate-pages/SKILL.md) — 
- [**`cnki-paper-detail`**](skills/cnki-paper-detail/SKILL.md) — 
- [**`cnki-parse-results`**](skills/cnki-parse-results/SKILL.md) — 
- [**`cnki-researcher`**](skills/cnki-researcher/SKILL.md) — 
- [**`cnki-search`**](skills/cnki-search/SKILL.md) — 
- [**`scholar-ppt-cn`**](skills/scholar-ppt-cn/SKILL.md) — 
- [**`sci-extract`**](skills/sci-extract/SKILL.md) — 
- [**`sci-figure`**](skills/sci-figure/SKILL.md) — 
- [**`sci-html`**](skills/sci-html/SKILL.md) — 
- [**`sci-ppt`**](skills/sci-ppt/SKILL.md) — 
- [**`sci-review`**](skills/sci-review/SKILL.md) — 
- [**`sci-search`**](skills/sci-search/SKILL.md) — 
- [**`sci-zotero`**](skills/sci-zotero/SKILL.md) — 

### 训练与推理 (39)

- [**`accelerate`**](skills/accelerate/SKILL.md) — 
- [**`awq`**](skills/awq/SKILL.md) — 
- [**`axolotl`**](skills/axolotl/SKILL.md) — 
- [**`bitsandbytes`**](skills/bitsandbytes/SKILL.md) — 
- [**`deepspeed`**](skills/deepspeed/SKILL.md) — 
- [**`flash-attention`**](skills/flash-attention/SKILL.md) — 
- [**`gguf`**](skills/gguf/SKILL.md) — 
- [**`gptq`**](skills/gptq/SKILL.md) — 
- [**`grpo-rl-training`**](skills/grpo-rl-training/SKILL.md) — 
- [**`hqq`**](skills/hqq/SKILL.md) — 
- [**`knowledge-distillation`**](skills/knowledge-distillation/SKILL.md) — 
- [**`litgpt`**](skills/litgpt/SKILL.md) — 
- [**`llama-cpp`**](skills/llama-cpp/SKILL.md) — 
- [**`llama-factory`**](skills/llama-factory/SKILL.md) — 
- [**`llamaguard`**](skills/llamaguard/SKILL.md) — 
- [**`llamaindex`**](skills/llamaindex/SKILL.md) — 
- [**`long-context`**](skills/long-context/SKILL.md) — 
- [**`mamba`**](skills/mamba/SKILL.md) — 
- [**`megatron-core`**](skills/megatron-core/SKILL.md) — 
- [**`miles`**](skills/miles/SKILL.md) — 
- [**`model-merging`**](skills/model-merging/SKILL.md) — 
- [**`model-pruning`**](skills/model-pruning/SKILL.md) — 
- [**`moe-training`**](skills/moe-training/SKILL.md) — 
- [**`nanogpt`**](skills/nanogpt/SKILL.md) — 
- [**`openpi`**](skills/openpi/SKILL.md) — 
- [**`openrlhf`**](skills/openrlhf/SKILL.md) — 
- [**`openvla-oft`**](skills/openvla-oft/SKILL.md) — 
- [**`peft`**](skills/peft/SKILL.md) — 
- [**`rwkv`**](skills/rwkv/SKILL.md) — 
- [**`sglang`**](skills/sglang/SKILL.md) — 
- [**`simpo`**](skills/simpo/SKILL.md) — 
- [**`slime`**](skills/slime/SKILL.md) — 
- [**`speculative-decoding`**](skills/speculative-decoding/SKILL.md) — 
- [**`torchforge`**](skills/torchforge/SKILL.md) — 
- [**`torchtitan`**](skills/torchtitan/SKILL.md) — 
- [**`trl-fine-tuning`**](skills/trl-fine-tuning/SKILL.md) — 
- [**`unsloth`**](skills/unsloth/SKILL.md) — 
- [**`verl`**](skills/verl/SKILL.md) — 
- [**`vllm`**](skills/vllm/SKILL.md) — 

### 评估与基准 (3)

- [**`bigcode-evaluation-harness`**](skills/bigcode-evaluation-harness/SKILL.md) — 
- [**`lm-evaluation-harness`**](skills/lm-evaluation-harness/SKILL.md) — 
- [**`nemo-evaluator`**](skills/nemo-evaluator/SKILL.md) — 

### 研究与写作 (5)

- [**`brainstorming-research-ideas`**](skills/brainstorming-research-ideas/SKILL.md) — 
- [**`creative-thinking-for-research`**](skills/creative-thinking-for-research/SKILL.md) — 
- [**`ml-paper-writing`**](skills/ml-paper-writing/SKILL.md) — 
- [**`presenting-conference-talks`**](skills/presenting-conference-talks/SKILL.md) — 
- [**`systems-paper-writing`**](skills/systems-paper-writing/SKILL.md) — 

### 设计与前端 (12)

- [**`academic-plotting`**](skills/academic-plotting/SKILL.md) — 
- [**`animation-vocabulary`**](skills/animation-vocabulary/SKILL.md) — 
- [**`apple-design`**](skills/apple-design/SKILL.md) — 
- [**`app-shell-ui`**](skills/app-shell-ui/SKILL.md) — 
- [**`chinese-plot-labels`**](skills/chinese-plot-labels/SKILL.md) — 
- [**`drawio-skill`**](skills/drawio-skill/SKILL.md) — 
- [**`emil-design-eng`**](skills/emil-design-eng/SKILL.md) — 
- [**`find-animation-opportunities`**](skills/find-animation-opportunities/SKILL.md) — 
- [**`improve-animations`**](skills/improve-animations/SKILL.md) — 
- [**`pick-ui-library`**](skills/pick-ui-library/SKILL.md) — 
- [**`prototype`**](skills/prototype/SKILL.md) — 
- [**`review-animations`**](skills/review-animations/SKILL.md) — 

### 数据与检索 (11)

- [**`chroma`**](skills/chroma/SKILL.md) — 
- [**`faiss`**](skills/faiss/SKILL.md) — 
- [**`nemo-curator`**](skills/nemo-curator/SKILL.md) — 
- [**`nnsight`**](skills/nnsight/SKILL.md) — 
- [**`pinecone`**](skills/pinecone/SKILL.md) — 
- [**`pyvene`**](skills/pyvene/SKILL.md) — 
- [**`qdrant`**](skills/qdrant/SKILL.md) — 
- [**`ray-data`**](skills/ray-data/SKILL.md) — 
- [**`sentencepiece`**](skills/sentencepiece/SKILL.md) — 
- [**`sentence-transformers`**](skills/sentence-transformers/SKILL.md) — 
- [**`transformer-lens`**](skills/transformer-lens/SKILL.md) — 

### 安全与对齐 (4)

- [**`bugbounty-workflow`**](skills/bugbounty-workflow/SKILL.md) — 
- [**`constitutional-ai`**](skills/constitutional-ai/SKILL.md) — 
- [**`nemo-guardrails`**](skills/nemo-guardrails/SKILL.md) — 
- [**`prompt-guard`**](skills/prompt-guard/SKILL.md) — 

### 机器人 (1)

- [**`cosmos-policy`**](skills/cosmos-policy/SKILL.md) — 

### 框架与平台 (13)

- [**`autogpt`**](skills/autogpt/SKILL.md) — 
- [**`crewai`**](skills/crewai/SKILL.md) — 
- [**`dspy`**](skills/dspy/SKILL.md) — 
- [**`guidance`**](skills/guidance/SKILL.md) — 
- [**`instructor`**](skills/instructor/SKILL.md) — 
- [**`langchain`**](skills/langchain/SKILL.md) — 
- [**`langsmith`**](skills/langsmith/SKILL.md) — 
- [**`mlflow`**](skills/mlflow/SKILL.md) — 
- [**`outlines`**](skills/outlines/SKILL.md) — 
- [**`phoenix`**](skills/phoenix/SKILL.md) — 
- [**`swanlab`**](skills/swanlab/SKILL.md) — 
- [**`tensorboard`**](skills/tensorboard/SKILL.md) — 
- [**`weights-and-biases`**](skills/weights-and-biases/SKILL.md) — 

### 工具与CLI (33)

- [**`0-autoresearch-skill`**](skills/0-autoresearch-skill/SKILL.md) — 
- [**`a-evolve`**](skills/a-evolve/SKILL.md) — 
- [**`alibabacloud-find-skills`**](skills/alibabacloud-find-skills/SKILL.md) — 
- [**`audiocraft`**](skills/audiocraft/SKILL.md) — 
- [**`blip-2`**](skills/blip-2/SKILL.md) — 
- [**`cli-anything`**](skills/cli-anything/SKILL.md) — 
- [**`cli-creator`**](skills/cli-creator/SKILL.md) — 
- [**`clip`**](skills/clip/SKILL.md) — 
- [**`dramaclaw`**](skills/dramaclaw/SKILL.md) — 
- [**`hatch-pet`**](skills/hatch-pet/SKILL.md) — 
- [**`huggingface-tokenizers`**](skills/huggingface-tokenizers/SKILL.md) — 
- [**`imagegen`**](skills/imagegen/SKILL.md) — 
- [**`image-gen-fuck`**](skills/image-gen-fuck/SKILL.md) — 
- [**`karpathy-guidelines`**](skills/karpathy-guidelines/SKILL.md) — 
- [**`lambda-labs`**](skills/lambda-labs/SKILL.md) — 
- [**`libreoffice-local-install`**](skills/libreoffice-local-install/SKILL.md) — 
- [**`llava`**](skills/llava/SKILL.md) — 
- [**`ml-training-recipes`**](skills/ml-training-recipes/SKILL.md) — 
- [**`modal`**](skills/modal/SKILL.md) — 
- [**`officecli`**](skills/officecli/SKILL.md) — 
- [**`playwright`**](skills/playwright/SKILL.md) — 
- [**`pytorch-fsdp2`**](skills/pytorch-fsdp2/SKILL.md) — 
- [**`pytorch-lightning`**](skills/pytorch-lightning/SKILL.md) — 
- [**`ray-train`**](skills/ray-train/SKILL.md) — 
- [**`saelens`**](skills/saelens/SKILL.md) — 
- [**`segment-anything`**](skills/segment-anything/SKILL.md) — 
- [**`skypilot`**](skills/skypilot/SKILL.md) — 
- [**`stable-diffusion`**](skills/stable-diffusion/SKILL.md) — 
- [**`tensorrt-llm`**](skills/tensorrt-llm/SKILL.md) — 
- [**`visiomaster`**](skills/visiomaster/SKILL.md) — 
- [**`whisper`**](skills/whisper/SKILL.md) — 
- [**`windows-deployment-cli-locations`**](skills/windows-deployment-cli-locations/SKILL.md) — 
- [**`winui-app`**](skills/winui-app/SKILL.md) — 

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