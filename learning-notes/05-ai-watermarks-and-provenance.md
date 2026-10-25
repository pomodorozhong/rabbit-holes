# Watermarks and provenance

**Bottom line:** An embedded watermark carries a detectable signal in the content. Signed provenance records claims about its origin and history. Each check provides evidence with a particular scope; neither gives a universal verdict about human or AI authorship.

**What each check answers**

- A watermark detector looks for the signal that its matching embedder was designed to leave. For example, [Stable Signature](https://arxiv.org/abs/2303.15435) trains an image generator's decoder to carry a binary signature that an extractor can recover.
- A signed provenance record identifies a signer and records assertions about an asset. [C2PA Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html) let a validator check the credential and its binding to the content. The signature does not establish that the depicted event is true.
- A visible badge can be copied or cropped. Its appearance alone does not establish a valid credential or a detected signal.

**Why a credential and a watermark can behave differently**

- A C2PA **hard binding** uses cryptographic hashes to bind a manifest to specified content. A **soft binding**, such as a fingerprint or invisible watermark, can help find the manifest after a transformation or metadata removal. A recovered match still needs verification. [C2PA binding guidance](https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html).
- Missing metadata therefore does not establish that an image was never signed. Likewise, a detector's failure to find its signal does not identify who created the content.

**What to keep in a result**

- Keep the original file and record its source and any edits. Report provenance validation and watermark detection separately, with the validator or detector used.
- Describe the observation narrowly: “this credential validated” or “this detector found no supported signal in this file.” The second statement leaves the origin unresolved.

**Open**

- A worked comparison of an original file and an edited copy, using a real validator, is still missing.

Companion notes: [text watermarks](05-ai-text-watermarks.md) and [image watermarks](05-ai-image-watermarks.md).
