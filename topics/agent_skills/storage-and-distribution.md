# Storing and Sharing Agent Skills

Repository examples, folder locations, and installer behavior checked on 2026-09-29.

Keep the files you maintain in Git. Put the skills you want an agent to use in that product's skill folder, either by copying, linking, or installing them. A repository can hold a large library without installing the whole library for every project.

This guide covers repository layouts, managing a collection, real examples, and installation. For a personal repository that links skills into Codex and Claude Code, including migration and recovery, follow [Back up and install skills from one Git repo](backup-and-restore.md). For how a skill works, see [Basics](basics.md). For product-specific discovery and permissions, see [Product differences](provider-differences.md).

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

1. **Keep a catalog in the README.** List each skill's name, purpose, supported products, software requirements, and an example request. Link directly to its folder and show how to install it separately.
2. **Keep each installed folder complete.** A script or reference outside that folder may not travel with it. Put required files inside the skill, or document and package the external dependency explicitly. See [Scripts and dependencies](scripts-and-mcp.md).
3. **Avoid maintaining several editable copies.** Make changes in the source repository, then refresh installations. If products need different settings, explain those differences rather than letting copies drift apart.
4. **Review changes by skill.** Update instructions, scripts, templates, and examples together. Check referenced paths and run any affected helpers. Try a request that should select the skill and one that should not.
5. **Record a reviewed version.** A Git tag or commit identifies the whole repository at that point. Two skills installed from the same revision come from the same snapshot. Record the revision and selected folders when a team needs reproducible installations.
6. **Install a useful subset.** Adding a skill to the library does not mean everyone needs it enabled. See [How many skills are too many?](managing-skills.md) for listing limits and selection problems.

These are maintenance recommendations, not extra requirements of the skill format. Start with a flat `skills/<name>/` layout; add categories only when browsing the collection becomes difficult and your chosen installer supports the nesting.

## Existing templates and example repositories

These are real repositories or folders you can inspect. The layouts above are suggested designs.

