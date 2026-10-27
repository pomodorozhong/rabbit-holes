# Using subagents to reduce token cost

**Bottom line:** A skill can move an existing task into a focused worker with less conversation history or a cheaper model. Savings depend on the handoff, model calls, caching, and rework; adding agents alone does not establish a saving. *(As of 2026-10-27.)*

**What can save tokens or money?**

- **Less repeated context:** A worker can read source files, documents, or logs and return a compact result. This keeps bulky intermediate material out of later main-agent calls. The worker still consumes tokens, so a smaller main context does not prove lower total usage.
- **A cheaper model:** Routine investigation, extraction, drafting, or Git work can move to a lower-cost model. Codex otherwise inherits the parent's model and reasoning effort; its documentation names `gpt-6-luna` as an option for lighter work. [Model selection for subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
- **Replacing work:** One worker can take over the ordinary workflow. If the main agent then repeats the full investigation, the duplicate work can erase the benefit. Parallelism is optional.
- **Caching changes the comparison:** Compare cost across both agents using uncached input, cached input, and output including reasoning, plus retries. A fresh worker is not automatically cheaper than a fork that reuses relevant cached context. [Usage and cost accounting](https://developers.openai.com/api/docs/guides/agents-api/observability#model-usage-and-cost), [Claude fork and cache behavior](https://code.claude.com/docs/en/sub-agents#how-forks-differ-from-other-subagents)

**Minimal `SKILL.md` examples for Claude Code and Codex**

Both examples summarize one named file, making it easy to inspect the result. They are documentation-checked starting points, not examples installed or run during this session. The selected model and subagent capability must be available.

**Claude Code:** Save this as `.claude/skills/brief-file/SKILL.md` in a project.

```markdown
---
name: brief-file
description: Summarize one named file using a cheaper subagent.
context: fork
agent: Explore
model: haiku
---

Read the file at $ARGUMENTS without editing it.
Return its purpose, key facts, and open questions in at most
200 words. Cite the file and relevant line numbers.
```

Invoke `/brief-file README.md`. `context: fork` runs the skill in a separate subagent without conversation history, and `model` selects its model. A Claude Code *conversation fork* instead inherits history. [Skill execution](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent), [model frontmatter](https://code.claude.com/docs/en/skills#frontmatter-reference)

**Codex:** Save this as `.agents/skills/brief-file/SKILL.md` in a project.

```markdown
---
name: brief-file
description: Summarize one named file using a cheaper subagent.
---

Spawn one gpt-6-luna subagent without conversation history.
If the spawn tool exposes fork_turns, set it to "none";
otherwise use its supported fresh-context option.
If that option or model is unavailable, report the limitation.

Give the worker only the file path from the user's request
and this task: read the file without editing it; return its
purpose, key facts, and open questions in at most 200 words,
with file and line references.

Wait for the worker and present its result.
```

Invoke `$brief-file Summarize README.md.` Codex supports delegation requested in skill instructions. [Subagent triggers](https://learn.chatgpt.com/docs/agent-configuration/subagents#triggering-subagent-workflows), [skill invocation](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills)

`fork_turns: "none"` is the tool argument available in this session, not shared skill frontmatter or a promise about every Codex client. Claude Code uses its own mechanism above. Fresh context still includes required instructions and tools. For a shared skill, describe the context boundary in its body and keep runtime-specific details explicit. [OpenAI context-propagation control](https://developers.openai.com/api/docs/guides/responses-multi-agent)

**Next to try**

These are proposed changes to existing skills, not measured savings or changes already made. Links marked **local** point to installed copies on this Mac; repository-backed links point to the reviewed Git revision.

| Skill | Work a focused, cheaper worker could replace | Why it could save cost |
| --- | --- | --- |
| [commit](https://github.com/pomodorozhong/skills/blob/e8071f344cc6e315e38d253c47f01b0585382a51/skills/commit/SKILL.md) | Inspect the diff, choose atomic commits and messages, perform routine checks, and make authorized commits. | After a long coding chat, the worker may need only the repository, intended scope and reasons, exclusions, and validation evidence. It can perform the Git steps without the debugging history. Keep one Git writer. |
| [file-issue — local](/Users/pomodorozhong/.codex/skills/file-issue/SKILL.md) | Search duplicates, inspect relevant evidence, and prepare the complete issue draft. | A compact report of expected/actual behavior and reproduction details can replace the full conversation; bulky logs stay with the worker. Present the draft through the existing approval flow. |
| [file-pr — local](/Users/pomodorozhong/.codex/skills/file-pr/SKILL.md) and [open-pr](https://github.com/pomodorozhong/skills/blob/e8071f344cc6e315e38d253c47f01b0585382a51/skills/open-pr/SKILL.md) | For implemented work, gather branch and issue context, run routine checks, and prepare the PR review package. | The worker gets scope, rationale, base/head references, and test evidence rather than the whole implementation history. Preserve the existing approval checkpoints; choose the model separately for complex missing implementation. |
| [github-repo-comparison — local](/Users/pomodorozhong/.codex/skills/github-repo-comparison/SKILL.md) | Read documentation and releases; return source-linked records using shared metric definitions and one timestamp. | Detailed comparisons can involve much more source text than the final table needs. Basic star counts and commit dates are better collected with batched API requests. |
| [ai-research-report](../.agents/skills/ai-research-report/SKILL.md) | Extract specified facts from model cards, papers, and announcements. | Keep large source collections in workers; return evidence, source locations, and uncertainty. The main agent handles feasibility judgments, contradictions, and complete chapter coverage. |
| [learning-path-builder — local](/Users/pomodorozhong/.codex/skills/learning-path-builder/SKILL.md) and [decision-memo-from-research — local](/Users/pomodorozhong/.codex/skills/decision-memo-from-research/SKILL.md) | Assess resources or extract evidence for specific questions. | Useful when reading dominates. The main agent keeps the learner's goal, prerequisite order, tradeoffs, and final recommendation. |
| [macos-application-data-storage — local](/Users/pomodorozhong/.codex/skills/macos-application-data-storage/SKILL.md) and [handoff](https://github.com/pomodorozhong/skills/blob/e8071f344cc6e315e38d253c47f01b0585382a51/skills/handoff/SKILL.md) | Inventory storage paths or collect branch/issue status. | Large inventories can be bounded cheaply. The main agent must supply decisions and authorization that cannot be reconstructed from files or status alone. |
| [propose-stack](https://github.com/pomodorozhong/skills/blob/e8071f344cc6e315e38d253c47f01b0585382a51/skills/propose-stack/SKILL.md) | Gather bounded context or interpret lengthy check logs. | Parallel trial rebuilds primarily save elapsed time. For token savings, move existing reading or interpretation to a cheaper worker; test commands alone do not require another model. |

Even a small commit or filing task can be worth delegating when the parent conversation contains extensive unrelated history and the task needs several tool rounds. An extra independent review is a separate quality expense.

**Open**

- Run the two examples and confirm the worker's actual model and context behavior in each client.
- Compare one bounded task on the same inputs: main-agent execution versus a cheaper worker. Record uncached/cached input and output including reasoning across all calls, plus retries and the main agent's verification work; check that the result remains useful.
- Decide which skill to change after that comparison. None of the candidate skills was changed to add delegation, and no before/after saving was measured in this session.

The [session record](sessions/2026-10-27-subagents-for-token-savings.md) preserves the discussion and the correction about commit and issue/PR workflows.
