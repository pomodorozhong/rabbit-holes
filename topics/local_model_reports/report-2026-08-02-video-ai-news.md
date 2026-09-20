# Local Runnability: Models from AI News Video (2026-08-02)

**Compiled:** 2026-08-02  
**Source video:** [New Deepseek, Seedance 2.5, Minimax H3, Gemini Robotics, AMD models: AI NEWS](https://youtu.be/OrcBSpADCGk)  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory** (same machine as [report-2026-07-17](./report-2026-07-17.md) and [report-2026-07-27-music](./report-2026-07-27-music.md))  
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
| **Runs well on this Mac** | **CrisperWhisper 2.0** (small → large; prefer turbo/medium) |
| **Tight / experimental** | **AMD Instella-MoE-16B-A3B** at **Q2–Q3** only (community GGUF + non-mainline llama.cpp) |
| **Open weights, not this machine** | DeepSeek-V4-Flash-0731, Kimi K3, Inkling-Small |
| **Weights promised / not out** | MiniMax H3, Wonder, PhiZero (code “coming soon”) |
| **Closed / cloud / gated** | Seedance 2.5, Gemini Robotics family, Ideogram Object Remover, Higgsfield, Gemini voice typing |
| **Research method, not a consumer local model** | ID-V2V, ReDesign, PRISM |

Of everything named in the video, only **CrisperWhisper** is a practical daily driver on a 16 GB M2. **Instella** is the only other open LLM that *might* load if you accept heavy quantization and a special llama.cpp branch.

---

## Runnability table (all models mentioned)

Chapter order follows the video ([AI Search / Wealth Health Self mirror](https://wealthhealthself.com/new-deepseek-seedance-2-5-minimax-h3-gemini-robotics-amd-models-ai-news/)).

| # | Model / item | Kind | Open weights? | Fits 16 GB M2? | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | **ID-V2V** | Identity-preserving video restyle (SIGGRAPH Asia 2026) | No public weights found | ❌ | Project page only; production research demo |
| 2 | **CrisperWhisper 2.0** | Verbatim ASR (Whisper-family) | Yes (non-commercial research license on standard weights) | ✅ | Small→large all fit; best pick in this video |
| 3 | **DeepSeek-V4-Flash-0731** | MoE LLM (284B / 13B active) | Yes (HF) | ❌ | Needs multi-H100 class VRAM; not laptop-local |
| 4 | **ReDesign** | ECCV 2026 research repo | No usable release (empty README as of compile date) | ❌ | Not a packaged local model |
| 5 | **Kimi K3** | MoE multimodal LLM (2.8T / 104B active) | Yes | ❌ | Full ~1.5 TB; pruned MLX still hundreds of GB |
| 6 | **AMD Instella-MoE-16B-A3B** | MoE LLM (16B / 2.8B active) | Yes (ResearchRAIL) | ⚠️ Q2–Q3 only | Q4_K_M ~10.5 GB weights → fragile on 16 GB |
| 7 | **Ideogram Object Remover** | Hosted image edit app | No | ❌ | Cloud product |
| 8 | **Higgsfield** | Hosted creative AI (video sponsor) | No | ❌ | Cloud product |
| 9 | **Inkling-Small** | Multimodal MoE (276B / 12B active) | Yes | ❌ | BF16 ~600 GB agg. VRAM; NVFP4 ≥~180 GB |
| 10 | **PRISM** | Motor-control representation (robotics) | Method paper / site; not a chat checkpoint | ❌ | Policy add-on for RL/IL, not a Mac LLM |
| 11 | **Seedance 2.5** | Video generation (ByteDance) | Closed | ❌ | API / Doubao only; no self-host |
| 12 | **MiniMax H3** | Omni video (text/image/audio/video → 2K A/V) | Promised “in coming days”; **not downloadable yet** | ❌ today | Even after release, video DiTs are unlikely to be comfortable on 16 GB |
| 13 | **Gemini Robotics 2** | VLA whole-body control | Early-access partners | ❌ | Not public download |
| 13b | **Gemini Robotics ER 2** | Embodied reasoning VLM | API / AI Studio preview | ❌ | Cloud; not local weights |
| 13c | **Gemini Robotics On-Device 2** | On-robot VLA | Trusted testers only | ❌ | “Local” means robot hardware, not your Mac |
| 14 | **Wonder** | Interactive video world model | Code / HF “coming soon” | ❌ today | Targets GPU rollouts (16 FPS claims); not Mac-packaged |
| 15 | **Gemini voice typing** | Gemini app feature on macOS | N/A (product feature) | ❌ as local model | Uses Google’s cloud Gemini, not a downloadable checkpoint |
| 16 | **PhiZero** | Physical-language world model | Preprint; code/weights not released | ❌ | Built on Wan2.2 VAE/decoder + Qwen3-VL-4B reasoner — heavy even if opened |

**Legend:** ✅ daily use · ⚠️ possible but painful / experimental · ❌ no

---

## Runnable / near-runnable: performance details

### 1) CrisperWhisper 2.0 — **recommended**

| | |
| --- | --- |
| **Org** | Nyra Labs |
| **Job** | Speech → text with **verbatim vs intended** control, word-level timestamps, longform |
| **Sizes** | `small` · `medium` · `turbo` · `large` (+ commercial-only Pro variants) |
| **Approx. FP16 footprint** | small ~**0.5 GB** · turbo ~**1.6 GB** · medium ~**3.1 GB** · large ~**6.7 GB** (GGML community builds) |
| **16 GB M2 fit** | **All sizes yes**. Prefer **turbo** or **medium** with apps open; **large** OK if you close heavy apps |
| **Mac path** | Official: `pip install "crisperwhisper[transformers]"` (PyTorch / MPS). Fastest stack is NVIDIA CTranslate2; on Mac use transformers backend or community MLX/GGML ports |
| **License** | Inference code MIT; **standard weights = non-commercial research**; Pro = commercial only |

**Quality / performance (vendor benchmarks, not re-run here):**

| Metric | CrisperWhisper 2.0 | Context |
| --- | --- | --- |
| Disfluency F1 (10-lang avg, nyra verbatim bench) | **87.8** | Beats ElevenLabs Scribe v2 (79.2), Microsoft MAI-Transcribe-1.5 (77.5); Pro reaches **93.5** |
| Word-boundary MAE · TIMIT (read) | **29.6 ms** | Best among systems they reported |
| Word-boundary MAE · Buckeye (conversational) | **40.6 ms** | Best among systems they reported |
| Rare-word recall w/ Verbatimize | **96.1%** (claimed) | Reconstructs fillers/sounds onto clean transcripts |
| Longform | Conditional continuation (no Whisper timestamp-token stitching) | Better seam behavior than naïve chunking |

**Practical Mac picks**

| Role | Size | Why |
| --- | --- | --- |
| Daily meetings / notes | **turbo** | Near-large quality, smallest “large-class” decoder |
| Best open quality on laptop | **large** | Fits; expect slower than turbo on M2 |
| Always-on / low memory | **small** or **medium** | Leaves RAM for IDE + browser |

**Install sketch**

```bash
pip install "crisperwhisper[transformers]"
python - <<'PY'
from crisperwhisper import CrisperWhisperModel
model = CrisperWhisperModel("turbo")  # or "medium" / "large" / "small"
print(model.transcribe("meeting.wav", language="en"))
PY
```

HF: [nyralabs/CrisperWhisper2.0_large](https://huggingface.co/nyralabs/CrisperWhisper2.0_large) · docs: [nyra-labs.com/crisperwhisper](https://www.nyra-labs.com/crisperwhisper) · code: [nyrahealth/CrisperWhisper](https://github.com/nyrahealth/CrisperWhisper)

---

### 2) AMD Instella-MoE-16B-A3B — **experimental on 16 GB**

| | |
| --- | --- |
| **Org** | AMD AGI |
| **Job** | Fully open MoE chat / think LLM |
| **Size** | **16B total**, **2.8B active**/token (2 shared + 6 of 64 routed experts) |
| **Arch extras** | Gated MLA, FarSkip-Collective, MTP during pre/mid-train |
| **Context (trained)** | Extended to **64K** at Base stage |
| **License** | Weights: **ResearchRAIL** (research; not general commercial). Training code MIT |
| **Official runtime** | Transformers / **SGLang** (AMD Instinct / ROCm story) |
| **Mac path** | Community GGUF only so far: [DevQuasar GGUF](https://huggingface.co/DevQuasar/amd.Instella-MoE-16B-A3B-Think-GGUF) + [llama.cpp `instella-moe` branch](https://github.com/csabakecskemeti/llama.cpp/tree/instella-moe) — **not** mainline Ollama/LM Studio yet |

**Quant footprint vs this Mac**

| Quant | On-disk | 16 GB M2 verdict |
| --- | ---: | --- |
| Q2_K | **6.51 GB** | ⚠️ Possible; expect quality loss |
| Q3_K_M | **8.22 GB** | ⚠️ Best “try it” tier; short context only |
| Q4_K_M | **10.5 GB** | ❌ / fragile (swap risk) |
| Q5_K_M | **12.0 GB** | ❌ |
| Q6_K / Q8_0 | 14–17 GB | ❌ |

Active-param count (2.8B) helps **decode bandwidth** vs a dense 16B, but you still must **resident-load all experts** — so disk size, not active params, is the RAM gate.

**Published quality (vendor / MarkTechPost summary of AMD tables)**

| Checkpoint | Highlight |
| --- | --- |
| **Base** | Avg **76.7** on AMD’s fully-open comparison set; WinoGrande **86.5**; HumanEval+ **65.7**; HELMET **41.5** / RULER **79.4** (long-context) |
| **Think** (post-train avg) | **73.22** — ahead of Olmo3-7B-Think (71.97), Gemma-4-E4B think (70.47), Qwen3.5-4B (69.73) |
| **IFEval** (Think) | **83.70** (up from 77.08 at DPO) |
| **AIME25 / AGIEval** (Think) | **73.40** / **82.50** (reported) |

**Systems notes from AMD:** FarSkip-Collective ≈ **12.7%** faster pretrain; expert-parallel SGLang ≈ **39.2%** lower TTFT — both are **cluster/ROCm** wins, not Metal wins.

**Bottom line for this Mac:** Worth a curiosity pull at **Q3_K_M** if you build the special llama.cpp branch. Not a replacement for your current 9–12B Metal daily drivers ([Gemma 4 12B / Ornith 9B](./report-2026-07-17.md)) until mainline + MLX support exists.

Official: [ROCm blog](https://rocm.blogs.amd.com/artificial-intelligence/instella-moe/README.html) · [amd/Instella-MoE-16B-A3B-Think](https://huggingface.co/amd/Instella-MoE-16B-A3B-Think)

---

## Why the headline models don’t run here

### DeepSeek-V4-Flash-0731

- **284B / 13B active**, 1M context class; official local recipes assume **multi-GPU H100** (FP8 ~ hundreds of GB).
- Open weights on HF; agent scores jumped hard vs preview (e.g. Terminal Bench 2.1 **82.7**, NL2Repo **54.2** on DeepSeek’s table) — irrelevant if it cannot load.
- Use API (`deepseek-v4-flash`) if you need the model; not a local laptop target.

### Kimi K3

- **2.8T / 104B active**, MXFP4 native multimodal, 1M context.
- Unpruned MLX ~**1.5 TB**; hardest REAP-pruned MLX builds still **~350 GB** and need **512 GB** Apple Silicon.
- Open and impressive; wrong machine class entirely.

### Inkling-Small

- **276B / 12B active**, text + image + audio, 1M context.
- NVFP4 still wants **≥ ~180 GB** aggregate VRAM.
- “Small” is relative to full Inkling, not to a 16 GB Mac.

### Seedance 2.5 / MiniMax H3

- **Seedance 2.5:** closed; 30 s clips, rich multimodal refs — cloud only.
- **MiniMax H3:** open-weights *promised*; as of 2026-08-02 no public H3 checkpoint. API/Hailuo today. When weights land, expect a **video DiT** footprint far above laptop ASR/LLM quants unless they ship a tiny distilled edge build (not announced).

### Gemini Robotics family

| Variant | Access | Local on Mac? |
| --- | --- | --- |
| Gemini Robotics 2 (VLA) | Early-access partners | No |
| Gemini Robotics ER 2 | AI Studio / API preview | Cloud only |
| On-Device 2 | Trusted testers + robot SDK | Runs on **robot** compute, not your laptop |

### World models & others

- **Wonder / PhiZero:** research demos; weights/code not generally available; both imply heavy video diffusion stacks (PhiZero explicitly uses Wan2.2-5B-class decoder pieces).
- **ID-V2V / ReDesign / PRISM:** papers or incomplete repos — not installable consumer models.
- **Ideogram Object Remover / Higgsfield / Gemini voice typing:** products or app features, not local checkpoints.

---

## Suggested actions on this machine

```
Need better local ASR from this video?
  └─ CrisperWhisper 2.0 turbo (or medium)

Want to poke at AMD’s new open MoE?
  └─ Instella-MoE Think Q3_K_M via instella-moe llama.cpp branch
     (curiosity only; keep Gemma/Ornith for real work)

Want DeepSeek / Kimi / Inkling quality?
  └─ Use their APIs or a rented multi-GPU box — not the M2

Want Seedance / H3 / Gemini Robotics video-or-robot features?
  └─ Official cloud or partner access; nothing to download for the Mac
```

---

## Sources

- Video: [youtu.be/OrcBSpADCGk](https://youtu.be/OrcBSpADCGk) · chapter/link mirror: [Wealth Health Self](https://wealthhealthself.com/new-deepseek-seedance-2-5-minimax-h3-gemini-robotics-amd-models-ai-news/)
- CrisperWhisper: [nyra-labs.com/crisperwhisper](https://www.nyra-labs.com/crisperwhisper), [GitHub](https://github.com/nyrahealth/CrisperWhisper), [GGML sizes](https://huggingface.co/drbaph/CrisperWhisper2.0-GGML)
- DeepSeek-V4-Flash-0731: [HF model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731)
- Kimi K3: [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3), [PipeNetwork MLX reality check](https://github.com/PipeNetwork/kimi-k3-mlx)
- Instella: [ROCm blog](https://rocm.blogs.amd.com/artificial-intelligence/instella-moe/README.html), [Think weights](https://huggingface.co/amd/Instella-MoE-16B-A3B-Think), [DevQuasar GGUF](https://huggingface.co/DevQuasar/amd.Instella-MoE-16B-A3B-Think-GGUF)
- Inkling-Small: [thinkingmachines.ai model card](https://thinkingmachines.ai/model-card/inkling-small/)
- Seedance 2.5 / MiniMax H3 / Gemini Robotics 2 / Wonder / PhiZero / ID-V2V / PRISM: linked project pages from the video description

## Method / caveats

- Inventory = every named model/tool in the video chapters, not only the title five.
- Hardware bar matches prior reports in this folder (16 GB M2 usable ~8–11 GB).
- Performance numbers for CrisperWhisper and Instella are **vendor-published**; this report did not re-benchmark on the M2.
- “Open weights” ≠ “runs on a laptop.” MoE active-param marketing still requires loading the full expert set unless a pruned/distilled build exists.
- MiniMax H3 / Wonder / PhiZero status is time-sensitive — recheck HF if reading this weeks later.
