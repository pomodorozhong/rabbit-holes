# Configure subagents and decide when to delegate

Delegation is useful when a worker can return something that the parent can check without repeating all the work. For a small edit, describing the task and checking a handoff can take longer than doing it directly. For a broad investigation, separate workers can explore independent questions while keeping intermediate logs out of the main conversation.

This guide compares Claude Code and Codex documentation reviewed on **2026-10-16**, with CLI examples and a [local experiment](experiments/README.md). The measured baseline is **Codex CLI 0.162.1** and **Claude Code 2.1.287**. Features documented for later versions are not assumed to work in those binaries.

## Follow one bounded assignment

Consider a library with billing functions in `money.mjs` and interval functions in `windows.mjs`. Its [specification](experiments/fixture/SPEC.md) gives the expected behavior of each export. A parent can assign one file to each worker, then reconcile the findings and run a combined check. The workers have independent questions and separate file ownership; the parent still owns whether the complete library satisfies the specification.

A useful handoff states the objective, relevant input, allowed edits, expected evidence, and stopping condition:

```text
Review money.mjs against SPEC.md. Own only this file; do not edit it.
Return each contract violation with the exported symbol, a concrete input,
expected behavior, and actual behavior. Ignore style preferences.
Do not delegate further. Stop after checking every export in this module.
```

Giving two workers the same request to “look for bugs” leaves their coverage and duplicated effort uncertain. Assigning different files makes ownership explicit, but does not make either result correct. The parent should reproduce findings and check interactions that neither worker saw.

## Define and start the workers

The [example configuration directory](experiments/examples/) accompanies the billing and scheduling fixture. Claude's measured workflow uses its custom worker definition. Codex's measured workflow uses native named workers and the concurrency configuration below; optional custom-role TOML is shown separately. Both workflows inherit the parent's model. When comparing alternatives, change model and effort deliberately: a cheaper model may need more retries or miss a finding. [Claude Code model configuration](https://code.claude.com/docs/en/model-config), [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

For Claude Code, create `.claude/agents/module-worker.md`:

```markdown
---
name: module-worker
description: Review or repair one explicitly assigned module against SPEC.md.
tools: Read, Glob, Grep, Edit, Write, Bash
model: inherit
---

Read SPEC.md and work only on the module assigned by the parent.
For review, do not edit files. Return defects with symbols and concrete examples.
For implementation, edit only your assigned module and verify its contracts.
Do not create further subagents. Return findings or changes and checks to the parent.
```

The YAML header configures the agent; the Markdown body supplies its instructions. For a worker that only reviews files, reduce `tools` to `Read, Glob, Grep`. That removes editing and shell tools, whereas the sentence “do not edit” alone is an instruction. [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents), [permission rules](https://code.claude.com/docs/en/permissions)

For a custom Codex role, the current documentation describes `.codex/agents/module-worker.toml`:

```toml
name = "module_worker"
description = "Review or repair one explicitly assigned module against SPEC.md."
developer_instructions = """
Read SPEC.md and work only on the module assigned by the parent.
For review, do not edit files. Return defects with symbols and concrete examples.
For implementation, edit only your assigned module and verify its contracts.
Do not create further subagents. Return findings or changes and checks to the parent.
"""
```

The documented schema requires those three fields, and Codex identifies a custom agent by its `name`. A worker inherits the parent's permission boundary. Start the parent with `codex --sandbox read-only` to enforce read-only shell execution. [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents), [sandbox and approval controls](https://learn.chatgpt.com/docs/agent-approvals-security)

Set explicit limits for this example. Claude Code's `.claude/settings.json` can contain:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "2",
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"
  }
}
```

The current documented defaults are 20 concurrent subagents and three layers of nesting. These controls require v2.1.217 or later, with the current nesting default dating from v2.1.219. The concurrency limit has documented exceptions for some features; it is not a total lifetime agent budget. [Claude Code environment variables](https://code.claude.com/docs/en/env-vars)

Codex's `.codex/config.toml` can contain:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 2
```

