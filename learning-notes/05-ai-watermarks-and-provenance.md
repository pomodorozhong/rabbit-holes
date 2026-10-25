# Watermarks and provenance

**Bottom line:** An embedded watermark is a signal added to content, such as an image. Provenance is a record of that content's origin and editing history. Looking for the signal and validating a signed history provide different kinds of evidence about where a file came from.

**Detecting a watermark and validating a provenance record**

- Suppose you receive an image and want to investigate its origin. A **watermark detector** examines the image for a signal from a particular watermarking method. For example, [Stable Signature](https://arxiv.org/abs/2303.15435) trains an image generator to insert identifying bits that a matching detector can recover.
- A **provenance validator** examines a signed record, or **credential**, associated with the file. It checks the signature and the record's connection to the content. [Content Credentials](https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html), defined by the Coalition for Content Provenance and Authenticity (C2PA), can record which tools created or edited a file. A valid signature does not establish that a depicted event is true.
- A visible “AI-generated” badge can be copied or cropped. Its appearance alone does not establish a valid credential or a detected signal.

**Why editing can affect the credential and the watermark differently**

- C2PA connects the signed record to specified content using a cryptographic hash, a value computed from that content to detect changes. This is a **hard binding**. An edit can break the match, and removing metadata can separate the record from the file. [C2PA binding guidance](https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html).
- A watermark signal may survive when metadata is removed. A fingerprint or watermark can serve as an identifier for looking up the separated record. This is a **soft binding**; a recovered match still needs verification. Missing metadata therefore does not establish that an image was never signed.

**Reporting watermark detection and provenance validation**

- After examining a file, record two findings separately: whether the detector found its watermark signal and whether the validator accepted the signed credential. Keep the original file and name the tools used, so the findings refer to a specific file and method.
- A credential can validate while a watermark is not detected. Those findings answer different questions. “No watermark detected” leaves the creator unresolved; it does not establish human authorship.

**Open**

- A worked comparison of an original file and an edited copy, using a real validator, is still missing.

Companion notes: [text watermarks](05-ai-text-watermarks.md) and [image watermarks](05-ai-image-watermarks.md).
