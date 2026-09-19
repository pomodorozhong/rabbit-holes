# MCP Memory Systems

Back to [research index](./README.md)

Agent memory is **separate from PKM content**. Memory systems give agents persistent context across sessions — preferences, decisions, episodic facts — whereas PKM/wiki stores domain knowledge you can read and audit.

## Systems overview

| System | Approach | PKM relevance |
| --- | --- | --- |
| [agent-knowledge](https://github.com/yucx-go/agent-knowledge) | Claim/evidence compilation, BM25 + graph, no vectors | Drop-in memory MCP for Claude Code / Cursor / Codex |
| [GraphMem-MCP](https://github.com/Sathvik-1007/graphmem-mcp) | Knowledge graph + semantic search, 28 tools | Per-project entity/decision memory for coding agents |
| [AKB](https://github.com/dnotitia/AKB) | Git-backed vault, hybrid search, URI graph | Team/org knowledge served over MCP |
| [Slipbox MCP](https://github.com/jamesfishwick/zettelkasten-mcp) | Zettelkasten-native, typed links, cluster detection | Active Zettelkasten partner with workflow prompts |

## Memory vs compiled wiki: when to use which

**Use a compiled wiki when:**

- Knowledge is domain content you want to read, browse, and link (research topics, book notes, competitive analysis)
- You need human-auditable markdown with git history
- Cross-references and synthesis across sources matter

**Use agent memory when:**

- The agent needs to remember *how you work* (preferences, past decisions, project context)
- Continuity across coding or research sessions matters
- Facts are agent-specific and should not pollute your readable wiki

**Use both (recommended):**

- Wiki = what you know about the world
- Memory = what the agent knows about working with you

Do not let memory replace a wiki. Memory lacks the structure, lint loop, and human readability that make PKM useful.

## Related

- [Foundations](./foundations.md)
- [Agent harness architecture](./agent_harness_architecture.md)
- [Decision framework](./decision_framework.md)
