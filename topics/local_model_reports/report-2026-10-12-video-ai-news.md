# Weekly AI video report — 2026-10-12

**As of:** 2026-10-12\
**Source video:** [New AI enzymes, 700+ math breakthroughs, AI for DNA mutations, room temp semiconductors: AI NEWS](https://www.youtube.com/watch?v=X0_GDOkLKzQ) by AI Search · published 2026-10-11 UTC · 45:11\
**Target:** M2 MacBook Pro, 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Local testing:** Not performed; assessments use artifacts, runtime documentation, and publisher measurements.\
**Coverage:** All 22 official chapters in order. Official description inspected; captions could not be retrieved.

## Worth trying on your Mac

Start with **EmbeddingGemma 2** if you want local search over your own notes, code, or photos. **Botanic1-M** is worth a look only if you work with plant DNA. Most of this week's video covers hosted services, scientific results, and visual or world models that need large NVIDIA systems. Amazon's ALoDLM-8B looks small enough, but its community GGUF files do not run the diffusion decoding that makes it interesting.

| Model / configuration | Best for | Why it matters this week | Mac fit |
| --- | --- | --- | --- |
| [EmbeddingGemma 2, text-only](#embeddinggemma-2) | ❓ Embeddings for local search and retrieval | 270M-parameter text path; Q8 GGUF is 310 MB; Apache-2.0; code retrieval improved sharply | ✅ Comfortable |
| [Botanic1-M, fp32 PyTorch on MPS](#botanic1-m) | ❓ Plant DNA variant scoring | 688M-parameter genomic model; publisher lists Apple-silicon (MPS) support | ✅ Comfortable |

**Mac fit:** ✅ Comfortable = credible path with headroom; ⚠️ Constrained = specific limits required; ⚠️ Experimental = important verification gaps; ❌ Outside budget = unsuitable in the checked configuration. These are deployment judgments, not M2 measurements. The shared budget is approximately **8–11 GB for the entire inference process**, including weights, caches, and activations.

## Embeddings for local search

An embedding model turns a passage, image, or audio clip into a list of numbers (a vector). Similar content produces nearby vectors, so a search tool can find relevant material by comparing vectors rather than matching keywords. Embedding models do not generate text; they supply the retrieval step that a chat model can then read from.

### EmbeddingGemma 2

**Mac fit:** ✅ Comfortable

**Why consider it:** Google's successor to EmbeddingGemma places text, images, audio, video, and code in one vector space. The text path uses about 270M of the model's 740M parameters; vision and audio encoders are optional additions. Google reports an MTEB Code score of **78.68**, up from 68.76 for the first version, with multilingual text results about level (61.36 vs 61.15). Output vectors can be truncated from 768 to 512 or 256 dimensions with little loss, which shrinks a search index. [Google announcement](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2) · [Model card](https://huggingface.co/google/embeddinggemma-2)

**Start with:** The text-only model, either through Ollama's `embeddinggemma-2:270m` tag (378 MB) or the `ggml-org` **Q8_0 GGUF (309.9 MB)** in llama.cpp. Embed a few hundred notes or source files and test search with the card's task prefixes, such as `task: search result | query: …` for queries and `title: … | text: …` for documents. Add the image projector only once text search is useful.\
**Main limitation:** Retrieval quality depends on applying the right prefix to queries and documents, and the card warns that **float16 can silently produce NaN or degraded embeddings**; use bfloat16 or float32 in Python, or a GGUF quantization. Audio and video embedding through llama.cpp or Ollama was not confirmed; the checked Ollama tags list text and image input only.

[Video chapter](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1597s) · [GGUF artifacts](https://huggingface.co/ggml-org/embeddinggemma-2-GGUF) · [Ollama](https://ollama.com/library/embeddinggemma-2) · [Deployment details](#embeddinggemma-2-deployment)

## Plant DNA variant scoring

### Botanic1-M

**Mac fit:** ✅ Comfortable

**Why consider it:** Living Models' Botanic1 family reads plant DNA one base at a time. To score a mutation, it compares how likely the model finds the mutated base versus the original base in its surrounding sequence; a strongly negative score suggests the change disrupts a conserved position. In a melon case study, Google's Gemma 4 E4B narrowed a region to 2,494 single-letter variants, and Botanic1 ranked the validated causal mutation first in 18 of 20 runs. That result comes from the publishers' agent pipeline, not from Botanic1-M alone. [Gemmaverse write-up](https://deepmind.google/models/gemma/gemmaverse/living-models/)

**Start with:** `living-models/Botanic1-M` (688M parameters, **about 2.8 GB of fp32 weights**) in PyTorch on MPS, with the card's `score_variant_zero_shot` helper. Score one known variant from the card's example, then a small batch of equal-length windows; the card defaults to batch 8 on CPU/MPS.\
**Main limitation:** Research use only: the license forbids production, clinical, and diagnostic use, and downloading requires accepting gated terms that share your Hugging Face username and email. Released models score windows of up to **8,191 bases**, shorter than the roughly 128 kb context described in the case study. A near-zero score does not mean a variant is harmless. [Model card](https://huggingface.co/living-models/Botanic1-M)

[Video chapter](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=626s) · [Model family](https://huggingface.co/collections/living-models/botanic1-6a97f4e3c33f3d109a75057d) · [Deployment details](#botanic1-m-deployment)

## Other developments worth knowing

- **ALoDLM-8B looks local but is not yet:** Amazon's diffusion language model, built from Qwen3-8B, drafts several tokens at once and spends extra passes only on uncertain tokens. The publisher reports a higher 11-benchmark average than Qwen3-8B and about 2.7× its throughput on a B200. The documented runtimes are CUDA or fp32 CPU, and the license is non-commercial. Community GGUF files load as an ordinary Qwen3 model and do not implement the adaptive decoding. [Model card](https://huggingface.co/amazon/ALoDLM-8B) · [Details](#alodlm-8b-near-miss)
- **AI-produced mathematics:** OpenAI published 719 manuscripts in 372 families from an unreleased internal model, with about 42% of top-line results formalized in Lean. OpenAI states that unformalized results may contain errors. [Repository](https://github.com/openai/math)
- **AI-assisted science claims:** AlphaProtein Novo releases code and separately licensed weights for designing enzymes around a catalytic site; it depends on AlphaFold 3 and JAX. A Vals.ai post describes Claude Opus 5.5 agents predicting two room-temperature magnetic semiconductors through simulation; neither band gap nor spin sorting has been measured. [AlphaProtein Novo](https://github.com/google-deepmind/alphaprotein-novo) · [Vals.ai](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors)
- **Hosted models:** OpenAI's Intelligent UI builds interactive ChatGPT answers; Nano Banana 2.1 edits images in Google products; Claude Haiku 5.5 is a low-cost API model. Mistral Large 4 is in API preview, with weights promised for late October. At about 1.05 trillion total parameters, even four-bit weights would need roughly 525 GB. [OpenAI](https://openai.com/index/gpt-6-for-everyone/) · [Google](https://deepmind.google/models/model-cards/nano-banana-2-1/) · [Anthropic](https://www.anthropic.com/claude-haiku-5-5) · [Mistral](https://mistral.ai/news/mistral-large-4/)
- **Visual generation without a local path:** Kandinsky 6.0 Lite has a 3B video generator, but its required files total about 26.7 GB, including a 16.6 GB text encoder. Iris-3B's text-to-image weights alone are 11.95 GB in fp32, and its code requires CUDA. [Kandinsky 6.0](https://github.com/kandinskylab/kandinsky-6) · [Iris](https://speridlabs.com/research/iris)

## What changed since the previous weekly report

The [October 4 report](./report-2026-10-04-video-ai-news.md) recommended AstaBrief for writing cited reports from supplied excerpts, while leaving retrieval as separate work. EmbeddingGemma 2 fills part of that gap: it can index local documents and select the excerpts a writer model reads. Running both at once is untested here; the text embedder adds well under 1 GB to AstaBrief's estimated 6.2 GB at an 8,192-token context. Earlier recommendations were not retested.

## Technical appendix

### Complete video chapter inventory

All 22 chapters below match the official description in source order. “❌ Hosted” means no verified downloadable local configuration; “⚠️ Unverified” records unresolved fit or release evidence. Research and non-model stories use “— N/A” where an inference verdict would mislead.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=0s) | AI news intro | Editorial | — N/A; introduces the roundup. |
| [01:08](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=68s) | [WorldPlay 2](https://worldplay2.github.io/) | Open weights / interactive world model | ❌ Outside budget; 69.8 GB checkpoint plus a 126 GB Wan2.2 base; CUDA. |
| [02:24](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=144s) | [MSFlow](https://yu1ut.com/MSFlow-HP/) | Open weights / text-to-motion research | ⚠️ Unverified; 0.55 GB checkpoints, but the Mac runtime path and evaluation dependencies are undocumented. |
| [03:30](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=210s) | [Kandinsky 6.0](https://github.com/kandinskylab/kandinsky-6) | Open weights / video with audio | ❌ Outside budget; Lite repository totals 26.7 GB; NVIDIA setup. |
| [04:54](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=294s) | [GPT-6 Intelligent UI](https://openai.com/index/gpt-6-for-everyone/) | Hosted chat feature | ❌ Hosted; ChatGPT feature using GPT-6 Sol and Luna. |
| [06:23](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=383s) | [ALoDLM](https://huggingface.co/amazon/ALoDLM-8B) | Open weights / diffusion LLM | ⚠️ Experimental; small GGUFs exist but lack the diffusion decoder; official path is CUDA or fp32 CPU. |
| [08:04](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=484s) | [AlphaProtein Novo](https://github.com/google-deepmind/alphaprotein-novo) | Open code and weights / enzyme design | ⚠️ Unverified; JAX pipeline with AlphaFold 3 and multi-GPU support; no memory guidance. |
| [10:26](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=626s) | [Botanic 1](https://deepmind.google/models/gemma/gemmaverse/living-models/) | Open weights (gated) / plant genomics | ✅ Comfortable for Botanic1-M; MPS support documented; research-only license. |
| [12:20](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=740s) | [OpenAI math results](https://github.com/openai/math) | Mathematics research | — N/A; manuscripts and Lean proofs from an unreleased model. |
| [17:17](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1037s) | [Higgsfield](https://higgsfield.ai/) | Sponsored hosted creative platform | ❌ Hosted; description identifies Higgsfield as sponsor. |
| [18:50](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1130s) | [OpenAI math results, continued](https://github.com/openai/math) | Mathematics research | — N/A; continuation of the 12:20 chapter. |
| [26:37](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1597s) | [EmbeddingGemma 2](https://huggingface.co/google/embeddinggemma-2) | Open weights / multimodal embeddings | ✅ Comfortable; 310 MB Q8 text GGUF; llama.cpp, Ollama, MLX listed. |
| [28:39](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1719s) | [Mistral Large 4](https://mistral.ai/news/mistral-large-4/) | Hosted preview; weights announced | ❌ Outside budget; about 1.05T total parameters; weights not yet published. |
| [30:08](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1808s) | [GenIA](https://facebookresearch.github.io/GenIA/) | 3D reconstruction research code | ❌ Outside supported Mac path; CUDA 12.8 and SAM 3D Objects; non-commercial. |
| [30:51](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=1851s) | [Room-temperature magnetic semiconductors](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors) | Materials science case study | — N/A; agent-run simulations, not a model release. |
| [35:55](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2155s) | [FlashDexRetarget](https://holiday-robot.github.io/FlashDexRetarget/) | Robotics research code | — N/A; Isaac Sim training; README cites about 110 GB of GPU memory. |
| [36:35](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2195s) | [Iris 3B](https://speridlabs.com/research/iris) | Open weights / pixel-space image generation | ❌ Outside budget; 11.95 GB fp32 generator plus 4B text encoder; CUDA only. |
| [38:10](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2290s) | [Terra](https://cnai.epfl.ch/terra/) | Musculoskeletal locomotion research | — N/A; Linux training pipeline; GPU needed for PPO. |
| [39:35](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2375s) | [CoDimRecon](https://shuzhaoxie.github.io/CoDimRecon/) | 3D scene reconstruction research | ⚠️ Unverified; project page lists code as forthcoming. |
| [40:36](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2436s) | [DistScene](https://coolbeam.github.io/DistScene/) | 3D scene generation research | ⚠️ Unverified; code, checkpoint, and dataset listed as forthcoming. |
| [41:29](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2489s) | [Nano Banana 2.1](https://deepmind.google/models/model-cards/nano-banana-2-1/) | Hosted image generation and editing | ❌ Hosted; Gemini app and API. |
| [42:41](https://www.youtube.com/watch?v=X0_GDOkLKzQ&t=2561s) | [Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5) | Hosted LLM | ❌ Hosted; API and cloud platforms. |

### EmbeddingGemma 2 deployment

**Configuration:** Official `google/embeddinggemma-2` revision `914f7f89142e33e77833254d9c9b90c3cef7303b`; GGUF conversion `ggml-org/embeddinggemma-2-GGUF` revision `bfcd298762cc34d0357ece5ebdd31791a3a374d8` (architecture `gemma-embedding2`). Ollama library tag `embeddinggemma-2:270m` for text only.\
**Fit evidence:** Exact file sizes and a publisher on-device memory measurement on a phone; no M2 run.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Text model, Q8_0 GGUF | 309,855,456 bytes = 0.310 GB | Text-only path; BF16 GGUF is 0.558 GB. |
| Image/audio projector (`mmproj`), Q8_0 GGUF | 554,821,024 bytes = 0.555 GB | Optional; needed only for non-text inputs. BF16 is 0.982 GB. |
| Official BF16 safetensors (all encoders) | 1,488,915,288 bytes = 1.489 GB | Full multimodal model for Transformers or sentence-transformers. |
| Vector index | Depends on corpus | 768 floats per item at full size; truncating to 256 dimensions cuts storage by two-thirds. |

**Working memory:** Google reports about **191 MB active RAM for quantized text-only weights and 567 MB for the full multimodal model** on a Pixel 11 Pro. The process peak on an M2 is unknown but should sit well inside the budget; batch size and the 8,192-token context set activation memory.\
**Starting limits:** Text only, documents chunked to a few hundred tokens, 768 or 256 output dimensions, modest batches.\
**Runtime support:** Google lists Ollama, llama.cpp, MLX, sentence-transformers, Transformers, transformers.js, and LM Studio. The Ollama listing shows a 256K context, which conflicts with the card's 8,192 tokens; follow the card. Avoid float16 in Python.\
**License:** Weights tagged Apache-2.0 on Hugging Face and described as Apache 2.0 by Google; the card's license link points to a file titled for Gemma 4, so read it before redistribution.\
**Unresolved:** M2 throughput for large corpora, retrieval quality at Q8 versus BF16, and audio/video support in local runtimes.

[Card and prefixes](https://huggingface.co/google/embeddinggemma-2) · [Pinned GGUF files](https://huggingface.co/ggml-org/embeddinggemma-2-GGUF/tree/bfcd298762cc34d0357ece5ebdd31791a3a374d8) · [Ollama tags](https://ollama.com/library/embeddinggemma-2) · [Announcement](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2)

### Botanic1-M deployment

**Configuration:** `living-models/Botanic1-M` revision `09f3998aeef9d66715193df24796ef2823e1ba10`, loaded with Transformers and `trust_remote_code=True`; card lists `torch>=2.8` and `transformers>=4.57`.\
**Fit evidence:** Parameter count and fp32 weight size, plus the publisher's statement that the pure-PyTorch path runs on MPS with parity checks for S and M; no M2 run.

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Botanic1-M weights | About 2.8 GB fp32 (687,526,665 parameters) | Bidirectional Mamba-2 encoder; no attention, so no KV cache. |
| Botanic1-S / Botanic1-L | About 1.3 GB / 8.4 GB fp32 | S is a lighter first test; L leaves little headroom and lacks reported MPS parity checks. |
| Reference genome / variant files | User-supplied | Sequence extraction and variant calling happen outside the model. |
| Optional CUDA kernels | Not used on Mac | `mamba-ssm` speedups apply only to CUDA. |

**Working memory:** Weights plus a scan transient that grows with batch size × sequence length; the card gives no M2 peak.\
**Starting limits:** Batch 8, equal-length windows (padding is not masked), at most 8,191 bases.\
**Runtime support:** Pure PyTorch on CPU, MPS, and CUDA in fp32.\
**License:** “livingmodels-research” terms: non-commercial research only, no production, clinical, or diagnostic use; gated download.\
**Unresolved:** MPS speed, how the 128 kb context in the case study relates to the released 8,191-base limit, and accuracy on species outside the training set.

The card reports a zero-shot AUROC of 0.713 on its benchmark. The melon Recall@1 of 0.90 and the 15.9% top-0.1% rate across more than 500 validated mutations come from the Gemmaverse write-up's combined Gemma-plus-Botanic workflow. [Card](https://huggingface.co/living-models/Botanic1-M) · [Large variant](https://huggingface.co/living-models/Botanic1-L) · [Case study](https://deepmind.google/models/gemma/gemmaverse/living-models/)

### ALoDLM-8B near-miss

ALoDLM's method lies in its decoder: it loops shared layers over a block of draft tokens, commits confident tokens early, and keeps refining the rest under a learned halting rule. The official checkpoint (revision `2c4623d93e285bea86a940c2801eac4509862edd`) is **16.381 GB in BF16 shards** and needs extra files, `exit_gate.pt` and `alodlm_config.json`, that standard Transformers loading ignores. The README shows CUDA examples only; the model card mentions fp32 CPU, which would need about 33 GB for weights.

`mradermacher/ALoDLM-8B-GGUF` offers a **5.028 GB Q4_K_M** file, but the GGUF reports the plain `qwen3` architecture, and its usage examples call ordinary `llama-cli` and `llama-server`. Running it that way generates one token at a time with the fine-tuned weights, without the adaptive loop. Its quality in that mode has not been evaluated, and the published speed and benchmark results do not apply. Code and weights are CC BY-NC 4.0, and the optimized engine carries extra WeDLM terms. [Model card](https://huggingface.co/amazon/ALoDLM-8B) · [Code](https://github.com/amazon-science/ALoDLM) · [GGUF](https://huggingface.co/mradermacher/ALoDLM-8B-GGUF)

### Visual and world-model dependencies

**Kandinsky 6.0 Lite:** The distilled Lite repository (revision `efbaeb9961770cc82fece5b9cb2197049d8c983c`) holds a 6.38 GB transformer, a **16.58 GB Qwen2.5-VL text encoder** in five shards, a 0.49 GB CLIP encoder, a 0.99 GB video VAE, a 1.71 GB audio VAE, and a 0.49 GB vocoder: about **26.7 GB** in all. The README targets NVIDIA GPUs with offloading. Diffusers support exists, but no quantized encoder or MPS path was found. Code is MIT. [Repository](https://github.com/kandinskylab/kandinsky-6) · [Lite files](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers)

**Iris-3B:** Revision `7445443349bc9abe3c96f01ff793e2098ca012b3` stores the text-to-image model as **11.95 GB fp32**, with separate 11.95 GB depth and upscaler models. A frozen Qwen3-VL-4B text encoder downloads on first run; its roughly 8–9 GB BF16 size is estimated from the parameter count. The custom code states that it needs an NVIDIA GPU with CUDA. Weights are Apache-2.0. [Card](https://huggingface.co/speridlabs/iris-3b) · [Project](https://speridlabs.com/research/iris)

**WorldPlay 2:** The 4-step model alone is **69.8 GB** (two 34.9 GB experts) and loads on top of Wan2.2 I2V-A14B, whose repository totals **126.2 GB**. Launch scripts default to eight GPUs; the hosted Reactor configuration uses four B200s. The license is CC BY-NC 4.0. [Code](https://github.com/WorldPlay2/WorldPlay2) · [Fast checkpoint](https://huggingface.co/aejion/WorldPlay2-Fast) · [Base model](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B)

**MSFlow:** Two 0.55 GB checkpoints generate body-motion sequences from text. The weights are Apache-2.0, with HumanML3D terms attached, and the code is CC0. The README notes the repository may become private. It does not mention CUDA, but it also does not document a Mac path, and evaluation needs external datasets and evaluators. It is small enough to try, but it is a research tool rather than a ready motion app. [Code](https://github.com/yu1ut/MSFlow) · [Weights](https://huggingface.co/ly-corporation/MSFlow)

### Science, research, and hosted notes

**OpenAI mathematics:** Most of the 719 manuscripts came from one unreleased model, at about three hours of ChatGPT Pro thinking compute per result, across roughly 4,000 posed problems. Two highlighted results, a zeta zero-free region and a Hodge-conjecture case, are listed as exceptions to that process, and the zeta write-up was human-edited. Corrections are published as new versions. This report did not check the proofs or run the Lean build. [Repository](https://github.com/openai/math)

**AlphaProtein Novo:** Code is Apache-2.0; generator weights download separately under their own terms, and the folding step uses AlphaFold 3 weights under AlphaFold 3's terms. The JAX environment installs for CUDA 12 or CPU only, and no memory requirements are stated. A CPU-only Mac run was not assessed. Outputs are design predictions that still need laboratory testing. [Repository](https://github.com/google-deepmind/alphaprotein-novo)

**Magnetic semiconductors:** The post's predictions rest on density functional theory calculations run by agents. One candidate, YBaMnFeO₅, has not been made, and standard synthesis may scramble its ordering. The other, KV[Cr(CN)₆], was made in 1999 and is magnetically ordered to 376 K, but its predicted spin-sorting property has not been measured. [Vals.ai post](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors)

**Robotics and 3D:** FlashDexRetarget trains one RL policy to turn many human hand demonstrations into robot-hand motions; its README cites about 110 GB of GPU memory, or 16 GB GPU plus about 100 GB RAM with CPU buffers. Terra retargets motion to muscle-driven bodies on Linux. GenIA aligns the frozen SAM 3D Objects model to input images at inference time, using CUDA 12.8. CoDimRecon and DistScene have not released code. [FlashDexRetarget](https://github.com/Holiday-Robot/FlashDexRetarget) · [Terra](https://github.com/amathislab/terra) · [GenIA](https://github.com/facebookresearch/GenIA)

**Hosted models:** Intelligent UI uses GPT-6 Sol for paid ChatGPT tiers and GPT-6 Luna for Free and Go. Nano Banana 2.1 builds on Gemini 3.6 Flash. Claude Haiku 5.5 lists $0.10 input and $0.50 output per million tokens for prompts up to 100K. Mistral states 52B active of about 1.05T total parameters for Large 4; its license is not yet published. [OpenAI](https://openai.com/index/gpt-6-for-everyone/) · [Nano Banana 2.1](https://deepmind.google/models/model-cards/nano-banana-2-1/) · [Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5) · [Mistral docs](https://docs.mistral.ai/models/mistral-large-4-0)

### Method and verification limits

- **Video evidence:** Retrieved official metadata, title, description, and chapter markers. Publication time is **2026-10-11 03:27:53 UTC**; duration is 2,711 seconds. The description lists 22 chapters.
- **Captions:** yt-dlp's English auto-caption download returned HTTP 429 twice. This is a chapter-based report; spoken claims within chapters were not checked.
- **Primary sources:** Inspected project pages, GitHub READMEs, model cards, and Hugging Face file metadata on 2026-10-12. The OpenAI announcement returned HTTP 403 to the web reader, so its details come from search excerpts of the official page. Mistral Large 4 has no description link; Mistral's own announcement and documentation were used. Botanic1 config files are gated, so architecture details come from the public model cards.
- **Memory interpretation:** MB/GB are decimal. Download size, resident memory, and peak memory differ. Phone RAM figures for EmbeddingGemma 2 are publisher measurements on different hardware.
- **Coverage:** All 22 chapters are preserved, including the sponsor slot and the two-part math segment, which shares one source.
- **Local verification:** Documentation and artifact inspection only. No model was downloaded for execution, installed, or benchmarked.

## Sources

- **Video:** [AI Search roundup](https://www.youtube.com/watch?v=X0_GDOkLKzQ) — official metadata and 22 chapters.
- **WorldPlay 2:** [Project](https://worldplay2.github.io/) · [Code](https://github.com/WorldPlay2/WorldPlay2) · [Fast checkpoint](https://huggingface.co/aejion/WorldPlay2-Fast) · [Wan2.2 base](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B).
- **MSFlow:** [Project](https://yu1ut.com/MSFlow-HP/) · [Code](https://github.com/yu1ut/MSFlow) · [Weights](https://huggingface.co/ly-corporation/MSFlow).
- **Kandinsky 6.0:** [Code](https://github.com/kandinskylab/kandinsky-6) · [Lite distilled files](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-distill-5s-Diffusers).
- **GPT-6 Intelligent UI:** [OpenAI announcement](https://openai.com/index/gpt-6-for-everyone/).
- **ALoDLM:** [Model card](https://huggingface.co/amazon/ALoDLM-8B) · [Code](https://github.com/amazon-science/ALoDLM) · [Community GGUF](https://huggingface.co/mradermacher/ALoDLM-8B-GGUF).
- **AlphaProtein Novo:** [Repository](https://github.com/google-deepmind/alphaprotein-novo).
- **Botanic 1:** [Gemmaverse case study](https://deepmind.google/models/gemma/gemmaverse/living-models/) · [Collection](https://huggingface.co/collections/living-models/botanic1-6a97f4e3c33f3d109a75057d) · [Botanic1-M](https://huggingface.co/living-models/Botanic1-M) · [Botanic1-L](https://huggingface.co/living-models/Botanic1-L).
- **OpenAI math:** [Repository](https://github.com/openai/math).
- **Higgsfield:** [Official platform](https://higgsfield.ai/) — sponsor.
- **EmbeddingGemma 2:** [Announcement](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2) · [Model card](https://huggingface.co/google/embeddinggemma-2) · [GGUF](https://huggingface.co/ggml-org/embeddinggemma-2-GGUF) · [Ollama](https://ollama.com/library/embeddinggemma-2).
- **Mistral Large 4:** [Announcement](https://mistral.ai/news/mistral-large-4/) · [Model documentation](https://docs.mistral.ai/models/mistral-large-4-0).
- **GenIA:** [Project](https://facebookresearch.github.io/GenIA/) · [Code](https://github.com/facebookresearch/GenIA).
- **Magnetic semiconductors:** [Vals.ai post](https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors).
- **FlashDexRetarget:** [Project](https://holiday-robot.github.io/FlashDexRetarget/) · [Code](https://github.com/Holiday-Robot/FlashDexRetarget).
- **Iris 3B:** [Project](https://speridlabs.com/research/iris) · [Weights](https://huggingface.co/speridlabs/iris-3b).
- **Terra:** [Project](https://cnai.epfl.ch/terra/) · [Code](https://github.com/amathislab/terra).
- **CoDimRecon:** [Project](https://shuzhaoxie.github.io/CoDimRecon/).
- **DistScene:** [Project](https://coolbeam.github.io/DistScene/).
- **Nano Banana 2.1:** [Model card](https://deepmind.google/models/model-cards/nano-banana-2-1/).
- **Claude Haiku 5.5:** [Anthropic](https://www.anthropic.com/claude-haiku-5-5).
