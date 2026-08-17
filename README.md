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

共 **150** 个技能，按类分组；**点击技能名查看完整 SKILL.md**；在线检索版（关键词搜索 + 分类筛选）：https://jensen-yao.github.io/agents-skills/
*150 skills grouped by category. Click a skill name to view its full SKILL.md; searchable online at the link above.*

### 学术文献 (19)

- [**`cnki-advanced-search`**](skills/cnki-advanced-search/SKILL.md) — 在 CNKI 上执行高级检索，支持作者、标题、期刊、日期范围、来源类别等字段过滤。当用户需要超越简单关键词的精确过滤检索时使用。
- [**`cnki-download`**](skills/cnki-download/SKILL.md) — 从 CNKI 下载论文 PDF/CAJ。需要用户已登录。当用户想下载某篇特定论文时使用。
- [**`cnki-export`**](skills/cnki-export/SKILL.md) — 从 CNKI 导出论文并推送到 Zotero，或保存为 RIS 文件。当用户想把论文保存到 Zotero 或导出引文数据时使用。
- [**`cnki-journal-index`**](skills/cnki-journal-index/SKILL.md) — 在 CNKI 上查询期刊收录与索引状态，获取影响因子和评价数据。当用户询问期刊级别、收录或排名时使用。
- [**`cnki-journal-search`**](skills/cnki-journal-search/SKILL.md) — 在 CNKI 上按名称、ISSN、CN 或主办单位搜索期刊或出版物。当用户想查找特定期刊或浏览出版物时使用。
- [**`cnki-journal-toc`**](skills/cnki-journal-toc/SKILL.md) — 在 CNKI 上浏览期刊期次、查看目录，并下载原始目录 PDF。当用户想查看某期期刊的论文或下载原始封面目录页时使用。
- [**`cnki-navigate-pages`**](skills/cnki-navigate-pages/SKILL.md) — 在 CNKI 搜索结果页之间导航或更改排序方式。当用户想查看更多结果或更改排序时使用。
- [**`cnki-paper-detail`**](skills/cnki-paper-detail/SKILL.md) — 从 CNKI 论文页面提取完整论文信息，包括标题、作者、机构、摘要、关键词、基金、分类。当用户需要某篇论文的详细信息时使用。
- [**`cnki-parse-results`**](skills/cnki-parse-results/SKILL.md) — 将当前 CNKI 搜索结果页解析为结构化论文数据（标题、作者、期刊、日期、被引）。在执行搜索后需要提取结果时使用。
- [**`cnki-researcher`**](skills/cnki-researcher/SKILL.md) — 在 Codex 中使用 Chrome DevTools MCP 协调 CNKI 文献研究工作流。当用户要求搜索 CNKI 论文、查看论文详情、浏览期刊或期次、检查期刊收录、下载 CNKI 文件、导出引文、处理登录，或将上述任务组合成文献研究工作流时使用。
- [**`cnki-search`**](skills/cnki-search/SKILL.md) — 按关键词在 CNKI（中国知网）搜索论文。当用户想查找某个主题的学术论文时使用。
- [**`scholar-ppt-cn`**](skills/scholar-ppt-cn/SKILL.md) — 当用户想要根据论文、学位论文、报告、图表、笔记、参考模板、截图或视觉原型创建、重设风格或重建中文学术 PowerPoint 时使用。该工作流保持用户界面简洁，同时恢复有用的规划环节。首先创建制作规划表，将每页幻灯片映射到叙事章节、源素材、核心信息和详细的版式原型；然后创建原型族加变体蓝图。只有确立这一族蓝图后，才会生成视觉样例和可编辑 PPTX。
- [**`sci-extract`**](skills/sci-extract/SKILL.md) — 通读学术论文并提取专业的研究洞见、图表、元数据和批判性评价。当用户分享科学论文、综述、系统综述、元分析、范围综述、arXiv 链接、DOI、PDF 或粘贴的论文文本，并要求阅读、总结、分析、提取、消化、评审、批判或解释时使用。对于原创研究论文，产出改良版 Heilmeier 分析；对于综述文献，产出范围地图式提取。不要将此技能用于非学术文章、博客或新闻。
- [**`sci-figure`**](skills/sci-figure/SKILL.md) — 从学术 PDF 论文中提取图形和子图。支持 Fig、Figure、Scheme、Chart、Supplementary Figure、Extended Data Figure 及对应中文（图、方案、示意图、附图、补充图）。子图标签识别支持多种格式。以可配置 DPI 输出高质量 PNG。
- [**`sci-html`**](skills/sci-html/SKILL.md) — 根据 PDF、结构化文本、Markdown、论文摘要、大纲或研究笔记生成学术演示风格的 HTML 幻灯片和浏览器报告。当用户想把科学论文 PDF 直接转换为交互式 HTML 报告、可点击的网页演示、可分享的浏览器幻灯片，或带图表、结构化洞见、章节页和离线目录输出的类 PPT HTML 时使用。
- [**`sci-ppt`**](skills/sci-ppt/SKILL.md) — 根据论文 PDF、结构化大纲或纯文本生成专业的学术 PowerPoint（PPTX）演示。用于论文答辩、组会报告、文献汇报和研究生申请。支持自动提取图表、LaTeX 公式渲染和中英双语排版。
- [**`sci-review`**](skills/sci-review/SKILL.md) — 用于起草、打磨和回应学术文献综述与同行评审意见的专项工作流。适用于文献综述大纲、研究空白综合、审稿人反驳、回复信和学术写作语气修正。
- [**`sci-search`**](skills/sci-search/SKILL.md) — 学术论文搜索与指标分析。同时检索 arXiv、PubMed 和 Web of Science，并附带期刊影响因子数据。当用户请求搜索论文或查找文献时触发。
- [**`sci-zotero`**](skills/sci-zotero/SKILL.md) — 与你的 Zotero 文献库交互，同步参考文献、按 DOI、ISBN、PMID 添加引文并管理 PDF。当用户提出与 Zotero 相关的请求时触发。

### 训练与推理 (39)

