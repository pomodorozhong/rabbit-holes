# How image watermarks work

**Bottom line:** An image can carry a signal through small changes to its pixel values. A matching detector tries to recover that signal after the image has been saved or edited. The useful questions are which changes it survives and what image-quality cost they require.

**Following a short message into image blocks**

- The [companion notebook](experiments/05-ai-watermarks/05-ai-image-watermarks.ipynb) turns the message `AI` into 16 **bits**, binary digits that are each `0` or `1`. This hidden message is the watermark's **payload**. The program splits an image into 8×8 blocks and distributes the bits across them.
- It transforms each block's pixel brightnesses into **coefficients**, numbers intended to describe patterns of brightness variation. To store a bit, it adjusts two coefficients so their difference is positive for `1` and negative for `0`. The detector reads that sign back.
- The same bits are repeated across blocks, which vote on each recovered bit. Repetition provides more observations at the cost of space for distinct message bits. This exploratory implementation still needs a full review.

**How embedding strength affects image distortion**

- **Embedding strength** controls how strongly the program alters the image to store the bits. In this notebook, it sets the minimum gap between the two coefficients. A larger required gap can require a larger change to the original block.
- The notebook's final saved figure plots the fraction of message bits recovered correctly alongside the average size of changes to pixel values. Larger strength settings produce more numerical distortion in that comparison; this measurement does not establish how noticeable the changes are to a viewer.

**How compression and cropping affect message recovery**

- JPEG compression can change the coefficient values that carry the bits. Cropping and resizing can also move pixels between blocks, while this detector expects the original grid. The notebook explores both kinds of change; it does not establish the robustness of a provider's watermark. [Notebook setup and review limits](experiments/05-ai-watermarks/README.md).

**Stable Signature trains the generator to embed a watermark**

- [Stable Signature](https://arxiv.org/abs/2303.15435) uses additional training to make an image generator's output contain an identifying binary signature. A matching trained extractor recovers the signature, followed by a statistical test. The notebook instead specifies its coefficient edits directly in code.
- This method requires control of the generator. Its published evaluations apply to that method and test setup; they cannot validate the notebook's coefficient-editing implementation.

**Open**

- Review the notebook's transform and detector against a reference implementation, then save representative static outputs for its transformation comparisons.

For how embedded signals relate to signed file metadata, see [watermarks and provenance](05-ai-watermarks-and-provenance.md).