| Example | What it contains | What to learn from it |
| --- | --- | --- |
| [Anthropic's starter template](https://github.com/anthropics/skills/blob/main/template/SKILL.md) | A minimal `SKILL.md` inside the `anthropics/skills` repository | Copy the starting file for one skill, then replace its placeholder name, description, and instructions |
| [anthropics/skills](https://github.com/anthropics/skills) | Multiple skills in `skills/<name>/`, plus the starter template | A collection with separate folders, supporting files, and installation documentation |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Multiple skills under `skills/`, with a README describing available skills | A collection intended for selective installation through the `skills` CLI |
| [openai/plugins](https://github.com/openai/plugins) | Plugin examples under `plugins/<name>/`; plugins can contain `skills/` and other components | How to package skills for Codex distribution, including skills used with connectors |

For a first skill, start with Anthropic's template. For a collection, study Anthropic's or Vercel's folder layout. For Codex plugin distribution, use OpenAI's current plugin examples. These are examples to adapt; the starter file is not a complete GitHub repository template. Check the license for the specific files you reuse. Anthropic's repository includes both open-source and source-available skills with different terms. [Anthropic repository notes](https://github.com/anthropics/skills#about-this-repository)

The older [openai/skills](https://github.com/openai/skills) catalog still shows useful folder patterns, but its README now marks it deprecated and points to `openai/plugins` for current examples.

## Install selected skills from a collection

Vercel's `skills` CLI can list a repository's skills and install selected names. In these examples, replace `your-name/agent-skills` with your repository. Run installation commands from the target project's root:

```bash
npx skills add your-name/agent-skills --list
npx skills add your-name/agent-skills --skill release-brief --agent codex
npx skills add your-name/agent-skills --skill release-brief --skill incident-brief --agent cursor
```

Project installation is the default. Add `--global` for a personal installation across projects. The CLI accepts public or private Git repositories and local folders; private repositories need working credentials. [CLI options](https://github.com/vercel-labs/skills#options)

For a reviewed revision, check out that tag or commit locally, then install selected skills from its local path:

```bash
npx skills add /absolute/path/to/agent-skills --skill release-brief --agent codex
```

Choose between **links** and **copies**. A symlink points an agent's installation to the installer's shared local copy. A copy has independent files; `--copy` selects that approach. Updating the source Git repository does not by itself refresh every installed copy. Agree on an update process and retest affected skills. [Installation methods](https://github.com/vercel-labs/skills#installation-methods)

## Exporting and installing a skill for Codex

### Export the whole skill folder

Include `SKILL.md` and every local file the skill uses, with their relative paths intact. Export one skill folder rather than the whole collection. Remove private examples, secrets, and machine-specific paths before sharing.

From a project containing `.agents/skills/release-brief`, these commands create an export folder and an archive:

```bash
mkdir skill-export
cp -R .agents/skills/release-brief skill-export/release-brief
tar -czf skill-export/release-brief.tar.gz -C skill-export release-brief
```

Choose a new export folder if `skill-export` already exists. For a collection repository, replace the copy source with `skills/release-brief`. The archive should contain `release-brief/SKILL.md` and supporting files. Unpack it before manual installation. These are file-copy commands, not a Codex export command.

### Install by copying the folder

Choose the scope using [Codex's documented discovery locations](https://developers.openai.com/codex/skills#where-codex-loads-local-skills):

| Scope | Codex's documented destination | Use it when |
| --- | --- | --- |
| Project | `.agents/skills/release-brief/` | The skill belongs with that project |
| Personal | `~/.agents/skills/release-brief/` | You want it across projects |

From the target project's root, copy an unpacked export into the project:

```bash
mkdir -p .agents/skills
test ! -e .agents/skills/release-brief && cp -R skill-export/release-brief .agents/skills/release-brief
```

Or copy it into your personal folder:

```bash
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/release-brief" && cp -R skill-export/release-brief "$HOME/.agents/skills/release-brief"
```

Change the source path if the export is elsewhere. The `test` stops the copy when an installation already exists; compare the versions before replacing it.

### Install from GitHub with Codex's installer

Ask the built-in installer for a specific folder and destination:

```text
$skill-installer Install release-brief from https://github.com/your-name/agent-skills/tree/main/skills/release-brief into ~/.agents/skills.
```

Replace the example URL with your repository. The published installer defaults to `$CODEX_HOME/skills`, usually `~/.codex/skills`, which differs from the personal discovery folder documented above. Giving the destination explicitly makes the intended location clear. Its helper supports `--dest`, `--ref` for a tag or commit, and multiple `--path` values for several skills. Ask for a reviewed revision if you need a fixed version. [Published installer instructions](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md)

### Check the installation

In Codex CLI or the IDE extension, open `/skills` or mention `$release-brief`. If it is missing, check the installed path and `SKILL.md`; restart Codex if needed. Then try a small task with sample records. Being listed proves discovery; following the steps on a sample task checks behavior. [Codex skill guide](https://developers.openai.com/codex/skills)

## Share through a product or public directory

Git stores the source files. A plugin or marketplace provides another way for people to install them. OpenAI recommends plugins for distributing reusable skills beyond one repository; a plugin can contain one or several skills and optional connectors. See the [Codex plugin packaging guide](https://developers.openai.com/plugins/build/plugins) and [OpenAI's example repository](https://github.com/openai/plugins).

Cursor has a team marketplace for sharing skills. Other products have their own packaging and upload rules; see [Product differences](provider-differences.md). [Cursor team sharing](https://prod.cursor.com/help/customization/skills)

[skills.sh](https://skills.sh/) helps people find public skills through Vercel's ecosystem. Treat a listing as a way to find candidates. Review the instructions, scripts, dependencies, and licenses before installation.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Codex: Build skills](https://developers.openai.com/codex/skills)
- [Cursor: Skills](https://prod.cursor.com/help/customization/skills)
- [Vercel `skills` CLI](https://github.com/vercel-labs/skills)
- [Anthropic skills and starter template](https://github.com/anthropics/skills)
- [Vercel's skill collection](https://github.com/vercel-labs/agent-skills)
- [OpenAI's current plugin examples](https://github.com/openai/plugins)
- [OpenAI's deprecated skill catalog](https://github.com/openai/skills)
- [Published skill-installer instructions](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md)
- [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins)

The repository layouts and maintenance advice are recommendations. Export and project-copy commands were checked with temporary files; no skill was installed into Codex. Product and installer behavior may change.
