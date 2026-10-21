# MLX vs oMLX

I use [MLX](https://github.com/ml-explore/mlx) to run models on a Mac because it runs faster than the GGUF version of the same model. I've used it for video generation, music generation, and Whisper. I heard oMLX is even faster, so I wanted to know whether switching would speed up my work.

**Short answer:** oMLX is not a faster MLX. It is a server built on top of MLX. It saves time by not redoing work across requests to text models, so it helps chat and agent workloads that resend long prompts. It does not make my generation workloads faster, and it does not serve video or music generation at all. Facts about oMLX are as of 2026-10-21; the project releases often.

## What oMLX is

[oMLX](https://github.com/jundot/omlx) is a local inference server for Apple Silicon. It runs as a macOS menu bar app and exposes OpenAI- and Anthropic-compatible APIs. Underneath, it calls Apple's MLX libraries: mlx-lm for text models, mlx-vlm for vision-language models, and mlx-audio for speech. So for a single request, it generates tokens through the same code as running mlx-lm directly. That should give about the same speed, although I haven't measured it.

## Where its speed comes from

Before a language model can answer, it reads the whole prompt. This step is called **prefill**. It produces the **KV cache**, which holds the model's intermediate results for the text it has read. A basic setup throws that cache away after each request, so a long prompt sent again is read again from scratch.

oMLX keeps the cache. When a new request starts with text it has already processed, such as the same system prompt, earlier conversation, or an agent's tool history, oMLX reuses the stored cache for that part and only prefills the new text. When RAM fills up, it moves cache blocks to the SSD instead of discarding them, and they survive a server restart. It also batches concurrent requests together. Its [README](https://github.com/jundot/omlx) describes these features but gives no speedup figures for them.

The gain is largest for coding agents and long chats, where every turn resends a long, mostly unchanged prompt. It does little for a single one-off request.

## What it covers

| Workload | oMLX status | Source |
| --- | --- | --- |
| LLMs, vision-language models, OCR, embeddings | Supported. This is the core. | [README](https://github.com/jundot/omlx) |
| Whisper and other speech-to-text models | Supported. Whisper worked by v0.3.x. v0.7.1 added realtime transcription for every speech-to-text model. | [#1072](https://github.com/jundot/omlx/issues/1072), [releases](https://github.com/jundot/omlx/releases) |
| Text-to-speech | Probably supported. A v0.7.2 fix mentions "TTS sampling fields", but I didn't find which release added TTS. | [releases](https://github.com/jundot/omlx/releases) |
| Image generation | Unclear. The feature request was closed in an issue-tracker cleanup, not rejected, and draft PRs (#4724, #4695) add image pipelines. | [#477](https://github.com/jundot/omlx/issues/477) |
| Video and music generation | No sign of plans. Video appears only as an input to vision models. | — |

The maintainer said in March 2026 that speech-to-text and text-to-speech would come through MLX-Audio ([#218](https://github.com/jundot/omlx/issues/218)), and that has mostly happened.

## Whisper on oMLX

Even for Whisper, oMLX probably wouldn't be faster, because it runs speech through mlx-audio, the same library I'd call directly. Its caching targets LLM prompts that repeat, and transcription doesn't repeat. The gain is convenience: one server and one API for both text and speech. This is an inference from how oMLX is built, not a benchmark. I've decided to wait a while before trying Whisper on oMLX.

## Open questions

- Is Whisper through oMLX any faster or slower than calling mlx-audio directly?
- Which part of my Whisper use is slow: long files or live transcription latency? The answer decides where a speedup would have to come from.
- Will the image-generation PRs be merged?
