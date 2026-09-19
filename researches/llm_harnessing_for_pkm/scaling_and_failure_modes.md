# Scaling Path and Failure Modes

Back to [research index](./README.md)

## Growth curve

| Stage | Size | Navigation | Tools |
| --- | --- | --- | --- |
| **Small** | ~10–50 pages | `index.md` only | Schema file + agent |
| **Medium** | ~100–200 pages | Index + hybrid search | Add [qmd](https://github.com/tobi/qmd) (CLI + MCP) |
| **Large** | 200+ pages | Hierarchical indexes | Subagent search, deterministic routing scripts |
| **Enterprise** | 1000s of docs | Full RAG pipeline | Vector DB, access control, eval harness |

Karpathy reports running ~100 articles and ~400K words via index navigation. Research suggests quality degrades around 130K tokens ("lost in the middle"), so plan search tooling before you hit that wall.

### When to add qmd (Roadmap C)

Add hybrid search when:

- `index.md` exceeds comfortable context limits (~100–200 pages)
- Ingest requires finding which existing pages to update across a large wiki
- Query sessions repeatedly miss relevant pages via index-only navigation

See [qmd](https://github.com/tobi/qmd) — local BM25 + vector + LLM rerank, available as CLI and MCP server.

## Failure modes

| Failure | Description | Mitigation |
| --- | --- | --- |
| **Wiki slop** | Agent-generated pages without curation; quality degrades over time | Human review on ingest; [contamination mitigation](https://github.com/arturseo-geo/llm-knowledge-base/blob/main/docs/contamination-mitigation.md) patterns; promotion gates from draft to canonical |
| **Index rot** | `index.md` out of sync with actual pages | Lint checks; update index on every ingest; deterministic validation scripts |
| **False compounding** | Hallucinated cross-refs that look authoritative | Require source attribution; contradiction callouts; periodic lint |
| **Context re-read tax** | Expensive sessions from loading full schema + index every time | Hot cache; compact routing files; subagents; deterministic pre-processing |
| **Over-collection** | PKM landfill — capture without synthesis | Optimize for reuse, not capture; regular lint for orphans and unused notes |
| **Stale wiki** | Compiled pages not updated when sources change | Re-ingest workflow; lint for stale claims; date metadata on pages |

## Related

- [Agent harness architecture](./agent_harness_architecture.md)
- [Decision framework](./decision_framework.md)
- [Harness POC](./poc/harness_poc.ipynb)
