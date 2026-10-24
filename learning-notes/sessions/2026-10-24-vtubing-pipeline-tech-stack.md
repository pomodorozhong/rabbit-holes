# Session record: Performant 2.5D VTubing on macOS, 2026-10-24

## Starting point

- **Already knew:** The user understood the broad VTubing pipeline and initially described the desired avatar as 3D.
- **Wanted to understand:** How to build a personal VTubing setup that runs performantly on an M2 Pro Mac alongside OBS, reusing existing tools when they meet the requirement and replacing only measured bottlenecks.

## Questions and conclusions

### What workload must the Mac sustain?

- **Understood:** The Mac must run face tracking, avatar rendering, and OBS. A game may run on a console through a capture device or through GeForce NOW, so local game rendering is not required. The working output target is 1080p60, but it has not been benchmarked or turned into CPU, GPU, memory, thermal, or latency limits.
- **Check:** The workload came from the user's answers; the performance target remains provisional.
- **Sources:** No external sources were needed for the user's intended workload.

### Is local RGB webcam tracking viable, and how would an iPhone change the load?

- **Understood:** Monocular RGB tracking on the Mac is viable. MediaPipe Face Landmarker can consume a live camera stream and produce landmarks, facial-expression coefficients, and a facial transform. A compatible TrueDepth-equipped iPhone running ARKit can instead produce pose and blendshape coefficients before sending compact motion data to the Mac, removing most face-inference work from the Mac. Whether that meaningfully improves the complete stream depends on which stage is the measured bottleneck.
- **Check:** The user confirmed that their phrase “bitmap tracking” meant local RGB webcam tracking. No benchmark was run on the target Mac.
- **Sources:** [Apple ARKit face tracking](https://developer.apple.com/documentation/arkit/tracking-and-visualizing-faces), [MediaPipe Face Landmarker options](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/FaceLandmarkerOptions), [MediaPipe Face Mesh model card](https://storage.googleapis.com/mediapipe-assets/Model%20Card%20MediaPipe%20Face%20Mesh%20V2.pdf), and [Core ML performance reports](https://developer.apple.com/documentation/coreml/analyzing-a-core-ml-model-s-performance-in-xcode).

### Is a traditional 3D avatar the right representation?

- **Understood:** No. Exploring VRoid, VRM, optimized meshes, and low-poly alternatives clarified that authoring-tool weight and runtime-asset weight are different, but the user ultimately rejected a conventional skinned 3D humanoid. The selected direction is a front-facing 2.5D puppet made from separated illustrated parts and deformable textured meshes. It only needs convincing limited head turns rather than side or rear views. The user's working hypothesis is that this constraint can preserve much of the perceived depth of a 3D avatar at lower runtime cost by replacing some geometry, skinning, lighting, and physics with artwork, masks, shallow deformation, and simple style passes. That is a plausible design hypothesis, not a measured result.
- **Check:** The representation and motion boundary came from the user's correction and follow-up choices. It has not been prototyped.
- **Sources:** The discarded 3D comparison used [VRoid Studio](https://vroid.com/en/studio), the [VRM feature specification](https://vrm.dev/en/vrm/vrm_features/), and [VRoid's optimization controls](https://vroid.pixiv.help/hc/en-us/articles/18849783759257-For-each-item-of-model-data-information-that-can-be-viewed-on-the-model-page).

### What visual direction should the puppet use?

- **Understood:** The user chose a stylized illustration rather than a photo-derived portrait. Their preferred visual family includes the painterly or toon-like rendering of *Monster Hunter Stories 3: Twisted Reflection* and *The Legend of Zelda: Breath of the Wild*, with additional interest in *Return of the Obra Dinn*'s 1-bit dithering and *Spider-Man: Into the Spider-Verse*'s line work, halftoning, hatching, print effects, and stepped animation.
- **Check:** The illustration direction came from the user's choice between generated examples. The exact house style remains open.
- **Sources:** [Monster Hunter Stories 3 announcement trailer](https://www.youtube.com/watch?v=XszCdDNI-ls), [Breath of the Wild GDC session](https://www.gdcvault.com/play/1024562/Change-and-Constant-Breaking-ConventionsInteresting), [Lucas Pope's Obra Dinn dithering explanation](https://dukope.com/devlogs/obra-dinn/tig-32/), and [Sony Pictures Imageworks on Into the Spider-Verse](https://www.imageworks.com/node/1371).

### Does cel shading make an avatar 2.5D?

- **Understood:** No. Dimensionality describes the representation and allowed motion; cel or toon shading describes how an image is rendered. A lightweight 2.5D puppet can borrow the visual language of full 3D non-photorealistic rendering. Separating the puppet from an alpha-aware style pass would allow painterly cel bands, palette quantization, 1-bit dithering, halftones, hatching, ink overlays, print-registration offsets, or stepped motion without rebuilding the rig.
- **Check:** Covered but not checked by a prototype or a restatement from the user.
- **Sources:** The sources for the referenced visual styles are listed in the preceding question.

### Which existing 2D tools provide a useful baseline?

- **Understood:** Live2D Cubism provides a mature authoring path from PSD layers to ArtMeshes and deformers, and its native SDK supports Metal on macOS. VTube Studio is useful as a reference implementation, but its own documentation describes macOS webcam tracking as limited or experimental and OBS transparency as constrained. Inochi2D is an open deformable-puppet alternative with macOS tools, but its runtime separates tracking and lacks Syphon output on macOS. Existing tools should be benchmarked before any stage is replaced.
- **Check:** The product capabilities were checked against current official documentation, but none was installed or benchmarked.
- **Sources:** [Live2D PSD import](https://docs.live2d.com/en/cubism-editor-manual/psd-import/), [Live2D deformers](https://docs.live2d.com/en/cubism-editor-manual/deformer/), [Cubism platform support](https://docs.live2d.com/en/cubism-sdk-manual/platform/), [VTube Studio known issues](https://github.com/DenchiSoft/VTubeStudio/wiki/Known-Issues), [VTube Studio OBS capture](https://github.com/DenchiSoft/VTubeStudio/wiki/Recording-Streaming-with-OBS), [Inochi2D documentation](https://github.com/Inochi2D/inochi2d-docs/blob/main/docs/source/index.rst), and [Inochi Session releases](https://github.com/Inochi2D/inochi-session/releases).

### What belongs in the end-to-end checklist?

- **Understood:** The first-pass checklist covers goals and budgets; source artwork; rig and parameters; camera capture; face tracking; parameter mapping and temporal filtering; 2.5D rendering; transfer into OBS; OBS composition and encoding; measurement; reliability and privacy; and packaging and licensing. More clarification is needed to assign pass/fail criteria within those stages, not to discover additional major stages.
- **Check:** The checklist was presented but not explicitly confirmed by the user.
- **Sources:** This conclusion synthesizes the session and the product sources listed above.

## The user's views and conclusions

- The user prioritizes maximum runtime speed on an M2 Pro Mac.
- The user prefers to reuse existing tools and write custom components only where measurement shows a shortfall.
- The required local workload is tracking plus OBS; local game rendering is optional.
- The avatar should be a front-facing stylized 2.5D illustration rather than a conventional 3D model or a photo-derived portrait.
- The project should test the user's hypothesis that 2.5D can preserve a convincing 3D effect at lower cost; it should not assume the advantage before measuring the whole pipeline.
- The user wants an explicit end-to-end checklist so individual features can be judged in their place within the system.
- The user is interested in painterly cel rendering, 1-bit dithering, and comic-print treatments rather than one conventional VTuber look.

## Set aside

- A conventional VRoid-to-VRM avatar is no longer the default direction. It remains useful only as a comparison baseline.
- A fully custom 3D model and unrestricted side or rear views are outside the current scope.

## Open questions

- Should the rig cover only the face and head, or also shoulders and upper-body sway?
- Should the stack permit proprietary tools such as Live2D Cubism, or remain open source?
- Which webcam, capture resolution, and capture rate should the RGB tracker use?
- What end-to-end motion-to-display latency is acceptable?
- What sustained CPU, GPU, memory, energy, and thermal limits define success?
- Which existing macOS setup should become the measured baseline?
- Which OBS handoff should the prototype target: window capture and chroma key, NDI, Syphon through a compatible path, or another mechanism?
- Should the rendering references form one hybrid house style or several switchable modes?
