# Local Runnability: Models from AI News Video (2026-09-26)

**Compiled:** 2026-09-26  
**Source video:** *Claude Opus 4.7, Qwen 3.6, Happy Oyster, realtime 3D worlds, new Google TTS: AI NEWS* — AI Search, 37:06.
**Hardware target:** Apple M2 MacBook Pro, 16 GB unified memory  
**Local stack assumption:** macOS, Metal / MLX / llama.cpp / Ollama / PyTorch-MPS where supported; **no CUDA**  
**Practical memory rule:** 16 GB unified memory is not 16 GB of disposable VRAM. macOS, runtime state, KV cache, activations, image/video tensors, and application overhead all share the same pool.

**Freshness note:** the source video is an April 2026 news roundup. Release status and downloadable artifacts below were re-checked on **2026-09-26**. Several projects have changed materially since the video was published.

### Verdict legend

- ✅ **Comfortable:** there is a realistic Apple-local path with enough memory headroom.
- ⚠️ **Experimental:** raw weights may fit, but backend support, activations, quantization quality, or missing Apple support makes it non-turnkey.
- ❌ **No:** the intended workflow does not realistically fit this 16 GB M2.
- **n/a:** hosted service, research method, benchmark, hardware story, or otherwise not a standalone local checkpoint.

---

## TL;DR

The most important local result in this video is **Ternary Bonsai 8B**. Its current Apple-native MLX artifact is only **2.30 GB**, despite having 8.19B parameters, and the publisher explicitly supports MLX on Apple Silicon. This is the one item from the roundup that I would call straightforwardly useful on this machine.

**Qwen 3.6 35B-A3B is not a “3B model” for memory purposes.** The official repository is 71.9 GB, and the Apple MLX 4-bit conversion is still 20.4 GB. The ~3B active-parameter figure reduces per-token compute, not the number of expert weights that need to reside somewhere. Community GGUF builds only get below 16 GB by going into aggressive ~2-bit quantization, where the quantizer itself labels several variants “low,” “very low,” or “extremely low” quality.

For video generation, **Motif-Video 2B is the closest near-miss**. The official default path expects ~30 GB VRAM; CPU offload gets it to ~19 GB, FP8 to ~15 GB, and a CUDA/SageAttention Q4 experiment reports 12.53 GB peak allocation. That makes reduced-resolution experimentation conceivable, but the published low-memory numbers are still CUDA-centric and leave very little unified-memory headroom on a 16 GB Mac.

For 3D, **WildDet3D** and the **WorldMirror 2.0** component of HY-World are interesting because their checkpoint sizes fit on paper. The blockers are software rather than raw storage: WildDet3D's official desktop inference code is explicitly CUDA-based, while HY-World recommends CUDA 12.8 and FlashAttention.

**GameWorld** is locally runnable as an evaluation harness rather than as a model. Its Python + Chromium benchmark environment is lightweight enough for the Mac, although the example self-hosted VLM in its documentation is far too large for this machine.

### Practical shortlist

| Item | Verdict | Why it matters on this Mac |
|---|---:|---|
| **Ternary Bonsai 8B** | ✅ | Best direct local candidate; 2.30 GB MLX artifact and native Apple path. |
| **GameWorld** | ✅ harness | Benchmark itself runs locally; model can be remote or separately selected. |
| **WildDet3D** | ⚠️ | 4.7 GB weights fit, but official desktop runtime is CUDA-only. |
| **HY-World: WorldMirror 2.0 only** | ⚠️ | 5.05 GB checkpoint fits, but official stack is CUDA/FlashAttention-oriented. |
| **Motif-Video 2B** | ⚠️ | Quantized memory is near the limit; Mac backend is not the publisher's validated path. |
| **Qwen 3.6 35B-A3B** | ⚠️ | Only extreme low-bit GGUFs fit; normal 4-bit MLX does not. |
| **AniGen / Lyra 2 / full HY-World / OmniShow** | ❌ | Checkpoint size or video-generation backbone exceeds this machine's practical envelope. |

---

## Runnability table — all substantive chapters

Timestamps below follow the source video's chapter ordering.

