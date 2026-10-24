# Local pipeline sources

[Topic overview](README.md) · [Feature catalogue](feature-catalogue.md) · [Product coverage](product-coverage.md)

These notes describe the paths used by Meetily, HushScribe, VOA, and Tacet to turn meeting audio into text and notes. The project documentation and selected source files were inspected on **2026-10-06**, Asia/Taipei, at the revisions recorded below. The configuration review below was completed on **2026-10-08**, Asia/Taipei, at the same project revisions. It selected a setup for a user-run trial; it provides no measured quality or runtime-memory result on the M2 Pro / 16 GB Mac.

## Candidate for the recording trial

The review selected a **HushScribe source build with Whisper Large v3 through WhisperKit, language detection enabled, and FluidAudio’s offline Community-1 diarizer**, for the user’s **macOS 26.6.2 (25G83), Chinese + English** recording trial. This meets the documented macOS 26+ requirement. It has an existing file-import path that transcribes a saved recording, separates speakers afterward, and offers a naming prompt. Whisper covers languages outside Parakeet v3’s 25 European languages, including Chinese. The stock wrapper needs the decoding override documented below before this Chinese/English trial; model language coverage alone does not configure the app. Chinese/English language switching is an explicit trial check. Summary generation was left unused for the first trial. This was a source-based selection; loading and speaker labels were left for the user’s trial to establish. [File-import and diarization code][h-engine], [Whisper model card][whisper-card]

The exact Whisper Core ML folder is about **3.09 GB**, and the offline diarizer’s required artifacts total **21.60 MB**. These fit below the repository’s approximate 8 GB artifact-size preference, but file size does not establish peak memory use: the app, audio buffers, Core ML working data, and resident transcription model also consume unified memory. The [memory-budget note](../local_model_reports/memory-budget.md) is a planning heuristic, not a measurement on this setup.

Tacet provides a different live-capture path; Meetily and VOA lack a confirmed speaker-separation path for this trial. The configuration sections explain those differences.

