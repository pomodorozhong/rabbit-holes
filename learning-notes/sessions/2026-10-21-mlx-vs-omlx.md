# Session record: MLX vs oMLX, 2026-10-21

## Starting point

- **Already knew:** The user has used MLX for some time and knows it runs faster on a Mac than the GGUF version of the same model. They have used MLX for video generation, music generation, and Whisper.
- **Wanted to understand:** They had heard that oMLX is faster than MLX and wanted to know whether switching would speed up their own workloads.

## Questions and conclusions

### Is oMLX a faster version of MLX?

- **Understood:** oMLX does not replace MLX. It is a local inference server for Apple Silicon, built on MLX: it calls mlx-lm for text models, mlx-vlm for vision-language models, and mlx-embeddings for embeddings, and it exposes OpenAI- and Anthropic-compatible APIs from a macOS menu bar app. Its speed comes from reusing work across requests: continuous batching, a prefix cache that reuses the KV cache for text it has already processed, and a second cache tier on the SSD that survives restarts. These help most when long prompts are resent, as in chats and coding agents. A single request should run at about mlx-lm speed, which is an inference, not a measurement. The README gives no speedup figures for these features; its one figure (about 30x prefill for GLM-5.2 on an M3 Ultra) compares custom kernels with oMLX's own fallback, not with plain MLX.
- **Check:** covered but not checked.
- **Sources:** [oMLX README](https://github.com/jundot/omlx), read 2026-10-21.

### Does oMLX plan to support speech, image, video, or music workloads?

- **Understood:** As of 2026-10-21, the answer differs by workload. Speech-to-text, including Whisper, has shipped: Whisper worked by v0.3.x, and v0.7.1 added realtime transcription for every speech-to-text model. Text-to-speech appears to exist, because a v0.7.2 fix mentions TTS sampling fields, but the release that added it was not found. Image generation is unclear: the feature request was closed in a tracker cleanup rather than rejected, and draft PRs #4724 and #4695 add image pipelines. No sign of video or music generation was found; video appears only as an input to vision models. Because oMLX runs speech through mlx-audio and its caching targets repeated LLM prompts, Whisper on oMLX would mostly bring convenience rather than speed. That last point is an inference, not a benchmark.
- **Check:** covered but not checked.
- **Correction:** An earlier answer in the session, based on a README summary, said oMLX would do nothing for Whisper. The release notes and issues showed that was wrong.
- **Sources:** [issue #218](https://github.com/jundot/omlx/issues/218), [issue #477](https://github.com/jundot/omlx/issues/477), [issue #1072](https://github.com/jundot/omlx/issues/1072), [releases](https://github.com/jundot/omlx/releases) (v0.7.1, v0.7.2). All read 2026-10-21.

## The user's views and conclusions

- The user's goal is speed, so they were disappointed that oMLX would not help their video and music generation.
- After learning that oMLX already serves Whisper, the user decided to wait a while before trying Whisper on oMLX.

## Set aside

- None.

## Open questions

- Which part of the user's Whisper use is slow: long-file transcription or live transcription latency? This was asked but not answered.
- Is Whisper through oMLX faster or slower than calling mlx-audio or mlx-whisper directly? Not benchmarked.
- Which oMLX release added text-to-speech, and which models does it serve?
- Will the draft image-generation PRs be merged, and does the maintainer intend to support image generation?
- Is there any plan for video or music generation? None was found.