| Item | Video | Kind | Weights / access | Fits 16 GB M2? | Local reality |
|---|---:|---|---|---:|---|
| **Prompt Relay** | 1:00 | Video-generation inference method | Code available; patches Wan 2.2 | ❌ reference workflow | It is training-free, but not a standalone small model. The published command targets `Wan2.2-T2V-A14B`, so local cost is still dominated by the 14B video backbone. |
| **Ternary Bonsai** | 2:45 | Ternary LLM family | Open MLX weights | ✅ | 8.19B model, 2.30 GB packed MLX artifact, native Apple Silicon support. |
| **GPT-Rosalind** | 5:35 | Specialized science model | Hosted / trusted access | n/a | Available through ChatGPT, Codex, and API to qualified customers; no local model artifact. It left research preview on Sep. 11. |
| **WildDet3D** | 7:39 | Promptable monocular 3D detection | Open ~4.7 GB checkpoint | ⚠️ | Weight size fits, and an iPhone implementation exists, but official Python setup requires CUDA 12.1, CUDA ops, and `.cuda()` inference calls. |
| **Motif-Video 2B** | 9:09 | T2V / I2V diffusion model | Open 2B model | ⚠️ | Default 720p/121-frame workflow wants ~30 GB; publisher reports 15 GB with FP8 and 12.53 GB with Q4 + SageAttention on CUDA. Not a comfortable M2 workflow. |
| **HubSpot AI content-team tool** | 10:54 | Hosted marketing/SaaS tool | Service | n/a | Product workflow rather than a downloadable inference checkpoint. |
| **AniGen** | 12:06 | Image → rigged 3D asset | Open code + checkpoints | ❌ | The AniGen checkpoint directory alone is 19.7 GB, already above the machine's total unified memory before activations and pipeline state. |
| **Happy Oyster** | 13:48 | Interactive world-model service | Client SDKs + hosted backend | n/a | Current SDKs establish RTC/service sessions and obtain temporary API keys/tickets from a backend; this is not a downloadable local world-model checkpoint. |
| **Lyra 2** | 15:05 | Generative 3D world model | Open code + weights | ❌ | 14B WAN-derived architecture; model checkpoint area is ~68.3 GB and the complete HF repo ~98.3 GB. |
| **HY-World 2.0** | 16:40 | Modular 3D world generation/reconstruction | Open code + weights | ❌ full / ⚠️ WorldMirror | Full stack includes ~80B HY-Pano and ~17B WorldStereo. WorldMirror-2 alone is ~1.2B with a 5.05 GB checkpoint, but the official environment recommends CUDA 12.8 and FlashAttention. |
| **OmniShow** | 18:03 | Controlled/UGC video generation | Code, but no released OmniShow fine-tuned checkpoint | ❌ | Current reference inference uses Wan2.1-I2V-14B; environment docs are CUDA-oriented. The project explicitly says its own checkpoints are not included. |
| **Claude Opus 4.7** | 20:22 | Hosted frontier LLM | Hosted | n/a | Proprietary Claude service, not a local checkpoint. It is now historical: Anthropic's current Opus page lists newer Opus releases and describes 5.5 as its current strongest Opus model. |
| **Qwen 3.6 35B-A3B** | 24:38 | Open MoE multimodal LLM | Open weights | ⚠️ extreme quant only | Official files total 71.9 GB; MLX 4-bit is 20.4 GB. Only aggressive ~1–2-bit GGUFs leave usable RAM headroom. |
| **Unitree sprint segment** | 26:14 | Robotics hardware/news | — | n/a | Physical-robotics story, not a downloadable local checkpoint evaluated here. |
| **Humanoid Marathon** | 26:57 | Robotics event/news | — | n/a | Hardware/event story rather than a local model release. |
| **Automated Humanoid Factory** | 27:51 | Robotics manufacturing/news | — | n/a | Industrial-production story; no relevant local checkpoint to size against the Mac. |
| **TokenLight** | 29:17 | Image-relighting research | Paper + public evaluation material | n/a / unreleased model | TokenLight is a conditional image-relighting method controlling intensity, color, diffuseness and 3D light position. I could verify the paper and VisibleFixture-60 evaluation repo, but not an official public inference checkpoint suitable for local deployment. |
| **GameWorld** | 31:30 | Multimodal-agent benchmark | Open benchmark code | ✅ harness | Python/Chromium benchmark can run locally. The documented self-hosting example uses a huge Qwen 122B model, but the harness also supports external model APIs. |
| **Gemini 3.1 Flash TTS** | 33:09 | Hosted TTS model | Gemini API / AI Studio | n/a | API model, not local weights. Google now labels 3.1 Flash TTS a legacy preview and directs new workloads to Gemini 3.8 Flash / Flash-Lite TTS. |