**Trial outcome:** the selected setup ran on the target Mac and transcribed the recording reasonably well, but its Community-1 speaker separation merged three voices into one label. Whisper Large v3 with Chinese forced, plus FluidAudio’s Sortformer diarizer, separated them; the [topic overview](README.md#what-the-recording-trial-found) summarizes the result.

## Observed pipeline patterns

### Meetily: local transcription with a choice of summary provider

**Inspected revision:** `a2cb62e827da7ef59f65064c97233efb2313878e`.

Meetily captures microphone and system audio, transcribes with local Whisper or Parakeet, and stores meeting data in a database. Its architecture separates the audio, transcription, database, and summary engines. The summary provider determines where that later processing runs: Ollama is a local option, while other provider configurations use APIs. [README](https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/README.md), [architecture](https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/docs/architecture.md)

The configuration review follows that separation: identify the transcription model, then check the summary provider and its settings. Choosing local transcription alone does not settle where the meeting text goes for summaries.

### HushScribe: speaker labels after the session

**Inspected revision:** `51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92`.

HushScribe keeps microphone and system audio as separate streams. Voice activity detection, which separates speech from silence, feeds the selected local speech-recognition model. Speaker separation runs after the session; a naming step and Markdown output follow. Summaries are requested from a saved transcript using a local MLX model or the separate Apple NaturalLanguage summarizer. [README](https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/README.md), [architecture](https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/ARCHITECTURE.md)

Final speaker-labelled text and live speaker-labelled text are different results here. That timing can suit a recording trial even when it would not satisfy a need for live attribution. The inspected documentation requires macOS 26 or later; the user’s confirmed macOS 26.6.2 meets this prerequisite.

### VOA: a saved transcript followed by structured notes

**Inspected revision:** `d2a9a3af2cc76f8f0a674c017dd439bc8609ab49`.

VOA sends detected speech segments to local Whisper and saves the transcript. Summary generation runs on request. Its README describes Qwen2.5-1.5B through `node-llama-cpp` as the default local summary option, with LM Studio or Ollama as alternatives. For long transcripts, the extraction code processes chunks and updates the summary with each new chunk. [README](https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/README.md), [structured extraction](https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/pipeline/structured-summarizer.ts)

The output format affects how the app can use the notes. VOA's action items have `text` and `done` fields; they do not have separate owner and deadline fields. A name or date in task text is therefore different from a field another application can read directly. The same source asks for English output when the input is non-English. Those choices matter for **MN-10** and for the desired note language, even if transcription itself is accurate. [Extraction schema and prompt](https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/pipeline/structured-summarizer.ts)

### Tacet: speaker processing alongside transcription

**Inspected revision:** `d976b40c0c63d5ab7f1121e5e48606ffb475fa2b`.

Tacet captures separate microphone and system audio streams. Silero voice activity detection passes speech to Whisper and to speaker processing based on voice embeddings—numeric descriptions used to compare voices. The resulting labelled transcript feeds analysis during the meeting, a final summary, and local Markdown and vault storage. Ollama is the local language-model option; cloud providers receive selected text, with optional screen analysis handled separately. [README](https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/README.md), [audio flow](https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/docs/audio-pipeline-flow.md)

The configuration review follows both the speech and speaker paths, then checks the language-model provider. A stable voice label still needs confirmed identity information before it becomes a person's name. Local audio processing does not by itself establish local processing for the later notes.

## What these patterns tell us

The projects expose separate choices for transcription, speaker handling, and summaries. They also schedule the work differently: during the call, afterward, or on request. These observations explain why the model and settings need to be recorded with the result. The same general feature can become available at a different time or depend on a different processing provider.

The configuration review below records the main model paths and the settings that affect the first trial. The user then tried the selected configuration with a recording; the [topic overview](README.md#what-the-recording-trial-found) records the outcome.

The catalogue includes more than the recording trial checks. The observations above can explain dependencies and missing application work, but they do not establish full feature coverage or summary quality.

## Confirmed models, runtimes, and settings

The inspection follows the code used to select and load models, rather than treating every model mentioned in a README as an active default. **GB and MB below are decimal**; exact byte counts and model snapshots appear in the artifact record. A project commit pins application code, but it does not pin a model downloaded from a moving `main` branch or an Ollama tag. Record the actual model snapshot or file hash during the later trial.

### HushScribe: the selected file-oriented setup

**Application source:** `51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92`. The cask names release **3.5.0**, but a downloaded release must be recorded separately; source inspection does not establish that its binary matches this commit. The Swift package requires macOS 26, Apple Silicon, and Xcode 26.3+ for a source build. The cask’s lower Sequoia requirement conflicts with the README and package, so use **26+** as the planning requirement. [Package][h-package], [architecture][h-architecture], [cask][h-cask]

| Step | Confirmed model and runtime | Download and relevant settings |
| --- | --- | --- |
| Default transcription | Parakeet-TDT **0.6B v3**, `FluidInference/parakeet-tdt-0.6b-v3-coreml`; FluidAudio pinned at `ea500621819cadc46d6212af44624f2b45ab3240`; Core ML | Required split preprocessor, encoder, decoder, joint, and vocabulary: **483.10 MB**. Code loads `.v3`; English and 24 other European languages, not Chinese. |
| Trial transcription | `argmaxinc/whisperkit-coreml/openai_whisper-large-v3`; WhisperKit **0.18.0** | Folder **3.090 GB**, rather than the app’s ~1.5 GB label. The wrapper calls `transcribe(audioArray:)` without custom decoding options. WhisperKit defaults include temperature 0, fallback increments of 0.2 up to five times, `usePrefillPrompt=true`, and `detectLanguage=false`; missing language then prefills English. The planned trial must enable detection. |
| Smaller transcription option | Same repository, `openai_whisper-base`; WhisperKit **0.18.0** | Folder **146.72 MB**. Multilingual model rather than `.en`; a fallback only if the chosen model cannot load or its output identifies a reason to change it. |
| Built-in transcription option | Apple `SFSpeechRecognizer`, selected locale | OS-managed assets, no independently identified model revision or download total. The implementation sets `requiresOnDeviceRecognition = true`. Availability depends on the locale and installed OS assets. |
| Speech detection | `FluidInference/silero-vad-coreml`, `silero-vad-unified-256ms-v6.0.0.mlmodelc`; FluidAudio/Core ML | **1.063 MB**. File transcription feeds 4,096 samples at 16 kHz per VAD call using FluidAudio’s default stream configuration. |
| Offline speaker separation | `FluidInference/speaker-diarization-coreml`, Community-1-derived `Segmentation`, `FBank`, `Embedding`, `PldaRho`, and `plda-parameters.json`; FluidAudio/Core ML | **21.60 MB** for the required set. HushScribe creates `OfflineDiarizerManager()` without overriding its defaults; it does not use the legacy online `wespeaker_v2` pair. |
| Default summary | Apple NaturalLanguage keyword/topic extraction | Built into macOS; no separately pinned weight file. It is a different operation from generative LLM summarization. |
| Optional local summaries | `mlx-community/Qwen3-0.6B-4bit`, `mlx-community/gemma-3-1b-it-qat-4bit`, or `mlx-community/gemma-4-e4b-it-4bit` | Weights **335.45 MB**, **732.58 MB**, and **5.147 GB** respectively, plus tokenizer/configuration files. The app labels them ~500 MB, ~600 MB, and ~800 MB; the last label materially understates the artifact. |

The table comes from [model settings][h-settings], [transcription engine][h-engine], [ASR wrapper][h-whisper], [WhisperKit defaults][wk-config], [summary model IDs][h-summary-models], FluidAudio’s [model catalogue][f-models] and [offline loader][f-offline-models], and the pinned model file records below. The Parakeet README link points to NVIDIA’s v2 model even though the label and loader select v3; use the code-selected v3 conversion when planning the download.

**Chinese/English configuration prerequisite:** HushScribe’s wrapper passes no `decodeOptions`. The pinned WhisperKit initializer sets `detectLanguage` to `!usePrefillPrompt`, so its default is false. Its text decoder substitutes `en` when the language is nil. The selected setup therefore needed a source build that passes `DecodingOptions(task: .transcribe, language: nil, detectLanguage: true)` to the wrapper’s transcription call; this lets the library detect language for each speech chunk and update its prefill. It does not prove accuracy within a chunk containing both languages. The stock DMG is not the selected mixed-language configuration unless its actual decoder settings are separately confirmed. The trial applied this change in a source build. With it, language detection ran per speech chunk and produced short invented lines in other languages; forcing Chinese worked better for this recording. [Defaults][wk-config], [decoder prefill][wk-decoder], [detection path][wk-task]

The locked summary stack is **mlx-swift 0.31.3**, **mlx-swift-lm `7e2b7107be52ffbfe488f3c7987d3f52c1858b4b`**, and **swift-transformers 1.1.9**. Summary defaults are temperature **0.3** and at most **4,000 output tokens**. A `ChatSession` receives the full transcript; these output-token settings do not cap input memory. No summary model needs to be loaded for this trial. [Dependency lock][h-lock], [summary engine][h-summary-engine]

Speaker separation runs after transcription. File import converts the source into a temporary **16 kHz mono Float32 WAV** for the diarizer and deletes that temporary file afterward. The offline defaults use 10-second segmentation windows, step ratio 0.2, a 1-second minimum embedding segment, batch size 32, clustering threshold 0.6, no fixed speaker count, and exclusive output segments. Thus overlapping voices are not represented as simultaneous final segments. The app can retain its transcription backend while diarization runs; the plan does not assume that models unload between steps. [File handling][h-engine], [offline defaults][f-offline-config]

Audio and text inference stay local in the inspected implementation. Network access is used to obtain model assets. Live capture separates microphone and system streams; a saved mixed recording instead relies on the file diarizer to distinguish all voices. The naming prompt lets the user assign known names, but an automatically generated label is not confirmed identity. The Apple Speech path explicitly requests on-device recognition; choose Whisper for the reproducible model-based trial. [Apple backend][h-apple], [project description][h-readme]

**Licenses:** HushScribe and WhisperKit use MIT licenses; FluidAudio uses Apache-2.0. The Core ML Whisper repository declares MIT, while the separately packaged Hugging Face `openai/whisper-large-v3` card declares Apache-2.0; retain the selected artifact’s own license rather than treating the packaging as interchangeable. Parakeet v3 is CC-BY-4.0. The offline diarizer’s notice covers its Community-1 components under scoped CC-BY-4.0 and asks for attribution to pyannote, WeSpeaker, BUT Speech@FIT, and Fluid Inference; it explicitly excludes legacy online artifacts from that confirmation. Qwen3 is Apache-2.0, Gemma conversions retain Gemma terms, and Apple frameworks/assets remain governed by Apple’s terms.

**Language boundaries:** Qwen3’s upstream card lists broad multilingual support; Gemma 3’s card reports multilingual support, with quality on this app’s 1B setup unmeasured; Gemma 4’s upstream card lists multilingual support. The app’s Apple NaturalLanguage path uses heuristic extraction rather than an independently versioned multilingual LLM. These are model capabilities, not verified note quality. [App license][h-license], [FluidAudio license][f-license], [diarizer notice][diar-notice], [Whisper card][whisper-card], [Qwen3 card][qwen3-card], [Gemma 3 card][gemma3-card], [Gemma 4 card][gemma4-card]

### Tacet: speaker embeddings during capture

**Application source:** `d976b40c0c63d5ab7f1121e5e48606ffb475fa2b`. The README requires macOS **13+**, Node **20+**, Python **3.11+**, and Xcode Command Line Tools for a source build. The Python requirements use lower bounds, including `mlx-whisper>=0.4.0`, `silero-vad>=5.0`, and `speechbrain>=1.1`; they do not lock an exact installed runtime. Record resolved versions if this alternative is used. [Requirements][t-requirements], [README][t-readme]

| Step | Confirmed model and runtime | Settings and timing |
| --- | --- | --- |
| Apple Silicon transcription | `mlx-community/whisper-large-v3-turbo`; mlx-whisper on Metal; **1.614 GB** weights | Auto architecture selection chooses MLX. `WHISPER_MLX_MODEL` overrides the preset. Language defaults to **`en`**, temperature 0, previous-text conditioning off, word timestamps off. |
| Other quality presets | Fast: `mlx-community/whisper-small.en-mlx`; accurate: `mlx-community/whisper-large-v3-mlx` | Fast is English-only. Balanced uses the turbo model. Exact download totals for these optional presets were not collected; they are not selected for the first trial. |
| Speech detection | Silero VAD via the installed `silero-vad` package | Speech threshold 0.5; minimum speech 500 ms; ending silence 800 ms; maximum speech chunk 20 seconds; 16 kHz input. The exact weight revision follows the installed package. |
| Speaker processing | `speechbrain/spkrec-ecapa-voxceleb`; SpeechBrain/PyTorch **CPU** | Snapshot **89.13 MB**, including 83.32 MB embedding weights. Similarity threshold 0.55; new-cluster minimum 2 seconds; matching minimum 1 second; reclustering distance 0.55. Online labels can be consolidated at meeting end. |
| Local notes option | Ollama, default tag `llama3.1` | The current default 8B tag is about **4.9 GB**, with a moving tag/version. Runs during live analysis and later summary/chat requests. The API payload defaults to temperature 0.7 and a 4,096-token output limit; context size depends on the server. |

Sources: [Whisper backend and presets][t-whisper], [VAD configuration][t-transcriber], [speaker embedder][t-speaker], [provider selection][t-llm], [Ollama model listing][ollama-llama], [provider payload][t-payload]. For non-English recordings, the default `en` must be changed. Whisper’s multilingual vocabulary does not cancel an app setting that forces English. ECAPA compares voices; its VoxCeleb-trained model card does not promise equal diarization quality across recording languages, short turns, or overlapping speech.

The app’s **default LLM provider is OpenRouter**, not Ollama. Its cloud providers receive transcript excerpts and chat messages; optional screen analysis sends frames to a vision provider. Selecting local Ollama at a localhost endpoint and disabling screen analysis is the documented local path. Downloads still use network access. Whisper/VAD and speaker processing are local; live GPU transcription and CPU embeddings can overlap in time and memory. [Provider configuration][t-config], [data flow][t-readme]

Tacet stores and restores text segments in saved sessions. That is not a raw-audio transcription-and-diarization input path; no saved-audio import route was confirmed in the inspected app. Its source requirements and live-capture focus make it a useful fallback to investigate, but less direct than HushScribe for the requested saved recording. [Session handling][t-main], [session restoration][t-engine]

**Licenses:** app MIT; Whisper and Silero MIT according to the app’s third-party notices; ECAPA model Apache-2.0; Llama 3.1 has Meta’s model terms rather than the app’s MIT license. The MLX conversion card does not state its own license, so its upstream license reference is an evidence limit to preserve. Meta lists eight supported Llama 3.1 languages (English, German, French, Italian, Portuguese, Hindi, Spanish, Thai); Chinese is outside that list, so the default summary model is not a documented Chinese option. No fixed server version, model digest, context length, or tested peak-memory figure is established here. [Third-party notices][t-notices], [ECAPA model card][ecapa-card], [Llama license][llama-license], [Llama language card][llama-card]

### Meetily: confirmed transcription and summaries, no selected speaker path

**Application source:** `a2cb62e827da7ef59f65064c97233efb2313878e`; the Tauri manifest reports **0.4.1**. Its lock records `whisper-rs 0.13.2`, `ort 2.0.0-rc.10`, and `llama-cpp-2 0.1.146`. macOS Whisper builds enable Metal/Core ML, while the inspected Parakeet ONNX code explicitly selects a CPU execution provider. This is different from HushScribe’s Core ML Parakeet implementation. [Manifest][m-cargo], [lock][m-lock], [Parakeet loader][m-parakeet-loader]

| Step | Confirmed configuration | Download and limits |
| --- | --- | --- |
| Default Whisper | `large-v3-turbo`, `ggerganov/whisper.cpp/ggml-large-v3-turbo.bin` | **1.625 GB**; language can be explicit, automatic, or automatic with translation to English. Decode settings include temperature 0.3 and hardware-adaptive beam size. |
| Parakeet choices | `parakeet-tdt-0.6b-v3-int8` or v2 int8; ONNX Runtime CPU | Code expects **670,619,706 bytes** for v3 and **661,331,448 bytes** for v2 across encoder, decoder/joint, preprocessor, and vocabulary. v3 uses the project’s model mirror; v2 URL pins `0bbb45a3365852604aef28b538a8f066f4ccaa85`. v3 supports 25 European languages; v2 is English-only. |
| Built-in notes | Qwen3.5 2B or 4B `Q4_K_M`; Gemma 3 4B `Q4_K_M` or 1B `Q8_0`; llama.cpp sidecar | Qwen files **1.281 GB / 2.741 GB**. Gemma catalogue estimates **2,374 / 1,019 MiB**; not independently remeasured. All catalogue contexts are 32,768 tokens. |
| Optional notes providers | Ollama or configured cloud API | The model and server version depend on the chosen provider; selecting a local transcription model does not select a local summary provider. |

Sources: [default and Whisper catalogue][m-config], [Whisper download/decoding][m-whisper], [Parakeet artifact catalogue][m-parakeet], [summary catalogue][m-summary]. The summary list’s first/default entry is Qwen3.5 2B, but the recommendation function chooses **4B at 14 GB system RAM or more**, so a 16 GB machine is recommended 4B. Qwen sampling is temperature 0.5, top-k 20, top-p 0.8, presence penalty 0.3, repetition penalty 1.05; Gemma sampling is temperature 1, top-k 64, top-p 0.95. A 32K context declaration is not evidence that the full combined setup fits 16 GB. [Recommendation][m-summary-commands]

Qwen3.5’s upstream card reports 201 languages and dialects, while Gemma 3’s card reports broad multilingual support. Those publisher claims do not establish Chinese/English note quality through Meetily’s prompts and runtime. [Qwen3.5 card][qwen35-card], [Gemma 3 card][gemma3-card]

The remaining Whisper downloads are explicitly selectable: tiny/base/small/medium/large-v3 are **77.69 / 147.95 / 487.60 / 1,533.76 / 3,095.03 MB**. Their quantized tiny/base/small q5_1 and medium/turbo/large q5_0 variants are **32.15 / 59.71 / 190.09 / 539.21 / 574.04 / 1,081.14 MB**. These are model-file sizes from the pinned Whisper.cpp artifact repository, not working-memory estimates.

No complete speaker-clustering path was confirmed in the current community capture/import pipeline. The README describes diarization as planned for the separate PRO codebase. Historical speaker-related fields do not establish an available voice-separation feature, so community Meetily is not the recording-trial candidate. Speech detection separates speech from silence, not one speaker from another. Live capture transcribes chunks; import/retranscription works on saved files; summaries are a later request. [Community/PRO description][m-readme], [current VAD][m-vad]

The inspected macOS capture code references Core Audio taps requiring **14.4+**, but the Tauri configuration does not declare a universal minimum OS. Source inspection therefore confirms a requirement for that capture backend, not compatibility of every release on older macOS. [Permissions][m-permissions], [bundle configuration][m-tauri]

**Licenses:** application MIT; Whisper.cpp model repository MIT; Parakeet conversions CC-BY-4.0; selected Qwen3.5 GGUF cards Apache-2.0; Gemma weights retain Gemma terms. The summary provider’s own model and service terms apply. The Rust wrapper licenses do not replace these model terms. [App license][m-license], [Qwen 2B artifact][qwen35-2], [Qwen 4B artifact][qwen35-4]

### VOA: small local models without voice separation

**Application source:** `d2a9a3af2cc76f8f0a674c017dd439bc8609ab49`; package version **1.0.0**. README requirements are macOS **13+** for dictation and **14+** for system-audio meeting capture. The npm lock resolves Electron **35.7.5**, Transformers.js `@xenova/transformers` **2.17.2**, its nested ONNX Runtime **1.14.0**, `node-llama-cpp` **3.19.1**, and `@ricky0123/vad-web` **0.0.30**. A separate top-level ONNX Runtime is 1.24.1; that is not the instance used by the Whisper child-process patch. [Package][v-package], [lock][v-lock], [Whisper child process][v-whisper]

| Step | Confirmed configuration | Download and settings |
| --- | --- | --- |
| First-run transcription | Onboarding selects `Xenova/whisper-base`; stored fallback default is `Xenova/whisper-tiny`; multilingual-off resolution appends `.en` | Unquantized English-only ONNX encoder + merged decoder: **291.03 MB** Base.en or **151.49 MB** Tiny.en, plus metadata/tokenizer. These differ from README’s ~142/~75 MB labels for other representations. |
| Optional transcription | Tiny/Base, with English-only variants available; Small/Medium disabled in the settings catalogue | Record the effective `.en` or multilingual ID and quantization switch. Saved defaults are English, multilingual off, quantized false. |
| Voice separation | No speaker model or clustering stage found in the inspected pipeline | It cannot satisfy the trial’s speaker requirement as inspected. Mentioning speakers in a summary prompt does not add diarization. |
| Structured notes | `Qwen/Qwen2.5-1.5B-Instruct-GGUF/qwen2.5-1.5b-instruct-q4_k_m.gguf` | **1,117,320,736 bytes** (**1.117 GB / 1.04 GiB**), with the same expected byte count in code. `node-llama-cpp` chooses its backend/context automatically; code does not set a fixed context size or sampling preset. |

Sources: [first-run selection][v-onboarding], [stored defaults][v-schema], [effective ID resolution][v-service], [model choices][v-constants], [Whisper options][v-whisper], [GGUF download][v-gguf], [LLM process][v-llama]. The unquantized ONNX totals count `encoder_model.onnx` and `decoder_model_merged.onnx`, the files used by the Transformers.js 2.x encoder-decoder path; selecting quantization or multilingual mode changes the files and total. These are metadata calculations, not a measured first-run transfer.

Whisper runs in an isolated utility process with greedy decoding, 30-second windows, 5-second stride, repetition penalty 1.3, and no-repeat-ngram size 3. The pinned child does not pass an explicit language argument in its inference call, so UI language defaults alone do not establish effective decoding behavior. Notes are generated on demand from transcript chunks; the structured extraction prompt requests English output for non-English input. Qwen2.5’s multilingual support does not override that prompt. LM Studio/Ollama are alternatives, whose configured endpoint determines the processing destination. [Whisper options][v-whisper], [structured extraction][v-structured]

**Licenses:** app MIT; Xenova ONNX cards declare Apache-2.0; the Qwen GGUF card declares Apache-2.0. Language support depends on the effective Whisper variant; Qwen’s card lists more than 29 languages, but this app asks for English notes. Model availability, native crash reports, and missing speaker processing make VOA unsuitable for this phase’s candidate selection. [App license][v-license], [Qwen GGUF card][qwen25-card]

## Artifact record and download accounting

Model metadata was read on **2026-10-08** without downloading weights. Each snapshot link below identifies the file tree used for the byte calculation and its model card. Count only the files used by the selected path, rather than all alternative encoders, precision variants, and conversion packages in a repository. Core ML totals include each selected compiled folder’s support files; tokenizer assets fetched from a separate repository, OS caches, and compilation growth are additional.

| Artifact repository and inspected snapshot | Counted files or scope | Size / license evidence |
| --- | --- | --- |
| [FluidInference/parakeet-tdt-0.6b-v3-coreml@7dd20fe6](https://huggingface.co/FluidInference/parakeet-tdt-0.6b-v3-coreml/tree/7dd20fe6b1797d35f5e3307e8b1732d9a178edfe) | Preprocessor, Encoder, Decoder, JointDecision compiled folders + vocabulary | 483.10 MB; CC-BY-4.0 |
| [FluidInference/silero-vad-coreml@b419383c](https://huggingface.co/FluidInference/silero-vad-coreml/tree/b419383c55c110e2c9271fa6ee0ea83d03c70d96) | v6.0.0 unified 256 ms compiled folder | 1.063 MB; MIT |
| [FluidInference/speaker-diarization-coreml@df2625ac](https://huggingface.co/FluidInference/speaker-diarization-coreml/tree/df2625ac79a7ac6b65ad868fee6d80f320da4232) | Community-1 offline set listed above | 21,599,417 bytes; scoped CC-BY-4.0 notice |
| [argmaxinc/whisperkit-coreml@0f63a780](https://huggingface.co/argmaxinc/whisperkit-coreml/tree/0f63a7800b00dd0226abd051b906c246e1907482) | openai_whisper-base / openai_whisper-large-v3 folders | 146,719,453 / 3,090,319,899 bytes; MIT |
| [mlx-community/Qwen3-0.6B-4bit@73e3e38d](https://huggingface.co/mlx-community/Qwen3-0.6B-4bit/tree/73e3e38d981303bc594367cd910ea6eb48349da8) | model.safetensors | 335,450,584 bytes; Apache-2.0 |
| [mlx-community/gemma-3-1b-it-qat-4bit@15fed4ea](https://huggingface.co/mlx-community/gemma-3-1b-it-qat-4bit/tree/15fed4eafb456c6fcb2a1165f19ac609670ed14b) | model.safetensors | 732,577,304 bytes; Gemma |
| [mlx-community/gemma-4-e4b-it-4bit@475b9088](https://huggingface.co/mlx-community/gemma-4-e4b-it-4bit/tree/475b9088d29754a3379866cf5aeb6b41acd313c2) | model.safetensors | 5,146,800,534 bytes; Gemma |
| [mlx-community/whisper-large-v3-turbo@a4aaeec0](https://huggingface.co/mlx-community/whisper-large-v3-turbo/tree/a4aaeec0636e6fef84abdcbe3544cb2bf7e9f6fb) | weights.safetensors | 1,613,977,612 bytes; card omits license |
| [speechbrain/spkrec-ecapa-voxceleb@0f99f2d0](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/tree/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286) | All snapshot files; embedding_model.ckpt dominates | 89,133,738 bytes; Apache-2.0 |
| [ggerganov/whisper.cpp@5359861c](https://huggingface.co/ggerganov/whisper.cpp/tree/5359861c739e955e79d9a303bcbc70fb988958b1) | Selected ggml files; not whole repository | File sizes listed above; MIT |
| [unsloth/Qwen3.5-2B-GGUF@f6d5376b](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/tree/f6d5376be1edb4d416d56da11e5397a961aca8ae) | Qwen3.5-2B-Q4_K_M.gguf | 1,280,835,840 bytes; Apache-2.0 |
| [unsloth/Qwen3.5-4B-GGUF@e87f1764](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/tree/e87f176479d0855a907a41277aca2f8ee7a09523) | Qwen3.5-4B-Q4_K_M.gguf | 2,740,937,888 bytes; Apache-2.0 |
| [Qwen/Qwen2.5-1.5B-Instruct-GGUF@91cad511](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/91cad51170dc346986eccefdc2dd33a9da36ead9) | qwen2.5-1.5b-instruct-q4_k_m.gguf | 1,117,320,736 bytes; Apache-2.0 |
| [Xenova/whisper-base.en@95bf40a5](https://huggingface.co/Xenova/whisper-base.en/tree/95bf40a508535962c6483ead40270b2e32267508) | Unquantized encoder + merged decoder | 291,033,798 bytes; Apache-2.0 |
| [Xenova/whisper-tiny.en@79fb389f](https://huggingface.co/Xenova/whisper-tiny.en/tree/79fb389fc764e7c395bd330e9531d9d32ada7049) | Unquantized encoder + merged decoder | 151,487,602 bytes; Apache-2.0 |

Meetily’s Parakeet totals instead come from its exact-byte catalogue because v3 downloads from a project mirror. The [separately inspected ONNX conversion card][parakeet-onnx] identifies CC-BY-4.0; byte counts do not attest that an independently hosted mirror file has identical contents. Ollama’s 4.9 GB Llama tag is a provider-reported size observed on this date, not a pinned digest.

## Method and limits

The review read the four projects’ pinned sources, dependency manifests/locks, the pinned FluidAudio and WhisperKit implementations, model cards, and Hugging Face file metadata. It traced model selection, downloads, decoding, file handling, speaker processing, and provider configuration. It downloaded **source code and metadata only**. No application dependencies, model weights, recording, or inference workload were installed or run.

Models fetched from moving branches and Python dependencies specified by lower bounds can change independently of app code. Publisher language coverage and artifact sizes establish inputs for a trial, not measured success, speed, memory pressure, or label reliability. The recording trial that followed measured one setup on one call; broader summary evaluation and the full 22-feature catalogue remained outside it.

## Sources

The links beside each finding are primary project sources. The artifact table pins the model snapshots used for size and license observations. These application revisions retain the original pipeline observations while the deeper configuration inspection is dated 2026-10-08.

- **HushScribe:** [README][h-readme], [package][h-package], [dependency lock][h-lock], [settings][h-settings], [transcription engine][h-engine], [Whisper wrapper][h-whisper], [Apple backend][h-apple], [summary IDs][h-summary-models], [summary engine][h-summary-engine], [architecture][h-architecture], [release cask][h-cask], [license][h-license].
- **FluidAudio / WhisperKit:** [model names][f-models], [offline loader][f-offline-models], [offline settings][f-offline-config], [FluidAudio license][f-license], [WhisperKit downloader][wk-download], [WhisperKit decode defaults][wk-config].
- **Meetily:** [README][m-readme], [Whisper defaults/catalogue][m-config], [Whisper engine][m-whisper], [Parakeet catalogue][m-parakeet], [Parakeet runtime][m-parakeet-loader], [summary catalogue][m-summary], [summary recommendation][m-summary-commands], [Cargo manifest][m-cargo], [lock][m-lock], [VAD][m-vad], [permissions][m-permissions], [bundle settings][m-tauri], [license][m-license].
- **Tacet:** [README][t-readme], [requirements][t-requirements], [Whisper backend][t-whisper], [VAD/transcriber][t-transcriber], [speaker embedder][t-speaker], [LLM selection][t-llm], [provider payload][t-payload], [desktop configuration][t-config], [session handling][t-main], [session restoration][t-engine], [notices][t-notices].
- **VOA:** [README][v-readme], [package][v-package], [lock][v-lock], [onboarding][v-onboarding], [defaults][v-schema], [effective model ID][v-service], [choices][v-constants], [Whisper inference][v-whisper], [GGUF download][v-gguf], [LLM inference][v-llama], [structured extraction][v-structured], [license][v-license].
- **Model support and terms:** [Whisper Large v3 card][whisper-card], [Qwen3 card][qwen3-card], [Gemma 3 card][gemma3-card], [Community-1 conversion notice][diar-notice], [ECAPA card][ecapa-card], [Qwen2.5 GGUF card][qwen25-card], [Ollama Llama 3.1 listing][ollama-llama], [Llama terms][llama-license].

[h-readme]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/README.md
[h-package]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Package.swift
[h-lock]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Package.resolved
[h-architecture]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/ARCHITECTURE.md
[h-cask]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/Casks/hushscribe.rb
[h-license]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/LICENSE
[h-settings]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Settings/AppSettings.swift
[h-engine]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Transcription/TranscriptionEngine.swift
[h-whisper]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Transcription/WhisperKitBackend.swift
[h-apple]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Transcription/SFSpeechBackend.swift
[h-summary-models]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Models/SummaryModel.swift
[h-summary-engine]: https://github.com/drcursor/HushScribe/blob/51103f0c8f97344ec7ecdf6480a2ee53cd9a0e92/HushScribe/Sources/HushScribe/Services/LLMSummaryEngine.swift
[f-models]: https://github.com/FluidInference/FluidAudio/blob/ea500621819cadc46d6212af44624f2b45ab3240/Sources/FluidAudio/ModelNames.swift
[f-offline-models]: https://github.com/FluidInference/FluidAudio/blob/ea500621819cadc46d6212af44624f2b45ab3240/Sources/FluidAudio/Diarizer/Offline/Core/OfflineDiarizerModels.swift
[f-offline-config]: https://github.com/FluidInference/FluidAudio/blob/ea500621819cadc46d6212af44624f2b45ab3240/Sources/FluidAudio/Diarizer/Offline/Core/OfflineDiarizerTypes.swift
[f-license]: https://github.com/FluidInference/FluidAudio/blob/ea500621819cadc46d6212af44624f2b45ab3240/LICENSE
[wk-download]: https://github.com/argmaxinc/WhisperKit/blob/e2adabbe7d98dc4d0ab9a5b75424ecc42a9cdbef/Sources/WhisperKit/Core/WhisperKit.swift
[wk-config]: https://github.com/argmaxinc/WhisperKit/blob/e2adabbe7d98dc4d0ab9a5b75424ecc42a9cdbef/Sources/WhisperKit/Core/Configurations.swift
[m-readme]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/README.md
[m-config]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/config.rs
[m-whisper]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/whisper_engine/whisper_engine.rs
[m-parakeet]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/parakeet_engine/parakeet_engine.rs
[m-parakeet-loader]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/parakeet_engine/model.rs
[m-summary]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/summary/summary_engine/models.rs
[m-summary-commands]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/summary/summary_engine/commands.rs
[m-cargo]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/Cargo.toml
[m-lock]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/Cargo.lock
[m-vad]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/audio/vad.rs
[m-permissions]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/src/audio/permissions.rs
[m-tauri]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/frontend/src-tauri/tauri.conf.json
[m-license]: https://github.com/Zackriya-Solutions/meetily/blob/a2cb62e827da7ef59f65064c97233efb2313878e/LICENSE.md
[t-readme]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/README.md
[t-requirements]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/requirements.txt
[t-whisper]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/whisper_backend.py
[t-transcriber]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/transcriber.py
[t-speaker]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/speaker_embedder.py
[t-llm]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/llm_service.py
[t-payload]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/openai_compat_service.py
[t-config]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/electron/config.js
[t-main]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/main.py
[t-engine]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/web/backend/engine.py
[t-notices]: https://github.com/Tacetapp/tacet/blob/d976b40c0c63d5ab7f1121e5e48606ffb475fa2b/NOTICES
[v-readme]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/README.md
[v-package]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/package.json
[v-lock]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/package-lock.json
[v-onboarding]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/renderer/pages/Onboarding.tsx
[v-schema]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/store/schema.ts
[v-service]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/services/transcriber.ts
[v-constants]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/lib/Constants.ts
[v-whisper]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/pipeline/whisper-process.ts
[v-gguf]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/gguf-model-cache.ts
[v-llama]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/pipeline/llama-process.ts
[v-structured]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/src/main/pipeline/structured-summarizer.ts
[v-license]: https://github.com/justanotherkevin/VOA/blob/d2a9a3af2cc76f8f0a674c017dd439bc8609ab49/LICENSE
[whisper-card]: https://huggingface.co/openai/whisper-large-v3
[qwen3-card]: https://huggingface.co/Qwen/Qwen3-0.6B
[gemma4-card]: https://huggingface.co/google/gemma-4-E4B-it
[gemma3-card]: https://ai.google.dev/gemma/docs/core/model_card_3
[diar-notice]: https://huggingface.co/FluidInference/speaker-diarization-coreml/blob/df2625ac79a7ac6b65ad868fee6d80f320da4232/NOTICE.md
[ecapa-card]: https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb/blob/0f99f2d0ebe89ac095bcc5903c4dd8f72b367286/README.md
[qwen25-card]: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/91cad51170dc346986eccefdc2dd33a9da36ead9/README.md
[ollama-llama]: https://ollama.com/library/llama3.1
[llama-license]: https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE
[qwen35-2]: https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/tree/f6d5376be1edb4d416d56da11e5397a961aca8ae
[qwen35-4]: https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/tree/e87f176479d0855a907a41277aca2f8ee7a09523
[qwen35-card]: https://huggingface.co/Qwen/Qwen3.5-2B
[llama-card]: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
[parakeet-onnx]: https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx/blob/8f23f0c03c8761650bdb5b40aaf3e40d2c15f1ce/README.md
[wk-decoder]: https://github.com/argmaxinc/WhisperKit/blob/e2adabbe7d98dc4d0ab9a5b75424ecc42a9cdbef/Sources/WhisperKit/Core/TextDecoder.swift
[wk-task]: https://github.com/argmaxinc/WhisperKit/blob/e2adabbe7d98dc4d0ab9a5b75424ecc42a9cdbef/Sources/WhisperKit/Core/TranscribeTask.swift
