# Learning notes

Compact notes from learning sessions and earlier research. Each note answers a few questions and keeps its sources and open questions nearby. Companion experiments can stay with a note while they are being explored or reviewed. Notes distilled from existing material do not require a session record; summaries of actual learning sessions are in [`sessions/`](sessions/).

[`topics/`](../topics/) is reserved for polished, fully reviewed documents and compact, interesting experiments. A note can be developed and reviewed for promotion there later.

The two-digit filename prefix follows the order in which each note subject was merged. Companion files for the same subject share one prefix, so they stay together when the directory is sorted by name.

## Notes

- [MLX vs oMLX](01-mlx-vs-omlx.md)
  - Is oMLX a faster version of MLX?
  - Where does oMLX's speed come from, and when does it help?
  - Does oMLX cover Whisper, TTS, image, video, or music generation?
- [Milestones in Running Lean](02-running-lean-milestones.md)
  - What counts as a milestone in *Running Lean* (3rd edition), and how is it set?
  - Are milestones only customer counts, or also stages such as Problem/Solution Fit?
  - What would the milestones look like for an indie iOS app or an indie game?
  - Do game sales really spike at launch?
- [Performant 2.5D VTubing on macOS](03-vtubing-pipeline-tech-stack.md)
  - Why might 2.5D preserve a convincing 3D effect at lower runtime cost?
  - What belongs in the complete webcam-to-OBS pipeline?
  - How can painterly toon, 1-bit, and comic-print rendering share one puppet?
- [Why Guoyu TTS can still sound like Putonghua](04-guoyu-voice-cloning.md)
  - Why can a model claim Guoyu support yet still sound closer to Putonghua?
  - Where is the gap between correct Traditional Chinese text and a convincing Guoyu voice?
  - Is training one specific voice realistic, and which Guoyu-oriented or trainable base best fits that goal?
  - What fallback and evaluation checklist can guide the search for a convincing local Guoyu voice?
- [How image watermarks work](05-ai-image-watermarks.md)
  - How can image changes carry bits without a visible label?
  - What do repetition, strength, compression, and cropping change?
- [How text watermarks work](05-ai-text-watermarks.md)
  - How can ordinary token choices carry a hidden statistical signal?
  - Why do passage length and rewriting affect detection?
- [Watermarks and provenance](05-ai-watermarks-and-provenance.md)
  - What do an embedded watermark and a signed provenance record each tell us?
  - What can we conclude when a signal or credential is missing?
- [Using subagents to reduce token cost](06-subagents-for-token-savings.md)
  - How can a Claude Code or Codex skill launch a subagent with a narrower context or cheaper model?
  - Is `fork_turns: "none"` portable between the two products?
  - Which of my existing skills, including commit and issue/PR filing, could benefit, and why?
- [ASICs and Local LLMs](07-llm-asics-and-local-inference.md)
  - What does an ASIC gain for LLM inference, and can it reduce local memory use?
  - What do current ASIC comparisons with GPUs measure, and how large are the gains?
  - How do their architectures differ, how long does a new ASIC take to make, and when were its speed results reported relative to the model release?
  - Could a frontier model such as Opus 5.5 run on an iPhone?