---

## Runnable: what is worth trying

### 1. Ternary Bonsai 8B — the clear local winner

This is the strongest local-computing story in the video.

The model has **8.19B parameters**, is based on Qwen3-8B, and publishes a **65,536-token maximum context**. The deployable MLX artifact is only **2.15 GiB / 2.30 GB**, compared with 16.38 GB for FP16. MLX and MLX Swift are explicitly supported for Apple Silicon.

There is one useful discrepancy to notice in the published numbers. The benchmark/intelligence-density table refers to Ternary Bonsai 8B as **1.75 GB**, while the actual packed MLX artifact used for deployment is **2.30 GB**. For local capacity planning, the deployable artifact is the number that matters.

On a 16 GB M2, 2.30 GB of weights leaves a great deal of room for runtime state and context. I would still avoid interpreting the advertised 65K context as the sensible starting point: context length increases KV/runtime memory, and the objective here is a responsive local model rather than proving a maximum.

**Recommended first experiment**

Start with Ternary Bonsai 8B through MLX and test:

- 4K and 8K context first;
- structured extraction / JSON;
- coding and shell assistance;
- short reasoning tasks;
- any offline task where you currently rely on a conventional 7B–8B local model.

Only after profiling memory pressure should context be pushed substantially higher.

The model card reports **83 generated tok/s on an M4 Pro 48 GB**, but that number should not be transplanted to an M2 16 GB machine. It establishes that the MLX kernels are real and performant on Apple Silicon, not what this particular MacBook will achieve.

**Verdict: ✅ install and benchmark.**

---

### 2. GameWorld — locally useful infrastructure, not a local model

GameWorld is different from the other entries: it is a **benchmark harness** for multimodal agents, covering 34 browser games and 170 tasks. The setup is essentially Python plus Playwright/Chromium.

The benchmark can point at commercial APIs or at a self-hosted model. Its documentation demonstrates local serving with Qwen3.5-122B-A10B through vLLM, which obviously does not belong on this M2, but that model is an example backend rather than a requirement of the harness itself.

That makes GameWorld locally useful if the goal is to evaluate agent loops, browser/game interaction, planning, and control.

The distinction is:

**GameWorld environment:** ✅  
**Fully local high-end multimodal GameWorld agent on 16 GB:** not established by this release.

**Verdict: ✅ worth cloning if agent evaluation is relevant.**

---

### 3. WildDet3D — weights fit; the backend does not

WildDet3D is a particularly useful example of why parameter/storage size alone is not enough.

Its main checkpoint is only about **4.7 GB**, so there is no obvious 16 GB memory wall. The project also has an actual **real-time on-device iPhone application**, proving that some version of the system can run on Apple hardware.

But the public desktop Python implementation is explicitly built around:

- PyTorch 2.5.1 from the CUDA 12.1 package index;
- `vis4d_cuda_ops`;
- inference tensors moved with `.cuda()`.

So this is not a case where changing:

`device="cuda"` → `device="mps"`

is likely to be sufficient.

There are custom CUDA components and assumptions in the reference path.

For this machine, the realistic options are therefore:

1. use the iPhone deployment if the mobile use case is sufficient;
2. treat a Mac desktop version as a porting project;
3. run the official Python implementation on an NVIDIA machine.

**Verdict: ⚠️ technically interesting, but not turnkey M2 software.**

---

### 4. HY-World 2.0 — ignore the full pipeline; WorldMirror is the interesting part

The video described HY-World 2.0 when only part of the project had been released. That is no longer current.

Tencent subsequently released HY-Pano 2.0, full world-generation inference code, and WorldStereo 2.0 weights. The repository now says all model weights, code, and technical details have been released.

