# Project-start handoff: mumble voice and 3D puppet system

Use this brief to build the first prototype autonomously in the implementation session's assigned workspace. The [learning note](08-mumble-voice-generator.md) explains the reasoning; the [original session record](sessions/2026-10-29-mumble-voice-generator.md) and [continuation record](sessions/2026-10-31-mumble-voice-generator.md) preserve the discussion. The user approved the first-prototype contract below; no implementation has been completed.

## Resume point

- **Current state:** Planning only. No project scaffold, implementation, package build, listening experiment, or latency measurement exists in this work.
- **Source checkpoint:** These documents were prepared in the research repository on `learning-session/mumble-voice-generator`, after base commit `b8a73103128c11be5a7588ffcb8604434fc22c2b`. Use the version containing these planning files; the base commit alone does not contain them. No implementation issue or implementation PR was created in this session.
- **Immediate next action:** Execute the first-prototype contract below, verify the result, and stop at its finish line.
- **Project location:** Use the workspace assigned to the implementation session. Choose a descriptive local project name if needed. This research repository holds the brief; no separate implementation repository has been created here.

## First-prototype execution contract

Build one locally runnable **TypeScript + Vite + Three.js + Web Audio** app, managed with **npm**, that lets the user hear invented speech and watch an expressive 3D face move with it.

| Area | Required for this session |
| --- | --- |
| Voice | Use klattsch with editable phoneme input and several invented-speech presets. Expose pitch and speaking-rate controls. |
| Face | Create a simple expressive face from procedural 3D geometry. Choose its appearance and construction autonomously. |
| Puppet controls | Implement jaw opening, lip width, and lip rounding with documented ranges and smooth transitions. |
| Architecture | Keep the instruction generator independent of Three.js; support voice playback with puppet output disabled. |
| Interface | Provide play/stop, preset selection, voice controls, a puppet toggle, and a display of the active sound and face-control values. |
| Delivery | Include setup/run instructions, assumptions, verification evidence, and known limitations. |

**Decision authority:** Make reasonable implementation choices without asking for design approval. Choose compatible dependency versions, face geometry, pose mappings, control ranges, UI layout, and project structure. Record assumptions and tradeoffs. If a dependency is unsuitable, choose a practical substitute that preserves this prototype's purpose and document the reason.

**Scope boundary:** Leave text-to-babble generation, microphone analysis, Rust migration, native packaging, and general streaming text interfaces for later sessions. A phoneme-driven prototype is sufficient for this assignment; Babble Engine + klattsch remains the broader feature direction.

**Finish line:** Complete the first-prototype acceptance checks below and deliver a runnable app with evidence of the checks. Then stop. The later roadmap is context, not additional work authorized for this build session. If the environment prevents a check, complete all feasible implementation and verification, report the exact limitation, and do not claim that check passed or wait for an aesthetic preference.

## Goal and decisions

Produce expressive fictional speech from text, with optional synchronized instructions that a host can apply to a 3D puppet. The user is particularly interested in the moving face shown in klattsch's *take seventeen* video.

| Status | Direction |
| --- | --- |
| User decision | There are two main modules: voice generation and optional 3D puppet instruction output. |
| User request | Add an optional live voice-analysis path that can feed the puppet instruction generator. |
| User decision | Babble Engine + klattsch define the feature direction; the exact feature checklist is still open. |
| Working prototype direction | Use TypeScript, Vite, Three.js, Web Audio, and npm, starting with the existing klattsch engine. |
| Longer-term user direction | Build a reusable Rust core, compile it to WASM for web use, and package it for npm, Python/uv, and Apple projects. |
| Deferred | General streaming text-to-voice interfaces remain outside the current plan. |

The browser playground tests the voice-and-face interaction before the longer-term Rust implementation. Native binding tools and the full feature set remain future decisions.

## Module boundaries

```text
Text → fictional pronunciation / speech performance plan
                           ├→ voice synthesis → audio
                           └→ optional puppet instructions

Microphone → optional live voice analysis → puppet instructions

Puppet instructions → host rig mapping → 3D character
```

The shared speech performance is an internal handoff between components, not a third main product module. It should retain the sound identity and timing needed to generate both audio and animation.

- **Voice generator:** Accept complete text and voice settings, invent pronounceable sounds, and produce audio. During the first experiment, accepting phonemes directly is enough to isolate the sound-and-face interaction. Text-to-babble follows as its own task.
- **Puppet instruction generator:** Turn the shared performance into timed facial controls. It must be possible to use the voice module with puppet output disabled. Keep the control format independent of Three.js so another host can map it to a different rig.
- **Live voice analyzer:** Accept microphone audio and estimate movement cues. Begin with activity/loudness-driven jaw movement; evaluate richer mouth-shape estimation separately. Word transcription is not a prerequisite for this first experiment.
- **Preview host:** Apply controls to a simple face, play audio, and expose settings. A model loader, full avatar editor, or full-body animation system is unnecessary for the first milestone.

## Proposed first control format

Start with timestamped jaw opening, lip width, and lip rounding. Keep a neutral pose and smooth the transitions. The following is a starting interface, which the implementing agent may refine and document without requesting design approval:

```ts
type FaceControlSample = {
  timeSeconds: number; // Relative to the utterance's playback start.
  jawOpen: number;
  lipWidth: number;
  lipRound: number;
};
```

