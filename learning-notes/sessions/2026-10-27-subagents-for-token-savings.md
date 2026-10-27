# Session record: Subagents, skills, and token cost, 2026-10-27

## Starting point

- **Already knew:** The user was familiar with the terms skill and subagent, but prior hands-on use was not established.
- **Wanted to understand:** Whether Claude Code and Codex skills can launch subagents, whether fresh context is portable, and which personal skills could reduce token usage or cost through delegation.

## Questions and conclusions

### Can a skill launch a subagent?

- **Covered:** Claude Code has a skill execution setting for a separate worker. Codex can follow delegation instructions in a skill body. The session compared the two mechanisms and provided illustrative workflows.
- **Check:** Documentation checked; no skill was installed or executed, and understanding was not checked by restatement.
- **Sources:** [Claude Code skill execution](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent), [Codex subagent triggers](https://learn.chatgpt.com/docs/agent-configuration/subagents#triggering-subagent-workflows), and [Codex skill invocation](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills).

### Is the fresh-context setting shared?

- **Covered:** The exact `fork_turns` argument belongs to the tool exposed in this session. It is not portable skill frontmatter. Claude Code's isolated skill execution differs from a conversation fork. Required instructions and tools still contribute context.
- **Check:** The current tool interface and official documentation were inspected. Other clients' exact tool interfaces were not tested.
- **Sources:** [OpenAI multi-agent context control](https://developers.openai.com/api/docs/guides/responses-multi-agent) and [Claude Code subagent startup context](https://code.claude.com/docs/en/sub-agents#what-loads-at-startup).

### How could delegation reduce usage or cost?

- **Covered:** A narrower worker can keep source text and intermediate output out of later main-agent calls. A lower-cost model can reduce expense even if total tokens increase. Handoff, duplicate work, caching, reasoning, and retries affect the complete comparison.
- **Check:** This is a mechanism and proposed optimization, not a measured result.
- **Sources:** [Codex subagent model selection](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning), [usage accounting](https://developers.openai.com/api/docs/guides/agents-api/observability#model-usage-and-cost), and [Claude fork/cache comparison](https://code.claude.com/docs/en/sub-agents#how-forks-differ-from-other-subagents).

### Which existing skills are candidates?

- **Covered:** The review inspected 14 personal skills in the legacy Codex skills folder and six in the shared skills repository; their six user-level symlinks were counted once. Three project-local skills were also considered. Source-heavy research, comparison, resource assessment, and inventories are plausible candidates for cheap extraction workers.
- **Correction:** The first review emphasized speed and extra review coverage. The user redirected the objective to cost. Commit and issue/PR filing can also benefit when one cheaper worker replaces the ordinary workflow with a compact task packet, especially after a long implementation conversation. Parallel execution is not required.
- **Check:** Static review only. No comparative usage or quality test was run.
- **Sources:** The local skill files reviewed during the session; specific candidates and links are in [the learning note](../06-subagents-for-token-savings.md).

## The user's views and conclusions

- The user prioritizes token or cost savings through narrower task context or a cheaper worker model.
- The user specifically challenged the omission of commit and issue/PR filing as cost-saving candidates.
- The user requested a learning note with separate minimal Claude Code and Codex skill examples and a next-to-try section linking to personal skills with reasons.
- On reviewing the note, the user found its personal-takeaway paragraph redundant. It repeated the cost-saving objective without adding a distinct decision, so that paragraph was removed.
- The user also requested clearer labels for personal context. The template and earlier-note revisions are tracked separately from this subagent write-up.

## Set aside

- The candidate skills were not changed to add subagent delegation. The personal-context template follow-up is a separate change.
- No GitHub issue, PR, or external publication was created during the learning discussion.
- The session did not install or run the examples or benchmark cost savings.

## Open questions

- Do the documented examples execute with the selected models and intended context boundary in the user's clients?
- Which bounded task demonstrates a worthwhile total saving at acceptable quality?
- Which candidate skill should be changed after that measurement?
