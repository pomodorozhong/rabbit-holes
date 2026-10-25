# How text watermarks work

**Bottom line:** A text watermark can slightly favor certain ordinary tokens during generation. A matching detector looks for an unusual excess of those choices across a passage. The signal is statistical, rather than a hidden character added to every response.

**What changes during generation**

- In [Kirchenbauer et al.'s green-list construction](https://arxiv.org/abs/2301.10226), a seeded rule partitions candidate tokens into groups and the sampler gives green candidates a probability advantage. A token is a unit of text handled by the model; it need not be a whole word.
- The preference leaves room for other tokens to win. It works through the choices available to the generator, so it needs access to the generation process.

**How detection works**

- The detector reconstructs the green lists and compares the observed green count with its chance expectation. One green token says little; a sustained excess across enough tokens can provide evidence. The [paper and implementation](https://github.com/jwkirchenbauer/lm-watermarking) describe the statistical test.
- Length, available token choices, and detection settings affect the result. A threshold from one toy simulation does not establish a false-positive rate for arbitrary human text.

**Why rewriting matters**

- Replacing, inserting, or deleting tokens changes the sequence the detector examines. The effect depends on the watermark scheme and the edit; the [authors' implementation](https://github.com/jwkirchenbauer/lm-watermarking) discusses seeding, robustness, and the limits of short or predictable text.

**Companion experiment**

- The [toy notebook](experiments/05-ai-watermarks/05-ai-text-watermarks.ipynb) uses a small vocabulary and position-based lists to illustrate probability bias and evidence accumulation. It does not run a language model or reproduce a provider's watermark. [Setup and review limits](experiments/05-ai-watermarks/README.md).
- Its paraphrase section encounters words outside the toy vocabulary, so that section does not demonstrate a measured loss of detection after rewriting.

**Open**

- Compare detection before and after an edit using a shared vocabulary, and check the detector on independent unmarked passages.

For interpreting results alongside file credentials, see [watermarks and provenance](05-ai-watermarks-and-provenance.md).
