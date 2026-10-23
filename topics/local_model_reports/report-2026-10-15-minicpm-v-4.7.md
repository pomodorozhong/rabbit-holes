# MiniCPM-V 4.7 on a 16 GB M2 Mac

**As of:** 2026-10-15  \
**Source video:** [This 35B Model Runs on an iPhone in 3GB? MiniCPM V 4.7 Tested](https://youtu.be/JYTXQ7oFTLA) by RepoChad · published 2026-10-13 · 18:36  \
**Question:** Is MiniCPM-V 4.7 worth trying locally, and how does it compare with Gemma 4 E2B, E4B, and 12B?  \
**Target:** M2 MacBook Pro, 16 GB unified memory · [Memory budget](./memory-budget.md)  \
**Scope:** Focused model and deployment review, not a weekly AI-news roundup. The video’s 11 custom tests, local artifacts, and the Gemma comparison are the useful evidence here.  \
**Local testing:** No model was run on the target M2. An independent M4 measurement is used only as secondary evidence.

## Bottom line

Start with **MiniCPM-V 4.7 1B Q4_K_M** if the job is local image, document, chart, screenshot, or short-video understanding. The language model plus projector is about **1.6–1.8 GB on disk**, so it has substantial room within this Mac’s estimated 8–11 GB working budget. That is an artifact-based fit judgment, not an M2 benchmark.

The 1B model is useful but not reliable enough to be the sole source for numbers. In the video’s custom scorecard it handled receipts, tables, charts, geometry, dashboards, and much of the short-video work, while tiny text, code screenshots, gauges, and counting exposed silent errors. Use **4x visual compression** for detail and **16x** for throughput; validate extracted values either way.

The **35B-A3B** model is a different category. Its standard Q4_K_M file is about **21.2 GB** before the projector. OpenBMB’s LES split streams experts from storage and makes an Apple-device experiment plausible, but the split is about **16.6 GB on disk** and has no M2 result in the evidence checked here. Do not treat “about 3B active parameters” as “a 3B model.”

For a general local assistant, **Gemma 4 E4B** is the balanced smaller generalist and **Gemma 4 12B Unified** is the strongest general baseline in Google’s table. MiniCPM-V 4.7 1B remains the more focused choice when visual extraction and a small footprint matter more than audio, coding, and broad reasoning.

## What the video actually shows

The video compares MiniCPM-V 4.7 1B, MiniCPM-V 4.6, MiniCPM-V 4.7 35B-A3B, and a hosted Qwen comparator across 11 custom tasks. The result is useful practical evidence, but it is not a reproducible benchmark: the task inputs and scoring code are not released.

| Test area | Observation from the video | Local implication |
| --- | --- | --- |
| Receipts, tables, charts, geometry, and dashboards | The 1B model was broadly useful and scored around 8/11 overall in the creator’s scorecard | A credible first local vision assistant |
| Tiny text, code screenshots, gauges, and dot counting | Plausible-looking errors included wrong characters, an incorrect PSI value, and 40 dots instead of 37 | Add OCR, image processing, or deterministic validation for decisions |
| 4x versus 16x visual compression | 4x preserves more detail; 16x reduces visual-token cost and was faster in the video | This is a quality/latency setting, not a way to fit a larger checkpoint |
| 35B-A3B on difficult visual tasks | The 35B path was strongest in the video’s harder reasoning examples | Quality evidence for an experiment, not proof of M2 runnability |

Relevant video chapters: [11 custom tests](https://www.youtube.com/watch?v=JYTXQ7oFTLA&t=159s), [code screenshots](https://www.youtube.com/watch?v=JYTXQ7oFTLA&t=396s), [4x versus 16x](https://www.youtube.com/watch?v=JYTXQ7oFTLA&t=633s), and [35B LES deployment](https://www.youtube.com/watch?v=JYTXQ7oFTLA&t=890s).

## Which MiniCPM-V path fits the Mac?

| Path | Relevant footprint and support | Verdict |
| --- | --- | --- |
| **1B Q4_K_M + projector** | The checked artifacts are about 672 MB for the Q4_K_M language model, 901 MB for the 4x projector, or 1.11 GB for the f16 projector. Standard llama.cpp documents a macOS path. | **Start here.** The complete bundle is small enough to leave room for the runtime, cache, and other Mac applications, but peak memory still needs an M2 measurement. |
| **35B-A3B standard GGUF** | About 21.2 GB for Q4_K_M, or about 15.5 GB for the smaller checked mix_q3gud_im file, before multimodal overhead. | **Do not start here.** The file itself is outside the normal working budget. |
| **35B-A3B LES split** | OpenBMB’s split bundle is about 16.6 GB on storage, with expert weights streamed from the internal drive. The official app recommends at least 12 GB of RAM; the checked measurements are on M4 Apple hardware. | **Experiment only.** It may reduce resident-memory pressure, but storage, latency, and M2 stability remain unverified. |

The 1B recommendation is based on artifact size and documented runtime support, not a local execution result. The 35B recommendation is even more conditional: an M4 iPad Pro report gives 17.39 tokens/s, while an independent M4 Mac mini report gives roughly 5.8–6.0 tokens/s and 4.6 GB peak RSS. Neither is an M2 measurement.

## MiniCPM-V 4.7 versus Gemma 4

The video does not test Gemma. The comparison below puts the video’s MiniCPM observations beside Google’s instruction-tuned Gemma 4 model-card results. These are **not a shared benchmark**: MiniCPM’s row is a creator-made 11-task scorecard, while the Gemma rows are standardized results from a different evaluation set. OpenBMB’s [4.7 documentation](https://github.com/OpenBMB/MiniCPM-V/blob/main/docs/minicpm_v4dot7_en.md) includes Gemma baseline rows for selected pairings, but not a clean E2B/E4B/12B head-to-head on the video’s tasks.

| Model | Evidence / published anchors | Best fit on this Mac |
| --- | --- | --- |
| **MiniCPM-V 4.7 1B** | About 8/11 in the video’s custom tasks; useful on documents, charts, dashboards, and short video, but weak on exact characters, gauges, and counting | Small visual sidecar when image and video understanding matter most |
| **MiniCPM-V 4.7 35B-A3B** | Strongest MiniCPM option in the video’s harder visual tasks; 35B total parameters with about 3B active per token | High-quality visual experiment only; standard files do not fit the normal budget |
| **Gemma 4 E2B** | MMLU Pro 60.0 · MMMU Pro 44.2 · MATH-Vision 52.4 · LiveCodeBench v6 44.0 | Smallest general multimodal/audio option; choose it when general assistant behavior matters more than MiniCPM’s visual specialization |
| **Gemma 4 E4B** | MMLU Pro 69.4 · MMMU Pro 52.6 · MATH-Vision 59.5 · LiveCodeBench v6 52.0 | The balanced generalist: stronger reasoning and coding than E2B, with a smaller footprint than 12B |
| **Gemma 4 12B Unified** | MMLU Pro 77.2 · MMMU Pro 69.1 · MATH-Vision 79.7 · LiveCodeBench v6 72.0; Google lists a 256K context | Strongest general baseline for chat, coding, reasoning, audio, and multimodal work if its runtime footprint is acceptable |

Gemma’s scores come from [Google’s Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4); they do not establish that Gemma will beat MiniCPM-V on the video’s receipts, gauges, or short videos. The practical division is simpler:

- Choose **MiniCPM-V 4.7 1B** for a small, vision-first local assistant.
- Choose **Gemma 4 E2B** when the smallest broad multimodal/audio model is the priority.
- Choose **Gemma 4 E4B** when you want the best balance of general capability and footprint.
- Choose **Gemma 4 12B Unified** when general reasoning and coding matter more than memory headroom.
- Consider **MiniCPM-V 4.7 35B-A3B** only as a storage-streaming experiment.

## Decision and limits

For this M2, the sensible order is:

1. Try MiniCPM-V 4.7 1B Q4_K_M with 4x compression and a short context.
2. Switch to 16x when throughput matters more than tiny visual details.
3. Put deterministic checks around every extracted number, identifier, total, or count.
4. Use Gemma 4 E4B or 12B instead if the primary need is general chat, coding, reasoning, or audio.
5. Investigate the 35B LES split only if expert streaming itself is the goal.

The important uncertainties are narrow: no target-M2 memory or speed measurement exists; the video’s scorecard is not independently reproducible; and the M4 LES results do not establish M2 behavior. The report therefore recommends a first test, not a claim that any path has already been validated on this Mac.

## Sources

- **Video:** [RepoChad — MiniCPM-V 4.7 test](https://youtu.be/JYTXQ7oFTLA) — title, description, selected chapters, and transcript panel inspected on 2026-10-15.
- **MiniCPM-V 4.7:** [Official documentation](https://github.com/OpenBMB/MiniCPM-V/blob/main/docs/minicpm_v4dot7_en.md) · [1B model card](https://huggingface.co/openbmb/MiniCPM-V-4.7-1B) · [1B GGUF files](https://huggingface.co/openbmb/MiniCPM-V-4.7-1B-gguf) · [llama.cpp guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal/minicpmv4.7.md).
- **35B deployment:** [MiniCPM-V Apps](https://github.com/OpenBMB/MiniCPM-V-Apps) · [LES documentation](https://github.com/OpenBMB/llama.cpp-omni/blob/main/docs/les/lookahead-expert-scheduling.md) · [Standard 35B GGUF files](https://huggingface.co/openbmb/MiniCPM-V-4.7-35B-A3B-gguf/tree/main) · [Split artifacts](https://huggingface.co/tc-mb/MiniCPM-V-Apps-gguf/tree/main/MiniCPM-V-4.7-35B-A3B).
- **Independent Apple Silicon evidence:** [M4 Mac mini test](https://lilting.ch/en/articles/minicpm-v-4-7-mac-mini).
- **Gemma 4:** [Google model card](https://ai.google.dev/gemma/docs/core/model_card_4) · [Deployment guide](https://ai.google.dev/gemma/docs/get_started).
