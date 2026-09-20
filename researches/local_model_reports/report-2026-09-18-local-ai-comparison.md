# Local AI Model Comparison for a 16 GB M2 Pro MacBook Pro

**As of:** 2026-09-18<br>
**Machine:** MacBook Pro 14-inch (Mac14,9), Apple M2 Pro, 10-core CPU, 16-core GPU, 16 GB unified memory<br>
**Goal:** compare current models by real local speed, memory, quality, modalities, context, licensing, and day-to-day usefulness—not merely whether a quantized file can technically open.

## Bottom line

The best models for this machine are not the newest flagships. My practical shortlist is:

1. **Qwen3.5-9B 4-bit** — best all-round local assistant with image/video understanding and strong tool use.
2. **Ornith 1.5 9B 4-bit** — best local coding/agent model.
3. **Qwen3.5-4B 4-bit** — best balance of speed and memory headroom while a browser and IDE remain open.
4. **Gemma 4 12B Unified 4-bit** — best local choice when audio understanding matters.
5. **Ling-3.0-tiny 4-bit** — fastest serious text-only option, though its long reasoning traces can erase some of that speed advantage.

**DeepSeek V4.1 Flash** and the newest open Qwen, **Qwen3.8-Flash-Next**, are included below, but neither remotely fits in 16 GB. They are server/API models. Qwen's newest release overall, **qwen3.8-omni-flash**, is hosted-only.

If I were installing only three models, I would use **Qwen3.5-4B**, **Ornith 1.5 9B**, and **Gemma 4 12B**. Together they cover fast general work, coding, vision, and audio without pretending that a 300+ GB flagship is a laptop model.

## How “fits” is defined

The laptop has 16 GB of unified memory, but macOS, the display server, browser, IDE, and runtime need part of it. In ordinary use, the safe model budget is roughly **8–11 GB**, as explained in [the memory-budget note](./memory-budget.md). A model can be loadable yet still be a poor daily choice because it forces memory compression, swap, a tiny context, or closing every other app.

Ratings used here:

- **Comfortable:** enough headroom for normal apps and an 8K–16K working context.
- **Good:** works well at 4K–8K; long context or heavier apps may need care.
- **Tight:** technically usable, but swap or app-closing is likely.
- **No fit:** even the smallest usable quant is far beyond physical memory.

Advertised 128K, 262K, or 1M context is not the same as practical local context. KV cache and runtime buffers grow with context, so **8K–16K is the sensible target** for most 4–12B models on this machine.

## Local performance and RAM

Generation speed is output tokens per second. Unless marked otherwise, the comparison uses a 4-bit model and a 4K prompt. RAM means peak runtime memory, not just the downloaded file. The first three oMLX results are especially useful because they were recorded on the same M2 Pro / 16-GPU / 16-GB configuration.

| Model | Local format | Gen speed at 4K | RAM at 4K / file floor | Practical context | Fit | Best use |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| **Qwen3.5-4B** | 4-bit | **55.9 tok/s** | **4.5 GB** | 8K–32K | Comfortable | Fast daily assistant, vision, tools |
| **Qwen3.5-9B** | 4-bit | **34.4 tok/s** | **6.5 GB** | 8K–16K | Comfortable | Best general quality/size balance |
| **Ornith 1.5 9B** | 4-bit | **34.1 tok/s** | **6.4 GB** | 8K–16K | Comfortable | Coding and agentic work |
| **Ling-3.0-tiny** | 4-bit | **~60–75 tok/s estimated** | **~5.7–6.0 GB** | 8K–32K | Comfortable | Very fast text/reasoning |
| **Gemma 4 12B Unified** | 4-bit | **21.6 tok/s** | **8.1 GB** | 4K–8K | Good | Local audio + image + text |
| **DeepSeek-Coder-V2-Lite 16B** | Ollama Q4_0 | **81.5 tok/s measured** | **10.0 GB loaded** | 4K | Tight | Fast legacy code completion |
| **Qwen3.8-27B** | ~2-bit only | **~10–12 tok/s estimated** | **11–13 GB** | 2K–4K | Experimental | Curiosity, not a daily driver |
| **Qwen3.8-Flash-Next** | smallest complete ~1-bit | — | **72.5 GB file minimum** | — | No fit | Server/large workstation |
| **DeepSeek V4.1 Flash** | smallest complete ~2-bit | — | **~335–366 GB file minimum** | — | No fit | Server/API frontier model |
| **qwen3.8-omni-flash** | API only | provider-dependent | cloud | up to 1M | Not local | Hosted audio/video/vision |

