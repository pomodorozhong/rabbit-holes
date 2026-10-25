# AI watermark toy experiments

These notebooks accompany the notes on [text watermarks](../../05-ai-text-watermarks.md) and [image watermarks](../../05-ai-image-watermarks.md). They were retained from earlier research for [issue #115](https://github.com/pomodorozhong/rabbit-holes/issues/115). They use synthetic examples and still need a full implementation and presentation review before promotion to `topics/`.

- [Text green-list notebook](01_text_green_list.ipynb) explores keyed token choices, probability bias, and evidence accumulation. Its position-based toy lists do not reproduce a provider's watermark. The paraphrase section encounters words outside its vocabulary and does not measure a before-and-after detection result.
- [Image notebook](02_image_dct.ipynb) explores coefficient edits, payload recovery, and transformations. Its transform and detector still need checking against a reference implementation; its results do not establish production watermark performance.

Several saved figures are widget views without embedded static fallbacks or saved widget state. Run the notebooks locally to inspect those parts. From the repository root:

```bash
cd learning-notes/experiments/05-ai-watermarks
uv sync
uv run jupyter notebook
```

Both notebooks accept `WATERMARKS_INTERACTIVE=0` for static execution. The current fallback shows default parameter choices; it does not save a complete comparison of every interactive setting.