The cap counts open spawned threads and excludes the primary thread. Close completed workers when reusing the slots. Current configuration uses `agents.enabled`; `agents.max_threads` is a legacy alias for the cap. Avoid copying older experimental-feature examples without checking the installed version. [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

Start `claude` or `codex` in the repository, then ask:

```text
Use exactly two module-worker subagents concurrently: one reviews money.mjs,
the other reviews windows.mjs, against SPEC.md. Do not edit files or let workers
delegate further. Wait for both, reproduce their findings, and combine the result.
```

For Codex, the measured runs asked for two `module_worker` subagents with the TOML file above present. Both workers ran, but their records show `agentRole: null`: naming the custom role in the prompt did not select it in Codex CLI 0.162.1. The working minimum here is therefore the `[agents]` configuration plus an explicit task assignment; treat the custom role as unverified until a worker record names it. Claude Code can also select matching descriptions automatically; current local Codex documentation describes delegation after a direct request or applicable project or skill instructions. [Claude Code delegation](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly), [Codex delegation](https://learn.chatgpt.com/docs/agent-configuration/subagents#triggering-subagent-workflows)

## Compare the configuration and handoff

| Concern | Claude Code | Codex |
| --- | --- | --- |
| Project and personal definitions | `.claude/agents/*.md`; `~/.claude/agents/`; session definitions through `--agents`; managed and plugin scopes also exist | `.codex/agents/*.toml`; `~/.codex/agents/` |
| Instructions | YAML metadata plus a Markdown system prompt | TOML `developer_instructions` plus metadata |
| Model selection | `model`, including `inherit`; invocation and environment overrides exist | Parent model/effort, defaults under `[agents]`, explicit spawn settings, and custom-file overrides |
| Tool access | `tools` and `disallowedTools`; parent permissions still matter | Parent capabilities; supported feature and skill settings can reduce them |
| Permission boundary | Permission rules and modes are enforced independently of prose | Parent sandbox and approval policy; custom-agent instructions do not create a new sandbox |
| Normal workspace | Shared files unless isolation is requested | Shared files in this experiment; separate context does not isolate edits |
| Completion | Parent receives worker results and combines them | Parent coordinates worker threads and consolidates results |

Sources for the matrix: [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents), [CLI definitions](https://code.claude.com/docs/en/cli-reference), [permissions](https://code.claude.com/docs/en/permissions), [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents), and [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-reference).

### Separate context still needs a handoff

A normal Claude Code subagent starts with its own prompt and the parent's delegation message, rather than the main conversation's history or already-read files. Project instructions and explicitly preloaded skills can also load. A conversation fork is different: it inherits the existing conversation. The current `/subtask` command creates that kind of fork; older versions used another command name. Do not infer the context of an ordinary worker from fork behavior. [Claude Code startup context](https://code.claude.com/docs/en/sub-agents#what-loads-at-startup)

The tested Codex path creates children whose metadata identifies the parent as `forkedFromId`; their stored history includes prior instruction and conversation roles. Other spawn paths need separate checking: a new App Server thread and a fork of stored history are distinct operations. Pass the task, constraints, and file references explicitly. The experiment records its child metadata without asserting that every client transfers context the same way. [Codex App Server thread lifecycle](https://learn.chatgpt.com/docs/app-server), [experiment evidence](experiments/README.md)

The returning summary should contain what the parent needs to decide: findings, evidence, changed files, checks, unresolved questions, and any permission or tool failures. A summary saves main-context space by discarding intermediate detail, so keep the underlying artifacts accessible when a finding matters. This is a workflow recommendation, not a guarantee that summarization preserves every relevant fact.

### Product surfaces affect coordination

Codex CLI exposes `/subagents` for inspecting worker threads. The desktop app and IDE provide activity views; controls and availability depend on the client. ChatGPT Work runs hosted workers, so local TOML and sandbox examples should not be assumed to control it. [Codex surfaces and controls](https://learn.chatgpt.com/docs/agent-configuration/subagents#managing-subagents)

Claude Code distinguishes foreground and background workers, ordinary subagents, conversation forks, agent teams, and independent background sessions. This guide measures ordinary in-session workers through `claude -p`. It does not measure teams or the desktop experience. The CLI can emit child messages with `--forward-subagent-text`; this is useful for checking what actually happened. [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)

## Decide whether the split pays for itself

A rough planning model is:

```text
elapsed time with delegation ≈ decomposition + longest worker path
                              + waiting/retries + integration/verification
usage with delegation ≈ coordinator usage + all worker usage
```

Workers only shorten the part that can overlap. If a test must wait for an implementation, and that implementation must wait for a design decision, extra workers do not remove the dependency chain. More workers can also repeat instructions, read the same files, and produce conflicting conclusions.

| Work | A useful split | What the parent must resolve |
| --- | --- | --- |
| Research | Assign distinct questions or primary-source sets | Contradictory claims, source quality, missing evidence |
| Code review | Assign independent modules or clearly different risk areas | Duplicate findings, false positives, interactions across modules |
| Implementation | Assign stable interfaces and disjoint files | Interface compatibility, combined tests, conflicting assumptions |
| Testing | Investigate independent failures or platforms | Shared fixtures, environment differences, whether failures have one cause |
| Small or sequential changes | Keep the work together initially | Delegate only if a separate, checkable question emerges |

Start with the fewest workers that cover independent work. Specify file ownership before concurrent edits. Use separate worktrees when independent implementations would otherwise touch the same checkout, and inspect their diffs before integrating. Isolation prevents direct file contention; it does not resolve incompatible designs.

Treat model choice and agent count as separate variables. A larger team using a smaller model changes more than concurrency. First compare the same model and settings with and without delegation, then test a cheaper worker or another decomposition. Judge successful completion, verification effort, elapsed time, and total usage together. The [local comparison](experiments/README.md) fixes models within each product's pair; it does not compare equal token budgets or identify an optimal model or agent count.

## What effectiveness evidence establishes

| Evidence | What it reports | What it does not establish |
| --- | --- | --- |
| [Anthropic's research-system report, June 2025](https://www.anthropic.com/engineering/multi-agent-research-system) | Its Opus 4 coordinator with Sonnet 4 workers improved an internal research evaluation by 90.2% over single-agent Opus 4. It reports roughly 15× chat token usage for multi-agent systems and 4× for agents. | A 15× multiplier over a single coding agent, equal-resource gains, or performance of current Claude Code versus Codex. This is vendor evidence about a different system. |
| [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) | A cross-system study of 180 configurations across four benchmarks finds that task structure, tool overhead, and coordination architecture affect gains; sequential tasks can degrade. | A universal worker count or a direct evaluation of these installed CLIs. Its Google and academic authors study broader architectures. |
| [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) | An academic failure analysis identifies 14 failure modes involving specification/design, inter-agent alignment, and verification/termination. | The probability of a failure in this repository, or a product ranking. Some failure patterns also occur with one agent. |
| [Eight local CLI runs](experiments/README.md) | Fixed, inspectable inputs, answers, patches, timing, usage fields, and checks for two tiny tasks. | Statistical reliability, broad productivity gains, or independent human quality judgments. |

These sources support testing decomposition and coordination explicitly. They do not make worker count a substitute for verification. On work that already fits comfortably in one short session, a successful single-agent run provides the baseline a team must improve upon.

## Sources

- [Claude Code: Custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code: Model configuration](https://code.claude.com/docs/en/model-config)
- [Claude Code: Permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code: Environment variables](https://code.claude.com/docs/en/env-vars)
- [Claude Code: Costs and usage accounting](https://code.claude.com/docs/en/costs)
- [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI: Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [OpenAI: Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [OpenAI: Codex App Server](https://learn.chatgpt.com/docs/app-server)
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Kim et al.: Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296)
- [Cemri et al.: Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)

The documentation supplies changing product behavior; the papers and engineering report supply evidence with different tasks and controls. The local experiment supplies measurements for its stated environment. Practical recommendations above are an interpretation of those sources and results.
