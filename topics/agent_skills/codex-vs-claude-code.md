# How Codex and Claude Code Use Skills Differently

Product documentation checked on 2026-10-12. This guide compares local coding workflows, rather than hosted APIs or model quality. The examples are illustrative; they were not run in both products.

A skill's instructions can travel between Codex and Claude Code more easily than its execution settings. A useful approach is to keep the task in ordinary Markdown, then adapt discovery, invocation, and permissions to each product. Claude Code also gives skill files specific syntax for arguments, command output, and subagent execution. Those features need attention when moving a workflow.

If you are new to the folder format, start with [Basics](basics.md). The [broader product comparison](provider-differences.md) includes other agents and hosted environments.

## Follow one shared workflow

Suppose a team wants a `change-brief` skill that explains a Git diff before review. Its output should identify the changed behavior, evidence for that interpretation, and unresolved questions. The shared folder could contain:

```text
change-brief/
├── SKILL.md
└── references/
    └── brief-format.md
```

An illustrative `SKILL.md`:

```markdown
---
name: change-brief
description: Explain a Git diff before review, including changed behavior and unresolved questions.
---

1. Use the comparison target supplied by the user. Ask if it is unclear.
2. Inspect the diff and enough surrounding code to explain the behavior.
3. Read references/brief-format.md for the output structure.
4. Write the brief. Separate observed changes from inferred effects.
5. State which checks ran and what still needs verification.
```

