# LLM PKM Harness POC

End-to-end proof of concept for the compiled-wiki harness pattern using **real Ollama LLM and embedding calls** — ingest extraction, semantic retrieval, and answer synthesis.

All implementation lives in [`harness_poc.ipynb`](./harness_poc.ipynb) (no separate Python module).

## Prerequisites

1. [Ollama](https://ollama.com/) installed and running (`ollama serve`)
2. Models pulled:

```bash
ollama pull nomic-embed-text   # embeddings
ollama pull qwen2.5:7b         # chat / ingest extraction (or llama3.2)
```

## Setup

```bash
cd researches/llm_harnessing_for_pkm/poc
uv sync
```

## Run

```bash
uv run jupyter notebook harness_poc.ipynb
```

Run all cells top to bottom. The notebook copies fixture sources from `fixtures/raw/` into `sample_vault/raw/`, ingests each via LLM, indexes embeddings, queries semantically, and lints the wiki.

## Fixture data

Sample raw sources live in [`fixtures/raw/`](fixtures/raw/) — **D&D trivia**, kept separate from PKM research topics:

| File | Topic |
| --- | --- |
| `chromatic-dragons.md` | The five chromatic dragon types |
| `cantrips-and-spell-slots.md` | Cantrips vs spell slots in 5e |
| `famous-taverns.md` | Iconic taverns across settings |

Add your own `.md` files to `fixtures/raw/` to test additional ingests.

## What the notebook implements

| Step | Mechanism |
| --- | --- |
| **Ingest** | Ollama chat → JSON extraction → wiki pages + `index.md` + `log.md` |
| **Embed** | Ollama `nomic-embed-text` → cached vectors in `.embeddings.json` |
| **Query** | Cosine similarity over embeddings → Ollama chat synthesis with citations |
| **Lint** | Deterministic wikilink / index checks (no model) |

See also: [Research index](../README.md) | [How to use local models](../local_models_how.md)
