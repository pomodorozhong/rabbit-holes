# How Different Products Use Skills

Checked against primary sources on 2026-09-29.

The same skill folder can work in several products, but where you put it, how you start it, and what it can access may differ. Compare the product running the agent as well as the model provider. Even two products from the same provider can load and share skills differently.

For a focused comparison with one shared workflow, see [How Codex and Claude Code use skills differently](codex-vs-claude-code.md).

## What is shared?

The [Agent Skills specification](https://agentskills.io/specification) defines a folder with `SKILL.md`, required `name` and `description` fields, Markdown instructions, and optional supporting files. It describes loading metadata first, instructions when selected, and other files as needed. It does not define one installation path, command, permission system, or sharing service for every product.

| Part | Shared idea | What the product decides |
| --- | --- | --- |
| Files | Instructions and supporting files live together | Extra settings and accepted metadata fields |
| Discovery | Names and descriptions help select a skill | Which folders or uploads are available to the agent |
| Activation | Full instructions load when the skill is used | User commands, automatic selection, and consent |
| Execution | Instructions can use scripts and assets | Tools, software, network access, and approvals |
| Sharing | The folder can be copied or versioned | User, team, workspace, plugin, or API distribution |

## Local coding agents

| Provider and product | Where it finds skills | How it starts a skill | Difference to keep in mind |
| --- | --- | --- | --- |
| OpenAI — Codex | Project `.agents/skills` folders from the working directory up to the Git root; personal `~/.agents/skills`; admin and bundled locations | `$skill-name` or `/skills` in CLI/IDE; automatic selection from the description | Duplicate names are not merged. `agents/openai.yaml` can disable automatic selection. [Codex guide](https://developers.openai.com/codex/skills) |
| Anthropic — Claude Code | Project `.claude/skills`, personal `~/.claude/skills`, and plugins | `/skill-name` or automatic selection | `disable-model-invocation: true` makes a skill manual-only. `context: fork` runs it in a subagent. [Claude Code guide](https://code.claude.com/docs/en/skills) |
| Google — Gemini CLI | Project `.gemini/skills` or `.agents/skills`; personal `~/.gemini/skills` or `~/.agents/skills`; extensions and built-ins | Agent calls `activate_skill`; `/skills` manages the list | Activation asks for consent, then loads the instructions and grants read access to the skill folder. Project skills take precedence over personal skills with the same name. [Gemini CLI guide](https://geminicli.com/docs/cli/skills/) |

Codex's initial skill list has a context limit. Descriptions may be shortened, and some entries may be omitted; a selected skill's full instructions still load. [Codex guide](https://developers.openai.com/codex/skills)

See [How many skills are too many?](managing-skills.md) for documented Codex and Claude Code budgets, warning signs, and ways to reduce the active list.

Claude Code accepts some files that are less strict than the open specification, including omitted `name` or `description` fields. For a skill you want to share across products, keep both fields. [Claude Code front matter](https://code.claude.com/docs/en/skills#frontmatter-reference)

### Permissions also differ

Do not treat `allowed-tools` as having the same effect everywhere. The open specification marks it experimental. Claude Code documents that it can allow listed tools without per-use approval during the invoking turn. Gemini CLI documents a consent step that adds the skill directory to allowed read paths. Review the target product's permission rules before moving a skill between them. [Specification](https://agentskills.io/specification), [Claude Code tool access](https://code.claude.com/docs/en/skills#restrict-tool-access), [Gemini CLI activation](https://geminicli.com/docs/cli/skills/#how-it-works)

## Hosted products and APIs

| Provider and product | How skills are made available | Loading and execution | Sharing or versioning |
| --- | --- | --- | --- |
| OpenAI — Responses hosted shell | Attach bundles through `tools[].environment.skills` | The model sees metadata and reads selected instructions in the shell environment | Uploaded bundles can be selected by version. The guide treats skill instructions as user prompt input. [OpenAI API guide](https://developers.openai.com/api/docs/guides/tools-skills) |
| OpenAI — Agents API | Put skill folders inside the sandbox and register their parent paths in `environment.capability_directories` | The agent harness discovers folders and exposes their metadata | Uses registered directories rather than Responses `skill_reference` attachments. [OpenAI API guide](https://developers.openai.com/api/docs/guides/tools-skills) |
| Anthropic — Claude API | Upload custom skills through the Skills API; reference their IDs in `container` alongside code execution | Skills run in a sandbox with no network access or runtime package installation | Uploaded custom skills are available across the workspace. [Claude Platform guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| Anthropic — claude.ai | Upload a custom skill ZIP through Settings → Features, with code execution enabled | Skills are available to the user's conversations; network access depends on settings | Custom uploads belong to each user and do not automatically sync to Claude Code or the API. [Claude Platform guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |

The Google comparison here covers Gemini CLI. It does not establish that the Gemini API has the same skill loading or installation system.

## Products that support several model providers

Cursor and GitHub Copilot show why folder rules belong to the product rather than the model alone:

| Product | Skill locations | How it uses skills |
| --- | --- | --- |
| Cursor | `.cursor/skills`, `.agents/skills`, personal equivalents, and compatibility folders for Claude and Codex | `/skill-name` runs a skill; `@` attaches it as context. Personal cloud sync covers `~/.cursor/skills`, not every local folder. [Cursor guide](https://prod.cursor.com/help/customization/skills) |
| GitHub Copilot | Project `.github/skills`, `.claude/skills`, or `.agents/skills`; personal `~/.copilot/skills` or `~/.agents/skills` | Loads relevant skills in its supported agents and interfaces. Check the documentation for the specific Copilot product you use. [Copilot guide](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |

### Cursor: project scope and cloud access

Cursor can find skills in nested project folders. For example, a skill under `apps/web/.cursor/skills/` is shown when the agent works on files in `apps/web/`. The `paths` front-matter field can also limit a skill to matching files.

For personal skills in Cloud Agents, enable **Sync Skills for Cloud Agents** in Settings → Agents. Only `~/.cursor/skills/` is synced this way; `~/.agents/skills/` stays local. To share with teammates, publish a personal skill through Customize → Skills to the team marketplace. [Cursor scope, sync, and sharing](https://prod.cursor.com/help/customization/skills)

## Moving one skill between products

Keep the main workflow in `SKILL.md`, with a clear name, description, and links to supporting files. Put product-specific settings in the appropriate metadata file or a clearly labeled section. Then check four things in each target product:

1. **Discovery:** does the skill appear, and is it the intended version?
2. **Selection:** does a direct request work, and does a realistic task select it when expected?
3. **Execution:** are the required tools, dependencies, files, and network access available?
4. **Output:** does it produce the same required content and pass the relevant checks?

These are suggested checks, not results from running the skill in every product. For installation examples, see [Storing and sharing skills](storage-and-distribution.md).

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI: Build skills](https://developers.openai.com/codex/skills)
- [OpenAI API: Skills](https://developers.openai.com/api/docs/guides/tools-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Claude Platform: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Gemini CLI: Agent Skills](https://geminicli.com/docs/cli/skills/)
- [Cursor: Skills](https://prod.cursor.com/help/customization/skills)
- [GitHub Copilot: About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

This compares documented behavior, not every provider or a test of every product. Paths, settings, and sharing rules may change after the checked date.
