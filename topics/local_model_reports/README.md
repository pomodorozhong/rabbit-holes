# Local Model Reports

Notes and shortlists for local models (Metal / MLX / llama.cpp / Ollama / audio pipelines), aimed at machines without a discrete GPU.

Shared hardware note: [Your real memory budget](./memory-budget.md).

## Reports

| Report | Window | Focus |
| --- | --- | --- |
| [report-2026-07-17.md](./report-2026-07-17.md) | mid-May → mid-July 2026 | LLMs that fit a 16 GB M2 MacBook Pro, vs Gemma 4 12B Unified |
| [report-2026-08-31.md](./report-2026-08-31.md) | mid-July → late August 2026 | Sequel shortlist vs Gemma 4 12B Unified: Ling-3.0-tiny, Ornith 1.5 9B, Bonsai 27B |
| [report-2026-07-27-music.md](./report-2026-07-27-music.md) | as of 2026-07-27 | Local **music generation**: clip vs song, streaming, VRAM, Mac fit, vs LLMs; cites r/LocalLLaMA & r/StableDiffusion |
| [report-2026-08-02-video-ai-news.md](./report-2026-08-02-video-ai-news.md) | video [OrcBSpADCGk](https://youtu.be/OrcBSpADCGk) (as of 2026-08-02) | Runnability on 16 GB M2 for every model named in that AI-news video; deep dive on CrisperWhisper + Instella |
| [report-2026-08-16-video-ai-news.md](./report-2026-08-16-video-ai-news.md) | video [62HSUsS0ypo](https://www.youtube.com/watch?v=62HSUsS0ypo) (as of 2026-08-16) | Runnability on 16 GB M2 for every model named in that AI-news video; IndexTTS 2.5 + Qwen3.8-27B vs the rest |
| [report-2026-08-23-video-ai-news.md](./report-2026-08-23-video-ai-news.md) | video [rQ4yX5qNYdY](https://youtu.be/rQ4yX5qNYdY) (as of 2026-08-23) | Runnability on 16 GB M2 for every model named in that AI-news video; Audio8-TTS 0.1B + Ornith 1.5 9B vs the rest |
| [report-2026-08-25-ltx-2.5.md](./report-2026-08-25-ltx-2.5.md) | as of 2026-08-25 | **LTX-2.5** deep dive vs **LTX-2.3** on the 16 GB M2; why the “16 GB VRAM” floor is not 16 GB unified |
| [report-2026-08-30-video-ai-news.md](./report-2026-08-30-video-ai-news.md) | video [4wjHNgMLeyY](https://www.youtube.com/watch?v=4wjHNgMLeyY) (as of 2026-08-30) | Runnability on 16 GB M2 for every model named in that AI-news video; MLX ports for GLM-5.3-Flash / Qwen3.8-Flash-Next / FastH3 / Fibo vs VoiceMem |
| [report-2026-09-06-video-ai-news.md](./report-2026-09-06-video-ai-news.md) | video [ngyFRCNq0Yc](https://www.youtube.com/watch?v=ngyFRCNq0Yc) (as of 2026-09-06) | Runnability on 16 GB M2 for every model named in that AI-news video; TimesFM-3 vs H3 world-model stack / frontier APIs |
| [report-2026-09-13-video-ai-news.md](./report-2026-09-13-video-ai-news.md) | video [nZYJdwM-_nI](https://www.youtube.com/watch?v=nZYJdwM-_nI) (as of 2026-09-13) | Runnability on 16 GB M2 for every chapter in that AI-news video; MiniCPM5-2B + Edge0-8B vs CUDA-heavy world, 3D, robot, and audio stacks |
| [report-2026-09-20-video-ai-news.md](./report-2026-09-20-video-ai-news.md) | video [hygMRgnDD7w](https://www.youtube.com/watch?v=hygMRgnDD7w) (as of 2026-09-20) | Runnability on 16 GB M2 for every chapter in that AI-news video; Needle 3 + Laya, Bonsai 2 and R2T2 near-miss analysis |

## Scripts

| Script | Purpose |
| --- | --- |
| [`scripts/fetch_localllama_posts.py`](./scripts/fetch_localllama_posts.py) | Fetch r/LocalLLaMA posts via the Arctic Shift archive API |
