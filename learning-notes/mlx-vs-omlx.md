# MLX vs oMLX

**Bottom line:** oMLX isn't a faster MLX. It's a server on top of MLX that saves time by reusing work between text requests. It won't speed up my video, music, or Whisper work. *(As of 2026-10-21.)*

**What it is**

- A local inference server for Apple Silicon ([oMLX](https://github.com/jundot/omlx)), running as a menu bar app with OpenAI- and Anthropic-compatible APIs.
- It calls mlx-lm, mlx-vlm, and mlx-audio underneath, so a single request should be about as fast as plain [MLX](https://github.com/ml-explore/mlx). I haven't measured this.

**Where the speed comes from**

- It keeps the **KV cache**, the model's stored results from reading a prompt, and reuses it when a new prompt starts with text it has already seen.
- It moves the cache to the SSD instead of discarding it, and the cache survives restarts.
- It batches concurrent requests.
- So it helps coding agents and long chats, which resend long prompts every turn, not one-off requests. The [README](https://github.com/jundot/omlx) gives no speedup numbers.

**Coverage**

| Workload | Status |
| --- | --- |
| Text, vision, OCR, embeddings | Supported ([README](https://github.com/jundot/omlx)) |
| Whisper / speech-to-text | Supported since v0.3.x ([#1072](https://github.com/jundot/omlx/issues/1072)); realtime transcription in v0.7.1 ([releases](https://github.com/jundot/omlx/releases)) |
| Text-to-speech | Probably; a v0.7.2 fix mentions TTS settings ([releases](https://github.com/jundot/omlx/releases)) |
| Image generation | Unclear; the request was closed in a cleanup, not rejected ([#477](https://github.com/jundot/omlx/issues/477)), and draft PRs add image pipelines |
| Video, music | No sign of plans |

**For me:** Whisper on oMLX is probably no faster, because it runs through the same mlx-audio library I'd call directly. The gain would be one server for everything. That's an inference, not a benchmark, so I'm waiting before trying it.

**Open**

- Is Whisper through oMLX faster or slower than calling mlx-audio directly?
- Is my Whisper slowness about long files or live transcription latency?
- Will the image-generation PRs be merged?
