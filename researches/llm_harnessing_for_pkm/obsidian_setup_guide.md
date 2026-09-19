# Step-by-Step: LLM PKM Harness in Obsidian

Back to [research index](./README.md)

This guide walks through setting up the Karpathy-style compiled wiki pattern in Obsidian, with an LLM agent (Claude Code or Cursor) as the maintainer.

**Time:** ~30–45 minutes for initial setup  
**Prerequisites:** Obsidian installed, Claude Code or Cursor installed, an API key or local Ollama (optional)

---

## Overview

You will end up with:

```
my-vault/
├── raw/                    # Your sources (immutable)
│   └── assets/             # Downloaded images from clips
├── wiki/                   # LLM-maintained compiled knowledge
│   ├── concepts/
│   ├── entities/
│   ├── sources/
│   ├── synthesis/
│   └── derived/
├── index.md                # Catalog of all wiki pages
├── log.md                  # Chronological audit trail
├── CLAUDE.md               # Agent schema (or AGENTS.md for Cursor/Codex)
└── .obsidian/              # Obsidian config (auto-created)
```

**Roles:** You curate sources and ask questions. The LLM ingests, cross-links, and maintains the wiki. Obsidian is your reader and graph viewer.

---

## Step 1: Create the Vault

1. Open Obsidian → **Create new vault**
2. Choose a folder location (e.g. `~/Documents/my-llm-wiki`)
3. Prefer a path **without spaces** if you will use terminal agents frequently

---

## Step 2: Create Folder Structure

In Obsidian's file explorer, create these folders:

| Folder | Purpose |
| --- | --- |
| `raw/` | Source articles, PDFs, transcripts — you add, LLM reads only |
| `raw/assets/` | Local images from web clips |
| `wiki/concepts/` | Frameworks, methods, terms |
| `wiki/entities/` | People, organizations, tools |
| `wiki/sources/` | One summary page per ingested source |
| `wiki/synthesis/` | Evolving overview and thesis |
| `wiki/derived/` | Query answers filed back into the wiki |

Create two root files:

**`index.md`** — start with:

```markdown
# Wiki Index

Catalog of compiled wiki pages. Updated on every ingest.

## Concepts

## Entities

## Sources

## Synthesis

## Derived
```

**`log.md`** — start with:

```markdown
# Wiki Log

Append-only timeline of ingests, queries, and lint passes.

## [YYYY-MM-DD] setup | Vault initialized
```

---

## Step 3: Configure Obsidian Settings

### Files and links

1. **Settings → Files and links**
2. Set **Default location for new notes** → `wiki/` (or a subfolder you prefer)
3. Set **Attachment folder path** → `raw/assets`
4. Enable **Automatically update internal links** (helps when the LLM renames pages)

### Hotkeys (recommended)

1. **Settings → Hotkeys**
2. Search for **Download attachments for current file**
3. Bind to e.g. `Ctrl+Shift+D` — use after clipping an article so images are local

---

## Step 4: Install Obsidian Plugins

Open **Settings → Community plugins → Browse** and install:

### Essential (compiled wiki workflow)

| Plugin | Purpose | Install |
| --- | --- | --- |
| **Obsidian Web Clipper** | Browser extension → save articles to `raw/` as markdown | [Chrome](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijejnhllmfkfig) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/web-clipper-obsidian/) |

Install the Web Clipper **browser extension** separately (not from Community plugins). Configure it to save clips into your vault's `raw/` folder.

### Optional (enhanced reading & AI-on-vault)

| Plugin | Purpose |
| --- | --- |
| **Smart Connections** | Local semantic search; related-notes sidebar |
| **Copilot for Obsidian** | Vault QA chat (RAG over your notes) |
| **Dataview** | Query wiki frontmatter (tags, dates, source counts) |
| **Marp Slides** | Generate slide decks from wiki content |

Enable community plugins: **Settings → Community plugins → Turn on community plugins**, then enable each installed plugin.

### Smart Connections + local Ollama (privacy-first, optional)

See [how to use local models](./local_models_how.md) for the full local stack. Quick start:

