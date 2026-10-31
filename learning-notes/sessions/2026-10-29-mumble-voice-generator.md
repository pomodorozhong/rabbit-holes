# Session record: planning a mumble voice generator, 2026-10-29

Reconstructed on 2026-10-31 from the complete two-turn Chat Mode discussion [Plan Mumble Voice Generator](https://chatgpt.com/c/6ae305e2-9ea8-83e8-a793-f0bc06af14f7). The thread contains a project brief, an assistant-proposed plan, and a request for more references. It does not contain a user selection of an approach or a comprehension check.

## Starting point

- **Already knew:** The user had a project concept: take text and produce vocal audio that resembles a language without speaking the input as intelligible words. The thread does not establish prior knowledge of speech synthesis.
- **Wanted to understand:** How to plan the generator so it could run in real time and be reused in web, iOS, macOS, and other projects; which existing projects and videos would help explore the sound and implementation.

## Questions and conclusions

### Which sound-generation approach should the project start with?

- **Covered:** The assistant compared recorded syllable concatenation, formant synthesis, vocal-tract simulation, and neural generation. It proposed formant synthesis as a starting point, with a short listening comparison against recorded syllables before committing. Formants were introduced as resonances that distinguish vowels. The cost and sound-quality comparisons were qualitative engineering expectations, not benchmark results.
- **Check:** Covered but not checked. The user did not choose between Animal Crossing chatter, Simlish-style conversation, and realistic mumbling. The assistant's assumption that expressive fictional speech was the intended target remains unconfirmed.
- **Sources:** [klattsch](https://github.com/tgies/klattsch) documents phoneme-driven formant synthesis; [Pink Trombone TypeScript](https://github.com/chdh/pink-trombone-mod) documents vocal-tract synthesis. Both were read during the write-up on 2026-10-31. No listening comparison was performed.

### How can text become consistent fictional speech?

- **Covered:** The proposed pipeline separates text analysis, invented pronunciation, performance planning, and audio synthesis. It uses a small sound inventory, syllable patterns, seeded word mappings, smooth transitions, and phrase-level timing and pitch. Language rules remain separate from speaker settings so characters can share invented words while sounding different. The assistant used a question sentence to illustrate retaining word-like groups and a question contour, and noted that Chinese and other scripts need rules beyond splitting on spaces or counting UTF-8 bytes.
- **Check:** This was a design proposal. No algorithm was implemented, and no generated audio demonstrated that the rules produced convincing language-like speech.
- **Sources:** The source conversation supplies the proposal and example; these are not reported experimental findings.

### How could the same engine serve web and Apple platforms?

- **Covered:** The assistant proposed C++ with a small C interface, caller-provided audio buffers, and host-owned playback. The suggested web path was WebAssembly with a TypeScript wrapper and AudioWorklet; the Apple path was a native library with a Swift wrapper and AVAudioEngine. Rust was offered as an alternative if already familiar to the user.
- **Check:** The integration mechanisms were checked during the write-up, but this project has no compiled portable core or verified iOS build. The user did not select C++ or Rust.
- **Sources:** Google's [Audio Worklet design patterns](https://developer.chrome.com/blog/audio-worklet-design-pattern/) documents WebAssembly integration. Apple's [AVAudioSourceNode](https://developer.apple.com/documentation/avfaudio/avaudiosourcenode) documents supplying audio through a render block. Both were read on 2026-10-31, using Apple's Markdown documentation for its page content.

### What would real-time behavior mean, and what should be built first?

- **Covered:** Suggested acceptance targets included first generated audio within 50 ms after a warm submission, excluding device latency; rendering each buffer before its playback deadline; prompt cancellation with a fade; appending complete words; reproducible output for the same text, language, voice, and seed; and offline operation. Cold initialization was to be measured separately. The assistant recommended preallocation and keeping parsing, file access, and blocking work outside the audio callback.
- **Covered:** The proposed sequence was a sound experiment, a deterministic text-driven prototype, the same utterance playing in a browser and minimal iOS app, then packaging with queue/cancel controls, subtitle events, and WAV export. One fictional language and three voices were suggested for a first release.
- **Check:** These are proposed targets and milestones, not agreed requirements or measured results. The conversation contains no implementation or performance test.
- **Sources:** The source conversation supplies the targets and sequence; Google's [Audio Worklet design patterns](https://developer.chrome.com/blog/audio-worklet-design-pattern/) supports the discussion of callback deadlines and allocation pressure.

### Which references are useful to explore?

- **Covered:** The assistant recommended starting with Babble Engine, Pink Trombone, and animalese-web to compare configurable gibberish, simulated articulation, and fast character chatter. Other references were klattsch, Equalo's Python Animalese generator, ACVoicebox, BabbleSynth, and gb-speech. It also supplied Equalo's implementation video and FrankJavCee's Pink Trombone demonstration.
- **Check:** Project documentation was read on 2026-10-31. [Babble Engine](https://github.com/wrongfloor-dev/babble-engine) documents voice and mood controls, recording, and WAV export; [animalese-web](https://github.com/stefanlegg/animalese-web) documents letter scheduling and subtitle callbacks; [ACVoicebox](https://github.com/mattmarch/ACVoicebox) documents a Godot interface and character signals; [Equalo's generator](https://github.com/equalo-official/animalese-generator) documents pydub-based file output; [BabbleSynth](https://github.com/clo-yunhee/babblesynth) identifies itself as a parametric voice synthesizer but leaves feature and installation sections unfinished; [gb-speech](https://github.com/paladin-t/gb-speech) documents a C implementation tied to Game Boy audio hardware. The [Rust Pink Trombone port](https://github.com/lostmsu/pink-trombone) documents floating-point sample output. Demo pages were checked for availability, and YouTube oEmbed metadata confirmed both linked videos exist. No demos or videos were evaluated by listening, and no project was built or benchmarked.
- **Sources:** The linked repositories, demo references in the source conversation, [Equalo's video](https://www.youtube.com/watch?v=RYnI_ZLj5ys), and [Pink Trombone demonstration](https://www.youtube.com/watch?v=33Ajh_U7ciY).

## The user's views and conclusions

- The user wants text-driven vocal output that gives the impression of a language without intelligible speech.
- Real-time speed and reuse across web, iOS, macOS, and other projects are explicit priorities.
- The user requested more references with YouTube examples or repository links after receiving the initial plan.
- The user did not explicitly adopt the suggested synthesis method, implementation language, offline requirement, latency threshold, or first-release scope.

## Set aside

- No explicit exclusions were recorded. Implementation, sound evaluation, and platform validation were not carried out in the thread.

## Open questions

- Which sound should guide the project: rapid character chatter, expressive fictional conversation, or realistic mumbling?
- Which method remains pleasant over several lines, with enough consonant/vowel variety and little repetition?
- Should the portable core use C++ or Rust, and which candidate components can actually build for the required platforms?
- Can a prototype meet the proposed latency and callback deadlines on target devices?
- Which suggested requirements and first-release limits should become actual project commitments?