- [**`accelerate`**](skills/accelerate/SKILL.md) — 最简单的分布式训练 API。只需 4 行代码即可为任意 PyTorch 脚本添加分布式支持。为 DeepSpeed/FSDP/Megatron/DDP 提供统一 API。自动设备放置、混合精度（FP16/BF16/FP8）。交互式配置、单条启动命令。HuggingFace 生态标准。
- [**`awq`**](skills/awq/SKILL.md) — 激活感知权重量化，实现 4-bit LLM 压缩，3 倍加速且精度损失极小。当在有限的 GPU 显存上部署大模型、需要比 GPTQ 更快且精度保持更好的推理，或处理指令微调和多模态模型时使用。MLSys 2024 最佳论文奖得主。
- [**`axolotl`**](skills/axolotl/SKILL.md) — 使用 Axolotl 微调 LLM 的专家级指导——YAML 配置、100+ 模型、LoRA/QLoRA、DPO/KTO/ORPO/GRPO、多模态支持。
- [**`bitsandbytes`**](skills/bitsandbytes/SKILL.md) — 将 LLM 量化到 8-bit 或 4-bit，内存减少 50-75% 且精度损失极小。当 GPU 显存有限、需要装入更大模型或想要更快推理时使用。支持 INT8、NF4、FP4 格式、QLoRA 训练和 8-bit 优化器。可与 HuggingFace Transformers 配合使用。
- [**`deepspeed`**](skills/deepspeed/SKILL.md) — 使用 DeepSpeed 进行分布式训练的专家级指导——ZeRO 优化阶段、流水线并行、FP16/BF16/FP8、1-bit Adam、稀疏注意力。
- [**`flash-attention`**](skills/flash-attention/SKILL.md) — 使用 Flash Attention 优化 transformer 注意力，实现 2-4 倍加速和 10-20 倍内存缩减。当训练或运行长序列的 transformer、遇到注意力机制的 GPU 显存问题，或需要更快推理时使用。支持 PyTorch 原生 SDPA、flash-attn 库、H100 FP8 和滑动窗口注意力。
- [**`gguf`**](skills/gguf/SKILL.md) — GGUF 格式与 llama.cpp 量化，实现高效的 CPU 与 GPU 推理。当在消费级硬件、Apple Silicon 上部署模型，或需要无需 GPU 的 2-8 bit 灵活量化时使用。
- [**`gptq`**](skills/gptq/SKILL.md) — 训练后 4-bit 量化，精度损失极小。用于在消费级 GPU 上部署大模型，需要 4 倍内存缩减且困惑度下降小于 2%，或相比 FP16 实现更快推理（3-4 倍加速）时使用。可与 transformers 和 PEFT 集成以进行 QLoRA 微调。
- [**`grpo-rl-training`**](skills/grpo-rl-training/SKILL.md) — 使用 TRL 进行 GRPO 与 RL 微调的专家级指导，适用于推理和任务特定模型的训练。
- [**`hqq`**](skills/hqq/SKILL.md) — 无需校准数据的半二次量化（HQQ）。当需要在没有校准数据集的情况下将模型量化到 4、3、2-bit 精度、追求快速量化工作流，或搭配 vLLM 或 HuggingFace Transformers 部署时使用。
- [**`knowledge-distillation`**](skills/knowledge-distillation/SKILL.md) — 通过从教师模型到学生模型的知识蒸馏压缩大语言模型。当部署保持性能的更小模型、将 GPT-4 的能力迁移到开源模型或降低推理成本时使用。涵盖温度缩放、软目标、反向 KLD、logit 蒸馏和 MiniLLM 训练策略。
- [**`litgpt`**](skills/litgpt/SKILL.md) — 使用 Lightning AI 的 LitGPT 实现并训练 LLM，支持 20+ 预训练架构（Llama、Gemma、Phi、Qwen、Mistral）。当需要干净的模型实现、教学式的架构理解，或使用 LoRA 与 QLoRA 进行生产微调时使用。单文件实现，无抽象层。
- [**`llama-cpp`**](skills/llama-cpp/SKILL.md) — 无需 NVIDIA 硬件即可在 CPU、Apple Silicon 和消费级 GPU 上运行 LLM 推理。用于边缘部署、M1 与 M2 与 M3 Mac、AMD 与 Intel GPU 或 CUDA 不可用的场景。支持 GGUF 量化以减少内存，在 CPU 上相比 PyTorch 快 4-10 倍。
- [**`llama-factory`**](skills/llama-factory/SKILL.md) — 使用 LLaMA-Factory 微调 LLM 的专家级指导——WebUI 无代码、100+ 模型、2 至 8-bit QLoRA、多模态支持。
- [**`llamaguard`**](skills/llamaguard/SKILL.md) — Meta 专用于 LLM 输入与输出过滤的 7-8B 审核模型。覆盖 6 类安全风险，准确率 94-95%。可通过 vLLM、HuggingFace、Sagemaker 部署，并与 NeMo Guardrails 集成。
- [**`llamaindex`**](skills/llamaindex/SKILL.md) — 用于构建 RAG LLM 应用的数据框架。专注于文档摄取（300+ 连接器）、索引和查询。具备向量索引、查询引擎、智能体与多模态支持。用于文档问答、聊天机器人、知识检索或构建 RAG 流水线，最适合以数据为中心的 LLM 应用。
- [**`long-context`**](skills/long-context/SKILL.md) — 使用 RoPE、YaRN、ALiBi 和位置插值技术扩展 transformer 模型的上下文窗口。当处理长文档、将预训练模型扩展到超出原始上下文限制，或实现高效位置编码时使用。涵盖旋转位置嵌入、注意力偏置、插值方法和面向 LLM 的外推策略。
- [**`mamba`**](skills/mamba/SKILL.md) — 复杂度为 O(n) 的状态空间模型，而 Transformer 为 O(n2)。推理快 5 倍、支持百万 token 序列、无需 KV cache。采用硬件感知设计的选择性 SSM。包含 Mamba-1 和 Mamba-2（多头）。HuggingFace 上有 130M-2.8B 的模型。
- [**`megatron-core`**](skills/megatron-core/SKILL.md) — 使用 NVIDIA Megatron-Core 训练大语言模型（2B-462B 参数），支持高级并行策略。当训练大于 1B 参数的模型、需要最大化 GPU 效率或需要张量、流水线、序列、上下文、专家并行时使用。用于 Nemotron、Llama、DeepSeek 的生产级框架。
- [**`miles`**](skills/miles/SKILL.md) — 提供使用 miles（slime 的生产级分支）进行企业级 RL 训练的指导。当训练 FP8 与 INT4 的大型 MoE 模型、需要训练与推理对齐，或需要投机 RL 以获得最大吞吐量时使用。
- [**`model-merging`**](skills/model-merging/SKILL.md) — 使用 mergekit 合并多个微调模型以组合能力，无需重新训练。当通过融合领域专长创建专用模型、追求超越单一模型的性能，或快速试验模型变体时使用。涵盖 SLERP、TIES-Merging、DARE、Task Arithmetic、线性合并和生产部署策略。
- [**`model-pruning`**](skills/model-pruning/SKILL.md) — 使用 Wanda、SparseGPT 等剪枝技术减小 LLM 体积并加速推理。当无需重新训练即可压缩模型、以极小精度损失实现 50% 稀疏度，或在硬件加速器上实现更快推理时使用。涵盖非结构化剪枝、结构化剪枝、N:M 稀疏、幅度剪枝和一次性方法。
- [**`moe-training`**](skills/moe-training/SKILL.md) — 使用 DeepSpeed 或 HuggingFace 训练混合专家（MoE）模型。当算力有限却要训练大规模模型、实现 Mixtral 8x7B 或 DeepSeek-V3 等稀疏架构，或在不按比例增加算力的情况下扩展模型容量时使用。涵盖 MoE 架构、路由机制、负载均衡、专家并行和推理优化。
- [**`nanogpt`**](skills/nanogpt/SKILL.md) — 约 300 行的教学版 GPT 实现。可在 OpenWebText 上复现 GPT-2（124M）。代码干净、易于改造，适合学习 transformer。作者 Andrej Karpathy。非常适合从零理解 GPT 架构。
- [**`openpi`**](skills/openpi/SKILL.md) — 使用 JAX 或 PyTorch 后端微调并部署 Physical Intelligence 的 OpenPI 模型（pi0、pi0-fast、pi0.5），在 ALOHA、DROID 和 LIBERO 环境中进行机器人策略推理。当将 pi0 模型适配到自定义数据集、运行策略推理服务器或排查归一化统计和 GPU 显存问题时使用。
- [**`openrlhf`**](skills/openrlhf/SKILL.md) — 高性能 RLHF 框架，搭载 Ray 与 vLLM 加速。用于大模型的 PPO、GRPO、RLOO、DPO 训练。基于 Ray、vLLM、ZeRO-3 构建。凭借分布式架构和 GPU 资源共享，比 DeepSpeedChat 快 2 倍。
- [**`openvla-oft`**](skills/openvla-oft/SKILL.md) — 微调并评估 OpenVLA-OFT 和 OpenVLA-OFT+ 策略，使用连续动作头、LoRA 适配和 FiLM 条件机制在 LIBERO 仿真与 ALOHA 真实场景中生成机器人动作。当复现论文结果、训练自定义 VLA 动作头、为 ALOHA 部署服务端-客户端推理，或排查归一化、LoRA 合并和跨 GPU 问题时使用。
- [**`peft`**](skills/peft/SKILL.md) — 使用 LoRA、QLoRA 及 25+ 方法对 LLM 进行参数高效微调。当 GPU 显存有限却要微调大模型、需要仅训练少于 1% 的参数且精度损失极小，或需要多适配器服务时使用。HuggingFace 官方库，与 transformers 生态深度集成。
- [**`rwkv`**](skills/rwkv/SKILL.md) — RNN 与 Transformer 混合架构，推理复杂度 O(n)。线性时间、无限上下文、无 KV cache。像 GPT 一样训练（并行）、像 RNN 一样推理（顺序）。Linux Foundation AI 项目。RWKV-7（2025 年 3 月）。模型参数最高达 14B。
- [**`sglang`**](skills/sglang/SKILL.md) — 具备 RadixAttention 前缀缓存的快速结构化生成与服务框架。用于 JSON 与正则输出、受约束解码、带工具调用的智能体工作流，或需要借助前缀共享实现比 vLLM 快 5 倍的推理时使用。支撑 xAI、AMD、NVIDIA 和 LinkedIn 的 30 万+ GPU。
- [**`simpo`**](skills/simpo/SKILL.md) — 用于 LLM 对齐的简单偏好优化（SimPO）。无需参考模型的 DPO 替代方案，性能更优（AlpacaEval 2.0 上+6.4 分）。不需要参考模型，比 DPO 更高效。当想要比 DPO 与 PPO 更简单、更快的偏好对齐训练时使用。
- [**`slime`**](skills/slime/SKILL.md) — 提供使用 slime（Megatron 与 SGLang 框架）进行 LLM 强化学习后训练的指导。当训练 GLM 模型、实现自定义数据生成工作流，或需要与 Megatron-LM 紧密集成以扩展 RL 时使用。
- [**`speculative-decoding`**](skills/speculative-decoding/SKILL.md) — 使用投机解码、Medusa 多头和前瞻解码技术加速 LLM 推理。当优化推理速度、降低实时应用延迟或在算力有限的环境部署模型时使用。涵盖草稿模型、树状注意力、Jacobi 迭代、并行 token 生成和生产部署策略。
- [**`torchforge`**](skills/torchforge/SKILL.md) — 提供使用 torchforge（Meta 将基础设施与算法分离的库）进行 PyTorch 原生智能体强化学习的指导。当想要干净的 RL 抽象、轻松的算法实验，或借助 Monarch 和 TorchTitan 进行可扩展训练时使用。
- [**`torchtitan`**](skills/torchtitan/SKILL.md) — 使用 torchtitan 进行 PyTorch 原生的分布式 LLM 预训练，支持 4D 并行（FSDP2、TP、PP、CP）。当使用 Float8、torch.compile 和分布式 checkpoint 预训练 Llama 3.1、DeepSeek V3 或自定义模型，规模从 8 到 512+ GPU 时使用。
- [**`trl-fine-tuning`**](skills/trl-fine-tuning/SKILL.md) — 使用 TRL 通过强化学习微调 LLM——SFT 用于指令微调、DPO 用于偏好对齐、PPO 与 GRPO 用于奖励优化，以及奖励模型训练。当需要 RLHF、让模型对齐偏好或基于人类反馈训练时使用。
- [**`unsloth`**](skills/unsloth/SKILL.md) — 使用 Unsloth 快速微调的专家级指导——训练快 2-5 倍、内存减少 50-80%、LoRA 与 QLoRA 优化。
- [**`verl`**](skills/verl/SKILL.md) — 提供使用 verl（火山引擎 RL）进行 LLM 强化学习训练的指导。当以灵活的基础设施后端大规模实现 RLHF、GRPO、PPO 或其他 RL 算法进行 LLM 后训练时使用。
- [**`vllm`**](skills/vllm/SKILL.md) — 使用 vLLM 的 PagedAttention 和连续批处理以高吞吐量服务 LLM。当部署生产级 LLM API、优化推理延迟与吞吐量或在有限 GPU 显存下服务模型时使用。支持 OpenAI 兼容端点、量化（GPTQ、AWQ、FP8）和张量并行。

