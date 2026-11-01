# Weekly AI video report — 2026-11-01

**Source:** [AI finally sleeps, Gemini 4 Carbon, ETH cracked, energy-based models, Anthropic IPO: AI NEWS](https://youtu.be/IGICYFyP_EI) by AI Search · published November 1, 2026 in Taipei (October 31 Pacific) · 53:54\
**Target:** M2 MacBook Pro with 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Evidence as of November 1:** All 34 chapters. Local fit is inferred from released files, runtime documentation, and tests on other machines. No models were benchmarked on this M2.

## Worth trying on your Mac

For reading an English article aloud, **Paradee** puts four voices in an 8.46 MB file and runs on the CPU. If you need another language or want to match a speaker, **Audio8 Realistic** adds a voice encoder and decoder and still has a compact Apple Silicon build. For text, **LFM3** is the smaller download; **Spark** is a useful second model for comparing answers on the same prompt.

| Configuration | Best for | Mac fit |
| --- | --- | --- |
| [Paradee 1.2 INT8](#speech-generation) | ❓ English narration in a fixed voice | ✅ Comfortable |
| [Audio8 Realistic 0.6B, 4-bit MLX](#speech-generation) | ❓ Multilingual speech and voice cloning | ✅ Comfortable for short clips |
| [LFM3-1.7B Q4_K_M](#text-and-tool-calls) | 💬 Short text tasks and tool selection | ✅ Comfortable |
| [Spark-X2.6-1.7B BF16](#text-and-tool-calls) | 💬 English or Chinese chat and coding | ✅ Comfortable at short context |
| [Unlimited OCR 2, 8-bit MLX](#document-parsing) | 💬 Turning page images into structured text | ⚠️ Constrained by page count and image buffers |

**Comfortable** means the listed configuration has a documented runtime and leaves room for the suggested input. **Constrained** means the input or working set needs particular care. Artifact sizes below use decimal GB and MB.

### Speech generation

**Paradee** is the easiest first listen. Choose one of two American or two British voices in the CPU package or the Chickadee browser extension. Try the same sentence in both accents: the package changes the pronunciation dictionary as well as the voice. The developer evaluated 200 held-out sentences; the British Isabella voice had the largest gap from its Kokoro teacher on predicted naturalness. [Release and samples](https://www.sahilmahendrakar.com/writings/paradee-1-2) · [Runtime](https://github.com/sahilmahendrakar/paradee)

**Audio8 Realistic** supports 23 languages and generates 44.1 kHz audio. Try one sentence without a reference first. For cloning, supply a short reference clip and its exact transcript. The MLX runner shares 2,048 positions among the text, reference, and generated audio, then returns a whole waveform. A longer reference leaves less room to speak. The publisher’s listening examples cover English and Chinese. [Listening examples](https://edge0-ai.github.io/Audio8_TTS/realistic-0.6b/) · [MLX Audio guide](https://blaizzy.github.io/mlx-audio/models/tts/audio8/)

### Text and tool calls

**LFM3-1.7B** is a good starting point for a bounded task such as selecting a tool from three descriptions and returning its arguments. Use Liquid’s Q4_K_M text model with llama.cpp b11960 or newer, one request at a time, and a short context such as 4K tokens. Its 256K training window describes what it can accept; working memory and prompt processing time still grow. Liquid’s release also includes vision, audio, omni, and two decision variants, each with different inputs and component costs. [GGUF card](https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF) · [Family and measurements](https://www.liquid.ai/blog/lfm3)

**Spark-X2.6-1.7B** keeps the preceding 1.7B architecture and changes the post-training. Its publisher’s Spark-MLX-LLM loads the two original weight shards on Apple Silicon. Start with one short coding or bilingual prompt, cap the answer, and check it against a known result. The model card’s benchmark gains describe the publisher’s evaluation; they give no M2 latency guarantee. [Model and inference instructions](https://huggingface.co/XHToken/Spark-X2.6-1.7B) · [Spark MLX runtime](https://github.com/XHToken/Spark-MLX-LLM)

### Document parsing

**Unlimited OCR 2** is worth trying on a scanned page with a table. Check that the rows and columns survive before adding a second page. Use the 8-bit conversion with the oMLX integration that includes mlx-vlm 0.7.11. An earlier integration rejected model parameters; the maintainer tested the fix on an M3 Ultra, including a 15-page request. Process one document at a time: the attention mechanism keeps routing state specific to that request. The published test does not establish a 15-page budget on this laptop. [Baidu’s release](https://github.com/baidu/Unlimited-OCR) · [oMLX fix and test conditions](https://github.com/jundot/omlx/pull/4934)

## Three headlines in context

- **“ETH cracked” refers to the Exponential Time Hypothesis.** OpenAI released a Lean formalization of a deterministic algorithm that counts satisfying assignments for fixed-width Boolean formulas in subexponential time in the number of variables, with polynomial space. A positive count answers the satisfiability question. This is an asymptotic result: it neither settles P versus NP nor establishes a faster solver on everyday inputs. The same announcement reports results on local smoothing (with implications for Kakeya and restriction) and on the existence of certain four-dimensional quantum field theories. OpenAI describes separate expert review efforts. [Formal statement and scope](https://github.com/openai/math/blob/main/lean/docs/378.md) · [Research announcement](https://openai.com/index/building-scientific-understanding-with-academic-communities/)
- **“Sleep” is an offline training phase.** Google’s SLEEP framework temporarily records new information during interaction. Later it generates practice examples and updates reserved memory blocks so that some information survives beyond the prompt. That distinction matters locally: leaving a chat model idle does not implement this training procedure. [Google Research](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning)
- **The energy-based model generates images.** Lee, Gladstone, and Du train a transformer to assign a score called energy to an image representation. Sampling repeatedly adjusts that representation toward lower energy. The authors demonstrate class-conditioned ImageNet synthesis and inpainting. Their results concern image generation; an end-to-end Mac configuration remains unverified. [TEM paper](https://arxiv.org/abs/2610.31889)

## Technical appendix

### Complete video chapter inventory

All 34 chapters follow the official description and timestamps. “❌ Hosted” means no public local weights were verified. “⚠️ Unverified” records unresolved deployment evidence; “— N/A” covers editorial, assets, company news, and research without a standalone inference configuration.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://youtu.be/IGICYFyP_EI?t=0) | AI news intro | Editorial | — N/A; introduces the roundup. |
| [01:10](https://youtu.be/IGICYFyP_EI?t=70) | [MotionBricks](https://nvlabs.github.io/motionbricks/) | Animation research | ⚠️ Unverified; no established M2 motion-generation runtime. |
| [03:11](https://youtu.be/IGICYFyP_EI?t=191) | [Idol](https://speridlabs.com/research/idol) | Open weights / 3D | ❌ Outside documented Mac path; CUDA SDK, with 7.2 GB reported complete GPU peak. [Model card](https://huggingface.co/speridlabs/idol) |
| [04:27](https://youtu.be/IGICYFyP_EI?t=267) | [SceneBloom](https://tinaliu0123.github.io/scenebloom/) | Scene-generation research | ⚠️ Unverified; complete scene-generation pipeline has no established Mac fit. |
| [05:48](https://youtu.be/IGICYFyP_EI?t=348) | [Unlimited OCR 2](https://github.com/baidu/Unlimited-OCR) | Open weights / OCR | ⚠️ Constrained; 8-bit MLX weights fit, but page processing adds memory. |
| [06:57](https://youtu.be/IGICYFyP_EI?t=417) | [UniAction](https://uniaction.github.io/) | World-model research | ⚠️ Unverified; no established complete local video pipeline. |
| [08:00](https://youtu.be/IGICYFyP_EI?t=480) | [AutoSwarm](https://github.com/HKUDS/AutoSwarm) | Agent coordination tool | — N/A for the coordinator; inference depends on the connected agents’ model providers. |
| [08:48](https://youtu.be/IGICYFyP_EI?t=528) | [Paradee 1.2](https://www.sahilmahendrakar.com/writings/paradee-1-2) | Open weights / speech | ✅ Comfortable; four voices in one 8.46 MB CPU model. |
| [10:02](https://youtu.be/IGICYFyP_EI?t=602) | [Hy-SimulMT](https://github.com/Tencent-Hunyuan/Hy-SimulMT) | Open weights / speech translation | ❌ Outside budget; [official Q4_K_M](https://huggingface.co/tencent/Hy-SimulMT-30B-A3B-GGUF/tree/main) is 19.75 GB before audio processing and cache. |
| [11:42](https://youtu.be/IGICYFyP_EI?t=702) | [NVIDIA SimReady Assets](https://huggingface.co/datasets/nvidia/simready-assets) | Simulation assets | — N/A; CC BY 4.0 assets, with rendering requirements set by the simulator. |
| [12:55](https://youtu.be/IGICYFyP_EI?t=775) | [OpenAI scientific discoveries](https://openai.com/index/building-scientific-understanding-with-academic-communities/) | Scientific research | — N/A; ETH, harmonic analysis, and quantum field theory results. [Released research](https://github.com/openai/math) |
| [18:10](https://youtu.be/IGICYFyP_EI?t=1090) | [Luma](https://lumalabs.ai/solutions) | Sponsored hosted creative tools | ❌ Hosted; sponsored visual-production tools. |
| [19:22](https://youtu.be/IGICYFyP_EI?t=1162) | [Anthropic IPO](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm) | Company news | — N/A; October 26 S-1 for a proposed offering. |
| [22:48](https://youtu.be/IGICYFyP_EI?t=1368) | [MatAnyone-E](https://shuyun-wang.github.io/projects/MatAnyone-E/) | Video-matting research | ⚠️ Unverified; 3.1 GB / 28.6 fps at 4K was measured on an H200 with compilation. |
| [24:02](https://youtu.be/IGICYFyP_EI?t=1442) | [Open-H3-Regenerate-2K](https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K/) | Open video refinement | ⚠️ Unverified; optimized refinement and decoding use CUDA graphs. |
| [25:19](https://youtu.be/IGICYFyP_EI?t=1519) | [StreamVibe](https://stream-vibe.github.io/) | Video-agent research | ⚠️ Unverified; project page lists code and weights as forthcoming at the report cutoff. |
| [26:26](https://youtu.be/IGICYFyP_EI?t=1586) | [MUNDO](https://mundo-world-model.github.io/) | World-model research | ⚠️ Unverified; combined reconstruction, simulation, and rendering budget is unknown on M2. |
| [27:40](https://youtu.be/IGICYFyP_EI?t=1660) | [GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra/) | Hosted LLM | ❌ Hosted; no verified public local weights. |
| [29:35](https://youtu.be/IGICYFyP_EI?t=1775) | [Gemini 4 Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) | Restricted hosted LLM | ❌ Restricted; initial access for selected cyber defenders and trusted partners. |
| [32:04](https://youtu.be/IGICYFyP_EI?t=1924) | [NVIDIA Nemotron 3.5 Transcribe](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | Open weights / ASR | ❌ Outside budget at four bits; 30B total parameters imply roughly 15 GB before overhead. |
| [33:24](https://youtu.be/IGICYFyP_EI?t=2004) | [Genie 4](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) | Hosted world model | ❌ Hosted; research preview for trusted testers. |
| [35:14](https://youtu.be/IGICYFyP_EI?t=2114) | [PhysAg3D](https://supra-3d.github.io/PhysAg3D/) | 3D asset research | ⚠️ Unverified; no established complete Mac generation path. |
| [36:24](https://youtu.be/IGICYFyP_EI?t=2184) | [SLEEP](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning) | Continual-learning research | — N/A; offline learning procedure, without a standalone inference configuration assessed here. |
| [38:29](https://youtu.be/IGICYFyP_EI?t=2309) | [Audio8 TTS](https://edge0-ai.github.io/Audio8_TTS/realistic-0.6b/) | Open weights / speech | ✅ Comfortable for short clips; Realistic 0.6B MLX conversion includes the codec. |
| [39:53](https://youtu.be/IGICYFyP_EI?t=2393) | [SenseNova Code2Video](https://github.com/OpenSenseNova/SenseNova-6.8-Code2Video) | Open weights / video code | ❌ Outside budget at four bits; roughly 13.5 GB before rendering tools and context. |
| [40:47](https://youtu.be/IGICYFyP_EI?t=2447) | [Energy-based model](https://arxiv.org/abs/2610.31889) | Image-generation research | ⚠️ Unverified; Mac sampling support and peak memory remain unresolved. |
| [41:53](https://youtu.be/IGICYFyP_EI?t=2513) | [OverSeer](https://runjiali-rl.github.io/OverSeer/) | Multi-agent world-model research | ⚠️ Unverified; joint video generation has no established M2 configuration. |
| [43:03](https://youtu.be/IGICYFyP_EI?t=2583) | [Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | Open weights / LLM | ❌ Outside budget at four bits; roughly 16.5 GB before cache and runtime overhead. |
| [44:17](https://youtu.be/IGICYFyP_EI?t=2657) | [LFM3](https://www.liquid.ai/blog/lfm3) | Open model family | ✅ Comfortable for the 1.7B quantized text model; other modalities need separate budgets. |
| [46:12](https://youtu.be/IGICYFyP_EI?t=2772) | [Apex 35B](https://www.apexin.com/apex-35b/) | Open weights / LLM | ❌ Outside budget at four bits; roughly 17.5 GB for all experts before cache. |
| [47:33](https://youtu.be/IGICYFyP_EI?t=2853) | [Groot](https://huggingface.co/GrootTeam/models) | Open weights / multimodal LLM | ❌ Outside budget; smallest [official Q4_K_M](https://huggingface.co/GrootTeam/Groot-19B-A3B-261023-GGUF/tree/main) is 11.66 GB plus a 0.90 GB projector. |
| [49:23](https://youtu.be/IGICYFyP_EI?t=2963) | [Clover 35B](https://diffuspace.ai/blog/clover-35b/) | Open weights / diffusion LLM | ❌ Outside budget at four bits; roughly 17.5 GB before runtime overhead. |
| [50:44](https://youtu.be/IGICYFyP_EI?t=3044) | [Spark-X2.6-1.7B](https://huggingface.co/XHToken/Spark-X2.6-1.7B) | Open weights / LLM | ✅ Comfortable at short context; publisher’s MLX runner loads both BF16 shards. |
| [51:58](https://youtu.be/IGICYFyP_EI?t=3118) | [SenseNova-Loop 9B](https://github.com/OpenSenseNova/SenseNova-Loop) | Open weights / multimodal LLM | ⚠️ Experimental; [community Q4_K_M](https://huggingface.co/AtomicChat/SenseNova-Loop-9B-Preview-GGUF/tree/main) is 5.63 GB, but Mac execution and peak remain unverified. |

### Deployment evidence

The machine usually has **8–11 GB** available for weights, intermediate results, and runtime overhead after macOS and other applications. A model file is only the starting cost. During text generation, cached attention keys and values grow with the conversation; for speech or OCR, reference audio and page images create their own temporary allocations. The starts above are suggested first trials. Full-process peaks, first-load peaks, and throughput on the target M2 are unmeasured. [Shared hardware assumptions](./memory-budget.md)

| Configuration and artifact evidence | What has to fit | Runtime and licensing |
| --- | --- | --- |
| [Paradee 1.2 files](https://huggingface.co/sahilmahendrakar/Paradee-8M-v1.2/tree/ed2934d4df8a4fd891e29584c5e1104649409765) | One 8.46 MB INT8 ONNX graph includes all four voices and waveform generation. Allow for the pronunciation dictionary, ONNX Runtime, and audio buffers. The teacher and alternate PyTorch files are unnecessary at inference. | [CPU package](https://github.com/sahilmahendrakar/paradee) and weights Apache-2.0. The reported 62× real-time comparison was for v1.1 on one M4 Pro CPU thread; the developer reports unchanged speed in v1.2. |
| [Audio8 4-bit MLX files](https://huggingface.co/nativ-community/Audio8-TTS-Realistic-0.6b-4bit/tree/d358839bd4e57c99b0da94659ec6f55ee68d8805) | 1.69 GB combined weights plus a 12 MB tokenizer. Only the speech generator is quantized. The codec retains source precision and handles reference encoding and waveform decoding. The [original release](https://huggingface.co/Edge0/Audio8-TTS-Realistic-0.6b/tree/main) separates the 1.20 GB model from its 1.35 GB codec. | Apache-2.0 weights, [MLX Audio](https://github.com/Blaizzy/mlx-audio) MIT. Loading the preconverted file avoids a local conversion peak. Long passages need chunking. |
| [LFM3 text GGUF](https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF/tree/bad5729bba61d076fff20d2548e62526665af215) | 1.10 GB Q4_K_M including tokenizer, no media encoder. Liquid reports 1.6 GB of KV cache alone at 128K context. Allow for compute buffers in addition to the cache. | Liquid’s LFM 1.0 weight license; [llama.cpp](https://github.com/ggml-org/llama.cpp) MIT, CPU or Metal. |
| [Spark text checkpoint](https://huggingface.co/XHToken/Spark-X2.6-1.7B/tree/e6406af83988f26e87ea92455f31db3f6476131b) | 2.00 + 1.42 GB shards, 3.42 GB total rounded, plus tokenizer and cache. No auxiliary model. Both shards are required. Use one short conversation while checking memory pressure. | Apache-2.0 for weights and [publisher’s MLX runtime](https://github.com/XHToken/Spark-MLX-LLM). Use the documented BF16 path. |
| [Unlimited OCR 2 MLX files](https://huggingface.co/mlx-community/Unlimited-OCR-2-8bit/tree/455c2df42a9df93fe4fbd945784d635d74b6261c) | 3.93 GB combined model, including vision weights, plus tokenizer. More pages increase image preprocessing, visual features, and prefill allocations. The maintainer verified output at several page counts but did not report a target-machine peak. | MIT weights, [oMLX](https://github.com/jundot/omlx) Apache-2.0. Use an integration containing the October 29 fix linked above. |

### Other chapter notes

- **Animation and 3D:** MotionBricks drives navigation and object interaction through a shared motion generator shown in Unreal Engine. SceneBloom combines language-guided layout with visual grounding to generate rooms. PhysAg3D builds geometry and articulation for movable objects. Their demonstrations do not establish complete M2 deployment paths. [MotionBricks](https://nvlabs.github.io/motionbricks/) · [SceneBloom](https://tinaliu0123.github.io/scenebloom/) · [PhysAg3D](https://supra-3d.github.io/PhysAg3D/)
- **Idol:** The 0.66B generator is part of a roughly 1.8B-parameter image-to-3D pipeline. Its reported 7.2 GB peak comes from a CUDA implementation; the published SDK requires NVIDIA hardware. [Model card](https://huggingface.co/speridlabs/idol)
- **World models:** UniAction accepts force, camera, hand, or robot controls. MUNDO combines scene reconstruction, a simulator, and video rendering. OverSeer uses fixed auxiliary camera views to keep players’ perspectives consistent. Each needs a complete runtime and memory assessment before a local recommendation. [UniAction](https://uniaction.github.io/) · [MUNDO](https://mundo-world-model.github.io/) · [OverSeer](https://runjiali-rl.github.io/OverSeer/)
- **Video processing:** MatAnyone-E separates foreground subjects from video backgrounds. Open-H3-Regenerate-2K refines a low-resolution H3 draft through diffusion and a VAE decoder. StreamVibe observes interactions over time to decide when to help. The inventory records the limits of each release’s local evidence. [MatAnyone-E](https://shuyun-wang.github.io/projects/MatAnyone-E/) · [Open-H3](https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K/) · [StreamVibe](https://stream-vibe.github.io/)
- **Larger releases:** Hy-SimulMT translates Chinese and English speech with voice cloning; Nemotron Transcribe adds transcription, translation, and diarization. Nanbeige’s 33B release is a teacher for smaller agents, and Apex derives from Qwen3.6-35B-A3B. Groot spans 19B, 65B, 238B, and 280B variants. Clover generates blocks in parallel, while Code2Video writes rendering code. Sparse activation and parallel generation still require the full weights in the configurations assessed here. [Hy-SimulMT](https://github.com/Tencent-Hunyuan/Hy-SimulMT) · [Nemotron](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) · [Nanbeige](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) · [Apex](https://www.apexin.com/apex-35b/) · [Groot](https://huggingface.co/GrootTeam/models) · [Clover](https://diffuspace.ai/blog/clover-35b/) · [Code2Video](https://github.com/OpenSenseNova/SenseNova-6.8-Code2Video)
- **SenseNova-Loop:** A shared transformer block executes repeatedly. The 5.63 GB community Q4 is small enough to investigate, but the upstream example uses custom CUDA code. A working Mac loop, image-input path, and full memory peak were not verified. [Upstream](https://github.com/OpenSenseNova/SenseNova-Loop) · [Community export](https://huggingface.co/AtomicChat/SenseNova-Loop-9B-Preview-GGUF/tree/main)

### Coverage and verification limits

The chapter inventory follows the dated video’s description and timestamps. Its opening promotional sentence names stories from another roundup, so the timestamped list determines coverage. Selected video frames identify the TEM paper at 40:47 and the three research topics at 12:55. YouTube listed English automatic captions, but the transcript text could not be retrieved. Coverage is complete at the chapter level; remarks within chapters may be missing.

For models without a checked artifact, four-bit estimates use total parameters × 0.5 bytes as a rough lower bound for that precision. Quantization metadata, larger unquantized tensors, cache, and temporary buffers add to it. Those verdicts apply to the stated precision. Published demos and timings on an H200, M3 Ultra, or M4 Pro are attributed to their source.

## Sources

- **Chapter coverage:** [AI Search video, official description, and chapter list](https://www.youtube.com/watch?v=IGICYFyP_EI). The chapter table links the primary source for each substantive item.
- **Speech:** [Paradee release and listening samples](https://www.sahilmahendrakar.com/writings/paradee-1-2), [Audio8 model and codec](https://huggingface.co/Edge0/Audio8-TTS-Realistic-0.6b), and [MLX Audio inference documentation](https://blaizzy.github.io/mlx-audio/models/tts/audio8/).
- **Text and documents:** [Liquid AI release](https://www.liquid.ai/blog/lfm3), [Spark release and runtime instructions](https://huggingface.co/XHToken/Spark-X2.6-1.7B), [Baidu OCR release](https://github.com/baidu/Unlimited-OCR), and [oMLX multi-page validation](https://github.com/jundot/omlx/pull/4934). The deployment table links the exact weight revisions used for sizing.
- **Research behind the headlines:** [ETH formalization](https://github.com/openai/math/blob/main/lean/docs/378.md), [Google’s SLEEP framework](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning), and [Lee, Gladstone, and Du’s image synthesis paper](https://arxiv.org/abs/2610.31889).
