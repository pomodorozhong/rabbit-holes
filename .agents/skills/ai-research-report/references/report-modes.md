# Report modes

Choose a mode from the user's question and source material. A report may combine modes, but keep its primary question visible and use only the sections that help answer it. First reuse the structure of a relevant report already in the topic directory.

## Video or news roundup

- Inventory each official chapter or listed item in source order; include timestamps when available.
- In a compact table, distinguish releases with weights, hosted products, research results, infrastructure stories, and non-model news.
- Deep-dive only on the most relevant candidates; still account for every chapter in the inventory.
- In `## Sources`, list the video and direct primary sources for every substantive item. Add a method note if the transcript, captions, chapters, or cutoff date constrain coverage.

## Local-model feasibility report

- State the target machine, software/runtime assumptions, and evaluation date.
- Separate model/weight size, auxiliary components, peak working memory, context use, supported runtimes, and accelerator requirements.
- Compare each candidate against the project's memory-budget note. Explain whether a verdict is measured, publisher-reported, inferred from artifact size, or blocked by missing platform support.
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
