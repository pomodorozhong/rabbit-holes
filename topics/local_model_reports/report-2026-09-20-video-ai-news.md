# Local Runnability: Models from AI News Video (2026-09-20)

- **Compiled:** 2026-09-20
- **Source video:** [OpenAI hacked, Jev, Google’s RSI, Qwen 3.8 Omni, Bonsai 2, new Gemini Live: AI NEWS](https://www.youtube.com/watch?v=hygMRgnDD7w) (AI Search, 41:06)
- **Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**
- **Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**
- **Memory budget:** [Your real memory budget](./memory-budget.md)

## TL;DR

The practical local releases are **Laya** and **Needle 3**, both narrow tools for classification, scoring, extraction, or structured decisions rather than general chat. **Bonsai 2 27B** is the most interesting general local-model experiment: its smallest published text-only GGUF is 5.95 GB, but it needs Prism’s custom low-bit runtime and has no M2 benchmark. The ready-to-load MLX package is 8.60 GB including its vision tower, so expect a tight, short-context experiment rather than a dependable daily model.

The other eye-catching model headlines hide larger or less compatible deployments. **Occamy** activates 3B parameters but stores a 35B model; its smallest official quantization is 10.86 GiB before runtime memory. **ZGCM-1**’s BF16 checkpoint is 14.8 GB. **R2T2** is only 2B parameters, but its documented live-serving path is CUDA/vLLM and its weight license is a custom NetEase agreement. None is a straightforward new M2 install.

The rest of the video is a mix of hosted APIs, research results, an inference harness, infrastructure news, a sponsor segment, and one security disclosure. They are inventoried below so every official chapter is covered.

## Runnability table (all chapters)

The timestamps follow the video’s official YouTube chapters. “Fits” refers to a useful local workflow alongside macOS and ordinary apps, not just the size of a weight file.

| Chapter / item | Kind / access | 16 GB M2 verdict | What it means locally |
| --- | --- | --- | --- |
| [0:00 — AI news intro](https://www.youtube.com/watch?v=hygMRgnDD7w&t=0s) | Roundup introduction | n/a | No model or project to install. |
| [1:08 — Meridian](https://www.youtube.com/watch?v=hygMRgnDD7w&t=68s) ([model card](https://huggingface.co/Viggle/Meridian)) | Video-generation model plus adapters | ❌ | Geometry-guided camera/view changes depend on a roughly 61.7 GiB base model, separate VGGT-Omega weights, and adapters. The reference path is high-memory CUDA; far beyond this Mac. |
| [2:39 — R2T2](https://www.youtube.com/watch?v=hygMRgnDD7w&t=159s) ([model card](https://huggingface.co/netease-youdao/Confucius4-R2T2)) | Public 2B speech-recognition checkpoint; custom NetEase weight license | ⚠️ | True streaming ASR with append-only text; the publisher reports 200–600 ms average latency. The documented server uses vLLM/CUDA; no first-party MLX/MPS streaming recipe is provided. |
| [4:09 — Jing + DAO](https://www.youtube.com/watch?v=hygMRgnDD7w&t=249s) ([project page](https://xgenlabs.ai/research/generative-world-simulation)) | World-simulation research | n/a | The video describes a persistent experience/world simulator. The linked project page does not surface a downloadable laptop checkpoint, so treat this as research rather than a local release. |
| [6:32 — Dream RSI](https://www.youtube.com/watch?v=hygMRgnDD7w&t=392s) ([project page](https://dream-rsi.com/)) | Search-policy research and code | n/a | Replays recorded search trees to compare exploration policies. It is an algorithmic improvement to search, not a new foundation model to run on the Mac. |
| [8:36 — Gemini 3.8 Live](https://www.youtube.com/watch?v=hygMRgnDD7w&t=516s) ([Google announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)) | Hosted model and API | ❌ | Live voice/visual interaction and an extended-thinking option are product/API capabilities; no local weights are offered in the announcement. |
| [10:36 — Qwen 3.8 Omni Flash](https://www.youtube.com/watch?v=hygMRgnDD7w&t=636s) ([Qwen announcement](https://qwen.ai/blog?id=qwen3.8-omni-flash)) | Hosted multimodal model/API | ❌ | The announcement focuses on the Qianwen platform and a long-context audio/video/image/text workflow. It does not link a local checkpoint. |
| [12:26 — Qwen 3.8 Live Translate](https://www.youtube.com/watch?v=hygMRgnDD7w&t=746s) ([Qwen announcement](https://qwen.ai/blog?id=qwen3.8-livetranslate)) | Hosted speech translation API | ❌ | Streaming translation with speaker separation and voice/timbre features; language coverage and latency comparisons are publisher claims. No local weights are linked. |
| [14:00 — Runway](https://www.youtube.com/watch?v=hygMRgnDD7w&t=840s) ([sponsor page](https://runwayml.com/aisearch-sept)) | Sponsor / hosted creative suite | ❌ | This chapter is a paid promotion for Runway’s cloud video tools, not a downloadable model release. |
| [15:27 — Needle 3](https://www.youtube.com/watch?v=hygMRgnDD7w&t=927s) ([Cactus model page](https://cactuscompute.com/needle)) | Tiny on-device task models | ✅ narrow tasks | The 8–29 MB model family targets structured extraction and tool/decision outputs. The tiny footprint is compelling, but it is not a conversational assistant and its speed figures are publisher-reported. |
| [17:07 — Z.ai Infra Agent](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1027s) ([Z.ai case study](https://z.ai/blog/glm-built-its-inference-infrastructure)) | Inference-infrastructure story | n/a | Z.ai describes using GLM-5.3-Flash and an internal agent to help build a large Chinese-accelerator serving fleet. This is a company case study, not a local model release. |
| [19:56 — Xiaomi real-time RL](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1196s) ([live dashboard](https://mimo.xiaomi.com/rl/)) | Live training dashboard | n/a | The dashboard showed MiMo-v2.6-Pro training in progress when checked on 2026-09-20. Its counters change over time; it is not a downloadable checkpoint page. |
| [21:27 — In-context learning](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1287s) ([GPT-Policy project](https://cheng-haha.github.io/GPT-Policy/)) | Robotics research using hosted model access | ❌ for this Mac | GPT-Policy adapts a fixed general VLM through context and an action layer. The demonstration uses a hosted GPT-6 Astra API and a robot stack; reported real-robot results cover 10 tasks with three trials per condition. |
| [23:06 — Decrypting German Enigma](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1386s) ([author’s artifact](https://mvueh-enigma-solved.carterl.chatgpt.site/)) | Human-directed model demo | n/a | The presenter describes using GPT-6 Astra during a human-led ciphertext investigation. The linked artifact page provides little inspectable evidence, so this is a demo claim, not an independently verified autonomous solve. |
| [24:57 — Jev](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1497s) ([TypeSafe announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev)) | Closed hosted decision API | ❌ | Returns structured choices/probabilities rather than free-form text. TypeSafe’s speed and calibration comparisons are vendor claims; no local weights are offered. |
| [28:38 — Laya](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1718s) ([model card](https://huggingface.co/convaiinnovations/laya)) | Open, small structured-decision models | ✅ weights fit; task-tune first | English checkpoint is 421M parameters (~808 MB); multilingual is 322M (~647 MB). Useful for finite-choice classification, routing, boolean decisions, and scoring—not general chat. The authors’ base checkpoints score below a majority baseline on their typed-decision test without task tuning; calibrate probabilities on your data. |
| [29:56 — Nimble](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1796s) ([model card](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B)) | 165 MiB LoRA adapter for Qwen3.5-9B | ❌ as released | The adapter is small, but it needs the full base model; the published reference requires a CUDA GPU with BF16 support, limits prompts to 2,048 tokens, and supports at most 26 choices. No Mac path is documented. |
| [31:00 — Astra for Law](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1860s) ([OpenAI announcement](https://openai.com/index/astra-for-law/)) | Hosted legal product | ❌ | A legal workflow around hosted GPT-6 Astra, search, and plugins. No local weights are offered. |
| [31:58 — OpenAI hacked](https://www.youtube.com/watch?v=hygMRgnDD7w&t=1918s) ([Hacktron disclosure](https://www.hacktron.ai/blog/hacking-openai)) | Security disclosure / news | n/a | Hacktron reports chaining a `libheif` issue on OpenAI’s Discourse forum with an SSO flaw to demonstrate employee-account and internal-repository access via a harmless PR. The post says the issue was fixed and a $6,500 bounty paid; OpenAI clarified the bounty recognized the OpenAI-side finding, not the researchers’ Discourse testing. These are attributed claims from the researchers’ account. |
| [34:20 — MiniMax Code](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2060s) ([GitHub](https://github.com/MiniMax-AI/minimax-code)) | Terminal coding-agent harness | ✅ as a client | This is an agent/CLI, not a base model. It can connect to a configured model endpoint, so local use depends on the model and runtime you supply. |
| [35:24 — Bonsai 2 27B](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2124s) ([MLX pack](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit), [GGUF pack](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)) | Ternary 27B text/multimodal model | ⚠️ best local experiment | The text-only GGUF is 5.95 GB (PTQ1_0) or 7.21 GB (PQ2_0); the MLX pack is 8.60 GB with the vision tower. GGUF needs Prism’s rotation-aware `llama.cpp` fork—stock `llama.cpp` does not support these weight types. Try only with a short context; no M2 performance or memory measurement is published. |
| [37:03 — Occamy](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2223s) ([model card](https://huggingface.co/Accio-Lab/occamy-1.0), [quantizations](https://huggingface.co/Accio-Lab/occamy-1.0-GGUF)) | Open agentic 35B MoE; 3B active | ❌ | Sparse activation lowers compute, not stored weight size. The smallest listed official GGUF is IQ2_M at 10.86 GiB (11.66 GB), before KV cache or runtime; Q4_K_M is 19.71 GiB. Community MLX builds exist, but the official minimum is already beyond the practical memory budget. |
| [37:59 — ZGCM](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2279s) ([model card](https://huggingface.co/zgcagi/ZGCM-1-7B), [training code](https://github.com/zgcagi/ZGCM-1)) | Open 7.39B math/search model | ❌ official pack | The published BF16 repository is 14.8 GB, leaving effectively no room for macOS, context, or activations. A smaller community quant might be possible, but the official card documents Transformers/vLLM/SGLang and `trust_remote_code`, not an Apple-native path. |
| [38:45 — Odyssey 3](https://www.youtube.com/watch?v=hygMRgnDD7w&t=2325s) ([Odyssey announcement](https://odyssey.systems/introducing-odyssey-3)) | Robotics/world-model research product | n/a | A world model plus task-specific robotics policies and simulation. No standalone M2 checkpoint/runtime was surfaced in the release material. |

**Legend:** ✅ practical fit for the stated narrow role · ⚠️ plausible but experimental or incomplete · ❌ exceeds the budget or lacks a usable local path · n/a not a local checkpoint

## Picks for this Mac

### Laya: best small structured-decision candidate

Laya is interesting when the output is a known label, boolean, or score. Its single-pass design returns typed answers and probabilities without generating prose; the English and multilingual checkpoints are each under 1 GB. The project supports `pip install laya` and Transformers loading.

Treat it as a base to specialize, not a ready zero-shot classifier. On the author’s own typed-decisions evaluation, the base English and multilingual checkpoints scored below the majority-class baseline; the higher fine-tuned score belongs to a checkpoint trained on that benchmark’s training split. Its probabilities also need temperature calibration on the target task. Use the multilingual checkpoint for non-English/non-Latin input, and validate the exact schema and choice count before deployment. The published speed measurements are on a T4 or CPU, not this M2.

### Needle 3: tiny edge extraction and tool calls

Needle 3 is the easiest fit by size: Cactus describes 8–29 MB specialized models for structured outputs and tool calls on small devices. That footprint makes it worth evaluating for one fixed extraction or routing task. Its scope is intentionally narrow, so it should complement a chat model rather than replace one. The speed and benchmark claims on the product page are publisher measurements, not M2 results.

### Bonsai 2: promising, but treat it as a short-context experiment

Bonsai 2 is the only general local model in this roundup that looks worth a deliberate test on the 16 GB M2. Do not use the headline “27B” or the smallest file size alone as a fit verdict:

- Its language weights are 5.95 GB in GGUF PTQ1_0 or 7.21 GB in GGUF PQ2_0. The separate vision tower is optional for text-only inference.
- The first-party MLX pack is 8.60 GB on disk: 7.67 GB of language weights plus 0.92 GB for the vision tower. That already exceeds this project’s preferred ~8 GB artifact target.
- The low-bit weights require the matching rotation-aware runtime. Prism says stock `llama.cpp` rejects the ternary types (and a nearby unsupported format can load with incorrect output); use Prism’s fork and matching instructions.
- Prism reports benchmarks on newer Apple Silicon systems, including M5 Pro/M5 Max. Those are publisher results, not estimates for an M2. The advertised 262K context is not a sensible starting point for this memory budget.

If testing it, start with the text-only PTQ1_0 pack and a short context. Watch memory pressure and output quality; do not infer daily-driver performance from file size or another Mac’s tokens-per-second.

### Not worth trying first

- **Occamy:** 3B active is not 3B stored. Even the smallest official quant is 10.86 GiB before cache and runtime.
- **ZGCM-1:** its official BF16 checkpoint is 14.8 GB, almost the whole unified-memory pool before inference overhead.
- **Meridian:** its base model alone is roughly 61.7 GiB, with additional geometry weights and adapters.
- **R2T2:** the model itself is modest at 2B, but the documented realtime server stack is CUDA/vLLM. It may be worth revisiting if an MPS/MLX backend appears; today there is no supported Mac streaming recipe to recommend.
- **Nimble:** the 165 MiB number is only a LoRA. The required base and CUDA/BF16 inference path are the actual deployment requirement.

## Sources

- Video, title, description, and official chapter list: [AI Search roundup](https://www.youtube.com/watch?v=hygMRgnDD7w)
- Meridian: [Viggle model card](https://huggingface.co/Viggle/Meridian)
- R2T2: [NetEase Youdao model card](https://huggingface.co/netease-youdao/Confucius4-R2T2), [inference code](https://github.com/netease-youdao/Confucius4-R2T2)
- Jing + DAO: [XGen Labs research page](https://xgenlabs.ai/research/generative-world-simulation)
- Dream RSI: [project and paper links](https://dream-rsi.com/)
- Gemini 3.8 Live: [Google announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)
- Qwen 3.8 Omni Flash: [Qwen announcement](https://qwen.ai/blog?id=qwen3.8-omni-flash)
- Qwen 3.8 Live Translate: [Qwen announcement](https://qwen.ai/blog?id=qwen3.8-livetranslate)
- Runway: [video sponsor page](https://runwayml.com/aisearch-sept)
- Needle 3: [Cactus model page](https://cactuscompute.com/needle)
- Z.ai Infra Agent: [Z.ai case study](https://z.ai/blog/glm-built-its-inference-infrastructure)
- Xiaomi real-time RL: [MiMo live dashboard](https://mimo.xiaomi.com/rl/)
- In-context robot learning: [GPT-Policy project](https://cheng-haha.github.io/GPT-Policy/)
- German Enigma demo: [author’s artifact](https://mvueh-enigma-solved.carterl.chatgpt.site/)
- Jev: [TypeSafe announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- Laya: [model card, usage, benchmarks, and limitations](https://huggingface.co/convaiinnovations/laya)
- Nimble: [Bespoke model card](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B)
- Astra for Law: [OpenAI announcement](https://openai.com/index/astra-for-law/)
- OpenAI security disclosure: [Hacktron’s report](https://www.hacktron.ai/blog/hacking-openai)
- MiniMax Code: [GitHub repository](https://github.com/MiniMax-AI/minimax-code)
- Bonsai 2: [MLX pack and full-size breakdown](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-mlx-2bit), [GGUF pack and runtime requirements](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf), [Prism announcement](https://prismml.com/news/bonsai-2-27b)
- Occamy: [official model card](https://huggingface.co/Accio-Lab/occamy-1.0), [GGUF file sizes](https://huggingface.co/Accio-Lab/occamy-1.0-GGUF)
- ZGCM-1: [model card and evaluations](https://huggingface.co/zgcagi/ZGCM-1-7B), [training repository](https://github.com/zgcagi/ZGCM-1)
- Odyssey 3: [Odyssey announcement](https://odyssey.systems/introducing-odyssey-3)
- Hardware threshold: [Your real memory budget](./memory-budget.md)

## Method / caveats

- Compiled on **2026-09-20**. I checked the official YouTube title, description, 24 chapter timestamps, and in-page transcript panel. The YouTube captions/export path was unavailable, but transcript text was visible in the page; chapter-specific details were checked against the linked primary sources where available.
- The Gemini, Qwen, Z.ai, Xiaomi, Jev, and benchmark/performance statements above are publisher claims unless explicitly labeled otherwise. The OpenAI security item is Hacktron’s disclosure account, with the bounty scope qualification quoted from the same report; it is not an OpenAI incident statement.
- The XGen Jing + DAO page and Enigma artifact exposed little independently inspectable technical material. Their descriptions are attributed to the video/presenter and are not treated as verified system capabilities.
- The Xiaomi dashboard is live and can change; its status here is a snapshot checked on the report date.
- No models were installed or benchmarked on this M2. “Fit” uses the project’s practical 8–11 GB available range for weights plus runtime/context, and distinguishes raw artifact size from a complete working inference path. See [memory-budget.md](./memory-budget.md).
- A missing Apple-native recipe in a release page means no supported path was surfaced in this research, not proof that no community conversion exists.