The reference could request three sections: changed behavior, verification evidence, and open questions. This keeps a reusable output format beside the workflow without putting the whole reference in the initial skill description. The [Agent Skills specification](https://agentskills.io/specification#progressive-disclosure) describes this progression: metadata first, selected instructions next, supporting files when needed.

The example tells the agent what to do. It leaves the comparison target in the user's request and avoids embedding a product's command syntax. That makes it a useful starting point for comparing the two hosts.

## Discovery and direct invocation

For local use, place the example in the appropriate project or personal directory:

| Operation | Codex | Claude Code |
| --- | --- | --- |
| Project location | `.agents/skills/change-brief/` | `.claude/skills/change-brief/` |
| Personal location | `~/.agents/skills/change-brief/` | `~/.claude/skills/change-brief/` |
| Direct request | CLI/IDE: `$change-brief Compare against origin/master.` | `/change-brief Compare against origin/master.` |
| Automatic selection | Matches the description | Matches the description |

Sources: [Codex discovery and invocation](https://learn.chatgpt.com/docs/build-skills), [Claude Code discovery and invocation](https://code.claude.com/docs/en/skills).

Codex scans project skill directories from the working directory up to the repository root. Duplicate names are not merged. [Codex discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

Claude Code also loads nested skills when it accesses that subdirectory. For ordinary enterprise, personal, and project name collisions, precedence is enterprise, then personal, then project; plugins use namespaced commands. [Claude Code discovery](https://code.claude.com/docs/en/skills#choose-where-skills-load)

For the team in the example, discovery is the first thing to verify: does the session see the checked-in `change-brief`, or another copy? A familiar name alone does not establish that the agent read the intended instructions. Distinct names or one maintained installation reduce that ambiguity.

## Controlling when the workflow starts

Manual-only invocation is configured differently:

| Intent | Codex | Claude Code |
| --- | --- | --- |
| Disable automatic selection | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | `disable-model-invocation: true` in `SKILL.md` front matter |
| Disable the local skill | `enabled = false` in a path-specific `[[skills.config]]` entry in `~/.codex/config.toml`; restart | `"off"` in `skillOverrides` |

Sources: [Codex metadata and disabling](https://learn.chatgpt.com/docs/build-skills#optional-metadata), [Claude Code invocation and overrides](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill).

For example, the Codex folder can add `agents/openai.yaml`:

```yaml
policy:
  allow_implicit_invocation: false
```

The Claude Code variant can add this field to its front matter:

```yaml
disable-model-invocation: true
```

Both choices retain direct invocation. They control selection, rather than granting permission for the workflow's actions. For `change-brief`, automatic selection may be convenient when someone asks for a review summary. For a separate workflow that publishes a release, an explicit start makes the intended timing clearer.

## Arguments and command output

Claude Code substitutes `$ARGUMENTS` and positional placeholders, and executes commands written as an exclamation mark followed by an inline code span before sending the resulting skill content to the model. [Claude Code arguments and dynamic context](https://code.claude.com/docs/en/skills#pass-arguments-to-skills)

A separate, illustrative Claude Code variant might contain:

```markdown
Compare the current branch with $ARGUMENTS.

Current working tree:
!`git status --short`
```

With `/change-brief origin/master`, the first line becomes `Compare the current branch with origin/master.` The command's output supplies the working-tree information. Substitution supplies an input; the command supplies fresh evidence. Neither establishes that the model's later interpretation is correct.

The Codex skills guide does not document these substitutions. A portable rewrite would say, "Read the comparison target from the user's request, then inspect the Git status and diff using the available tools." This moves data collection into the agent's workflow. When migrating, treat preprocessing syntax as a behavior to replace explicitly, rather than relying on the model to interpret it the same way.

## Tool access and execution context

Claude Code's `allowed-tools` grants listed tools without per-use approval for the invoking turn; it does not restrict the tool pool. Managed policy can suppress the grant. [Claude Code tool permissions](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill)

Codex's filesystem and network permissions are configured separately from the skill, alongside approval policy. Connector and MCP access have their own controls. [Codex permissions](https://learn.chatgpt.com/docs/permissions)

For `change-brief`, this means that "inspect the diff" still depends on available tools and file access. A skill may explain a command correctly while the environment prevents it from running. Keep requirements such as Git availability in the workflow, and configure actual access in the host. Do not infer a cross-product permission grant from a metadata field with a familiar name.

Claude Code also supports `context: fork`: the skill becomes a task for a subagent, with `agent` selecting its configuration. This starts without the parent conversation history. Conversely, a subagent definition can preload named skills through its `skills` field. [Claude Code subagents and skills](https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents)

In a separate illustrative variant, a brief could use:

```yaml
context: fork
agent: Explore
```

That changes how to write the task: include the comparison target and required output in the skill input, rather than assuming the worker knows an earlier discussion. The Codex skills guide does not document these fields as a delegation mechanism. A Codex adaptation therefore needs its own supported agent workflow if delegation is required; copying the fields does not establish equivalent behavior.

## Large catalogs and context loading

Both use progressive disclosure, but their initial catalogs have different documented budgets:

| Catalog behavior | Codex | Claude Code |
| --- | --- | --- |
| Budget | 2% of context; 8,000 characters if the window is unknown | 1% of context by default |
| Overflow | Shortens descriptions, then may omit entries with a warning | Keeps names; drops descriptions starting with less-used skills |

Sources: [Codex catalog budget](https://learn.chatgpt.com/docs/build-skills), [Claude Code catalog budget](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short).

These budgets are for discovery, not a safe skill count or a limit on a selected workflow's total context use. For `change-brief`, keep the distinctive trigger near the start of its description and put the detailed format in the reference. If direct invocation works while an ordinary review request misses the skill, inspect the visible catalog and overlapping descriptions before rewriting the procedure. See [How many skills are too many?](managing-skills.md) for catalog management.

## Moving the workflow with confidence

Keep the shared procedure and reference together, then adapt the host settings around them. A useful migration check has four steps:

1. Confirm that the intended skill appears in the target session.
2. Try a direct request, a matching ordinary request, and a nearby request that should not select it.
3. Check any argument expansion, command output, tool access, and delegation separately.
4. Compare the brief with the actual diff and verification evidence.

This is a proposed verification procedure, not a reported runtime result. The useful portability boundary is the workflow's meaning: what input it needs, what work it performs, and what output counts as complete. Installation paths and executable metadata must be checked again in each host.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI: Permissions](https://learn.chatgpt.com/docs/permissions)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents)

This comparison uses official documentation, rather than a benchmark of skill selection or output quality. The checked date applies to this guide; related guides may have earlier dates.
