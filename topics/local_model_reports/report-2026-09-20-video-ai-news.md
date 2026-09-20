# Local Runnability: Models from AI News Video (2026-09-20)

**Compiled:** 2026-09-20\
**Source video:** [OpenAI hacked, Jev, Google’s RSI, Qwen 3.8 Omni, Bonsai 2, new Gemini Live: AI NEWS](https://www.youtube.com/watch?v=hygMRgnDD7w) (AI Search, 41:06)\
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**\
**Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**\
**Memory budget:** [Your real memory budget](./memory-budget.md)

## TL;DR

| Verdict | Models / items |
| --- | --- |
| **Runs well on this Mac** | **Needle 3** (about **9–29 MB**, with a native macOS ARM64 engine) for tool calls, structured extraction, and embeddings; **Laya** (**0.4B**, about **808 MB** for the English checkpoint) for small, typed text decisions |
| **Tight / experimental** | **Bonsai 2 27B** (official MLX pack is **8.6 GB**; about **8.6 GB at 4K context** in the project memory table, with no M2/16 GB benchmark); **R2T2** (2B BF16, memory-sized for the Mac, but its first-party install is CUDA/vLLM-focused); **Nimble 9B** (a small LoRA adapter that still needs a quantized 9B base) |
| **Open weights, not this machine as published** | **Meridian**, **XGEN-JING**, **Occamy 1.0**, and **ZGCM-1** in its BF16 release |
| **Hosted services / products** | Gemini 3.8 Live, Qwen 3.8 Omni Flash, Qwen 3.8 Live Translate, Runway, Jev, Astra for Law, and Odyssey 3 |
| **Research, agent, or infrastructure stories** | Dream-RSI, DAO, Z.ai’s inference system, Xiaomi’s MiMo training stream, GPT-Policy, and the Enigma and OpenAI security stories |

The useful local finds are small task-specific models and one very compressed general model. **Needle 3** targets fixed tool calls, extraction, and embeddings; **Laya** scores structured choices rather than writing chat replies. **Bonsai 2** is the week’s most interesting general local model, but its Apple MLX memory numbers leave little room for other apps at short context. R2T2 is a promising local speech model by size, with an unverified Mac runtime.

The video’s “open” items vary a lot: some have downloadable weights, some are APIs, and some are research or product announcements. In particular, **3B active parameters does not mean a 35B model has a 3B-sized checkpoint**, and published maximum context is not a practical 16 GB setting.

---

## Runnability table (all chapters)

Chapter order follows the video’s official YouTube chapters.

| Model / item | Video | Kind | Weights / access | Fits 16 GB M2? | Local reality |
| --- | --- | --- | --- | --- | --- |
| **Meridian** | [1:08](https://www.youtube.com/watch?v=hygMRgnDD7w&t=68s) | Video re-camera and retiming model | Public adapters; MiniMax-H3 base and VGGT-Omega also required | ❌ | The [model card](https://huggingface.co/Viggle/Meridian) lists a 61.7 GiB H3 base plus two 2.5 GiB adapters. Its reference run peaks at 88 GiB GPU memory on a B200, with no supported quantization or CPU offload. |
| **R2T2** | [2:39](https://www.youtube.com/watch?v=hygMRgnDD7w&t=159s) | Streaming speech recognition | Public 2B BF16 weights; code Apache 2.0, weights under NetEase’s separate model license | ⚠️ | About 4 GB of raw BF16 weights is plausible on this Mac, but the [official repo](https://github.com/netease-youdao/Confucius4-R2T2) recommends vLLM/CUDA and Docker with an NVIDIA GPU. It also mentions a Transformers backend, but gives no MPS/MLX recipe. |
| **JING / DAO** | [4:09](https://www.youtube.com/watch?v=hygMRgnDD7w&t=249s) | First-person audio/video generation plus a persistent world engine | JING weights are public under the MiniMax H3 Community License; DAO is a research preview | ❌ | [JING’s release](https://github.com/XGEN-Labs/XGEN-JING) is validated on **six H100s** and also loads MiniMax-H3 assets. The [XGEN page](https://xgenlabs.ai/research/generative-world-simulation) describes DAO’s research direction, not a small local engine. |
| **Dream-RSI** | [6:32](https://www.youtube.com/watch?v=hygMRgnDD7w&t=392s) | Research method for improving exploration policies | Paper and code; no new base-model weights | n/a | It replays recorded discovery trees to compare alternative policies without repeating those executions. The [project page](https://dream-rsi.com/) says the underlying coding agent remains unchanged; this is an agent method, not a new laptop model. |
| **Gemini 3.8 Live** | [8:36](https://www.youtube.com/watch?v=hygMRgnDD7w&t=516s) | Real-time voice and multimodal agent | Hosted Gemini API / AI Studio | ❌ | Google’s [release page](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/) lists the Gemini API, AI Studio, Search Live, and enterprise services. No downloadable weights are offered there. |
| **Qwen 3.8 Omni Flash** | [10:36](https://www.youtube.com/watch?v=hygMRgnDD7w&t=636s) | Audio, image, and video understanding with text output | Alibaba Cloud Model Studio API | ❌ | The official [Model Studio page](https://help.aliyun.com/en/model-studio/qwen3-8-omni-flash) names Alibaba Cloud as the inference provider and requires its API service. This named Omni-Flash endpoint is not the separate Qwen3.8 open-weight release. |
| **Qwen 3.8 Live Translate** | [12:26](https://www.youtube.com/watch?v=hygMRgnDD7w&t=746s) | Real-time speech translation and synthesized interpretation | DashScope real-time API | ❌ | The [Qwen release](https://qwen.ai/blog?id=qwen3.8-livetranslate) shows a WebSocket client using an API key and workspace ID. The client can run on a Mac; model inference remains remote. |
| **Runway** (sponsor) | [14:00](https://www.youtube.com/watch?v=hygMRgnDD7w&t=840s) | Hosted creative suite | Cloud product | ❌ | The chapter promotes a hosted image/video generation workflow; it does not introduce local weights. |
| **Needle 3** | [15:27](https://www.youtube.com/watch?v=hygMRgnDD7w&t=927s) | Tiny on-device tool selection, structured extraction, and embeddings | Cactus runtime and model files; public page does not specify a model-weight license | ✅ | The [Cactus release](https://www.cactuscompute.com/needle) describes 9–29 MB CQ2 subnetworks and a prebuilt **macOS ARM64** engine. It is designed for constrained structured tasks and offline execution, not open-ended chat. |
| **Z.ai inference infrastructure** | [17:07](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1027s) | Production serving / infrastructure agent report | No new local model package | n/a | The [Z.ai write-up](https://z.ai/blog/glm-built-its-inference-infrastructure) describes GLM-5.3-Flash inference on a cluster of over 100,000 accelerators. It is systems engineering at datacenter scale. |
| **Xiaomi MiMo real-time RL** | [19:56](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1196s) | Public view of a model training process | Training stream; no local checkpoint linked | n/a | The [MiMo RL page](https://mimo.xiaomi.com/rl/) is about reinforcement-learning progress for an upcoming model. A training stream does not provide a laptop inference package. |
| **GPT-Policy** | [21:27](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1287s) | Framework for robotic in-context learning | Research code; experiments use hosted GPT-6 Astra plus robot/control hardware | ❌ as a complete local setup | The [project report](https://cheng-haha.github.io/GPT-Policy/) evaluates a VLM connected to constrained robot tools on real robots. It reports 10 tasks with three trials per condition and calls out physical-safety and execution limits; the robot stack and VLM are not a local M2 package. |
| **Enigma case study** | [23:06](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1386s) | Historical cryptanalysis result, attributed in the video to GPT-6 Astra | No model release | n/a | The [case page](https://mvueh-enigma-solved.carterl.chatgpt.site/) documents a two-day recovery of one 1941 message using source copies, a guessed phrase, and modern computation. It is a case study, not a local model release. |
| **Jev** | [24:57](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1497s) | Typed System One decision model | Closed early-access service | ❌ | TypeSafe describes [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) as returning structured decisions and probabilities rather than strings. That constrained output design is different from a local general-purpose chat model; weights are not published. |
| **Laya** | [28:38](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1718s) | Text-only structured decision model | Apache 2.0 weights | ✅ | The [Hugging Face card](https://huggingface.co/convaiinnovations/laya) lists a 0.4B model and a Transformers path. Its English checkpoint handles up to 512 tokens per question; the card recommends validating calibration on your own data. |
| **Bespoke Nimble 9B** | [29:56](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1796s) | LoRA for scoring choices, booleans, and rubric levels | Apache 2.0 adapter; requires Qwen3.5-9B base | ⚠️ | The [adapter is about 165 MiB](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B), but it is not a standalone 9B model. The published example uses Transformers and PEFT; using it on this Mac means sourcing and quantizing the base and validating adapter support in the chosen Apple runtime. |
| **Astra for Law** | [31:00](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1860s) | Hosted legal workflow and search product | OpenAI product; no local weights | ❌ | The [OpenAI announcement](https://openai.com/index/astra-for-law/) describes a legal workflow built around hosted GPT-6 Astra and legal search. |
| **OpenAI security story** | [31:58](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1918s) | Hacktron security research | No model release | n/a | [Hacktron’s post](https://www.hacktron.ai/blog/hacking-openai) is a security report, not a model or local inference release. |
| **MiniMax Code CLI** | [34:20](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2060s) | Open-source terminal coding harness | Code is public; default inference is a provider | ⚠️ harness only | The [CLI](https://github.com/MiniMax-AI/minimax-code) runs as a local tool and supports a custom provider URL. A local M2 setup depends on pointing it at a compatible local inference server; the harness itself does not include a new base model. |
| **Bonsai 2 27B** | [35:24](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2124s) | Compressed general model based on Qwen3.8 27B | Apache 2.0; official MLX and GGUF artifacts | ⚠️ 4K-context experiment | The [release](https://prismml.com/news/bonsai-2-27b) reports a 5.9 GB ternary representation and Apple MLX support. The actual [MLX checkpoint](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit) is an 8.6 GB pack including the vision tower. Its memory table is about **8.6 GB at 4K**, **8.9 GB at 10K**, and **14.4 GB at 100K**; the published Mac speed run used an M5 Pro, not this M2. |
| **Occamy 1.0** | [37:03](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2223s) | Vision-capable agentic MoE | Public 35B weights; Q4_K_M, Q8, and community MLX formats | ❌ | The [model card](https://huggingface.co/Accio-Lab/occamy-1.0) specifies **35B total / 3B active**. Even the ideal 4-bit lower bound for 35B weights is 17.5 GB before scales, KV cache, or macOS; sparse activation reduces compute, not stored checkpoint size. |
| **ZGCM-1** | [37:59](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2279s) | Dense math-reasoning and agent-search model | MIT weights; published checkpoint is BF16 | ⚠️ only after quantization | The [model card](https://huggingface.co/zgcagi/ZGCM-1-7B) lists 7.39B parameters and 256K context. BF16 weights alone are roughly **14.8 GB** by parameter count, leaving no practical M2 headroom; a community Q4 conversion would be an experiment, and no first-party Mac package is listed. |
| **Odyssey 3** | [38:45](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2325s) | Physical-intelligence world model for robots, cars, drones, and agents | Odyssey API access | ❌ | The [announcement](https://odyssey.systems/introducing-odyssey-3) points to API access. It does not provide a downloadable local checkpoint, and its target use depends on physical systems. |

**Legend:** ✅ comfortable local use · ⚠️ possible but experimental / incomplete · ❌ no · n/a not a local checkpoint

---

## Runnable: what is worth trying

### 1) Needle 3 — compact on-device automation

| | |
| --- | --- |
| **Job** | Choose app tools, fill structured arguments, extract typed fields, or embed text for local search/routing |
| **Model size** | **9–29 MB** for the published CQ2 subnetworks, from 2 to 20 layers; each target engine is under 1 MB |
| **Mac path** | Cactus publishes a **macOS ARM64** build. Its docs show building the native files with **needle build --platform macos-arm64** |
| **16 GB M2 fit** | **Easy on memory.** After building, inference can run offline; the data needed to operate a fixed tool set stays small |
| **Scope** | A task model for structured outputs and tool calls, not a conversational language model |
| **License note** | The public model page describes the runtime and files but does not state a model-weight license. Review Cactus’s current terms before redistribution or commercial deployment |

Needle is the most directly usable device-side item from the video. Keep its tool schemas narrow and explicit: the model is designed to return the requested calls or fields, including an empty answer when no tool applies. The [Cactus Python docs](https://www.cactuscompute.com/blog/needle-python-docs) describe fetching the engine and weights once, then using the cached local files.

### 2) Laya — small structured decisions

| | |
| --- | --- |
| **Job** | Classify, route, score, or choose from a fixed set of options with probabilities |
| **Model size** | **0.4B parameters**; the project site lists an English artifact of about **808 MB** |
| **License** | Apache 2.0 |
| **Mac path** | Hugging Face Transformers; the project also publishes a **laya** Python package |
| **16 GB M2 fit** | **Comfortable by weight size.** The model is small enough to leave room for the rest of the desktop |
| **Limits** | English, text-only, and at most **512 tokens per question** on the cited English checkpoint; test confidence calibration against your own examples |

Laya fits jobs where the output shape is known in advance, such as routing a support ticket or returning a calibrated yes/no score. Use ordinary code for arithmetic, counting, and date comparisons; those are listed as limitations in the [model card](https://huggingface.co/convaiinnovations/laya).

### 3) Bonsai 2 27B — useful only with a short context

| | |
| --- | --- |
| **Job** | General text and image model with reasoning, coding, and agent-oriented behavior |
| **Architecture** | Qwen3.8 27B compressed to ternary weights; Apache 2.0 |
| **MLX artifact** | **8.6 GB** including the vision tower; the language weights alone are listed as 7.67 GB |
| **Reported memory** | About **8.6 GB at 4K**, **8.9 GB at 10K**, and **14.4 GB at 100K** context in the publisher’s table |
| **Mac path** | **mlx-lm** with the published MLX model; the model card shows **mlx_lm.chat** and a local server |
| **16 GB M2 fit** | **Plausible at 4K–8K context with a quiet desktop, but unverified on M2.** The low context is essential; the advertised 262K maximum is not a laptop target |

The advertised **5.9 GB** is the ternary representation. For the Apple MLX build, use the artifact and memory table above: the complete MLX pack is **8.6 GB**, leaving little spare memory once the system and prompt cache are included. Start with the publisher’s MLX path and a short context; do not expect the M5 Pro throughput figure to transfer to an M2.

### 4) R2T2 — a promising Mac port candidate

R2T2 is a 2B BF16 speech model built on Qwen3-ASR, with stable-prefix streaming and reported 200–600 ms average latency. The official repository documents vLLM and a Transformers backend, but its tested setup centers on CUDA and an NVIDIA container. Its size is plausible; the missing piece is a documented Apple Silicon backend. The checkpoint also has a separate NetEase model license even though the code is Apache 2.0.

---

## Near-misses and hardware walls

### Open weights do not guarantee local fit

- **Meridian** uses the 61.7 GiB MiniMax-H3 base plus adapters and has an 88 GiB B200 reference memory figure.
- **JING** requires MiniMax-H3 assets and a six-H100 validated runtime. DAO is a research-preview world engine.
- **Occamy** is sparse for computation, but it still stores 35B weights. Three billion active parameters do not make its Q4 checkpoint a 3B file.
- **ZGCM-1** and **Nimble** have plausible quantized paths by model size, but their cited releases do not include a tested M2/MLX workflow. ZGCM’s official BF16 weights alone consume almost the full 16 GB.

### Hosted chapters and systems research

Gemini Live, both Qwen endpoints, Runway, Jev, Astra for Law, and Odyssey 3 route inference to hosted services. The Z.ai and Xiaomi chapters cover serving or training systems. GPT-Policy and the Enigma case are studies built around models and external systems; they are not local checkpoints to install.

---

## Suggested actions on this machine

**For offline tool calls or structured extraction:** Try **Needle 3** for fixed schemas and a narrow tool set.


**For a small local router, classifier, or scoring model:** Try **Laya** on English questions within its 512-token limit.


**To try the strongest general model in this video:** Load **Bonsai 2 27B** through MLX at 4K context, with spare apps closed; watch memory pressure.


**For local streaming transcription:** Keep **R2T2** on the list, but wait for or build an MPS path before treating it as a Mac-ready install.
