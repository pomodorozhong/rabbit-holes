# How text watermarks work

**Bottom line:** A text watermark creates a statistical pattern in a model's choices of **tokens**, the text units it generates. A matching detector later looks for that pattern across a passage. The words can look ordinary while their selection carries a signal.

**Favoring a group of tokens while generating text**

- When choosing the next token, a model assigns probabilities to possible continuations. In [Kirchenbauer et al.'s green-list construction](https://arxiv.org/abs/2301.10226), a reproducible rule selects a group of candidates called the **green list**, and the generation procedure slightly increases their probabilities. A token need not be a whole word.
- Tokens outside the green list can still be selected. Embedding this watermark requires access to the generation process, where the preference can influence token selection.

**Detecting an excess of green-list choices in a passage**

- The detector reconstructs the green lists for the passage and counts how often the chosen tokens belong to them. It asks whether that count is unusually high compared with text generated without the preference. The [authors' implementation](https://github.com/jwkirchenbauer/lm-watermarking) includes this statistical test.
- A few green choices can occur by chance. Passage length, available choices, and detection settings affect the evidence. A **false positive** is unmarked text flagged as watermarked; how often this happens needs measuring on representative unmarked text.

**How rewriting affects watermark detection**

- A paraphrase can preserve a passage's meaning while replacing, inserting, or deleting tokens. That changes the sequence examined by the watermark detector and can weaken the statistical pattern it is looking for. The effect depends on the scheme and the edit; the [authors' implementation](https://github.com/jwkirchenbauer/lm-watermarking) discusses these trade-offs.

**The text notebook's simplified version**

- The [toy notebook](experiments/05-ai-watermarks/05-ai-text-watermarks.ipynb) uses a small vocabulary and position-based lists to illustrate probability bias and evidence accumulation. It does not run a language model or reproduce a provider's watermark. [Setup and review limits](experiments/05-ai-watermarks/README.md).
- Its paraphrase section encounters words outside the toy vocabulary, so that section does not demonstrate a measured loss of detection after rewriting.

**Open**

- Compare detection before and after an edit using a shared vocabulary, and check the detector on independent unmarked passages.

For interpreting results alongside file credentials, see [watermarks and provenance](05-ai-watermarks-and-provenance.md).
