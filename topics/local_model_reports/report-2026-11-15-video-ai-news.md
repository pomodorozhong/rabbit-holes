# Weekly AI video report — 2026-11-15

**Source:** [Gemini 4 Carbon & Hydrogen, realtime voices, new TTS, 3D models, Seedream 5.5: AI NEWS](https://www.youtube.com/watch?v=woWo80dPkVk) by AI Search · published November 15, 2026 in Taipei (November 14 Pacific) · 45:51\
**Target:** M2 MacBook Pro with 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Evidence as of November 16:** All 27 chapters, plus the video's auto-generated English captions. Local fit is inferred from released files and runtime documentation. No model was benchmarked on this M2.

## Worth trying on your Mac

This week's useful local releases are both about speech. **ZONOS3-Mini** is a text-to-speech model with voice cloning whose default Mac files total about 1.2 GB, so it is the easy first test. **Haru 4B** is a model you talk with in real time, and it has a native macOS app, but its 10.5 GB checkpoint uses most of the memory this machine can spare.

| Configuration | Best for | Mac fit |
| --- | --- | --- |
| [ZONOS3-Mini, default GGUF files on the MLX server](#speech-generation) | ❓ Speech synthesis and voice cloning | ✅ Comfortable |
| [Haru 4B in the Haru for macOS app, 8-bit backbone](#spoken-conversation) | ❓ Real-time spoken conversation | ⚠️ Constrained |

**Comfortable** means the listed files leave room for normal use. **Constrained** means the model can fit only if other applications are closed and the suggested limits are kept. Artifact sizes use decimal GB. Both models list Chinese, but neither documents Traditional characters or Guoyu delivery; see [Chinese script and Guoyu](#chinese-script-and-guoyu) before relying on either for Guoyu speech.

### Speech generation

**ZONOS3-Mini** from Zyphra turns text into speech in a voice taken from a short reference clip, and lets you steer accent, mood and delivery. It is a Mixture-of-Experts model: 800 million parameters in total, of which about 100 million are used for each step. Zyphra reports under 150 ms to the first audio on an M3 MacBook Air, which suggests it can keep up with real time on Apple silicon, though no M2 timing was found. The repository's Apple silicon path is an MLX server that reads the same GGUF files as the C++ server. Three of them are needed for speech: the 0.66 GB quantized backbone, the 0.45 GB default decoder and a 0.045 GB speaker encoder. Cloning from raw audio rather than a saved voice loads two more files (5.58 GB) on first use and frees them when idle, which still keeps the total under the 8 GB comfort line. Code and weights are Apache-2.0. [Announcement](https://www.zyphra.com/our-work/zonos3-mini) · [Repository](https://github.com/Zyphra/ZONOS3-Mini) · [Weights](https://huggingface.co/Zyphra/ZONOS3-Mini) · [Video chapter](https://www.youtube.com/watch?v=woWo80dPkVk&t=1415s)

### Spoken conversation

**Haru 4B** from higurashi listens and speaks at the same time. Every 133 ms it reads one frame of your audio and produces one frame of its own speech, so it can laugh, interrupt or say "mm-hm" while you talk, instead of waiting for you to finish. The authors release it as a pretrained base model, not an instruction-tuned assistant, so expect natural conversation rather than reliable answers. The checkpoint is one 10.54 GB BF16 file. The authors' macOS app README says 16 GB of memory is the practical minimum, and the app can switch the language model to 8-bit in its settings. Start with the native app, close other large applications, and switch to 8-bit before a long conversation. Whether the 8-bit switch avoids a full BF16 load first was not checked, so the first load may still peak near the checkpoint size. Code and weights are Apache-2.0. [Announcement](https://www.higurashi.ai/haru4b/) · [Repository](https://github.com/higurashi-ai/Haru) · [Weights](https://huggingface.co/higurashi-ai/Haru-4B) · [Video chapter](https://www.youtube.com/watch?v=woWo80dPkVk&t=1210s)

## Other developments worth knowing

- **Sophon-Realtime** is another open full-duplex voice model with an official Mac build, but that build is the 32B Flash model in 4-bit MLX (24.66 GB), and its authors recommend 36 GB or more of memory. The new 4B builds (November 16) target one 24–32 GB consumer GPU. Neither fits this Mac. [Repository](https://github.com/adventists-ai/sophon-realtime)
- **Gemini 4 Carbon and Gemini 4 Hydrogen** are Google's new hosted models. Carbon costs $2 per million input tokens and $10 per million output tokens through the API; Hydrogen, the faster tier, costs $1.50 and $7.50. In the video, the narrator's own tests of Carbon were disappointing, while public leaderboards placed it among the top three frontier models. [Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) · [Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/)
- **Gemini Decisions API** answers multiple-choice questions about text, images or audio quickly, priced at $0.10 per million input tokens with no output charge. It is a hosted service for routing and classification. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/)
- **Large open releases.** MiniMax H3 Image (an open image model with 2K and 4K output) has a 204 GB repository. PAN 2, a world model that turns actions into video, needs a 29B diffusion model plus a 9B text encoder. ERNIE 5.5 Flash Preview has 280B total parameters, with weights promised under Apache 2.0. None fits this Mac.
- **Budget3D** turns one image into 3D Gaussian splats and lets you trade quality for speed with a token budget. Its weights are only 1.5–1.6 GB, but the code requires a CUDA GPU. [Project](https://budgetany.github.io/budget3d/)

## Technical appendix

### Complete video chapter inventory

All 27 chapters follow the official description and timestamps. "❌ Hosted" means no public local weights were verified. "⚠️ Unverified" records unresolved deployment evidence; "— N/A" covers editorial, sponsor, robotics hardware and research without a standalone inference configuration.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [00:00](https://www.youtube.com/watch?v=woWo80dPkVk&t=0s) | AI news intro | Editorial | — N/A; introduces the roundup. |
| [01:03](https://www.youtube.com/watch?v=woWo80dPkVk&t=63s) | [Budget3D](https://budgetany.github.io/budget3d/) | Open weights / image to 3D | ❌ Outside the supported path; 1.5 GB weights, but the README requires a CUDA GPU. |
| [02:18](https://www.youtube.com/watch?v=woWo80dPkVk&t=138s) | [Reshoot 4D](https://itsmetamike.github.io/reshoot-4d/) | Tool / ComfyUI workflow | ❌ Outside budget; tested on Ubuntu with a 24 GB RTX 3090, and LTX 2.3 renders the final frames. |
| [03:15](https://www.youtube.com/watch?v=woWo80dPkVk&t=195s) | [SplatAnything](https://zju3dv.github.io/SplatAnything/) | 3D research / code linked | ⚠️ Unverified; the page links code and a demo but states no requirements. |
| [04:21](https://www.youtube.com/watch?v=woWo80dPkVk&t=261s) | [Open-H3-Regenerate-2K IC](https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K/) | Open LoRA / video upscaling | ❌ Outside budget; a LoRA on the frozen MiniMax H3 video model, timed on one B200. |
| [05:13](https://www.youtube.com/watch?v=woWo80dPkVk&t=313s) | [Gemini 4 Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) | Hosted LLM | ❌ Hosted; API, Antigravity and Gemini app. |
| [12:39](https://www.youtube.com/watch?v=woWo80dPkVk&t=759s) | "THE MOST IMPORTANT PART" | Editorial | — N/A; continues the Carbon review with the narrator's image and coding tests and public leaderboards. |
| [17:08](https://www.youtube.com/watch?v=woWo80dPkVk&t=1028s) | [Seedream 5.5](https://www.byteplus.com/en/contact-us/seedream5-5) | Sponsor / hosted image model | ❌ Hosted; BytePlus API. |
| [18:55](https://www.youtube.com/watch?v=woWo80dPkVk&t=1135s) | [Gemini 4 Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) | Hosted LLM | ❌ Hosted; API and Google apps. |
| [20:10](https://www.youtube.com/watch?v=woWo80dPkVk&t=1210s) | [Haru 4B](https://www.higurashi.ai/haru4b/) | Open weights / full-duplex speech | ⚠️ Constrained; 10.54 GB BF16 checkpoint, native macOS app with an 8-bit option. |
| [22:03](https://www.youtube.com/watch?v=woWo80dPkVk&t=1323s) | [Fish Audio Live 3](https://fish.audio/live3/) | Hosted voice agent | ❌ Hosted; priced per minute. |
| [23:35](https://www.youtube.com/watch?v=woWo80dPkVk&t=1415s) | [ZONOS3-Mini](https://www.zyphra.com/our-work/zonos3-mini) | Open weights / text to speech | ✅ Comfortable; about 1.16 GB of default GGUF files, MLX server for Apple silicon. |
| [25:33](https://www.youtube.com/watch?v=woWo80dPkVk&t=1533s) | [Sophon-Realtime](https://github.com/adventists-ai/sophon-realtime) | Open weights / full-duplex speech | ❌ Outside budget; the Mac build is 24.66 GB and recommends 36 GB or more. |
| [27:21](https://www.youtube.com/watch?v=woWo80dPkVk&t=1641s) | [MiniMax H3 Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | Open weights / image | ❌ Outside budget; 204 GB repository. The description links only the narrator's [tutorial](https://youtu.be/Er0740eVIEw). |
| [28:02](https://www.youtube.com/watch?v=woWo80dPkVk&t=1682s) | [LingBot-Touch](https://technology.robbyant.com/lingbot-touch) | Open weights / tactile encoder | — N/A; the 5.46M-parameter encoder is tiny but needs tactile sensor recordings as input. |
| [29:19](https://www.youtube.com/watch?v=woWo80dPkVk&t=1759s) | [Flash ALOHA](https://johnyao93.github.io/flash-aloha/) | Robotics hardware and research | — N/A; a bimanual robot system, not a standalone model. |
| [30:41](https://www.youtube.com/watch?v=woWo80dPkVk&t=1841s) | [ACE Music v1](https://acemusic.ai/acemusic-v1/) | Hosted music model | ❌ Hosted; a smaller Flash version is planned as open source in late 2026. |
| [34:07](https://www.youtube.com/watch?v=woWo80dPkVk&t=2047s) | [MPEG-Diffusion](https://dennismenn.github.io/mpeg-diffusion/) | Video generation research | ⚠️ Unverified; code is marked as coming soon, and results use Wan2.1 14B. |
| [35:25](https://www.youtube.com/watch?v=woWo80dPkVk&t=2125s) | [Muse Ember](https://dev.meta.ai/models/muse-ember) | Hosted LLM | ❌ Hosted; Meta's API and Muse Code plans. |
| [36:24](https://www.youtube.com/watch?v=woWo80dPkVk&t=2184s) | [ERNIE 5.5 Flash Preview](https://ernie.baidu.com/release/ernie-5-5-flash-preview/) | Hosted LLM, weights announced | ❌ Outside budget; 280B total and 14B active parameters, weights "soon". |
| [37:15](https://www.youtube.com/watch?v=woWo80dPkVk&t=2235s) | [Gemini Decisions API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/) | Hosted classifier | ❌ Hosted; Gemini API. |
| [38:10](https://www.youtube.com/watch?v=woWo80dPkVk&t=2290s) | [NovaAtom-Lite](https://www.geodesiclab.com/news/introducing-novaatom-lite) | Hosted structure prediction | ❌ Hosted; Geodesic API and NovaDDE. |
| [39:33](https://www.youtube.com/watch?v=woWo80dPkVk&t=2373s) | [AlphaGenome 2](https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/) | Hosted genomics model | ❌ Hosted; non-commercial API access. |
| [41:04](https://www.youtube.com/watch?v=woWo80dPkVk&t=2464s) | [Iris-Z](https://speridlabs.com/research/iris-z) | Open weights / image and depth | ❌ Outside budget; 9B and 32B versions, about 33 GB and 112 GB of GPU memory. |
| [42:21](https://www.youtube.com/watch?v=woWo80dPkVk&t=2541s) | [PAN 2](https://huggingface.co/IFM/PAN2) | Open weights / world model | ❌ Outside budget; 86 GB repository and a CUDA setup. |
| [43:19](https://www.youtube.com/watch?v=woWo80dPkVk&t=2599s) | [pi-H3](https://hanshengchen.com/blog/pi-h3/) | Video generation research | ❌ Outside budget; a few-step version of MiniMax H3, with weights due November 16–22. |
| [44:17](https://www.youtube.com/watch?v=woWo80dPkVk&t=2657s) | [PixVid](https://chenshuo20.github.io/PixVid/) | Video generation research | ⚠️ Unverified; fine-tuned from Wan2.1-14B, and no release was checked. |

### Deployment evidence

The machine usually has **8–11 GB** available for weights and working memory after macOS and other applications. A file's size is only the starting cost: speech models also hold audio buffers and a cache that grows with the conversation. The starting points above are suggested first trials, and peak memory and speed on the target M2 are unmeasured. [Shared hardware assumptions](./memory-budget.md)

| Configuration and artifact evidence | What has to fit | Runtime and licensing |
| --- | --- | --- |
| [ZONOS3-Mini GGUF files](https://huggingface.co/Zyphra/ZONOS3-Mini/tree/main/gguf) | Default speech: `backbone-ptq.gguf` 0.66 GB (Q4_0 experts, Q8_0 mixers), `zac-keep2.gguf` 0.45 GB, `spk-encoder.gguf` 0.045 GB. Raw-reference cloning adds `zac-encoder.gguf` 4.03 GB and `ssl-teacher.gguf` 1.55 GB, loaded on first use. The repository's quick start downloads the whole `gguf/` folder (about 9.9 GB, including an optional 2.20 GB full-size decoder). | Apache-2.0. The [MLX server](https://github.com/Zyphra/ZONOS3-Mini/blob/main/servers/mlx/README.md) runs the GGUF files on Apple silicon; the [ggml server](https://github.com/Zyphra/ZONOS3-Mini/blob/main/servers/ggml/README.md) supports Metal and lists the minimal three-file download. |
| [Haru-4B checkpoint](https://huggingface.co/higurashi-ai/Haru-4B/tree/main) | One 10.54 GB BF16 `model.safetensors`. The 8-bit option covers the language model's weight matrices and embeddings; the audio codec and head stay at checkpoint precision. | Apache-2.0 code and weights. [haru_mlx](https://github.com/higurashi-ai/Haru/blob/main/haru_mlx/README.md) uses custom Metal kernels; the [macOS app](https://github.com/higurashi-ai/Haru/blob/main/haru_mlx/swift/README.md) needs macOS 13 and the Command Line Tools. |

### Other chapter notes

- **Why Sophon-Realtime does not fit despite a Mac build.** All three 32B builds share one 32B "brain" that listens and writes the reply; they differ only in how the reply becomes sound. The Mac build is that brain in 4-bit MLX plus a 3.86 GB speech model. The 4B builds keep the turn-taking but, by the authors' own numbers, know much less (VoiceBench 62.4 against 82.8 for 32B). The smallest 4B build's repository is 13.0 GB. [Repository](https://github.com/adventists-ai/sophon-realtime) · [4B Flash weights](https://huggingface.co/adventists-ai/Sophon-Realtime-4B-Flash)
- **The Gemini 4 Carbon review spans two chapters.** The narrator ran the same tests as an earlier Fable 5.2 review. In the captions, they report that Carbon found the hidden frog in an image test, identified one of six brain tumor types, and produced a poor water-balloon physics animation. These are single informal runs, not benchmarks.
- **Video research built on large models.** Open-H3-Regenerate-2K and pi-H3 both build on MiniMax H3, whose repository is 498 GB. MPEG-Diffusion and PixVid report results on Wan2.1 14B. They are useful as research directions, not as local tools for this machine.
- **Science models.** NovaAtom-Lite predicts the 3D structure of proteins, DNA, RNA and bound molecules, and its authors report beating AlphaFold 3 on antibody–antigen interfaces. AlphaGenome 2 predicts how DNA variants affect gene activity in specific cell types. Both are reached through their providers' APIs. [NovaAtom-Lite](https://www.geodesiclab.com/news/introducing-novaatom-lite) · [AlphaGenome 2](https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/)

### Chinese script and Guoyu

Here, **Guoyu** and **Putonghua** refer to two closely related Mandarin standards with distinct conventions in pronunciation and usage. A model's "Chinese support" can mean several separate things: it reads Traditional characters, it follows Guoyu readings, or it produces Guoyu timing and intonation. Each needs its own evidence. [Why Guoyu TTS can still sound like Putonghua](../../learning-notes/04-guoyu-voice-cloning.md) explains the distinction in more detail.

**ZONOS3-Mini** lists "Mandarin Chinese" (`zh`) among its 43 languages, and its text normalizer has a Mandarin grammar. Neither the [model card](https://huggingface.co/Zyphra/ZONOS3-Mini) nor the [normalizer](https://github.com/Zyphra/zyphra-textnorm) mentions Traditional characters (`zh-Hant`) or a `zh-TW` locale. Its [8,192-entry tokenizer](https://huggingface.co/Zyphra/ZONOS3-Mini/blob/main/lm/zonos3_mini/tokenizer/superbpe8192.json) is byte-level, so any character can be encoded, but only 414 Chinese characters have their own entry. In one 24-character test sentence, 9 Traditional characters had their own entry, against 17 for the same sentence in Simplified characters; the rest split into byte fragments. Fewer whole-character entries suggest that the model saw these characters less often in training, but the count does not show how the speech sounds. Converting the text to Simplified characters first (for example with OpenCC) is a reasonable experiment, though it can lose Guoyu-specific vocabulary and readings.

**Haru 4B** lists "Chinese" (`zh`) among nine languages on its [model card](https://huggingface.co/higurashi-ai/Haru-4B), without naming a script or a regional standard. Because it listens to speech and speaks back, script matters mainly for the text character card and the text the model writes alongside its speech. Which script that text uses was not checked.

For both models, a Guoyu reference clip sets the voice, but cloning can copy a speaker's timbre more reliably than their accent. Whether either model's output sounds like Guoyu to Guoyu-speaking listeners is untested. A short listening test with the same sentences in both scripts, compared against a real Guoyu speaker, would answer it.

### Coverage and verification limits

The chapter inventory follows the video's official description and timestamps. The video's auto-generated English captions were retrieved and used for the two chapters without a primary source of their own ("THE MOST IMPORTANT PART" and MiniMax H3 Image) and to check what the narrator said about the local candidates. The description links a tutorial video rather than a release page for MiniMax H3 Image, so that row points to MiniMax's model repository instead.

Artifact sizes come from Hugging Face file listings on November 16. Speed figures are attributed to their sources: ZONOS3-Mini's timing comes from an M3 MacBook Air, and other timings come from H100, B200 or RTX PRO 6000 GPUs. None is an M2 result.

## Sources

- **Chapter coverage:** [AI Search video, official description, and chapter list](https://www.youtube.com/watch?v=woWo80dPkVk). The chapter table links the primary source for each item.
- **Local candidates:** [ZONOS3-Mini announcement](https://www.zyphra.com/our-work/zonos3-mini), [ZONOS3-Mini repository](https://github.com/Zyphra/ZONOS3-Mini), [ZONOS3-Mini weights](https://huggingface.co/Zyphra/ZONOS3-Mini), [Haru 4B announcement](https://www.higurashi.ai/haru4b/), [Haru repository](https://github.com/higurashi-ai/Haru), and [Haru-4B weights](https://huggingface.co/higurashi-ai/Haru-4B).
- **Near misses:** [Sophon-Realtime](https://github.com/adventists-ai/sophon-realtime), [Sophon-Realtime 32B Flash 4-bit MLX](https://huggingface.co/adventists-ai/Sophon-Realtime-32B-Flash-4bit-MLX), [Budget3D repository](https://github.com/BudgetAny/Budget3D), and [Budget3D-Idol weights](https://huggingface.co/BudgetAny/Budget3D-Idol).
- **Hosted releases:** [Gemini 4 Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/), [Gemini 4 Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/), [Gemini Decisions API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/), [Fish Audio Live 3](https://fish.audio/live3/), [Muse Ember](https://dev.meta.ai/models/muse-ember), [ACE Music v1](https://acemusic.ai/acemusic-v1/), and [Seedream 5.5](https://www.byteplus.com/en/contact-us/seedream5-5).
- **Large open or announced models:** [MiniMax H3 Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image), [PAN 2](https://huggingface.co/IFM/PAN2), [Iris-Z](https://huggingface.co/speridlabs/iris-z), [ERNIE 5.5 Flash Preview](https://ernie.baidu.com/release/ernie-5-5-flash-preview/), and [pi-H3](https://hanshengchen.com/blog/pi-h3/).
