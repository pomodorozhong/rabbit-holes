# AI Meeting Notes

This note examines how to produce meeting notes locally on a **MacBook Pro with M2 Pro and 16 GB unified memory**. The first test was whether a model can produce an accurate transcript and reliably distinguish the speakers in a meeting recording, because those outputs provide the material for summaries, decisions, and action items. A recording trial answered that question for one real call: Whisper Large v3 with Chinese forced, plus FluidAudio’s Sortformer diarizer, the model that decides who is speaking when, produced a usable transcript and kept the three speakers apart. Building the tool now continues in its own repository, [meeting-recap](https://github.com/pomodorozhong/meeting-recap).

We extracted the [Feature catalogue](feature-catalogue.md) from the documented workflows of [established paid AI meeting assistants](product-coverage.md): Notion, Amie, and Spellar. Its 22 features describe the intended behavior and common failures. They give the investigation a reference: which features each pipeline step supports, how errors affect later outputs, and what additional work a local implementation needs.

## General pipeline and its bottlenecks

The [open-source local solutions](open-source-pipelines.md) **Meetily, HushScribe, VOA, and Tacet** provide implementations to inspect. Their documented pipelines capture audio, split it into speech segments, turn speech into text, and produce notes. Speaker processing adds labels to the text where supported. Saving these outputs makes them available for history, search, export, and follow-up features.

The apps schedule that work differently. HushScribe describes separating speakers after the call and generating summaries on request; Tacet describes speaker processing alongside transcription and analysis during the call. This changes when labelled text and notes become available, and which models must run together. The [source overview](open-source-pipelines.md#observed-pipeline-patterns) records the documentation and selected source files inspected on **2026-10-06**. The [configuration review](open-source-pipelines.md#confirmed-models-runtimes-and-settings), inspected on **2026-10-08**, confirms the main model paths and requirements; it did not cover the wider feature set.

Consider this fictional exchange in a two-person meeting:

> Mei: “Let’s launch on Monday, not Friday.”
>
> Lin: “Agreed. I’ll update the checklist.”

Transcription needs to preserve the words, including “not.” Speaker separation needs to keep the two voices distinct so “I’ll update” stays attached to Lin’s turn. It can label them “Speaker 1” and “Speaker 2”; attaching their names requires confirmed identity information. The diagram connects those jobs to the later notes. It combines the observed paths into a general model; each app may run the steps in a different order or leave some out.

```mermaid
flowchart TD
    input["Microphone, call audio, or imported file"] --> capture["Capture and recording controls"]
    capture --> chunks["Detect speech and form audio chunks"]
    chunks --> A["A. Transcribe speech"]
    chunks --> B["B. Separate speaker voices"]
    B --> names["Confirm speaker names"]
    A --> transcript["Assemble text, times, and speaker labels"]
    names --> transcript
    transcript --> C["C. Summarize and extract decisions and actions"]
    transcript --> storage["Save source material and derived notes"]
    C --> storage
    storage --> use["History, search, questions, export, and follow-up"]
    classDef core fill:#e8f0fe,stroke:#4263eb,stroke-width:2px,color:#172554
    class A,B,C core
```

A bottleneck is a step that holds up the work that follows it. For example, if transcription takes longer to process speech than new speech takes to arrive, unfinished audio accumulates and the live text falls behind. Several models running together can also exceed the available memory. Processing speakers or summaries after the call reduces the work that must run at once, at the cost of waiting for those outputs.

Speed alone does not make the output useful. If capture misses Mei’s sentence, the transcript has no launch decision to pass to the summary step. If the text loses “not,” or the speaker labels move Lin’s words to Mei, later notes can report the wrong meaning or task owner. Keeping the text’s order, times, and speaker labels makes these errors easier to trace. The [stage-to-feature map](feature-catalogue.md#pipeline-steps-and-feature-impact) lists the starting dependencies for all 22 features.

## Why these steps can be bottlenecks and why they matter

**A. Transcription** produces the text (**MN-04**) that the other steps read. It must preserve the meeting's languages, names, technical terms, and meaning. In the exchange above, losing the word “not” changes the launch statement. A model that gets the words right but processes the recording too slowly may also be impractical.

**B. Speaker separation and identity** keep each part of the text attached to a voice (**MN-06**). Overlapping speech or several voices picked up by one microphone can cause speakers to be merged or labelled inconsistently. That matters even when the words are correct: Lin's “I'll update the checklist” needs to stay attached to Lin's turn. Attaching a person's name (**MN-07**) requires confirmed identity information as well as voice separation.

**C. Summaries, decisions, and actions** use that text and speaker context to produce the notes (**MN-08**–**MN-10**). In the example, the expected decision is a Monday launch and the task belongs to Lin; no task deadline was stated. Errors in A or B can change those outputs before the summary model reads them. Long transcripts can also increase processing time and memory use at C. This makes transcription and speaker separation a useful first check, while leaving summary quality as a separate question.

The [source observations](open-source-pipelines.md#what-these-patterns-tell-us) provided the starting options for that check. The rule was to stop testing once a model reliably distinguished speakers and produced a good transcript on this Mac, and otherwise to let the actual failures choose the next experiment.

## What the recording trial found

The [configuration review](open-source-pipelines.md) selected a HushScribe source build with Whisper Large v3, language detection enabled, and FluidAudio’s offline Community-1 diarizer. In October 2026 it ran on a ten-minute excerpt of a three-person online call in Mandarin with English product terms, recorded by a meeting app as one mono track. Two full recordings, 22 and 65 minutes long, then checked whether speaker labels stayed stable over time.

**Whisper Large v3 with Chinese forced, plus FluidAudio’s Sortformer diarizer, produced a usable transcript and kept the speakers apart.** The author named the speakers in 34 short clips by listening. On the 14 clips from the excerpt, Sortformer recovered 29 of the 30 speaker turns. Over both full recordings, 87 minutes in total, it kept one label each for two participants and split the third participant’s voice across two labels, which a naming step can merge. For the 65-minute recording, transcription took 14 minutes and speaker separation 26 minutes, each under 1.6 GB of peak memory.

**The setup first chosen from the source review did not separate the speakers.** Its transcript mostly preserved the meaning, with misheard names, a few wrong words, and short invented lines in other languages where language detection ran on very short chunks. But its Community-1 diarizer put almost all speech from three people under one label. No setting fixed it; the best recovered 19 of the 30 speaker turns.

These results come from one call and from clips checked by one listener, so they show the kinds of errors rather than error rates. They do not cover summaries, live labels during a call, or calls with more than four speakers, which is Sortformer’s limit.

## Where the work continues

Testing more models stopped there. Building a working tool, starting with a pipeline for saved recordings, continues in [meeting-recap](https://github.com/pomodorozhong/meeting-recap). The investigation plan and the review guide moved there, and the full trial record and the experiment code were written there. The [experiment summaries](https://github.com/pomodorozhong/meeting-recap/tree/main/docs/experiments) give the pinned setup, runtimes, and scores behind each result above, starting with the [HushScribe trial](https://github.com/pomodorozhong/meeting-recap/blob/main/docs/experiments/2026-10-24-hushscribe-trial.md), the [diarizer comparison](https://github.com/pomodorozhong/meeting-recap/blob/main/docs/experiments/2026-10-24-diarizer-comparison.md), and the [full-recording run](https://github.com/pomodorozhong/meeting-recap/blob/main/docs/experiments/2026-10-24-full-recordings.md). This topic keeps the background research: the feature catalogue, the paid-product comparison, and the review of open-source pipelines.

## Documents in this topic

- [Feature catalogue](feature-catalogue.md)
  - Which 22 behaviors should a meeting-notes tool provide, and what are their common failures?
  - Which pipeline step supports each feature?
- [Product coverage](product-coverage.md)
  - How do Notion, Amie, and Spellar document each catalogue feature?
- [Paid meeting-notes baseline](paid-baseline.md)
  - What do the paid products cost, and what limits, languages, and processing boundaries do they state?
- [Local pipeline sources](open-source-pipelines.md)
  - How do Meetily, HushScribe, VOA, and Tacet turn audio into notes?
  - Which models, runtimes, and settings do they use, and why was HushScribe chosen for the trial?

## Sources

The catalogue comes from the [dated paid-product research](paid-baseline.md#sources). Pipeline observations come from the primary project documentation and selected source files listed in [Local pipeline sources](open-source-pipelines.md#sources), initially inspected on **2026-10-06**, with configuration and artifact checks on **2026-10-08**. The combined diagram, feature dependencies, and choice of first experiments are our analysis of those sources. The trial result summarizes evidence recorded in [meeting-recap](https://github.com/pomodorozhong/meeting-recap).

[Back to all topics](../../README.md)
