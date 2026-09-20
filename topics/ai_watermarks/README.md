# Understanding AI watermarks

AI watermarking is the practice of adding a machine-detectable signal to generated content. It sits alongside signed provenance metadata, which records claims about origin and edits. Each evidence layer survives different transformations and supports different conclusions.

This research is a guided introduction to those ideas. It develops the vocabulary first, follows a watermark through embedding and detection, compares representative systems, and ends with practical interpretation. The companion notebooks make the hidden intermediate steps visible.

This work grew from [issue #115](https://github.com/pomodorozhong/rabbit-holes/issues/115).

## How to use this guide

A useful learning order is:

1. Distinguish a watermark from provenance metadata and generic AI detection.
2. Follow the common embed–transform–detect pipeline.
3. Learn how the signal changes across image, audio and text.
4. Study the trade-offs that determine whether a design is useful.
5. Map those concepts onto real systems and chat products.
6. Practice with the focused notebooks and the detection guide.

## 1. Why generated content needs evidence

Once content leaves a model, its origin does not automatically travel with it. A file can be renamed, copied, recompressed, cropped, screenshotted or detached from its metadata. Text can be pasted, shortened, translated or paraphrased. Every transformation changes which evidence remains available.

This makes “Was this made by AI?” too broad to be a single technical question. A useful system asks narrower questions:

- Who signed the claim about this asset?
- Does this rendition contain a signal associated with a known generator?
- Has the asset changed since it was signed?
- Can a transformed copy still be linked to its original manifest?
- How likely is this detector result under human or unmarked content?

Watermarking is therefore best understood as evidence engineering, not as a universal AI label.

## 2. Four different kinds of evidence

The word “watermark” is often used for mechanisms that behave very differently.

| Evidence type | Where it lives | What it can show | Typical weakness |
|---|---|---|---|
| Visible label | Rendered pixels or product UI | A platform chose to display an “AI” mark or logo | Easy to crop, cover or copy onto unrelated content |
| Signed provenance | A cryptographically signed manifest, often using C2PA | An issuer made a claim about origin, edits and ingredients | Metadata can be removed; trust depends on signatures, issuers and validation |
| Embedded watermark | Pixel values, frequency coefficients, audio samples or token choices | A detector recognized a provider-specific signal | Transformations and attacks can weaken the signal; detection needs calibration |
| Generic AI detector | A separate classifier's model of style or distribution | The content resembles examples the classifier learned | It does not recover a watermark key or prove origin and can misclassify human content |

A valid signature is evidence about a signed claim. A detected watermark is evidence that a detector recognized a signal. A generic detector produces a probabilistic resemblance judgment. None of these alone proves that an unmarked asset is human-made.

## 3. The embed–transform–detect pipeline

Most watermark systems can be understood through the same sequence:

```text
generator or editor
    -> embed a keyed signal and/or sign provenance
    -> publish the asset
    -> asset is copied, compressed, cropped, translated or edited
    -> detector or validator examines the resulting rendition
    -> report a scoped result with confidence and provenance state
```

The visible asset is only one part of the system. A deployable design also needs:

- an **embedder** that controls where and how strongly the signal is added;
- a **secret or model identity** that prevents arbitrary parties from reproducing the signal;
- a **channel model** describing expected transformations such as JPEG, resizing or paraphrase;
- a **detector** that converts noisy observations into a score or recovered message;
- a **calibration policy** that turns scores into decisions at a measured false-positive rate;
- operational records for keys, detector versions, thresholds and manifests.

Skipping any of these pieces can make an otherwise clever embedding algorithm unusable in practice.

## 4. How the signal changes by medium

### Images and video

An image watermark slightly changes pixel values or an internal frequency/feature representation. Classical methods often modify DCT or wavelet coefficients. Learned methods use an encoder and detector trained together while simulating transformations.

```text
image + payload -> embedder -> watermarked image
watermarked image + resize/JPEG/crop -> detector -> payload or confidence
```

The signal must be strong enough to survive ordinary processing but weak enough to remain visually unobtrusive. Video adds temporal consistency: a frame-by-frame mark may flicker, disappear during editing or be averaged away, so systems distribute evidence across space and time.

The [image DCT notebook](02_image_dct.ipynb) exposes this process one stage at a time, from RGB pixels to an 8×8 block, coefficient editing, reconstruction and stress testing.

### Audio

An audio watermark changes waveform samples or time-frequency features while using perceptual masking to keep the signal difficult to hear. Speech-focused systems may also localize which time ranges contain generated audio.

The relevant channel includes resampling, codecs, background noise, filtering, time shifts and splicing. A detector trained only on clean speech is not automatically robust to music, telephone audio or heavily edited recordings.

### Text

Text has no continuous pixel or waveform space. A text watermark must usually be inserted while the model selects tokens. A secret-keyed rule labels candidate tokens or assigns them watermark scores, and the sampler slightly favors choices that carry the desired signal.

For a simple green-list construction, let:

- `n` be the number of scored tokens;
- `g` be the number assigned to the keyed green list;
- `γ` be the expected green fraction for unmarked text.

An illustrative detector uses:

```text
z = (g - γn) / sqrt(nγ(1 - γ))
```

One green token proves nothing. Detection comes from an unusual excess accumulated across many positions. Short passages provide little evidence, while paraphrase and translation replace token choices and can erase the pattern.

The [text green-list notebook](01_text_green_list.ipynb) makes the keyed mapping, probability changes, cumulative evidence and length/bias trade-off visible.

## 5. The trade-offs that shape a watermark

A watermark should be evaluated against a stated threat model rather than described as simply “robust.”

| Property | Question to test | Typical tension |
|---|---|---|
| Imperceptibility | Can people see, hear or notice the mark? | More signal energy often improves detection but harms quality |
| Robustness | Which transformations preserve detection? | Training for more transformations can reduce capacity or clean-input accuracy |
| Reliability | What are false-positive and false-negative rates at the chosen threshold? | A lower threshold finds more marked content but accuses more unmarked content |
| Capacity | Is the goal one attribution bit, a provider ID or a longer payload? | Larger payloads need more signal or redundancy |
| Localization | Can the detector identify an edited region or time span? | Local evidence is harder than one score for the whole asset |
| Security | Can an attacker remove, forge or estimate the mark? | Public detector access can help evaluation while exposing an attack oracle |
| Synchronization | Can the detector realign after crop, time shift or frame edits? | Synchronization structures consume capacity and may reveal the signal |

Robustness must always name the channel: “survives JPEG quality 50” is meaningful; “robust to editing” is not.

## 6. Provenance and watermarking work at different layers

[C2PA Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html) use signed manifests to describe who created or edited an asset and what actions were recorded.

A **hard binding** links the manifest to the exact asset or file structure. If the bytes change, validation may fail. A **soft binding** uses a fingerprint or invisible watermark to help locate the manifest after ordinary transformations or after embedded metadata is removed.

That produces a layered design:

```text
signed manifest      -> explains issuer, actions and ingredient history
hard binding         -> detects changes to the exact signed asset
watermark/fingerprint -> helps recover identity after transformation
manifest store       -> returns the detached provenance record
```

The signature establishes trust in the claim. The watermark or fingerprint helps find the claim again; it does not make the claim true by itself.

## 7. Representative approaches

The following systems illustrate different points in the design space.

| Solution or family | Medium | Core idea | What it is useful for | Main limitation |
|---|---|---|---|---|
| [C2PA Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html) | Image, video, audio, text and more | Signed manifests with hard bindings and optional soft bindings | Origin, edit history and signer claims | Metadata can be stripped; recovery needs a store or soft binding |
| [Google SynthID](https://deepmind.google/models/synthid/) | Image, video, audio and text | Provider-specific invisible signals adapted to each modality | Attribution inside participating product ecosystems | Detector and training details are provider-controlled; it is not a universal authenticity proof |
| [Stable Signature](https://arxiv.org/abs/2303.15435) | Image | Fine-tune a diffusion decoder so its outputs carry a decoder-specific signal | Mark every image emitted by a controlled model | Requires control of the generator and remains subject to post-processing and attacks |
| [AudioSeal](https://github.com/facebookresearch/audioseal) | Speech/audio | Joint watermark generator and localized detector | Detect generated speech and locate marked intervals | A speech-oriented model is not automatically suitable for music or arbitrary audio |
| [VideoSeal](https://github.com/facebookresearch/videoseal) | Image/video | Learned embedder and extractor with augmentation and temporal propagation | Open post-hoc image and video watermarking | Requires model runtime and careful codec, resize and temporal evaluation |
| LLM green-list watermarking ([SynthID Text](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/) and [Kirchenbauer et al.](https://arxiv.org/abs/2301.10226)) | Generated text | Keyed token partition or score adjustment during sampling | Statistical attribution when the generator is controlled | Short text, paraphrase, translation and distribution shift reduce detection power |

These are not interchangeable products. The medium, generator access, payload, detector ownership and expected transformations determine which family is appropriate.

## 8. How mainstream chat products map onto the concepts

Watermark keys and detectors are provider-specific. A signal from one provider is not a universal AI detector, and a chat service may attach metadata, embed a signal, do both or do neither depending on the modality, model and product version.

| Service | Text responses | Image/file outputs | Practical verification route | Meaning of a negative result |
|---|---|---|---|---|
| **ChatGPT / OpenAI** | OpenAI's official provenance documentation describes checks for images and audio, not a provider-specific watermark detector for pasted ChatGPT prose. Generic writing detectors are a separate probabilistic class. | OpenAI's Content Provenance API checks supported images for C2PA and SynthID signals and provides a browser flow. | Preserve the original image bytes, then use [OpenAI's content provenance check](https://developers.openai.com/api/docs/guides/content-provenance) or a C2PA-aware verifier. | `not_detected` does not rule out OpenAI generation: metadata may be stripped, a watermark may be degraded or the file may predate the signal. |
| **Gemini / Google** | Google says SynthID Text changes token probabilities during Gemini generation. Detection is statistical and provider-keyed and is strongest on longer, diverse passages. | Gemini Apps combine invisible SynthID and C2PA signals for generated or edited visual media. Visible labels are a separate setting. | Use Gemini's verification flow or the SynthID Detector where available. | A missing SynthID signal means “not detected by Google's signal,” not “human-made” or “not made by another provider.” |
| **Claude / Anthropic** | Anthropic announced keyed, SynthID-Text-style watermarking for future Claude models; its detection API is described as private preview for eligible organizations. | For supported files such as PNG, JPG or SVG, Anthropic says Claude attaches signed C2PA metadata. | Use Anthropic's detector when eligible; validate file credentials with a C2PA-aware tool. | Short, factual, code or lightly edited passages may lack enough watermarkable choices; credentials can also be stripped during conversion. |

These are product statements, not permanent guarantees. Record the product, model, generation date and original rendition with every result.

## 9. Detection results are evidence, not verdicts

The safest interpretation preserves both the observation and its scope.

| Observation | Defensible conclusion | Overclaim to avoid |
|---|---|---|
| Trusted C2PA credential naming a provider | That issuer signed a claim that the file was created or processed by the stated tool | The full history is true, or the current holder is the original author |
| Provider watermark detected | The detector found a signal associated with that provider in this rendition | The provider created every word or pixel |
| Provider watermark not detected | No supported signal was found by that detector in this rendition | The content is human-made or was not produced by another AI system |
| Text looks “AI-like” | A style detector produced a probabilistic clue | A watermark was found |
| Screenshot, crop, re-encode or pasted text | The evidence channel may have been damaged or removed | A negative result is meaningful evidence of absence |

The [provenance and detection guide](03_provenance_detection.md) develops this workflow with product routing, transformation scenarios, structured result examples and an investigation checklist.

## 10. Learning companion

This README is the entry point for the research. Keep this compact distinction in mind while working through the focused materials:

```text
provenance:  asset -> signed claim -> validate issuer and history
watermark:   asset -> embedded signal -> transform -> detect signal
```

The repository separates interactive mechanics from static reference material:

| Order | Resource | Learning goal | Main material |
|---|---|---|---|
| 1 | [Text green-list notebook](01_text_green_list.ipynb) | Understand keyed statistical text signals | Candidate mappings, probability shifts, generation examples, cumulative detection, power and paraphrase |
| 2 | [Image DCT notebook](02_image_dct.ipynb) | Understand frequency-domain image embedding | Eight pipeline stages, coefficient voting, visual residuals, transform tests and robustness/quality trade-offs |
| 3 | [Provenance and detection guide](03_provenance_detection.md) | Interpret evidence responsibly | Product routing, artifact workflow, edit scenarios, valid conclusions and investigation checklist |

Start with either mechanics notebook according to the medium you care about, then read the provenance guide to connect the signal to real artifact handling.

The examples are deliberately small and inspectable. They teach the pattern and trade-offs; they do not reproduce the security or performance of proprietary or research-grade systems.

## Run the notebooks

Install the environment:

```bash
cd topics/ai_watermarks
uv sync
```

Then open either focused notebook directly:

```bash
uv run jupyter notebook 01_text_green_list.ipynb
uv run jupyter notebook 02_image_dct.ipynb
```

For deterministic headless checks:

```bash
for notebook in 01_text_green_list.ipynb 02_image_dct.ipynb; do
  WATERMARKS_INTERACTIVE=0 uv run jupyter nbconvert --to notebook --execute "$notebook" \
    --output-dir /tmp --output "${notebook%.ipynb}.executed.ipynb"
done
```

## Sources

### Provenance and standards

- [C2PA Specifications 2.4 — Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html)
- [C2PA Implementation Guidance — invisible watermarking and soft bindings](https://spec.c2pa.org/specifications/specifications/2.2/guidance/Guidance.html)

### Provider documentation

- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/)
- [Google DeepMind — watermarking AI-generated text and video with SynthID](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/)
- [Google DeepMind — identifying AI-generated images with SynthID](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/)
- [Google Gemini Apps Help — verify AI-generated images, videos and audio](https://support.google.com/gemini/answer/16722517?hl=en)
- [Google Gemini Apps Help — manage visible and invisible watermark settings](https://support.google.com/gemini/answer/17405358?hl=en-GB)
- [OpenAI — content provenance guide](https://developers.openai.com/api/docs/guides/content-provenance)
- [OpenAI — content provenance API reference](https://developers.openai.com/api/reference/go/resources/content_provenance_checks/methods/create)
- [Anthropic — how Claude's text watermark works](https://www.anthropic.com/news/claude-text-watermark)
- [Anthropic Help — can Claude produce images?](https://support.anthropic.com/en/articles/9002504-can-claude-produce-images)

### Research and implementations

- [Fernandez et al. — VideoSeal: Open and Efficient Video Watermarking](https://arxiv.org/abs/2412.09492)
- [San Roman et al. — Proactive Detection of Voice Cloning with Localized Watermarking](https://arxiv.org/abs/2401.17264)
- [AudioSeal implementation](https://github.com/facebookresearch/audioseal)
- [VideoSeal implementation](https://github.com/facebookresearch/videoseal)
- [Fernandez et al. — Stable Signature](https://arxiv.org/abs/2303.15435)
- [Kirchenbauer et al. — A Watermark for Large Language Models](https://arxiv.org/abs/2301.10226)