1. Install [Ollama](https://ollama.com/)
2. Pull models: `ollama pull nomic-embed-text` and `ollama pull llama3.2`
3. In Smart Connections settings, use local embeddings
4. In Copilot settings, set base URL to `http://localhost:11434/v1`

Smart Connections and Copilot complement the compiled wiki: they help **you** navigate; the agent maintains the **wiki layer**.

---

## Step 5: Write the Agent Schema (`CLAUDE.md` or `AGENTS.md`)

Create **`CLAUDE.md`** (Claude Code) or **`AGENTS.md`** (Cursor / Codex) at the vault root. This is the constitution the agent reads every session.

Minimal starter schema:

```markdown
# LLM Wiki — Agent Instructions

You maintain a compiled personal wiki in this Obsidian vault.

## Layers

- `raw/` — immutable sources. Read only; never modify.
- `wiki/` — compiled knowledge. You create and update pages here.
- `index.md` — catalog of all wiki pages with one-line summaries.
- `log.md` — append-only log of operations.

## Page conventions

- Use `[[wikilinks]]` for cross-references.
- Source pages go in `wiki/sources/` with frontmatter:
  ```yaml
  ---
  source: raw/filename.md
  ingested: YYYY-MM-DD
  tags: [concept-tag]
  ---
  ```
- Concept pages go in `wiki/concepts/`.
- Entity pages go in `wiki/entities/`.
- When new data contradicts an existing page, add a callout:
  `> [!contradiction] Contradicts [[Other Page]] — reason`

## Workflows

### Ingest
1. Read the source in `raw/`
2. Discuss key takeaways with the user (if interactive)
3. Create or update pages in `wiki/` (typically 3–10 pages per source)
4. Update `index.md`
5. Append entry to `log.md` with format: `## [YYYY-MM-DD] ingest | Source Title`

### Query
1. Read `index.md` to find relevant pages
2. Read those pages
3. Synthesize answer with `[[citations]]`
4. If the answer is worth keeping, file it in `wiki/derived/`

### Lint
1. Check for orphan pages (no inbound links)
2. Check for dead wikilinks
3. Flag contradictions and stale claims
4. Suggest missing concept pages
5. Append entry to `log.md`: `## [YYYY-MM-DD] lint | N issues found`

## Rules

- Never modify files in `raw/`.
- Always update `index.md` after creating or renaming wiki pages.
- Prefer updating existing pages over creating duplicates.
- Keep summaries in `index.md` to one line each.
```

Co-evolve this file with your agent as you learn what works for your domain.

---

## Step 6: Connect the Agent to Your Vault

### Option A: Claude Code (recommended for Karpathy pattern)

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
2. Open a terminal in your vault directory:
   ```bash
   cd ~/Documents/my-llm-wiki
   claude
   ```
3. On first run, paste the [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and ask:
   > Read CLAUDE.md and confirm the vault structure. Then walk me through ingesting my first source.

Claude Code reads `CLAUDE.md` automatically and can edit files in the vault.

### Option B: Cursor

1. Open the vault folder in Cursor: **File → Open Folder** → select your vault
2. Ensure `AGENTS.md` exists at the root (Cursor reads this)
3. Use Agent mode and say:
   > Follow AGENTS.md. Ingest the article in raw/ and update the wiki.

### Option C: VS Code + microsoft/llmwiki extension

1. Install [llmwiki](https://github.com/microsoft/llmwiki) from VS Code marketplace
2. Open vault folder in VS Code / Cursor
3. Use `@wiki` chat participant and the extension's ingest commands

---

## Step 7: Capture Your First Source

1. Find an article you want in your knowledge base
2. Use **Obsidian Web Clipper** → save to `raw/`
3. Open the clipped note in Obsidian
4. Press your **Download attachments** hotkey (`Ctrl+Shift+D`) so images are local
5. Tell the agent:
   ```
   Ingest raw/my-article.md
   ```

The agent should:

- Create `wiki/sources/my-article.md`
- Update relevant concept/entity pages
- Refresh `index.md`
- Append to `log.md`

Browse results in Obsidian — follow wikilinks, open **Graph view** to see connections.

---

## Step 8: Query the Wiki

Ask the agent (not raw files):

```
What do we know about [topic]?
```

Or:

```
Compare [concept A] and [concept B] based on the wiki.
```

Good answers can be filed back:

```
Save this answer to wiki/derived/comparison-a-vs-b.md and update the index.
```

---

## Step 9: Run Periodic Lint

Weekly or after several ingests:

```
Lint the wiki. Report orphans, dead links, contradictions, and missing concept pages.
```

Review the report in Obsidian. Fix or approve agent-suggested changes.

---

## Step 10: Optional Enhancements

### Git version control

Init git in your vault for history and backup:

```bash
cd ~/Documents/my-llm-wiki
git init
echo ".obsidian/workspace.json" >> .gitignore
echo ".smart-env/" >> .gitignore
git add .
git commit -m "Initial vault setup"
```

### qmd for larger wikis (100+ pages)

When `index.md` outgrows comfortable context limits, add [qmd](https://github.com/tobi/qmd) hybrid search:

```bash
npm install -g @tobilu/qmd
qmd collection add ~/Documents/my-llm-wiki/wiki --name wiki
```

Add to `CLAUDE.md`: "Use `qmd search wiki 'query'` before reading pages."

If your agent supports MCP, enable qmd's MCP server for native tool access.

### Two-vault setup

Some practitioners keep:

- **Agent vault** — raw + wiki (agent writes here)
- **Personal vault** — daily notes, journaling (human only)

Symlink or periodically promote curated pages from agent vault to personal vault. See [two-vault setup](https://github.com/arturseo-geo/llm-knowledge-base/blob/main/docs/two-vault-setup.md).

---

## Daily Workflow Cheat Sheet

| You do | Agent does |
| --- | --- |
| Clip article to `raw/` | — |
| `Ingest raw/article.md` | Creates/updates wiki pages, index, log |
| Ask questions | Reads index → pages → synthesizes |
| `Save this to derived/` | Files answer into wiki |
| `Lint the wiki` | Health report |
| Browse in Obsidian | — |

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Agent modifies `raw/` | Reinforce in schema: "Never modify raw/" |
| Duplicate concept pages | Add rule: "Search index before creating new pages" |
| Index out of sync | Run lint; add "always update index.md" to ingest workflow |
| High API cost | Use subagents for search; batch ingests; add qmd for retrieval |
| Broken wikilinks after rename | Enable Obsidian auto-update links; run lint |
| Agent forgets conventions | Ensure `CLAUDE.md` / `AGENTS.md` is at vault root |

---

## Related

- [Research index](./README.md)
- [Why use local models](./local_models_why.md)
- [How to use local models](./local_models_how.md)
- [LLM Wiki pattern](./llm_wiki_pattern.md)
- [POC README](./poc/README.md) — uv setup and run instructions
- [Harness POC notebook](./poc/harness_poc.ipynb)
