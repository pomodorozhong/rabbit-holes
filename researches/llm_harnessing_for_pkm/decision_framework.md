# Decision Framework: Synthesis-Time vs Query-Time

Back to [research index](./README.md)

Based on [Ranjan Kumar's analysis](https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory): LLM Wiki and RAG are the same thing at **different synthesis times**. The real architectural question is: **when does synthesis happen — at ingest or at query?**

## Comparison

| Factor | Favor compiled wiki (ingest-time) | Favor RAG (query-time) |
| --- | --- | --- |
| Corpus size | Curated, under ~200 compiled pages | Thousands of raw docs, frequently changing |
| Query frequency | Same topics queried repeatedly | Ad-hoc one-off lookups |
| Human role | Curator + questioner | Author of notes |
| Auditability | High (readable markdown, git history) | Lower (vector store is opaque) |
| Privacy | Local markdown + local agent | Depends on plugin/API choices |
| Cost at scale | Fixed (hardware); see [local models — why](./local_models_why.md) | Per-token; see cost analysis |
| Maintenance | Agent lint loop | Re-index on change |
| Output durability | Persistent wiki pages | Ephemeral chat responses |

## The compiler analogy

- **RAG** = interpreter: every query re-reads raw documents, re-derives relationships, re-synthesizes
- **Compiled wiki** = compiler: process sources once at ingest, store compiled output, query the output not the source

At scale, the irony is deliberate: compiled wikis add [qmd](https://github.com/tobi/qmd) (hybrid BM25 + vector + LLM rerank) for navigation — which *is* retrieval. The pattern that positioned itself as a RAG replacement quietly becomes RAG-augmented at scale.

## Hybrid recommendation (default best practice)

1. **PKM layer** — human exploratory notes, drafts, unfinished thinking
2. **Compiled wiki layer** — agent-maintained synthesis from `raw/` sources
3. **Search layer** — `index.md` first; add qmd/BM25 when scale demands
4. **Memory layer** — session continuity and user preferences only; not a substitute for wiki

## Related

- [Foundations](./foundations.md)
- [LLM Wiki pattern](./llm_wiki_pattern.md)
- [Tool landscape comparison](./tool_landscape.md)
- [Scaling & failure modes](./scaling_and_failure_modes.md)
