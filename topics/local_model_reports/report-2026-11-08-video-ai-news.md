# Weekly AI video report — 2026-11-08

**Source:** [Weight space programming, science agents, 3D generators, new Gemini Omni, new GPT Image: AI NEWS](https://www.youtube.com/watch?v=9RIK3A24ZxA) by AI Search · published November 8, 2026 in Taipei (November 7 Pacific) · 48:08\
**Target:** M2 MacBook Pro with 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Evidence as of November 8:** All 33 chapters. Local fit is inferred from released files, runtime documentation, and workflow files. No model was benchmarked on this M2.

## Worth trying on your Mac

Three releases this week are small enough to try. **Mirage** is a 21.6 MB vision model with a native macOS runner, so it is the easiest first test. **Qwen3.5-0.8B with edited weights** is a good small experiment if you want to see what the week's biggest idea does to an actual model. **NitroFusion2** is the most useful image generator, but its full pipeline sits near the edge of the memory budget.

| Configuration | Best for | Mac fit |
| --- | --- | --- |
| [Mirage, `.cact` build](#scene-description-and-detection) | ❓ Describing, detecting and segmenting objects in a photo | ✅ Comfortable |
| [Qwen3.5-0.8B, weight-space edit](#small-text-model) | 💬 Short math and instruction-following prompts | ✅ Comfortable |
| [NitroFusion2, Q4_K_M with a Q4_K_M text encoder](#fast-image-generation) | 🖼️ One- or two-step image generation | ⚠️ Experimental |

**Comfortable** means the listed files leave room for the suggested input. **Experimental** means the files fit on paper, but no run on a Mac was found. Artifact sizes use decimal GB and MB.

### Scene description and detection

**Mirage** answers several questions about one image: it describes the scene, detects objects, reads text, draws segmentation masks and reports spatial relations. The model has 51.3 million parameters, and Cactus Compute’s 2-bit build is a 21.6 MB file. Start with one photograph and ask for a description, then ask for a mask of one named object. The published timings of 74 ms (phone NPU) and 107 ms (phone CPU) come from a Samsung Galaxy S26, so they show that the model is small, not how fast it runs here. The Cactus runtime lists a macOS Apple Silicon build. [Mirage post](https://cactuscompute.com/blog/mirage) · [Model card](https://huggingface.co/Cactus-Compute/mirage) · [Runtime](https://huggingface.co/Cactus-Compute/cactus) · [Video chapter](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1594s)

### Small text model

**Weight-space programming** asks a language model to read a network’s weights and rewrite some of them, without training. In the authors’ best-known example, the model traced the “looping” of Qwen3.5-0.8B to one direction written by two layers, then subtracted it from 131,072 weights (0.016% of the model). The authors report MATH-500 rising from 7.9% to 48.1% and IFEval from 21.0% to 62.3% for that edited model. Both numbers come from the authors’ post and use long thinking budgets (up to 32,768 tokens), so test it on short math problems before trusting any result. The 1.75 GB checkpoint is the author’s own; a 4-bit GGUF of a *copy* of the edit exists from a different account, so check that it matches before comparing results. [Post and experiment logs](https://rikiyat.github.io/blog/weight-space-programming/) · [Edited model](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming) · [Live demo](https://huggingface.co/spaces/akhaliq/weight-space-programming-demo) · [Video chapter](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=721s)

### Fast image generation

**NitroFusion2** is a version of Z-Image-Turbo trained to produce an image in one or two steps. The authors’ ComfyUI workflow for GGUF files uses three parts: the image model (nf2-Q4_K_M, 5.07 GB), a Qwen3-4B text encoder (the workflow names the 4.28 GB Q8_0 build) and a 0.32 GB decoder. Together that is 9.67 GB of weights, above the 8 GB comfort line. Swapping in the 2.50 GB Q4_K_M text encoder lowers the total to 7.89 GB. The swap is untested by the authors and may change how well the image follows the prompt. [Video chapter](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=230s) · [Checkpoints](https://huggingface.co/ChenDY/NitroFusion2) · [GGUF workflow](https://github.com/ChenDarYen/NitroFusion2/blob/main/workflows/nitrofusion2_1step_gguf.json)

## Other developments worth knowing

- **Gemini Omni 1.2 Flash** generates and edits video up to 15 seconds and is available through Google’s API, Flow, Vids and the Gemini app; Google lists $0.07 per second at 720p. It is hosted. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/)
- **GPT Images 2.6** adds GIF output and offers two API variants, Flare and Sunburst. Hosted only. [Source](https://openai.com/index/introducing-images-2-6/)
- **GPT-6 Cyber** is OpenAI’s security-research model, offered to verified defenders through its Daybreak program. Hosted and restricted. [Source](https://openai.com/index/introducing-gpt-6-cyber/)
- **Open-weight releases are growing past a laptop.** Kimi K3.1 Pro has 2.8 trillion total parameters and a 1.56 TB download. ERNIE 5.5 Flash Base has 280B total parameters. Ripple-65B is dense, so all 65B parameters are used for every token. Tencent’s Hy4 and LongCat-2.5 say weights are coming; Thinking Machines plans Inkling 2 Small weights under Apache 2.0 within a week of its November 5 post. None of these fit this Mac.
- **P-JiT 21K** is a 2B image model trained for about $21,000 and released under Apache 2.0, but its code requires an NVIDIA GPU and it needs an 8 GB text encoder beside 8.7 GB of weights. [Blog](https://www.linum.ai/field-notes/pjit-21k)

## Technical appendix

### Complete video chapter inventory

All 33 chapters follow the official description and timestamps. “❌ Hosted” means no public local weights were verified. “⚠️ Unverified” records unresolved deployment evidence; “— N/A” covers editorial, sponsor, tools, and research without a standalone inference configuration.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=0s) | AI news intro | Editorial | — N/A; introduces the roundup. |
| [00:54](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=54s) | [HairDeck](https://hyzcluster.github.io/HairDeck/) | 3D research / code and weights linked | ⚠️ Unverified; project page links code and a [model page](https://huggingface.co/hyz317/HairDeck), with no hardware figures. |
| [02:32](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=152s) | [RelayVSR](https://kopperx.github.io/RelayVSR/) | Video upscaling research / weights | ⚠️ Unverified; 13.82 GB peak GPU memory at 1080p was measured on an A100 80 GB. |
| [03:50](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=230s) | [NitroFusion2](https://github.com/ChenDarYen/NitroFusion2) | Open weights / image | ⚠️ Experimental; 9.67 GB with the workflow’s encoder, 7.89 GB with a Q4_K_M encoder. |
| [05:11](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=311s) | [STRATA](https://huggingface.co/nvidia/strata) | Open weights / atmosphere model | ❌ Outside the supported path; requires Linux and NVIDIA Ampere, Hopper or Blackwell GPUs. |
| [06:47](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=407s) | [FlowHMR](https://flowhmr.github.io/) | Motion-capture research | ⚠️ Unverified; page links code, model and demo but gives no requirements. |
| [08:23](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=503s) | [ReLift](https://relift3d.github.io/) | 3D tracking research | ⚠️ Unverified; code linked, weights not confirmed, and it needs separate 2D tracker and geometry models. |
| [09:35](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=575s) | [Gemini Omni 1.2 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/) | Hosted video model | ❌ Hosted; Gemini API, Google Cloud and apps. |
| [10:48](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=648s) | [GPT Images 2.6](https://openai.com/index/introducing-images-2-6/) | Hosted image model | ❌ Hosted; ChatGPT, Codex and API. |
| [12:01](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=721s) | [Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) | Research / open edited model | ✅ Comfortable for the 0.8B edited model; the editing method used GPT-6 Astra, a hosted model. |
| [16:59](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1019s) | [Higgsfield](https://higgsfield.ai/) | Sponsor / hosted creative tools | ❌ Hosted; sponsor segment. |
| [18:10](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1090s) | [Lucid Lyra](https://research.nvidia.com/labs/sil/projects/lucidlyra/) | 3D scene research | ⚠️ Unverified; project page says code is coming soon. |
| [19:30](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1170s) | [P-H3 Image](https://www.pruna.ai/blog/oss-p-h3-image-launch) | Open weights / image | ❌ Outside budget; smallest 4-bit set is 20 GB, with 21 GB peak at 8 MP. |
| [20:46](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1246s) | [OpenRoboKit](https://openrobokit.com/) | Open-source robotics libraries | — N/A; tooling, not a model. |
| [22:11](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1331s) | [MOSS-Live](https://www.moss.cn/models/moss-live) | Hosted speech and video model | ❌ Hosted; API and playground, no weights listed. |
| [24:07](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1447s) | [P-JiT 21K](https://www.linum.ai/field-notes/pjit-21k) | Open weights / image | ❌ Outside budget; CUDA-only code, 8.7 GB weights plus an 8 GB text encoder. |
| [25:34](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1534s) | [CoLa3D](https://master-cai.github.io/CoLa3D/) | 3D research | ⚠️ Unverified; page links code and a model page but states no requirements. |
| [26:34](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1594s) | [Mirage](https://cactuscompute.com/blog/mirage) | Open weights / vision | ✅ Comfortable; 21.6 MB `.cact` file, macOS Apple Silicon runner. |
| [28:21](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1701s) | [DreamX](https://cvlab-kaist.github.io/DreamX/) | Robot-video research | ⚠️ Unverified; code is marked as coming soon. |
| [29:11](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1751s) | [ZAP](https://zero-real.github.io/) | Robot-control research | ⚠️ Unverified; the reported system builds on a 27B Qwen model, and the page states no release. |
| [30:39](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1839s) | [Hy4](https://hy.tencent.ai/research/hy4) | Announced open model | ❌ Weights not yet released; the [preview](https://huggingface.co/tencent/Hy4-preview) is a 1.56 TB download. |
| [31:59](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=1919s) | [Hydrogen 1.0](https://blog.deepprinciple.com/introducing-hydrogen-1.0/) | Open weights / science LLM | ⚠️ Unverified; built on GLM-5.3, parameter count not stated. |
| [34:04](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2044s) | [GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber/) | Restricted hosted LLM | ❌ Hosted; offered through OpenAI’s Daybreak program. |
| [35:10](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2110s) | [Muse voice and avatars](https://about.fb.com/news/2026/11/introducing-muse-ai-voice-expressive-avatars/) | Hosted product | ❌ Hosted; Meta’s Muse app on mobile, web and Mac. |
| [36:06](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2166s) | [Möbius](https://jiazhishu.github.io/mobius/) | Motion-language research | ⚠️ Unverified; 0.6B and 1.7B versions appear in the paper, weights not confirmed. |
| [38:02](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2282s) | [Kimi K3.1](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) | Open weights / LLM | ❌ Outside budget; 2.8T total parameters, 1.56 TB download. |
| [38:42](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2322s) | [ERNIE 5.5 Flash](https://ernie.baidu.com/release/ernie-5-5-flash-base/) | Open weights / base LLM | ❌ Outside budget; 280B total parameters. |
| [39:52](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2392s) | [Ling 3.2 Flash](https://developer.ant-ling.com/en/docs/models/ling/#ling-32-flash) | LLM | ❌ Outside budget; 560B total parameters, and no 3.2 weights were found on Hugging Face. |
| [41:26](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2486s) | [Ripple-65B Preview](https://www.ricursive.com/ripple) | Open weights / LLM | ❌ Outside budget; dense 65B, so about 32.5 GB at four bits before cache. |
| [42:34](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2554s) | [LongCat-2.5](https://longcat.ai/blog/longcat-2.5/) | Announced multimodal LLM | ❌ Weights “coming soon”; 1.6T total parameters. |
| [44:04](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2644s) | [Inkling 2 Small](https://thinkingmachines.ai/news/inkling-2-small/) | Announced open model | ❌ Weights not yet released; 594B total parameters. |
| [45:29](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2729s) | [VoxLution](https://daoyig.github.io/VoxLution/) | 3D scene research | ⚠️ Unverified; code is marked as coming soon. |
| [46:13](https://www.youtube.com/watch?v=9RIK3A24ZxA&t=2773s) | Solver | Unlinked | ⚠️ Unverified; the description lists no link for this chapter, so no source could be checked. |

### Deployment evidence

The machine usually has **8–11 GB** available for weights and working memory after macOS and other applications. A file’s size is only the starting cost: image models add intermediate results, and language models add a cache that grows with the conversation. The starting points above are suggested first trials. Peak memory and speed on the target M2 are unmeasured. [Shared hardware assumptions](./memory-budget.md)

| Configuration and artifact evidence | What has to fit | Runtime and licensing |
| --- | --- | --- |
| [Mirage `.cact` and weights](https://huggingface.co/Cactus-Compute/mirage/tree/main) | `mirage.cact` is 21.6 MB. The repository also holds a 216 MB `mirage.safetensors`; whether the native runner reads it was not checked. Runtime memory is not reported. | Apache-2.0 on the model card. The [macOS arm64 runner](https://huggingface.co/Cactus-Compute/cactus) is from release 4.0.0, and Python wheels cover macOS ARM64. |
| [Edited Qwen3.5-0.8B](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming/tree/main) | 1.75 GB single safetensors file, BF16, 873 million parameters. A community [GGUF of a copy](https://huggingface.co/mradermacher/Qwen3.5-0.8B-weight-space-programming-GGUF) has a 0.54 GB Q4_K_M file, but it comes from a different upload. | Apache-2.0 weights; the model is a Qwen3.5-0.8B derivative. Use Transformers; llama.cpp support for this checkpoint was not checked. |
| [NitroFusion2 Q4_K_M and workflow](https://huggingface.co/ChenDY/NitroFusion2/tree/main) | 5.07 GB image model, plus a [Qwen3-4B GGUF](https://huggingface.co/Qwen/Qwen3-4B-GGUF/tree/main) text encoder (sizes shown are from Qwen’s official upload; the workflow links an unsloth copy: 4.28 GB Q8_0 as published, 2.50 GB Q4_K_M as an untested swap) and a 0.32 GB decoder. Working memory at 1024 px is unreported. | Apache-2.0 weights. The workflow requires ComfyUI with the [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) node; a Mac run was not found. The official diffusers example targets CUDA. |

### Other chapter notes

- **Why Weight-Space Programming is not a recipe.** The edits were made by a frontier model, GPT-6 Astra, working in a Python session with a budget of forward passes. Only the resulting Qwen3.5-0.8B checkpoint is local. The authors also report that the same method could not improve Gemma 3 270M, and that it needed attention patterns to identify one fine-tuned model. [Post](https://rikiyat.github.io/blog/weight-space-programming/)
- **3D, motion and robotics research.** HairDeck, FlowHMR, ReLift, Lucid Lyra, CoLa3D, VoxLution, Möbius and DreamX each combine a research model with other pretrained parts, and several mark code as coming soon. Their project pages state no Mac memory figures. ZAP trains a 27B Qwen model in simulation and reports results on a real robot. [HairDeck](https://hyzcluster.github.io/HairDeck/) · [ZAP](https://zero-real.github.io/)
- **RelayVSR.** A large generative model produces reference latents for sparse keyframes and a small network upscales each frame. At 1080p on an A100 80 GB the project reports 29.29 frames per second and 13.82 GB peak GPU memory. Community ComfyUI workflows and quantized files exist; none was checked here. [RelayVSR](https://kopperx.github.io/RelayVSR/)
- **Large open models.** Kimi K3.1 Pro uses MXFP4 weights with a Mixture-of-Experts design of 104B active parameters per token, but all experts are in the download. Ripple-65B is dense with 80 layers. ERNIE 5.5 Flash Base is a base model, not an instruction-tuned release. Tencent says it plans to open Hy4’s weights; its earlier Hy4 preview is Apache-2.0. [Kimi](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) · [Ripple](https://www.ricursive.com/ripple) · [ERNIE](https://ernie.baidu.com/release/ernie-5-5-flash-base/) · [Hy4](https://hy.tencent.ai/research/hy4)
- **Hosted stories.** Gemini Omni 1.2 Flash (released November 5), GPT Images 2.6 (November 4), GPT-6 Cyber (November 5) and Muse voice (November 5) are available only through their providers. MOSS-Live is a hosted API with an online playground. [MOSS-Live](https://www.moss.cn/models/moss-live)
- **Atmosphere model.** STRATA is a 331.7M-parameter weather emulator, small by parameter count, but its supported stack is Linux, PyTorch, NVIDIA PhysicsNeMo and NATTEN on NVIDIA GPUs. [STRATA](https://huggingface.co/nvidia/strata)

### Coverage and verification limits

The chapter inventory follows the video’s official description and timestamps. No transcript was retrieved, so claims about what the narrator said are not included; coverage is complete at the chapter level only. The description lists no link for the final chapter, Solver, so that row records the gap instead of guessing a source. Several sites rendered their content with scripts, and Ling 3.2 Flash’s documentation did not state a license or download link; its row records only what was visible.

For models without a checked artifact, verdicts rely on published parameter counts and file sizes. Four-bit estimates use total parameters × 0.5 bytes as a lower bound, with quantization metadata, cache and temporary buffers adding to it. Published timings on an A100, H100 or phone are attributed to their source and are not Mac results.

## Sources

- **Chapter coverage:** [AI Search video, official description, and chapter list](https://www.youtube.com/watch?v=9RIK3A24ZxA). The chapter table links the primary source for each item.
- **Local candidates:** [Mirage post](https://cactuscompute.com/blog/mirage), [Mirage model card](https://huggingface.co/Cactus-Compute/mirage), [Cactus runtime](https://huggingface.co/Cactus-Compute/cactus), [Weight-Space Programming post](https://rikiyat.github.io/blog/weight-space-programming/), [edited Qwen3.5-0.8B](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming), [NitroFusion2 repository](https://github.com/ChenDarYen/NitroFusion2), and [NitroFusion2 checkpoints](https://huggingface.co/ChenDY/NitroFusion2).
- **Hosted releases:** [Gemini Omni 1.2 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/), [GPT Images 2.6](https://openai.com/index/introducing-images-2-6/), [GPT-6 Cyber](https://openai.com/index/introducing-gpt-6-cyber/), and [Muse voice](https://about.fb.com/news/2026/11/introducing-muse-ai-voice-expressive-avatars/).
- **Large open or announced models:** [Kimi K3.1 Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro), [ERNIE 5.5 Flash Base](https://ernie.baidu.com/release/ernie-5-5-flash-base/), [Ripple-65B](https://www.ricursive.com/ripple), [Hy4](https://hy.tencent.ai/research/hy4), [LongCat-2.5](https://longcat.ai/blog/longcat-2.5/), [Inkling 2 Small](https://thinkingmachines.ai/news/inkling-2-small/), [P-H3 Image](https://www.pruna.ai/blog/oss-p-h3-image-launch), and [P-JiT 21K](https://www.linum.ai/field-notes/pjit-21k).
