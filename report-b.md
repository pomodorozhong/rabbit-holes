# Local Runnability: Models from AI News Video (2026-09-26)

Compiled: 2026-09-26  
Source video: [Claude Opus 4.7, Qwen 3.6, Happy Oyster, realtime 3D worlds, new Google TTS: AI NEWS](https://www.youtube.com/watch?v=G8fqduzB5lc) (AI Search, 37:05; published 2026-04-19)  
Hardware target: Apple M2 MacBook Pro, 16 GB unified memory  
Stack assumption: Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — no CUDA  
Memory budget: [Your real memory budget](https://github.com/pomodorozhong/rabbit-holes/blob/master/topics/local_model_reports/memory-budget.md)

## TL;DR

Verdict | Models / items
--- | ---
Runs well on this Mac | **Ternary Bonsai** 1.7B, 4B, and especially the 8B GGUF. The actual 8B Q2_0 download is 2.18 GB and Prism publishes a Metal-capable llama.cpp fork.
Tight / experimental | **WildDet3D** is memory-sized but its desktop reference code assumes CUDA and custom CUDA operations; **WorldMirror-2**, the 1.2B part of HY-World 2.0, is a possible port candidate by parameter count but not by the published stack; **GameWorld** can run as a local benchmark harness, but not with its suggested large local agent on this Mac.
Open weights, not this machine as published | **Prompt Relay / Wan2.2**, **MotifVideo**, **AniGen**, **Lyra 2**, the complete **HY-World 2.0** suite, and **Qwen3.6-35B-A3B**.
Hosted services / products | **GPT-Rosalind**, **Happy Oyster**, **Claude Opus 4.7**, **Gemini 3.1 Flash TTS**, and the HubSpot sponsor segment.
Research, incomplete releases, or hardware stories | **OmniShow** (code but no released OmniShow checkpoint), **TokenLight** (paper and evaluation set), **GameWorld** (benchmark), and the three humanoid-robot chapters.

The one clear local-model recommendation from this video is Ternary Bonsai. Its 8B GGUF is small enough to leave normal operating-system headroom, and its first-party instructions include a Metal path. The publisher's throughput number was measured on an M4 Pro with 48 GB, so it should not be treated as an M2 speed promise, but the memory fit is convincing.

Several headlines need qualification. A 2B video model can still require 12–30 GB of accelerator memory once activations and the video pipeline are included. A model with 3B *active* parameters can still require all 35B stored weights. “Code released” can mean a method layered on a much larger base model, and it can also mean that the defining checkpoint is absent.

---

## Runnability table (all chapters)

Chapter order follows the video's official YouTube chapters. Status and availability were rechecked on 2026-09-26, not frozen at the video's April publication date.

Model / item | Video | Kind | Weights / access | Fits 16 GB M2? | Local reality
--- | --- | --- | --- | --- | ---
Prompt Relay | [1:00](https://www.youtube.com/watch?v=G8fqduzB5lc&t=60s) | Training-free temporal prompt routing for multi-event video generation | Method code is public; requires the Wan2.2-T2V-A14B base | ❌ as a complete setup | The [repository](https://github.com/GordonChen19/Prompt-Relay) modifies Wan2.2 and invokes its A14B checkpoint with offloading. The routing method is light; the required video generator is not a 16 GB M2 workload, and no MPS/MLX path is documented.
Ternary Bonsai | [2:45](https://www.youtube.com/watch?v=G8fqduzB5lc&t=165s) | 1.58-bit language models at 1.7B, 4B, and 8B scale | Apache 2.0 GGUF and unpacked weights | ✅ | The [8B GGUF card](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf) lists a 2.18 GB Q2_0 file and a Metal-capable Prism llama.cpp fork. Stock/mainline llama.cpp did not yet include this Q2_0 kernel at review time.
GPT-Rosalind | [5:35](https://www.youtube.com/watch?v=G8fqduzB5lc&t=335s) | Scientific research agent | Trusted-access hosted model through ChatGPT, Codex, and API | ❌ | OpenAI's [current announcement](https://openai.com/index/introducing-gpt-rosalind/) offers organizational access, not downloadable weights. A local plugin does not make the model inference local.
WildDet3D | [7:39](https://www.youtube.com/watch?v=G8fqduzB5lc&t=459s) | Promptable 3D object detection from images | Public ~1.2B checkpoint and research code under the SAM License; separate on-device iPhone app | ⚠️ port candidate | The [desktop repository](https://github.com/allenai/WildDet3D) pins a CUDA PyTorch build, compiles CUDA operations, and sends tensors to `.cuda()`. The roughly 4.7 GB checkpoint is memory-sized, but the published Mac runtime is missing.
MotifVideo | [9:09](https://www.youtube.com/watch?v=G8fqduzB5lc&t=549s) | 2B text/image-to-video model | Apache 2.0 weights and ComfyUI workflow | ❌ as published | The [model card](https://huggingface.co/Motif-Technologies/Motif-Video-2B) calls for about 30 GB CUDA VRAM, about 19 GB with CPU offload, or roughly 12.5 GB allocation for a Q4 path. The last figure still leaves too little unified-memory headroom and the documented acceleration stack is CUDA-centric.
HubSpot AI content team (sponsor) | [10:54](https://www.youtube.com/watch?v=G8fqduzB5lc&t=654s) | Hosted content-marketing workflow | Cloud product / guide | n/a | This is a sponsor segment, not a downloadable inference model.
AniGen | [12:06](https://www.youtube.com/watch?v=G8fqduzB5lc&t=726s) | Rigged, animation-ready 3D asset generation from one image | Weights and MIT-licensed project code; one third-party dependency has a research-only restriction | ❌ | The [official repository](https://github.com/VAST-AI-Research/AniGen) is tested on Linux with CUDA 11.8/12.2 and specifies an NVIDIA GPU with at least 18 GB, including RTX 3090 and A800 examples.
Happy Oyster | [13:48](https://www.youtube.com/watch?v=G8fqduzB5lc&t=828s) | Real-time, open-ended world-model product | Early-access product; no downloadable weights | ❌ | The [product site](https://www.happyoyster.cn/) describes access to a service. It does not publish a local checkpoint or Apple runtime.
Lyra 2 | [15:05](https://www.youtube.com/watch?v=G8fqduzB5lc&t=905s) | Persistent 3D-world generation from images or video | Research weights under NVIDIA's scientific R&D license | ❌ | The [official release](https://github.com/nv-tlabs/lyra/tree/main/Lyra-2) builds on a 14B Wan foundation and reports an H100 80 GB workflow. The small “131 MB” figure mentioned in the video cannot represent the complete runnable stack.
HY-World 2.0 | [16:40](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1000s) | Suite for world reconstruction, panoramic generation, stereo, and export | Code and checkpoints released after the video | ❌ as a suite | The [current repository](https://github.com/Tencent-Hunyuan/HY-World-2.0) includes WorldMirror-2 (~1.2B), HY-Pano-2 (~80B), HY-Pano-2-Qwen (425M), and WorldStereo-2 (~17B). The documented stack uses CUDA, FlashAttention, custom Gaussian-splatting operations, and multi-GPU pipelines. Only the smallest components are plausible port projects.
OmniShow | [18:03](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1083s) | Human-object interaction video generation | Apache 2.0 method code; OmniShow checkpoints are not included | ❌ | The [repository](https://github.com/Correr-Zhou/OmniShow) was released after the video, but says checkpoints cannot be published under the authors' internal policy. It also depends on 14B Wan2.1 video bases and a CUDA setup.
Claude Opus 4.7 | [20:22](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1222s) | Frontier language and coding model | Claude app/API and cloud platforms | ❌ | Anthropic's [release page](https://www.anthropic.com/news/claude-opus-4-7) lists hosted access through Claude, its API, and cloud partners; no weights are offered.
Qwen3.6-35B-A3B | [24:38](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1478s) | Sparse MoE text model, 35B total / 3B active | Apache 2.0 weights; BF16, GGUF, and community MLX builds | ❌ | The [official BF16 repository](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/tree/main) is about 71.9 GB. The [community 4-bit MLX pack](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit/tree/main) is about 20.4 GB before runtime and KV-cache headroom. Sparse activation reduces computation, not stored-weight memory.
Unitree H1 sprinter | [26:14](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1574s) | Humanoid-robot speed demonstration | Physical robot / control stack | n/a | Unitree reports a greater-than-10 m/s H1 run on its [company timeline](https://www.unitree.com/about/). This is a robotics milestone, not a laptop model release.
Humanoid marathon | [26:57](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1617s) | Physical-robot competition | Event and robot systems | n/a | The result depends on complete robots, control software, batteries, and operator teams; the chapter does not provide a standalone local checkpoint.
Automated humanoid factory | [27:51](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1671s) | Robot-manufacturing story | Industrial hardware and production system | n/a | This is manufacturing infrastructure, not a model package that can be assessed against 16 GB unified memory.
TokenLight | [29:17](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1757s) | Controllable image relighting using attribute tokens | Paper, project demos, and evaluation data; no inference checkpoint found | n/a | The [project page](https://vrroom.github.io/tokenlight/) and [evaluation repository](https://github.com/Vrroom/VisibleFixture-60) document the research and metrics. They do not provide the trained relighting model needed for a local run.
GameWorld | [31:30](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1890s) | Browser-game benchmark for multimodal agents | Apache 2.0 benchmark code and game library | ⚠️ harness only | The [repository](https://github.com/gameworld-project/gameworld) can run the games and evaluator locally. Its documented agents use hosted API keys or a local vLLM server; the suggested Qwen3.5-122B-A10B local model is far beyond this Mac and vLLM is not an Apple-Silicon path.
Gemini 3.1 Flash TTS | [33:09](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1989s) | Controllable multilingual text-to-speech | Hosted Gemini API, AI Studio, Vertex AI, and Google Vids | ❌ | Google offered the model as a hosted preview, not downloadable weights. Its [current model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview) now labels 3.1 a legacy preview and directs new workloads to Gemini 3.8 Flash TTS or Flash-Lite TTS.

Legend: ✅ comfortable local use · ⚠️ possible but experimental / incomplete · ❌ no · n/a not a local checkpoint

---

## Runnable: what is worth trying

### 1) Ternary Bonsai 8B — the clear local win

Field | Details
--- | ---
Job | General text chat, short-form reasoning, coding assistance, instruction following, and tool selection
Architecture | Qwen3-8B converted to ternary weights; 8.19B parameters; Apache 2.0
Actual local artifact | 2.03 GiB / 2.18 GB for `Ternary-Bonsai-8B-Q2_0.gguf`; the publisher's 1.75 GB headline is a representation-size claim, not the current GGUF download size
Mac path | Build the `prism` branch of PrismML's llama.cpp fork with Metal enabled, then load the Q2_0 GGUF
16 GB M2 fit | Comfortable by weight size. Begin with a 4K context, then test 8K while watching memory pressure
Published performance | 76 generation tokens/s on an M4 Pro with 48 GB via Metal; useful as proof that the kernel works, not as an M2 forecast
Limit | The 65,536-token architectural maximum is not the recommended starting point on a 16 GB machine; KV cache and application memory still grow with context

Use the 8B edition unless latency is more important than quality; the unusually small weight file removes the normal reason to drop immediately to the 1.7B or 4B versions. The important implementation detail is the runtime: the Q2_0 ternary kernel was still outside mainline llama.cpp at the review date, so generic one-click instructions that select the F16 file would defeat the memory advantage. Follow the Q2_0 instructions on the [model card](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf), not the generic Hugging Face launcher snippet.

### 2) WildDet3D — plausible size, unsupported Mac path

WildDet3D is the most interesting port candidate. Its roughly 1.2B model and 4.7 GB checkpoint can fit in 16 GB, and the separate iPhone application shows that some form of device-side execution is possible. The public desktop research code is a different path: it uses a CUDA PyTorch wheel, `vis4d` CUDA operations, and hard-coded CUDA transfers. Treat this as a development project requiring operator replacement and MPS validation, not as an installable Mac app.

### 3) GameWorld — local benchmark, not a local model

GameWorld's browser environment, games, result files, and dashboard are light enough to run locally. What performs the visual reasoning and actions is a separate multimodal agent. The first-party quick start uses hosted Google, OpenAI, or Anthropic keys, while the documented self-hosted example uses a 122B-class model through vLLM. On this Mac, the practical route is to run the harness locally and use a hosted agent; connecting a small Apple-compatible VLM would be a separate compatibility experiment.

---

## Near-misses and hardware walls

### Open weights do not guarantee an Apple runtime

- MotifVideo's 2B parameter count looks small, but the published end-to-end video pipeline ranges from roughly 12.5 GB in its most compressed path to 30 GB, and depends on CUDA-oriented components.
- AniGen explicitly calls for an NVIDIA GPU with at least 18 GB. Lyra 2 reports an H100 80 GB workflow around a Wan 14B foundation.
- HY-World 2.0 is a collection of models and 3D rendering components, not one 1.2B download. The full workflow contains 17B- and 80B-class stages and custom CUDA operations.
- Prompt Relay is training-free, but “training-free” does not mean “base-model-free”: it still loads Wan2.2-T2V-A14B.

### Active parameters are not stored parameters

Qwen3.6-35B-A3B activates about 3B parameters per token, which can reduce compute cost. The runtime still needs the 35B model's stored experts. The available 4-bit MLX artifact is about 20.4 GB before the KV cache, temporary buffers, macOS, or other applications, so it is not a 16 GB target.

### Code release and model release are different

OmniShow now has method code, but its own checkpoint is withheld and the setup requires large Wan bases. TokenLight publishes a paper, demos, and an evaluation dataset rather than inference weights. The robot chapters describe integrated physical systems. None of these is a laptop model simply because source code, a project page, or a demo exists.

### Hosted chapters remain useful, but not local

GPT-Rosalind, Happy Oyster, Claude Opus 4.7, and Gemini TTS are accessed as products or APIs. A local client, SDK, plugin, or browser does not change where inference runs. Gemini 3.1 Flash TTS has also moved from “new preview” in the April video to a legacy preview by this review date.

---

## Suggested actions on this machine

For a genuinely local model from the video: Try **Ternary Bonsai 8B Q2_0** through Prism's Metal-enabled llama.cpp fork at 4K context. Increase context only after checking memory pressure and latency.

For the GameWorld benchmark: Run the browser/game harness locally and use a hosted multimodal agent first. Consider a small local VLM only after confirming that its API and image-message format match GameWorld's adapter.

For 3D detection experimentation: Keep WildDet3D as a porting project, not a quick install. The checkpoint size is encouraging, but the custom CUDA dependencies are the real blocker.

For video, animated 3D, and persistent-world generation: Use a rented CUDA GPU or the project's hosted demo where available. MotifVideo, AniGen, Lyra 2, Prompt Relay's Wan base, and the complete HY-World suite are poor uses of time on a 16 GB M2.

For TTS: Use Google's current hosted Gemini TTS generation rather than trying to find local 3.1 weights; no such weights are offered, and Google now recommends the 3.8 family for new work.

## Sources

- Roundup: [YouTube video](https://www.youtube.com/watch?v=G8fqduzB5lc)
- Prompt Relay: [project page](https://gordonchen19.github.io/Prompt-Relay/), [GitHub repository](https://github.com/GordonChen19/Prompt-Relay)
- Ternary Bonsai: [release post](https://prismml.com/news/ternary-bonsai), [8B GGUF model card](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf), [Metal-capable llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp)
- GPT-Rosalind: [OpenAI announcement](https://openai.com/index/introducing-gpt-rosalind/)
- WildDet3D: [project page](https://allenai.github.io/WildDet3D/), [GitHub repository](https://github.com/allenai/WildDet3D)
- MotifVideo: [project page](https://motiftech.io/videoshowcase), [Hugging Face model card](https://huggingface.co/Motif-Technologies/Motif-Video-2B)
- AniGen: [GitHub repository](https://github.com/VAST-AI-Research/AniGen), [project page](https://yihua7.github.io/AniGen_web/)
- Happy Oyster: [product site](https://www.happyoyster.cn/)
- Lyra 2: [GitHub release](https://github.com/nv-tlabs/lyra/tree/main/Lyra-2), [Hugging Face model card](https://huggingface.co/nvidia/Lyra-2.0/blob/main/README.md)
- HY-World 2.0: [GitHub repository](https://github.com/Tencent-Hunyuan/HY-World-2.0)
- OmniShow: [project page](https://correr-zhou.github.io/OmniShow/), [GitHub repository](https://github.com/Correr-Zhou/OmniShow)
- Claude Opus 4.7: [Anthropic announcement](https://www.anthropic.com/news/claude-opus-4-7)
- Qwen3.6-35B-A3B: [Qwen release post](https://qwen.ai/blog?id=qwen3.6-35b-a3b), [official BF16 files](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/tree/main), [community MLX 4-bit files](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit/tree/main)
- Unitree H1: [Unitree company timeline](https://www.unitree.com/about/)
- TokenLight: [project page](https://vrroom.github.io/tokenlight/), [paper](https://arxiv.org/abs/2604.15310), [VisibleFixture-60 evaluation repository](https://github.com/Vrroom/VisibleFixture-60)
- GameWorld: [project page](https://gameworld-project.github.io/), [GitHub repository](https://github.com/gameworld-project/gameworld), [technical report](https://arxiv.org/abs/2604.07429)
- Gemini 3.1 Flash TTS: [Google announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/), [current model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)