Use a documented range for each control. A convenient default is 0–1: jaw opening runs from closed to fully open, lip width from relaxed to wide, and lip rounding from unrounded to rounded. Zero is the default neutral value for this simple mapping. The agent may adjust these conventions if needed and document the result. Map the controls to the preview face's geometry in the host; a future character can supply a different mapping.

Use the same playback timeline for audio and animation. Inspect klattsch's compiled schedule before designing the adapter: its documentation establishes timed synthesis targets, not a ready-made viseme track. Preserve phoneme identity alongside timing if the face mapping needs it. The values above are animation controls, not estimates of physical lip dimensions.

## First-session work order

1. **Build the voice-and-face experiment.** Create the npm/Vite/TypeScript playground, integrate klattsch, and add a simple Three.js face. Provide phoneme input, playback, and a few voice/face controls. Keep rendering separate from instruction generation.
2. **Make synchronization inspectable.** Derive a small face-control track from known phoneme timing, play it with the audio, and display the active sound and control values. Start with jaw opening, lip width, and rounding.
3. **Verify and deliver.** Run the build and type checks, exercise the browser controls and playback, document the interface and limitations, and stop at the finish line.

Exact versions, project structure, and presentation details are delegated implementation choices. The broader feature set and live-analysis dependencies are outside this session.

## First-prototype acceptance checks

- A short invented phoneme sequence produces audible speech and visibly different mouth poses in the browser.
- Audio and face movement follow one playback timeline. Replaying the utterance or stopping playback does not leave the face stuck in an active mouth pose.
- Voice playback still works when puppet output is disabled.
- The preview consumes a documented control track through a small host adapter; the instruction generator does not require a Three.js scene.
- The interface makes it easy to repeat a few phrases and compare voice settings, timing, and mouth motion. Record observations rather than assuming that technical synchronization makes the result appealing.
- The npm production build and TypeScript check pass, and the development server serves the app successfully. Document the commands used.
- Inspect the running app in a browser: exercise presets, editing, voice controls, puppet enable/disable, play, stop, and replay. Check the console for errors and record what was actually observed about audio and animation. Use available browser and audio inspection tools without requiring a human listening session to complete the assignment.
- The README explains installation, development, build/check commands, module boundaries, face-control ranges, and known limitations. Include a screenshot or short capture when tooling permits.

Do not block the first prototype on agreeing to a numerical latency target. Record the available environment and any responsiveness observations; measure latency if the tooling supports it. The earlier 50 ms warm-start suggestion is neither an acceptance threshold for this session nor a demonstrated result.

## Later roadmap and design questions

After this prototype is reviewed, possible next work is text-to-babble, a basic microphone-to-jaw mode, richer live mouth-shape estimation, then extraction of the selected behavior into Rust/WASM and native packages. This is future context; stop the current build at the first-prototype finish line.

- Which Babble Engine and klattsch features are essential for the first release? Their combined feature direction is broader than the initial experiment.
- What should a production character look like, and which rigs should it support? The implementing agent chooses the prototype face independently.
- Which sound style should guide evaluation: rapid chatter, expressive fictional conversation, or realistic mumbling?
- How far should live microphone control go beyond a loudness-driven jaw, and what extra latency is acceptable?
- When should behavior move from TypeScript into Rust, and which Python/Apple platforms should be packaged first?

These questions do not block the first-prototype assignment. Record useful observations for the later review.

## References and checked limits

- **[klattsch engine](https://github.com/tgies/klattsch):** The open-source JavaScript engine documents phoneme input, timed synthesis schedules, AudioWorklet integration, and voice controls. Inspect its current exports when implementing the adapter.
- **[Babble Engine](https://github.com/wrongfloor-dev/babble-engine):** A reference for text-to-gibberish behavior, voice/mood controls, recording, and WAV export. No complete feature-parity claim has been made.
- **[The face in take seventeen](https://crashunited.itch.io/klattsch/devlog/1683093/take-seventeen-a-short-animation-starring-klattsch):** The creator confirms app visualizer/video export and subsequent scene composition. Availability of that renderer in the engine package, and whether it is 3D, were not established. Use the appearance as inspiration for the prototype.
- **[Vite](https://vite.dev/guide/), [Three.js mesh controls](https://threejs.org/docs/pages/Mesh.html), and [AudioWorklet](https://developer.chrome.com/blog/audio-worklet-design-pattern/):** These document the proposed browser components. None has yet been integrated in this project.
- **[Audio2Face](https://docs.nvidia.com/ace/audio2face-3d-microservice/latest/text/getting-started/overview.html):** Evidence that audio-driven facial-control output is feasible; it is not a selected live-analysis dependency or proof of a lightweight browser implementation.
- **[wasm-pack](https://wasm-bindgen.github.io/wasm-pack/), [maturin](https://www.maturin.rs/), [uv](https://docs.astral.sh/uv/concepts/projects/dependencies/), and [Swift binary packages](https://developer.apple.com/documentation/xcode/distributing-binary-frameworks-as-swift-packages):** Candidate packaging paths for the later Rust core, with no build or distribution validation yet.

## Verification at handoff

Documentation was reviewed against the session and checked sources; local links and whitespace were checked. No app build, audio playback, visual inspection of a prototype, microphone test, package build, or performance benchmark was run. To resume elsewhere, take the version containing these planning files rather than the recorded base commit alone.
