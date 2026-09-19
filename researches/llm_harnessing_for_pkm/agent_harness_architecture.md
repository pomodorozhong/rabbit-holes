# Agent Harness Architecture

Back to [research index](./README.md)

"Harnessing" means **constraining and operationalizing** the LLM for PKM — not just prompting it ad hoc.

## Harness components

| Component | Purpose | Examples |
| --- | --- | --- |
| **Schema / rules file** | Persistent agent instructions across sessions | `AGENTS.md`, `CLAUDE.md` |
| **Skills / commands** | Executable workflow modules with triggers and steps | `.claude/skills/`, `/ingest`, `/lint`, `/save` |
| **MCP servers** | Standardized tool protocol for search, graph, memory | qmd MCP, Slipbox, GraphMem, AKB |
| **Deterministic scripts** | Token-efficient routing, validation, ingest pipelines | Python routers (community pattern from gist comments) |
| **Subagents** | Isolate search from synthesis to preserve context window | Main agent orchestrates; subagent retrieves |

The schema file is the most critical piece. A vague schema produces vague wiki pages. A schema that defines page formats, contradiction handling, and when to split vs extend a page produces a wiki you can rely on.

## Skills pattern

Practitioners encode workflows as skill modules rather than repeating instructions each session. Each skill typically includes:

- Trigger conditions (when to run)
- Execution steps
- Output formats
- Edge case handling
- Reference templates in a `reference/` directory

Example from [Wenjie Xu's LLM personal wiki](https://blog.wenjiexu.site/en/posts/llm-personal-wiki/):

- `syncing-wiki` — daily entry point; composes detection + ingestion
- `detecting-resources-sync` — find new files in `raw/`
- `ingesting-resources` — process a source into wiki pages
- `querying-wiki` — answer from compiled knowledge
- `checking-wiki-health` — lint pass

Skills should be **composable**: run standalone or embedded in larger flows. Query results can be answered or backfilled as new wiki pages.

## Token economics

A recurring pain point (from gist comment threads): token burn comes not from reasoning but from **repeated context loading** — the agent re-reads `AGENTS.md`, `index.md`, manifests, and raw sources across short sessions.

Mitigations:

1. **Deterministic scripts** for intake, routing, validation — reserve the LLM for synthesis and judgment
2. **Compact routing files** instead of scanning the whole wiki
3. **Subagents for search** — main agent context reserved for orchestration
4. **Hot cache** — a small `hot.md` summarizing recent context ([agent-based-knowledge-management](https://github.com/philippsied/agent-based-knowledge-management))

## Reference implementations

| Project | Platform | Notes |
| --- | --- | --- |
| [microsoft/llmwiki](https://github.com/microsoft/llmwiki) | VS Code / Cursor | Extension with tree views, `@wiki` chat participant, MCP server, bulk ingest |
| [ystreibel/logseq-wiki](https://github.com/ystreibel/logseq-wiki) | Logseq | Skill-based framework; ingest → extract → resolve → evolve |
| [clonn/obsidian_plugin_LLM-Wiki](https://github.com/clonn/obsidian_plugin_LLM-Wiki) | Obsidian | Plugin + Python CLI; queue-based prompt bundles for Claude Code |
| [daje0601/Obsidian-RAG](https://github.com/daje0601/Obsidian-RAG) | Obsidian + Claude Code | Minimal: no vector DB; agent reads files directly via index hierarchy |
| [philippsied/agent-based-knowledge-management](https://github.com/philippsied/agent-based-knowledge-management) | Obsidian + Claude Code | 15 skills; contradiction callouts, 8-category lint, autoresearch loop |
| [arturseo-geo/llm-knowledge-base](https://github.com/arturseo-geo/llm-knowledge-base) | Tool-agnostic | Formalized schema + learning layer (FSRS flashcards, gap tracking, contamination mitigation) |
| [jamesfishwick/slipbox-mcp](https://github.com/jamesfishwick/zettelkasten-mcp) | MCP (any agent) | Zettelkasten-native; 19 tools, typed links, cluster detection |

## Related

- [Why use local models](./local_models_why.md)
- [How to use local models](./local_models_how.md)
- [LLM Wiki pattern](./llm_wiki_pattern.md)
- [Obsidian setup guide](./obsidian_setup_guide.md)
- [Harness POC](./poc/harness_poc.ipynb)
- [Scaling & failure modes](./scaling_and_failure_modes.md)
