# Tool Landscape Comparison

Back to [research index](./README.md)

## Comparison matrix

| Approach | Setup cost | Privacy | Compounding | Human effort | Best for |
| --- | --- | --- | --- | --- | --- |
| NotebookLM / ChatGPT uploads | Low | Cloud | Low | Low | Quick exploration |
| Obsidian + Smart Connections + Copilot | Medium | Local option | Medium | Medium (you write notes) | Existing Obsidian users |
| Karpathy LLM Wiki + Claude Code | Medium | Local | High | Low (curator role) | Research deep-dives |
| microsoft/llmwiki VS Code ext | Medium | Local | High | Low | VS Code / Cursor users |
| Zettelkasten + Slipbox MCP | Medium | Local | High | Medium | Atomic-note thinkers |
| Plain markdown + agent (this repo) | Low | Local | High | Low–Medium | Git-native researchers |
| Full RAG stack (vector DB) | High | Configurable | Low | High | Production apps, 5000+ docs |

## Decision flowchart

```mermaid
flowchart TD
  Start[Start: I want LLM help with PKM] --> Q1{Do you already use Obsidian/Logseq?}
  Q1 -->|Yes, large vault| PluginStack[Smart Connections + Copilot on existing vault]
  Q1 -->|No or small| Q2{Primary goal?}
  Q2 -->|Research deep-dives over sources| CompiledWiki[Karpathy LLM Wiki pattern]
  Q2 -->|Daily notes and journaling| PluginStack
  Q2 -->|Atomic notes / Zettelkasten| Slipbox[Slipbox MCP + agent]
  CompiledWiki --> Q3{IDE preference?}
  Q3 -->|VS Code / Cursor| LLMWikiExt[microsoft/llmwiki or AGENTS.md]
  Q3 -->|Terminal / Claude Code| AgentSkills[agent-based-km or custom skills]
  Q3 -->|Plain Git markdown| PlainMD[AGENTS.md + researches/ structure]
```

## Related

- [Local models — why](./local_models_why.md) — effectiveness, cost analysis, comparisons
- [Local models — how](./local_models_how.md) — setup and integration
- [Traditional PKM + LLM](./traditional_pkm_and_llm.md)
- [Decision framework](./decision_framework.md)
- [Obsidian setup guide](./obsidian_setup_guide.md)
- [Agent harness architecture](./agent_harness_architecture.md)
