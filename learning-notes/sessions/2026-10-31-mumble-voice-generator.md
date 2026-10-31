# Session record: mumble voice generator continuation, 2026-10-31

Continues the [2026-10-29 planning discussion](2026-10-29-mumble-voice-generator.md). This record separates the user's current decisions from implementation suggestions.

## Starting point

- **Already knew:** The user had reviewed a plan for text-driven fictional speech with real-time speed and web/iOS/macOS portability goals.
- **Wanted to understand:** Whether adding streaming input and output would change the design.

## Questions and conclusions

### What changes with streaming input/output?

- **Covered:** Audio output can be rendered in successive buffers while preserving synthesizer state. Incremental text needs buffering because chunks can split words or arrive before sentence-ending punctuation. Waiting for context can improve phrasing at the cost of initial latency; already-played audio cannot be revised.
- **Example:** Starting an utterance before its final question mark arrives limits how much of its pitch contour can still be changed. The explanation was illustrative; no audio was generated.
- **Check:** The user judged the added complexity unnecessary for the current use case. This is an explicit scope decision, not a demonstrated comprehension check or a performance result.
- **Sources:** Google's [Audio Worklet design patterns](https://developer.chrome.com/blog/audio-worklet-design-pattern/) supports the discussion of render deadlines and buffering. The incremental text planner and latency/context tradeoff were engineering deductions for this project, not measured results.

### What is the current implementation and packaging plan?

