# Local Runnability: Models from AI News Video (2026-09-06)

**Compiled:** 2026-09-06  
**Source video:** [GPT 6 Astra, Claude Fable 5.1, Gemini 3.8, realtime Minimax, new world models: AI NEWS](https://www.youtube.com/watch?v=ngyFRCNq0Yc) (AI Search)  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**  
**Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**  
**Memory budget:** [Your real memory budget](./memory-budget.md)

## TL;DR

| Verdict | Models |
| --- | --- |
| **Runs well on this Mac** | **TimesFM-3** (330M; ~**1.32 GB** FP32; official PyTorch or community **MLX**) |
| **Tight / experimental** | **LLaDA-Image-Turbo FP8** (~**6.5–6.7 GB** transformer) — size OK, path is **CUDA Diffusers**; Metal/MPS unproven |
| **Open weights, not this machine** | H3-World, SolarWM (Wan-5B/14B/LTX/H3), VideoDeltaNet / VDN-H3, DeepSeek-V4-Flash-Vision-Exp (~305B / video **~168 GB**), Viggle-Animate (H3 finetune + LoRA) |
| **API / web / early access / not released** | Qwen3.8-Max-0902, Claude Fable 5.1, Gemini 3.8 Flash (+ Cyber), Muse Spark 1.3, GPT-6 Astra, Atlas (World Labs), GWM Worlds 2 (Runway), InternLumina-U2 (code; weights stub), Lucida (paper) |
| **Product / dataset / not a laptop checkpoint** | WeatherNext 3, fruit-fly connectome, Higgsfield (sponsor) |

This week’s headline is **closed frontier LLMs** (Astra / Fable / Gemini Flash / Muse Spark) plus **MiniMax-H3 world-model wrappers**. None of the H3 / LTX / Wan interactive stacks fit this Mac — same wall as [report-2026-08-30](./report-2026-08-30-video-ai-news.md) and the [LTX-2.5 deep dive](./report-2026-08-25-ltx-2.5.md). The only practical local pickup is **TimesFM-3**. Keep daily chat on Gemma 4 12B / Ornith 1.5 9B / Ling-3.0-tiny from prior reports.

---

## Runnability table (all models mentioned)

Chapter order follows the video. Timestamps are the official YouTube chapters.

| Model / item | Video | Kind | Open weights? | Fits 16 GB M2? | Notes |
| --- | --- | --- | --- | --- | --- |
| **H3-World** | [1:00](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=60s) | Keyboard → language control LoRA on MiniMax-H3 | Yes (LoRA + code) | ❌ | Needs **MiniMax-H3 base ~135 GB** + DiffSynth. Rank-32 LoRA is small; backbone is not |
| **SolarWM** | [2:02](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=122s) | Long-horizon interactive video WM framework | Yes (Apache 2.0 code + data; backbone licenses apply) | ❌ | Family: Wan-5B / 14B / LTX-2.5 / MiniMax-H3. Hour-scale demos; CUDA backends. Same H3/LTX floor as prior reports |
| **TimesFM-3** | [3:33](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=213s) | Multivariate zero-shot time-series FM (330M) | Yes (non-commercial weights) | ✅ | HF FP32 ~**1.32 GB**. Official `timesfm[torch]`; community **MLX** ports exist |
| **Lucida** | [5:03](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=303s) | Real room → editable per-object 3D assets | Paper / project page | ❌ | Parse–generate–place + GizmoAct VLM. No public laptop checkpoint in the video |
| **VideoDeltaNet / VDN-H3** | [6:07](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=367s) | Hybrid-attention speedup of MiniMax-H3 | Yes (H3 community license) | ❌ | Headline: **14.4 s @ 768p in 11.23 s on 8× B200**. Single H200 still **~51–90 s**. ComfyUI nodes are CUDA |
| **LLaDA-Image** (+ Turbo / FP8) | [8:25](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=505s) | 6B unified T2I + edit | Yes (Apache 2.0) | ⚠️ | Turbo FP8 DiT ~**6.5–6.7 GB**. Official `device="cuda"`. No productized Metal path |
| **DeepSeek-V4-Flash-Vision-Exp** | [9:56](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=596s) | Multimodal MoE (~305B) | Yes (MIT) | ❌ | Video ~**168 GB** shards. Multi-GPU / API story; was API-only in the [Aug 23 report](./report-2026-08-23-video-ai-news.md) |
| **Qwen3.8-Max-0902** | [10:38](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=638s) | Hosted 2.4T / coding post-train | No (API) | ❌ | Same architecture class as prior Max; Qwen Cloud only |
| **Claude Fable 5.1** | [11:37](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=697s) | Frontier hosted LLM | No | ❌ | Anthropic Max / API. Review video linked in description |
| **Gemini 3.8 Flash** (+ **Cyber**) | [14:41](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=881s) | Hosted multimodal / cyber variants | No | ❌ | AI Studio / Gemini app / Antigravity. Fast (~**348 tok/s** claimed), not local |
| **Muse Spark 1.3** | [18:28](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1108s) | Meta agentic coding model | No | ❌ | Muse Code + Meta Model API |
| **GPT-6 Astra** | [19:38](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1178s) | Frontier hosted agent / computer-use | No | ❌ | Plus/Pro rollout; free tier out. Not weights |
| **WeatherNext 3** | [24:50](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1490s) | Weather forecast system | No public laptop weights | ❌ | Search / Maps / Gemini / Earth Engine / API |
| **Male fruit-fly connectome** | [26:28](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1588s) | Full CNS wiring map | Research data | n/a | ~166k neurons / ~125M synapses — biology dataset, not an LLM |
| **Atlas** (World Labs) | [28:40](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1720s) | Multimodal → 3D world / camera path | Early access form | ❌ | Preview; not a downloadable Mac checkpoint |
| **InternLumina-U2** | [30:15](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1815s) | Unified understand + gen + edit (dLLM) | Code yes; **weights stub** | ❌ today | ~**16B-A1B** class when weights land; HF empty at compile time |
| **Viggle-Animate** | [31:44](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1904s) | Single-frame character swap on H3 ref2va | Yes (H3 license) | ❌ | Full finetune **~66 GB** + **2.5 GB** LoRA; needs base H3 VAEs. Peak **~80+ GiB** bf16; offload still CUDA |
| **GWM Worlds 2** (Runway) | [33:00](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=1980s) | Realtime interactive world (720p24) | Research preview form | ❌ | Autoregressive video+audio; not public |
| **Higgsfield** (sponsor) | [12:58](https://www.youtube.com/watch?v=ngyFRCNq0Yc&t=778s) | Cloud creative suite | n/a | ❌ | Hosted Seedance / GPT Image / studios |

**Legend:** ✅ daily use · ⚠️ possible but painful / experimental · ❌ no

---

## Runnable / near-runnable: how it would run

### 1) TimesFM-3 — **the only practical pickup from this video**

| | |
| --- | --- |
| **Org** | Google Research |
| **Job** | Zero-shot **multivariate** time-series forecasting (targets + past / past-future covariates); full horizon in one pass; 9 quantiles |
| **Size** | **330M** params |
| **On-disk** | [`google/timesfm-3.0-pytorch`](https://huggingface.co/google/timesfm-3.0-pytorch) FP32 ~**1.32 GB** (`model.safetensors`) |
| **16 GB M2 fit** | **Yes, comfortable.** Leaves headroom for Cursor + browser |
| **Mac path** | Official: `pip install timesfm[torch]` then `device="cpu"` or MPS if your torch build supports it. Prefer community **MLX**: [`hskyto-timesfm-mlx`](https://pypi.org/project/hskyto-timesfm-mlx/) or [`mlx-timesfm`](https://pypi.org/project/mlx-timesfm/) (no PyTorch) |
| **License** | Inference code Apache-ish / package terms; **weights = TimesFM non-commercial** (`timesfm-non-commercial-license-v1.0`). For commercial ship, TimesFM **2.5** remains the Apache option |

**How it runs on this Mac**

- Accept the HF license, download once, forecast locally. Multivariate + covariates are the upgrade over 2.5.
- Do **not** expect stock-chart magic without checking the non-commercial terms.
- This is a **specialist**, not a chat replacement. Keep Gemma / Ornith / Ling for general work.

```bash
# Official PyTorch (CPU/MPS)
pip install "timesfm[torch]"
# then load google/timesfm-3.0-pytorch per google-research/timesfm docs

# Or pure MLX on Apple Silicon
pip install hskyto-timesfm-mlx
# weights auto-fetch from google/timesfm-3.0-pytorch on first use
```

Blog: [TimesFM-3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/) · code: [google-research/timesfm](https://github.com/google-research/timesfm)

---

### 2) LLaDA-Image-Turbo FP8 — **only if you insist on local images; not daily**

| | |
| --- | --- |
| **Org** | inclusionAI / Ant Group |
| **Job** | Unified **text-to-image + instruction edit** (posters, photoreal, bilingual text); Turbo = **4 steps** |
| **Size** | **~6B** DiT family; Turbo FP8 safetensors param count ~**6.54B** |
| **On-disk (transformer)** | Video / card: Turbo FP8 ~**6.7 GB** |
| **16 GB M2 fit** | **Borderline on paper, no on practice.** Weight file clears the ≤8 GB prefer-line, but official pipeline is **`device="cuda"`** Diffusers; activations + VAE + any VQ path (LLaDA2) push past comfortable unified use. No MLX / Metal pack at compile time |
| **Mac path** | Curiosity only (PyTorch-MPS hack). Prefer hosted image models, or the prior week’s **Fibo 1.5 mflux q4** experiment if you already tried that stack |
| **License** | Apache 2.0 |

**How it would feel**

- Close everything, load Turbo FP8 only, skip VQ mode if that pulls another LLM.
- Expect thrashing or OOM once decode / editing buffers spike — same class of “file size lies about peak RSS” as Fibo in [report-2026-08-30](./report-2026-08-30-video-ai-news.md).
- Do not follow the CUDA quickstart hoping MPS is drop-in.

Repo: [inclusionAI/LLaDA-Image](https://github.com/inclusionAI/LLaDA-Image) · Turbo FP8: [inclusionAI/LLaDA-Image-Turbo-FP8](https://huggingface.co/inclusionAI/LLaDA-Image-Turbo-FP8)

---

## Why the rest fail on this Mac

### MiniMax-H3 ecosystem (most of the open “wow” this week)

| Model | Local reality |
| --- | --- |
| **H3-World** | LoRA teaches keyboard→English control on H3. Inference still loads **full MiniMax-H3** (~**135 GB** base per project table). DiffSynth / CUDA |
| **SolarWM** | Excellent open **data + recipe** story (1.43M clips / 25 TB). Instantiated on Wan-5B, Wan-14B, LTX-2.5, H3 — all previously ❌ or painful on this M2. Realtime hour-scale interaction is a **datacenter / high-VRAM** demo |
| **VDN-H3** | Hybrid linear+softmax attention + 8-step distill. Faster H3, **not smaller** H3. ComfyUI-VDN-H3 is NVIDIA. Prior FastH3 MLX needed **~36 GB** Apple Silicon |
| **Viggle-Animate** | Character swap from one edited frame. **33B** finetuned transformer (~**66 GB**) + **2.5 GB** LoRA + base H3 VAEs. Card: **96 GB+** or heavy offload |

Same conclusion as [FastH3 / MiniMax H3 in the Aug 30 report](./report-2026-08-30-video-ai-news.md): interactive H3 on this laptop is a non-starter.

### Frontier open / hosted LLMs

| Model | Local reality |
| --- | --- |
| **DeepSeek-V4-Flash-Vision-Exp** | Now **open (MIT)** — still ~**305B** / video **~168 GB**. Multi-GPU serve (vLLM / SGLang). Use the API if you want vision Flash |
| **Qwen3.8-Max-0902** | Post-train bump for coding / co-work. **API only**; 2.4T class never was a 16 GB target |
| **Claude Fable 5.1 / Gemini 3.8 Flash / Muse Spark 1.3 / GPT-6 Astra** | Closed. Astra’s computer-use demos are the product; not a GGUF |

### Research / preview / non-weights

- **Lucida:** ByteDance real-to-sim paper + project page; no Mac install path in the roundup.
- **InternLumina-U2:** Inference harness public; **weights “coming soon.”** Even at 16B-A1B, wait for a real quant pack before revisiting.
- **Atlas / GWM Worlds 2:** Early-access forms (World Labs / Runway).
- **WeatherNext 3 / fruit-fly map:** Google products and connectomics — interesting, not local models.
- **Higgsfield:** Sponsor cloud suite.

---

## Suggested actions on this machine

```
Want something new from this video that actually fits?
  └─ TimesFM-3 (multivariate forecasting, ~1.3 GB)
     Prefer MLX port on Apple Silicon; respect non-commercial weight license
     Keep chat on Gemma 4 12B / Ornith 1.5 9B / Ling-3.0-tiny
     (see report-2026-08-31)

Want LLaDA-Image locally?
  └─ Only as a CUDA-box / MPS experiment (Turbo FP8 ~6.7 GB DiT).
     Not a daily Metal workflow. Prefer hosted T2I, or prior Fibo mflux try.

Want H3-World / SolarWM / VDN-H3 / Viggle interactive video?
  └─ Need MiniMax-H3-class GPU (or 36 GB+ Apple Silicon for FastH3-class ports).
     This M2 still has no daily local video (see LTX-2.5 report).

Want DeepSeek V4 Flash Vision / Qwen Max 0902 intelligence?
  └─ Their APIs. Local Vision-Exp is multi-hundred-GB.

Want Astra / Fable / Gemini 3.8 / Muse Spark?
  └─ Hosted only. Not software for this laptop.

Want Atlas / GWM 2 / Lucida / InternLumina-U2?
  └─ Wait for access or weights. Not runnable here today.
```

---

## Sources

- Video: [YouTube](https://www.youtube.com/watch?v=ngyFRCNq0Yc)
- H3-World: [project page](https://danzer1xxxxchan.github.io/H3-World/), [GitHub](https://github.com/Danzer1xxxxChan/H3-World), arXiv:2609.01560
- SolarWM: [project page](https://junchao-cs.github.io/SolarWM-Web/), [GitHub](https://github.com/Junchao-cs/SolarWM), [Hugging Face](https://huggingface.co/junchaoh-cs/SolarWM), arXiv:2609.02886
- TimesFM-3: [Google blog](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/), [Hugging Face](https://huggingface.co/google/timesfm-3.0-pytorch), [GitHub](https://github.com/google-research/timesfm)
- Lucida: [project page](https://lucida-r2s.github.io/), arXiv:2608.30821
- VideoDeltaNet / VDN-H3: [project page](https://openvdn.github.io/), [Hugging Face](https://huggingface.co/OpenVDN/vdn-minimax-h3), [ComfyUI nodes](https://github.com/Saganaki22/ComfyUI-VDN-H3)
- LLaDA-Image: [GitHub](https://github.com/inclusionAI/LLaDA-Image), [Hugging Face (Turbo FP8)](https://huggingface.co/inclusionAI/LLaDA-Image-Turbo-FP8)
- DeepSeek-V4-Flash-Vision-Exp: [Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp)
- Qwen3.8-Max-0902: [Qwen Cloud](https://www.qwencloud.com/models/qwen3.8-max-0902)
- Gemini 3.8 Flash: [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)
- GPT-6 Astra: [OpenAI announcement](https://openai.com/index/gpt-6-astra/)
- WeatherNext 3: [DeepMind blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3)
- Fly connectome: [Google Research blog](https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain)
- Atlas: [World Labs blog](https://www.worldlabs.ai/blog/atlas)
- InternLumina-U2: [project page](https://internlm.github.io/InternLumina-U2/)
- Viggle-Animate: [Hugging Face](https://huggingface.co/Viggle/Viggle-Animate)
- GWM Worlds 2: [Runway research](https://runway.com/research/introducing-gwm-worlds-2)
- Prior hardware bar: [report-2026-07-17](./report-2026-07-17.md), [memory budget](./memory-budget.md)

## Method / caveats

- Inventory = every named software model/tool in the video chapters/description, plus sponsor/hardware/biology called out as non-applicable. ASR names (Miniax, Quen, Lada image, Vigle, GLM Worlds) map to **MiniMax**, **Qwen**, **LLaDA-Image**, **Viggle**, **GWM Worlds 2**.
- Hardware bar: [memory-budget.md](./memory-budget.md).
- File sizes from Hugging Face safetensors metadata / project pages / video narration as of **2026-09-06**. Packs differ by a few hundred MB.
- Tok/s, RTF, and vendor speedups (8× B200 realtime VDN, ARC-AGI harness scores, etc.) are **published / video figures**, not re-benchmarked on this M2.
- “Open weights” ≠ “runs on a laptop.” This week’s open video stack is still H3/LTX/Wan; the runnable exception is a **330M time-series** model.
