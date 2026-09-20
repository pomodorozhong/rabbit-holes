# Local Runnability: Models from AI News Video (2026-09-13)

**Compiled:** 2026-09-13\
**Source video:** [New Deepseek, human genome map, Navier Stokes, GPT finance, Suno v6, YuE2: AI NEWS](https://www.youtube.com/watch?v=nZYJdwM-_nI) (AI Search, 38:53)\
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**\
**Stack assumption:** Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**\
**Memory budget:** [Your real memory budget](./memory-budget.md)

## TL;DR

| Verdict | Models |
| --- | --- |
| **Runs well on this Mac** | **MiniCPM5-2B** (official **1.42 GB MLX 4-bit** / **1.56 GB GGUF Q4**) and **Edge0-8B** (~**4.2 GB** on disk, Apple-native MLX + SSD expert streaming) |
| **Tight / experimental** | **Edge0-35B** (~**23 GB** on disk, ~**2.9 GiB active MLX memory** at short context) — designed for Apple Silicon, but published speed/memory tests used an **M4 Pro with 24 GB**, not this M2/16 GB |
| **Open weights, not this machine** | Marigold V2, LingBot-World-v2, Isaac 0.5, WorldSculpt, Fire3D, AuK / AuK-Flash, DeepSeek-V4.1-Flash, YuE2 |
| **Framework / research / release incomplete** | UniMate, AlphaGenome Atlas, Navier–Stokes research system, Show-Harness, RealSWE, UMR, UnifoLM-WLA-1.0 |
| **Hosted product, not local weights** | Higgsfield (sponsor), Suno v6, ChatGPT for financial services |

This is a better local week than the previous roundup. **MiniCPM5-2B** is a straightforward small-model install with first-party MLX, GGUF, Ollama, and LM Studio paths. **Edge0-8B** is the more interesting systems release: it keeps MoE experts on SSD and streams only the active experts through MLX, making an 8B-class sparse model practical in unusually little active memory. Start with MiniCPM for reliability; try Edge0-8B if the SSD-streaming architecture is the point of the experiment.

The rest demonstrate why **“open weights” is not the same as “16 GB Mac software.”** Their official runtimes range from 17–29 GB GPU memory to four/eight GPUs, 80–96 GB accelerators, or CUDA-only robot stacks.

---

## Runnability table (all chapters)

Chapter order follows the video's official YouTube chapters.

| Model / item | Video | Kind | Open weights? | Fits 16 GB M2? | Local reality |
| --- | --- | --- | --- | --- | --- |
| **Marigold V2** | [1:03](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=63s) | Single-step depth, see-through depth, normals, and albedo predictors | Yes (LoRA adapters; base license also applies) | ❌ | Quantized Qwen-Image-Edit base + adapters. Official floor is **~17 GB GPU memory at 1024²**, **~29 GB at 2048²** |
| **UniMate** | [2:27](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=147s) | Text + rigged 3D asset → skeleton-aware animation | Code yes; checkpoints pending | ❌ today | MIT code and UniML3D recipe are public; pretrained checkpoints are still marked **TODO** |
| **AlphaGenome Atlas** | [3:37](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=217s) | Variant-effect catalogue over all 9B possible single-nucleotide substitutions | Database / web portal | n/a | Roughly **1 PB** of predictions. A scientific data product, not a downloadable laptop model |
| **LingBot-World-v2** | [5:30](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=330s) | Interactive long-horizon world/video model | Yes (non-commercial) | ❌ | Official inference: **14B on 8 GPUs**; even the **1.3B DiT uses 4 GPUs** and borrows T5/VAE/tokenizer assets from the 14B release |
| **Isaac 0.5** | [7:01](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=421s) | Multimodal robot-learning and control model | Yes | ❌ | **36B sparse** Qwen-family VLM plus Flow/diffusion action stack. Custom LeRobot/CUDA deployment; a clean checkout still lacks separately maintained runtime pieces |
| **WorldSculpt** | [8:27](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=507s) | Images + masks + 3D boxes → editable compositional meshes | Yes | ❌ | TRELLIS.2 / Pixal3D pipeline with CUDA-specific NATTEN setup; no Metal path |
| **Fire3D** | [9:32](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=572s) | Feed-forward scene decomposition into complete textured 3D assets | Yes | ❌ | Reference stack is Linux, CUDA 12.8, custom CUDA extensions, and Blender; project tests cite **80–96 GB GPU** class hardware |
| **AuK / AuK-Flash** | [10:30](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=630s) | Unified speech generation, editing, enhancement, and separation | Yes | ❌ | 1.5B DiT is only part of the stack: it also loads Qwen2.5-Omni-3B + VAE. Official A800 peak is **~24.8–25.0 GiB**, or **~16.75–16.98 GiB with CUDA-only CPU offload** |
| **Higgsfield** (sponsor) | [14:52](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=892s) | Cloud creative suite | No local pack | ❌ | Hosted generation product |
| **DeepSeek-V4.1-Flash** | [16:11](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=971s) | Multimodal long-context MoE | Yes (MIT) | ❌ | **552B backbone**, 8B active at prefill / 16B at decode, plus large conditional memory. Sparse activation lowers compute, not the hundreds-of-GB storage requirement |
| **Navier–Stokes research system** | [19:20](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1160s) | AI-assisted mathematical research result | No released model | ❌ | The chapter discusses an internal research system and its result, not downloadable weights or a consumer runtime |
| **Show-Harness** | [23:00](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1380s) | Semantic-action-unit harness for embodied VLM agents | Code + small LoRA adapters | ⚠️ pieces only | Some Qwen adapters are only ~87–346 MB and 0.8B/2B bases fit; the supported harness is vLLM plus robot/simulator infrastructure, with no ready MLX workflow |
| **Edge0** | [24:28](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1468s) | MLX MoE inference with SSD expert streaming | Yes (Apache 2.0) | ✅ 8B / ⚠️ 35B | **The local highlight.** Ships complete 4-bit 8B-A1B (~4.2 GB) and 35B-A3B (~23 GB) packs for M1–M4 Macs |
| **RealSWE** | [26:17](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1577s) | Realistic software-engineering benchmark | Paper / benchmark | n/a | 381 multi-variant task families; evaluates agents rather than providing a new base model |
| **Suno v6** | [27:42](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1662s) | Music generation and editing product | No | ❌ | Hosted v6 / v6-wild / v6-mini product; no weights |
| **YuE2-3B** | [29:54](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=1794s) | Long-form music generation, covers, and score-guided editing | Yes (non-commercial) | ❌ | Official runtime asks for **Linux + 24 GB NVIDIA GPU + 24 GB host RAM**; RTX 4090 peak reaches **~14.1 GiB** at maximum context before macOS overhead |
| **ChatGPT for financial services** | [33:32](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=2012s) | Hosted finance workflows and connected-data product | No | ❌ | A ChatGPT / Codex product workflow, not an open checkpoint |
| **UMR** | [34:22](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=2062s) | Unified motion retargeting across humanoid bodies | Research code / web studio | n/a | Robot motion-transfer pipeline, not a general-purpose local model; deployment still assumes robotics/simulation assets |
| **UnifoLM-WLA-1.0** | [35:35](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=2135s) | 6B humanoid-robot foundation model | Release plan; WLA base pending | ❌ today | Announcement covers a 6B model trained on ~2,500 robot hours / 64 tasks, but the repo currently links only the ER component weights; WLA code/base remain unchecked roadmap items |
| **MiniCPM5-2B** | [37:11](https://www.youtube.com/watch?v=nZYJdwM-_nI&t=2231s) | Compact dense text LLM for local assistants, code, tools, and reasoning | Yes (Apache 2.0) | ✅ | Official **MLX 4-bit**, GGUF, Ollama, LM Studio, and llama.cpp packs. The easy recommendation for this Mac |

**Legend:** ✅ comfortable local use · ⚠️ possible but experimental / incomplete · ❌ no · n/a not a local checkpoint

---

## Runnable: what to install

### 1) MiniCPM5-2B — the safe recommendation

| | |
| --- | --- |
| **Job** | Small local assistant, coding helper, reasoning model, and tool-use base |
| **Architecture** | Dense `LlamaForCausalLM`; **2,516,756,480 parameters**, 42 layers, GQA (16 query / 2 KV heads), advertised **131,072-token** maximum context |
| **Official Mac artifact** | [`openbmb/MiniCPM5-2B-MLX`](https://huggingface.co/openbmb/MiniCPM5-2B-MLX), 4-bit `model.safetensors` = **1,416,035,216 bytes (~1.42 GB)** |
| **Official GGUFs** | F16 **5.04 GB**, Q8_0 **2.68 GB**, Q4_K_M **1.56 GB** |
| **16 GB M2 fit** | **Comfortable.** The 4-bit model leaves ample room for macOS, a browser, and an editor. Long-context KV memory still grows with tokens; use 8k–32k unless 131k is genuinely needed |
| **Best path** | First-party **MLX** recipe (`mlx-lm >= 0.31`) or Q4_K_M in llama.cpp / Ollama / LM Studio |
| **License** | Apache 2.0 |

The publisher positions it as 2B-class state of the art and reports unusually strong code/math/agent scores. Treat those as **vendor benchmark results**, not proof that a 2B model replaces Gemma 4 12B or Ornith 1.5 9B. Its value is the tiny footprint and broad first-party runtime support.

```bash
# Apple-native MLX (official path)
pip install "mlx-lm>=0.31"
mlx_lm.generate --model openbmb/MiniCPM5-2B-MLX \
  --prompt $'<|im_start|>user\nExplain GQA in one sentence.<|im_end|>\n<|im_start|>assistant\n' \
  --max-tokens 200 --temp 1.0 --top-p 0.95

# Or download the smallest official GGUF for llama.cpp / LM Studio / Ollama
huggingface-cli download openbmb/MiniCPM5-2B-GGUF \
  MiniCPM5-2B-Q4_K_M.gguf --local-dir ./minicpm5
```

Official guides: [MLX](https://github.com/OpenBMB/MiniCPM/blob/main/docs/deployment/mlx.md) · [llama.cpp](https://github.com/OpenBMB/MiniCPM/blob/main/docs/deployment/llama_cpp.md)

---

### 2) Edge0-8B — the interesting Apple-native experiment

| | |
| --- | --- |
| **Job** | General text generation through an OpenAI-compatible local server |
| **Architecture** | Ling 3.0 hybrid MoE; ~**7.9B total / 1.2B active**, 128 routed experts, 4-bit expert weights |
| **On disk** | [`Edge0/Edge0-8B-A1B-preview`](https://huggingface.co/Edge0/Edge0-8B-A1B-preview), ~**4.2 GB**, including Recover-LoRA and prerouter heads |
| **Memory design** | Expert tensors are memory-mapped from SSD and fetched on demand. Published MLX allocator peak: **~1.0 GiB** at short context; **~3.3 GiB** at a 3.3k-token context |
| **Published speed** | **23.9–25.3 tok/s** decode on an M4 Pro / 24 GB; no M2/16 GB number yet |
| **16 GB M2 fit** | **Yes by design and footprint.** Expect lower throughput than the M4 Pro result; SSD latency and context length matter |
| **License** | Apache 2.0 |

This is not an ordinary “load a 4-bit GGUF into RAM” package. Edge0 predicts which experts the next token will need, prefetches them from SSD, and applies a small LoRA trained to recover quantization quality. That makes the **active-memory number real but narrow**: it is MLX allocator usage, not total system RSS, and macOS will still use file cache opportunistically.

```bash
git clone https://github.com/Edge0-AI/edge0.git
cd edge0
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev,fetch]'
.venv/bin/python scripts/fetch_models.py --tier edge0-8b --target-dir models
.venv/bin/edge0 chat --name edge0-8b --model-dir models/edge0-8b \
  --prompt "Give me a concise explanation of mixture-of-experts routing."
```

Pin the project's stated versions (`mlx==0.30.6`, `mlx-metal==0.30.6`, `mlx-lm==0.31.0`) before diagnosing model output.

#### What about Edge0-35B?

The 35B-A3B tier uses the same idea with Qwen3.5-MoE, ~**23 GB** on disk and a published **~2.9 GiB** short-context MLX peak. It is explicitly supported on Apple Silicon, so the 16 GB M2 should be able to execute it through SSD streaming. I still rate it **⚠️**, because the only published benchmark here is an M4 Pro with 24 GB, the checkpoint exceeds this Mac's physical memory, and sustained speed depends heavily on SSD/page-cache behavior. Try the 8B tier first; the 35B tier is a systems experiment, not the default daily driver.

---

## The most tempting near-misses

### AuK / AuK-Flash: small headline, large runtime

AuK is a genuinely broad audio model: zero-shot and instruction TTS, speech/lyric/acoustic/paralinguistic editing, denoising, separation, and target-speaker extraction all use one instruction interface. AuK-Flash distills generation to four fixed steps.

The **1.5B** headline hides the full graph. Inference separately loads a **Qwen2.5-Omni-3B encoder** and VAE. Tencent's own A800 measurements are ~24.8–25.0 GiB without offload and ~16.75–16.98 GiB with its explicitly **CUDA-only** CPU-offload mode. A 16 GB unified-memory Mac has less than 16 GB available after macOS, so this is a firm **no today**, not a speculative MPS install.

For local speech on this machine, keep the smaller TTS paths from the [2026-08-23 report](./report-2026-08-23-video-ai-news.md) rather than forcing AuK.

### Show-Harness: the adapters fit; the product does not

Show-Harness publishes LoRA adapters for small Qwen/Gemma VLM bases; the adapter files themselves are only tens to hundreds of MB. A 0.8B or 2B base plus adapter can fit in 16 GB. But the official serving path is vLLM and the useful system includes a simulator or robot, action interfaces, cameras, and evaluation plumbing. Until there is a tested MLX adapter conversion and a Mac-friendly simulator recipe, count this as **research components**, not a ready local assistant.

### Marigold V2 and YuE2: close-looking VRAM numbers still miss

- **Marigold V2:** 4-bit DiT adapters do not make the base pipeline small. Its model card says **~17 GB GPU memory at 1024²**, already above the entire unified-memory pool.
- **YuE2:** its RTX 4090 peak can be around **11 GB** for a warm short run, but maximum context reaches **~14.1 GiB**, and the official recipe also requires **24 GB host RAM**, Linux, CUDA graphs, and FlashAttention. There is no equivalent Metal pack.

---

## Why the remaining releases are not local-Mac candidates

### World / 3D / robotics

- **LingBot-World-v2:** the new 1.3B variant sounds laptop-sized, but the official command still uses four GPUs and shared 14B T5/VAE assets. The 14B fast model uses eight GPUs. It is a distributed CUDA video system.
- **Isaac 0.5:** a 36B sparse multimodal robot model plus action heads and external runtime components. It is useful open robotics infrastructure, not a standalone chat VLM.
- **WorldSculpt / Fire3D:** both publish impressive editable 3D pipelines; both depend on CUDA-specific 3D stacks. Fire3D's validated hardware is especially far from this Mac.
- **UMR / UnifoLM-WLA:** UMR is a robot motion-retargeting pipeline. UnifoLM-WLA is still an announcement/open-source plan at this cutoff—the 6B WLA checkpoint and post-training code are not linked releases yet.
- **UniMate:** code is available, but pretrained checkpoints remain pending.

### Frontier model / research / product

- **DeepSeek-V4.1-Flash:** only 8B/16B parameters activate per phase, but the model still stores a 552B backbone and large conditional-memory tensors. Even aggressive community quants are server/workstation scale.
- **AlphaGenome Atlas:** a petabyte-scale variant-effect atlas accessed as a data product, not a local neural checkpoint.
- **Navier–Stokes chapter:** an AI-assisted research result produced by an internal system; no public model package to evaluate on this Mac.
- **RealSWE:** an important warning about benchmark realism, but it is an evaluation set/framework rather than a new model.
- **Suno v6 / ChatGPT financial services / Higgsfield:** useful hosted products, no local weights.

---

## Suggested actions on this machine

```text
Want the easiest useful install from this video?
  └─ MiniCPM5-2B-MLX (1.42 GB) or Q4_K_M GGUF (1.56 GB).
     Use it for lightweight local chat, code, extraction, and tool experiments.

Want the most technically novel local release?
  └─ Edge0-8B (~4.2 GB on disk).
     It is purpose-built for Apple Silicon and streams MoE experts from SSD.

Want to test Edge0-35B?
  └─ Possible through the same MLX/SSD design, but budget 23 GB of storage
     and expect M2 performance below the published M4 Pro result.

Want local speech or music?
  └─ Skip AuK and YuE2 on 16 GB. Their complete stacks exceed the practical
     memory/runtime budget. Reuse the smaller audio picks from prior reports.

Want the visual, world, or robot demos?
  └─ Use their hosted demos or a Linux CUDA machine. A small headline parameter
     count does not remove the shared encoders, VAEs, custom kernels, or robots.
```

---

## Sources

- Roundup: [YouTube video](https://www.youtube.com/watch?v=nZYJdwM-_nI)
- Marigold V2: [Hugging Face model card](https://huggingface.co/huawei-bayerlab/marigold-v2-0), [GitHub](https://github.com/huawei-bayerlab/marigold-v2)
- UniMate: [project page](https://linzhanmou.com/unimate/), [GitHub](https://github.com/Friedrich-M/UniMate)
- AlphaGenome Atlas: [Google DeepMind announcement](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphagenome-atlas/)
- LingBot-World-v2: [project page](https://technology.robbyant.com/lingbot-world-v2), [GitHub](https://github.com/robbyant/lingbot-world-v2)
- Isaac 0.5: [Hugging Face model card](https://huggingface.co/PerceptronAI/Isaac-0.5), [GitHub](https://github.com/perceptron-ai-inc/isaac)
- WorldSculpt: [project page](https://alaya-lab.github.io/WorldSculpt/), [GitHub](https://github.com/AlayaLab/WorldSculpt)
- Fire3D: [project page](https://xiahongchi.github.io/Fire3D/), [GitHub](https://github.com/xiahongchi/Fire3D)
- AuK: [project page](https://auk-project.github.io/), [GitHub](https://github.com/Tencent-Hunyuan/AuK), [AuK-Flash weights](https://huggingface.co/tencent/AuK-Flash)
- DeepSeek-V4.1-Flash: [DeepSeek announcement](https://www.deepseek.com/en/news/deepseek-v4-1-flash/), [Hugging Face model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
- Show-Harness: [project page](https://showlab.github.io/Show-Harness/), [GitHub](https://github.com/showlab/Show-Harness), [adapters](https://huggingface.co/showlab/Show-Harness-VLMs)
- Edge0: [GitHub and benchmarks](https://github.com/Edge0-AI/edge0), [8B weights](https://huggingface.co/Edge0/Edge0-8B-A1B-preview), [35B weights](https://huggingface.co/Edge0/Edge0-35B-A3B-preview)
- RealSWE: [paper](https://arxiv.org/abs/2608.27831), [project site](https://realswe.withspecific.com/)
- Suno v6: [Suno announcement](https://suno.com/blog/introducing-v6)
- YuE2: [project page](https://map-yue2.github.io/), [Hugging Face model card](https://huggingface.co/m-a-p/YuE2-3B)
- ChatGPT finance workflows: [OpenAI Learn](https://learn.chatgpt.com/use-cases?category=data&team=finance)
- UMR: [project page](https://hanyang9.github.io/UMR/)
- UnifoLM-WLA-1.0: [project page](https://unigen-x.github.io/unifolm-wla.github.io/), [GitHub](https://github.com/unitreerobotics/unifolm-wla)
- MiniCPM5-2B: [Hugging Face model card](https://huggingface.co/openbmb/MiniCPM5-2B), [official MLX pack](https://huggingface.co/openbmb/MiniCPM5-2B-MLX), [official GGUF pack](https://huggingface.co/openbmb/MiniCPM5-2B-GGUF)
- Prior hardware bar: [report-2026-07-17](./report-2026-07-17.md), [memory budget](./memory-budget.md)

## Method / caveats

- Inventory comes from the video's official chapter and description metadata. YouTube exposed a caption track but returned no usable transcript during this pass, so this report does **not** invent transcript-only claims; technical facts were checked against the linked project pages, repositories, and model cards.
- File sizes were checked from Hugging Face repository metadata as of **2026-09-13**. Decimal GB and binary GiB are kept as published where practical.
- Memory and speed figures are publisher measurements, not benchmarks run on this M2. Edge0's numbers are specifically from an **M4 Pro / 24 GB** machine; AuK's are from an NVIDIA A800.
- “Fits” means a realistic local workflow alongside macOS and ordinary apps, not merely that one weight shard is smaller than 16 GB. See [memory-budget.md](./memory-budget.md).
- Vendor quality claims (MiniCPM benchmark rank, Edge0 recovery scores, realtime world-model demos) are recorded as published and were not independently reproduced here.
