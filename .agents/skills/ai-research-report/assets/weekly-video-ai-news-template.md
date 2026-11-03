<!--
AUTHORING NOTES — remove this comment from a finished report.

Use for topics/local_model_reports/report-YYYY-MM-DD-video-ai-news.md.
Keep the main report a five-minute read; move the complete chapter inventory, component budgets, runtime evidence, and detailed source notes into the appendix.
Inspect the official video title, publication date, description, and chapters.
Account for every official chapter in source order, including hosted services, research, tools, hardware, editorial transitions, and items that cannot run locally.
If official chapters are unavailable, identify how the inventory was constructed and disclose incomplete coverage. Never invent timestamps or transcript claims.
Release recency and Reddit attention are not eligibility filters for this mode: the source video defines coverage. Verify its claims against primary sources.
Highlight only worthwhile local candidates; do not fill a quota or invent a winner.
Choose card-section categories from notable findings; do not require fixed modalities.
Use short task/category names for headings, such as "Speech recognition and transcription" or "Research synthesis". Put recommendations and caveats in the takeaway text below the heading.
Best for emoji: 🖼️ image output/editing, 📹 video output, 💬 text-output LLMs(including multimodal input), ⚖️ decisions, 🎵 music, 🗣️ speech recognition/transcription, ❓ other/new model types.
Mac fit emoji: ✅ Comfortable, ⚠️ Constrained, ⚠️ Experimental, ❌ Outside budget.
Base Mac fit on publisher memory tables or measured artifact metadata, not parameter-count arithmetic. If arithmetic is all you have, show the assumption and leave headroom for scales, cache, activations, runtime, and macOS.
In the chapter inventory, ❌ Hosted means no verified local weights; use — N/A for non-model stories, and ⚠️ Unverified when evidence cannot establish fit.
Distinguish a local application/harness from its remote model dependencies.
Keep text labels with emojis. API access from a Mac is not local inference.
Cite important claims near their evidence. Use exact checkpoint/runtime versions when known; verify the entire pipeline and label measured versus inferred fit.
Only include executable setup commands when checked against the chosen runtime; otherwise link to documentation and describe the suggested starting configuration.
Replace all {placeholders}; remove unused drafting sections and comments.
Relative links below are relative to the output report directory, not this asset.
-->

# Weekly AI video report — {YYYY-MM-DD}

**As of:** {YYYY-MM-DD}\
**Source video:** [{Official title}]({Video URL}) by {Channel} · {Publication date} · {Duration}\
**Target:** M2 MacBook Pro, 16 GB unified memory · [Memory budget](./memory-budget.md)\
**Local testing:** {Not performed / configurations actually tested}\
**Coverage:** {All N official chapters / inventory basis and known gaps}

## Worth trying on your Mac

{Two sentences: what this week's video means for this machine and the best starting point. If no candidate qualifies, say so and omit the shortlist table.}

| Model / configuration | Best for | Why it matters this week | Mac fit |
| --- | --- | --- | --- |
| [{Exact candidate}](#candidate-slug) | {Task emoji} {Task} | {Brief reason} | {Fit emoji} {Fit label} |

**Mac fit:** ✅ Comfortable = credible path with headroom; ⚠️ Constrained = specific limits required; ⚠️ Experimental = important verification gaps; ❌ Outside budget = unsuitable for local inference on this machine. Evidence basis is recorded in the appendix.

## {Task or category}

{One-sentence takeaway. Repeat this section only for findings worth highlighting.}

### {Candidate name}

**Mac fit:** {Emoji and label}

**Why consider it:** {Useful capability and the substantive development covered in the video.}\
**Start with:** {Exact variant, runtime, and initial context/output limits, or the verification required before installation.}\
**Main limitation:** {The constraint most likely to affect the user's decision.}

[Video chapter]({Timestamped video URL}) · [Model/runtime]({Primary URL}) · [Deployment details](#candidate-slug-deployment)

## Other developments worth knowing

{A few brief bullets about notable larger-machine releases, hosted products,
research, or tools. State their relevance and access limits. Omit when unnecessary;
every remaining chapter is still covered in the appendix.}

- **{Item}:** {What changed and why it matters; local/hosted/research distinction.} [Source]({Primary URL})

## Technical appendix

### Complete video chapter inventory

Every official chapter appears below in source order. Verdicts concern local inference on this Mac. Hosted access and non-model stories are labeled separately.

| Chapter | Item / primary source | Type | Local verdict / main reason |
| --- | --- | --- | --- |
| [{MM:SS}]({Timestamped video URL}) | [{Item}]({Primary URL}) | {Open weights / Hosted / Tool / Research / Hardware / Editorial} | {Emoji + label; short reason} |

<!-- Repeat for every chapter. If a chapter contains multiple substantive items,
identify all of them within its entry or use clearly labeled additional rows.
For editorial/unverified chapters, keep the row and explain unavailable evidence;
do not invent a primary artifact. Put long explanations in item notes below.
-->

### {Candidate name} deployment

**Configuration:** {Publisher/model ID, checkpoint revision, quantization, runtime/version, OS requirements}\
**Fit evidence:** {Measured on this Mac / publisher measurement with hardware and settings / inference / unverified}

| Component | Artifact size | Loading / residency notes |
| --- | --- | --- |
| Main model | {GB} | {Total weights versus active parameters; conversion overhead} |
| Encoder / projector / planner | {GB or not required} | {Required/optional; simultaneous or sequential residency} |
| Decoder / VAE / vocoder | {GB or not required} | {Decode peaks, chunking/tiling, output limits} |
| Complete required weights | {GB or unknown} | {Configuration-specific total; not peak RAM} |

**Working memory:** {Peak and measurement scope/settings/hardware; or explicitly unknown. Cover encoding, loading/conversion, inference, and decoding.}\
**Starting limits:** {Context, concurrency, resolution, frames, duration, batch size as applicable}\
**Runtime support:** {Confirmed CPU/Metal/MLX/MPS path; unsupported features and setup maturity}\
**License:** {Weights and runtime separately, with direct links}\
**Unresolved:** {Missing check or measurement that could change the verdict}

{Brief quality/performance evidence. Attribute video claims, publisher benchmarks,
community anecdotes, and own measurements separately. Do not present another
machine's timings or a single-stage memory peak as a complete M2 benchmark.}

[Card]({URL}) · [Artifacts]({URL}) · [Runtime]({URL}) · [Measurement]({URL})

<!-- Repeat deployment entries for recommended candidates and important near-misses. -->

### Other chapter notes

{Group only the items needing more explanation. Explain hidden dependencies,
CUDA-only runtimes, absent local weights, unclear licenses, or research/hardware
scope. Cross-reference the chapter inventory; avoid repeating it in prose.}

### Method and verification limits

- **Video evidence:** {Official chapters/description inspected; transcript availability and limitations.}
- **Primary-source checks:** {Model cards, artifacts, runtime docs/source, and evaluation date.}
- **Memory interpretation:** {Shared unified-memory budget, GB/GiB units, complete pipeline, and evidence basis.}
- **Coverage check:** {Official chapter count versus inventory coverage; unresolved items.}
- **Local verification:** {Checks actually performed; no benchmark claim unless measured on the target Mac.}

## Sources

- **Video:** [{Official title}]({Video URL}) — {Channel, publication date}; timestamps appear in the inventory.
- **{Item/category}:** [Publisher]({URL}) · [Model/artifacts]({URL}) · [Runtime/evidence]({URL})

<!-- Include a direct primary source for every substantive item where available.
Record missing sources in the relevant inventory row and method notes.
-->
