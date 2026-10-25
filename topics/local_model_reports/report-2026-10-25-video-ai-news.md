# Weekly AI video report — 2026-10-25

**As of:** 2026-10-25 (Asia/Taipei)\
**Source video:** [Cybersecurity chaos, AI for DNA, Kimi K3.1, Claude Duet, Dessa, Fibo 2, Minimax 3.1: AI NEWS](https://www.youtube.com/watch?v=EfyQOAJjx1A) by AI Search · published 2026-10-25 UTC · 43:05\
**Target:** M2 MacBook Pro, 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Local testing:** Not performed; assessments use artifacts, runtime source, and publisher or converter measurements.\
**Coverage:** All 24 official chapters in order; official description and English automatic transcript inspected.

## Worth trying on your Mac

**Bark 3.0** and **Ming-3.0-tts-0.5B** are this week's practical additions: English transcription and multilingual speech generation, both with native MLX paths. **Carbon-X** is a specialized, memory-constrained experiment for DNA questions. Fibo 2 has downloadable weights and Mac-compatible tooling, but its complete pipeline leaves much less headroom than its transformer size suggests.

| Model / configuration | Best for | Why it matters this week | Mac fit |
| --- | --- | --- | --- |
| [Bark 3.0 / Clean, upstream MLX](#bark-30-and-bark-30-clean) | 🗣️ English transcription and dictation | 163–179 MB compressed downloads; publisher reports an M2 inference result | ✅ Comfortable |
| [Ming-3.0-tts-0.5B, MLX BF16](#ming-30-tts-05b) | ❓ Speech synthesis and voice cloning | About 2.99 GB of complete weights; converter reports about 4.4 GB peak on M4 Pro | ✅ Comfortable |
| [Carbon-X, official Q4_K_M GGUF](#carbon-x) | 💬 DNA and English chat | Custom DNA tokenization works in recent llama.cpp; 9.64 GB weights require short context | ⚠️ Constrained |

**Mac fit:** ✅ Comfortable = credible path with headroom; ⚠️ Constrained = specific limits required; ⚠️ Experimental = important verification gaps; ❌ Outside budget = unsuitable for daily local inference on this machine. These are fit assessments, not measurements on this Mac. Hosted services, restricted releases, and unsupported runtimes are labeled separately.

## Speech recognition and transcription

### Bark 3.0 and Bark 3.0 Clean

**Mac fit:** ✅ Comfortable

**Why consider it:** Conway Research's Bark 3.0 is a 0.6B English speech recognizer. Standard Bark preserves fillers and repeated words; Clean removes them for dictation. The publisher reports 7.82% word error on AMI meetings and about 1.5 seconds to transcribe a minute of audio on an M2 laptop. Those are publisher results, with no independent replication here. [Model card](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0) · [Release and Clean comparison](https://underdog.ai/bark)

**Start with:** The upstream `bark_mlx.py` runner and its default FP16 cache. Choose standard Bark for a faithful transcript and Clean for edited dictation. Begin with one short English recording.\
**Main limitation:** The small download expands to roughly 1.25 GB of weights, and first-time unpacking needs about 6 GB of RAM. Neither variant supplies speaker diarization or word timestamps; English-only recognition will not replace a multilingual meeting pipeline. [Pinned MLX runner](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0/blob/85db2ad18ab41e534a222ee253c29191d77ed919/bark_mlx.py)

[Video chapter](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=190s) · [Clean model](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Clean) · [Deployment details](#bark-30-deployment)

## Speech generation

### Ming-3.0-tts-0.5B

**Mac fit:** ✅ Comfortable

**Why consider it:** Ming generates 44.1 kHz speech with cloning, voice design, delivery instructions, and sounds such as laughter or sighs. The dense model supports seven languages, including Chinese and English, plus Cantonese and Sichuanese with suitable references. Its complete speech system is larger than its 0.5B language backbone. [Project](https://nomorecoding.github.io/Ming-3.0-tts/)

**Start with:** `mlx-community/Ming-3.0-tts-0.5B-bf16` in **mlx-audio 0.6.1 or newer**. Try a short sentence and built-in voice, then cloning with a short reference and its exact transcript. Version 0.6.1 fixes the prompt format; older versions can load the model but speak different words. [Converter card](https://huggingface.co/mlx-community/Ming-3.0-tts-0.5B-bf16) · [Merged fix](https://github.com/Blaizzy/mlx-audio/pull/1047)\
**Main limitation:** The converter reports roughly real-time generation and 4.4 GB peak on M4 Pro; M2 speed is unknown. The dense MLX implementation still lacks automatic speaker-embedding extraction and the reference text normalizer, so spell out numbers and evaluate voice identity separately from intelligibility. An occasional stopping failure leaves trailing noise. [Runtime notes](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/dense/README.md)

[Video chapter](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=813s) · [MLX weights](https://huggingface.co/mlx-community/Ming-3.0-tts-0.5B-bf16) · [Deployment details](#ming-30-tts-deployment)

## DNA sequence research

### Carbon-X

**Mac fit:** ⚠️ Constrained

**Why consider it:** Hugging Face Bio's 14.8B model reads DNA and English in the same conversation. It groups DNA into six-base tokens rather than treating sequences as ordinary prose, supporting sequence questions and continuation without a separate encoder. The publisher identifies it as a research model with no clinical validation. [Model card](https://huggingface.co/HuggingFaceBio/Carbon-X)

**Start with:** The official `carbon-x-q4_k_m.gguf` in **llama.cpp b11742 or newer**, with Metal, one request, and 2K total context. Older runtimes may load the file while tokenizing DNA incorrectly. Disable thinking as the release recommends. These are suggested limits, not a tested M2 configuration. [Official GGUF card](https://huggingface.co/HuggingFaceBio/Carbon-X-GGUF) · [Tokenizer release](https://github.com/ggml-org/llama.cpp/releases/tag/b11742)\
**Main limitation:** The file is 9.64 GB before cache and compute buffers. A 2K FP16 key/value cache adds about 0.34 GB, calculated from the model configuration; peak memory remains unknown. The publisher's Q4 results are lower than the original model on both reported quantization tests. There is little room for another model or a long context.

[Video chapter](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=457s) · [Pinned files](https://huggingface.co/HuggingFaceBio/Carbon-X-GGUF/tree/cbb978c02e494bbe4043ed582c532296fc97a31e) · [Deployment details](#carbon-x-deployment)

## Other developments worth knowing

- **Fibo 2.0:** Bria combines generation and editing, with a separate few-step Edit Turbo variant. A plausible ComfyUI Q3 pipeline totals **10.38 GB of weights** before image tensors and buffers. The [October 18 report's FLUX 3 Image Klein](./report-2026-10-18-video-ai-news.md#flux-3-image-klein) still has better published evidence for a sub-10 GB Mac peak. Neither was retested here. [Bria](https://huggingface.co/briaai/Fibo-2.0-dev) · [Full budget](#fibo-20-deployment)
- **Kimi K3.1 Pro and MiniMax M3.1 Flash:** Both are hosted at the cutoff. Moonshot promises full Kimi weights by November 4; MiniMax says weights will follow later. An announced open release does not yet provide a downloadable local configuration. [Kimi](https://www.kimi.ai/blog/kimi-k3-1-pro) · [MiniMax](https://www.minimax.io/blog/minimax-m31f)
- **Dessa:** Block demonstrates full-duplex speech trained from conversation audio alone and says inference runs on an M4 Max or better. Access is limited to selected safety researchers. Block specifies **one GB200 NVL72 system** for training; the transcript's single-GPU wording should not be read as the hardware specification. No public weights or 16 GB budget are provided. [Block](https://block.xyz/dessa)
- **Security:** The video groups software vulnerabilities, weak certificate keys, and credential theft. The [seven-case notes](#cybersecurity-chapter-notes) distinguish the mechanisms and evidence of AI involvement; they do not establish a common attacker or cause.

## Technical appendix

### Complete video chapter inventory

All 24 chapters follow the official description and markers. “❌ Hosted” means no public local weights were verified. “⚠️ Unverified” records unresolved deployment evidence; “— N/A” covers editorial, infrastructure, and hardware stories.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=0s) | AI news intro | Editorial | — N/A; introduces the roundup. |
| [01:01](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=61s) | [WeVisOne-VL](https://tencent.github.io/WeVisOne-VL/) | Open weights / perception | ⚠️ Experimental; custom pixel decoder, with no verified complete Metal or MLX path. |
| [03:10](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=190s) | [Bark 3.0](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0) | Open weights / ASR | ✅ Comfortable; upstream MLX runner; compressed weights expand before inference. |
| [04:53](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=293s) | [Fibo 2.0](https://huggingface.co/briaai/Fibo-2.0-dev) | Open weights / images | ⚠️ Experimental; Q3 pipeline is 10.38 GB before working memory; no verified M2 peak. |
| [07:37](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=457s) | [Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) | Open weights / DNA language model | ⚠️ Constrained; official Q4 GGUF and compatible tokenizer exist; short context required. |
| [09:27](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=567s) | [Hy-Nomas](https://github.com/Tencent-Hunyuan/Hy-Nomas) | Open weights / world generation | ❌ Outside supported Mac path; Linux/CUDA kernels; low-memory recipe targets an RTX 4090. |
| [11:14](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=674s) | [Hi3D 1.0](https://github.com/hi3d-official/Hi3Dv1.0) | Open weights / 3D refinement | ❌ Outside supported Mac path; Linux and NVIDIA compute capability ≥8.0; no CPU inference. |
| [12:24](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=744s) | [PURE](https://funnyguy525.github.io/PURE-Page/) | Open weights / 3D reconstruction | ❌ Outside documented Mac path; release setup requires Linux and CUDA. |
| [13:33](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=813s) | [Ming 3.0 TTS](https://nomorecoding.github.io/Ming-3.0-tts/) | Open weights / speech | ✅ Comfortable for dense 0.5B MLX; Tiny needs a separate budget and runtime check. |
| [15:22](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=922s) | [Luma](https://lumalabs.ai/) | Sponsored hosted creative tools | ❌ Hosted; sponsor segment, not a local model release. |
| [16:51](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1011s) | AI cybersecurity ([PHP](https://www.php.net/archive/2026.php#2026-10-21-5), [seven-case notes](#cybersecurity-chapter-notes)) | Security news | — N/A; software patches, certificate incident, and credential theft require separate evidence. |
| [22:42](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1362s) | [OpenAI research agents](https://openai.com/index/scaling-ai-research-for-complex-biological-data/) | Biological research workflow | — N/A; distributed GPT-Rosalind analysis, not released local model weights. |
| [24:34](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1474s) | [JST-2](https://viggle.ai/jst2) | Hosted world model | ❌ Hosted; browser renders generated 3D splats locally; new content requires inference. |
| [25:51](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1551s) | [SKY-001](https://skyfall.ai/blog/introducing-sky-001) | Engineering world-model research | ⚠️ Unverified; visual CAD/BIM plans demonstrated; no deployment download found in the announcement. |
| [27:26](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1646s) | [Kimi K3.1 Pro](https://www.kimi.ai/blog/kimi-k3-1-pro) | Hosted LLM / announced weights | ❌ Hosted at cutoff; 3T-class model; full weights promised by November 4. |
| [29:50](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1790s) | [Ideogram Vector](https://ideogram.ai/models/vector/) | Hosted vector generation | ❌ Hosted; editable SVG outputs do not imply downloadable inference weights. |
| [30:51](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=1851s) | [Dessa](https://block.xyz/dessa) | Restricted speech-to-speech research | ❌ Restricted; claimed M4 Max operation, but no public weights or memory measurement. |
| [34:12](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2052s) | [Claude Duet](https://claude.com/resources/articles/claude-duet) | Hosted proactive agent | ❌ Hosted; cloud VM; preview starts with US Pro/Max subscribers through a waitlist. |
| [35:28](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2128s) | Unitree H2X | Robot demonstration | — N/A; H2X-specific primary specifications were not verified; no endurance or autonomy conclusion drawn. |
| [36:10](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2170s) | [Sage-A1.5](https://huggingface.co/collections/InternScience/sage-a15) | Open weights / research agent | ❌ Outside budget; official Q4 language-model file alone is 21.71 GB. |
| [37:39](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2259s) | [MiniMax M3.1 Flash](https://www.minimax.io/blog/minimax-m31f) | Hosted LLM / announced weights | ❌ Hosted at cutoff; API and products available, weights promised later. |
| [38:33](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2313s) | [MemT 1.0](https://huggingface.co/MemTensor/MemT-1.0-Nano) | Open weights / memory LLM | ❌ Outside budget; Nano stores about 70.22 GB of weights, including its memory block. |
| [40:00](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2400s) | [Ling 3.0 Flash Santé](https://huggingface.co/inclusionAI/Ling-3.0-flash-Sante) | Open weights / healthcare LLM | ❌ Outside budget; 124B total / 5.1B active; about 254.98 GB of released weights. |
| [41:00](https://www.youtube.com/watch?v=EfyQOAJjx1A&t=2460s) | [FastH3 Omni](https://haoailab.com/blogs/fastvideo-omniref-update/) | Open weights / video and audio | ❌ Outside budget; native MLX path validated on a 36 GB M4 Max, not a 16 GB Mac. |

### Bark 3.0 deployment

**Configuration:** Upstream Bark revision `85db2ad18ab41e534a222ee253c29191d77ed919`; Clean revision `6d34ed8639b2b9a33e764acf06748519bbb950cf`; shipped MLX loader and FP16 cache. Standard card pins mlx-audio 0.5.3 and MLX 0.32.2 for reproduction.\
**Fit evidence:** Publisher M2 timing, converter source, and artifact metadata; no run here.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Standard / Clean `model.bark` | 0.163 / 0.179 GB | Compressed complete recognition weights; download size is not RAM usage. |
| Expanded FP16 model | About 1.25 GB | Encoder, prediction network, and joint network; cached by the runner. |
| Tokenizer, vocabulary, configuration | Under 1 MB | Shipped in `mlx/`; no separate LLM or vocoder needed. |

**Working memory:** About 6 GB for initial unpacking according to runner source; M2 inference peak is unpublished. Small expanded weights leave substantial headroom.\
**Starting limits:** Short recording, one request; extend duration after observing memory. The runner processes the full input without a fixed duration cap.\
**Runtime support:** Native MLX. Keep the documented Bark environment separate from Ming's newer mlx-audio when reproducing the published settings; Bark on that newer version was not checked. An alternative [FluidAudio Core ML conversion](https://huggingface.co/FluidInference/bark-3.0-coreml) supplies the full pipeline and requires macOS 15+; its M5 Pro timings are not M2 timings.\
**License:** CC-BY-4.0 weights; [MIT mlx-audio](https://github.com/Blaizzy/mlx-audio/blob/main/LICENSE).\
**Unresolved:** Long-meeting peak, microphone quality, and integration of speaker separation and timestamps.

[Pinned standard files](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0/tree/85db2ad18ab41e534a222ee253c29191d77ed919) · [Pinned Clean files](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Clean/tree/6d34ed8639b2b9a33e764acf06748519bbb950cf)

### Ming 3.0 TTS deployment

**Configuration:** Dense BF16 MLX revision `283b3c342c6fb69a7a87832c97f9799567efe05d`; mlx-audio ≥0.6.1 with [prompt fix #1047](https://github.com/Blaizzy/mlx-audio/pull/1047).\
**Fit evidence:** Converter M4 Pro measurement, file metadata, and runtime documentation.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Dense BF16 `model.safetensors` | 2.959 GB | Language backbone plus acoustic generation/decoding modules. |
| Bundled `campplus.safetensors` | 0.028 GB | Speaker weights present; dense runner still lists automatic extraction as unimplemented. |
| Complete BF16 weights | **2.987 GB** | Tokenizer adds about 16 MB; activations and waveform are extra. |
| Alternative MLX 8-bit weights | 1.601 GB including CAMPPlus | Quantizes the audio VAE too; BF16 already fits. |
| Tiny MLX 4-bit alternative | 6.651 GB including CAMPPlus | Separate 7.9B-total / 1.3B-active MoE; acoustic modules and routers remain floating point. |

**Working memory:** Dense converter reports about 4.4 GB peak on M4 Pro, with incomplete clip/settings detail. Encoding, generation, and final waveform decode still need an M2 measurement. Tiny's fitting files do not establish its peak; treat it as experimental.\
**Starting limits:** One sentence, one output, no concurrent model. Test longer text and controls separately.\
**Runtime support:** Native dense MLX; [Tiny has a separate MLX guide](https://blaizzy.github.io/mlx-audio/models/tts/ming3-tiny/). These ports avoid the upstream CUDA environment.\
**License:** MIT Ming weights/code; MIT mlx-audio.\
**Unresolved:** M2 latency, long-form stopping, intended-language pronunciation, speaker identity, and parity with upstream task combinations.

[Pinned BF16 files](https://huggingface.co/mlx-community/Ming-3.0-tts-0.5B-bf16/tree/283b3c342c6fb69a7a87832c97f9799567efe05d) · [8-bit files](https://huggingface.co/mlx-community/Ming-3.0-tts-0.5B-8bit/tree/d0d1da6f627e4b3f20cc2db6ba4aee86d45343ad) · [Tiny 4-bit files](https://huggingface.co/mlx-community/Ming-3.0-tts-tiny-4bit/tree/6010a1204b1a07da4a310b923975b673117eeae9)

### Carbon-X deployment

**Configuration:** Official Q4_K_M revision `cbb978c02e494bbe4043ed582c532296fc97a31e`; llama.cpp ≥b11742 with Metal.\
**Fit evidence:** Exact artifacts, model configuration, and merged tokenizer support; memory estimate is inferred.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Q4_K_M GGUF | 9.636 GB | Publisher's K-quants keep embedding/output tensors at Q8_0. |
| Separate encoder / projector / decoder | Not required | DNA and text share one decoder and tokenizer. |
| FP16 KV cache, 2K tokens | 0.336 GB, calculated | 40 layers × 8 KV heads × 128 dimensions × K/V × 2 bytes × 2,048 tokens. |
| Weights plus that cache | **About 9.97 GB** | Excludes compute buffers, loading peaks, application, and OS. |

**Working memory:** Unknown. At 4K context, that subtotal becomes 10.31 GB; at the advertised 40,960 tokens, FP16 KV alone is about 6.71 GB. Start at 2K and stop if memory pressure or swap makes it impractical.\
**Starting limits:** One request, 2K total context, thinking disabled; sequence, question, and answer share that context.\
**Runtime support:** b11742 implements the required HybridDNA tokenizer and provides macOS ARM64 binaries. Older builds accepting the file do not establish correct DNA behavior.\
**License:** Apache-2.0 weights; [MIT llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/LICENSE).\
**Unresolved:** M2 peak/speed, long-sequence reliability, and Q4 quality for the intended research.

In the publisher's single-run quantization tests, Q4 scores 67.8 versus 70.4 for the original on FrontierVEP and 38.6 versus 39.4 on NextBase, with sampling uncertainty. The BF16 card still describes GGUF tokenization as unsupported; the separate GGUF card and actual b11742 release establish the path assessed here. [Quantization evaluation](https://huggingface.co/HuggingFaceBio/Carbon-X-GGUF#evaluation) · [Pinned configuration](https://huggingface.co/HuggingFaceBio/Carbon-X/blob/539ad36790e78a38718c547bcb12c55b8a447c56/config.json)

### Fibo 2.0 deployment

The full official BF16 pipeline totals about **25.47 GB**: transformer, Qwen3-VL-4B encoder, and FLUX.2 VAE. Quantizing the transformer alone does not finish the memory reduction.

| Component | Candidate artifact | Size |
| --- | --- | --- |
| Dev or Edit Turbo transformer | `vantagewithai` Q3_K_M GGUF | 5.190 GB |
| Text/image encoder | Comfy-Org Qwen3-VL-4B INT8 ConvRot | 4.859 GB |
| VAE | Comfy-Org FLUX.2 VAE | 0.336 GB |
| Complete candidate weights | Q3 + INT8 encoder + VAE | **10.385 GB** |
| Q4 alternative | Same auxiliaries, Q4_K_M transformer | **11.429 GB** |
| Comfy-Org INT8 alternative | INT8 transformer and encoder, VAE | **13.603 GB** |

**Verdict:** ⚠️ Experimental for Q3; the larger bundles exceed the practical target before activations. The converter's workflow names these Q3, encoder, and VAE files and uses `UnetLoaderGGUF`, but publishes no 16 GB M2 peak. ComfyUI has a Mac path; exact Fibo GGUF operations and quality still need validation. CPU offload uses the same unified pool.

If testing, begin with Edit Turbo, one reference, batch one, and a small canvas before 1024². Supply structured prompts directly so this budget does not add a prompt-expansion service or model. Peak memory and low-bit quality are unknown here. Bria's card uses its Fibo noncommercial terms; Comfy-Org and the converter label their releases CC-BY-NC-4.0. Check Bria's commercial terms separately from the runtime license.

[Official card](https://huggingface.co/briaai/Fibo-2.0-dev) · [Pinned GGUF workflow/files](https://huggingface.co/vantagewithai/Fibo-2.0-Dev-and-Edit-Turbo-ComfyUI-GGUF/tree/ace2f69cbd88f8b8c5ee63443696649c3e28155f) · [Pinned encoder/VAE](https://huggingface.co/Comfy-Org/Fibo-2.0/tree/b2bffaf57d48825a6989b986f24d5cfb8c71231b)

### Other deployment notes

- **WeVisOne-VL:** Its 2B release stores 2.442B parameters in FP32: 9.767 GB, plus a 0.038 GB pixel-decoder sidecar. The inspected engine automatically chooses CPU on a Mac and forces FP32 there. Passing MPS would be a compatibility experiment. A generic Qwen3-VL GGUF does not establish custom segmentation/matting support. Code and weights are Apache-2.0. [Pinned files](https://huggingface.co/tencent/WeVisOne-VL-2B/tree/3dad9ce8bcb6fbe0aea945bf8860bd2cfc3663bf) · [Pinned engine](https://github.com/Tencent/WeVisOne-VL/blob/40f735b8daed437ece982db9718e9c9856f52a79/wevisone_vl/engine.py)
- **Hi3D and PURE:** Hi3D refines a coarse mesh with a reference image; the coarse generator is another dependency. Its validated high-resolution stack uses a 96 GB H20 and CUDA sparse kernels. PURE post-trains Pi3, DA3, or VGGT; its 2,000-frame showcase accumulates offline clips, rather than showing live causal reconstruction. Neither has a documented Mac path. [Hi3D scope/requirements](https://github.com/hi3d-official/Hi3Dv1.0) · [PURE runtime](https://github.com/IGL-HKUST/PURE) · [Showcase method](https://funnyguy525.github.io/PURE-Page/)
- **Hy-Nomas and FastH3 Omni:** Hy-Nomas's low-memory recipe remains Linux/CUDA, with an INT8 DiT and separate video components. FastH3 has a merged native MLX path validated with INT6 on a **36 GB M4 Max**, so calling the entire release CUDA-only would be wrong. Even its separate NVIDIA NVFP4 transformer is 11.92 GB before conditioning, reference encoding, video decoding, and audio components; that file is not an MLX peak measurement. [Hy-Nomas](https://github.com/Tencent-Hunyuan/Hy-Nomas) · [FastH3 MLX PR](https://github.com/hao-ai-lab/FastVideo/pull/2000) · [MLX build kit](https://huggingface.co/FastVideo/FastH3-Omni-MLX) · [NVFP4 artifacts](https://huggingface.co/FastVideo/FastH3-Omni-NVFP4-QAD/tree/f01e6a23ac6066aa9eb622cf94b6259442e70ec2)
- **Sage, MemT, and Santé:** Sage's Q4 language weights are 21.71 GB, with a separate 0.90 GB projector available. MemT Nano's 70.22 GB includes its 0.902 GB trainable memory block; compact persistent state does not shrink the 36B backbone. Santé's 5.1B active parameters likewise do not remove its 124B total-weight storage. [Sage Q4](https://huggingface.co/InternScience/Sage-A1.5-Q4_K_M-GGUF/tree/10b179b52f2c841030db327627e707d076b4c8cf) · [MemT files](https://huggingface.co/MemTensor/MemT-1.0-Nano/tree/30fe0b22422c4cc4c87475f98db5c8baa5c1a902) · [Santé files](https://huggingface.co/inclusionAI/Ling-3.0-flash-Sante/tree/f74bd27bd26ffc71a50dd847805f8f7666ff0b43)

### Hosted products and research interpretation

OpenAI reports thousands of GPT-Rosalind agents analyzing existing mouse-brain perturbation data in 32 minutes. Their output links hypotheses to literature, with follow-up experiments still needed. This does not establish that Carbon-X or a local agent reproduces that workflow's performance. [OpenAI research](https://openai.com/index/scaling-ai-research-for-complex-biological-data/)

JST-2 separates generation from viewing: browsers render a scene after server-side generation. Its approximately one-second result uses an NVIDIA B200 and excludes network latency. SKY-001 demonstrates visual design plans; its announcement puts executable CAD operations and editable BIM conversion among future steps. Neither establishes a local engineering model for this Mac. [Viggle](https://viggle.ai/jst2) · [Skyfall](https://skyfall.ai/blog/introducing-sky-001)

Ideogram Vector exports editable SVGs through a hosted product. Claude Duet runs its proactive agent in a cloud VM, so continuing while a laptop is off is expected. Dessa's claimed local inference remains restricted research access. None supplies a public 16 GB checkpoint configuration. [Ideogram](https://ideogram.ai/models/vector/) · [Anthropic](https://claude.com/resources/articles/claude-duet) · [Block](https://block.xyz/dessa)

### Cybersecurity chapter notes

The chapter names seven cases. These sources establish different incidents and vulnerabilities; they do not show that every case was discovered or exploited by AI.

| Case | Primary evidence and interpretation as of October 25 |
| --- | --- |
| PHP | CVE-2026-109618 and CVE-2026-109619 were fixed in 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35. The archive also carries an October 23 session-upload-progress follow-up; the earlier patch headline is not the whole current advisory. [PHP](https://www.php.net/archive/2026.php#2026-10-21-5) |
| GitLab | CVE-2026-110264 is an unauthenticated regex-compiler overflow rated CVSS 10.0. The advisory lists seven patched branches, including 19.5.1, and says managed infrastructure is patched. This is separate from the PHP flaws. [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/) |
| Node.js | October 21 fixes include a Brotli memory-corruption flaw credited to OpenAI Codex Security, alongside other issues and certificate updates. Fixed releases: 26.12.1 / 24.22.1 / 22.23.4. That credit does not establish AI involvement in every chapter item. [Node.js](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases) |
| eMudhra | Mozilla verified control of eight intermediate keys and independently recovered them, establishing flawed key generation. This does not mean TLS cryptography itself was broken. The company's statement distinguishes global TLS from Indian DSC/eSign services. [Mozilla](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449) · [eMudhra](https://emudhra.com/en/press-release/emudhra-statement-distrust-global-tls-intermediate-root-ca) |
| Railway | Preliminary report: an attacker decrypted environment variables for a subset of workspaces. Running services stayed online while builds/deployments were interrupted. AI-assisted exploitation and a distillation motive are Railway's preliminary assessment; forensics remained ongoing. [Railway](https://blog.railway.com/p/preliminary-report-october-security-incident) |
| OpenCode | Official October 17 statement: 1.4% of **Console** users affected, a subset with external providers linked; affected users were emailed. This does not establish compromise of every local installation. The statement does not disclose the intrusion mechanism. [OpenCode](https://x.com/opencode/status/2111519637049319818) |
| LiteLLM | October 23 investigation traces malicious release **1.107.0** to an exposed, unrevoked agent-platform master key, then GitHub tokens and release-pipeline access. Keep this separate from the March incident and from a generic developer-password theft account. [LiteLLM](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain) |

The video's claim that roughly 3% of historical critical bugs were found in a recent month was not independently verified with a defined dataset and denominator; it is not used to quantify the trend. Related timing and targets also do not establish one coordinated campaign across all seven cases.

### Method and verification limits

- **Video:** Title, author, duration, description, all 24 chapters, and English automatic transcript inspected. Publication metadata says October 24, 20:29 Pacific, which is October 25 UTC and in Taipei. Primary sources resolve caption errors in model names and hardware terms.
- **Sources:** Publisher pages, cards, artifact metadata, converter code, runtime PRs, and incident reports checked on October 25. Unitree H2X is the explicit primary-source gap; no H2X-specific specification was verified, and endurance/autonomy claims are omitted.
- **Memory:** GB is decimal; GiB is binary. Sums cover a chosen configuration, not all alternative files in a repository. Download size, expanded weights, conversion/loading peaks, cache, activations, and output decoding are separate costs. CPU offload does not add unified memory.
- **Evidence strength:** Bark's M2 timing is publisher-reported; Ming's M4 peak is converter-reported; Carbon's cache is calculated. Fibo and WeVisOne remain compatibility experiments. No model was installed or benchmarked for this report.
- **Repository checks:** Index/local links, section anchors, all chapter timestamps/order, and component arithmetic checked; `git diff --check` run. Of 68 distinct external destinations, 67 answered direct HTTP checks; OpenAI blocked that fetch, but its article was successfully inspected through the web reader. No executable setup commands are included because no runtime was exercised.

## Sources

- **Video:** [AI Search weekly news](https://www.youtube.com/watch?v=EfyQOAJjx1A), published October 25 UTC; timestamps in the inventory.
- **Perception:** [WeVisOne-VL project](https://tencent.github.io/WeVisOne-VL/) · [Runtime](https://github.com/Tencent/WeVisOne-VL) · [2B weights](https://huggingface.co/tencent/WeVisOne-VL-2B).
- **Transcription:** [Bark announcement](https://underdog.ai/bark) · [Standard](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0) · [Clean](https://huggingface.co/ConwayResearch/Underdog-Bark-3.0-Clean) · [Core ML conversion](https://huggingface.co/FluidInference/bark-3.0-coreml).
- **Speech generation:** [Ming project](https://nomorecoding.github.io/Ming-3.0-tts/) · [Upstream](https://github.com/inclusionAI/Ming-3.0-tts) · [Dense MLX](https://huggingface.co/mlx-community/Ming-3.0-tts-0.5B-bf16) · [Runtime notes](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/tts/models/dense/README.md) · [Tiny MLX](https://blaizzy.github.io/mlx-audio/models/tts/ming3-tiny/).
- **DNA:** [Carbon-X](https://huggingface.co/HuggingFaceBio/Carbon-X) · [Official GGUF](https://huggingface.co/HuggingFaceBio/Carbon-X-GGUF) · [Tokenizer implementation](https://github.com/ggml-org/llama.cpp/pull/30825).
- **Images:** [Fibo Dev](https://huggingface.co/briaai/Fibo-2.0-dev) · [Comfy-Org components](https://huggingface.co/Comfy-Org/Fibo-2.0) · [GGUF workflow](https://huggingface.co/vantagewithai/Fibo-2.0-Dev-and-Edit-Turbo-ComfyUI-GGUF) · [Ideogram Vector](https://ideogram.ai/models/vector/).
- **3D/world models:** [Hy-Nomas](https://github.com/Tencent-Hunyuan/Hy-Nomas) · [Hi3D announcement](https://www.hi3d.ai/hi3d-1-0-open-source) · [Hi3D runtime](https://github.com/hi3d-official/Hi3Dv1.0) · [PURE](https://funnyguy525.github.io/PURE-Page/) · [JST-2](https://viggle.ai/jst2) · [SKY-001](https://skyfall.ai/blog/introducing-sky-001).
- **Video/audio generation:** [FastH3 Omni](https://haoailab.com/blogs/fastvideo-omniref-update/) · [MLX PR](https://github.com/hao-ai-lab/FastVideo/pull/2000) · [MLX build kit](https://huggingface.co/FastVideo/FastH3-Omni-MLX).
- **Large models:** [Sage project](https://alpha-innovator.github.io/Sage-A1.5/) · [Current Sage artifacts](https://huggingface.co/collections/InternScience/sage-a15) · [MemT Nano](https://huggingface.co/MemTensor/MemT-1.0-Nano) · [Ling Santé](https://huggingface.co/inclusionAI/Ling-3.0-flash-Sante).
- **Hosted/restricted releases:** [Kimi K3.1 Pro](https://www.kimi.ai/blog/kimi-k3-1-pro) · [MiniMax M3.1 Flash](https://www.minimax.io/blog/minimax-m31f) · [Dessa](https://block.xyz/dessa) · [Claude Duet](https://claude.com/resources/articles/claude-duet) · [Luma sponsor destination](https://lumalabs.ai/).
- **Research agents:** [OpenAI biological-data analysis](https://openai.com/index/scaling-ai-research-for-complex-biological-data/).
- **Security:** [PHP](https://www.php.net/archive/2026.php#2026-10-21-5) · [GitLab](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/) · [Node.js](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases) · [Mozilla/eMudhra](https://bugzilla.mozilla.org/show_bug.cgi?id=2083449) · [eMudhra statement](https://emudhra.com/en/press-release/emudhra-statement-distrust-global-tls-intermediate-root-ca) · [Railway](https://blog.railway.com/p/preliminary-report-october-security-incident) · [OpenCode](https://x.com/opencode/status/2111519637049319818) · [LiteLLM](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain).
