# Local Runnability: Models from AI News Video (2026-08-16)

**Compiled:** 2026-08-16  
**Source video:** [New Deepseek, GLM 5.3, Grok 4.6, LTX 2.5, Qwen 3.8, Gemini 3.7: AI NEWS](https://www.youtube.com/watch?v=62HSUsS0ypo) (AI Search)  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory** (same machine as [report-2026-07-17](./report-2026-07-17.md), [report-2026-07-27-music](./report-2026-07-27-music.md), and [report-2026-08-02-video-ai-news](./report-2026-08-02-video-ai-news.md))  
**Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**

## Your real memory budget (unchanged)

16 GB unified ≠ 16 GB for the model.

- macOS + browser + IDE typically leave **~8–11 GB** usable for weights + KV / activations.
- Metal’s default GPU working set on ≤32–64 GB Macs is often ~**10.5 GB**.
- Prefer artifacts whose **on-disk size is ≤ ~8 GB**; keep context short unless measured.
- If a file is **>11 GB**, treat as “does not run” for daily use.

---

## TL;DR

| Verdict | Models |
| --- | --- |
| **Runs well on this Mac** | **IndexTTS 2.5** (MLX int8 ~5 GB) · **Cactus Needle 2** (14 MB; tool-calling toy, not a chat LLM) |
| **Tight / experimental** | **Qwen3.8-27B** at **IQ2 / Q2 only** (~9 GB) · **MiDashengLM-Gen** (CUDA-first, claimed &lt;12 GB) · **MiniMax Music 3** INT8+offload (ComfyUI / CUDA story; Metal unproven) |
| **Open weights, not this machine** | JoyAI-Video-Edit, Tencent SCoPE (Wan2.2), DeepSeek-V4-Pro, Qwen3.8-Max (2.4T), LTX-2.5, MAGI-2, Nemotron 3.5 Lightning, Muse Glimmer 30B (Q4+) |
| **Weights promised / not out** | **GLM-5.3** (~2 weeks after 2026-08-14; same ~744B/40B-active base as 5.2) |
| **Closed / cloud / gated** | Grok 4.6, Gemini 3.7 Flash, GPT-5.6 Sol ultra-fast, Google sign-language typing (Pixel 11) |
| **Framework / research, not a laptop checkpoint** | DeepSeek Harness, NeMo SwitchYard, WorldClaw, Dyna 2, Matrix |

Of everything named in the video, only **IndexTTS 2.5** is a practical new daily driver on a 16 GB M2. **Needle 2** runs trivially but is a 45M tool-caller, not a replacement for Gemma 12B / Ornith 9B. **Qwen3.8-27B** is the headline local LLM — it *loads* only as a 2-bit curiosity here; Q4 wants a **24 GB** class machine.

---

## Runnability table (all models mentioned)

Chapter order follows the video. Timestamps are the official YouTube chapters; SwitchYard is in the Nemotron Lightning chapter.

| # | Model / item | Video | Kind | Open weights? | Fits 16 GB M2? | Notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | **JoyAI-Video-Edit** | [0:47](https://www.youtube.com/watch?v=62HSUsS0ypo&t=47s) | 16B autoregressive video editor | Yes (Apache 2.0) | ❌ | DiT ~**32.5 GB**; 30 FPS @ 720p measured on a **single B200**, not a laptop |
| 2 | **Tencent SCoPE** | [2:28](https://www.youtube.com/watch?v=62HSUsS0ypo&t=148s) | Camera-path control for Wan2.2 I2V | Yes (Apache 2.0) | ❌ | Self-contained Wan2.2-I2V-A14B stack ~**67 GB**; CUDA + PyTorch 2.9 |
| 3 | **DeepSeek-V4-Pro-0813** | [3:32](https://www.youtube.com/watch?v=62HSUsS0ypo&t=212s) | MoE LLM (1.6T / 49B active) | Yes (MIT; ~893 GB shards) | ❌ | Needs multi-accelerator nodes; DSpark + DeepSeek Harness are cluster/API stories |
| 3b | **DeepSeek Harness** | [5:28](https://www.youtube.com/watch?v=62HSUsS0ypo&t=328s) | Agentic orchestrator | Yes (dev preview) | n/a | Software, not weights; still needs a huge backend model |
| 4 | **Grok 4.6** | [6:24](https://www.youtube.com/watch?v=62HSUsS0ypo&t=384s) | Frontier LLM | No | ❌ | Cursor / API / Grok Build only |
| 5 | **Qwen3.8-Max / 2.4T-A95B** | [8:11](https://www.youtube.com/watch?v=62HSUsS0ypo&t=491s) | MoE LLM (2.4T / 95B active) | Yes (weights) / hosted Max extras | ❌ | BF16 ~**4.5 TB**; NVFP4 still ~**1.3 TB** and 8× B300-class |
| 6 | **MiDashengLM-Gen** | [9:43](https://www.youtube.com/watch?v=62HSUsS0ypo&t=583s) | Unified speech/music/SFX generator | Yes (Apache 2.0) | ⚠️ | Qwen3-1.7B + flow-matching DiT; video claims **&lt;12 GB**; official `infer.py` is **`.cuda()`** |
| 7 | **LTX-2.5** | [14:04](https://www.youtube.com/watch?v=62HSUsS0ypo&t=844s) | 22B audio-video DiT | Yes (LTX-2 community license) | ❌ | Distilled INT8 transformer **21.5 GB** *plus* Gemma 4 12B text encoder + VAEs; 16 GB NVIDIA floor with offload, not 16 GB unified |
| 8 | **Google sign-language → text** | [20:38](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1238s) | On-device ASR for sign | No public weights | ❌ | Gboard / Live Transcribe on **Pixel 11** |
| 9 | **GPT-5.6 Sol ultra-fast** | [21:53](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1313s) | Hosted LLM (Cerebras) | No | ❌ | Private preview; ~750 tok/s is a datacenter SKU |
| 10 | **Qwen3.8-27B** | [23:28](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1408s) | Dense 27B VLM | Yes (Apache 2.0) | ⚠️ IQ2 only | BF16 **56 GB** · FP8 **30 GB** · Q4_K_M **~17 GB** · IQ2 **~9 GB** |
| 11 | **GLM-5.3** | [25:44](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1544s) | MoE coding/cyber LLM | Promised ~2026-08-28 | ❌ today | Same ~**744B / 40B active** base as 5.2 — never a 16 GB target even when weights land |
| 12 | **Gemini 3.7 Flash** | [28:20](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1700s) | Hosted multimodal LLM | No | ❌ | AI Studio / Gemini app (Pro/Ultra) |
| 13 | **MiniMax Music 3** | [31:03](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1863s) | Full-song generator (≤5 min) | Yes (Music3 community license) | ⚠️ | Official SGLang wants **2 CUDA GPUs**; Diffusers offload can squeeze **8 GB NVIDIA**; INT8 DiT ~**2.5 GB** + INT8 text encoder ~**9.2 GB** already fills this Mac |
| 14 | **IndexTTS 2.5** | [32:13](https://www.youtube.com/watch?v=62HSUsS0ypo&t=1933s) | Zero-shot voice clone TTS | Yes (Bilibili IndexTTS license) | ✅ | Official PyTorch wants NVIDIA ~6 GB; **MLX int8 ~5 GB**, RTF &lt;1 on Apple Silicon |
| 15 | **MAGI-2 Preview** | [34:42](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2082s) | 114B MoE audio-video | Yes (Apache 2.0) | ❌ | Preview transformer **228 GB**; full zoo **~307 GB**; **8× Hopper** for 1080p |
| 16 | **Cactus Needle 2** | [35:45](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2145s) | 45M tool-calling edge LLM | Yes (Apache 2.0) | ✅ | **14 MB** binary, **~28 MB RAM**; not a general assistant |
| 17 | **WorldClaw** | [37:32](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2252s) | Agentic 3D world builder | Code/paper; not a single checkpoint | ❌ | Orchestrates Claude + Hunyuan3D + SAM3 in Blender; hours on multi-GPU |
| 18 | **Dyna 2** | [38:42](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2322s) | Robotics world-action model | Research | ❌ | Trained on ~1M hours of egocentric video; not a Mac chat/weights drop |
| 19 | **Nemotron 3.5 Lightning** | [40:05](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2405s) | 30B MoE (3B active) | Yes (OpenMDW) | ❌ | Smallest Unsloth GGUF still **~19 GB**; official NVFP4 ~**22 GB**; H100-class story |
| 19b | **NeMo SwitchYard** | [40:05](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2405s) | LLM router / proxy | Yes (Apache 2.0, Rust) | n/a | Routes *to* models; does not replace them |
| 20 | **Matrix** | [42:05](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2525s) | 8.3B persona-agent sim | Research system | ❌ | Population simulation, not a downloadable laptop LLM |
| 21 | **Muse Glimmer 30B** | [44:00](https://www.youtube.com/watch?v=62HSUsS0ypo&t=2640s) | Dense 30B + ViT | Yes (Apache 2.0) | ⚠️ IQ2 only | Official Q4_K_M **16.8 GB** (24 GB card). Unsloth IQ2_XXS **~10.0 GiB** is fragile here; vendor tables trail Qwen 3.6/3.8 |

**Legend:** ✅ daily use · ⚠️ possible but painful / experimental · ❌ no

Sponsor product in the video (**Genspark Second Brain**) is a wearable + cloud app, not a local model.

---

## Runnable / near-runnable: how it would run

### 1) IndexTTS 2.5 — **recommended new pickup from this video**

| | |
| --- | --- |
| **Org** | IndexTeam / Bilibili |
| **Job** | Zero-shot TTS: clone a ≤15 s reference voice, speak ZH/EN/JA/ES/AR (MLX port: ZH/EN/JA/Yue) |
| **Size** | ~0.8B GPT backbone + flow-matching S2M + BigVGAN |
| **On-disk** | Official HF tree ~**5.5–7 GB** with aux codecs; **MLX int8 pack ~5 GB** |
| **16 GB M2 fit** | **Yes.** Weights sit in the comfortable band; leave headroom by closing heavy apps during synth |
| **Mac path** | Prefer **`index-tts-2.5-mlx`** (Metal, torch-free). Official `index-tts` wants NVIDIA. CPU fallback: `index-tts-2.5-mnn` (~3.6 GB fp16) if you must, but vocoder is slower |
| **License** | Bilibili IndexTTS Model Use License (not Apache) |

**How it runs on this Mac**

- Load once (~5 GB unified). Clone speaker embedding from a short WAV. Then each line is GPT decode → CFM DiT → BigVGAN.
- Packaged MLX int8 reports **RTF ≈ 0.45–0.47** on an **M5 Pro** (~2.1× realtime). On an **M2 16 GB** expect slower — likely still interactive for short lines, not instant. Stage mix: GPT is bandwidth-bound (int8 helps); CFM + BigVGAN are FLOP-bound (stay fp32).
- Do **not** use the official CUDA/vLLM recipe. Do **not** expect Ollama.

```bash
uvx index-tts-2.5-mlx synth \
  --ref voice.wav \
  --text "Hello from IndexTTS 2.5 on Metal." \
  --lang en \
  --out out.wav
```

HF: [IndexTeam/IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5) · MLX: [yunfengwang/IndexTTS-2.5-mlx](https://huggingface.co/yunfengwang/IndexTTS-2.5-mlx) · code: [index-tts/index-tts](https://github.com/index-tts/index-tts)

---

### 2) Cactus Needle 2 — **runs, different job**

| | |
| --- | --- |
| **Org** | Cactus Compute |
| **Job** | Tool calling / device control / structured extraction — **not** open-ended chat |
| **Size** | **45M** params, CQ2-bit, baked into a **14 MB** engine |
| **RAM** | **~28 MB** ceiling (256-token sliding window + tool KV sinks) |
| **16 GB M2 fit** | Trivial. Could run alongside the IDE with no thought |
| **Mac path** | `pip install cactus-needle` or the C++/WASM engine; macOS binary exists |
| **License** | Apache 2.0 |

**How it runs:** hundreds of tok/s even on a Raspberry Pi 5 (~500 tok/s claimed). On M2 it will feel instant. Quality is in the FunctionGemma-270M class on tool benches, not Gemma 12B / Ornith 9B. Use it to drive local tools or extract JSON; do not ask it to write a PR.

HF: [Cactus-Compute/needle2](https://huggingface.co/Cactus-Compute/needle2) · [cactus-compute/needle](https://github.com/cactus-compute/needle)

---

### 3) Qwen3.8-27B — **the interesting LLM, wrong RAM class at usable quants**

| | |
| --- | --- |
| **Org** | Alibaba / Qwen |
| **Job** | Dense 27B text + native image/video encoder; thinking mode; agentic coding |
| **Arch** | Hybrid: 48 Gated DeltaNet layers + 16 full attention (3:1). Native **262K** context (1M is hosted/YaRN, not the laptop default) |
| **License** | Apache 2.0 |
| **Mac path** | llama.cpp / LM Studio / Ollama GGUF once templates work. Need `--jinja` / the Qwen3.8 chat template or it rambles |

**Quant vs this Mac** (Unsloth / community GGUF, Aug 2026):

| Quant | On-disk | 16 GB M2 verdict |
| --- | ---: | --- |
| UD-IQ2_XXS | **~9.0 GB** | ⚠️ Only realistic load; visible quality loss; short context |
| UD-Q2_K_XL | **~10.7 GB** | ⚠️ Fragile (swap) |
| Q3_K_M | **~13.8 GB** | ❌ over the 11 GB daily-use line |
| IQ4_XS | **~15.7 GB** | ❌ (this is the 16 GB *discrete GPU* pick, not 16 GB unified) |
| Q4_K_M | **~17.1 GB** | ❌ — 24 GB card sweet spot |
| BF16 | **~56 GB** | ❌ |

Hybrid attention caches full KV on only **16 of 64** layers, so context is cheaper than a dense 27B of 2024 — still irrelevant if the weights themselves do not fit.

**How IQ2 would feel here:** Metal llama.cpp, 4K–8K context, close everything else. Expect low tens of tok/s at best on M2, with 2-bit quality tax. Community notes that **32 GB unified is the comfortable Q4 machine**; **24 GB** is the “nothing else open” floor. This 16 GB M2 is below that floor.

**Published quality (Qwen card — vendor harness, not re-run here):**

| Task | Qwen3.8-27B | Qwen3.6-27B | Muse Glimmer-30B | Opus 4.6 Max |
| --- | ---: | ---: | ---: | ---: |
| SWE-bench Pro | **61.7** | 53.5 | 51.2 | 53.4 |
| Terminal Bench 2.1 | 73.0 | 63.4 | 51.7 | **78.2** |
| LiveCodeBench v6 | **90.3** | 83.9 | — | 88.8 |
| GPQA Diamond | 89.2 | 87.8 | 83.5 | **91.3** |
| OSWorld-Verified | **84.3** | 63.9 | 65.9 | 72.7 |

Treat the “beats Opus 4.6 Max” lines as **vendor-reported**. Independent Artificial Analysis had not listed 3.8-27B yet as of this compile; 3.6-27B was already #1 in the medium-size bucket.

**Vision:** extra **mmproj ~0.9 GB**. Do not add it on 16 GB.

HF: [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) · GGUF: [unsloth/Qwen3.8-27B-GGUF](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF)

---

### 4) MiniMax Music 3 — **best new song model, awkward on this Mac**

| | |
| --- | --- |
| **Job** | Lyrics + caption → full song up to **~5 min**, 32 kHz stereo |
| **Arch** | 8B global LM + 0.6B local LM + flow-matching + Flow-VAE |
| **Official runtime** | SGLang-Omni on **two CUDA GPUs** |
| **Consumer path** | ComfyUI 0.33+ (INT8 DiT + INT8 text encoder + tiled VAE decode) or Diffusers with CPU offload |

**Footprint:** video quoted **9.8 GB** full / smaller INT8. ComfyUI split is roughly INT8 DiT **~2.5 GB** + pruned INT8 text encoder **~9.2 GB** + VAE **~0.2 GB**. Diffusers docs: full precision ~**22–24 GB** VRAM; leaf-level LM offload can land on **8 GB NVIDIA** (slow).

**16 GB M2:** weights *can* be downloaded. Running them through **ComfyUI Metal** is unproven; the 9.2 GB encoder alone eats the usable pool before the DiT and decode spike. Treat as **curiosity / CUDA-box**, not a replacement for [ACE-Step 1.5 2B turbo](./report-2026-07-27-music.md) on this laptop.

---

### 5) MiDashengLM-Gen — **maybe, CUDA-shaped**

Xiaomi’s unified audio-scene model: **Qwen3-1.7B** backbone + Dasheng tokenizer + 16-layer flow-matching DiT (hidden 2048), 16 kHz mono, Apache 2.0. Video: total **&lt;12 GB**, “mid-range GPU.” Official inference is `AutoModel.from_pretrained(...).cuda()`.

On paper the 1.7B LM fits easily; the DiT + tokenizer + CFG Euler steps are the RAM/latency question. No MLX/Comfy pack found at compile time. **Possible** if you force MPS and keep clips short; expect slow autoregressive audio, not IndexTTS-class UX.

Code: [xiaomi-research/midashenglm-gen](https://github.com/xiaomi-research/midashenglm-gen) · HF: [mispeech/midashenglm-gen](https://huggingface.co/mispeech/midashenglm-gen)

---

### 6) Muse Glimmer 30B — **skip unless you enjoy 2-bit**

Dense ~30B + 1.8B ViT, Apache 2.0. Official GGUF Q4_K_M **16.8 GB** is a **24 GB VRAM** file. Unsloth **UD-IQ2_XXS ~10.0 GiB** is the only file that even *approaches* this Mac — same “fragile / quality tax” bucket as Qwen3.8 IQ2, with **worse** vendor numbers vs Qwen 3.6/3.8. Keep Gemma 12B / Ornith 9B as daily drivers.

---

## Why the headline models don’t run here

### Video generators (JoyAI, SCoPE, LTX-2.5, MAGI-2)

| Model | Why not |
| --- | --- |
| **JoyAI-Video-Edit** | 16B causal DiT, **32.5 GB** weights, realtime only on **B200**. Also pulls MiMo-VL + ONNX detectors. |
| **SCoPE** | Not a small LoRA. It *is* Wan2.2-I2V-A14B (~**67 GB**) plus camera-ray PE. CUDA, 81-frame clips. |
| **LTX-2.5** | 22B DiT. INT8 transformer **21.5 GB** + Gemma 4 12B encoder (the same size class as your whole daily LLM) + video/audio VAEs. NVIDIA 16–24 GB is the *entry* tier with offload. |
| **MAGI-2** | 114B / 6B active, **228 GB** preview transformer, **8× Hopper**, 10 s clips only. |

MiniMax **H3** (compared in the LTX chapter) was already ❌ on this machine in the [2026-08-02 report](./report-2026-08-02-video-ai-news.md).

### Frontier LLMs

| Model | Local reality |
| --- | --- |
| **DeepSeek-V4-Pro-0813** | **1.6T / 49B active**, ~**893 GB** FP8 shards, 1M context, DSpark. Open MIT weights; laptop-irrelevant. Use the API. |
| **Qwen3.8-Max (2.4T-A95B)** | **2.4T / 95B active**. BF16 ~4.5 TB; smallest documented NVIDIA recipe is **NVFP4 on 8× B300**. Hosted Max adds vision / 1M / tools the open text checkpoint may not. |
| **GLM-5.3** | API/ZCode now; weights after safety hold (~2 weeks). Same **~744B / 40B active** GLM-5.2 base — cluster-scale when it opens. |
| **Nemotron 3.5 Lightning** | 30B MoE / 3B active, 1M context, **speed** play vs Qwen 3.6. Lowest GGUFs still **~19 GB**. NVFP4 ~22 GB. Aimed at H100 / 5090, not 16 GB unified. |
| **Grok 4.6 / Gemini 3.7 Flash / GPT-5.6 Sol ultra-fast** | Closed. Ultra-fast Sol is Cerebras-backed (~750 tok/s), private preview. |

### Everything else

- **WorldClaw:** agent graph (Claude Opus-class planner + Hunyuan3D + SAM3 + Blender), not a GGUF.
- **Dyna 2:** robot policy / world model from human video; no consumer Mac checkpoint.
- **Matrix:** 8.3 billion simulated personas — a research platform.
- **NeMo SwitchYard:** Rust proxy that *picks* a backend. Useful later if you host Qwen locally on a bigger box; zero help loading 27B on 16 GB.
- **Google sign language:** Pixel 11 keyboard feature.

---

## Suggested actions on this machine

```
Want a new local tool from this video?
  └─ IndexTTS 2.5 via `uvx index-tts-2.5-mlx`  (~5 GB, Metal)

Want a 14 MB gadget for tool JSON?
  └─ Cactus Needle 2  (not a chat model)

Want the new Qwen 3.8 27B intelligence?
  └─ IQ2 GGUF only if you insist (quality tax)
     Better: keep Ornith 9B / Gemma 4 12B locally; use Qwen 3.8-27B via API
     Real local Q4 wants ~24 GB VRAM or 32 GB unified

Want Music 3 quality?
  └─ Not this Mac. Keep ACE-Step 1.5 2B turbo (see music report)
     Rent a 24 GB NVIDIA if you need MiniMax songs

Want JoyAI / LTX / SCoPE / MAGI video?
  └─ Cloud or a workstation GPU. Nothing here is 16 GB Metal

Want DeepSeek V4 Pro / Qwen 3.8 Max / GLM 5.3 / Grok 4.6?
  └─ APIs. GLM weights, when they drop, still will not fit
```

---

## Sources

- Video: [youtu.be/62HSUsS0ypo](https://www.youtube.com/watch?v=62HSUsS0ypo)
- JoyAI-Video-Edit: [jd-opensource/JoyAI-Video-Edit](https://github.com/jd-opensource/JoyAI-Video-Edit), [HF](https://huggingface.co/jdopensource/JoyAI-Video-Edit), arXiv:2608.03974
- SCoPE: [TencentARC/SCoPE](https://github.com/TencentARC/SCoPE), [project page](https://visual-ai.github.io/scope/)
- DeepSeek-V4-Pro: [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- Qwen3.8-27B: [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B); GGUF sizes: Unsloth / [orcarouter GGUF guide](https://www.orcarouter.ai/blog/qwen-3-8-27b-gguf)
- Qwen3.8-Max: [Qwen/Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)
- MiDashengLM-Gen: [xiaomi-research/midashenglm-gen](https://github.com/xiaomi-research/midashenglm-gen)
- LTX-2.5: [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5), [ComfyUI tutorial](https://docs.comfy.org/tutorials/video/ltx/ltx-2-5)
- GLM-5.3: [z.ai/blog/glm-5.3](https://z.ai/blog/glm-5.3)
- MiniMax Music 3: [MiniMax-AI/MiniMax-Music3](https://github.com/MiniMax-AI/MiniMax-Music3), [ComfyUI tutorial](https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3)
- IndexTTS 2.5: [IndexTeam/IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5), [index-tts-2.5-mlx](https://pypi.org/project/index-tts-2.5-mlx/)
- MAGI-2: [sand-ai/MAGI-2-preview](https://huggingface.co/sand-ai/MAGI-2-preview)
- Needle 2: [cactuscompute.com/needle](https://cactuscompute.com/needle)
- Nemotron 3.5 Lightning GGUF: [unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF](https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF)
- SwitchYard: [NVIDIA-NeMo/Switchyard](https://github.com/NVIDIA-NeMo/Switchyard)
- Muse Glimmer: [meta-models/Muse-Glimmer-30B-GGUF](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF), [unsloth GGUF](https://huggingface.co/unsloth/Muse-Glimmer-30B-GGUF)
- WorldClaw: [Tencent-Hunyuan/Hunyuan3D-WorldClaw](https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw)

## Method / caveats

- Inventory = every named model/tool in the video, not only the title five.
- Hardware bar matches prior reports in this folder (16 GB M2 usable ~8–11 GB).
- File sizes from Hugging Face / Unsloth / Comfy-Org / vendor docs as of 2026-08-16. Packs differ by a few hundred MB.
- Qwen / GLM / MiniMax / IndexTTS speed and quality numbers are **vendor or packager-published**; this report did not re-benchmark on the M2.
- “Open weights” ≠ “runs on a laptop.” MoE active-param marketing still requires loading the full expert set unless a pruned/distilled build exists.
- GLM-5.3 weight drop is time-sensitive — recheck HF around 2026-08-28. Even then it will not fit this machine.