### 评估与基准 (3)

- [**`bigcode-evaluation-harness`**](skills/bigcode-evaluation-harness/SKILL.md) — 使用 pass@k 指标在 HumanEval、MBPP、MultiPL-E 等 15+ 基准上评估代码生成模型。当对代码模型做基准测试、比较编码能力、测试多语言支持或衡量代码生成质量时使用。来自 BigCode Project 的行业标准，被 HuggingFace 排行榜采用。
- [**`lm-evaluation-harness`**](skills/lm-evaluation-harness/SKILL.md) — 在 60+ 学术基准（MMLU、HumanEval、GSM8K、TruthfulQA、HellaSwag）上评估 LLM。当对模型质量做基准测试、比较模型、报告学术结果或追踪训练进度时使用。EleutherAI、HuggingFace 及各大实验室使用的行业标准。
- [**`nemo-evaluator`**](skills/nemo-evaluator/SKILL.md) — 整合 18+ 评测工具、跨 100+ 基准以多后端执行评估 LLM。当需要在本地 Docker、Slurm HPC 或云平台上进行可扩展评估时使用。NVIDIA 的企业级平台，采用容器优先架构，保证基准测试可复现。

### 研究与写作 (5)

- [**`brainstorming-research-ideas`**](skills/brainstorming-research-ideas/SKILL.md) — 引导研究者通过结构化构思框架发现高影响力的研究方向。当探索新的问题领域、在项目之间转换方向或为现有工作寻找新颖视角时使用。
- [**`creative-thinking-for-research`**](skills/creative-thinking-for-research/SKILL.md) — 将认知科学的创造性思维框架应用于 CS 与 AI 研究的构思。当希望通过组合式创造、类比推理、约束操控等有实证依据的创意策略寻找真正新颖的研究方向时使用。
- [**`ml-paper-writing`**](skills/ml-paper-writing/SKILL.md) — 为 NeurIPS、ICML、ICLR、ACL、AAAI、COLM 撰写达到发表水准的 ML 与 AI 论文。当从研究仓库起草论文、组织论证结构、核实引用或准备 camera-ready 终稿时使用。若面向系统类会议，请改用 systems-paper-writing。
- [**`presenting-conference-talks`**](skills/presenting-conference-talks/SKILL.md) — 根据已完成的论文生成会议演讲幻灯片（Beamer LaTeX PDF 和可编辑 PPTX），附带演讲者备注和讲稿。当为 ML 和系统类会议准备口头报告、spotlight 展示或特邀报告时使用。
- [**`systems-paper-writing`**](skills/systems-paper-writing/SKILL.md) — 面向 OSDI、SOSP、ASPLOS、NSDI 和 EuroSys 的系统类论文写作综合指南。提供段落级结构蓝图、写作范式、按会议区分的检查清单、审稿人指南、LaTeX 模板和会议截稿日期。所有系统类会议论文写作都使用本技能。

