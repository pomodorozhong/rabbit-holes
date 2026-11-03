# Organizing Agent Skills in a Repository

Repository examples, folder locations, and installer behavior checked on 2026-09-29. The personal-repository example was checked on 2026-11-03.

Keep the files you maintain in Git. A repository can hold a large library without installing the whole library for every project.

This guide covers where skills live in a repository, how to keep a collection manageable, and which existing repositories you can learn from. To get those skills onto a machine or share them with other people, see [Installing and sharing skills](installing-and-sharing-skills.md). For how a skill works, see [Basics](basics.md).

## Choose a repository layout

| Situation | Suggested layout | How the agent gets the skills |
| --- | --- | --- |
| A skill belongs to an existing project | `.agents/skills/<name>/SKILL.md`, or the product's documented folder | The agent discovers it while working in that project |
| A separate repository publishes one skill | `SKILL.md` at the repository root, with supporting folders beside it | Install or copy that skill into the target agent's folder |
| A separate repository publishes several skills | `skills/<name>/SKILL.md`, one folder per skill | Select and install the skills needed for each project |

These are practical layout choices. The skill format requires each skill to have its own `SKILL.md`; a Git repository is only the container. Vercel's installer supports root skills and collections under `skills/`. [Agent Skills specification](https://agentskills.io/specification), [Installer discovery rules](https://github.com/vercel-labs/skills#skill-discovery)

For one skill, a small repository can look like this:

```text
release-brief/
├── README.md              Recommended: purpose, setup, and example request
├── LICENSE                Recommended: terms for reuse
├── SKILL.md               Required: skill metadata and instructions
├── references/            Optional: supporting instructions
├── assets/                Optional: templates and other files
└── scripts/               Optional: executable helpers
```

For skills kept with application code, Codex and Cursor both support `.agents/skills/`. A publishing folder named `skills/` alone is not a Codex discovery location. Install or link selected skills into a location the agent scans. [Codex locations](https://developers.openai.com/codex/skills#where-codex-loads-local-skills), [Cursor locations](https://prod.cursor.com/help/customization/skills)

## Manage several skills in one Git repository

Use a separate folder for each installable skill. Keep its instructions and supporting files together so it can be installed on its own:

```text
agent-skills/
├── README.md                          Recommended: catalog and installation guide
├── LICENSE                            Recommended: shared terms, if applicable
├── .gitignore                         Recommended: exclude local/generated files
├── CHANGELOG.md                       Optional: changes to the collection
└── skills/                            Collection folder in this layout
    ├── release-brief/                 One installable skill
    │   ├── SKILL.md                   Required
    │   ├── agents/openai.yaml         Optional: OpenAI settings
    │   ├── references/                Optional
    │   │   └── change-evidence.md
    │   ├── assets/                    Optional
    │   │   └── briefing-template.docx
    │   └── scripts/                   Optional
    │       └── render-brief.mjs
    └── incident-brief/                Another installable skill
        ├── SKILL.md                   Required
        └── references/                Optional
            └── incident-evidence.md
```

The repository root does not need a `SKILL.md` for the collection. Put one inside each skill folder, and make the front matter's `name` match that folder's name. For example, `skills/release-brief/SKILL.md` uses `name: release-brief`. The name/folder match is part of the shared specification. [Naming rules](https://agentskills.io/specification#name-field)

A manageable collection needs a few conventions:

1. **Keep a catalog in the README.** For each skill, list its purpose, supported products, software requirements, and an example request, with a link to its folder and its install command.
2. **Keep each installed folder complete.** A script or reference outside the folder may not travel with it, so put required files inside the skill or document the dependency. See [Scripts and dependencies](scripts-and-mcp.md).
3. **Keep one editable copy.** Change the source repository, then refresh installations. If products need different settings, explain those differences rather than letting copies drift apart.
4. **Review changes by skill.** Update instructions, scripts, templates, and examples together, then check referenced paths and run affected helpers. Try a request that should select the skill and one that should not.
5. **Record a reviewed version.** A Git tag or commit identifies the whole repository at that point, so record it with the selected folders when a team needs reproducible installations.
6. **Install a useful subset.** Adding a skill to the library does not mean everyone needs it enabled. See [How many skills are too many?](managing-skills.md) for listing limits and selection problems.

These are maintenance recommendations, not extra requirements of the skill format. Start with a flat `skills/<name>/` layout; add categories only when browsing the collection becomes difficult and your chosen installer supports the nesting.

## Existing templates and example repositories

These are real repositories or folders you can inspect. The layouts above are suggested designs.

| Example | What it contains | What to learn from it |
| --- | --- | --- |
| [Anthropic's starter template](https://github.com/anthropics/skills/blob/main/template/SKILL.md) | A minimal `SKILL.md` inside the `anthropics/skills` repository | Copy the starting file for one skill, then replace its placeholder name, description, and instructions |
| [anthropics/skills](https://github.com/anthropics/skills) | Multiple skills in `skills/<name>/`, plus the starter template | A collection with separate folders, supporting files, and installation documentation |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Multiple skills under `skills/`, with a README describing available skills | A collection intended for selective installation through the `skills` CLI |
| [pomodorozhong/skills](https://github.com/pomodorozhong/skills) | Personal skills under `skills/`, maintenance scripts under `scripts/`, and a setup and recovery guide | How one Git checkout can supply shared skills to Codex and Claude Code, with import checks and undoable link runs |
| [openai/plugins](https://github.com/openai/plugins) | Plugin examples under `plugins/<name>/`; plugins can contain `skills/` and other components | How to package skills for Codex distribution, including skills used with connectors |

For a first skill, start with Anthropic's template. For a collection, study Anthropic's or Vercel's folder layout. For Codex plugin distribution, use OpenAI's current plugin examples. These are examples to adapt; the starter file is not a complete GitHub repository template. Check the license for the specific files you reuse. Anthropic's repository includes both open-source and source-available skills with different terms. [Anthropic repository notes](https://github.com/anthropics/skills#about-this-repository)

The older [openai/skills](https://github.com/openai/skills) catalog still shows useful folder patterns, but its README now marks it deprecated and points to `openai/plugins` for current examples.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex: Build skills](https://developers.openai.com/codex/skills)
- [Cursor: Skills](https://prod.cursor.com/help/customization/skills)
- [Vercel `skills` CLI](https://github.com/vercel-labs/skills)
- [Anthropic skills and starter template](https://github.com/anthropics/skills)
- [Vercel's skill collection](https://github.com/vercel-labs/agent-skills)
- [OpenAI's current plugin examples](https://github.com/openai/plugins)
- [OpenAI's deprecated skill catalog](https://github.com/openai/skills)

The repository layouts and collection conventions are recommendations. Product and installer behavior may change.