Sources for the hardware-matched rows: [Qwen3.5-4B oMLX result](https://omlx.ai/benchmarks/performance/w7awuhua), [Qwen3.5-9B oMLX result](https://omlx.ai/benchmarks/performance/bz4abedv), and [Ornith 1.5 9B oMLX result](https://omlx.ai/benchmarks/performance/76xv3opq). The [Gemma 4 result](https://omlx.ai/benchmarks/performance/rd4szf61) used the same M2 Pro 16-core GPU but a 32-GB host, so its 8.1-GB model peak is informative while overall system headroom is not directly comparable. The [Ling result](https://omlx.ai/benchmarks/performance/0zjonnaf) was measured on a faster M2 Max; its M2 Pro number above is therefore an explicitly labeled estimate.

### Measurement made on this Mac

The already-installed `deepseek-coder-v2:16b` was tested locally through Ollama with a 4K context:

- Warm generation: **81.46 tok/s** for 512 output tokens.
- Prompt processing: **92.50 tok/s**.
- Loaded working set: **10.0 GB**, reported as 100% GPU-resident.
- Cold load: **9.33 seconds**; warm load: **0.18 seconds**.
- On-disk model: **8.9 GB**, Q4_0.

This is a useful reminder that parameter count alone does not predict speed: DeepSeek-Coder-V2-Lite has 16B total parameters but activates about 2.4B per token. It is fast, but its 10-GB working set leaves little room for the rest of the system, and its 2024-era quality is now behind the best 9B coding models.

## Capability matrix

“Video” generally means sampled frames rather than native video generation. All local models here produce text; none produces speech or images.

| Model | Text | Image | Video input | Audio input | Tool use | Offline | License |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| Qwen3.5-4B / 9B | Yes | Yes | Yes | No | Yes | Yes | Apache-2.0 |
| Ornith 1.5 9B | Yes | Optional vision projector | — | No | Yes | Yes | MIT |
| Ling-3.0-tiny | Yes | No | No | No | Yes | Yes | MIT |
| Gemma 4 12B Unified | Yes | Yes | Frames | **Yes** | Yes | Yes | Apache-2.0 |
| DeepSeek-Coder-V2-Lite | Yes | No | No | No | Limited/legacy | Yes | DeepSeek model license |
| Qwen3.8-27B | Yes | Yes | Yes | No | Yes | Only at severe 2-bit | Apache-2.0 |
| Qwen3.8-Flash-Next | Yes | Yes | Yes | No | Yes | Not on this Mac | Apache-2.0 |
| DeepSeek V4.1 Flash | Yes | Yes | Not advertised as native video | No | Yes | Not on this Mac | MIT |
| qwen3.8-omni-flash | Yes | Yes | **Yes** | **Yes, including spatial audio** | Yes | **No—hosted API** | Service terms |

Model sources: [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B), [Ornith 1.5](https://ornith.ai/ornith_1_5.html), [Ling-3.0-tiny](https://huggingface.co/inclusionAI/Ling-3.0-tiny), [Gemma 4 12B](https://huggingface.co/google/gemma-4-12B), and [DeepSeek-Coder-V2-Lite](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct).

## Benchmark quality

These are official, full-precision model-card results, not results from the 4-bit files used for the speed table. They are directional rather than perfectly apples-to-apples: vendors may use different prompts, harness versions, tool environments, and inference budgets. For local selection, a high score matters only after the model passes the memory test.

| Model | Reasoning | Coding / agent benchmark | Vision | Interpretation |
| --- | ---: | ---: | ---: | --- |
| **Qwen3.5-4B** | GPQA Diamond **76.2** | LiveCodeBench v6 **55.8** | MMMU-Pro **66.3** | Remarkably capable for 4B; best speed/headroom choice |
| **Qwen3.5-9B** | GPQA Diamond **81.7** | LiveCodeBench v6 **65.6** | MMMU-Pro **70.1** | Best balanced local general model |
| **Ornith 1.5 9B** | GPQA Diamond **86.4** | SWE-bench Verified **70.6**; Terminal-Bench 2.1 **46.2** | No comparable published score | Strongest local coding specialist here |
| **Gemma 4 12B** | GPQA Diamond **78.8** | LiveCodeBench v6 **72.0** | MMMU-Pro **69.1** | Strong multimodal model; audio is the differentiator |
| **Ling-3.0-tiny** | Artificial Analysis Index **25** | Agentic Index **16** | — | Very fast, but below the 9B leaders on quality |
| **Qwen3.8-27B** | GPQA Diamond **89.2** | Terminal-Bench 2.1 **73.0**; SWE-bench Pro **61.7** | RealWorldQA **85.9** | Excellent model, poor 16-GB fit |
| **Qwen3.8-Flash-Next** | GPQA Diamond **91.7** | LiveCodeBench v6 **91.9**; SWE-bench Pro **62.5** | RealWorldQA **88.5** | Frontier open model, but 72.5+ GB even at extreme quantization |
| **DeepSeek V4.1 Flash** | GPQA Diamond **90.9** | Codeforces **3471**; Terminal-Bench 2.1 **90.6**; DeepSWE **74.2** | Chartography **78.9** | Highest capability here; a datacenter model |
| **qwen3.8-omni-flash** | Not yet published in a comparable public card | — | — | Same-day hosted release; judge after independent evaluations |

The Qwen3.5 scores come from the [official Qwen3.5-9B card](https://huggingface.co/Qwen/Qwen3.5-9B), which includes the family table. Qwen3.8 results come from the [Qwen3.8-27B card](https://huggingface.co/Qwen/Qwen3.8-27B) and [Qwen3.8-Flash-Next card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next). DeepSeek's results are from the [official V4.1 Flash release](https://www.deepseek.com/en/news/deepseek-v4-1-flash/) and [model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash).

## The requested frontier models

### DeepSeek V4.1 Flash: impressive, but not a laptop model

DeepSeek V4.1 Flash was released on 2026-09-10. Its architecture uses a **552B-parameter MoE backbone**, activating 8B parameters during input processing and 16B during generation, plus a **196B-parameter Engram conditional-memory component**. The full published checkpoint is described as roughly **763B parameters** when auxiliary weights are included. It has a 1M-token context and native image understanding.

The architecture is efficient relative to its size, not small in absolute terms. Public quantization evidence makes the local conclusion unambiguous:

- A complete community Q2 build is roughly **335–366 GB**.
- A normal Q4 build is about **519 GB**, before comfortable runtime overhead.
- A roughly 170-GB “backbone-only” experiment omits the Engram memory, MTP/auxiliary components, and vision path, so it is not a complete runnable substitute.
- DeepSeek's own deployment discussion describes a cluster-scale setup involving roughly 2,000 GPUs plus storage.

See the [official checkpoint](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash), [complete public GGUF files](https://huggingface.co/antirez/deepseek-v4.1-flash-gguf/tree/main), and the [mixed-quant experiment](https://huggingface.co/apetersson/DeepSeek-V4.1-Flash-MixedQ2-GGUF).

**Verdict:** use it through an API or remote GPU server when its quality justifies sending the task off-device. There is no honest local tokens-per-second figure for this Mac because the model cannot be loaded.

### What “Qwen's newest model” means today

Qwen now has three relevant “newest” answers:

1. **Newest release overall: `qwen3.8-omni-flash` (2026-09-18).** It accepts text, image, audio, and video, including multichannel spatial audio, and offers up to a 1M context. It is an API-only Qwen Cloud model; there are no downloadable weights to benchmark locally.
2. **Newest open-weight flagship: Qwen3.8-Flash-Next (2026-08-26).** It has a 125B main model with 6B active parameters, plus large n-gram memory and MTP components—about 177–180B parameters in the complete package. The smallest complete public quant is still **72.5 GB**; Q4 is about **111 GB**.
3. **Newest dense open model: Qwen3.8-27B.** Its Q4 file is about **17.4 GB**, already larger than physical memory after runtime overhead. A 2-bit build can squeeze into roughly 11–13 GB, but quality loss, a short context, and system swapping make it a demonstration rather than a recommendation.

Qwen's [official model changelog](https://docs.qwencloud.com/changelog/models) identifies the hosted releases. Quant sizes are documented in the [Qwen3.8-Flash-Next GGUF collection](https://huggingface.co/unsloth/Qwen3.8-Flash-Next-GGUF) and [Qwen3.8-27B GGUF card](https://huggingface.co/bartowski/Qwen3.8-27B-GGUF/blob/main/README.md).

**Verdict:** the newest Qwen that *comfortably fits* this Mac remains **Qwen3.5-9B**, or **Qwen3.5-4B** when latency and multitasking matter more than the last increment of quality.

## Model-by-model recommendations

### Qwen3.5-4B — fastest safe default

- **Why choose it:** 56 tok/s, 4.5-GB peak at 4K, vision/video input, tool calling, and lots of system headroom.
- **Trade-off:** noticeably weaker than 9B on difficult reasoning and sustained coding.
- **Use it for:** quick chat, document/image inspection, lightweight agents, and working alongside a full browser/IDE setup.

### Qwen3.5-9B — best overall

- **Why choose it:** strong general and vision scores at only 6.5 GB and 34 tok/s.
- **Trade-off:** slower than 4B; no audio input.
- **Use it for:** the main local assistant, screenshots, PDFs converted to images, research synthesis, and tool-driven workflows.

At 16K context, the same-machine oMLX run still produced **27.4 tok/s** with an **8.6-GB** model peak ([long-context result](https://omlx.ai/benchmarks/performance/l6njy98t)), though total system pressure will depend on other open apps.

### Ornith 1.5 9B — best coding model

- **Why choose it:** excellent SWE-bench results, 34 tok/s, and nearly the same RAM footprint as Qwen3.5-9B.
- **Trade-off:** less broadly multimodal; vision requires the optional projector.
- **Use it for:** repository work, terminal agents, patches, debugging, and code review.

### Gemma 4 12B Unified — best local audio/omnimodal model

- **Why choose it:** the only comfortable local candidate here that understands audio directly as well as text and images.
- **Trade-off:** 22 tok/s and 8.1 GB at 4K leave less system headroom; use 4K–8K context.
- **Use it for:** speech/audio analysis, image-plus-audio tasks, and one-model multimodal workflows.

### Ling-3.0-tiny — fastest modern text model

- **Why choose it:** only 1.3B of its roughly 8B MoE parameters are active per token, so it should be very fast on this GPU.
- **Trade-off:** text only; weaker overall quality than Qwen3.5-9B or Ornith; verbose reasoning can increase time-to-answer even when tok/s is high.
- **Use it for:** high-throughput summarization, drafting, and text-only reasoning where speed matters.

### DeepSeek-Coder-V2-Lite — fast but no longer efficient enough

- **Why keep it:** the measured 81.5 tok/s is excellent and it is already installed.
- **Why replace it:** a 10-GB working set is expensive for a dated code model; Ornith provides much better current coding quality in about 6.4 GB.
- **Use it for:** low-latency code completion if its behavior already suits the workflow. Do not select it solely from its speed number.

## Other vectors worth considering

### Time to a useful answer

Tokens per second measures the engine, not the experience. Thinking models may generate hundreds or thousands of hidden reasoning tokens. A 60 tok/s model that overthinks can finish later than a 34 tok/s model with better instruction-following. Compare wall-clock completion time on real tasks before choosing a default.

### Quantization sensitivity

4-bit is the practical quality floor for a daily model. A 27B model at 2-bit may score well in full precision but can lose enough reasoning and instruction fidelity that a clean 9B 4-bit model is better. This is why Qwen3.8-27B is not the winner here despite its benchmark table.

### Memory headroom and swap

Sustained swap makes an interactive model feel inconsistent, increases SSD writes, and leaves less memory for tool servers or image/audio projectors. Prefer a 4.5–6.5-GB peak for normal multitasking. Reserve 8–10 GB models for a focused session.

### Privacy and availability

Local models keep prompts, files, audio, and images on the Mac and continue working without network access. DeepSeek V4.1 Flash and qwen3.8-omni-flash can be much more capable, but using them introduces provider retention terms, network latency, cost, rate limits, and service availability.

### Runtime support

For Apple Silicon, prefer **MLX/oMLX** when a good port exists; it generally provides efficient unified-memory use and straightforward multimodal support. **llama.cpp, LM Studio, or Ollama** remain useful for GGUF compatibility and easy serving. Compare models within the same runtime where possible because prompt processing, cache type, and kernels can materially change results.

## Recommended setup

| Slot | Model | Quant | Reason |
| --- | --- | --- | --- |
| Fast assistant | Qwen3.5-4B | 4-bit | Maximum headroom and responsive multimodal chat |
| Main assistant | Qwen3.5-9B | 4-bit | Best all-round quality that comfortably fits |
| Coding | Ornith 1.5 9B | 4-bit | Best current coding/agent quality per GB |
| Audio/multimodal | Gemma 4 12B Unified | 4-bit | Native audio understanding |
| Optional fast text | Ling-3.0-tiny | 4-bit | High text throughput |
| Remote frontier | DeepSeek V4.1 Flash or qwen3.8-omni-flash | API | Use only when local quality is insufficient |

The simplest everyday configuration is **Qwen3.5-9B at 8K context**. Switch to **Qwen3.5-4B** when many apps are open, **Ornith** for code, and **Gemma 4** for audio. Treat the newest DeepSeek and Qwen flagships as remote escalation paths, not downloads for this laptop.

## Reproducibility notes

- Local DeepSeek test date: 2026-09-18, Ollama, Q4_0, 4K context, one warm 512-token generation after a cold 256-token run.
- Community oMLX results may use different runtime versions, sampling, and cache settings; they are evidence-quality estimates, not guarantees.
- Benchmark scores are vendor-reported and may change as evaluation harnesses are corrected.
- Model RAM grows with prompt length and multimodal projectors. Add safety margin rather than treating a table value as a hard maximum.
- “Fits” in this report means useful alongside macOS, not merely that bytes can be streamed from SSD.