### 设计与前端 (20)

- [**`academic-plotting`**](skills/academic-plotting/SKILL.md) — 根据研究上下文为 ML 论文生成出版级图表。给定论文章节或描述时，提取系统组件与关系，通过 Gemini 生成架构图；给定实验结果或数据时，自动选择图表类型，通过 matplotlib/seaborn 生成数据图表。为会议论文制作任何图表时使用。
- [**`animation-vocabulary`**](skills/animation-vocabulary/SKILL.md) — 反向查找术语表，把对网页动画或动效的模糊描述转换为准确术语。当用户问&quot;这叫什么来着&quot;、或描述一个动效却不知道其名称、想要正确的词来提示 AI 或设计师时使用。用于命名效果，而非设计或实现。
- [**`apple-design`**](skills/apple-design/SKILL.md) — 将 Apple 的界面设计与流畅物理动效方法论移植到 Web。当构建或评审手势驱动的 UI、弹簧动画、拖拽/滑动/底部面板交互、动量和可打断转场、半透明材质与层次、排版、减弱动态效果，或 Apple 风格界面背后的设计基础时使用。
- [**`app-shell-ui`**](skills/app-shell-ui/SKILL.md) — 使用 App Shell UI 风格构建或重设前端界面——简洁克制的 macOS 风桌面工具外壳（左侧导航加内容区、柔和表面、抬升卡片、单一品牌强调色、设置列表式文案），自带明暗双主题。
- [**`baseline-ui`**](skills/baseline-ui/SKILL.md) — 快速清理 AI 生成界面的间距、层级、排版和小型布局问题。当界面需要一轮快速整理或打磨时使用。
- [**`chinese-plot-labels`**](skills/chinese-plot-labels/SKILL.md) — 当 Codex 编写或修改生成图表、曲线图、图形或图片输出的 Python、Java 或 C++ 代码时使用。若用户未明确指定其他语言，生成的图像需使用中文标题、坐标轴标签和图例。
- [**`create-design-md`**](skills/create-design-md/SKILL.md) — 根据现有产品仓库或公开网站创建或更新 DESIGN.md，记录经过证据验证的设计语言、设计令牌与实现指导。当需要为编码智能体补充持久化 UI 上下文时使用。
- [**`diagram-design`**](skills/diagram-design/SKILL.md) — 创建带品牌感的架构图、流程图、时序图、状态机、ER 图、时间线、泳道图、矩阵和数据流图，并可将 draw.io 或 Mermaid 源文件重绘为独立 HTML、SVG 或 PNG。
- [**`drawio-skill`**](skills/drawio-skill/SKILL.md) — 当用户要求绘制示意图、流程图、架构图、ER 图、UML 时序或类图、网络拓扑、ML 与 DL 模型结构图、思维导图或任何可视化时使用。当图表需要自定义样式、丰富的形状库、泳道或可导出图片（PNG、SVG、PDF、JPG）时最为合适。生成 .drawio XML，并通过本机 draw.io 桌面 CLI 导出。
- [**`emil-design-eng`**](skills/emil-design-eng/SKILL.md) — 本技能凝练了 Emil Kowalski 关于 UI 打磨、组件设计、动画决策以及让软件手感出色的那些隐形细节的设计哲学。
- [**`find-animation-opportunities`**](skills/find-animation-opportunities/SKILL.md) — 在代码库或 UI 中找出应该加动画却没有加的地方，并排除不该加动画的部分。只读操作；它给出带精确参数的动效建议，但不会落地实现。若要修复现有动画，请改用 improve-animations 或 review-animations。
- [**`fixing-accessibility`**](skills/fixing-accessibility/SKILL.md) — 审计并修复 HTML 无障碍问题，包括 ARIA 标签、键盘导航、焦点管理、颜色对比度和表单错误。当添加交互控件、表单、对话框或检查 WCAG 合规性时使用。
- [**`fixing-metadata`**](skills/fixing-metadata/SKILL.md) — 审计并修复页面元数据，包括标题、描述、规范链接、Open Graph、Twitter 卡片、favicon、JSON-LD 和 robots 指令。当需要 SEO 或社交分享预览时使用。
- [**`fixing-motion-performance`**](skills/fixing-motion-performance/SKILL.md) — 审计并修复动画性能问题，包括布局抖动、合成属性、滚动关联动效和模糊效果。当动画卡顿或转场不流畅时使用。
- [**`improve-animations`**](skills/improve-animations/SKILL.md) — 以资深动效顾问的身份审视代码库中的动画与动效代码，产出带优先级的审计报告和可独立执行的实现方案，供其他智能体执行。对源代码只读——它只规划改进，不实际修改。
- [**`improve-ui`**](skills/improve-ui/SKILL.md) — 基于产品自身的设计证据审计现有界面，识别已验证的 UI 问题，并为另一个智能体编写可独立执行的改进计划；保持产品身份且只读产品源代码。
- [**`pick-ui-library`**](skills/pick-ui-library/SKILL.md) — 从一份精心筛选、带倾向性建议的前端库清单中，为给定任务挑选合适的库——数字输入、OTP 输入、图表、命令菜单、虚拟化、拖拽、toast 提示、状态管理、样式等。仅在显式调用时运行，不会自行触发。
- [**`prototype`**](skills/prototype/SKILL.md) — 为你描述的 UI 片段构建多个真正不同的版本，渲染在可视化选择器后面，让你可以实时翻看并把感觉合适的那一版提升为正式方案。仅在显式调用时运行，不会自行触发。
- [**`review-animations`**](skills/review-animations/SKILL.md) — 以源自 Emil Kowalski 设计工程哲学的高工艺标准评审动画与动效代码。默认倾向标记问题；通过标准才算通过。
- [**`ui-skills-root`**](skills/ui-skills-root/SKILL.md) — UI 任务的路由层，使用 ui-skills CLI 选择最小且最合适的 UI Skills 上下文，再进入实现阶段。

