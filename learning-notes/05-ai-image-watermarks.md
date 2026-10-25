# How image watermarks work

**Bottom line:** An image can carry a signal through small changes to its pixel values. A matching detector tries to recover that signal after the image has been saved or edited. The useful questions are which changes it survives and what image-quality cost they require.

**How the toy construction stores bits**

- The [companion notebook](experiments/05-ai-watermarks/05-ai-image-watermarks.ipynb) illustrates a frequency-domain construction: transform an 8×8 image block, compare two coefficients, and adjust their difference to represent a `0` or `1`. The detector reads that relationship back. This is an exploratory implementation that still needs a full review.
- Its message `AI` occupies 16 bits, repeated across blocks. Several blocks vote on each recovered bit. Repetition provides more observations at the cost of space for distinct message bits.

**What strength and editing change**

- The saved strength comparison shows more pixel distortion at larger coefficient margins. It plots payload recovery alongside that distortion so the two can be considered together.
- Its JPEG and crop-and-resize paths test different changes. Cropping and resizing can move the pixels assigned to each block, while this detector expects the original grid. The experiment does not establish the robustness of a provider's watermark. [Notebook setup and review limits](experiments/05-ai-watermarks/README.md).

**How a learned method differs**

- [Stable Signature](https://arxiv.org/abs/2303.15435) fine-tunes a diffusion model's decoder so generated images carry a binary signature. A trained extractor recovers it, followed by a statistical test. That is a different construction from the notebook's coefficient edits, and requires control of the generator.
- Its published evaluations belong to that method and test setup. They cannot validate this toy implementation or an unrelated product.

**Open**

- Review the notebook's transform and detector against a reference implementation, then save representative static outputs for its transformation comparisons.

For how embedded signals relate to signed file metadata, see [watermarks and provenance](05-ai-watermarks-and-provenance.md).
