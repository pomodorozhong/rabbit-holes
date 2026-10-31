# How mumble speech can drive a 3D puppet

**Main insight:** Generated speech can give a puppet both its sound and its movement cues through a shared plan of sounds and timings. Live microphone input reverses part of the problem: the system has to estimate useful movement cues from audio whose contents it did not plan.

This note records explanations from the [original planning discussion](sessions/2026-10-29-mumble-voice-generator.md) and its [continuation](sessions/2026-10-31-mumble-voice-generator.md). Sources were checked on 2026-10-31; the mechanisms below have not yet been tested in a project prototype. The [project-start handoff](08-mumble-voice-generator-handoff.md) holds the implementation assignment.

**What makes invented speech feel like a language?**

- A proposed pipeline is `text → invented sounds → timing and pitch → audio`. The sound sequence supplies word-like groups; timing, stress, pauses, and pitch supply a performance. In the session's illustrative question, “Where are you going?”, invented words could keep the phrase's grouping and question contour without preserving intelligible speech.
- The proposed language rules use a small consonant/vowel inventory and syllable patterns such as consonant–vowel (`CV`). A seeded word mapping can make repeated words consistent. Language rules and speaker settings answer different questions: which invented sounds are spoken, and how a character sounds while speaking them.
- Text analysis depends on the script. Spaces and word-length estimates can guide one frontend, but Chinese needs other rules or configurable heuristics. UTF-8 byte counts do not represent speech length. These were design considerations from the session, not evaluated algorithms.

**How can a small synthesizer produce a voice?**

- Formant synthesis shapes a generated voice source with resonances that distinguish vowel sounds. [klattsch](https://github.com/tgies/klattsch) demonstrates a phoneme-driven formant engine with pitch, timing, and voice-character controls. A **phoneme** is a speech-sound unit; sequences of these units let the prototype explore invented utterances directly.
- Recorded syllables offer human vocal texture but introduce joins and repetition to manage. Vocal-tract simulation, illustrated by [Pink Trombone](https://github.com/chdh/pink-trombone-mod), offers another way to control articulation. The session expected simple formants to be relatively inexpensive to render, but it did not benchmark the alternatives or establish which sounds most appealing.

**Why share speech timing with the puppet?**

- When the generator plans a sound, it can also plan the corresponding mouth movement. For an invented rounded vowel, the proposed system can schedule its audio and lip rounding together. This avoids making the generated-voice path rediscover its planned sounds by analyzing its own audio.
- A puppet instruction is a timed control value, such as jaw opening or lip rounding. A host maps that value onto its character's geometry or rig and renders it. Keeping that mapping outside the instruction generator lets different characters consume the same performance plan. This is an architectural proposal; it does not guarantee that the movement will look convincing.

**What did klattsch's moving face demonstrate?**

- The creator says the faces in *take seventeen* were rendered through the app's visualizer/video export feature, then composited into the finished scene. The app therefore generates the face animation, while the film adds scene composition. [Creator's behind-the-scenes post](https://crashunited.itch.io/klattsch/devlog/1683093/take-seventeen-a-short-animation-starring-klattsch)
- This confirms a visual feature in the app, but does not establish a 3D renderer or a reusable face renderer in the npm engine or free browser edition. The useful distinction is between the speech engine, the visualizer, and the finished scene; finding one does not establish availability of the others.

**Does live puppet control require recognizing words?**

- Word transcription is optional for the mouth-animation goal discussed here. A simple experiment can use voice activity and loudness to drive jaw opening. A richer analyzer estimates **visemes**, the visible mouth shapes associated with speech sounds.
- The live path has to estimate cues that the generated-voice path already planned. [NVIDIA Audio2Face](https://docs.nvidia.com/ace/audio2face-3d-microservice/latest/text/getting-started/overview.html) documents speech-audio input and facial-control output, establishing the general approach. It does not establish a lightweight Rust/WASM implementation for this project.
- Audio alone does not reveal the speaker's actual blinks or head movements. Those would require another input or authored animation. A talking face can therefore include expressive motion without claiming to track a real face.

**Where is the difficulty?**

The following ranking is an engineering estimate for simple facial animation, not a measured comparison.

| Task | Main difficulty | Relative effort |
| --- | --- | --- |
| Puppet instructions from known speech timing | Map sounds to appealing poses and smooth their transitions. | Lower |
| Convincing fictional voice generation | Tune articulation, rhythm, and variation over repeated lines. | Middle |
| Rich live mouth-shape estimation | Infer cues from unfamiliar voices and noisy audio with little delay. | Higher |

- A loudness-driven live jaw is an exception: it may be easier to prototype than the voice generator. Full-body puppeteering was outside this comparison. The difficulty depends on the fidelity being attempted, not just the module's name.

**Why prototype the voice and face in a browser?**

- The proposed TypeScript/Vite/Three.js/Web Audio playground puts editable voice controls, audio playback, and a face in one experiment. [klattsch](https://github.com/tgies/klattsch) already exposes timed synthesis targets; [Three.js](https://threejs.org/docs/pages/Mesh.html) exposes morph-target weights for shaping a mesh. The adapter still has to turn speech information into useful face controls.
- The purpose is to judge the combined effect before investing in the portable core. A sound can be synchronized correctly and still look unappealing. A small prototype makes repeated listening and visual comparisons possible; the recommendation is a convenience judgment, not a stack benchmark. [Vite](https://vite.dev/guide/) and [AudioWorklet documentation](https://developer.chrome.com/blog/audio-worklet-design-pattern/) describe the proposed browser infrastructure.
- Reusing one Rust codebase later does not require one binary format everywhere. The discussed packaging routes compile it to WASM for the web and native code for other hosts, with ecosystem-specific wrappers: [wasm-pack](https://wasm-bindgen.github.io/wasm-pack/) for web, PyO3/[maturin](https://www.maturin.rs/) for Python, and an [XCFramework in a Swift package](https://developer.apple.com/documentation/xcode/distributing-binary-frameworks-as-swift-packages) for Apple platforms. Those builds remain untested.

**What changes with streaming?**

- Audio output in successive buffers needs continuous synthesizer state and timely rendering. Streaming text adds incomplete information: after playing “Where are you”, the system cannot change that audio when “ going?” arrives. Waiting for words or punctuation trades starting speed for phrasing context.
- Audio rendering cannot block while waiting for text; buffering also does not increase the callback's processing budget. [AudioWorklet guidance](https://developer.chrome.com/blog/audio-worklet-design-pattern/) explains the rendering constraint. General streaming text-to-voice interfaces were deferred; the later microphone-to-puppet request is a separate live-input path.

**Project context and open questions**

- I want expressive fictional speech and an optional moving 3D puppet, with Babble Engine and klattsch as feature references. The [handoff](08-mumble-voice-generator-handoff.md) keeps the first prototype bounded to generated voice and face movement.
- What combinations of sound, pose mapping, and transition timing make the character appealing over several utterances?
- How much does richer live mouth-shape estimation improve the result over a loudness-driven jaw, and at what latency and processing cost?