That does **not** make the full system appropriate for this Mac.

The current model zoo contains:

| Component | Approx. parameters |
|---|---:|
| WorldMirror-2 | ~1.2B |
| HY-Pano-2 | ~80B |
| HY-Pano-2-Qwen | ~425M |
| WorldStereo-2 | ~17B |


The complete Hugging Face repository is about **175 GB**.

The exception is **WorldMirror-2**. Its primary safetensors file is only **5.05 GB**, making the raw checkpoint interesting for a 16 GB machine.

Unfortunately, the official environment recommends CUDA 12.8, installs a Gaussian-splatting extension, and asks for a FlashAttention backend. No first-party MPS path is documented.

So the useful conclusion is not “HY-World runs locally.” It is:

> **WorldMirror-2 is small enough to justify watching for an MLX/MPS/CoreML port; the complete HY-World generation pipeline is not a 16 GB Mac workflow.**

**Verdict: ⚠️ WorldMirror only; ❌ full pipeline.**

---

### 5. Motif-Video 2B — the video model closest to the boundary

A 2B video model sounds promising until activation memory enters the calculation.

The project's standard configuration is:

- 1280 × 736;
- 121 frames;
- ~5 seconds at 24 fps;
- BF16;
- publisher recommendation of a CUDA GPU with **30 GB+ VRAM**.

The official low-memory figures are more interesting:

| Mode | Published peak |
|---|---:|
| Standard | ~30 GB |
| CPU offload | ~19 GB |
| + FP8 | ~15 GB |
| GGUF Q8 + SageAttention | 13.44 GB |
| GGUF Q4_K_M + SageAttention | 12.53 GB |


At first glance, 12.53 GB is under 16 GB.

That is not enough to call it a viable M2 workflow.

Those measurements come from the project's CUDA/SageAttention path. On the Mac, the same 16 GB pool must also hold macOS, Python, the MPS runtime and anything not represented by that CUDA peak-allocation measurement.

Therefore:

- **default 720p:** no;
- **published Q4 CUDA configuration:** interesting evidence, but not a Mac result;
- **shorter clips / smaller resolution / experimental MPS port:** plausible experiment.

This is a good model to revisit if the project or community publishes a known-good Apple path.

**Verdict: ⚠️ research experiment, not a dependable local video generator.**

---

### 6. Qwen 3.6 35B-A3B — “3B active” is not “3B resident”

The video's efficiency story around Qwen 3.6 is real in compute terms, but it is easy to translate it incorrectly into a local-memory claim.

The official Qwen3.6-35B-A3B repository occupies **71.9 GB**.

A current MLX-community **4-bit** conversion occupies **20.4 GB**, before allocating useful context/runtime memory. It therefore does not fit this 16 GB machine.

This is exactly what one would expect from a mixture-of-experts model: only a subset of experts participates in a token's forward pass, but the rest of the model does not magically stop existing.

Community GGUFs demonstrate how far it can be pushed:

| Quant | File size | Publisher description |
|---|---:|---|
| IQ3_XXS | 15.76 GB | lower quality |
| Q2_K_L | 14.00 GB | very low quality |
| Q2_K | 13.51 GB | very low quality |
| IQ2_M | 12.96 GB | relatively low quality |
| IQ2_S | 11.91 GB | low quality |
| IQ2_XS | 11.69 GB | low quality |
| IQ2_XXS | 10.68 GB | very low quality |
| IQ1_M | 9.42 GB | extremely low quality / not recommended |


For a 16 GB machine, the 15.76 GB build is effectively useless because there is virtually no headroom. The ~11–13 GB variants are physically more plausible, but the quality trade-off is now the defining characteristic of the deployment.

If the purpose is specifically to answer:

> “Can I make Qwen 3.6 35B-A3B emit tokens on a 16 GB M2?”

then an IQ2-class GGUF is worth trying.

If the purpose is:

> “What is a sensible daily local model for this laptop?”

then Ternary Bonsai is the much cleaner candidate from this particular video.

**Verdict: ⚠️ quantization experiment only.**

---

## Near-misses and hardware walls

### Prompt Relay

