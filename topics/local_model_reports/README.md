# Local Model Reports

Notes and shortlists for local models (Metal / MLX / llama.cpp / Ollama / audio pipelines), aimed at machines without a discrete GPU.

Shared hardware note: [Your real memory budget](./memory-budget.md).

Reusable formats: [Community shortlist](../../.agents/skills/ai-research-report/assets/local-community-shortlist-template.md) and [weekly AI video report](../../.agents/skills/ai-research-report/assets/weekly-video-ai-news-template.md). Both keep the main report concise and deployment evidence in an appendix; weekly reports also retain every video chapter.

## Reports

| Report | Window | Focus |
| --- | --- | --- |
| [report-2026-07-17.md](./report-2026-07-17.md) | mid-May → mid-July 2026 | LLMs that fit a 16 GB M2 MacBook Pro, vs Gemma 4 12B Unified |
| [report-2026-08-31.md](./report-2026-08-31.md) | mid-July → late August 2026 | Sequel shortlist vs Gemma 4 12B Unified: Ling-3.0-tiny, Ornith 1.5 9B, Bonsai 27B |
| [report-2026-10-03.md](./report-2026-10-03.md) | September → October 2, 2026; searched 2026-10-03 | September community roundup for the 16 GB M2: text/coding, Jev-style decisions, music, images/editing, and video; compact model cards with deployment evidence in an appendix |
| [report-2026-07-27-music.md](./report-2026-07-27-music.md) | as of 2026-07-27 | Local **music generation**: clip vs song, streaming, VRAM, Mac fit, vs LLMs; cites r/LocalLLaMA & r/StableDiffusion |
| [report-2026-08-02-video-ai-news.md](./report-2026-08-02-video-ai-news.md) | video [OrcBSpADCGk](https://youtu.be/OrcBSpADCGk) (as of 2026-08-02) | Runnability on 16 GB M2 for every model named in that AI-news video; deep dive on CrisperWhisper + Instella |
| [report-2026-08-16-video-ai-news.md](./report-2026-08-16-video-ai-news.md) | video [62HSUsS0ypo](https://www.youtube.com/watch?v=62HSUsS0ypo) (as of 2026-08-16) | Runnability on 16 GB M2 for every model named in that AI-news video; IndexTTS 2.5 + Qwen3.8-27B vs the rest |
| [report-2026-08-23-video-ai-news.md](./report-2026-08-23-video-ai-news.md) | video [rQ4yX5qNYdY](https://youtu.be/rQ4yX5qNYdY) (as of 2026-08-23) | Runnability on 16 GB M2 for every model named in that AI-news video; Audio8-TTS 0.1B + Ornith 1.5 9B vs the rest |
| [report-2026-08-25-ltx-2.5.md](./report-2026-08-25-ltx-2.5.md) | as of 2026-08-25 | **LTX-2.5** deep dive vs **LTX-2.3** on the 16 GB M2; why the “16 GB VRAM” floor is not 16 GB unified |
| [report-2026-08-30-video-ai-news.md](./report-2026-08-30-video-ai-news.md) | video [4wjHNgMLeyY](https://www.youtube.com/watch?v=4wjHNgMLeyY) (as of 2026-08-30) | Runnability on 16 GB M2 for every model named in that AI-news video; MLX ports for GLM-5.3-Flash / Qwen3.8-Flash-Next / FastH3 / Fibo vs VoiceMem |
| [report-2026-09-06-video-ai-news.md](./report-2026-09-06-video-ai-news.md) | video [ngyFRCNq0Yc](https://www.youtube.com/watch?v=ngyFRCNq0Yc) (as of 2026-09-06) | Runnability on 16 GB M2 for every model named in that AI-news video; TimesFM-3 vs H3 world-model stack / frontier APIs |
| [report-2026-09-13-video-ai-news.md](./report-2026-09-13-video-ai-news.md) | video [nZYJdwM-_nI](https://www.youtube.com/watch?v=nZYJdwM-_nI) (as of 2026-09-13) | Runnability on 16 GB M2 for every chapter in that AI-news video; MiniCPM5-2B + Edge0-8B vs CUDA-heavy world, 3D, robot, and audio stacks |
| [report-2026-09-20-video-ai-news.md](./report-2026-09-20-video-ai-news.md) | video [hygMRgnDD7w](https://www.youtube.com/watch?v=hygMRgnDD7w) (as of 2026-09-20) | Runnability on 16 GB M2 for every chapter in that AI-news video; Needle 3 + Laya, Bonsai 2 and R2T2 near-miss analysis |
| [report-2026-09-22-qwen-image-2.1.md](./report-2026-09-22-qwen-image-2.1.md) | as of 2026-09-22 | **Qwen-Image-2.1** on the 16 GB M2: full-pipeline footprint, GGUF/ComfyUI path, MPS edit bug, LoRA and license caveats |
| [report-2026-09-28-video-ai-news.md](./report-2026-09-28-video-ai-news.md) | video [nX0fgBL3sIM](https://www.youtube.com/watch?v=nX0fgBL3sIM) (as of 2026-09-28) | Runnability on 16 GB M2 for every chapter in that AI-news video; Supra2-IMG as the practical local candidate, with Limite 1B / CLM near-misses and large hosted, robotics, and research stacks separated out |
| [report-2026-10-04-video-ai-news.md](./report-2026-10-04-video-ai-news.md) | video [lHmZoRHMZyM](https://www.youtube.com/watch?v=lHmZoRHMZyM) (as of 2026-10-04) | All 28 chapters; Whistle and Phonon-2 for local speech recognition, AstaBrief Q4 for cited synthesis, and full-pipeline checks for InSpatio, PixelUMM, DMAD and PDMD |
| [report-2026-10-12-video-ai-news.md](./report-2026-10-12-video-ai-news.md) | video [X0_GDOkLKzQ](https://youtu.be/X0_GDOkLKzQ) (as of 2026-10-12) | All 22 chapters; EmbeddingGemma 2 for local search, Botanic1-M with window/batch limits for plant DNA scoring, and experimental ALoDLM-1.7B CPU decoding; 8B GGUF gap and Kandinsky 6.0 / Iris-3B full-pipeline checks |
| [report-2026-10-15-minicpm-v-4.7.md](./report-2026-10-15-minicpm-v-4.7.md) | video [JYTXQ7oFTLA](https://youtu.be/JYTXQ7oFTLA) (as of 2026-10-15) | Focused MiniCPM-V 4.7 deep dive; 1B local vision path, 35B-A3B LES experiment, and capability comparison with Gemma 4 E2B, E4B, and 12B |
| [report-2026-10-18-video-ai-news.md](./report-2026-10-18-video-ai-news.md) | video [tDWtcyeNNew](https://youtu.be/tDWtcyeNNew) (as of 2026-10-18) | All 27 chapters; FLUX 3 Image Klein through a 6-bit MLX port for local image generation and editing, experimental 2–3-bit LFM2.5-24B-A2B for tool-calling agents, and an unverified MOSS-Image path through `stable-diffusion.cpp` and a 3-bit text encoder |

## Scripts

| Script | Purpose |
| --- | --- |
| [`scripts/fetch_localllama_posts.py`](./scripts/fetch_localllama_posts.py) | Fetch r/LocalLLaMA posts via the Arctic Shift archive API |
