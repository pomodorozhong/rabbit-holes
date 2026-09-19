# Bibliography

Back to [research index](./README.md)

## Primary sources

- [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the foundational pattern document
- [Glukhov: PKM vs RAG vs Wiki vs Memory](https://www.glukhov.org/knowledge-management/foundations/pkm-vs-rag-vs-wiki-vs-memory-systems/) — taxonomy and mental model
- [Ranjan Kumar: Synthesis-Time Decision](https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory) — when to compile vs retrieve

## Implementations

- [microsoft/llmwiki](https://github.com/microsoft/llmwiki) — VS Code extension + MCP
- [daje0601/Obsidian-RAG](https://github.com/daje0601/Obsidian-RAG) — minimal Obsidian + Claude Code
- [clonn/obsidian_plugin_LLM-Wiki](https://github.com/clonn/obsidian_plugin_LLM-Wiki) — Obsidian plugin + CLI
- [ystreibel/logseq-wiki](https://github.com/ystreibel/logseq-wiki) — Logseq skill framework
- [arturseo-geo/llm-knowledge-base](https://github.com/arturseo-geo/llm-knowledge-base) — formalized schema + learning layer
- [philippsied/agent-based-knowledge-management](https://github.com/philippsied/agent-based-knowledge-management) — 15 Claude skills for Obsidian

## MCP memory and Zettelkasten

- [jamesfishwick/slipbox-mcp](https://github.com/jamesfishwick/zettelkasten-mcp) — Zettelkasten MCP server
- [yucx-go/agent-knowledge](https://github.com/yucx-go/agent-knowledge) — claim/evidence memory MCP
- [Sathvik-1007/GraphMem-MCP](https://github.com/Sathvik-1007/graphmem-mcp) — knowledge graph MCP
- [dnotitia/AKB](https://github.com/dnotitia/AKB) — Git-backed agent knowledgebase

## Practitioner write-ups

- [Built a Self-Maintaining Personal Wiki (Wenjie Xu)](https://blog.wenjiexu.site/en/posts/llm-personal-wiki/) — skills-based workflow in production
- [Obsidian + AI plugin comparison (Code Culture)](https://codeculture.store/blogs/developer-culture/obsidian-ai-plugin-comparison-2025) — Smart Connections vs Copilot vs Claude Code
- [Karpathy LLM Wiki: compile knowledge (Z Engineer)](https://zengineer.blog/blog/tech/karpathy-llm-wiki-compile-knowledge-en/) — compiler analogy and scale limits
- [Obsidian Was Never the Problem (Drink Your OJ)](https://drinkyouroj.substack.com/p/obsidian-was-never-the-problem) — PKM tool vs agent maintenance bottleneck

## Search tooling

- [qmd](https://github.com/tobi/qmd) — local hybrid search for markdown (BM25 + vector + LLM rerank, MCP server)

## Local models

- [Why use local models](./local_models_why.md) — effectiveness, cost, comparisons
- [How to use local models](./local_models_how.md) — Ollama stack, integration, configuration
- [Obsidian Local AI 2026 (Local AI Master)](https://localaimaster.com/blog/local-ai-obsidian-integration) — Ollama + Obsidian plugin setup
