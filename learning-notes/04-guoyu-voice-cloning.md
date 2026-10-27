# Why Guoyu TTS can still sound like Putonghua

**Bottom line:** A model can genuinely train on Guoyu and still sound Putonghua-leaning. “Uses Guoyu data” does not reveal which part of the system learned from it, how representative that speech was, how strongly adaptation changed a pretrained Mandarin model, or whether anyone evaluated regional accent. The likely issue is incomplete or mismatched adaptation—not simply an absence of Guoyu data. For one target voice with many recordings, custom training can be realistic, but an ordinary speaker fine-tune may improve timbre without fixing the accent. *(As of 2026-10-25.)*

Here, **Guoyu** and **Putonghua** refer to two closely related Mandarin standards with distinct conventions in pronunciation and usage.

**Goal and fallback**

- My primary goal is to clone one specific voice, and I have many samples of it.
- My fallback is a TTS voice that speaks convincing Guoyu even if it cannot clone that speaker.

**Why “Guoyu support” can barely deliver**

“Support” can mean several different things. Accepting Traditional Chinese proves script handling. A `zh-TW` tag names an intended locale. Bopomofo can disambiguate readings. Voice cloning can copy identity cues. Low character error rate shows intelligibility. None of these, alone, establishes Guoyu timing, pitch movement, reductions, phrasing, or conversational register.

The stronger claim “trained on Guoyu” is still incomplete:

| Claim | What it establishes | What remains unknown |
| --- | --- | --- |
| Guoyu text frontend | Local text and readings can be represented | Whether the generated delivery sounds like Guoyu |
| Guoyu speech in training | Some model parameters learned from it | Which components, how much speech, and what speakers or styles |
| Voice cloning | The output can follow a reference speaker | Whether accent survives the conditioning path |
| Low ASR error | The words are recoverable | Whether native listeners hear the intended regional variety |

The inspected models illustrate the difference:

- [OmniVoice documents Chinese as one `zh` / `cmn` language](https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md), and [its listed Chinese dialect controls do not include a Guoyu condition](https://github.com/k2-fsa/OmniVoice/blob/master/docs/voice-design.md). Its public controls therefore provide no explicit Guoyu-specific condition.
- [BreezyVoice](https://arxiv.org/html/2501.17790) genuinely uses Guoyu data. Its paper says it trains the LLM component for three epochs and inherits the other components from CosyVoice. That architecture is documented fact. Whether an inherited component caused the user's Putonghua-leaning output is only a hypothesis; the available evidence does not isolate the cause.
- [BlueMagpie-TTS](https://arxiv.org/html/2607.06054) is also genuinely Guoyu-focused. It replaces the text-semantic frontend, reuses the VoxCPM2 acoustic stack, and jointly fine-tunes the assembled system on target-voice speech. Its controlled comparison shows that the localized frontend materially improves results with the same downstream stack. The paper calls the fine-tuning short relative to training from scratch, but does not justify describing the underlying audio amount as small.
- [PrimeTTS v2.1](https://huggingface.co/Luigi/PrimeTTS) trains on synthetic VibeVoice-Large speech and filters it by ASR character error. That gate checks intelligibility, not accent or naturalness. Teacher-accent inheritance is therefore plausible, but it has not been demonstrated for the user's samples. [Breeze2-VITS-ONNX](https://huggingface.co/MediaTek-Research/Breeze2-VITS-onnx) is distilled from BreezyVoice; its card does not measure how regional nuance survives distillation.

The user heard the same broad problem in every `twtts` candidate tested, including unmerged branches, and in stock TTS as well as cloning. This makes one cloning bug an unlikely complete explanation, but different models may still fail for different reasons.

**Where the gap is**

A safer simplified pipeline is:

`text → text/semantic planner → acoustic renderer → waveform`

Speaker or reference information is not necessarily a later serial step. Depending on the architecture, it can condition the planner, the renderer, or both. In BreezyVoice, speaker information enters both the LLM and CFM stages.

Guoyu support can affect any part of this system. Bopomofo fixes selected readings but cannot determine the whole delivery. Conversely, BlueMagpie's controlled result shows that a richer text-semantic frontend can affect more than character pronunciation. A Putonghua-leaning result could arise from the planner, renderer, reference-conditioning path, training coverage, or their interaction.

Three gaps remain plausible rather than proven:

- **Adaptation:** Guoyu data changes only part of a large pretrained system, or does not outweigh every salient prior.
- **Coverage:** authentic recordings still miss the desired age, register, speaking style, or regional mixture.
- **Conditioning:** a clone preserves timbre more reliably than accent because its reference representation discards or underweights pronunciation and prosody.

Evaluation creates another gap. Character error rate measures recoverable words; speaker similarity measures identity. Neither asks whether Guoyu-speaking listeners hear regionally natural speech. BlueMagpie's native-listener study is stronger evidence, but it establishes preference over its VoxCPM2 baseline—not universal accent fidelity.

**Is training one specific voice realistic?**

Training a general Guoyu foundation model from scratch remains a large research project. Training one fixed voice is different. If the available recordings form a clean, accurately transcribed, authorized corpus, a model can learn that speaker's voice and Guoyu delivery together.

The kind of training matters. A speaker embedding or acoustic-only LoRA can strengthen resemblance while leaving a Putonghua-leaning speech plan intact. A broader adaptation must reach the model's language or semantic-prosody planner as well as its acoustic renderer. A direct single-speaker TTS avoids arbitrary-speaker cloning altogether; it trades generality for a better chance of binding the target voice to the delivery found in the corpus.

**Is there a Guoyu-oriented training base?**

The closest public systems are Guoyu-oriented at inference time, but no inspected release cleanly combines that prior with a supported custom-training recipe:

| Candidate | Guoyu prior | Route to the target voice | Main limitation |
| --- | --- | --- | --- |
| [BlueMagpie-TTS](https://github.com/OpenFormosa/BlueMagpie-TTS) | Explicit | Reference audio or a multi-clip speaker centroid | Its [published checkpoint is an inference artifact](https://huggingface.co/OpenFormosa/BlueMagpie-TTS), not a documented fine-tuning release |
| [BreezyVoice](https://github.com/mtkresearch/BreezyVoice) | Explicit | Reference-prompt cloning | Its public repository documents inference, not a supported training workflow |
| [VoxCPM2](https://github.com/OpenBMB/VoxCPM) | General Chinese, not explicit Guoyu | Official LoRA or full fine-tuning | Custom training may still need to overcome a Putonghua prior |
| [Piper/VITS](https://github.com/OHF-Voice/piper1-gpl) | Supplied by the corpus and frontend | Train one fixed voice directly | Produces a fixed voice rather than an arbitrary-speaker cloner |

The distinction makes BlueMagpie the best ready-made Guoyu cloning test, but not yet the easiest model to adapt. Its current documentation recommends checkpoint `step_0006000` or later and says that averaging several clean samples into a speaker centroid gives more stable cloning. An older experimental integration does not establish how the current checkpoint performs.

**Directions that match the two goals**

- First retest the current [BlueMagpie checkpoint](https://github.com/OpenFormosa/BlueMagpie-TTS/blob/main/USAGE.md) with a centroid averaged from several clean target-speaker clips. This is the least expensive route to the primary goal.
- If that fails, try [VoxCPM2's supported adaptation path](https://voxcpm.readthedocs.io/en/latest/finetuning/finetune.html). A relevant first experiment enables LoRA on both its language model and diffusion transformer, uses the documented rank-64 setting for style or language adaptation, and makes 30–50% of samples reference-conditioned. The guide estimates about 20 GB of VRAM for VoxCPM2 LoRA. With at least 1,000 high-quality clips, full fine-tuning is the documented larger-customization path, at roughly 40 GB of VRAM. These settings make accent adaptation possible; they do not guarantee it.
- In parallel or if the VoxCPM prior persists, train one compact [Piper/VITS](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/TRAINING.md) voice with Guoyu Bopomofo or custom phoneme IDs. A vocoder-only warm start preserves waveform knowledge without importing a complete Putonghua text-to-prosody model. This is both a candidate solution and a diagnostic: Guoyu delivery with lower audio richness would show that the corpus and frontend can teach the accent.
- If the recordings can be shared under appropriate authorization, ask the BlueMagpie/OpenFormosa maintainers about a target-speaker adaptation. The project explicitly seeks speech-data and speaker-licensing partners, while its self-service training recipe is not public.
- If custom voice training remains unsatisfactory, return to the secondary goal: choose between current BlueMagpie and BreezyVoice stock voices by blinded Guoyu listening tests rather than by model labels or character error rate.
- Establish an accent control: ideally a real Guoyu speaker reading the same sentences, with an Azure `zh-TW` voice as a secondary diagnostic baseline. Azure currently lists `HsiaoChen`, `YunJhe`, and `HsiaoYu` under its [`zh-TW` locale](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=text-to-speech).
- Treat two-stage voice conversion as an experiment: generate or record the right Guoyu delivery, pass it through an authorized [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) model, then listen specifically for accent and prosody retention as well as conversion artifacts. RVC documentation establishes a conversion workflow, not that accent will necessarily survive it.

**Rough checklist for finding and testing a better solution**

1. **Define the target, corpus, and rights.** Inventory how many hours are clean and accurately transcribed, how consistent the microphones and registers are, and whether cloning, adaptation, or conversion is authorized. Record native references for the exact test sentences.
2. **Screen evidence, not labels.** Look for real versus synthetic speech, Guoyu speaker provenance, hours and speaker counts, read versus conversational coverage, which components were adapted, and native-listener accent evaluation.
3. **Freeze the test conditions.** Use one pack containing polyphonic characters, numbers, Guoyu-specific vocabulary, questions, sentence-final particles, punctuation-sensitive phrasing, code-switching, and long-form text. Record checkpoint, frontend, language tag, seed, decoding settings, reference clips, and transcript.
4. **Compare stages.** Listen to the human reference, a known `zh-TW` control, each stock voice, its clone, and the voice-conversion experiment. This locates whether the problem begins in base TTS, cloning, or conversion.
5. **Score separate dimensions.** Rate words, Guoyu pronunciation, rhythm, intonation, naturalness, artifacts, speaker similarity, and long-form stability. Blind filenames and use more than one Guoyu-speaking listener where possible.
6. **Apply stop rules.** Reject a candidate whose stock TTS fails the accent target. Investigate conditioning only when stock TTS passes but cloning fails. Keep conversion only if a native source retains its accent after conversion. Compare speed, memory, and privacy only among candidates that first pass the listening test.

**Open**

- Which exact pronunciation, rhythm, or intonation cues make the output sound like Putonghua?
- Did the earlier tests include BlueMagpie checkpoint `step_0006000` or later?
- Does the best clone preserve timbre but lose accent, or fail at both?
- How many hours of the target voice are clean, accurately transcribed, and consistent enough for training?