- **Decided:** The user selected Rust and WASM, with packages usable from npm for web projects, uv for Python projects, and the appropriate iOS package ecosystem.
- **Proposed interpretation:** Use a shared Rust engine, compile to WASM for the web, and provide native builds for Python and Apple platforms. Candidate tools are wasm-pack for web packaging, PyO3/maturin for Python wheels, and a Swift wrapper with an XCFramework distributed through Swift Package Manager for Apple platforms. These specific tools and the native build approach are assistant proposals, not separately approved user choices.
- **Check:** Packaging mechanisms were checked against documentation during the write-up. No bindings, packages, or platform builds were created.
- **Sources:** [wasm-pack](https://wasm-bindgen.github.io/wasm-pack/), [wasm-pack build documentation](https://rustwasm.github.io/docs/wasm-pack/commands/build.html), [maturin](https://www.maturin.rs/), [uv dependency management](https://docs.astral.sh/uv/concepts/projects/dependencies/), and Apple's [binary frameworks as Swift packages](https://developer.apple.com/documentation/xcode/distributing-binary-frameworks-as-swift-packages), read 2026-10-31. The older wasm-pack build documentation describes generated WASM/JavaScript/npm artifacts; the project homepage now lives under wasm-bindgen.

### What features should guide the project?

- **Decided:** The user's stated feature goal is the combination of Babble Engine and klattsch.
- **Covered:** Babble Engine documents text-to-gibberish generation, voice and mood controls, recording, and WAV export. klattsch documents phoneme-driven formant synthesis with timing and pitch controls. These capabilities describe the references; the user has not yet selected an exhaustive first-release checklist or a code reuse strategy.
- **Check:** The reference capabilities were checked during the earlier write-up on 2026-10-31. No implementation or listening comparison establishes feature parity.
- **Sources:** [Babble Engine](https://github.com/wrongfloor-dev/babble-engine) and [klattsch](https://github.com/tgies/klattsch).

### Is klattsch's moving face part of the app?

- **Finding:** The creator confirms that the faces in *take seventeen* were rendered through the app's visualizer/video export feature and composited into a scene. The renderer's inclusion in the npm engine or browser edition, and whether it is 3D, were not established.
- **User response:** The user especially liked the face and changed the plan to include optional 3D puppet instructions.
- **Check:** Checked against the creator's post; no application or video-export test was run.
- **Sources:** [Creator's behind-the-scenes post](https://crashunited.itch.io/klattsch/devlog/1683093/take-seventeen-a-short-animation-starring-klattsch), read 2026-10-31.

### How should voice generation and puppet instructions connect?

- **Decided:** The user requested two main modules: a voice generator and optional output of instructions for manipulating a 3D puppet.
- **Proposed:** Share a timed speech-performance plan between audio generation and puppet controls. A host maps the controls to its character and renders it. Jaw opening, lip width, and lip rounding are candidate starting controls; no instruction format or rig was selected.
- **Check:** The two-module direction is explicit. The shared timeline and rig-independent control interface are assistant proposals; no prototype or comprehension check established their behavior.
- **Sources:** The conversation supplies the architecture. The [klattsch repository](https://github.com/tgies/klattsch) documents a timed synthesis schedule but does not establish a ready-made puppet-control track.

### Could live voice analysis feed the puppet generator?

- **Requested:** The user asked for a live voice-recognition module as another input to the puppet instruction generator.
- **Covered:** For the proposed mouth-animation goal, word transcription is optional. A basic path can map activity and loudness to jaw opening; a richer path estimates visible speech-mouth shapes, or visemes. The generated-voice path knows its planned sounds, while the microphone path has to infer movement cues from audio. Actual blinks and head motion are not established by audio alone; procedural movement would be authored animation.
- **Check:** The distinction was explained but not checked by restatement or implementation. The user continued to ask about difficulty and prototyping. No live-analysis model was selected or tested.
- **Sources:** [NVIDIA Audio2Face overview](https://docs.nvidia.com/ace/audio2face-3d-microservice/latest/text/getting-started/overview.html) documents speech-audio input and facial-control output. It demonstrates the category of system, not this project's performance or portability. The simpler jaw mapping and shared interface are proposed experiments.

### Which component is harder?

- **Covered:** The assistant estimated puppet instructions from known speech timing as easier, convincing fictional voice generation as intermediate, and rich live mouth-shape analysis as harder. The estimate assumes simple facial controls; full-body animation is outside its scope. A loudness-driven live jaw is an exception and may be easier than the voice generator.
- **Check:** This is an engineering judgment, not a benchmark. No implementation or separate understanding check was performed.
- **Sources:** The conversation supplies the estimate and its limits.

### Which prototype stack is most convenient?

- **Working direction:** The assistant recommended a TypeScript/Vite browser playground with Three.js and Web Audio, managed with npm, initially using klattsch's JavaScript engine. The first experiment would play invented phonemes and drive a simple face. The user responded positively and asked for a learning note paired with a project-start handoff.
- **Proposed sequence:** Explore behavior in TypeScript first, then implement selected core behavior in Rust and integrate its WASM build into the same playground. Starting in Rust/WASM was also offered as an alternative if avoiding a rewrite becomes more important.
- **Check:** Documentation confirms the components' relevant capabilities. Convenience is a project-specific judgment; no prototype, face rig, audio playback, or microphone test was produced.
- **Sources:** [Vite guide](https://vite.dev/guide/), [Three.js morph-target controls](https://threejs.org/docs/pages/Mesh.html), [klattsch engine](https://github.com/tgies/klattsch), and [AudioWorklet guidance](https://developer.chrome.com/blog/audio-worklet-design-pattern/), read 2026-10-31.

### What makes the first prototype ready for an unattended agent session?

- **Covered:** The direction was sufficient to begin, but the five-stage roadmap did not clearly bound one build session. Routine choices such as face geometry and control ranges can be delegated; the assignment needs an explicit deliverable, scope boundary, verification requirements, and stopping point.
- **Approved:** The user asked to adopt the proposed first-prototype contract: an npm/TypeScript/Vite/Three.js/Web Audio app using klattsch, editable phonemes and presets, a procedural face, jaw/lip controls, and optional puppet output. The agent may make reasonable design and dependency choices, document them, verify the scoped app, and stop without seeking aesthetic approval.
- **Deferred:** Text-to-babble, live microphone analysis, Rust migration, native packaging, and general streaming text interfaces belong to later sessions. The implementation session's assigned workspace supplies the destination.
- **Check:** This is authorization and scope, not an implementation result. No agent build was started. Control-range defaults, UI details, and operational verification steps in the handoff make the approved contract concrete.
- **Sources:** The conversation supplies the contract and approval; the handoff records it for the implementing session.

### What should the learning note preserve?

- **User correction:** The user found the earlier note too focused on project decisions and asked for what was learned instead.
- **Revision direction:** Explain fictional-speech planning, shared audio/puppet timing, the difference between word transcription and mouth-shape estimation, the limits of the klattsch face evidence, relative difficulty, browser prototyping, portability, and streaming. Keep the implementation assignment in the companion handoff and retain a brief attributed project goal in the note.
- **Check:** This reflects the user's requested editorial purpose. It does not add new technical experiments or claim that discussed design proposals have been validated.

## The user's views and conclusions

- Streaming adds more complexity than the current use case needs. Keep a short note about it and leave it out of the main plan.
- Rust and WASM are the current implementation direction, replacing the earlier unselected C++ suggestion.
- The engine should be reusable through familiar package managers in web, Python, and iOS projects.
- Babble Engine and klattsch together define the feature direction.
- The moving face is a major source of interest. The user explicitly expanded the project to two main modules, with puppet instructions optional for consumers.
- The user also requested a live microphone input path for puppet control.
- The browser playground is the working prototype direction; the portable Rust engine and ecosystem packages remain longer-term goals.
- The user approved a bounded autonomous first-prototype assignment, including delegated routine choices, explicit verification, and a stop before the later roadmap.
- The user wants the learning note to preserve explanations and insights; the handoff is the home for implementation decisions and instructions.

## Set aside

- General streaming text-to-voice interfaces are deferred. Their buffering policies and incremental API remain outside the main plan. The later live microphone-to-puppet request is a separate desired input path.
- Full-body puppeteering was outside the difficulty estimate. No camera-tracking system or word-transcription requirement was added.

## Open questions

- Which features from the two reference projects are essential for the first release?
- What production face appearance and rigs should follow the prototype? Prototype appearance and initial control conventions are delegated implementation choices.
- How far should live analysis go beyond a basic loudness-driven jaw?
- When should the prototype's selected behavior move into Rust?
- Which native binding tools and platform/architecture builds should the packages support first?
- What listening criteria and measured latency target should the prototype satisfy?