### 数据与检索 (11)

- [**`chroma`**](skills/chroma/SKILL.md) — 面向 AI 应用的开源嵌入向量数据库。存储 embedding 与元数据，支持向量和全文检索、按元数据过滤。仅 4 个函数的简单 API。可从笔记本扩展到生产集群。用于语义搜索、RAG 应用或文档检索，最适合本地开发和开源项目。
- [**`faiss`**](skills/faiss/SKILL.md) — Facebook 的高效稠密向量相似度搜索与聚类库。支持数十亿向量、GPU 加速和多种索引类型。用于快速 k-NN 搜索、大规模向量检索，或需要不带元数据的纯相似度搜索场景，最适合高性能应用。
- [**`nemo-curator`**](skills/nemo-curator/SKILL.md) — 用于 LLM 训练的 GPU 加速数据治理工具。支持文本、图像、视频、音频。具备模糊去重、质量过滤、语义去重、PII 脱敏、NSFW 检测。通过 RAPIDS 跨 GPU 扩展。
- [**`nnsight`**](skills/nnsight/SKILL.md) — 提供使用 nnsight 解释和操控神经网络内部的指导，可选 NDIF 远程执行。当需要在不具备本地 GPU 资源的情况下对大规模模型（70B+）运行可解释性实验，或处理任意 PyTorch 架构时使用。
- [**`pinecone`**](skills/pinecone/SKILL.md) — 面向生产 AI 应用的托管向量数据库。全托管、自动扩展，支持混合检索、元数据过滤和命名空间。低延迟。用于生产级 RAG、推荐系统或大规模语义搜索，最适合无服务器托管基础设施。
- [**`pyvene`**](skills/pyvene/SKILL.md) — 提供使用 pyvene 声明式干预框架对 PyTorch 模型进行因果干预的指导。当进行因果追踪、激活替换、交换干预训练或检验关于模型行为的因果假设时使用。
- [**`qdrant`**](skills/qdrant/SKILL.md) — 用于 RAG 和语义搜索的高性能向量相似度检索引擎。当构建需要快速近邻搜索、带过滤的混合检索或具备 Rust 高性能可扩展向量存储的生产级 RAG 系统时使用。
- [**`ray-data`**](skills/ray-data/SKILL.md) — 面向 ML 工作负载的可扩展数据处理。支持跨 CPU 与 GPU 流式执行，支持 Parquet、CSV、JSON、图像。与 Ray Train、PyTorch、TensorFlow 集成。可从单机扩展到数百节点。用于批量推理、数据预处理、多模态数据加载或分布式 ETL 流水线。
- [**`sentencepiece`**](skills/sentencepiece/SKILL.md) — 与语言无关的分词器，将文本视为原始 Unicode。支持 BPE 和 Unigram 算法。速度快、轻量、词表确定。无需预分词即可在原始文本上训练。当需要多语言支持、中日韩文字或可复现的分词时使用。
- [**`sentence-transformers`**](skills/sentence-transformers/SKILL.md) — 用于 SOTA 句子、文本和图像 embedding 的框架。提供 5000+ 预训练模型，支持语义相似度、聚类和检索。支持多语言、领域特定和多模态模型。用于为 RAG、语义搜索或相似度任务生成 embedding，最适合生产环境下的 embedding 生成。
- [**`transformer-lens`**](skills/transformer-lens/SKILL.md) — 提供使用 TransformerLens 进行机制可解释性研究的指导，通过 HookPoints 和激活缓存检查与操控 transformer 内部。当逆向解析模型算法、研究注意力模式或进行激活替换实验时使用。

