# Session record: Guoyu voice cloning, 2026-10-24

## Starting point

- **Already knew:** The user had tested local voice cloning and ordinary TTS, including OmniVoice and every model available through `twtts` or its unmerged branches. The results consistently sounded closer to Putonghua than Guoyu.
- **Wanted to understand:** Why models advertised for Guoyu barely delivered the desired accent, where the technical gap was, and how to search for a better local solution.

## Questions and conclusions

### Why can a model claim Guoyu support yet sound wrong?

- **Understood:** Guoyu support can refer to several different capabilities. A model may accept Traditional Chinese text, use a `zh-TW` locale, provide a Bopomofo frontend, or copy the timbre of a Guoyu speaker without having learned Guoyu timing, intonation, and articulation. Some inspected models genuinely use Guoyu data, so its complete absence is not a sufficient explanation. The remaining question is where that data enters the stack and how much it changes the pretrained model. BreezyVoice trains the LLM component of its inherited CosyVoice pipeline for three epochs. BlueMagpie replaces the text-semantic frontend, reuses the VoxCPM2 acoustic stack, and jointly fine-tunes the assembled system on target-voice speech. Its paper calls this fine-tuning short relative to training from scratch, but does not establish that the amount of audio is small. PrimeTTS v2.1 instead learns from synthetic teacher speech filtered for intelligibility. These documented designs establish different forms of Guoyu adaptation; they do not establish which component caused the user's outputs.
- **Check:** The documentation supports the distinction, and the user's listening tests support that a label or frontend was insufficient. The exact cause of each model's output was not isolated with controlled audio comparisons.
- **Sources:** [OmniVoice languages](https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md), [OmniVoice voice design](https://github.com/k2-fsa/OmniVoice/blob/master/docs/voice-design.md), [BreezyVoice paper](https://arxiv.org/html/2501.17790), [BlueMagpie-TTS paper](https://arxiv.org/html/2607.06054), [PrimeTTS model card](https://huggingface.co/Luigi/PrimeTTS), and [Breeze2-VITS-ONNX model card](https://huggingface.co/MediaTek-Research/Breeze2-VITS-onnx), read 2026-10-24.

### Where is the gap?

- **Understood:** The working gap is incomplete or mismatched adaptation across the system. A safer generic pipeline is `text → text/semantic planner → acoustic renderer → waveform`, while speaker or reference information may condition the planner, renderer, or both. Bopomofo can select readings but cannot determine the whole delivery; BlueMagpie's controlled comparison also shows that a richer text-semantic frontend can materially affect output. Pretraining priors, component-level adaptation, speaker and register coverage, and the conditioning path are plausible contributors rather than proven causes of the user's samples. Common evaluations leave the same blind spot: character error rate measures intelligibility, and speaker similarity measures identity, but neither establishes that Guoyu-speaking listeners hear the regional variety as native.
- **Check:** This is the working explanation supported by the reviewed model documentation and the user's cross-model experience. It has not yet been confirmed by comparing intermediate representations or controlled outputs from the same sentences.
- **Sources:** [PrimeTTS model card](https://huggingface.co/Luigi/PrimeTTS), [BlueMagpie-TTS usage and evaluation](https://github.com/OpenFormosa/BlueMagpie-TTS/blob/main/USAGE.md), and [BreezyVoice](https://github.com/mtkresearch/BreezyVoice), read 2026-10-24.

### What directions are more promising?

- **Understood:** A better search should favor models that disclose real Guoyu speech data and accent-sensitive evaluation. BlueMagpie-TTS and BreezyVoice are the strongest local leads found because both explicitly target Guoyu; BlueMagpie supports ordinary synthesis, reference-clip cloning, and multi-clip speaker centroids, while BreezyVoice adds Bopomofo control to a Guoyu-adapted cloning system. An established `zh-TW` service or real Guoyu recording can serve as an accent baseline even when final deployment must remain local. A native source followed by consented RVC is a separate experiment: it tests whether conversion preserves accent and prosody without introducing unacceptable artifacts. Qwen3-TTS Base belongs in the reference-prompting track because its official repository does not document fine-tuning; GPT-SoVITS belongs in the adaptation track because it does document few-shot training.
- **Check:** The candidates and their documented capabilities were checked, but the user has not yet run a controlled comparison or confirmed whether the current BlueMagpie checkpoint was among the unmerged-branch tests.
- **Sources:** [BlueMagpie-TTS](https://github.com/OpenFormosa/BlueMagpie-TTS), [BlueMagpie usage guide](https://github.com/OpenFormosa/BlueMagpie-TTS/blob/main/USAGE.md), [BreezyVoice](https://github.com/mtkresearch/BreezyVoice), [Azure Speech language support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=text-to-speech), [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI), [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS), and [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS), read 2026-10-24.

### Is training one model realistic, and would ordinary fine-tuning fix the accent?

- **Understood:** Training a general Guoyu foundation model from scratch is not a realistic first solo project. Training one fixed voice can be realistic when the target corpus is clean, accurately transcribed, and authorized. However, a speaker embedding or acoustic-only LoRA may improve timbre without changing a Putonghua-leaning semantic or prosodic plan. BreezyVoice's training targets the speech-unit LLM, while BlueMagpie adapts its text-semantic frontend, bridge, and acoustic stack together. These systems support the need to adapt accent-relevant components rather than treating the task as ordinary speaker fitting.
- **Check:** The architectural distinction is documented. The amount and quality of the user's usable corpus are still unknown, so no training outcome is established.
- **Sources:** [BreezyVoice paper](https://arxiv.org/abs/2501.17790), [BlueMagpie-TTS paper](https://arxiv.org/abs/2607.06054), and [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS), read 2026-10-25.

### Is there a Guoyu-oriented base for the user's priority?

- **Understood:** The primary goal is one specific voice for which the user has many samples; the fallback is any TTS voice that speaks convincing Guoyu. BlueMagpie-TTS and BreezyVoice are the clearest Guoyu-oriented public checkpoints, but their supported releases focus on inference and do not provide turnkey custom training. BlueMagpie's model card explicitly describes an inference artifact. The current BlueMagpie release should first be tested with checkpoint `step_0006000` or later and a centroid averaged from several clean clips.
- **Understood:** VoxCPM2 is not an explicit Guoyu base, but it offers a documented LoRA and full-fine-tuning pipeline. Its LoRA can target both the language model and diffusion transformer; the official guide recommends rank 64 for style or language adaptation, 30–50% reference-conditioned samples to retain cloning behavior, roughly 20 GB VRAM for VoxCPM2 LoRA, and roughly 40 GB for full fine-tuning. Full training is the documented path for 1,000 or more clips. A separate single-speaker Piper/VITS model with Guoyu Bopomofo or custom phoneme IDs can test whether the target corpus teaches the desired delivery without inheriting a full Putonghua planner.
- **Understood:** The BlueMagpie/OpenFormosa project explicitly seeks speech-data and speaker-licensing partners. If the corpus can be shared under appropriate authorization, maintainer-supported target-speaker adaptation is the strongest direct route found to combine a Guoyu prior with the desired voice.
- **Check:** Release capabilities, public training support, and documented hardware figures were checked. The corpus duration, transcripts, recording consistency, and sharing constraints remain open.
- **Sources:** [BlueMagpie-TTS](https://github.com/OpenFormosa/BlueMagpie-TTS), [BlueMagpie model card](https://huggingface.co/OpenFormosa/BlueMagpie-TTS), [BlueMagpie usage guide](https://github.com/OpenFormosa/BlueMagpie-TTS/blob/main/USAGE.md), [BreezyVoice](https://github.com/mtkresearch/BreezyVoice), [VoxCPM2](https://github.com/OpenBMB/VoxCPM), [VoxCPM2 fine-tuning guide](https://voxcpm.readthedocs.io/en/latest/finetuning/finetune.html), and [Piper training guide](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/TRAINING.md), read 2026-10-25.

## The user's views and conclusions

- The user considers the tested outputs poor and consistently closer to Putonghua than Guoyu.
- The user found the same problem in ordinary TTS, so voice cloning alone cannot explain it.
- After testing all models available through `twtts`, including unmerged work, the user asked for a checklist that screens future candidates by evidence of Guoyu speech quality rather than by a `zh-TW` label alone.
- The user challenged the overbroad implication that the failed models lacked Guoyu training data. This led to the more precise conclusion that some models use genuine Guoyu data but apply it to only part of an inherited stack, use a narrow or synthetic distribution, or optimize metrics that do not directly measure regional accent.
- The user asked for the reviewed note to be fixed. The final revision corrects the conditioning model, separates documentation from causal hypotheses, distinguishes Qwen reference prompting from GPT-SoVITS training, frames RVC as an experiment, and restores the document to learning-note length.
- The user prefers the regional standards to be named Guoyu and Putonghua rather than with geographic Mandarin labels; official locale identifiers such as `zh-TW` remain unchanged.
- The user's first priority is one specific cloned voice, backed by many samples. If that cannot meet the accent target, the fallback is a non-cloning TTS model that speaks convincing Guoyu.
- The user expects that ordinary speaker fine-tuning may leave the underlying Putonghua bias intact. The revised training direction distinguishes speaker fitting from adapting the language, semantic-prosody, and acoustic components that can carry regional delivery.

## Set aside

- No individual model was installed or benchmarked during the session.
- The session did not attempt to define one universal Guoyu accent or catalog its phonetic features.

## Open questions

- Which audible features most strongly make the output sound like Putonghua to the user?
- Did the earlier tests include BlueMagpie checkpoint `step_0006000` or a later checkpoint?
- Does the best tested clone preserve the target speaker's timbre while losing the accent, or fail at both?
- Would a cloud `zh-TW` voice be acceptable as a diagnostic baseline even if deployment must remain local?
- How many hours of target-speaker audio are clean, accurately transcribed, consistently recorded, and authorized for adaptation or conversion?
