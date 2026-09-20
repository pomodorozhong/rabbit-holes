# Local Runnability: Models from AI News Video (2026-08-30)

**Compiled:** 2026-08-30  
**Source video:** [Ox Alpha reveal, realtime Minimax, Qwen Next, Hy4, robot olympics: AI NEWS](https://www.youtube.com/watch?v=4wjHNgMLeyY) (AI Search)  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**  
**Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**  
**Memory budget:** [Your real memory budget](./memory-budget.md)

## TL;DR

| Verdict | Models |
| --- | --- |
| **Runs well on this Mac** | **VoiceMem** local stack only (FunASR + e5-small + sherpa-onnx; writes go to a cloud LLM) |
| **Tight / experimental** | **Fibo 1.5** via **mflux / MLX q4** of the 8B DiT (~10.2 GiB disk, **~11.4 GB** peak RSS) — over the daily-use line; official path is CUDA |
| **Open weights, not this machine** | GLM-5.3-Flash (Ox Alpha), GLM-5.3, Qwen3.8-Flash-Next, Hy4-preview, FastH3 / MiniMax H3, FixAnything (Wan 2.1 14B), OVOW, Block3D, Code World Model |
| **API / web / not released** | FAL H3 Max, Gemini 3.5 Transcribe, Gemini Omni 1.1 Flash, Google Planetary Prediction Engine, Skild **S1**, Xiaomi AI Cube |
| **Framework / hardware, not a laptop checkpoint** | DiffusionOPSD (training recipe), Orbit++ (benchmark), World Humanoid Games, Luma Agents (sponsor) |

This week’s headline open models are **100 GB+ even at 1-bit**. MLX ports exist for Flash-tier LLMs and MiniMax H3; they do **not** drop the floor to 16 GB. The only new local-adjacent pickup is **VoiceMem**. Keep daily chat on Gemma 4 12B / Ornith 1.5 9B from prior reports.

---

## MLX / MPS vs GGUF (does a Mac port change the verdict?)

The user-facing question this week is whether an Apple-native port makes any of the frontier drops runnable here. Short answer: **only Fibo, and barely.**

| Model | Mac-native port? | Smallest practical artifact | 16 GB M2? |
| --- | --- | ---: | --- |
| **GLM-5.3-Flash** | **Yes — MLX** ([PipeNetwork/glm53-flash-mlx](https://github.com/PipeNetwork/glm53-flash-mlx), `glm5_next` in mlx-vlm main). Also Unsloth GGUF **Metal** (fork until llama.cpp merges) | GGUF UD-IQ1_S **93.1 GB** (Unsloth: **~100 GB RAM**). OrcaRouter MLX 2bit-lite **~102 GB** / **112 GB min** | ❌ MLX is *larger* than 1-bit GGUF |
| **GLM-5.3** (full) | GGUF **Metal** via Unsloth. No useful MLX laptop pack | UD-IQ1_S **217 GB** (~**220 GB RAM**) | ❌ |
| **Qwen3.8-Flash-Next** | **Yes — MLX** ([PipeNetwork/qwen38-flash-next-mlx](https://github.com/PipeNetwork/qwen38-flash-next-mlx)). GGUF **Metal** can **mmap the 51B n-gram table** to SSD | Unsloth UD-IQ1_S **72.5 GB**. AtomicChat mmap build still wants **≥64 GB unified**. PipeNetwork MLX 4-bit **103.8 GB** | ❌ MLX keeps the table in RAM; GGUF mmap still starts at **64 GB** |
| **Hy4-preview** | **No MLX.** GGUF needs a **patched** llama.cpp (`hyv4`); CUDA-first | AngelSlim STQ1_0 **~214 GiB** | ❌ |
| **FastH3 / MiniMax H3** | **Yes — MLX** ([FastVideo MPS guide](https://haoailab.com/FastVideo/getting_started/installation/mps/), [PipeNetwork/minimax-h3-mlx](https://github.com/PipeNetwork/minimax-h3-mlx)) | PipeNetwork 4-bit DiT **11.5 GB resident** — but Qwen3-VL-32B encoder is **~67 GB**. FastH3 MLX validated on **M4 Max 36 GB** | ❌ encoder + DiT + VAE |
| **Fibo 1.5** | **Yes — mflux / mlx-gen** for the **FIBO 8B** family (`fibo` / `fibo-lite`; 1.5 is the same 8B DiT, fewer steps) | q4/BF16 **10.2 GiB** disk, **11.39 GB** max RSS | ⚠️ at the 11 GB line |
| **VoiceMem** | FunASR **`device=mps`**. Not an MLX LLM | e5-small + Paraformer + Silero — small | ✅ engine; cloud for writes |
| **FixAnything / OVOW / Block3D / CWM** | CUDA / A100 / H800 recipes. No MLX ports that matter | Wan 14B ~**60 GB**; OVOW **>40 GB VRAM**; CWM + H3 on **H800 80 GB** | ❌ |

**Read:** an MLX conversion is not a RAM-class drop. For this week’s MoEs, GGUF + mmap is the *more* Mac-friendly path, and even that wants a **64–128 GB** machine.

---

## Runnability table (all models mentioned)

Chapter order follows the video. Timestamps are the official YouTube chapters.

| # | Model / item | Video | Kind | Open weights? | Fits 16 GB M2? | Notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | **Block3D** | [1:11](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=71s) | Text → 3D (block-wise diffusion over Cube tokens) | Code yes (RAIL-MS). Cube tokenizer + your own `gpt_final.safetensors` | ❌ | **5 s on A100 80 GB**. Official env is **Linux + CUDA**. No MLX |
| 2 | **OVOW** (One Video, One World) | [2:07](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=127s) | Video → simulation-ready 4D meshes | Code yes (training-free pipeline) | ❌ | Video: **>40 GB VRAM**. Chains **Qwen3-VL + SAM 3 + FLUX.2 + Hi3DGen**. Non-commercial pieces in the stack |
| 3 | **FixAnything** | [3:30](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=210s) | 3DGS/NeRF/mesh render cleanup | Yes (Apache 2.0 LoRA) | ❌ | Rank-64 LoRA on **Wan2.1-I2V-14B-480P** (~**60 GB** base). CUDA / DiffSynth |
| 4 | **Google Planetary Prediction Engine** | [4:53](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=293s) | Earth-data ML agent | No public laptop weights | ❌ | Google Research system, not a checkpoint |
| 5 | **Code World Model** | [6:28](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=388s) | Coding-agent world + MiniMax H3 renderer | Yes (Apache 2.0 LoRA + examples) | ❌ | Fine-tuned **MiniMax-H3 Ref2VA**. Video: **H800 80 GB**. Same H3 tax as FastH3 |
| 6 | **VoiceMem** | [8:27](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=507s) | Streaming dual-brain memory for voice agents | Yes (Apache 2.0) | ✅ engine | Local: FunASR / sherpa-onnx / e5-small. **Writes need OpenAI-class LLM**. Qwen Omni reply SLMs do **not** fit |
| 7 | **FastH3** (FastVideo × MiniMax H3) | [10:25](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=625s) | 4-step distilled H3 T2VA (~14× on Blackwell) | Yes (H3 community license) | ❌ | **Apple Silicon guide exists.** FastH3 MLX: **M4 Max 36 GB**. PipeNetwork 4-bit DiT 11.5 GB resident **without** the 32B encoder |
| 7b | **Kijai ComfyUI H3** | same chapter | Quantized H3 for Comfy | Yes | ❌ | Video’s **~22.9 GB** Comfy checkpoint; w4a8 FL2VA **12.5 GB** is CUDA/Comfy-kitchen, not Metal |
| 8 | **FAL H3 Max** | [12:40](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=760s) | Faster H3 finetune | **Closed API** (OSS promised) | ❌ | Not a local drop |
| 9 | **Ox Alpha → GLM-5.3-Flash** | [15:31](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=931s) | 320B / 18B-A multimodal MoE | Yes (MIT) | ❌ | BF16 ~**328–643 GB**. Unsloth 1-bit **93.1 GB**. Floor **~100 GB RAM**. First GLM-5 with **vision** |
| 10 | **GLM-5.3** (full) | [19:30](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=1170s) | ~744–753B / ~40B-A text MoE | Yes | ❌ | No vision (unlike Flash). 1-bit **217 GB**. Mac Studio / multi-GPU story |
| 11 | **Qwen3.8-Flash-Next** | [20:42](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=1242s) | 125B / 6B-A + 51B n-gram; Qwen4 preview | Yes | ❌ | Unsloth 1-bit **72.5 GB**. AtomicChat: **no build fits ≤48 GB**, even with table on SSD. MLX 4-bit **104 GB** |
| 12 | **Hy4-preview** (Tencent Hunyuan) | [24:14](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=1454s) | 770B / 49B-A productivity MoE | Yes (Apache 2.0) | ❌ | BF16 ~**1.56 TB**. STQ1_0 GGUF **~214 GiB**. vLLM/SGLang **8-GPU**. **No MLX** |
| 13 | **Gemini 3.5 Transcribe** | [31:35](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=1895s) | ASR / live captions | No | ❌ | AI Studio / Gemini Mac app / enterprise |
| 14 | **Gemini Omni 1.1 Flash** | [33:53](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2033s) | Hosted video generator | No | ❌ | AI Studio / Flow. Not Veo weights |
| 15 | **Orbit++** | [35:10](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2110s) | Hard camera-motion benchmark | Dataset | n/a | Stress-test for COLMAP / MegaSAM-class systems |
| 16 | **Xiaomi AI Cube** | [36:22](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2182s) | 80–160 GB unified NPU box | Hardware prototype | ❌ | Not software you install on an M2 |
| 17 | **DiffusionOPSD** | [38:14](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2294s) | Reward post-training for diffusion | Code + recipe (Apache 2.0) | ❌ | Trains **SD3.5-M / Z-Image-Turbo** on CUDA. Not an inference checkpoint for this Mac |
| 18 | **Fibo 1.5** (Bria) | [40:27](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2427s) | 8B JSON-native image DiT (4–6 step distilled) | Yes (gated, non-commercial) | ⚠️ | Same 8B + SmolLM3-3B + Wan 2.2 VAE as FIBO 1.0. Official `.to("cuda")`. MLX q4 **~11.4 GB RSS** |
| 19 | **S1** (Skild AI) | [41:32](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=2492s) | Robot FM: one-video in-context learning | **No weights / no API** | ❌ | Needs a robot. Industrial partners only |
| — | **World Humanoid Games 2026** | [26:19](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=1579s) | Tiangong / AGIBOT demos | n/a | ❌ | Hardware |
| — | **Luma Agents** (sponsor) | [13:40](https://www.youtube.com/watch?v=4wjHNgMLeyY&t=820s) | Cloud creative workspace | n/a | ❌ | Seedance / Kling / Ray hosted |

**Legend:** ✅ daily use · ⚠️ possible but painful / experimental · ❌ no

---

## Runnable / near-runnable: how it would run

### 1) VoiceMem — **the only practical pickup from this video**

| | |
| --- | --- |
| **Org** | xzf-thu / VoiceMem |
| **Job** | Streaming memory graph for voice agents: “left brain” facts, “right brain” persona/emotion. Retrieval ~**134 ms** |
| **What is local** | Paraformer streaming ASR, Silero VAD, 3D-Speaker, **multilingual-e5-small**, mem0 backend |
| **What is not** | Default **write-side extraction uses `OPENAI_API_KEY`**. Optional reply SLMs (Qwen2.5-Omni / Qwen3-Omni / Step-Audio2-Mini) and the Qwen3.6-35B-A3B LoRA are **not** 16 GB daily drivers |
| **16 GB M2 fit** | **Yes for the engine.** FunASR documents **`device=mps`**. e5-small is hundreds of MB |
| **Mac path** | `pip install voicemem` + HF default-models env. PyTorch-MPS / ONNX, not mlx-lm |
| **License** | Apache 2.0 |

**How it runs on this Mac**

- Download `zhifeixie/VoiceMem_Default_Models_Env`. Ingest audio locally; **search/retrieval stays on-device**.
- Keep extraction on a cheap API (the demo’s OpenAI key) *or* point writes at whatever small local LLM you already run (Gemma 4 12B / Ornith 1.5 9B) if you patch the client — quality of extracted memories will track that model.
- Do **not** also load Qwen Omni as the spoken reply model on this laptop. Pair VoiceMem with IndexTTS / Audio8-TTS from prior reports if you want local voice out.

```bash
pip install voicemem
hf download zhifeixie/VoiceMem_Default_Models_Env --local-dir ./models
# demo UI still wants a cloud key for write-side extraction
export OPENAI_API_KEY=sk-...
python web/run.py   # http://localhost:8787
```

HF env: [zhifeixie/VoiceMem_Default_Models_Env](https://huggingface.co/zhifeixie/VoiceMem_Default_Models_Env) · code: [xzf-thu/VoiceMem](https://github.com/xzf-thu/VoiceMem)

---

### 2) Fibo 1.5 — **only if you insist on local images; not daily**

| | |
| --- | --- |
| **Org** | Bria AI |
| **Job** | JSON-native T2I + iterative edit; 4–6 steps, no CFG |
| **Size** | **8B DiT** + **SmolLM3-3B** encoder + Wan 2.2 VAE (architecture unchanged vs FIBO 1.0; distillation is steps, not width) |
| **On-disk (MLX, base FIBO)** | q8 **14.5 GiB** / **15.89 GB** RSS · q4 **10.2 GiB** / **11.39 GB** RSS ([AbstractFramework/fibo-4bit](https://huggingface.co/AbstractFramework/fibo-4bit)) |
| **16 GB M2 fit** | **Borderline no for daily use.** 11.39 GB peak already crosses the **>11 GB** line; local FIBO-VLM is a second model. Official card is **`pipe.to("cuda")`** with CPU offload as the OOM escape |
| **Mac path** | **mflux** / mlx-gen presets `fibo` / `fibo-lite` (ComfyUI-mflux-AnyModel). **1.5 distilled weights may still need a loader update** — treat q4 numbers as the 8B family, not a guaranteed 1.5 pack |
| **License** | Gated **non-commercial** (`bria-fibo`) |

**How it would feel**

- Close everything. Load **q4 only**, skip the local VLM, expand prompts with Gemini or with Gemma 4 12B **not loaded at the same time**.
- Expect swap if Cursor + browser stay open. This is the same class of “it loaded once on an M5 Max 128 GB measurement” — those RSS numbers are not a 16 GB M2 workflow.
- Do not follow the CUDA quickstart hoping MPS is a drop-in; if you try Diffusers, it is an experiment, not a productized Metal pipeline.

```bash
# Conceptual mflux path (base FIBO family — confirm 1.5 repo id before downloading)
# q4 pack ~10 GB; peak RSS reported 11.39 GB on a 128 GB Mac
```

If you want local images on this machine at all, this is the **least-impossible** item in the video. It is still worse UX than skipping image gen locally.

---

## Why the rest fail on this Mac

### Frontier open LLMs (the video’s main event)

| Model | Local reality | MLX note |
| --- | --- | --- |
| **GLM-5.3-Flash** (ex **Ox Alpha**) | 320B / 18B-A, native multimodal. Unsloth: 1-bit **93 GB**, run on **102 GB**; 3-bit on **128 GB**. Atomic Chat: **below 64 GB there is no path** | PipeNetwork MLX 4-bit **178 GB**, 8-bit **334 GB**. OrcaRouter 2bit-lite still **~112 GB min**. MLX does **not** beat 1-bit GGUF |
| **GLM-5.3** | Same size class as 5.2 (~744B / 40B-A). Unsloth 1-bit **217 GB** / ~**220 GB RAM**; 2-bit **239 GB** for **256 GB** machines. **Text-only** (Flash stole vision) | Not a laptop MLX target |
| **Qwen3.8-Flash-Next** | 125B / 6B-A + **51B n-gram table**. Unsloth 1-bit **72.5 GB**, docs say **~75 GB RAM**. AtomicChat mmap: **64 GB Mac** is the floor; **≤48 GB = none** | PipeNetwork MLX 4-bit **103.8 GB** (table stays hot). **GGUF mmap is the Mac trick; this M2 still has 16 GB** |
| **Hy4-preview** | 770B / 49B-A, 1M context. HF ~**1.56 TB** BF16. AngelSlim Q4_K_M **435 GiB**, STQ1_0 **214 GiB**. Official serve: **vLLM TP=8** | **No MLX port.** Patched llama.cpp is CUDA-oriented |

None of these replace Gemma 4 12B / Ornith 1.5 9B on this laptop. Use the **APIs** (Flash-tier is cheap by design) if you want that intelligence.

### Video / 3D / world

| Model | Local reality |
| --- | --- |
| **FastH3** | Distilled MiniMax H3. FastVideo **has an Apple Silicon guide** and streams the Qwen3-VL conditioner, but they validated **M4 Max 36 GB**, not 16 GB. PipeNetwork 4-bit DiT **11.5 GB resident** still needs encoder (~**67 GB** bf16) + VAEs. Kijai **22.9 / 12.5 GB** Comfy files are NVIDIA w4a8 |
| **Code World Model** | H3 LoRA + coding agent. Published path is **CUDA**, **H800 80 GB**. Quantized H3 still isn’t this Mac |
| **FixAnything** | LoRA is small; **Wan2.1-I2V-14B** is not. Same Wan wall as prior video reports |
| **OVOW** | Not one model — a **foundation-model pile**. Video’s **40 GB VRAM** line is the tell |
| **Block3D** | Fast on **A100 80 GB** (~5 s). Cube tokenizer + CUDA. Research-only RAIL. You are meant to **train** `gpt_final.safetensors` |
| **FAL H3 Max** | Paid closed API on open H3. Skip |

The same FastVideo MPS doc also lists **FastMetal-1.3B-QAD** as **16 GB+**. That is a **Wan-family** distilled model, **not** FastH3, and it is **not in this video**. Do not treat it as a FastH3 substitute.

### Cloud / robots / recipes

- **Gemini 3.5 Transcribe / Omni 1.1 Flash / Planetary Prediction Engine:** hosted. Transcribe in the Gemini **Mac app** is still cloud inference.
- **Orbit++:** harder 360° crops for reconstruction research — a dataset, not weights.
- **Xiaomi AI Cube:** 80–160 GB unified **prototype**. The point of that chapter is “this M2 is not that device.”
- **DiffusionOPSD:** ByteDance **training** method (SD3.5-M, Z-Image-Turbo). CUDA hours, not a Mac app.
- **S1 / Gen 1.5 / humanoid games:** robot policies and stadium clips.

---

## Suggested actions on this machine

```
Want something new from this video that actually fits?
  └─ VoiceMem (local ASR + memory graph)
     Keep extraction on an API, or reuse Gemma 4 12B / Ornith 1.5 9B
     Pair with IndexTTS 2.5 / Audio8-TTS for speech out
     (see 2026-08-16 and 2026-08-23 reports)

Want GLM-5.3-Flash / Qwen3.8-Flash-Next / Hy4 intelligence?
  └─ Their APIs. Local 1-bit still wants 64–128 GB unified.
     MLX ports exist for Flash and Qwen Next; they do not fit 16 GB.

Want MiniMax / FastH3 video locally?
  └─ Need ~36 GB+ Apple Silicon (FastH3 MLX) or a CUDA card.
     This M2 still has no daily local video (see LTX-2.5 report).

Want Fibo 1.5 images locally?
  └─ Only as a swap-risk experiment (mflux q4 ~11.4 GB RSS).
     Prefer a hosted image model. Do not also load a VLM.

Want Block3D / OVOW / FixAnything / Code World Model?
  └─ Workstation GPU. Not the M2.

Want S1 / AI Cube / robot games?
  └─ Not software for this laptop.
```

---

## Sources

- Video: [youtu.be/4wjHNgMLeyY](https://www.youtube.com/watch?v=4wjHNgMLeyY)
- Block3D: [ziplab/Block3D](https://github.com/ziplab/Block3D), [project](https://alexandertsui.github.io/block3d/), arXiv:2608.19567
- OVOW: [onevideooneworld.github.io](https://onevideooneworld.github.io/), [yisuanwang/OVOW](https://github.com/yisuanwang/OVOW)
- FixAnything: [kvuong2711/fix-anything](https://github.com/kvuong2711/fix-anything), [HF LoRA](https://huggingface.co/kvuong2711/fix-anything)
- Code World Model: [buaacyw/code-world-model](https://github.com/buaacyw/code-world-model), [project](https://buaacyw.github.io/cwm/)
- VoiceMem: [xzf-thu/VoiceMem](https://github.com/xzf-thu/VoiceMem), arXiv:2608.26005
- FastH3: [hao-ai-lab/FastVideo](https://github.com/hao-ai-lab/FastVideo), [MPS install](https://haoailab.com/FastVideo/getting_started/installation/mps/), [PipeNetwork/minimax-h3-mlx](https://github.com/PipeNetwork/minimax-h3-mlx)
- GLM-5.3-Flash: [z.ai blog](https://z.ai/blog/glm-5.3-flash), [Unsloth run guide](https://unsloth.ai/docs/models/glm-5.3-flash), [unsloth/GLM-5.3-Flash-GGUF](https://huggingface.co/unsloth/GLM-5.3-Flash-GGUF), [PipeNetwork GLM MLX](https://huggingface.co/pipenetwork/GLM-5.3-Flash-MLX-4bit)
- GLM-5.3: [Unsloth GLM-5.3](https://unsloth.ai/docs/models/glm-5.3), [unsloth/GLM-5.3-GGUF](https://huggingface.co/unsloth/GLM-5.3-GGUF)
- Qwen3.8-Flash-Next: [Unsloth](https://unsloth.ai/docs/models/qwen3.8-next), [unsloth/Qwen3.8-Flash-Next-GGUF](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF), [Atomic Chat guide](https://atomic.chat/blog/guides/how-to-run-qwen-3-8-flash-next-locally), [PipeNetwork Qwen MLX](https://github.com/PipeNetwork/qwen38-flash-next-mlx)
- Hy4: [Tencent-Hunyuan/Hy4-preview](https://github.com/Tencent-Hunyuan/Hy4-preview), [AngelSlim/Hy4-preview-GGUF](https://huggingface.co/AngelSlim/Hy4-preview-GGUF)
- Fibo 1.5: [briaai/Fibo-1.5](https://huggingface.co/briaai/Fibo-1.5), [AbstractFramework/fibo-4bit](https://huggingface.co/AbstractFramework/fibo-4bit)
- DiffusionOPSD: [worldbench/DiffusionOPSD](https://github.com/worldbench/DiffusionOPSD)
- S1: [skild.ai/blogs/s1](https://www.skild.ai/blogs/s1)
- Prior hardware bar: [report-2026-07-17.md](./report-2026-07-17.md)

## Method / caveats

- Inventory = every named software model/tool in the video transcript, plus robotics/hardware called out as non-applicable. ASR names in the auto-captions (Quen, Miniax, Hi4) are mapped to **Qwen**, **MiniMax**, **Hy4**.
- Hardware bar: [memory-budget.md](./memory-budget.md).
- File sizes from Hugging Face / Unsloth / Atomic Chat / PipeNetwork / vendor docs / video narration as of **2026-08-30**. Packs differ by a few hundred MB. GLM-5.3 BF16 is cited as **~756 GB** in the video vs **~744B** in Unsloth’s 5.2-same-base writeup — same class either way.
- llama.cpp support for `glm5next` / `qwen4exp` / `hyv4` was still **PR / fork** territory at compile time. That does not change the RAM math.
- Tok/s, RTF, and vendor speedups (14× FastH3, 5 s Block3D) are **published / video figures**, not re-benchmarked on this M2.
- “Open weights” ≠ “runs on a laptop.” This week is Flash-tier MoEs and Wan/H3 video — all above the 16 GB unified line even after MLX.