### 安全与对齐 (4)

- [**`bugbounty-workflow`**](skills/bugbounty-workflow/SKILL.md) — 授权范围内漏洞挖掘全流程工作流:侦察到挖掘到验证到报告。当用户要求挖洞、测目标、渗透测试、打点或提交 SRC 时使用。
- [**`constitutional-ai`**](skills/constitutional-ai/SKILL.md) — Anthropic 通过自我改进训练无害 AI 的方法。两阶段方案——先进行带自我批评与修订的监督学习，再进行 RLAIF（基于 AI 反馈的强化学习）。用于安全对齐、无需人工标注即可减少有害输出。支撑 Claude 的安全系统。
- [**`nemo-guardrails`**](skills/nemo-guardrails/SKILL.md) — NVIDIA 面向 LLM 应用的运行时安全框架。具备越狱检测、输入与输出校验、事实核查、幻觉检测、PII 过滤、毒性检测。使用 Colang 2.0 DSL 实现可编程护栏。生产就绪，可在 T4 GPU 上运行。
- [**`prompt-guard`**](skills/prompt-guard/SKILL.md) — Meta 的 86M 提示注入与越狱检测器。为 LLM 应用过滤恶意提示和第三方数据。TPR 99%+、FPR 小于 1%。速度快（GPU 上小于 2ms）。支持多语言。可通过 HuggingFace 部署或批量处理，用于 RAG 安全。

### 机器人 (1)

- [**`cosmos-policy`**](skills/cosmos-policy/SKILL.md) — 在 LIBERO 和 RoboCasa 仿真环境中评估 NVIDIA Cosmos Policy。当为机器人操作评估配置 cosmos-policy、使用 EGL 渲染运行无头 GPU 评估，或在集群或本地 GPU 机器上分析推理延迟时使用。

### 框架与平台 (13)

- [**`autogpt`**](skills/autogpt/SKILL.md) — 用于构建和部署持续性智能体的自主 AI 智能体平台。当创建可视化工作流智能体、部署持久运行的自主智能体或构建复杂的多步骤 AI 自动化系统时使用。
- [**`crewai`**](skills/crewai/SKILL.md) — 面向自主 AI 协作的多智能体编排框架。当构建由专职智能体组成的团队协作处理复杂任务、需要带记忆的基于角色的智能体协作，或需要顺序与分层执行的生产工作流时使用。不依赖 LangChain，精简而快速。
- [**`dspy`**](skills/dspy/SKILL.md) — 使用声明式编程构建复杂 AI 系统，自动优化提示词，用 DSPy 创建模块化 RAG 系统和智能体——斯坦福 NLP 的系统化 LM 编程框架。
- [**`guidance`**](skills/guidance/SKILL.md) — 用正则和文法控制 LLM 输出，保证生成的 JSON、XML、代码有效，强制结构化格式，并用 Guidance 构建多步骤工作流——微软研究院的受约束生成框架。
- [**`instructor`**](skills/instructor/SKILL.md) — 使用 Instructor 从 LLM 响应中提取结构化数据——Pydantic 校验、自动重试失败的提取、类型安全地解析复杂 JSON、流式返回部分结果。久经考验的结构化输出库。
- [**`langchain`**](skills/langchain/SKILL.md) — 用于构建 LLM 应用的框架，支持智能体、链和 RAG。支持多家提供商、500+ 集成、ReAct 智能体、工具调用、记忆管理和向量库检索。用于构建聊天机器人、问答系统、自主智能体或 RAG 应用，最适合快速原型开发和生产部署。
- [**`langsmith`**](skills/langsmith/SKILL.md) — 用于追踪、评估和监控的 LLM 可观测性平台。当调试 LLM 应用、按数据集评估模型输出、监控生产系统或为 AI 应用构建系统化测试流水线时使用。
- [**`mlflow`**](skills/mlflow/SKILL.md) — 使用 MLflow 追踪 ML 实验、管理带版本控制的模型注册表、将模型部署到生产环境并复现实验——与框架无关的 ML 生命周期平台。
- [**`outlines`**](skills/outlines/SKILL.md) — 使用 Outlines 保证生成过程输出有效的 JSON、XML、代码结构，用 Pydantic 模型实现类型安全输出，支持本地模型并最大化推理速度——dottxt.ai 的结构化生成库。
- [**`phoenix`**](skills/phoenix/SKILL.md) — 面向 LLM 追踪、评估和监控的开源 AI 可观测性平台。当使用详细追踪调试 LLM 应用、在数据集上运行评估或实时洞察监控生产 AI 系统时使用。
- [**`swanlab`**](skills/swanlab/SKILL.md) — 提供使用 SwanLab 进行实验追踪的指导。当需要开源的运行追踪、本地或自托管仪表盘，以及面向 ML 工作流的轻量媒体日志时使用。
- [**`tensorboard`**](skills/tensorboard/SKILL.md) — 使用 TensorBoard 可视化训练指标、用直方图调试模型、比较实验、可视化模型图和性能剖析——Google 的 ML 可视化工具包。
- [**`weights-and-biases`**](skills/weights-and-biases/SKILL.md) — 使用 W&amp;B 自动记录并追踪 ML 实验、实时可视化训练、通过 sweep 优化超参数并管理模型注册表——协作式 MLOps 平台。

### 工具与CLI (35)

