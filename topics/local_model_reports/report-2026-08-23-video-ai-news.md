# Local Runnability: Models from AI News Video (2026-08-23)

**Compiled:** 2026-08-23  
**Source video:** [AI never sleeps…](https://youtu.be/rQ4yX5qNYdY) (AI Search — weekly open-source / robotics roundup)  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory** (same machine as [report-2026-07-17](./report-2026-07-17.md), [report-2026-07-27-music](./report-2026-07-27-music.md), [report-2026-08-02-video-ai-news](./report-2026-08-02-video-ai-news.md), and [report-2026-08-16-video-ai-news](./report-2026-08-16-video-ai-news.md))  
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
| **Runs well on this Mac** | **Audio8-TTS Preview 0.1B** (~1.7 GB; ONNX/PyTorch-MPS) · **Ornith 1.5 9B** Q4–Q6 GGUF (~5–8.5 GB; Metal llama.cpp) |
| **Tight / experimental** | **Audio8-TTS 0.6B** MLX bf16 (~2.5+ GB weights; better quality, still OK if apps closed) · **SenseNova U1.5** GGUF + heavy offload (CUDA-first; MPS curiosity, slow) |
| **Open weights, not this machine** | Evoke (~57 GB, H200), 4D Anyone (~12 GB + Wan/T5 stack), Bernini v2 (~180 GB), Qwen VideoEdit (~41 GB), Ornith 1.5 35B / 397B |
| **API / web / not released** | DeepSeek V4 Flash Vision Experimental (API), Happy Shrimp (web music), Geo Weaver (paper only) |
| **Framework / hardware, not a laptop checkpoint** | Comfy MCP, Gen 1.5 (robot FM), Nvidia AO harness, robots / gloves / World Robot Conference demos |

Of everything named in the video, **Audio8-TTS 0.1B** is the practical new pickup, and **Ornith 1.5 9B** is the meaningful LLM upgrade over Ornith 1.0 from [report-2026-07-17](./report-2026-07-17.md). Video / world / 4D / Bernini-class models stay off this laptop.

---

## Runnability table (all models mentioned)

Chapter order follows the video. Timestamps are the official YouTube chapters.

| # | Model / item | Video | Kind | Open weights? | Fits 16 GB M2? | Notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | **Evoke (AlayaLab)** | [0:55](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=55s) | 14B interactive world model | Yes (Apache 2.0) | ❌ | Final stage ~**57 GB**; realtime recipe is **1× H200**. CUDA + custom diffusers fork |
| 2 | **4D Anyone** | [3:02](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=182s) | Monocular video → 4D Gaussian character | Yes (multi-license assets) | ❌ | Video quoted ~**12 GB** core; full tree pulls Wan VAE + UMT5 + GVHMR. Mid/high NVIDIA story |
| 3 | **SenseNova U 1.5 8B-MoT** | [4:24](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=264s) | Unified image gen / edit / VQA (native 4K) | Yes (Apache 2.0) | ⚠️ | Video ~**50 GB** full install. BF16 wants ~**40 GB** class; GGUF + `vram_mode` targets **10–12 GB NVIDIA**. MPS unproven / slow |
| 4 | **Bernini v2** (ByteDance) | [6:22](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=382s) | Omnimodal video editor | Yes | ❌ | Video quoted **~180 GB** model alone + VAE/encoders. Dead-on-arrival for laptops |
| 5 | **Ornith 1.5 9B** | [7:27](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=447s) | Dense agentic coding VLM | Yes (MIT) | ✅ | BF16 ~**18–19 GB** no; **Q4 ~5.6–5.9 GB** / **Q5–Q6 ~6.5–8.5 GB** yes. Same class as Ornith 1.0 on this Mac |
| 5b | **Ornith 1.5 35B-A3B** | [7:27](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=447s) | MoE coding (3B active) | Yes (MIT) | ❌ | Q4 weights ~**21–22 GB**; catalogue mins often **24 GB GPU / 48 GB RAM** |
| 5c | **Ornith 1.5 397B** | [7:27](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=447s) | Flagship MoE | Yes (MIT) | ❌ | Video ~**794 GB**; multi-accelerator |
| 6 | **Audio8-TTS Preview 0.1B** | [9:43](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=583s) | Zero-shot voice-clone TTS | Yes | ✅ | Total pack ~**1.7 GB**; ~0.17B + codec. ONNX path measured ~**1 GiB** online on **M2** |
| 6b | **Audio8-TTS Preview 0.6B** | [9:43](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=583s) | Larger sibling (same family) | Yes (Apache 2.0) | ✅ | HF tree ~**2.6 GB**; **MLX bf16** via `mlx-audio` ≥0.4.7. Prefer if quality > tiny footprint |
| 7 | **Geo Weaver** | [13:30](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=810s) | Long-video → coherent 3D | Paper only | ❌ | No weights at recording time |
| 8 | **Qwen VideoEdit** | [14:38](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=878s) | Frame-wise edit via Qwen ImageEdit + Wan | Yes (code) | ❌ | Video ~**41 GB** total; high-end GPU. MiniMax H3 already ❌ here |
| 9 | **DeepSeek V4 Flash Vision Experimental** | [23:22](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1402s) | Multimodal coding LLM | API | ❌ | Video: **API only**. Text V4 Flash is also not a 16 GB target |
| 10 | **Happy Shrimp** | [24:12](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1452s) | Music generator (Happy Horse lab) | Web / free tier | ❌ | Not a local weights drop. Keep ACE-Step from music report |
| 11 | **Comfy MCP** | [27:03](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1623s) | Agentic ComfyUI connector | Yes (code) | n/a | Useful only if you already run Comfy + GPU models — you don’t on this Mac |
| 12 | **Gen 1.5** | [28:02](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1682s) | Robot foundation / one-shot imitation | Research | ❌ | Needs a robot body + sensors |
| 13 | **Nvidia AO** | [29:52](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1792s) | Agentic harness for Arc-AGI-3 | Research / harness | n/a | Wraps **Claude Opus-class** cloud models; not local weights |
| — | **PX Cap Pro** (Paxini glove) | [15:40](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=940s) | Robotics hardware | n/a | ❌ | Data-collection glove, not a Mac model |
| — | **Arc Shell MXD1** | [16:44](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1004s) | Transforming robot | n/a | ❌ | Hardware demo |
| — | **World Robot Conference demos** (Annie, UBTECH, Elf Schwan 2.0) | [17:43](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1063s) | Humanoid demos | n/a | ❌ | Conference footage |
| — | **Qiji / Chi horse** (DAX AI) | [19:13](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1153s) | Robot horse | n/a | ❌ | Hardware / product |
| — | **Humanoid games / Unitree Superman / sprinters / tennis robots** | [20:07](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1207s) | Robot sports demos | n/a | ❌ | Includes [Superman](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1235s), [sprinting](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1273s), [tennis](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=1329s) |

**Legend:** ✅ daily use · ⚠️ possible but painful / experimental · ❌ no

Sponsor chapter (**HubSpot Codex prompts**, [12:10](https://www.youtube.com/watch?v=rQ4yX5qNYdY&t=730s)) is a cloud/docs product, not a local model.

---

## Runnable / near-runnable: how it would run

### 1) Audio8-TTS Preview 0.1B — **recommended new pickup from this video**

| | |
| --- | --- |
| **Org** | Audio8 |
| **Job** | Multilingual TTS + zero-shot voice cloning from a few seconds of reference audio |
| **Size** | ~**0.17B** DualAR LM + ~**0.12B** codec decoder |
| **On-disk** | Complete preview pack ~**1.7 GB** (video figure) |
| **16 GB M2 fit** | **Yes, comfortable.** Leave Cursor/browser open without drama |
| **Mac path** | Official Transformers: `device = "mps"` or `"cpu"`. Prefer **ONNX INT4** runtime from [Audio8-AI/Audio8_TTS](https://github.com/Audio8-AI/Audio8_TTS) (`onnx_runtime/`) — vendors report ~**1 GiB** online memory on an **Apple M2**. MLX exists for the **0.6B** sibling; treat 0.1B as PyTorch-MPS / ONNX until an mlx-community 0.1B pack appears |
| **License** | Check HF card (0.1B preview; 0.6B is Apache 2.0) |

**How it runs on this Mac**

- Load once (~2 GB unified peak with codec). Pass `reference.wav` + matching transcript, then generate.
- Expect interactive short lines on M2; not cloud-API instant, but far lighter than IndexTTS 2.5’s ~5 GB MLX pack from the [Aug 16 report](./report-2026-08-16-video-ai-news.md).
- Do **not** follow CUDA-only install notes if present; force MPS/CPU.

```bash
# Transformers (MPS) — sketch from the model card pattern
python - <<'PY'
from transformers import AutoModel, AutoProcessor
import torch, soundfile as sf
model_id = "Audio8/Audio8-TTS-Preview-0.1b"
device = "mps" if torch.backends.mps.is_available() else "cpu"
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
model = AutoModel.from_pretrained(model_id, trust_remote_code=True).to(device).eval()
# see HF card for reference_audio / generate / decode_audio
PY
```

HF: [Audio8/Audio8-TTS-Preview-0.1b](https://huggingface.co/Audio8/Audio8-TTS-Preview-0.1b) · code: [Audio8-AI/Audio8_TTS](https://github.com/Audio8-AI/Audio8_TTS)

**If you want the stronger clone quality:** [Audio8/Audio8-TTS-Preview-0.6b](https://huggingface.co/Audio8/Audio8-TTS-Preview-0.6b) via [mlx-community/Audio8-TTS-Preview-0.6b-bf16](https://huggingface.co/mlx-community/Audio8-TTS-Preview-0.6b-bf16) (`mlx-audio` ≥ 0.4.7). Still well inside the 16 GB budget.

---

### 2) Ornith 1.5 9B — **the LLM that actually upgrades your daily driver**

| | |
| --- | --- |
| **Org** | ornith-ai / DeepReinforce |
| **Job** | Agentic coding / tool use; dense ~9B with optional vision projector |
| **Size** | ~8.95B language (+ ~0.46B vision) |
| **On-disk** | BF16 ~**17.9 GB** · Q8 ~**9.5 GB** · Q6 ~**7.4 GB** · Q5 ~**6.5 GB** · Q4 / AD-Q4 ~**5.2–5.9 GB** |
| **16 GB M2 fit** | **Yes** at Q4–Q6. AtomicChat’s 16 GB Mac row suggests **AD-Q8_0-Q6_K (~8.6 GB)** with ~64K context if you close heavy apps; safer daily pick is **Q4_K_M / AD-Q5_K-Q4_K** at **4K–8K** |
| **Mac path** | **llama.cpp Metal** or Ollama once a tag exists. Architecture string `qwen35` — need a **recent** llama.cpp. Optional `mmproj` (~0.9 GB) only if you want vision |
| **License** | MIT |

**How it runs on this Mac**

- Same memory class as **Ornith 1.0 9B** from [report-2026-07-17](./report-2026-07-17.md): mid tens of tok/s at Q4 is the right order of magnitude on M2 (build-dependent; slower than M3/M4).
- Self-improvement training story is interesting; local agent quality may still trail vendor tables (community gap reports exist). Treat as a **coding peer** to Ornith 1.0 / Gemma 4 12B, not Opus.
- Skip 35B and 397B on this machine entirely.

```bash
# Example: bartowski Q4_K_M via llama.cpp / llama.app
llama-server -hf bartowski/Ornith-1.5-9B-GGUF:Q4_K_M -c 8192
```

HF: [ornith-ai/Ornith-1.5-9B](https://huggingface.co/ornith-ai/Ornith-1.5-9B) · GGUF: [bartowski/Ornith-1.5-9B-GGUF](https://huggingface.co/bartowski/Ornith-1.5-9B-GGUF), [AtomicChat/Ornith-1.5-9B-GGUF](https://huggingface.co/AtomicChat/Ornith-1.5-9B-GGUF)

---

### 3) SenseNova U 1.5 — **only as a curiosity**

| | |
| --- | --- |
| **Job** | Native 4K text-to-image + natural-language edit |
| **Reality on M2** | Full BF16 is a **~40 GB** class job. Official low-VRAM path is **GGUF + layer offload** aimed at **10–12 GB NVIDIA**. Diffusers/`transformers` stack is **CUDA-first** |
| **Verdict** | Downloadable, not daily. Prefer cloud image APIs or wait for a real MLX / Comfy Metal pack. Do not expect IndexTTS-class Mac UX |

---

## Why the rest fail on this Mac

### Video / world / 3D

| Model | Local reality |
| --- | --- |
| **Evoke** | 14B few-step world model; weights ~**57 GB**; published realtime numbers are **H200**. Needs CUDA 12.4 + forked diffusers + ViGeo depth backend |
| **4D Anyone** | Character 4DGS from one video. Core weights ~12 GB but the shipped tree also carries **Wan VAE + UMT5-XXL + pose stack** — workstation GPU territory |
| **Bernini v2** | ~**180 GB** renderer lineage (Wan2.2-class). Video itself says good luck locally |
| **Qwen VideoEdit** | ~**41 GB** Wan + image-edit pipeline; high-end GPU. MiniMax H3 already ruled ❌ in prior reports |
| **Geo Weaver** | Paper / benchmarks only — nothing to download |

### Large Ornith / DeepSeek / music

| Model | Local reality |
| --- | --- |
| **Ornith 1.5 35B-A3B** | MoE with 3B active, but Q4 still ~**21 GB** of weights. Needs **24 GB+** GPU or **32 GB+** unified |
| **Ornith 1.5 397B** | Cluster. Video’s **794 GB** figure is the tell |
| **DeepSeek V4 Flash Vision** | **API-only** in this video. Even text Flash is multi-hundred-B MoE — not a laptop GGUF |
| **Happy Shrimp** | Hosted music UI. Local music on this Mac remains **ACE-Step 1.5 2B turbo** / MusicGen (see [music report](./report-2026-07-27-music.md)) |

### Tools & robots

- **Comfy MCP:** MCP server that drives *your* ComfyUI install. Without a GPU Comfy stack, nothing to drive.
- **Nvidia AO:** Harness that pushed Opus 5 to 100% on Arc-AGI-3 public set — cloud-model scaffolding.
- **Gen 1.5 / gloves / humanoids / robot horse:** Hardware and robot policies, not Metal chat checkpoints.

---

## Suggested actions on this machine

```
Want a new local tool from this video?
  └─ Audio8-TTS 0.1B (ONNX or PyTorch-MPS, ~1.7 GB)
     or Audio8-TTS 0.6B MLX if you want better clones

Want a better local coding LLM than Ornith 1.0?
  └─ Ornith 1.5 9B Q4_K_M / Q5 via llama.cpp Metal
     Keep Gemma 4 12B Unified for multimodal chat
     (see report-2026-07-17)

Want Evoke / 4D Anyone / Bernini / Qwen VideoEdit?
  └─ Cloud GPU or a 24–80 GB CUDA box. Not the M2

Want SenseNova U1.5 image gen?
  └─ Not daily on 16 GB. Use a hosted image model
     or rent ≥24 GB NVIDIA with GGUF offload

Want DeepSeek V4 Flash Vision / Happy Shrimp?
  └─ Their APIs / websites

Want Comfy MCP?
  └─ Skip until you have a real Comfy + GPU setup
```

---

## Sources

- Video: [youtu.be/rQ4yX5qNYdY](https://youtu.be/rQ4yX5qNYdY)
- Evoke: [AlayaLab/Evoke](https://github.com/AlayaLab/Evoke), [HF](https://huggingface.co/AlayaLab/Evoke), [project](https://evoke-world.github.io/Evoke/)
- 4D Anyone: [AntResearch/4DAnyone](https://huggingface.co/AntResearch/4DAnyone), arXiv:2608.20335
- SenseNova U1.5: [OpenSenseNova/SenseNova-U1](https://github.com/OpenSenseNova/SenseNova-U1), [sensenova/SenseNova-U1.5-8B-MoT](https://huggingface.co/sensenova/SenseNova-U1.5-8B-MoT)
- Bernini: [ByteDance/Bernini-R](https://huggingface.co/ByteDance/Bernini-R)
- Ornith 1.5: [ornith-ai/Ornith-1.5-9B](https://huggingface.co/ornith-ai/Ornith-1.5-9B), [AtomicChat run guide](https://atomic.chat/blog/guides/how-to-run-ornith-1-5-locally)
- Audio8-TTS: [Audio8/Audio8-TTS-Preview-0.1b](https://huggingface.co/Audio8/Audio8-TTS-Preview-0.1b), [0.6b](https://huggingface.co/Audio8/Audio8-TTS-Preview-0.6b), [mlx-community 0.6b](https://huggingface.co/mlx-community/Audio8-TTS-Preview-0.6b-bf16), [Audio8_TTS](https://github.com/Audio8-AI/Audio8_TTS)
- Prior hardware bar: [report-2026-07-17.md](./report-2026-07-17.md)

## Method / caveats

- Inventory = every named software model/tool in the video transcript, plus robotics called out as non-applicable.
- Hardware bar matches prior reports in this folder (16 GB M2 usable ~**8–11 GB**).
- File sizes from Hugging Face / AtomicChat / vendor docs / video narration as of **2026-08-23**. Packs differ by a few hundred MB.
- Tok/s and RTF figures are **order-of-magnitude / vendor-published**; this report did not re-benchmark on the M2.
- “Open weights” ≠ “runs on a laptop.” World models and Wan-class video stacks dominate this week’s releases.
