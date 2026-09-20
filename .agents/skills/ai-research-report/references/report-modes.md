# Report modes

Choose a mode from the user's question and source material. A report may combine modes, but keep its primary question visible and use only the sections that help answer it. First reuse the structure of a relevant report already in the topic directory.

## Video or news roundup

- Inventory each substantive official chapter or listed item in source order. Account for generic intro/outro chapters in the surrounding prose or method note rather than creating empty inventory rows.
- Give timestamps a dedicated `Video` or `Timestamp` column containing only the linked time. Never combine a timestamp with the model/item name, a source citation, or descriptive text.
- Keep the other inventory dimensions separate: item name, kind, weights/access, verdict, and evidence-based reality. For a local-runnability roundup, prefer `Model / item | Video | Kind | Weights / access | Fits <target>? | Local reality` unless an established local report has an equally clear schema.
- Distinguish releases with weights, hosted products, research results, infrastructure stories, agent/client software, and non-model news. If one chapter names multiple systems, identify and source each component rather than treating the whole chapter as one undifferentiated release.
- Deep-dive only on the most relevant candidates; still account for every chapter in the inventory.
- In `## Sources`, list the video and direct primary sources for every substantive item. Add a method note if the transcript, captions, chapters, or cutoff date constrain coverage.

### Video roundup with local-model feasibility

When the video roundup is primarily a local-model decision report:

1. Start the TL;DR with a compact verdict table. Useful buckets are comfortable local use, tight/experimental, open weights that do not fit as published, hosted products, and research/infrastructure/non-model stories. Follow it with a short interpretation of the best candidates and the main trap behind misleading size or access claims.
2. Use a consistent verdict scale:
   - `✅` for a published or straightforward local path that fits the stated machine and task.
   - `⚠️` for a size-plausible path that needs an unverified conversion, custom runtime, short context, missing benchmark, or other material condition. State that condition in the verdict or local-reality cell.
   - `❌` when the complete published stack exceeds the practical budget, depends on incompatible hardware, or is hosted-only.
   - `n/a` when the item is not a local checkpoint. A local client or harness may receive a qualified verdict such as `⚠️ harness only`.
3. Support each verdict with the most decision-relevant concrete evidence available: full artifact/component sizes, precision or quantization, measured or estimated memory, context, supported runtime, accelerator, platform install path, license/access, and the hardware used for any published benchmark. Label arithmetic estimates and missing measurements.
4. Evaluate both the release as published and any realistic local route. Do not mark a model impossible merely because its first-party example uses CUDA when its complete size and architecture make an Apple conversion plausible; rate that route `⚠️` and say what remains unverified. Do not call an adapter, active-parameter count, or language-only shard a complete fit when required base weights, auxiliary encoders, projectors, cache, or runtime overhead change the result.
5. Deep-dive the few candidates worth acting on. Use compact key-value tables where useful, covering the job, complete model/artifact size, license, Mac/runtime path, target-machine fit, context or memory limit, and scope. Then group near-misses by the actual limiting factor and end with suggested actions mapped to user goals.

## Local-model feasibility report

- State the target machine, software/runtime assumptions, and evaluation date.
- Separate model/weight size, auxiliary components, peak working memory, context use, supported runtimes, and accelerator requirements.
- Compare each candidate against the project's memory-budget note. Explain whether a verdict is measured, publisher-reported, inferred from artifact size, or blocked by missing platform support.
- Prefer an explicit publisher memory table or measured artifact metadata over parameter-count arithmetic. When only arithmetic is possible, show the assumption and leave room for scales, cache, activations, runtime, and the operating system.
- End with practical candidates, near-misses, and next steps appropriate to the requested scope.

## Model deep dive or comparison

- State the decision question and comparison baseline before comparing versions or alternatives.
- Compare like with like where possible: architecture, capabilities, artifact formats, licenses, supported runtimes, resource needs, and benchmark setup.
- Label incomparable vendor results and unsupported deployment claims. Include a recommendation tied to the user's stated machine and use case when those are in scope.

## Modality or product survey

- Organize by user task or capability, not by a generic model list.
- Compare relevant dimensions such as output type/length, quality, latency, streaming, access, license, runtime, and resource requirements.
- Keep hosted services separate from downloadable local weights and note when a small headline model is only one component of a larger pipeline.

## Technical AI topic guide

- Teach concepts in a useful order: define terms, explain mechanisms, compare approaches, describe tradeoffs, and ground them in representative systems or examples.
- Cite primary papers, standards, official documentation, and implementations where applicable. Make the limits of each example explicit.
- Use an explanatory guide structure rather than a model-fit matrix unless local deployment is part of the question.

## Other AI research question

Inspect the repository's nearest topical material, identify the research question and audience, and build a compact structure around the evidence needed to answer it. Do not add comparison tables, recommendations, or hardware sections just to fill a template. Keep `## Sources` and include method/caveats when source selection or evidence limits affect the conclusion.
