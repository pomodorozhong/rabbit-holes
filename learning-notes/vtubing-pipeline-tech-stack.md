# Performant 2.5D VTubing on macOS

**Bottom line:** My working hypothesis is that a front-facing 2.5D puppet can preserve the depth cues I want from 3D while doing less work at runtime. The first project should test that hypothesis across the complete webcam-to-OBS path on my M2 Pro, starting with existing tools and replacing only measured bottlenecks. *(As of 2026-10-24.)*

**Project handoff:** [Bootstrap brief for a dedicated implementation repository](vtubing-pipeline-tech-stack-handoff.md).

**What I am building**

- A personal VTubing setup in which the Mac runs face tracking, the avatar, and OBS. The game can come from a console capture or GeForce NOW, so local game rendering is not required.
- A stylized, front-facing illustrated character with convincing small head turns, expressions, and some secondary motion—not a freely rotating 3D humanoid.
- A provisional 1080p60 output. That is a direction, not yet a performance budget.

**Why 2.5D might cost less than traditional 3D**

The intuition makes sense, but “2.5D” is not automatically fast. The potential saving comes from constraining the problem. A conventional 3D avatar may evaluate a skeleton, deform a mesh, simulate secondary motion, light a scene, and render surfaces that can be viewed from many directions. A front-facing 2.5D puppet can bake much of that information into artwork and reproduce only the cues visible from the intended camera.

| Desired 3D cue | Possible 2.5D substitute |
| --- | --- |
| Small head turns | Warp separated face and hair layers; shift them at different rates |
| Facial volume | Painted values, masks, or a shallow normal/depth hint |
| Expressions | Tracked parameters driving mesh deformation and texture swaps |
| Overlap and depth | Ordered layers, masks, and limited parallax |
| Stylized lighting | A small number of tone bands or a screen-space style pass |
| Hair and accessory motion | A few deformers or simple springs rather than a full physical rig |

That trade removes capabilities I do not need, such as rear views and arbitrary camera rotation. It does **not** guarantee a saving: many high-resolution layers, expensive full-screen effects, or complex deformation can make 2.5D heavy, while a carefully optimized 3D model can be cheap. Tracking, OBS composition, and video encoding may also cost more than the avatar renderer. The useful claim is therefore measurable: *this constrained puppet may deliver the desired depth cues within a lower end-to-end resource budget on this Mac*.

**Dimensionality and rendering style are separate**

Cel shading does not make a model 2.5D. Dimensionality describes the representation and the motion it supports; cel shading describes how the final image looks. The same 2.5D puppet could support several treatments:

- A painterly or toon-like default inspired by *Monster Hunter Stories 3: Twisted Reflection* and *The Legend of Zelda: Breath of the Wild*.
- A monochrome, 1-bit dithered mode inspired by *Return of the Obra Dinn*. Lucas Pope describes reducing a grayscale render to a 1-bit image through dithering in his [development notes](https://dukope.com/devlogs/obra-dinn/tig-32/).
- A comic-print mode drawing from *Spider-Man: Into the Spider-Verse*: line work, halftones, hatching, registration-like offsets, and deliberately stepped motion. [Sony Pictures Imageworks](https://www.imageworks.com/node/1371) describes the film's combination of CG imagery with hand-drawn and comic-book techniques.

The implementation details of the game references are not the requirement. They are visual targets. A useful renderer boundary is:

`puppet deformation -> base color and masks -> alpha-aware style pass -> OBS`

This keeps the rig reusable while the visual treatment changes. A hybrid house style or several switchable modes remains an art-direction decision.

**The complete pipeline checklist**

| Stage | What must be decided or verified |
| --- | --- |
| Goal and budget | Output resolution and frame rate; acceptable motion latency; sustained CPU, GPU, memory, energy, and thermal limits |
| Source artwork | Layer separation, overlap hidden beneath moving parts, working resolution, masks, and ownership or licensing |
| Rig | Parameters, deformers, draw order, clipping, expression states, head-turn range, and secondary motion |
| Capture | Camera, resolution, frame rate, exposure, lighting, framing, and behavior after disconnect or sleep |
| Tracking | Landmarks, head pose, expression coefficients, confidence, calibration, inference rate, and lost-face behavior |
| Mapping | Ranges, neutral pose, smoothing, dead zones, asymmetric expressions, blink and mouth logic, and per-user calibration |
| Rendering | Frame pacing, layer and texture limits, color management, antialiasing, alpha correctness, and cost of each style pass |
| OBS handoff | Window capture, chroma key, NDI, Syphon through a compatible path, or another transparent-output mechanism |
| OBS and encoding | Canvas and output sizes, encoder choice, scene complexity, capture source, audio sync, and dropped frames |
| Measurement | Per-stage timings, motion-to-display latency, CPU/GPU/ANE use, memory, energy, temperature, and a sustained-load test |
| Reliability and privacy | Camera permission, local processing expectations, recovery from device loss, logging, and safe defaults |
| Packaging | App startup, configuration, asset versioning, model portability, third-party licenses, and reproducible benchmarks |

The major stages are known. More clarification is needed to turn each row into a pass/fail contract.

**RGB webcam tracking is viable**

[MediaPipe Face Landmarker](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/FaceLandmarkerOptions) can process a live camera stream and return face landmarks, facial-expression coefficients, and a facial transformation matrix. That is enough data for the proposed limited-motion puppet. On the Mac, a likely optimization is to run inference below the display rate, then smooth or interpolate its parameters while rendering at 60 fps. That is a design proposal, not a benchmark result.

A compatible TrueDepth-equipped iPhone can help because [ARKit face tracking](https://developer.apple.com/documentation/arkit/tracking-and-visualizing-faces) produces face pose and blendshape coefficients on the phone. Sending those compact controls to the Mac can remove most face-inference work from the streaming machine. It will matter only if local tracking is a meaningful part of the measured bottleneck; it cannot fix an expensive renderer or overloaded OBS scene.

**Existing tools are the baseline, not the enemy**

- [Live2D Cubism](https://docs.live2d.com/en/cubism-editor-manual/psd-import/) already turns layered PSD artwork into deformable ArtMeshes, and its native SDK [supports Metal on macOS](https://docs.live2d.com/en/cubism-sdk-manual/platform/). It is the mature proprietary baseline.
- VTube Studio can exercise a Live2D model, but its documentation calls out [macOS tracking limitations](https://github.com/DenchiSoft/VTubeStudio/wiki/Known-Issues) and constraints in its [OBS capture paths](https://github.com/DenchiSoft/VTubeStudio/wiki/Recording-Streaming-with-OBS). Those are test items, not proof that it will fail this setup.
- [Inochi2D](https://github.com/Inochi2D/inochi2d-docs/blob/main/docs/source/index.rst) is an open deformable-puppet alternative. Its runtime keeps tracking separate, and the [Inochi Session release notes](https://github.com/Inochi2D/inochi-session/releases) do not offer a ready-made macOS Syphon path, so integration work may be larger.

The sensible sequence is to benchmark one existing setup under the real OBS workload, profile it, and custom-build only the stage that misses the contract. A custom renderer cannot recover time spent in tracking or encoding, and a custom tracker cannot repair a costly post-process stack.

**For me:** The project is not “build a VTuber stack from scratch.” It is “find the lightest architecture that produces this front-facing illustrated illusion on an M2 Pro while OBS is running.” I should preserve the option to write a small Metal renderer or local tracker, but earn that complexity with measurements.

**Open**

- Does the rig stop at the head, or include shoulders and upper-body sway?
- May the baseline use proprietary Live2D tools, or must the finished stack be open source?
- Which webcam, capture resolution, and tracking rate should the test use?
- What motion-to-display latency and sustained resource ceilings define success?
- Which existing setup should be the first measured baseline?
- Which OBS handoff should the first vertical slice target?
- Should the visual references become one hybrid style or separate modes?
