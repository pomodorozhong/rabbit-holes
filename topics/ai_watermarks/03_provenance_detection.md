# Learning provenance and detection: reason from evidence

The mechanics notebooks show how a signal is embedded and detected. This guide takes the next step: it connects those signals to real artifacts and asks what each observation allows you to conclude.

Read it as an evidence guide rather than a detector recipe. It begins by separating three evidence channels, then moves through product routing, artifact handling, transformation effects and result interpretation. Product details can change with model and release, so every investigation should record the product, model, generation date and original bytes.

## How to use this guide

Work through the sections in order:

1. Identify which evidence channel you actually have.
2. Route the artifact to a verifier that matches its provider and modality.
3. Preserve the original before running checks.
4. Account for transformations that may have damaged the evidence.
5. Translate the observation into a conclusion without exceeding its scope.

## 1. Start by separating the evidence channels

| Channel | Question answered | What it does not establish |
|---|---|---|
| Signed provenance | Did a recognized issuer sign a claim about this file and its history? | That the entire asserted history is true, or that the current holder is the author |
| Provider watermark | Did a provider-specific detector find its signal in this rendition? | That the provider created every word or pixel, or that an undetected asset is human-made |
| Generic AI detector | Does the content resemble examples in the detector's calibration or training data? | A watermark, provenance, authorship or reliable provider attribution |

These channels are complementary, not interchangeable. Keeping them separate is the foundation for everything that follows: a signature validates a claim, a keyed detector recognizes a signal, and a generic classifier estimates resemblance. A missing signal can mean stripping, editing, unsupported media, a changed product version or a genuinely unmarked asset.

## 2. Route the artifact to the matching verifier

