# Weekly AI video report — 2026-10-18

**As of:** 2026-10-18\
**Source video:** [Quantum breakthrough, Gemini 4 Argon, MOSS Image, KLING 4, OpenAI spy, Muse Wonder: AI NEWS](https://www.youtube.com/watch?v=tDWtcyeNNew) by AI Search · published 2026-10-18 UTC · 40:55\
**Target:** M2 MacBook Pro, 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Local testing:** Not performed; assessments use artifacts, runtime documentation, and publisher or converter measurements.\
**Coverage:** All 27 official chapters in order. Official description inspected; captions could not be retrieved.

## Worth trying on your Mac

**FLUX 3 Image Klein** is the most practical local release this week: a community MLX port runs text-to-image, editing, and box-guided layout on Apple Silicon, and its converter measured a 9.6 GB peak at 1024² in low-memory mode. **LFM2.5-24B-A2B** is worth an experiment if you want a local tool-calling agent, but only its 2- and 3-bit files fit this Mac, and nobody has published quality results at those sizes. **MOSS-Image** also has a portable runner with Metal support; its plausible sub-10 GB configuration is only a compatibility experiment because it depends on an untested 3-bit text encoder and has no published Mac memory result. Most other chapters cover hosted services, very large open models, and world-model research built for NVIDIA clusters.

| Model / configuration | Best for | Why it matters this week | Mac fit |
| --- | --- | --- | --- |
| [FLUX 3 Image Klein, MLX 6-bit via `flux3-mlx`](#flux-3-image-klein) | 🖼️ Image generation and editing | 5.6B open-weights generator and editor; 9.01 GB of required weights; 9.6 GB peak measured at 1024² with `--low-memory` | ⚠️ Constrained |
| [MOSS-Image SFT, INT8 DiT plus 3-bit Qwen encoder](#moss-image) | 🖼️ Image-generation compatibility testing | `stable-diffusion.cpp` added MOSS support and has a Metal backend; the candidate files total about 9.77 GB before runtime buffers | ⚠️ Experimental |
| [LFM2.5-24B-A2B, 2–3-bit GGUF](#lfm25-24b-a2b) | 💬 Local agents and tool calling | 2.45B active parameters keep decoding cheap; small KV cache; the 8.0–9.0 GB files are the only ones within budget | ⚠️ Experimental |

**Mac fit:** ✅ Comfortable = credible path with headroom; ⚠️ Constrained = specific limits required; ⚠️ Experimental = important verification gaps; ❌ Outside budget = unsuitable for local inference on this machine. Evidence basis is recorded in the appendix.

## Image generation and editing

A diffusion image model has three parts that all need memory: a text encoder that turns the prompt into conditioning vectors, a transformer that denoises the image over several steps, and a VAE that decodes the result into pixels. The headline parameter count usually describes only the transformer, so the whole pipeline decides whether a model fits.

### FLUX 3 Image Klein

**Mac fit:** ⚠️ Constrained

**Why consider it:** Black Forest Labs released Klein as the open-weights member of FLUX 3 Image. One 5.6B transformer handles text-to-image, instruction edits, and compositions from up to 10 reference images. Prompts can also place elements with bounding boxes on a 0–1000 grid. The text encoder is Qwen3-VL-4B-Instruct. [BFL model page](https://bfl.ai/models/flux-3-image-klein) · [Model card](https://huggingface.co/black-forest-labs/flux-3-image-klein)

**Start with:** `VisualInference/FLUX-3-Image-Klein-MLX-6bit` and the [`flux3-mlx`](https://github.com/felix-ab/flux3-mlx) runner. The repository bundles a 6-bit transformer (4.833 GB), the encoder's text path in 8-bit (3.845 GB), and the VAE (0.336 GB), totaling 9.014 GB, or 8.395 GiB. Low-memory mode turns on by default below 24 GB. Begin with text-to-image at 1024² or smaller, keep the distilled model's 16 steps, and write a complete scene description in place of the optional prompt upsampler. Each image gets a JSON record with its peak memory, so the first run shows how the pipeline behaves on this Mac. Add a single reference image for editing after that.\
**Main limitation:** The converter measured **about 114 s per image** and the 9.6 GB peak on an M4 Pro with 48 GB, so an M2 will be slower, and 9.6 GB sits near the top of this Mac's 8–11 GB working budget. Each reference image adds tokens: one-reference edits took about 200–270 s on that machine. The weights are under the FLUX Kommunity License: non-commercial use, with commercial use of outputs only for Qualifying Users under US$5M in revenue.

[Video chapter](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1154s) · [MLX 6-bit port](https://huggingface.co/VisualInference/FLUX-3-Image-Klein-MLX-6bit) · [Deployment details](#flux-3-image-klein-deployment)

### MOSS-Image

**Mac fit:** ⚠️ Experimental

**Why consider it:** OpenMOSS released a 5B Apache-2.0 image model with JSON layout prompts and prompts up to 4K tokens. Before this report's cutoff, `stable-diffusion.cpp` added support for both Base and SFT, alongside its existing Metal backend. That creates a portable path missing from the official NVIDIA-only setup. [Project](https://openmoss.ai/MOSS-Image/) · [`stable-diffusion.cpp` guide](https://github.com/leejet/stable-diffusion.cpp/blob/68285df319457e2d79310b48513e4ba1bf8ebe9a/docs/moss_image.md)

**Start with:** Treat the first run as a load and compatibility test. Pair the 5.414 GB SFT INT8 ConvRot transformer with the 4.016 GB `Qwen3.5-9B-UD-IQ3_XXS.gguf` text encoder and the 0.336 GB VAE. Together they occupy about 9.77 GB before the tokenizer, runtime buffers, and image tensors. First confirm that the files load, then generate one small image before trying 1024².\
**Main limitation:** The runner's documented example uses the larger Q4_K_M encoder, while the fitting 3-bit substitution has no published image-quality or compatibility result. There is also no M2 peak-memory or timing measurement. The runner warns that Metal operations on very large matrices can be inefficient, and `--offload-to-cpu` does not create extra unified memory on this Mac.

[Video chapter](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1247s) · [Pinned 3-bit encoder](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/tree/3885219b6810b007914f3a7950a8d1b469d598a5) · [Deployment details](#moss-image-deployment)

## Local agents and tool calling

### LFM2.5-24B-A2B

**Mac fit:** ⚠️ Experimental

**Why consider it:** Liquid AI's model stores 24B parameters but routes each token through about 2.45B, so decoding costs about as much as a small model's. Liquid reports that it leads or matches Qwen3.6-35B-A3B on five of eight agentic and tool-use benchmarks, including 48.09 vs 38.19 on LiveClaw, while trailing on knowledge-heavy tests such as GPQA Diamond. It always writes a chain of thought before answering. [Liquid AI announcement](https://www.liquid.ai/blog/lfm2-5-24b-a2b) · [Model card](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B)

**Start with:** Unsloth's `UD-Q2_K_XL` (8.04 GB) or `UD-IQ3_XXS` (8.96 GB) GGUF in llama.cpp, an 8K–16K context, and the card's sampling settings (temperature 0.1, top-k 50, repetition penalty 1.05). Only 10 of its 40 layers use attention, so the KV cache adds roughly 0.3 GB at 16K tokens. Try a few tool-calling tasks and pair the model with search or retrieval, as Liquid recommends for factual questions.\
**Main limitation:** Liquid's official GGUF and MLX files start at 13.6 GB, which is outside this Mac's budget. The fitting files are community 2- and 3-bit quantizations with no published quality measurements, and the benchmark scores apply to the full-precision model. Reasoning traces also lengthen every reply. The LFM Open License allows commercial use below US$10M in annual revenue.

[Video chapter](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2267s) · [Unsloth GGUF](https://huggingface.co/unsloth/LFM2.5-24B-A2B-GGUF) · [Deployment details](#lfm25-24b-a2b-deployment)

## Other developments worth knowing

- **Big open-weight releases:** Meta's Muse Spark Open (816B total, 42B active) targets two 512 GB Mac Studios through MLX. Step 5 Preview (600B), Ling-3.1-flash (560B), and Nemotron 3.5 Super VL (120B) are also open, all far beyond 16 GB. [Muse Spark Open](https://research.meta.ai/blog/muse-spark-open) · [Details](#large-open-language-models)
- **Hosted frontier models:** Google launched Gemini 4 Argon at an introductory $2 / $10 per million input / output tokens. Meta's Muse Wonder and Muse Wonder Full are available through its API and Muse Code. [Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon) · [Muse Wonder](https://research.meta.ai/blog/muse-wonder)
- **Engine-driven world models:** Matrix-Game 4.0 and StreamRender-H3 let a game engine track world state while a video model only renders frames. Matrix-Game 4.0 runs on a single RTX 5080 but needs Linux and CUDA; StreamRender-H3 uses eight GPUs. [Matrix-Game 4.0](https://matrix-game-v4-0.github.io/page/) · [StreamRender-H3](https://nvlabs.github.io/Sana/Sol-Engine/StreamRender-H3/)
- **Quantum error correction:** Google reports in *Science* that magic state cultivation on its Willow processor cut errors about 40-fold and produced T-states with 99.99% logical fidelity. [Google](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/)

## What changed since the previous weekly report

The [October 12 report](./report-2026-10-12-video-ai-news.md) found no visual generator that fits this Mac. Kandinsky 6.0 Lite and Iris-3B both needed far more memory or CUDA. The earlier [Qwen-Image-2.1 deep dive](./report-2026-09-22-qwen-image-2.1.md) found a capable editor whose quantized files alone reached about 10–11 GB, with no credible 16 GB measurement and an MPS bug in its edit path. FLUX 3 Image Klein is the first editor in this series with a native MLX runner and a published low-memory peak under 10 GB, though that peak was measured on a larger Mac. The October 12 recommendations were not retested.

## Technical appendix

### Complete video chapter inventory

All 27 chapters below match the official description in source order. “❌ Hosted” means no verified downloadable local configuration; “⚠️ Unverified” records unresolved fit or release evidence. Research and non-model stories use “— N/A” where an inference verdict would mislead.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=tDWtcyeNNew&t=0s) | AI news intro | Editorial | — N/A; introduces the roundup. The description names Luma as sponsor, without a separate chapter. |
| [00:58](https://www.youtube.com/watch?v=tDWtcyeNNew&t=58s) | [Drama 3](https://huggingface.co/fishaudio/drama-3) | Open weights / text-to-speech | ❌ Outside supported Mac path; official inference needs at least 48 GB and an NVIDIA GPU, with no Apple MPS support. |
| [02:43](https://www.youtube.com/watch?v=tDWtcyeNNew&t=163s) | [Matrix-Game 4.0](https://matrix-game-v4-0.github.io/page/) | Open weights / interactive world model | ❌ Outside supported Mac path; inference needs Linux and an NVIDIA GPU; 10 GB checkpoint per game. |
| [03:53](https://www.youtube.com/watch?v=tDWtcyeNNew&t=233s) | [GaussiAnimate](https://cookmaker.cn/gaussianimate/) | Rigging research code | — N/A; rigs reconstructed 4D Gaussian or mesh sequences; Gaussian stages use CUDA environments. |
| [05:06](https://www.youtube.com/watch?v=tDWtcyeNNew&t=306s) | [UniForge3D](https://xishuxishu.github.io/uniforge3d-project/) | 3D reconstruction research | ⚠️ Unverified; paper and code listed as coming soon. |
| [06:10](https://www.youtube.com/watch?v=tDWtcyeNNew&t=370s) | OpenAI spy case ([Al Jazeera](https://www.aljazeera.com/news/2026/10/14/saudi-national-charged-with-planting-a-listening-device-at-openai-offices), [SF Standard](https://sfstandard.com/2026/10/13/openai-engineer-arrested-alleged-bugging-executive-conference-room/)) | Security news | — N/A; criminal complaint over a hidden recorder; allegations, not findings. No description link. |
| [07:42](https://www.youtube.com/watch?v=tDWtcyeNNew&t=462s) | [Google magic state cultivation](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/) | Quantum computing research | — N/A; hardware experiment published in *Science*. |
| [09:27](https://www.youtube.com/watch?v=tDWtcyeNNew&t=567s) | [MosaiChunk](https://mosaichunk.github.io/) | Video-memory research code | ❌ Outside budget; 0.1 GB router, but frozen backbones need 1–8 H200 GPUs. |
| [10:37](https://www.youtube.com/watch?v=tDWtcyeNNew&t=637s) | [Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon) | Hosted LLM | ❌ Hosted; API, Antigravity, and Gemini app. |
| [15:58](https://www.youtube.com/watch?v=tDWtcyeNNew&t=958s) | [Multics](https://karine-huang.github.io/Multics/) | Open weights / multi-player world model | ❌ Outside budget; 59.9 GiB peak for four players; Linux and CUDA 12.8. |
| [17:17](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1037s) | [Kling 4.0](https://kling.ai/) | Hosted video generation | ❌ Hosted; Kling web app and API. |
| [18:08](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1088s) | [Krea 3](https://www.krea.ai/blog/introducing-krea-3) | Hosted image editing | ❌ Hosted; Krea and API partners, $0.06 per 2K image. |
| [19:14](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1154s) | [FLUX 3 Image Klein](https://bfl.ai/models/flux-3-image-klein) | Open weights / image generation and editing | ⚠️ Constrained; MLX 6-bit port measured at 9.6 GB peak in low-memory mode on a 48 GB M4 Pro. |
| [20:47](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1247s) | [MOSS-Image](https://openmoss.ai/MOSS-Image/) | Open weights / image generation | ⚠️ Experimental; portable runner and about 9.77 GB of candidate files exist, but the 3-bit encoder path and M2 peak are unverified. |
| [22:03](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1323s) | [Muse Wonder](https://research.meta.ai/blog/muse-wonder) | Hosted LLM | ❌ Hosted; Meta Model API and Muse Code. |
| [24:59](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1499s) | [Muse Spark Open](https://research.meta.ai/blog/muse-spark-open) | Open weights / multimodal LLM | ❌ Outside budget; 816B total; 1.64 TB repository; gated download. |
| [27:11](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1631s) | [ATAS](https://lhmd.top/atas/) | Agentic video research code | ❌ Outside supported Mac path; geometry service needs about 20 GB of NVIDIA memory; generation uses hosted APIs. |
| [28:05](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1685s) | [InfiniSplat v2](https://zju3dv.github.io/InfiniSplat2/) | Open weights / 3D reconstruction | ❌ Outside supported Mac path; 6.6 GB weights, but installation requires CUDA. |
| [29:22](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1762s) | [StreamRender-H3](https://nvlabs.github.io/Sana/Sol-Engine/StreamRender-H3/) | Open weights / neural game rendering | ❌ Outside budget; 206.87 GB bundle; eight-GPU real-time loop. |
| [31:09](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1869s) | [Streaming Code World Model](https://github.com/TingtingLiao/streaming-code-world-model) | LoRA weights / world-model research | ❌ Outside budget; LoRAs for MiniMax-H3; 123 GB peak on an H200. |
| [32:12](https://www.youtube.com/watch?v=tDWtcyeNNew&t=1932s) | [RP1](https://github.com/Roboparty/RP1) | Open-source humanoid hardware | — N/A; robot CAD, electronics, firmware, and control stack. |
| [33:36](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2016s) | [PingpongDuo](https://www.archon.tech/research/PingpongDuo) | Robotics research | — N/A; humanoid table-tennis doubles paper; no code listed. |
| [34:53](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2093s) | [Step 5 Preview](https://www.stepfun.com/step-5-preview) | Open weights / multimodal LLM | ❌ Outside budget; 600B total, 27B active; 650 GB FP8 repository. |
| [35:58](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2158s) | [Nemotron 3.5 Super VL](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/) | Open weights / multimodal LLM | ❌ Outside budget; 120B total, 12B active; NVFP4 files total 75 GB. |
| [37:12](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2232s) | [Ling-3.1-flash](https://huggingface.co/inclusionAI/Ling-3.1-flash) | Open weights / LLM | ❌ Outside budget; 560B total, 25B active; 574 GB repository. |
| [37:47](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2267s) | [LFM2.5-24B-A2B](https://www.liquid.ai/blog/lfm2-5-24b-a2b) | Open weights / reasoning LLM | ⚠️ Experimental; 8.0–9.0 GB 2–3-bit GGUF files fit; quality at those sizes unmeasured. |
| [38:42](https://www.youtube.com/watch?v=tDWtcyeNNew&t=2322s) | [Next-Concept Modeling](https://hazyresearch.stanford.edu/blog/2026-10-12-ncm) | Language-modeling research | ⚠️ Unverified; task-specific checkpoints of 0.16–2.9 GB, MIT; CUDA recommended, Mac path untested. |

### FLUX 3 Image Klein deployment

**Configuration:** `VisualInference/FLUX-3-Image-Klein-MLX-6bit` revision `ff3aacda6ceb95207e8dbafcf7b1e4fcd94e9a5c`, converted from `black-forest-labs/flux-3-image-klein` (distilled, 16 steps); runner `flux3-mlx` 0.1.0 from PyPI (released 2026-10-16).\
**Fit evidence:** Peak memory and timing measured by the converter on an M4 Pro with 48 GB; exact file sizes; no M2 run.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Transformer, 6-bit MLX | 4.833 GB | 43 blocks' linear layers in 6-bit; embeddings and final layer stay BF16. Official BF16 is 11.10 GB. |
| Text encoder, 8-bit MLX | 3.845 GB | Text path of Qwen3-VL-4B-Instruct, layers 0–31 only; official BF16 encoder is 8.89 GB. |
| VAE | 0.336 GB | FLUX autoencoder, unchanged fp32. |
| Complete required weights | 9.014 GB (8.395 GiB) | Exact total from repository metadata; this is not peak memory. |
| Prompt upsampler, 4-bit MLX (optional) | 5.97 GB | Fine-tuned Qwen3.5-9B; the runner's README measures a 7.5 GB peak for this step alone. |

**Working memory:** The converter reports **13.0 GB peak at 1024² and 16 steps, or 9.6 GB with `--low-memory`**, which is on by default below 24 GB. For reference, BFL reports 31 GB peak for its BF16 code on a B200 at 1024² without the upsampler. Whether the upsampler and generator overlap in memory is not documented, so measure them together before relying on both.\
**Starting limits:** 1024² or smaller, 16 steps, no upsampler, one image at a time; then one reference image. At 4 steps, the converter and BFL's own code both produce visibly grainy, under-denoised output.\
**Runtime support:** Native MLX through `flux3-mlx`. The converter validated its port against BFL's reference outputs: the text-encoder hidden states, VAE, and transformer outputs match closely (cosine similarity at least 0.9999), and the 6-bit image scores 30.1 dB PSNR against BFL's example. Unsloth's GGUF transformers (2.62–6.09 GB) load in Diffusers, but that path was not checked on MPS.\
**License:** FLUX Kommunity License v1.0 for the transformer and its derivatives; Qwen3-VL-4B encoder and upsampler under Apache-2.0. The official repository is gated; the MLX port is not.\
**Unresolved:** M2 time per image, M2 peak with and without the upsampler, and edit memory with several references.

The converter skipped 4-bit on purpose: in its tests, 4-bit transformers added 5–23% high-frequency grain and changed design details, while 6-bit matched BF16 texture. The 4-bit `vanch007` MLX port (6.12 GB) and Unsloth's GGUF quality tables show the same trade-off, but neither publishes a Mac memory measurement. [Converter card](https://huggingface.co/VisualInference/FLUX-3-Image-Klein-MLX-6bit) · [Runner](https://github.com/felix-ab/flux3-mlx) · [Official card](https://huggingface.co/black-forest-labs/flux-3-image-klein) · [GGUF quality table](https://huggingface.co/unsloth/flux-3-image-klein-GGUF)

### LFM2.5-24B-A2B deployment

**Configuration:** `unsloth/LFM2.5-24B-A2B-GGUF` revision `faa77113e93335b63423e9e8d33395f86eaf8946`, quantized from `LiquidAI/LFM2.5-24B-A2B` revision `1769516ac588c4c558089c94f27d96b0dc67b183`; llama.cpp.\
**Fit evidence:** Exact file sizes and the KV cache size calculated from the model config; no M2 run.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| UD-Q2_K_XL / UD-IQ3_XXS GGUF | 8.04 GB / 8.96 GB | Community dynamic quantizations; UD-Q3_K_XL is 10.95 GB and leaves almost no headroom. |
| Official Q4_0 (QAD) GGUF / MLX 4-bit | 13.58 GB / 13.59 GB | Outside budget. Q4_K_M is 14.53 GB. |
| KV cache | About 20 KB per token at f16 | 10 attention layers × 8 KV heads × 64 dimensions; about 0.34 GB at 16K tokens, calculated. |
| Convolution state | Small, fixed | The other 30 layers use short convolutions with a 3-token cache. |

**Working memory:** Unknown on the M2. Weights plus a 16K cache come to roughly 8.4–9.3 GB before compute buffers, so the 3-bit file approaches the top of the budget.\
**Starting limits:** 8K–16K context, one request at a time, short reasoning budgets. The 131K maximum context is not a sensible starting point here.\
**Runtime support:** Liquid lists day-one llama.cpp, MLX, vLLM, SGLang, and ONNX support. Its 184 tokens/s decode figure comes from an M5 Max at an unstated quantization and does not predict M2 speed.\
**License:** LFM Open License v1.0; commercial use is licensed only below US$10M in annual revenue.\
**Unresolved:** Tool-calling quality at 2–3 bits, M2 decode speed, and peak memory with a working agent harness.

[Model card](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) · [Pinned GGUF files](https://huggingface.co/unsloth/LFM2.5-24B-A2B-GGUF/tree/faa77113e93335b63423e9e8d33395f86eaf8946) · [Official GGUF](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-GGUF) · [Announcement](https://www.liquid.ai/blog/lfm2-5-24b-a2b)

### MOSS-Image deployment

**Configuration:** MOSS-Image SFT revision `fc5de0d5`; `stable-diffusion.cpp` commit `68285df319457e2d79310b48513e4ba1bf8ebe9a`; Comfy-Org INT8 transformer and VAE at revision `f28da8f93449c16cfa7efa07dcd1303a1c0c44d1`; Unsloth Qwen3.5-9B GGUF revision `3885219b6810b007914f3a7950a8d1b469d598a5`.\
**Fit evidence:** Exact artifact metadata and runner documentation; no M2 run and no published result for the lower-bit encoder combination.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| SFT transformer, INT8 ConvRot | 5.414 GB | File documented by `stable-diffusion.cpp`; larger than the standalone community GGUF transformers but supported by this runner. |
| Qwen3.5-9B `UD-IQ3_XXS` encoder | 4.016 GB | Substitutes a 3-bit GGUF for the guide's documented Q4_K_M file; image-conditioning quality is unmeasured. |
| FLUX.2 VAE | 0.336 GB | Full VAE used for the conservative total; a 0.250 GB small VAE also exists. |
| Candidate required weights | About 9.77 GB | Before the tokenizer, runtime buffers, and image tensors. |
| Documented Q4_K_M configuration | About 11.43 GB | Uses a 5.681 GB encoder and exceeds the report's practical working target before runtime allocations. |
| Official SFT pipeline | 27.23 GB | 10.17 GB BF16 transformer, 16.79 GB BF16 text encoder, and 0.25 GB VAE. |

**Working memory:** Unknown on the M2. The candidate files already sit near the top of the 8–11 GB working target. The guide uses `--offload-to-cpu`, but CPU and GPU share the same 16 GB pool on Apple Silicon, so that flag cannot remove the total-memory risk.\
**Starting limits:** First confirm that the INT8 transformer, 3-bit encoder, VAE, and external tokenizer all load. Then try one image at a small resolution, with dimensions divisible by 16, before moving to 1024².\
**Runtime support:** `stable-diffusion.cpp` supports MOSS-Image Base and SFT and can be built with Metal. Its build guide warns that Metal is currently inefficient on some very large matrix operations. The MOSS guide demonstrates the INT8 transformer with Q4_K_M; using `UD-IQ3_XXS` is the unverified step that brings the files below 10 GB.\
**License:** Apache-2.0.\
**Unresolved:** Whether this exact combination loads and generates correctly on Metal, peak unified memory, M2 generation time, and the layout and prompt-following loss from a 3-bit text encoder.

[Project](https://openmoss.ai/MOSS-Image/) · [Pinned runner guide](https://github.com/leejet/stable-diffusion.cpp/blob/68285df319457e2d79310b48513e4ba1bf8ebe9a/docs/moss_image.md) · [Pinned Metal build guide](https://github.com/leejet/stable-diffusion.cpp/blob/68285df319457e2d79310b48513e4ba1bf8ebe9a/docs/build.md) · [Pinned portable weights](https://huggingface.co/Comfy-Org/MOSS-Image/tree/f28da8f93449c16cfa7efa07dcd1303a1c0c44d1) · [Pinned encoder files](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/tree/3885219b6810b007914f3a7950a8d1b469d598a5)

### Large open language models

**Muse Spark Open:** 816B total, 42B active, 1M-token context, natively multimodal. Meta targets two M5 Ultra Mac Studios with 512 GB each through MLX. The weights are gated and use the Muse Model License, which has limited commercial terms. [Announcement](https://research.meta.ai/blog/muse-spark-open) · [Model card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B)

**Step 5 Preview:** 600B total, 27B active, up to 1M tokens, text and image input. The FP8 repository is 650 GB; BF16 and NVFP4 versions exist. [Model card](https://huggingface.co/stepfun-ai/Step-5-Preview)

**Ling-3.1-flash:** 560B total, 25B active, hybrid linear-attention MoE with a 1M-token context; MIT license; 574 GB repository. [Model card](https://huggingface.co/inclusionAI/Ling-3.1-flash)

**Nemotron 3.5 Super VL:** 120B total, 12B active, with text, image, document, and video input. The NVFP4 checkpoint alone is 75 GB, and NVIDIA's optimizations target its own GPUs and DGX Spark. [NVIDIA blog](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/) · [NVFP4 weights](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4)

### World models and 3D

**Matrix-Game 4.0:** A game engine keeps world state and draws a low-poly proxy; a coding agent adds rules; a causal video model distilled to one or two steps renders each chunk. Each of the three games has a 10 GB checkpoint fine-tuned from Wan2.2-Fun-5B-Control, plus shared umT5 and VAE files. Inference requires Linux and an NVIDIA GPU. RTX 5080 and RTX 5070 Ti presets support fixed prompts only. The standalone game builds on macOS, but the model does not run there. Apache-2.0. [Code](https://github.com/SkyworkAI/Matrix-Game) · [Weights](https://huggingface.co/Skywork/Matrix-Game-4.0)

**StreamRender-H3 and Streaming Code World Model:** Both render engine-driven worlds with MiniMax-H3. StreamRender-H3 converts a three.js engine's semantic maps to video; its weight bundle is about 207 GB, and the real-time loop uses eight GPUs. The streaming CWM releases 2.4 GB of LoRAs and reports a 123 GB bf16 peak on one H200 at 5.1 s per 0.71 s chunk, which is not yet real time. [StreamRender-H3](https://github.com/NVlabs/Sana/tree/sol-engine/models/streamrender_h3) · [Streaming CWM](https://github.com/TingtingLiao/streaming-code-world-model)

**Multics and MosaiChunk:** Multics builds a shared world for several players on Wan2.1-1.3B; its README measures 59.9 GiB allocated at four players, growing to 106.1 GiB at ten. MosaiChunk trains only a small router that selects past KV entries for a frozen video generator. The router is 0.1 GB, but the T2V backbone runs on eight H200 GPUs and the I2V backbone on one. [Multics](https://github.com/TencentARC/Multics) · [MosaiChunk](https://github.com/mosaichunk/MosaiChunk)

**ATAS, InfiniSplat v2, GaussiAnimate, UniForge3D:** ATAS compiles a screenplay into shots with persistent scene and event memory. Its client needs no GPU, but generation calls hosted video APIs, and the geometry service needs about 20 GB of NVIDIA memory. InfiniSplat v2 reconstructs Gaussian scenes from posed or unposed images; its 6.6 GB weights are small enough, but installation requires CUDA. GaussiAnimate (MIT) rigs reconstructed characters and garments, with Gaussian stages on CUDA. UniForge3D has not released code. [ATAS](https://github.com/ziplab/ATAS) · [InfiniSplat](https://github.com/zju3dv/InfiniSplat) · [GaussiAnimate](https://github.com/Net-Maker/GaussiAnimate)

### Science, research, hosted, and news notes

**Next-Concept Modeling:** Stanford's Hazy Research lab encodes text as a hierarchy of discrete codes, from coarse to fine, and predicts each level in parallel. On an H100, the authors report 10–21× faster unconditional generation than the strongest diffusion baselines at similar perplexity. The released checkpoints are task-specific research models (TinyStories, LM1B, OpenWebText, XSum, WMT14, Sudoku), not a chat model. [Blog](https://hazyresearch.stanford.edu/blog/2026-10-12-ncm) · [Code](https://github.com/HazyResearch/ncm) · [Checkpoints](https://huggingface.co/hazyresearch/ncm-checkpoints)

**Robotics:** RP1 publishes the full design of a humanoid robot, from CAD and PCBs to firmware and learning code. PingpongDuo coordinates two humanoids playing table-tennis doubles, with a team planner that filters risky positioning; only the paper is listed. [RP1](https://github.com/Roboparty/RP1) · [PingpongDuo paper](https://arxiv.org/abs/2610.20579)

**Drama 3:** Fish Audio published downloadable weights for this 35B mixture-of-experts speech model, with 3B parameters active per token. It supports multi-character speech, voice cloning, and natural-language control, so it is not a hosted-only release. The official installer nevertheless requires at least 48 GB of GPU memory in FP8 and explicitly limits Drama 3 to NVIDIA GPUs: CPU, Apple MPS, and AMD ROCm are unsupported. [Model card](https://huggingface.co/fishaudio/drama-3) · [Pinned installation requirements](https://github.com/fishaudio/fish-speech/blob/1ff3c3ed2f80d3106a83909dd25b83129c3d816f/docs/en/install.md)

**Hosted models:** Kling 4.0 generates video with audio. Krea 3 reports edits in under 8 s at native 2K for $0.06. Gemini 4 Argon ranks first on the Vals Index, according to Google. Muse Wonder adds what Meta calls Active Memory and Active Focus for long-running agent work. [Kling](https://kling.ai/) · [Krea 3](https://www.krea.ai/blog/introducing-krea-3) · [Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon) · [Muse Wonder](https://research.meta.ai/blog/muse-wonder)

**OpenAI recording-device case:** According to news reports on the unsealed complaint, prosecutors charged OpenAI engineer Abdulrahman Alfozan with intercepting oral communications after a recorder was found in an executive conference room on September 30. They allege that a chatbot account tied to his spouse researched how to build and hide the device. OpenAI says it found no sign that code, model weights, or customer data were taken. These are allegations; the complaint itself was not reviewed for this report. [Al Jazeera](https://www.aljazeera.com/news/2026/10/14/saudi-national-charged-with-planting-a-listening-device-at-openai-offices) · [SF Standard](https://sfstandard.com/2026/10/13/openai-engineer-arrested-alleged-bugging-executive-conference-room/)

### Method and verification limits

- **Video evidence:** Retrieved official metadata, title, description, and chapter markers. Publication time is **2026-10-18 03:30:33 UTC**; duration is 2,455 seconds. The description lists 27 chapters.
- **Captions:** The English auto-caption download was rate-limited (HTTP 429). This is a chapter-based report; spoken claims within chapters were not checked.
- **Primary sources:** Inspected project pages, model cards, GitHub READMEs, and Hugging Face file metadata on 2026-10-18. The official FLUX 3 Image Klein card is gated, so its text comes from Unsloth's mirror of the card; file sizes come from the official repository's metadata. MOSS-Image's portable assessment combines a runner and artifacts available before the report cutoff, but the exact lower-bit configuration was not run. The OpenAI chapter has no description link, and no Justice Department filing was retrieved; news reports are cited instead. The Step 5 Preview page renders without static content, so details come from its Hugging Face card.
- **Memory interpretation:** MB/GB are decimal unless a source reports GiB. Download size, resident memory, and peak memory differ. The FLUX peaks are the converter's measurements on a 48 GB M4 Pro; the LFM2.5 KV cache is calculated from its config.
- **Coverage:** All 27 chapters are preserved. The Luma sponsorship appears only in the description.
- **Local verification:** Documentation and artifact inspection only. No model was downloaded for execution, installed, or benchmarked.

## Sources

- **Video:** [AI Search roundup](https://www.youtube.com/watch?v=tDWtcyeNNew) — official metadata and 27 chapters.
- **Drama 3:** [Fish Audio](https://fish.audio/drama-3/) · [Model card](https://huggingface.co/fishaudio/drama-3) · [Pinned installation requirements](https://github.com/fishaudio/fish-speech/blob/1ff3c3ed2f80d3106a83909dd25b83129c3d816f/docs/en/install.md).
- **Matrix-Game 4.0:** [Project](https://matrix-game-v4-0.github.io/page/) · [Code](https://github.com/SkyworkAI/Matrix-Game) · [Weights](https://huggingface.co/Skywork/Matrix-Game-4.0).
- **GaussiAnimate:** [Project](https://cookmaker.cn/gaussianimate/) · [Code](https://github.com/Net-Maker/GaussiAnimate).
- **UniForge3D:** [Project](https://xishuxishu.github.io/uniforge3d-project/).
- **OpenAI recording-device case:** [Al Jazeera](https://www.aljazeera.com/news/2026/10/14/saudi-national-charged-with-planting-a-listening-device-at-openai-offices) · [SF Standard](https://sfstandard.com/2026/10/13/openai-engineer-arrested-alleged-bugging-executive-conference-room/).
- **Google Quantum AI:** [Google blog](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/) · [*Science* paper](https://www.science.org/doi/10.1126/science.aee7961).
- **MosaiChunk:** [Project](https://mosaichunk.github.io/) · [Code](https://github.com/mosaichunk/MosaiChunk) · [Weights](https://huggingface.co/mosaichunk/MosaiChunk).
- **Gemini 4 Argon:** [Google announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon).
- **Multics:** [Project](https://karine-huang.github.io/Multics/) · [Code](https://github.com/TencentARC/Multics) · [Weights](https://huggingface.co/TencentARC/Multics).
- **Kling 4.0:** [Kling AI](https://kling.ai/).
- **Krea 3:** [Krea announcement](https://www.krea.ai/blog/introducing-krea-3).
- **FLUX 3 Image Klein:** [BFL model page](https://bfl.ai/models/flux-3-image-klein) · [Official weights](https://huggingface.co/black-forest-labs/flux-3-image-klein) · [MLX 6-bit port](https://huggingface.co/VisualInference/FLUX-3-Image-Klein-MLX-6bit) · [`flux3-mlx` runner](https://github.com/felix-ab/flux3-mlx) · [Unsloth GGUF](https://huggingface.co/unsloth/flux-3-image-klein-GGUF) · [Prompt upsampler](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup).
- **MOSS-Image:** [Project](https://openmoss.ai/MOSS-Image/) · [Base](https://huggingface.co/OpenMOSS-Team/MOSS-Image-Base) · [SFT](https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT) · [Pinned runner guide](https://github.com/leejet/stable-diffusion.cpp/blob/68285df319457e2d79310b48513e4ba1bf8ebe9a/docs/moss_image.md) · [Pinned Metal build guide](https://github.com/leejet/stable-diffusion.cpp/blob/68285df319457e2d79310b48513e4ba1bf8ebe9a/docs/build.md) · [Pinned portable weights](https://huggingface.co/Comfy-Org/MOSS-Image/tree/f28da8f93449c16cfa7efa07dcd1303a1c0c44d1) · [Pinned encoder files](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF/tree/3885219b6810b007914f3a7950a8d1b469d598a5) · [Community transformer GGUF](https://huggingface.co/realrebelai/MOSS-Image_GGUFs).
- **Muse Wonder:** [Meta announcement](https://research.meta.ai/blog/muse-wonder).
- **Muse Spark Open:** [Meta announcement](https://research.meta.ai/blog/muse-spark-open) · [Model card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B).
- **ATAS:** [Project](https://lhmd.top/atas/) · [Code](https://github.com/ziplab/ATAS).
- **InfiniSplat v2:** [Project](https://zju3dv.github.io/InfiniSplat2/) · [Code](https://github.com/zju3dv/InfiniSplat) · [Weights](https://huggingface.co/Edisoneh/InfiniSplat-v2).
- **StreamRender-H3:** [Project](https://nvlabs.github.io/Sana/Sol-Engine/StreamRender-H3/) · [Code](https://github.com/NVlabs/Sana/tree/sol-engine/models/streamrender_h3).
- **Streaming Code World Model:** [Code](https://github.com/TingtingLiao/streaming-code-world-model) · [LoRAs](https://huggingface.co/Luffuly/streaming-code-world-model).
- **RP1:** [Repository](https://github.com/Roboparty/RP1).
- **PingpongDuo:** [Project](https://www.archon.tech/research/PingpongDuo) · [Paper](https://arxiv.org/abs/2610.20579).
- **Step 5 Preview:** [StepFun page](https://www.stepfun.com/step-5-preview) · [Model card](https://huggingface.co/stepfun-ai/Step-5-Preview).
- **Nemotron 3.5 Super VL:** [NVIDIA blog](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/) · [NVFP4 weights](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4).
- **Ling-3.1-flash:** [Model card](https://huggingface.co/inclusionAI/Ling-3.1-flash).
- **LFM2.5-24B-A2B:** [Liquid AI announcement](https://www.liquid.ai/blog/lfm2-5-24b-a2b) · [Model card](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) · [Official GGUF](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-GGUF) · [Unsloth GGUF](https://huggingface.co/unsloth/LFM2.5-24B-A2B-GGUF).
- **Next-Concept Modeling:** [Blog](https://hazyresearch.stanford.edu/blog/2026-10-12-ncm) · [Code](https://github.com/HazyResearch/ncm) · [Checkpoints](https://huggingface.co/hazyresearch/ncm-checkpoints).
