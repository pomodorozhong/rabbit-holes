# POC fixture data

Sample raw sources for [`harness_poc.ipynb`](../harness_poc.ipynb). These mimic clipped articles dropped into a vault's `raw/` folder.

The notebook copies `fixtures/raw/` into `sample_vault/raw/` on each run, then ingests each file via Ollama.

Topics are **D&D trivia** — deliberately unrelated to PKM/LLM research so ingest output is easy to distinguish from the research docs.

| File | Topic |
| --- | --- |
| `chromatic-dragons.md` | The five chromatic dragon types |
| `cantrips-and-spell-slots.md` | 1st-level casting basics |
| `famous-taverns.md` | Iconic inns and taverns across the multiverse |