Use this as a routing table, not as a universal AI detector. The detailed product statements and source links are maintained in the [README](README.md#8-how-mainstream-chat-products-map-onto-the-concepts).

| Product | Text path | Image/file path | Verification route |
|---|---|---|---|
| **ChatGPT / OpenAI** | No provider-specific watermark detector for pasted ChatGPT prose is described in the official path | Supported images can be checked for C2PA and SynthID signals | [OpenAI Content Provenance API](https://developers.openai.com/api/docs/guides/content-provenance) or [browser verifier](https://openai.com/verify) |
| **Gemini / Google** | SynthID Text detection is provider-keyed and statistical | Gemini media can carry SynthID and C2PA signals; visible labels are separate | Gemini verification flow or the [SynthID Detector](https://deepmind.google/technologies/synthid/) where available |
| **Claude / Anthropic** | Provider detector access depends on eligibility | Supported generated files can contain signed C2PA metadata | Eligible Anthropic detector for text; a C2PA-aware validator for files |

The route must match both product and modality. A generic writing detector cannot recover a provider's secret key, and an image verifier cannot answer whether pasted prose came from a chat model. Treat the table as a routing map, then check the linked product documentation for current scope and availability.

## 3. Preserve evidence before detecting

Detection begins with artifact handling, not with an API call. Follow these stages in order because later checks become less meaningful if the file was changed before the original rendition was preserved.

| Stage | Action | Establishes | Common mistake |
|---|---|---|---|
| 1. Preserve bytes | Keep the original file; compute a hash; record MIME type, dimensions, product, model and timestamp | Which exact rendition was examined | Starting from a screenshot, copy-paste or social-media download |
| 2. Separate visible labels | Record logos, “AI” labels and UI settings separately | A product or presentation policy was visible | Treating a visible label as proof of an invisible signal |
| 3. Validate provenance | Inspect C2PA signature, issuer, validation state, hard binding, actions and ingredient history | A signed issuer claim about creation or processing | Treating present-but-invalid metadata as trusted provenance |
| 4. Run the provider detector | Use the provider-specific detector on the same original rendition | Whether that detector recognized its signal in that rendition | Using a generic detector or a different transformed copy |
| 5. Report a scoped result | Record `trusted provenance`, `watermark detected`, `not detected` or `inconclusive`, with detector/version and scope | A reproducible, calibrated observation | Collapsing every result into “AI” or “human” |

## 4. Learn what transformations change

Every evidence layer has a different failure mode. The scenarios below help build intuition for those differences, but they are not universal performance guarantees. A real result depends on the signal, detector version, transformation severity and calibration set.

| Rendition or edit | C2PA credential | Provider watermark | Generic AI detector | What the pattern means |
|---|---|---|---|---|
| Original file | Valid, if correctly signed | Detected, if the provider signal is present | Uncertain | Best evidence path: preserve and verify the original bytes |
| Metadata stripped | Missing | May still be detected | Uncertain | Removing the manifest does not necessarily remove a surviving signal |
| JPEG re-encode | Invalid or missing hard binding | Possibly detected | Uncertain | Compression may preserve a robust signal while breaking a file binding |
| Crop and resize | Invalid or missing | Possibly not detected by a simple detector | Uncertain | Geometry changes can break synchronization even when the source was marked |
| Screenshot of text | Not applicable or missing | Not detected for the original token-level signal | Uncertain | Copying a visual rendition can remove metadata and text-token evidence |
| Paraphrased text | Not applicable | Possibly not detected | Uncertain | Meaning can remain while the keyed token sequence changes |

The key distinction is between absence of evidence and evidence of absence. `not_detected` means only that a supported signal was not found in this rendition by this detector. It does not reconstruct what happened before the artifact was transformed.

## 5. Translate observations into scoped claims

The detector output is an observation; the conclusion is an interpretation. Use the middle column as the stopping point unless independent evidence supports a stronger claim.

| Observation | Defensible conclusion | Overclaim to avoid |
|---|---|---|
| Valid C2PA credential naming a provider | That issuer signed a claim that the file was created or processed by the stated tool | The entire file history is true, or the current holder is the original author |
| Provider watermark detected | The provider detector recognized a signal associated with that provider | The provider wrote every word or pixel |
| Provider watermark not detected | No supported signal was found in this rendition | It was human-made or was not produced by another AI system |
| Text looks “AI-like” | A style detector produced a probabilistic clue | A watermark was found |
| Metadata is absent | No readable manifest is present in this rendition | No provenance exists |
| Screenshot, crop, re-encode or pasted text | The evidence channel may have been damaged or removed | A negative result is strong evidence of absence |

## 6. Keep independent results separate

For an image check, C2PA and a provider watermark are independent observations. Preserve them as separate fields rather than collapsing them into one `AI` or `human` label:

```json
{
  "artifact_sha256": "hash-the-original-bytes",
  "c2pa": {
    "outcome": "detected",
    "issuer": "example provider",
    "validation_state": "valid"
  },
  "synthid": {
    "outcome": "not_detected"
  },
  "scope": "supported image rendition only"
}
```

Read the fields independently. In this example, one trusted signed claim is present while the separate watermark was not detected. That combination is not contradictory, and it is not a universal statement about authorship or the complete file history.

## 7. Apply the investigation checklist

- Preserve the original bytes and calculate a cryptographic hash before conversion or upload.
- Record product, model, generation date, MIME type, dimensions and every transformation applied.
- Check visible labels separately from cryptographic provenance and embedded signals.
- Validate C2PA with a C2PA-aware viewer or validator; an EXIF dump is not enough.
- Use the provider's detector for the matching modality and rendition.
- Keep positive, negative and inconclusive results scoped to the detector and version used.
- Treat a generic AI detector as weak secondary evidence, never as proof of a watermark or authorship.

The habit to carry forward is simple: preserve the rendition, identify the evidence channel, use the matching verifier and report only what the result supports.

## Sources

- [C2PA Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html)
- [OpenAI content provenance guide](https://developers.openai.com/api/docs/guides/content-provenance)
- [Google SynthID](https://deepmind.google/models/synthid/)
- [Anthropic: how Claude's text watermark works](https://www.anthropic.com/news/claude-text-watermark)
