# Local Runnability: Qwen-Image-2.1 on a 16 GB M2 Mac

**Compiled:** 2026-09-22
**Model:** [Qwen-Image-2.1](https://github.com/QwenLM/Qwen-Image-2.1), released 2026-09-20
**Reference video:** [“Finally! New best local AI image editor is here”](https://www.youtube.com/watch?v=BaE6UBfNdQk) by AI Search, published 2026-09-22
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory**
**Stack assumption:** ComfyUI / PyTorch-MPS — **no CUDA**

This report asks whether Qwen-Image-2.1 is a useful local image generator and editor on this Mac, rather than whether one checkpoint file can fit in a nominal memory figure. File sizes below come from the Hugging Face repositories as of the compilation date. Runtime conclusions are inferred from the complete pipeline, the project’s [memory budget](./memory-budget.md), and current MPS issue reports; this model was **not benchmarked on the target Mac**.

## TL;DR

| Question | Answer |
| --- | --- |
| **What is it?** | A unified text-to-image and image-editing system with a **7.1B single-stream DiT**, **Qwen3-VL 8B** text/image encoder, and an RGBA VAE. It supports native transparent output, background extraction, typography, local edits, and up to 10 reference images. |
| **Does the official model fit?** | **No.** The BF16 pipeline is about **33.1 GB on disk** before runtime memory: 17.5 GB encoder + 14.2 GB DiT + 1.4 GB VAE. Official examples are CUDA-first. |
| **Do community quants fit?** | **Barely, as an experiment.** Q3 DiT + W4A8 encoder + VAE totals about **10.17 GB** of files; Q4 totals **11.18 GB**. That reaches or exceeds the Mac’s practical 8–11 GB model-and-working-memory budget before activations, caches, ComfyUI, and macOS. Expect offload, swap, and long runs. |
| **Text-to-image on the M2?** | **Plausible only with aggressive quants, reduced resolution, and patience.** No credible 16 GB M2 measurement was found. The official native 2K setting is not a sensible starting point. |
| **Image editing on the M2?** | **Currently fragile.** An open MPS bug corrupts the VAE encode path at 512×512 and above. Text-to-image is unaffected because it only decodes. In ComfyUI, `--cpu-vae` is the conservative workaround for edits and background removal. |
| **Is “4 GB VRAM” the whole requirement?** | **No.** The video’s 3.19 GB Q3 number is only the diffusion transformer. The workflow still needs the 6.31 GB W4A8 encoder and 0.68 GB VAE, plus working memory. |
| **Are LoRAs ready?** | One supplied anime-consistency edit LoRA is only **168 MB**, but its author calls it experimental. It does not reduce the base pipeline’s memory needs, and Mac editing still hits the VAE issue. |
| **Commercial use?** | The weights use the **Qwen Research License**, not Apache 2.0. Model materials are licensed for research/evaluation only; commercial use requires a separate license. Qwen separately says users retain rights to generated images, but output ownership does not clearly authorize commercial operation of the local model. |

**Verdict:** Qwen-Image-2.1 is a strong capability release and unusually compact for its class, but it is **not a comfortable 16 GB M2 daily driver**. Treat quantized text-to-image as a slow experiment. For image editing, wait for the MPS VAE fix to land or run the VAE on CPU. A 24–32 GB Apple Silicon machine is the more credible local floor; 32 GB still does not imply fast native-2K generation.

---

## What changed in Qwen-Image-2.1

Qwen-Image-2.1 replaces the older 20B-class Qwen-Image backbone with a 32-layer, 7.1B single-stream diffusion transformer. The smaller headline number is real, but it describes the visual generator rather than the complete pipeline. The system also loads a Qwen3-VL 8B encoder and a 64-channel RGBA autoencoder.

The release combines several jobs in one pipeline:

- text-to-image and image-conditioned editing;
- native RGBA generation and editing, including transparent subject extraction;
- up to **10 reference images** for composition and identity/product preservation;
- circle, painted-annotation, and mask-guided local editing;
- native 2K output presets, including wide panoramas and vertical layouts;
- improved text rendering, portraits, product images, and detailed textures.

The architectural efficiency comes from mixed-granularity block-causal attention. Text and reference images form a prefix whose keys and values can be cached after the first denoising step. That reduces repeated computation for multi-reference editing, but the encoder, prefix cache, target-image activations, and VAE still consume memory. Prefix reuse is a compute optimization, not proof that the full system fits in 7B-model memory.

The reference defaults are **40 Euler flow-matching steps** with guidance scale **1**. Increasing CFG above 1 engages a second model pass only when a negative prompt is supplied, roughly doubling denoising work in the reference pipeline.

## The complete footprint

### Official BF16 Diffusers pack

The official [Qwen/Qwen-Image-2.1 file tree](https://huggingface.co/Qwen/Qwen-Image-2.1/tree/main) and the [vLLM recipe](https://recipes.vllm.ai/Qwen/Qwen-Image-2.1) break the model into three large components.

| Component | Role | On-disk size | 16 GB M2 |
| --- | --- | ---: | --- |
| Qwen3-VL 8B | Encodes prompts and reference images | **17.5 GB** | ❌ larger than the daily weight budget by itself |
| Qwen-Image-2.1 DiT | 7.1B visual generation transformer | **14.2 GB** | ❌ |
| RGBA VAE | Encodes/decodes four-channel images | **1.4 GB** | ✅ alone |
| **Total** | Complete BF16 pipeline | **~33.1 GB** | ❌ |

The vendor’s vLLM measurement reports **34.0 GB peak** for one 1024×1024 image on an NVIDIA GB300. That is a publisher measurement on a datacenter GPU, not an MPS estimate. The official Diffusers quick start moves the pipeline to `cuda`; the repository does not provide a tested 16 GB Apple recipe.

### ComfyUI files

[Comfy-Org/Qwen-Image-2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) repackages the components for native ComfyUI workflows.

| File | Size | Purpose |
| --- | ---: | --- |
| `qwen_image_2.1_bf16.safetensors` | **14.23 GB** | BF16 DiT |
| `qwen_image_2.1_int8_convrot.safetensors` | **7.26 GB** | INT8 DiT used in the video |
| `qwen3vl_8b_bf16.safetensors` | **17.53 GB** | BF16 encoder |
| `qwen3vl_8b_int8_convrot.safetensors` | **9.35 GB** | INT8 encoder |
| `qwen3vl_8b_w4a8.safetensors` | **6.31 GB** | Smallest encoder in the supplied Comfy pack |
| `qwen_image_2.1_vae_bf16.safetensors` | **0.68 GB** | RGBA VAE |

The smallest supplied all-Comfy pack is therefore about **14.24 GB** on disk: INT8 DiT + W4A8 encoder + VAE. “The 7.2 GB INT8 model fits 8 GB VRAM” only describes the DiT file. On an NVIDIA PC, ComfyUI can move components between discrete VRAM and a separate system-RAM pool. The M2 has one 16 GB unified pool shared by macOS, CPU, and GPU, so the same claim does not transfer directly.

### GGUF transformer quants

[Abiray/Qwen-Image-2.1-GGUF](https://huggingface.co/Abiray/Qwen-Image-2.1-GGUF) quantizes only the diffusion transformer for ComfyUI-GGUF.

| DiT quant | DiT file | Complete file set with 6.31 GB encoder + 0.68 GB VAE | Target-Mac read |
| --- | ---: | ---: | --- |
| Q3_K_M | **3.19 GB** | **~10.17 GB** | Smallest plausible experiment; little room for activations/runtime |
| Q4_K_S | **4.06 GB** | **~11.05 GB** | At the project’s daily-use ceiling before overhead |
| Q4_K_M | **4.19 GB** | **~11.18 GB** | Best quality/size starting point only if Q3 quality is unacceptable |
| Q5_K_M | **5.01 GB** | **~12.00 GB** | Too tight |
| Q6_K | **5.88 GB** | **~12.86 GB** | Too tight |
| Q8_0 | **7.59 GB** | **~14.58 GB** | No practical advantage over the Comfy INT8 path here |

These totals are file sizes, not peak memory. GGUF dequantization, the encoder, image latents, the prefix KV cache, VAE workspaces, PyTorch, ComfyUI, and the operating system all add overhead. Q3/Q4 may load through aggressive offload and swap, but “loads” is a lower bar than usable local generation.

## What should run on this Mac

### Text-to-image: experimental

Text-to-image avoids the broken VAE encode path, so it is the best first test. The most defensible configuration is:

| Setting | Starting point |
| --- | --- |
| Runtime | Current ComfyUI source with the native Qwen-Image-2.1 text-to-image template |
| DiT | Q3_K_M first; Q4_K_M only if memory pressure remains acceptable |
| Encoder | `qwen3vl_8b_w4a8.safetensors` |
| VAE | Official BF16 VAE |
| Resolution | **512–768 px class**, not native 2K |
| Sampling | 40 steps, CFG 1, no negative prompt |
| Desktop state | Close memory-heavy apps and watch macOS memory pressure and swap |

This is an inferred test plan, not a measured recipe. A community report on an **M2 MacBook Pro with 32 GB** described roughly **16 minutes** for 40 steps at 1024×1024. That is not directly comparable to a 16 GB machine, but it sets the right expectation: MPS support does not imply interactive speed.

### Image editing and background removal: use CPU VAE

As of 2026-09-22, [ComfyUI issue #16433](https://github.com/Comfy-Org/ComfyUI/issues/16433) and [Qwen-Image-2.1 issue #6](https://github.com/QwenLM/Qwen-Image-2.1/issues/6) remain open. They independently isolate a PyTorch-MPS error in temporal padding inside the VAE encoder:

- at 512×512 and above, the MPS encode path returns corrupted latents;
- text-to-image remains clean because it uses VAE decode only;
- image editing and background extraction encode a reference image and are affected;
- switching to FP32 does not fix the error;
- ComfyUI’s `--cpu-vae` produces a clean round trip;
- a small `F.pad` → `torch.cat` patch also worked in reported tests, but it was not merged at the report cutoff.

On this Mac, use `--cpu-vae` for any workflow that ingests an image. CPU and GPU still share the same physical memory, so this is a correctness workaround rather than a capacity trick. It will not turn the 10–11 GB quantized file set into a comfortable workload.

### No mature MLX path yet

The release has day-zero Diffusers, ComfyUI, vLLM-Omni, SGLang, LightX2V, AMD ROCm, and several accelerator backends. No first-party MLX conversion or Apple-specific runtime was found at the cutoff. ComfyUI/PyTorch-MPS is the available Mac path, complete with the quantization and VAE caveats above.

## Prompt enhancer and LoRA add-ons

The optional [Qwen-Image-2.1-PE-T2I](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I) and PE-I2I models are fine-tuned **Qwen3.5-VL 9B** prompt rewriters. The BF16 T2I checkpoint alone is about **18.8 GB**. Skip it on this machine; prompt rewriting can be done with a smaller local LLM or manually without keeping another 9B vision-language model beside the image pipeline.

The supplied [WarmBloodAban/Qwen-Image-2.1-LoRAs](https://huggingface.co/WarmBloodAban/Qwen-Image-2.1-LoRAs) repository currently contains one **168 MB** anime-consistency edit LoRA. Its model card says:

- it was trained mainly on four-view character sheets and facial-expression edits;
- it is experimental, with no guarantee of stable output;
- the suggested starting weight is **0.6–0.8**.

The adapter size is friendly, but the complete base pipeline is unchanged. ComfyUI-GGUF also describes LoRA loading as experimental, and this particular adapter targets editing, the exact path affected by the Mac VAE bug.

## Cross-check of the supplied video

The official chapter list and automatic captions were available. The video is a useful ComfyUI walkthrough on an **RTX 5000 Ada laptop with 16 GB discrete VRAM**; it is not a Mac or unified-memory test.

| Chapter | What it establishes | Local-report caveat |
| --- | --- | --- |
| [0:00 Intro](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=0s) / [0:26 Features](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=26s) | Unified generation/editing and transparent images | Supported by the official model card |
| [1:18 Editing and references](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=78s) | Reference-image editing and preservation examples | Official model supports up to 10 references; more references increase prefix and encoder work |
| [3:20 Install](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=200s) | ComfyUI native workflows and model placement | The demonstrated INT8 DiT is only one part of the download |
| [7:00 Text to image](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=420s) | 40-step generation workflow | Demonstrated on 16 GB NVIDIA VRAM, not a 16 GB M2 |
| [8:30 Image editing](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=510s) | Unified edit workflow | On current MPS, use CPU VAE or a verified patch |
| [10:45 Luma](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=645s) | Sponsor segment | Hosted product; not evidence about local Qwen performance |
| [12:00 Background removal](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=720s) | Native alpha extraction workflow | This encodes the source image and therefore hits the same MPS issue |
| [13:21 Loading LoRAs](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=801s) | LoRA stack and anime-consistency example | Supplied LoRA is experimental; base memory cost remains |
| [15:40 Low VRAM](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=940s) | Q3–Q8 GGUF DiT files; video suggests Q3 for under 4 GB VRAM | The 3.19 GB figure excludes the 6.31 GB encoder, 0.68 GB VAE, and working memory |
| [18:10 License](https://www.youtube.com/watch?v=BaE6UBfNdQk&t=1090s) | Notes non-commercial weights and Qwen’s output-rights clarification | Output ownership and permission to operate the model commercially are separate questions |

## License: the practical reading

The [Qwen Research License Agreement](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/LICENSE) grants use, modification, and redistribution of the model materials for **non-commercial research or evaluation only**. It directs commercial users to request a separate license. It also requires “Built with Qwen” or “Improved using Qwen” if the materials or their outputs are used to create or improve another distributed model.

[Qwen’s public clarification](https://x.com/Alibaba_Qwen/status/2101929292175495569) says users retain rights to images and other content they generate. That resolves who Qwen claims owns an output; it does not rewrite the repository license’s restriction on commercial use of the model materials. For a business workflow, hosted product, client work, or paid generation service, obtain the commercial license rather than relying on the output-rights statement alone.

The community LoRA page labels its adapter Apache 2.0, but an adapter license cannot expand the base model’s Qwen Research License.

## Recommended action

**For local text-to-image curiosity:** try the Q3 GGUF + W4A8 encoder + BF16 VAE in current ComfyUI, begin below 1024 px, keep CFG at 1, and expect slow generation and memory pressure. Move to Q4 only after a successful Q3 run.

**For local image editing or background removal:** wait for the MPS VAE fix, or launch ComfyUI with `--cpu-vae`. Do not judge prompt quality from an unpatched MPS edit because the corruption is silent.

**For regular creative work:** use a hosted Qwen demo/service or a machine with at least 24–32 GB unified memory. The release’s strongest features—multi-reference editing, 2K output, and alpha-aware editing—are exactly the workloads most likely to exceed this laptop’s practical headroom.

**For commercial work:** request a commercial license before using the local weights in the workflow.

## Sources

- Qwen: [official GitHub repository and model overview](https://github.com/QwenLM/Qwen-Image-2.1), [Hugging Face model card and BF16 files](https://huggingface.co/Qwen/Qwen-Image-2.1), [Qwen Research License Agreement](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/LICENSE), [output-rights clarification](https://x.com/Alibaba_Qwen/status/2101929292175495569)
- Runtime integrations: [Diffusers Qwen-Image-2.1 pull request](https://github.com/huggingface/diffusers/pull/14804), [vLLM-Omni recipe and memory measurement](https://recipes.vllm.ai/Qwen/Qwen-Image-2.1), [ComfyUI native workflow template](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json)
- ComfyUI weights: [Comfy-Org/Qwen-Image-2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1)
- Low-memory DiT quants: [Abiray/Qwen-Image-2.1-GGUF](https://huggingface.co/Abiray/Qwen-Image-2.1-GGUF), [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)
- Add-ons: [Qwen-Image-2.1 prompt enhancer](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I), [experimental anime-consistency LoRA](https://huggingface.co/WarmBloodAban/Qwen-Image-2.1-LoRAs)
- Apple Silicon correctness: [ComfyUI MPS VAE issue #16433](https://github.com/Comfy-Org/ComfyUI/issues/16433), [Qwen-Image-2.1 MPS VAE issue #6](https://github.com/QwenLM/Qwen-Image-2.1/issues/6)
- Independent Mac evidence: [M2 32 GB community run](https://www.reddit.com/r/LocalLLaMA/comments/1wmb2ug/deterministic_kittens_fun_with_qwen_image_21_on/)
- Supplied walkthrough: [AI Search video](https://www.youtube.com/watch?v=BaE6UBfNdQk)
- Hardware bar: [Your real memory budget](./memory-budget.md)