Prompt Relay itself is lightweight—it modifies cross-attention at inference time and requires no retraining.

The problem is the host model.

The published usage example runs:

`Wan2.2-T2V-A14B`

with 81 frames at 832 × 480.

So Prompt Relay does not convert a large video generator into a small one. It adds control to the model that is already consuming the memory.

**M2 16 GB verdict: ❌ for the documented reference pipeline.**

---

### AniGen

AniGen is genuinely open enough to run: there is inference code and a web demo, and the pipeline produces rigged meshes plus skeletons.

But the official AniGen checkpoint directory is **19.7 GB**.

That exceeds the entire unified-memory capacity before loading inputs, decoder state, intermediate tensors, geometry processing or macOS itself.

**M2 16 GB verdict: ❌ hard memory wall.**

---

### Lyra 2

The video makes Lyra sound lightweight in part because code/repository size is not the same thing as model size.

The actual Lyra 2 architecture is derived from **WAN-14B**, with NVIDIA listing 14B model parameters.

The Hugging Face repository is ~98.3 GB, and the model checkpoint subtree alone is ~68.3 GB.

NVIDIA also released the Lyra 2 GUI and training code in July, so it is more open today than it was at the time of the video—but that does not change the local memory arithmetic.

**M2 16 GB verdict: ❌.**

---

### OmniShow

OmniShow's code release has also improved since the video.

Today there are training and inference scripts, but the project's default video pipeline is based on **Wan2.1-I2V-14B**, and its installation instructions are CUDA-oriented.

More importantly, the authors explicitly state that **OmniShow's checkpoints are not included** because of internal policy constraints.

So downloading the repository does not provide a small finished OmniShow model.

**M2 16 GB verdict: ❌ for the intended workflow.**

---

## Hosted / non-local items

Several chapters are interesting AI developments but do not participate in a local-model comparison.

**GPT-Rosalind** is now more broadly available than at launch, but it remains a controlled hosted model available through ChatGPT, Codex and the API for qualified customers.

**Happy Oyster** now has Android, iOS and Web SDKs, but these SDKs establish RTC sessions and rely on temporary API credentials and server-side world/history/artifact logic. That is a client integration story, not an offline model release.

**Claude Opus 4.7** is a hosted Claude model and has already been superseded in the Opus family. Anthropic's current page describes Opus 5.5 as its strongest current Opus model.

**Gemini 3.1 Flash TTS** is also service-side. More importantly for anyone following the video months later, Google's documentation now explicitly marks it as a **legacy preview** and recommends Gemini 3.8 Flash TTS or 3.8 Flash-Lite TTS for new production workloads.

The **HubSpot** segment is similarly a SaaS/product workflow rather than a local checkpoint.

The three **humanoid/robotics** chapters are hardware, event and manufacturing stories and therefore have no meaningful 16 GB local-model verdict.

---

## TokenLight: interesting research, but not yet a local-model entry

The video characterization can be sharpened here.

TokenLight is a **conditional image-relighting** method. It uses attribute tokens to control properties including intensity, color, ambient illumination, diffuseness and 3D light position.

The public GitHub material I could verify is the **VisibleFixture-60 evaluation dataset and metric code**, including pre-generated TokenLight predictions. It is not an inference implementation of the model itself.

Without a verified official inference checkpoint and runtime, there is no useful M2 memory calculation to perform yet.

**Verdict: n/a — watch for a model/code release.**

---

## Suggested actions on this machine

### 1. Benchmark Ternary Bonsai 8B first

This is the highest-value experiment from the video.

Use the MLX 2-bit release and record:

- peak memory pressure;
- prompt-processing speed;
- generation speed;
- 4K / 8K / 16K context behavior;
- JSON/tool-format reliability;
- performance on the actual tasks for which a local model is useful.

The **2.30 GB real artifact size** is small enough that this should be an actual usable laptop model rather than a “technically boots if everything else is closed” demo.

### 2. Treat Qwen 3.6 as a quantization experiment, not the default

Do not download the 20.4 GB MLX 4-bit version for a 16 GB machine.

If the model itself is specifically interesting, test one of the ~11–13 GB IQ2-class GGUFs with a short context and compare output quality against a smaller model that is not being quantized nearly as aggressively.