- [**`0-autoresearch-skill`**](skills/0-autoresearch-skill/SKILL.md) — 使用双循环架构编排端到端的自主 AI 研究项目：内循环以明确的优化目标快速迭代实验，外循环综合结果、识别模式并引导研究方向。路由到领域专属技能执行，通过 Claude Code /loop 和 OpenClaw heartbeat 支持智能体持续运行，并产出研究演示文稿和论文。当启动研究项目、运行自主实验或管理多假设研究任务时使用。
- [**`a-evolve`**](skills/a-evolve/SKILL.md) — 提供使用 LLM 驱动的进化算法在任意领域自动进化与优化 AI 智能体的指导。当构建自我改进的智能体、针对基准优化智能体提示词和技能，或实现自动化智能体评估循环时使用。
- [**`alibabacloud-find-skills`**](skills/alibabacloud-find-skills/SKILL.md) — 搜索、发现和浏览阿里云的智能体技能，按类目查找可用 skill 并了解其用途与安装方式。
- [**`audiocraft`**](skills/audiocraft/SKILL.md) — PyTorch 音频生成库，支持文生音乐（MusicGen）和文生音效（AudioGen）。当需要从文本描述生成音乐、创作音效或进行旋律条件音乐生成时使用。
- [**`blip-2`**](skills/blip-2/SKILL.md) — 连接冻结图像编码器与 LLM 的视觉-语言预训练框架。当需要图像描述、视觉问答、图文检索，或具备 SOTA 零样本性能的多模态对话时使用。
- [**`cli-anything`**](skills/cli-anything/SKILL.md) — 当用户希望 Codex 为 GUI 应用或源代码仓库构建、改进、测试、验证或列出 CLI-Anything harness 时使用。将完整的 CLI-Anything 方法论适配到 Codex，且不改变生成的 Python harness 格式。
- [**`cli-creator`**](skills/cli-creator/SKILL.md) — 基于 API 文档、OpenAPI 规范、现有 curl 示例、SDK、Web 应用、管理工具或本地脚本，为 Codex 构建可组合的 CLI。当用户希望 Codex 创建命令行工具时使用，该工具可在任意仓库中运行、提供可组合的读写命令、返回稳定 JSON、管理认证，并可搭配配套技能使用。
- [**`clip`**](skills/clip/SKILL.md) — OpenAI 的连接视觉与语言的模型。支持零样本图像分类、图文匹配和跨模态检索。基于 4 亿图文对训练。用于图像搜索、内容审核或无需微调的视觉-语言任务，最适合通用图像理解。
- [**`dramaclaw`**](skills/dramaclaw/SKILL.md) — 按照官方工作流操作、检查、配置、排障并继续 DramaClaw 项目。当用户提及 DramaClaw、NovelVideo、虾导、虾料、虾塘、虾镜、虾画、虾格、虾条、项目同步、模型或存储配置、角色、身份、肖像、场景、道具、配音、剧集、剧本、分镜草图、首帧、音频、视频、合成、项目状态、恢复与继续，或要求生成或修复 DramaClaw 作品时使用。
- [**`hatch-pet`**](skills/hatch-pet/SKILL.md) — 根据角色美术、生成图像、品牌线索或视觉参考，创建、修复、验证、视觉质检并打包兼容 Codex 的动画宠物和宠物精灵表。本技能组合已安装的 imagegen 系统技能进行视觉生成，并使用内置脚本确定性组装精灵表。
- [**`huggingface-tokenizers`**](skills/huggingface-tokenizers/SKILL.md) — 为研究与生产优化的高速 tokenizer。基于 Rust 的实现可在 20 秒内完成 1GB 文本的切分。支持 BPE、WordPiece 和 Unigram 算法。可训练自定义词表、追踪对齐、处理 padding 与截断。与 transformers 无缝集成。当需要高性能分词或自定义 tokenizer 训练时使用。
- [**`imagegen`**](skills/imagegen/SKILL.md) — 当任务受益于 AI 生成的位图视觉内容（如照片、插图、纹理、精灵图、模型稿或透明背景抠图）时，生成或编辑栅格图像。若任务更适合编辑现有 SVG、矢量或代码原生资产、扩展现有图标或标志体系，或直接在 HTML、CSS、canvas 中构建视觉，则不要使用。
- [**`image-gen-fuck`**](skills/image-gen-fuck/SKILL.md) — imagegen 的辅助工作流，用于 Codex 需要高质量图像生成但内置 image_gen 工具不可用或未暴露的场景。与 imagegen 配合使用，通过单独的临时绘图 API key 运行已安装的 image_gen.py CLI，且不改变 Codex 桌面或聊天模型的 API 配置。
- [**`karpathy-guidelines`**](skills/karpathy-guidelines/SKILL.md) — 减少常见 LLM 编码错误的行为准则。当编写、评审或重构代码时使用，以避免过度复杂化、做精准改动、显式暴露假设并定义可验证的成功标准。
- [**`lambda-labs`**](skills/lambda-labs/SKILL.md) — 用于 ML 训练和推理的预留与按需 GPU 云实例。当需要可通过简单 SSH 访问的专用 GPU 实例、持久化文件系统或用于大规模训练的高性能多节点集群时使用。
- [**`libreoffice-local-install`**](skills/libreoffice-local-install/SKILL.md) — 使用本机已安装的 LibreOffice 进行 CLI 文档转换、PDF 导出、渲染、打印和 Office 格式自动化。在记录的可执行文件可用时，不要下载或重装 LibreOffice。
- [**`local-models`**](skills/local-models/SKILL.md) — 按需操作本机托管的 CosyVoice3、bge-m3、Ollama、MusicGen 和 LM Studio 等模型服务。仅在任务真正需要本地模型时加载或启动资源。
- [**`llava`**](skills/llava/SKILL.md) — 大型语言与视觉助手（LLaVA）。支持视觉指令微调和基于图像的对话。将 CLIP 视觉编码器与 Vicuna 与 Llama 语言模型结合。支持多轮图像对话、视觉问答和指令跟随。用于视觉-语言聊天机器人或图像理解任务，最适合对话式图像分析。
- [**`ml-training-recipes`**](skills/ml-training-recipes/SKILL.md) — 覆盖所有领域的久经考验的 PyTorch 训练配方——LLM、视觉、扩散模型、医学影像、蛋白质与药物发现、空间组学、基因组学。涵盖训练循环、优化器选择、学习率调度、混合精度、调试和系统化实验。
- [**`modal`**](skills/modal/SKILL.md) — 用于运行 ML 工作负载的无服务器 GPU 云平台。当需要按需访问 GPU 而无需管理基础设施、将 ML 模型部署为 API，或运行自动扩展的批处理任务时使用。
- [**`officecli`**](skills/officecli/SKILL.md) — 使用 officecli 命令行工具创建、分析、校对和修改 Office 文档（docx、xlsx、pptx）。当用户想要创建、检查、核对格式、查找问题、添加图表或修改 Office 文档时使用。
- [**`playwright`**](skills/playwright/SKILL.md) — 当任务需要通过 playwright-cli 或内置包装脚本从终端自动化真实浏览器（导航、表单填写、快照、截图、数据提取、UI 流程调试）时使用。
- [**`pytorch-fsdp2`**](skills/pytorch-fsdp2/SKILL.md) — 为训练脚本添加 PyTorch FSDP2（fully_shard），包含正确的初始化、分片、混合精度与卸载配置和分布式 checkpoint。当模型超出单卡显存，或需要基于 DTensor 配合 DeviceMesh 分片时使用。
- [**`pytorch-lightning`**](skills/pytorch-lightning/SKILL.md) — 高层 PyTorch 框架，提供 Trainer 类、自动分布式训练（DDP、FSDP、DeepSpeed）、回调系统和极简样板代码。同一份代码可从笔记本扩展到超级计算机。当想要内置最佳实践的简洁训练循环时使用。
- [**`ray-train`**](skills/ray-train/SKILL.md) — 跨集群的分布式训练编排。可将 PyTorch、TensorFlow、HuggingFace 从笔记本扩展到数千节点。内置基于 Ray Tune 的超参数调优、容错和弹性扩展。当跨多台机器训练超大规模模型或运行分布式超参数搜索时使用。
- [**`saelens`**](skills/saelens/SKILL.md) — 提供使用 SAELens 训练和分析稀疏自编码器（SAE）的指导，将神经网络激活分解为可解释的特征。当发现可解释特征、分析叠加现象或研究语言模型中的单语义表征时使用。
- [**`segment-anything`**](skills/segment-anything/SKILL.md) — 具备零样本迁移能力的图像分割基础模型。当需要用点、框或掩码作为提示分割图像中的任意物体，或自动生成图像中所有物体的掩码时使用。
- [**`skypilot`**](skills/skypilot/SKILL.md) — 面向 ML 工作负载的多云编排，带自动成本优化。当需要跨多个云运行训练或批处理任务、利用支持自动恢复的 spot 实例，或跨提供商优化 GPU 成本时使用。
- [**`stable-diffusion`**](skills/stable-diffusion/SKILL.md) — 通过 HuggingFace Diffusers 使用 Stable Diffusion 模型进行 SOTA 文生图。当从文本提示生成图像、进行图生图转换、图像修补或构建自定义扩散流水线时使用。
- [**`tensorrt-llm`**](skills/tensorrt-llm/SKILL.md) — 使用 NVIDIA TensorRT 优化 LLM 推理，实现最大吞吐量和最低延迟。用于 NVIDIA GPU（A100、H100）上的生产部署、需要比 PyTorch 快 10-100 倍的推理，或以量化、动态批处理和多 GPU 扩展方式服务模型时使用。
- [**`visiomaster`**](skills/visiomaster/SKILL.md) — 面向 Windows 优先的 Visio 图表重建工作流，用于流程图、架构图和论文风格模块图。通过 scene.json 到 Visio 的流水线输出可编辑的 Visio vsdx 以及导出的 svg 和 png。当用户希望把图表重建为可编辑的 Visio 形状时使用。
- [**`whisper`**](skills/whisper/SKILL.md) — OpenAI 的通用语音识别模型。支持 99 种语言、转写、翻译成英语和语种识别。提供从 tiny 到 large 的六种尺寸。用于语音转文字、播客转写或多语言音频处理，最适合稳健的多语言 ASR。
- [**`windows-deployment-cli-locations`**](skills/windows-deployment-cli-locations/SKILL.md) — 定位并调用此 Windows 工作站上已安装的部署与数据库工具，尤其是 Supabase CLI、Netlify CLI、Neon CLI、Vercel CLI、Cloudflare Wrangler、Railway CLI、PostgreSQL 和 Docker 检查。当任务需要这些命令之一、命令不在 PATH 中、需要检查工具是否已安装或在安装另一个副本之前使用。
- [**`windows-ios-cicd`**](skills/windows-ios-cicd/SKILL.md) — 在没有本机 Mac/Xcode 的 Windows 上，通过 XcodeGen、Swift Package、GitHub Actions macOS CI 和 XCUITest 完成 iOS/watchOS 的构建、测试、截图验证与分发。
- [**`winui-app`**](skills/winui-app/SKILL.md) — 使用 C# 和 Windows App SDK 引导、开发和设计现代 WinUI 3 桌面应用，参考微软官方指南、WinUI Gallery 模式、Windows App SDK 示例和 CommunityToolkit 组件。当创建全新应用、为 WinUI 准备机器、评审、重构、规划、排障、环境检查，或配置 WinUI 3 的 XAML、控件、导航、窗口、主题、无障碍、响应式、性能、部署及相关 Windows 应用设计与开发工作时使用。

## 🔔 更新监控 · Update Monitoring

[![Check skill updates](https://github.com/Jensen-Yao/agents-skills/actions/workflows/check-skill-updates.yml/badge.svg)](https://github.com/Jensen-Yao/agents-skills/actions/workflows/check-skill-updates.yml)

GitHub Actions 每日检查 `skills/` 与 README、Pages 索引是否一致，并比较配置的公开上游仓库。发现遗漏或上游内容变化时，会在本仓库创建或更新唯一的 `skill-update` Issue；Pages 首页会读取该 Issue 并显示提醒。检查恢复干净后，Issue 会自动关闭。*The scheduled check compares the installed skills with both catalogs and configured public upstreams. When changes are found it maintains one `skill-update` issue, which is surfaced on Pages and closed automatically once current.*

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
