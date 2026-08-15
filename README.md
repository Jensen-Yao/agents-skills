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

共 **140** 个技能 · *140 skills in total*（说明为触发条件，英文 · descriptions are English trigger conditions）：

| 技能 · Skill | 说明 · Description |
|---|---|
| `0-autoresearch-skill` | Orchestrates end-to-end autonomous AI research projects using a two-loop architecture. The inner loop runs rapid experiment iterations with clear optimization targets. The outer loop synthesizes results, identifies patterns, and steers research direction. Routes to domain-specific skills for execution, supports continuous agent operation via Claude Code /loop and OpenClaw heartbeat, and produces research presentations and papers. Use when starting a research project, running autonomous experiments, or managing a multi-hypothesis research effort. |
| `academic-plotting` | Generates publication-quality figures for ML papers from research context. Given a paper section or description, extracts system components and relationships to generate architecture diagrams via Gemini. Given experiment results or data, auto-selects chart type and generates data-driven figures via matplotlib/seaborn. Use when creating any figure for a conference paper. |
| `accelerate` | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic device placement, mixed precision (FP16/BF16/FP8). Interactive config, single launch command. HuggingFace ecosystem standard. |
| `a-evolve` | Provides guidance for automatically evolving and optimizing AI agents across any domain using LLM-driven evolution algorithms. Use when building self-improving agents, optimizing agent prompts and skills against benchmarks, or implementing automated agent evaluation loops. |
| `alibabacloud-find-skills` | > |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). Use when the user asks "what's it called when…", or describes a motion effect without knowing its name and wants the right word to prompt an AI or designer with. For naming an effect, not designing or building one. |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and depth, typography (optical sizing, tracking, leading), reduced-motion, or the design foundations (feedback, spatial consistency, restraint) behind Apple-style interfaces. |
| `app-shell-ui` | > |
| `audiocraft` | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text descriptions, create sound effects, or perform melody-conditioned music generation. |
| `autogpt` | Autonomous AI agent platform for building and deploying continuous agents. Use when creating visual workflow agents, deploying persistent autonomous agents, or building complex multi-step AI automation systems. |
| `awq` | Activation-aware weight quantization for 4-bit LLM compression with 3x speedup and minimal accuracy loss. Use when deploying large models (7B-70B) on limited GPU memory, when you need faster inference than GPTQ with better accuracy preservation, or for instruction-tuned and multimodal models. MLSys 2024 Best Paper Award winner. |
| `axolotl` | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support |
| `bigcode-evaluation-harness` | Evaluates code generation models across HumanEval, MBPP, MultiPL-E, and 15+ benchmarks with pass@k metrics. Use when benchmarking code models, comparing coding abilities, testing multi-language support, or measuring code generation quality. Industry standard from BigCode Project used by HuggingFace leaderboards. |
| `bitsandbytes` | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memory is limited, need to fit larger models, or want faster inference. Supports INT8, NF4, FP4 formats, QLoRA training, and 8-bit optimizers. Works with HuggingFace Transformers. |
| `blip-2` | Vision-language pre-training framework bridging frozen image encoders and LLMs. Use when you need image captioning, visual question answering, image-text retrieval, or multimodal chat with state-of-the-art zero-shot performance. |
| `brainstorming-research-ideas` | Guides researchers through structured ideation frameworks to discover high-impact research directions. Use when exploring new problem spaces, pivoting between projects, or seeking novel angles on existing work. |
| `bugbounty-workflow` | 授权范围内(补天/SRC 等赏金平台)漏洞挖掘全流程工作流:侦察→挖掘→验证→报告。当用户要求"挖洞""挖漏洞""测目标""渗透测试""打点""提交SRC/补天"时使用。 |
| `chinese-plot-labels` | Use when Codex writes or modifies Python, Java, or C++ code that generates charts, plots, figures, or saved image outputs. If the user has not explicitly specified another language, require Chinese titles, axis labels, and legends in generated result images. |
| `chroma` | Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-function API. Scales from notebooks to production clusters. Use for semantic search, RAG applications, or document retrieval. Best for local development and open-source projects. |
| `cli-anything` | Use when the user wants Codex to build, refine, test, validate, or list CLI-Anything harnesses for GUI applications or source repositories. Adapts the full CLI-Anything methodology to Codex without changing the generated Python harness format. |
| `cli-creator` | Build a composable CLI for Codex from API docs, an OpenAPI spec, existing curl examples, an SDK, a web app, an admin tool, or a local script. Use when the user wants Codex to create a command-line tool that can run from any repo, expose composable read/write commands, return stable JSON, manage auth, and pair with a companion skill. |
| `clip` | OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding. |
| `cnki-advanced-search` | Perform advanced search on CNKI with field filters like author, title, journal, date range, source category (SCI/EI/CSSCI/北大核心). Use when user needs precise filtered search beyond simple keywords. |
| `cnki-download` | Download a paper PDF/CAJ from CNKI. Requires user to be logged in. Use when user wants to download a specific paper. |
| `cnki-export` | Export paper from CNKI and push to Zotero, or save as RIS file. Use when user wants to save a paper to Zotero or export citation data. |
| `cnki-journal-index` | Query journal indexing/inclusion status on CNKI - check which databases include a journal (北大核心, CSSCI, CSCD, SCI, EI, etc.), get impact factors and evaluation data. Use when user asks about a journal's level, indexing, or ranking. |
| `cnki-journal-search` | Search for journals/publications on CNKI by name, ISSN, CN, or sponsor. Use when the user wants to find a specific journal or browse publications. |
| `cnki-journal-toc` | Browse journal issues, view table of contents, and download original TOC PDF from CNKI. Use when user wants to see papers in a specific journal issue or download the original cover/TOC pages. |
| `cnki-navigate-pages` | Navigate CNKI search result pages (next/previous/specific page) or change sort order. Use when user wants to see more results or change sorting. |
| `cnki-paper-detail` | Extract full paper details from a CNKI paper page including title, authors, affiliations, abstract, keywords, fund, classification. Use when the user needs detailed information about a specific paper. |
| `cnki-parse-results` | Parse current CNKI search results page into structured paper data (title, authors, journal, date, citations). Use after a search has been performed and you need to extract the results. |
| `cnki-researcher` | Coordinate CNKI research workflows in Codex using Chrome DevTools MCP. Use when the user asks to search CNKI papers, inspect paper details, browse journals or issues, check journal indexing, download CNKI files, export citations, handle institution/off-campus CNKI login, or combine these tasks into a literature research workflow. |
| `cnki-search` | Search CNKI (中国知网) for papers by keyword. Use when the user wants to find academic papers on a topic. |
| `constitutional-ai` | Anthropic's method for training harmless AI through self-improvement. Two-phase approach - supervised learning with self-critique/revision, then RLAIF (RL from AI Feedback). Use for safety alignment, reducing harmful outputs without human labels. Powers Claude's safety system. |
| `cosmos-policy` | Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments. Use when setting up cosmos-policy for robot manipulation evaluation, running headless GPU evaluations with EGL rendering, or profiling inference latency on cluster or local GPU machines. |
| `creative-thinking-for-research` | Applies cognitive science frameworks for creative thinking to CS and AI research ideation. Use when seeking genuinely novel research directions by leveraging combinatorial creativity, analogical reasoning, constraint manipulation, and other empirically grounded creative strategies. |
| `crewai` | Multi-agent orchestration framework for autonomous AI collaboration. Use when building teams of specialized agents working together on complex tasks, when you need role-based agent collaboration with memory, or for production workflows requiring sequential/hierarchical execution. Built without LangChain dependencies for lean, fast execution. |
| `deepspeed` | Expert guidance for distributed training with DeepSpeed - ZeRO optimization stages, pipeline parallelism, FP16/BF16/FP8, 1-bit Adam, sparse attention |
| `dramaclaw` | "Operate, inspect, configure, troubleshoot, and continue DramaClaw projects according to the official workflow. Use whenever the user mentions DramaClaw, NovelVideo, 虾导, 虾料, 虾塘, 虾镜, 虾画, 虾格, 虾条, CLI/API/Web project synchronization, model or storage configuration, characters, identities, portraits, scenes, props, voices, episodes, Beats, scripts, sketches, first frames, audio, video, composition, project status, resume/continue, or asks to generate/fix a DramaClaw production. Enforces asset, image, and review gates before downstream generation." |
| `drawio-skill` | Use when the user requests diagrams, flowcharts, architecture diagrams, ER diagrams, UML / sequence / class diagrams, network topology, ML/DL model figures (Transformer/CNN/LSTM), mind maps, or any visualization. Also use proactively when explaining systems with 3+ components, complex data flows, or relationships that benefit from visual representation. Best suited when the diagram needs custom styling, rich shape vocabulary, swimlanes, or exportable images (PNG/SVG/PDF/JPG). Generates .drawio XML and exports locally via the native draw.io desktop CLI. |
| `dspy` | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming |
| `emil-design-eng` | This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| `faiss` | Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index types (Flat, IVF, HNSW). Use for fast k-NN search, large-scale vector retrieval, or when you need pure similarity search without metadata. Best for high-performance applications. |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it does not implement it. Use when the user asks "what could be animated here?" or wants to "make this feel more alive". For fixing existing animations, use improve-animations or review-animations instead. |
| `flash-attention` | Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long sequences (>512 tokens), encountering GPU memory issues with attention, or need faster inference. Supports PyTorch native SDPA, flash-attn library, H100 FP8, and sliding window attention. |
| `gguf` | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements. |
| `gptq` | Post-training 4-bit quantization for LLMs with minimal accuracy loss. Use for deploying large models (70B, 405B) on consumer GPUs, when you need 4× memory reduction with <2% perplexity degradation, or for faster inference (3-4× speedup) vs FP16. Integrates with transformers and PEFT for QLoRA fine-tuning. |
| `grpo-rl-training` | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training |
| `guidance` | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework |
| `hatch-pet` | Create, repair, validate, visually QA, and package Codex-compatible animated pets and pet spritesheets from character art, generated images, company or prospect brand cues, or visual references. Use when a user wants a lightweight-worker Codex pet workflow, a non-pixel custom pet style, a prospect or company mascot pet, or a full 8x9 animated pet atlas with transparent unused cells, QA contact sheets, and pet.json packaging. This skill composes the installed $imagegen system skill for visual generation and uses bundled scripts for deterministic spritesheet assembly. |
| `hqq` | Half-Quadratic Quantization for LLMs without calibration data. Use when quantizing models to 4/3/2-bit precision without needing calibration datasets, for fast quantization workflows, or when deploying with vLLM or HuggingFace Transformers. |
| `huggingface-tokenizers` | Fast tokenizers optimized for research and production. Rust-based implementation tokenizes 1GB in <20 seconds. Supports BPE, WordPiece, and Unigram algorithms. Train custom vocabularies, track alignments, handle padding/truncation. Integrates seamlessly with transformers. Use when you need high-performance tokenization or custom tokenizer training. |
| `imagegen` | "Generate or edit raster images when the task benefits from AI-created bitmap visuals such as photos, illustrations, textures, sprites, mockups, or transparent-background cutouts. Use when Codex should create a brand-new image, transform an existing image, or derive visual variants from references, and the output should be a bitmap asset rather than repo-native code or vector. Do not use when the task is better handled by editing existing SVG/vector/code-native assets, extending an established icon or logo system, or building the visual directly in HTML/CSS/canvas." |
| `image-gen-fuck` | Auxiliary workflow for $imagegen when Codex needs high-quality image generation but the built-in image_gen tool is unavailable or not exposed. Use this with $imagegen to run the installed image_gen.py CLI through a separate temporary drawing API key, preferably configured in Codex++ cliWrapper settings, defaulting to OPENAI_BASE_URL=https://code.codingplay.top/v1, without changing the Codex desktop/chat model API configuration. |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not apply them. Use when the user asks to "improve the animations", "audit the motion", "make this app feel better", or wants a roadmap of animation fixes rather than a review of a single diff. |
| `instructor` | Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and stream partial results with Instructor - battle-tested structured output library |
| `karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. |
| `knowledge-distillation` | Compress large language models using knowledge distillation from teacher to student models. Use when deploying smaller models with retained performance, transferring GPT-4 capabilities to open-source models, or reducing inference costs. Covers temperature scaling, soft targets, reverse KLD, logit distillation, and MiniLLM training strategies. |
| `lambda-labs` | Reserved and on-demand GPU cloud instances for ML training and inference. Use when you need dedicated GPU instances with simple SSH access, persistent filesystems, or high-performance multi-node clusters for large-scale training. |
| `langchain` | Framework for building LLM-powered applications with agents, chains, and RAG. Supports multiple providers (OpenAI, Anthropic, Google), 500+ integrations, ReAct agents, tool calling, memory management, and vector store retrieval. Use for building chatbots, question-answering systems, autonomous agents, or RAG applications. Best for rapid prototyping and production deployments. |
| `langsmith` | LLM observability platform for tracing, evaluation, and monitoring. Use when debugging LLM applications, evaluating model outputs against datasets, monitoring production systems, or building systematic testing pipelines for AI applications. |
| `libreoffice-local-install` | Use the existing local LibreOffice installation for CLI document conversion, PDF export, rendering, printing, and Office-format automation on this Windows machine. Trigger when a task mentions LibreOffice, soffice, headless document conversion, DOCX/XLSX/PPTX/ODF conversion, or needs the local LibreOffice executable path. Do not download or reinstall LibreOffice while the recorded executable works. |
| `litgpt` | Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama, Gemma, Phi, Qwen, Mistral). Use when need clean model implementations, educational understanding of architectures, or production fine-tuning with LoRA/QLoRA. Single-file implementations, no abstraction layers. |
| `llama-cpp` | Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when CUDA is unavailable. Supports GGUF quantization (1.5-8 bit) for reduced memory and 4-10× speedup vs PyTorch on CPU. |
| `llama-factory` | Expert guidance for fine-tuning LLMs with LLaMA-Factory - WebUI no-code, 100+ models, 2/3/4/5/6/8-bit QLoRA, multimodal support |
| `llamaguard` | Meta's 7-8B specialized moderation model for LLM input/output filtering. 6 safety categories - violence/hate, sexual content, weapons, substances, self-harm, criminal planning. 94-95% accuracy. Deploy with vLLM, HuggingFace, Sagemaker. Integrates with NeMo Guardrails. |
| `llamaindex` | Data framework for building LLM applications with RAG. Specializes in document ingestion (300+ connectors), indexing, and querying. Features vector indices, query engines, agents, and multi-modal support. Use for document Q&A, chatbots, knowledge retrieval, or building RAG pipelines. Best for data-centric LLM applications. |
| `llava` | Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA language models. Supports multi-turn image chat, visual question answering, and instruction following. Use for vision-language chatbots or image understanding tasks. Best for conversational image analysis. |
| `lm-evaluation-harness` | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs. |
| `long-context` | Extend context windows of transformer models using RoPE, YaRN, ALiBi, and position interpolation techniques. Use when processing long documents (32k-128k+ tokens), extending pre-trained models beyond original context limits, or implementing efficient positional encodings. Covers rotary embeddings, attention biases, interpolation methods, and extrapolation strategies for LLMs. |
| `mamba` | State-space model with O(n) complexity vs Transformers' O(n²). 5× faster inference, million-token sequences, no KV cache. Selective SSM with hardware-aware design. Mamba-1 (d_state=16) and Mamba-2 (d_state=128, multi-head). Models 130M-2.8B on HuggingFace. |
| `megatron-core` | Trains large language models (2B-462B parameters) using NVIDIA Megatron-Core with advanced parallelism strategies. Use when training models >1B parameters, need maximum GPU efficiency (47% MFU on H100), or require tensor/pipeline/sequence/context/expert parallelism. Production-ready framework used for Nemotron, LLaMA, DeepSeek. |
| `miles` | Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime. Use when training large MoE models with FP8/INT4, needing train-inference alignment, or requiring speculative RL for maximum throughput. |
| `mlflow` | Track ML experiments, manage model registry with versioning, deploy models to production, and reproduce experiments with MLflow - framework-agnostic ML lifecycle platform |
| `ml-paper-writing` | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, verifying citations, or preparing camera-ready submissions. For systems venues (OSDI, NSDI, ASPLOS, SOSP), use systems-paper-writing instead. |
| `ml-training-recipes` | Battle-tested PyTorch training recipes for all domains — LLMs, vision, diffusion, medical imaging, protein/drug discovery, spatial omics, genomics. Covers training loops, optimizer selection (AdamW, Muon), LR scheduling, mixed precision, debugging, and systematic experimentation. Use when training or fine-tuning neural networks, debugging loss spikes or OOM, choosing architectures, or optimizing GPU throughput. |
| `modal` | Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling. |
| `model-merging` | Merge multiple fine-tuned models using mergekit to combine capabilities without retraining. Use when creating specialized models by blending domain-specific expertise (math + coding + chat), improving performance beyond single models, or experimenting rapidly with model variants. Covers SLERP, TIES-Merging, DARE, Task Arithmetic, linear merging, and production deployment strategies. |
| `model-pruning` | Reduce LLM size and accelerate inference using pruning techniques like Wanda and SparseGPT. Use when compressing models without retraining, achieving 50% sparsity with minimal accuracy loss, or enabling faster inference on hardware accelerators. Covers unstructured pruning, structured pruning, N:M sparsity, magnitude pruning, and one-shot methods. |
| `moe-training` | Train Mixture of Experts (MoE) models using DeepSpeed or HuggingFace. Use when training large-scale models with limited compute (5× cost reduction vs dense models), implementing sparse architectures like Mixtral 8x7B or DeepSeek-V3, or scaling model capacity without proportional compute increase. Covers MoE architectures, routing mechanisms, load balancing, expert parallelism, and inference optimization. |
| `nanogpt` | Educational GPT implementation in ~300 lines. Reproduces GPT-2 (124M) on OpenWebText. Clean, hackable code for learning transformers. By Andrej Karpathy. Perfect for understanding GPT architecture from scratch. Train on Shakespeare (CPU) or OpenWebText (multi-GPU). |
| `nemo-curator` | GPU-accelerated data curation for LLM training. Supports text/image/video/audio. Features fuzzy deduplication (16× faster), quality filtering (30+ heuristics), semantic deduplication, PII redaction, NSFW detection. Scales across GPUs with RAPIDS. Use for preparing high-quality training datasets, cleaning web data, or deduplicating large corpora. |
| `nemo-evaluator` | Evaluates LLMs across 100+ benchmarks from 18+ harnesses (MMLU, HumanEval, GSM8K, safety, VLM) with multi-backend execution. Use when needing scalable evaluation on local Docker, Slurm HPC, or cloud platforms. NVIDIA's enterprise-grade platform with container-first architecture for reproducible benchmarking. |
| `nemo-guardrails` | NVIDIA's runtime safety framework for LLM applications. Features jailbreak detection, input/output validation, fact-checking, hallucination detection, PII filtering, toxicity detection. Uses Colang 2.0 DSL for programmable rails. Production-ready, runs on T4 GPU. |
| `nnsight` | Provides guidance for interpreting and manipulating neural network internals using nnsight with optional NDIF remote execution. Use when needing to run interpretability experiments on massive models (70B+) without local GPU resources, or when working with any PyTorch architecture. |
| `officecli` | Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents. |
| `openpi` | Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast, pi0.5) using JAX or PyTorch backends for robot policy inference across ALOHA, DROID, and LIBERO environments. Use when adapting pi0 models to custom datasets, converting JAX checkpoints to PyTorch, running policy inference servers, or debugging norm stats and GPU memory issues. |
| `openrlhf` | High-performance RLHF framework with Ray+vLLM acceleration. Use for PPO, GRPO, RLOO, DPO training of large models (7B-70B+). Built on Ray, vLLM, ZeRO-3. 2× faster than DeepSpeedChat with distributed architecture and GPU resource sharing. |
| `openvla-oft` | Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot action generation with continuous action heads, LoRA adaptation, and FiLM conditioning on LIBERO simulation and ALOHA real-world setups. Use when reproducing OpenVLA-OFT paper results, training custom VLA action heads (L1 or diffusion), deploying server-client inference for ALOHA, or debugging normalization, LoRA merge, and cross-GPU issues. |
| `outlines` | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library |
| `peft` | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem. |
| `phoenix` | Open-source AI observability platform for LLM tracing, evaluation, and monitoring. Use when debugging LLM applications with detailed traces, running evaluations on datasets, or monitoring production AI systems with real-time insights. |
| `pick-ui-library` | Pick the right library for a given frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. Only runs when explicitly invoked; it does not trigger on its own. |
| `pinecone` | Managed vector database for production AI applications. Fully managed, auto-scaling, with hybrid search (dense + sparse), metadata filtering, and namespaces. Low latency (<100ms p95). Use for production RAG, recommendation systems, or semantic search at scale. Best for serverless, managed infrastructure. |
| `playwright` | "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script." |
| `presenting-conference-talks` | Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script. Use when preparing oral talks, spotlight presentations, or invited talks for ML and systems conferences. |
| `prompt-guard` | Meta's 86M prompt injection and jailbreak detector. Filters malicious prompts and third-party data for LLM apps. 99%+ TPR, <1% FPR. Fast (<2ms GPU). Multilingual (8 languages). Deploy with HuggingFace or batch processing for RAG security. |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one that feels right. Only runs when explicitly invoked; it does not trigger on its own. |
| `pytorch-fsdp2` | Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpointing. Use when models exceed single-GPU memory or when you need DTensor-based sharding with DeviceMesh. |
| `pytorch-lightning` | High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerplate. Scales from laptop to supercomputer with same code. Use when you want clean training loops with built-in best practices. |
| `pyvene` | Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative intervention framework. Use when conducting causal tracing, activation patching, interchange intervention training, or testing causal hypotheses about model behavior. |
| `qdrant` | High-performance vector similarity search engine for RAG and semantic search. Use when building production RAG systems requiring fast nearest neighbor search, hybrid search with filtering, or scalable vector storage with Rust-powered performance. |
| `ray-data` | Scalable data processing for ML workloads. Streaming execution across CPU/GPU, supports Parquet/CSV/JSON/images. Integrates with Ray Train, PyTorch, TensorFlow. Scales from single machine to 100s of nodes. Use for batch inference, data preprocessing, multi-modal data loading, or distributed ETL pipelines. |
| `ray-train` | Distributed training orchestration across clusters. Scales PyTorch/TensorFlow/HuggingFace from laptop to 1000s of nodes. Built-in hyperparameter tuning with Ray Tune, fault tolerance, elastic scaling. Use when training massive models across multiple machines or running distributed hyperparameter sweeps. |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned. |
| `rwkv` | RNN+Transformer hybrid with O(n) inference. Linear time, infinite context, no KV cache. Train like GPT (parallel), infer like RNN (sequential). Linux Foundation AI project. Production at Windows, Office, NeMo. RWKV-7 (March 2025). Models up to 14B parameters. |
| `saelens` | Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable features. Use when discovering interpretable features, analyzing superposition, or studying monosemantic representations in language models. |
| `scholar-ppt-cn` | Use this skill when a user wants to create, restyle, or rebuild a Chinese academic PowerPoint from papers, theses, reports, figures, notes, reference templates, screenshots, or visual mockups. The workflow keeps the user interface simple while restoring useful planning. First create a production planning table that maps each slide to narrative section, source asset, source-asset geometry, core message, and detailed layout archetype. Then create a mockup family + variants blueprint that groups planned slides into reusable visual families and assigns concrete variants. Visual samples and editable PPTX are generated only after this family blueprint is established. Template DNA controls visual identity; layout archetypes and mockup family variants control page structure; approved mockups override fallback layouts. |
| `sci-extract` | Read an academic paper end to end and extract professional research insights, figures, metadata, and critique. Use this skill whenever the user shares a scientific paper, review paper, survey paper, systematic review, meta-analysis, scoping review, arXiv link, DOI, PDF, or pasted paper text and asks to read, summarize, analyze, extract, digest, review, critique, or explain it. For original research papers, produce a modified Heilmeier analysis. For review literature, produce a field-map extraction covering scope, taxonomy, evidence quality, consensus, controversies, gaps, and future directions. Do NOT use this skill for non-academic articles, blog posts, or news. |
| `sci-figure` | Extracts figures and sub-figures from academic PDF papers. Supports Fig/Figure, Scheme, Chart, Supplementary Figure, Extended Data Figure (Nature), and Chinese equivalents (图/方案/示意图/附图/补充图). Sub-figure label recognition supports (a)/(A)/a)/(i)/(1)/a. formats. High-quality PNG output at configurable DPI. Use when user asks to "extract figure", "截取文献图片", "提取子图", "get figure from paper", "Scheme", "方案图", "补充图", "Supplementary Figure", or "Extended Data". |
| `sci-html` | Generate academic presentation-style HTML slide decks and browser reports from PDFs, structured text, Markdown, paper summaries, outlines, or research notes. Use whenever the user wants to convert a scientific paper PDF directly into an interactive HTML report, clickable web presentation, shareable browser deck, or PPT-like HTML output with figures, structured insights, section pages, and offline deck-directory output. In the Aut_Sci_Write suite, choose this skill when the user wants HTML/web output; choose sci-ppt when they explicitly need a .pptx file. |
| `sci-ppt` | Generate professional academic PowerPoint (PPTX) presentations from paper PDFs, structured outlines, or plain text. Use for thesis defense, seminar reports, literature presentations, and graduate school applications. Supports automatic figure extraction, LaTeX formula rendering, and bilingual (Chinese/English) layouts. |
| `sci-review` | Specialized workflows for drafting, refining, and responding to academic literature reviews and peer review feedback. Use this skill for literature review outlines, research-gap synthesis, reviewer rebuttals, response letters, and academic writing tone repair. |
| `sci-search` | Academic paper search and metrics analysis. Searches arXiv, PubMed, and Web of Science simultaneously with journal impact factor data. Triggers on requests to search for papers or find literature. |
| `sci-zotero` | Interact with your Zotero library to sync references, add citations by DOI/ISBN/PMID, and manage PDFs. Triggers on Zotero-related requests. |
| `segment-anything` | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image. |
| `sentencepiece` | Language-independent tokenizer treating text as raw Unicode. Supports BPE and Unigram algorithms. Fast (50k sentences/sec), lightweight (6MB memory), deterministic vocabulary. Used by T5, ALBERT, XLNet, mBART. Train on raw text without pre-tokenization. Use when you need multilingual support, CJK languages, or reproducible tokenization. |
| `sentence-transformers` | Framework for state-of-the-art sentence, text, and image embeddings. Provides 5000+ pre-trained models for semantic similarity, clustering, and retrieval. Supports multilingual, domain-specific, and multimodal models. Use for generating embeddings for RAG, semantic search, or similarity tasks. Best for production embedding generation. |
| `sglang` | Fast structured generation and serving for LLMs with RadixAttention prefix caching. Use for JSON/regex outputs, constrained decoding, agentic workflows with tool calls, or when you need 5× faster inference than vLLM with prefix sharing. Powers 300,000+ GPUs at xAI, AMD, NVIDIA, and LinkedIn. |
| `simpo` | Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No reference model needed, more efficient than DPO. Use for preference alignment when want simpler, faster training than DPO/PPO. |
| `skypilot` | Multi-cloud orchestration for ML workloads with automatic cost optimization. Use when you need to run training or batch jobs across multiple clouds, leverage spot instances with auto-recovery, or optimize GPU costs across providers. |
| `slime` | Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. Use when training GLM models, implementing custom data generation workflows, or needing tight Megatron-LM integration for RL scaling. |
| `speculative-decoding` | Accelerate LLM inference using speculative decoding, Medusa multiple heads, and lookahead decoding techniques. Use when optimizing inference speed (1.5-3.6× speedup), reducing latency for real-time applications, or deploying models with limited compute. Covers draft models, tree-based attention, Jacobi iteration, parallel token generation, and production deployment strategies. |
| `stable-diffusion` | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines. |
| `swanlab` | Provides guidance for experiment tracking with SwanLab. Use when you need open-source run tracking, local or self-hosted dashboards, and lightweight media logging for ML workflows. |
| `systems-paper-writing` | Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys. Provides paragraph-level structural blueprints, writing patterns, venue-specific checklists, reviewer guidelines, LaTeX templates, and conference deadlines. Use this skill for all systems conference paper writing. |
| `tensorboard` | Visualize training metrics, debug models with histograms, compare experiments, visualize model graphs, and profile performance with TensorBoard - Google's ML visualization toolkit |
| `tensorrt-llm` | Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when you need 10-100x faster inference than PyTorch, or for serving models with quantization (FP8/INT4), in-flight batching, and multi-GPU scaling. |
| `torchforge` | Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra from algorithms. Use when you want clean RL abstractions, easy algorithm experimentation, or scalable training with Monarch and TorchTitan. |
| `torchtitan` | Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP). Use when pretraining Llama 3.1, DeepSeek V3, or custom models at scale from 8 to 512+ GPUs with Float8, torch.compile, and distributed checkpointing. |
| `transformer-lens` | Provides guidance for mechanistic interpretability research using TransformerLens to inspect and manipulate transformer internals via HookPoints and activation caching. Use when reverse-engineering model algorithms, studying attention patterns, or performing activation patching experiments. |
| `trl-fine-tuning` | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers. |
| `unsloth` | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization |
| `verl` | Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL). Use when implementing RLHF, GRPO, PPO, or other RL algorithms for LLM post-training at scale with flexible infrastructure backends. |
| `visiomaster` | Windows-first Visio diagram reconstruction workflow for flowcharts, architecture diagrams, and paper-style module figures. Reuses ppt-master style analysis and composition discipline on the front half, but outputs editable Visio .vsdx plus exported .svg and .png through a scene.json to Visio pipeline. Use when the user wants a diagram recreated as editable Visio shapes instead of a pasted screenshot or PPT-only result. |
| `vllm` | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism. |
| `weights-and-biases` | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform |
| `whisper` | OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR. |
| `windows-deployment-cli-locations` | Locate and invoke the deployment and database tools installed on this Windows workstation, especially Supabase CLI, Netlify CLI, Neon CLI, Vercel CLI, Cloudflare Wrangler, Railway CLI, PostgreSQL, and Docker checks. Use when a task needs one of these commands, when a command is not on PATH, when checking whether a tool is installed, or before installing another copy. |
| `winui-app` | Bootstrap, develop, and design modern WinUI 3 desktop applications with C# and the Windows App SDK using official Microsoft guidance, WinUI Gallery patterns, Windows App SDK samples, and CommunityToolkit components. Use when creating a brand new app, preparing a machine for WinUI, reviewing, refactoring, planning, troubleshooting, environment-checking, or setting up WinUI 3 XAML, controls, navigation, windowing, theming, accessibility, responsiveness, performance, deployment, or related Windows app design and development work. |


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
