# Project guidance

This repository collects questions explored through topic READMEs, guides, research notes, notebooks, comparisons, and small experiments. Write for a curious reader who wants to understand the reasoning and return to the material later.

Reserve `topics/` for polished, fully reviewed documents and compact, interesting experiments. Keep shorter notes and material still being refined in `learning-notes/`. Notes distilled from existing research do not need a learning-session record.

<!-- handoff:start (from the handoff skill; edit the skill's template, not this copy) -->
## Handoff

`HANDOFF.md` at the repository root is how sessions resume. It has three sections: `In progress` (one `### <branch>` subsection per active branch, holding its state and its own approval requests), `Ranked work`, and `Pending` (approval requests not tied to a branch). A pending entry, such as `P-01`, records a request, not approval.

- **Start of a session:** read `HANDOFF.md` and the subsection for `git branch --show-current`; none means this branch has no work in progress. Compare its code checkpoint with `git log`, re-check verification made stale by later commits, and run the documented checks before building on it. If this branch's PR merged or closed, follow the `commit` skill's branch-safety rules before committing or pushing. Before recommending or starting work, show each unresolved request that existing authorization doesn't cover, from every branch subsection and `Pending` (marking any a merged or closed PR made obsolete), and each blocking decision in `Ranked work`, and ask the user about them. Pick new work from the default branch's `Ranked work`.
- **Edit only this branch's subsection,** plus `Ranked work` and `Pending` when they actually change. Keep it current rather than a log, and never write secrets.
- **Commit `HANDOFF.md`** only before a push and at wrap-up, as a `docs:` commit on the work branch. Never commit it on the default branch.
- **PRs:** use the `open-pr` skill, and keep its unanswered approval requests in this branch's subsection until they are resolved. **End of a session:** use the `handoff` skill.
- **Before creating a branch, editing `HANDOFF.md`, or resolving a conflict in it,** read the `handoff` skill's working rules (`references/working-rules.md` in that skill).
<!-- handoff:end -->

## Writing

Before drafting, substantially revising, or reviewing prose in a README, topic document, research report, or notebook, read and apply [the explanatory-writing skill](.agents/skills/explanatory-writing/SKILL.md). Read the relevant bundled references as directed by SKILL.md. This includes editorial changes within other research or notebook workflows. For a mechanical typo or link fix, use the defaults below without loading the full skill.

- Use calm, concrete wording and explain what happens and why.
- Introduce ideas in an order that builds understanding; connect examples with their interpretation.
- Use topic root READMEs to help readers choose documents by the questions they answer.
- In lessons and notebooks, keep explanations close to the relevant code, experiment, and result.
- Keep evidence and important limitations close to the claims they support.

Follow the user's requested audience, format, and scope. Preserve required topic or report formats. Apply the writing skill alongside relevant research and technical guidance. Routine code-only changes, PR descriptions, and chat replies do not require this writing skill unless the user requests it.

## Learning sessions

When the user wants to learn a topic by conversation, or asks to write up a learning session, read and apply [the learning-session skill](.agents/skills/learning-session/SKILL.md).

## Verification

For prose changes, review the final diff and run `git diff --check`. Check links that you add or change. If notebook prose refers to outputs, confirm the descriptions match the saved outputs; use the appropriate notebook checks if code or outputs also change.
