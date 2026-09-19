# Traditional PKM + LLM (Plugin / RAG-in-Vault)

Back to [research index](./README.md)

For users who keep **human-written notes** and add AI on top, the 2026 Obsidian landscape offers a mature plugin stack. Users typically pair two or more specialized plugins.

## Obsidian AI plugin landscape (2026)

| Plugin | Role | RAG | Local LLM | Model |
| --- | --- | --- | --- | --- |
| [Smart Connections](https://smartconnections.app/) | Semantic search, related-notes sidebar | Yes | Local embeddings by default | Free core; optional Pro |
| [Copilot for Obsidian](https://github.com/logancyang/obsidian-copilot) | Vault QA chat, agents | Yes (Vault QA) | Ollama, LM Studio | BYOK free; Plus ~$15/mo |
| [Smart Composer](https://github.com/glowingjade/obsidian-smart-composer) | Cursor-style in-note editing | Yes | Ollama, LM Studio | Open source, BYOK |
| [Text Generator](https://github.com/nhaouari/obsidian-textgenerator-plugin) | Template-driven generation | No | Ollama, multi-provider | Open source, BYOK |
| [Companion](https://github.com/rizerphe/obsidian-companion) | Ghost text autocompletion | No | Ollama, OpenAI | Open source, BYOK |

**Recommended combo for most users:** Smart Connections (embedding/search layer) + Copilot (chat layer), both pointed at a local [Ollama](https://ollama.com/) backend for privacy. See [how to use local models](./local_models_how.md) for setup and [why](./local_models_why.md) for tradeoffs.

- Embeddings: `nomic-embed-text` or `mxbai-embed-large`
- Chat: `llama3.2` or similar via `http://localhost:11434/v1`

## Plugin RAG vs compiled wiki

| Dimension | Plugin RAG (Obsidian stack) | Compiled Wiki (Karpathy pattern) |
| --- | --- | --- |
| Who writes notes | You | LLM (you curate sources) |
| When synthesis happens | Query time | Ingest time |
| Knowledge accumulation | Stateless per query | Compounds over time |
| Cross-references | Discovered ad hoc | Pre-built and maintained |
| Contradictions | May go unnoticed | Flagged during ingest/lint |
| Best for | Existing vaults, daily journaling | Research deep-dives, source corpora |

These are not mutually exclusive. You can maintain human-written daily notes in Obsidian while using an agent to compile a `wiki/` layer from `raw/` sources.

## Other PKM tools

- **Logseq** — [logseq-wiki](https://github.com/ystreibel/logseq-wiki) adapts the Karpathy pattern with block-based pages and namespace conventions
- **Notion / cloud PKM** — typically rely on API-connected agents or copy-export to markdown for agent workflows; less local-first
- **Plain markdown in Git** — natural fit for agent harnessing; version history and collaboration are free (this repo is an example)

## Related

- [Why use local models](./local_models_why.md)
- [How to use local models](./local_models_how.md)
- [Obsidian setup guide](./obsidian_setup_guide.md)
- [LLM Wiki pattern](./llm_wiki_pattern.md)
- [Tool landscape comparison](./tool_landscape.md)