The useful experiment is not just “does it launch?” but:

> Does the larger architecture survive 2-bit quantization well enough to outperform a much smaller model running at a healthier precision?

### 3. Use GameWorld if agent evaluation is a goal

The benchmark environment is cheap enough to run locally and gives a reproducible way to compare agent behavior.

Run the harness first with an existing hosted multimodal model to validate the setup. A fully local VLM can be substituted later if a suitably small model is available.

### 4. WildDet3D: use the Apple implementation that actually exists

If the task is local/on-device 3D detection, the iPhone application is more concrete than trying to force the CUDA Python repository onto MPS.

Only invest in a Mac port if the desktop integration itself is valuable.

### 5. For HY-World, isolate WorldMirror

Do not attempt the complete HY-World world-generation stack on this machine.

If 3D reconstruction is the actual objective, WorldMirror-2's 5.05 GB checkpoint is the only component in the release whose raw size makes a Mac port interesting.

Watch for community MPS/MLX support rather than installing the entire CUDA pipeline.

### 6. Motif-Video is the video-generation experiment to revisit

Among this video's open video-generation work, Motif-Video 2B has the most plausible path toward consumer hardware.

But wait for either:

- a documented Apple/MPS configuration;
- a lower-memory ComfyUI/GGUF workflow;
- or evidence that substantially reduced frame count and resolution runs within 16 GB.

The current publisher numbers do not yet justify calling it a practical M2 generator.

### 7. Skip these on this laptop

For a 16 GB M2, I would not spend setup time attempting the intended local workflows for:

- Lyra 2;
- AniGen;
- OmniShow;
- Prompt Relay on its documented Wan2.2-A14B backend;
- full HY-World 2.0 world generation.

Their current checkpoint/runtime requirements make external NVIDIA compute the more appropriate environment.

---

## Bottom line

This roundup looks, at first, like it contains several “efficient” or “open” models that might belong on a consumer laptop.

After checking the actual artifacts and runtimes, the picture is much narrower.

**Ternary Bonsai 8B is the clear local deployment result.** It has a real Apple-native MLX artifact, a very small 2.30 GB weight footprint, and enough memory margin to behave like a normal application on a 16 GB Mac rather than a hardware stress test.

**GameWorld is useful local infrastructure**, although not itself a model.

**WildDet3D and WorldMirror-2 are potential port targets:** their weights fit, but their official desktop software stacks are CUDA-oriented.

**Motif-Video 2B sits near the memory boundary:** interesting, but the low-memory evidence is still based on NVIDIA/CUDA configurations.

**Qwen 3.6 35B-A3B demonstrates the most important MoE caveat in the report:** active parameter count is not resident parameter count. On a 16 GB Mac, the normal 4-bit Apple build does not fit; only aggressive low-bit community quants do.

Everything else is either a clear hardware wall, a hosted service, a research release without deployable weights, or a non-model news item.

For this machine, the actionable order is therefore:

**Ternary Bonsai 8B → GameWorld harness → WildDet3D / WorldMirror port experiments → Motif-Video reduced-memory experiment → Qwen 3.6 extreme-quant curiosity.**

---

## Sources

- Source video and chapter ordering.
- Prompt Relay official repository and Wan2.2-A14B reference command.
- Ternary Bonsai 8B MLX model card.
- OpenAI GPT-Rosalind release and September access update.
- WildDet3D repository, weights, iPhone deployment and CUDA setup.
- Motif-Video 2B model card and memory-efficient inference figures.
- AniGen official repository and checkpoint tree.
- Happy Oyster SDK/service documentation.
- NVIDIA Lyra 2 repository/model card and checkpoint sizes.
- Tencent HY-World 2.0 current repository/model zoo.
- OmniShow current repository and Wan-based reference workflow.
- Qwen 3.6 official weights, MLX 4-bit conversion and community GGUF quantizations.
- TokenLight CVPR paper and VisibleFixture-60 evaluation repository.
- GameWorld official benchmark repository.
- Google Gemini 3.1 Flash TTS current model documentation.
- Anthropic Claude Opus model history/current availability.