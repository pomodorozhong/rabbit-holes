---
name: ai-research-report
description: Create or update a sourced AI research report in this repository. Use for video roundups, local-model feasibility reports, comparisons, modality surveys, and technical AI topic guides. Not for quick factual Q&A or code-only tasks.
---

# AI research reports for this repository

Produce a complete, reviewable report that follows the relevant topic's existing conventions. Use a report shape suited to the research question; do not force every subject into a local-model runnability table.

## Workflow

1. Inspect repository guidance, the target topic directory, its README/index, and the closest existing report. Use the report-mode guide in [references/report-modes.md](references/report-modes.md) to choose the structure. Use [assets/report-template.md](assets/report-template.md) only when no closer local format exists.
2. Research current or uncertain claims from primary sources: official project pages, papers, documentation, release notes, repositories, standards, and model cards. Cite important factual claims inline and include a `## Sources` section with direct links. Date-stamp facts that can change. Distinguish source claims, independent evidence, and your own inference.
3. For a video roundup, inspect the video's official title, chapters, timestamps, and description. Account for every chapter in the report. Find a primary source for each substantive item. If a transcript or chapter list is unavailable, state the limitation and do not invent transcript-only details.
4. For local-model feasibility, read `topics/local_model_reports/memory-budget.md` and use its hardware target and constraints. Evaluate the whole inference path: complete weights and auxiliary components, actual memory needs, runtime and accelerator support, context, license, and setup maturity. Distinguish total checkpoint size from active parameters and publisher measurements from tests run on this Mac.
5. Write the report in the topic's established location and naming style. Update the relevant README/index with a correct relative link and concise description. Keep unrelated files and work out of scope.
6. Review the final diff. Confirm the report has a `## Sources` section; links support the claims they accompany; no template placeholders remain; all required video chapters are covered; units, dates, versions, and uncertainty are clear; the recommendations follow from the evidence; and the index link resolves. Use `git diff --check` for Markdown changes.

## Pull request preference

The user has asked for an open PR by default whenever they request a report as a repository deliverable in this project. This standing preference authorizes the report-specific commit, push, and create/update PR steps. Follow the available pull-request skill, inspect the branch and any existing PR first, preserve unrelated work, and leave the PR open without merging. Honor a later request to omit the PR. If the repository has no usable remote or pushing is blocked, finish the report and clearly report that gate.

## Delivery

Return links to the report and PR, state the checks actually run, and mention any source or CI limitation that still needs attention. Do not claim that a report was locally benchmarked unless it was run on the stated hardware.
