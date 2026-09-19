# LLM Harnessing for PKM

This page tracks research progress on using LLM agents to harness Personal Knowledge Management (PKM). Consider creating a [GitHub Issue](https://github.com/pomodorozhong/personal-research/issues) and Project board to manage work, mirroring the [git_and_github research](../git_and_github/README.md) workflow.

## Goal

Understand how to **harness LLM agents for PKM** — not just chat about notes, but architect when synthesis happens, what the agent maintains, and how human curation + agent compilation compound over time.

The working thesis: Karpathy's **compiled wiki pattern** (synthesis at ingest time) is the dominant 2026 approach, with RAG and agent memory as complementary layers — not replacements.

## Research documents

| Topic | Document |
| --- | --- |
| Foundations & mental model | [foundations.md](./foundations.md) |
| LLM Wiki / compiled knowledge pattern | [llm_wiki_pattern.md](./llm_wiki_pattern.md) |
| Agent harness architecture | [agent_harness_architecture.md](./agent_harness_architecture.md) |
| Local models — why | [local_models_why.md](./local_models_why.md) |
| Local models — how | [local_models_how.md](./local_models_how.md) |
| Traditional PKM + LLM (plugins) | [traditional_pkm_and_llm.md](./traditional_pkm_and_llm.md) |
| MCP memory systems | [mcp_memory_systems.md](./mcp_memory_systems.md) |
| Decision framework (ingest vs query time) | [decision_framework.md](./decision_framework.md) |
| Scaling path & failure modes | [scaling_and_failure_modes.md](./scaling_and_failure_modes.md) |
| Mapping to this repo | [repo_mapping.md](./repo_mapping.md) |
| Tool landscape comparison | [tool_landscape.md](./tool_landscape.md) |
| Bibliography | [bibliography.md](./bibliography.md) |

## Guides & demos

| Guide | Document |
| --- | --- |
| Obsidian setup (step-by-step) | [obsidian_setup_guide.md](./obsidian_setup_guide.md) |
| Harness POC (Jupyter + uv) | [poc/harness_poc.ipynb](./poc/harness_poc.ipynb) · [poc/README.md](./poc/README.md) — Ollama ingest, embed, query |

## Roadmaps

### Roadmap A — Conceptual foundations

-   [x] PKM vs RAG vs Wiki vs Memory taxonomy → [foundations.md](./foundations.md)
-   [x] Karpathy LLM Wiki pattern deep read → [llm_wiki_pattern.md](./llm_wiki_pattern.md)
-   [x] Synthesis-time vs query-time framework → [decision_framework.md](./decision_framework.md)

### Roadmap B — Tool evaluation

-   [x] Obsidian plugin stack (Smart Connections, Copilot) → [traditional_pkm_and_llm.md](./traditional_pkm_and_llm.md)
-   [x] Local model usage in harness stack → [local_models_how.md](./local_models_how.md)
-   [x] Local model effectiveness & cost analysis → [local_models_why.md](./local_models_why.md)
-   [x] Agent skill frameworks (logseq-wiki, agent-based-km) → [agent_harness_architecture.md](./agent_harness_architecture.md)
-   [x] MCP memory servers (Slipbox, agent-knowledge) → [mcp_memory_systems.md](./mcp_memory_systems.md)

### Roadmap C — Practical harness design

-   [x] Schema file design (`AGENTS.md` conventions) → [obsidian_setup_guide.md](./obsidian_setup_guide.md)
-   [x] Ingest / query / lint workflow specification → [poc/harness_poc.ipynb](./poc/harness_poc.ipynb)
-   [ ] Scaling triggers (when to add qmd/search) → [scaling_and_failure_modes.md](./scaling_and_failure_modes.md)

### Roadmap D — Application to personal-research repo

-   [ ] Prototype `AGENTS.md` for this repo → [repo_mapping.md](./repo_mapping.md)
-   [ ] Cross-topic `index.md`
-   [ ] Pilot: compile this LLM-PKM research into wiki format
