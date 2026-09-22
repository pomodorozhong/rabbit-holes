# OCR Model Comparison: RapidOCR vs. TrOCR

This topic extends [issue #80](https://github.com/pomodorozhong/personal-research/issues/80) with a reproducible comparison between:

- **RapidOCR** — a compact OCR pipeline backed by bundled PP-OCR ONNX models.
- **Microsoft TrOCR Small Printed** — an end-to-end image-Transformer/text-Transformer model that autoregressively generates text. It is “LLM-adjacent,” not a general-purpose LLM.

The notebook creates a small synthetic corpus of single-line English images, applies blur, low contrast, rotation, and noise, then compares strict and case-folded character/word error rates plus warm inference latency. Reporting both error-rate variants separates formatting fidelity from transcription content. The experiment uses line crops because the TrOCR checkpoint is a recognizer, not a page-layout or text-detection system.

## Install and run with uv

Create the complete Python environment, including RapidOCR, its bundled OCR models, ONNX Runtime, PyTorch, and Transformers:

```bash
cd researches/ocr
uv sync --locked
uv run rapidocr check
uv run jupyter notebook ocr_model_comparison.ipynb
```

No Homebrew or `apt` OCR package is required. RapidOCR ships its small PP-OCR models in the Python wheel. TrOCR's code dependencies are also locked and installed by `uv`; its Hugging Face checkpoint is model data rather than a Python package. The notebook downloads and caches it automatically on first use. To fetch and verify it ahead of time, still through the `uv` environment, run:

```bash
uv run python -c "from transformers import TrOCRProcessor, VisionEncoderDecoderModel; m='microsoft/trocr-small-printed'; TrOCRProcessor.from_pretrained(m, use_fast=False); VisionEncoderDecoderModel.from_pretrained(m); print('TrOCR ready')"
```

Or execute the notebook headlessly:

```bash
uv run jupyter nbconvert --to notebook --execute ocr_model_comparison.ipynb --inplace \
  --ExecutePreprocessor.timeout=900
```

The prefetch command or first notebook run downloads the `microsoft/trocr-small-printed` checkpoint (about 61 million parameters), so it needs internet access and takes longer than later runs. Later runs use the Hugging Face cache.

## What the comparison can and cannot say

It can show how two recognition approaches behave on exactly the same controlled line images. It cannot establish production accuracy: the corpus is tiny and synthetic, and both arms are deliberately used as recognizers on pre-cropped lines rather than as page-layout systems.

## Sources

- [Issue #80: to practice Optical Character Recognition](https://github.com/pomodorozhong/personal-research/issues/80)
- [RapidOCR installation guide](https://rapidai.github.io/RapidOCRDocs/main/en/install_usage/rapidocr/install/)
- [RapidOCR usage guide](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr/usage/)
- [TrOCR paper](https://arxiv.org/abs/2109.10282)
- [`microsoft/trocr-small-printed` model card](https://huggingface.co/microsoft/trocr-small-printed)
- [Hugging Face vision encoder-decoder documentation](https://huggingface.co/docs/transformers/model_doc/vision-encoder-decoder)
