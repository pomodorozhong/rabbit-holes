# Handoff

## In progress

### codex/context-files-video-research

- Task: research instruction files and skill workflows
- PR: #212, ready for review, mergeable when last checked
- Code checkpoint: 817d537, rebased onto `master` after #208
- State: awaiting review and merge. Its two reports hold the three video appendices: one in `repository-instructions-evidence.md`, two in `theo-skills-workflows.md`.
- Verification: `git diff --check` passed and all 70 local links in the topic resolve. External links not re-run after the rebase.
- Next action: review, and decide where its two guides belong in the topic index. They were added after "How many skills are too many?" only to resolve the rebase conflict.

### docs/ab-test-math

- Task: #231 the math of an A/B test
- PR: #247, draft, holds only a plan
- Code checkpoint: 4de8d3d
- State: plan filed; guide, figures and script not written
- Verification: `git diff --check` passed; the plan's external links returned 200; its sources haven't been read
- Next action: write `topics/indie-hacking/ab-test-math/README.md` following the plan, recomputing every number
- Avoid: merging the plan alone

### docs/cpp-header-note

- Task: #54 and #58 C++ include guards and header cycles
- PR: #250, draft
- Code checkpoint: ba1debf
- State: awaiting review
- Verification: the example builds and prints `July`; a two-header cycle failed with `unknown type name 'Report'`; external links returned 200. Only tested with one compiler.
- Next action: review the note, then mark the PR ready

### docs/git-topic-guides

- Task: #38, #75, #103 and #217 focused Git guides behind the topic hub
- PR: #249, draft
- Code checkpoint: 7078250
- State: three guides, two figures and hub entries are awaiting review. #104 stays open.
- Verification: the recovery and large-file exercises ran, with `git-filter-repo` through `uvx`; figures rendered locally; links resolve. Figures not viewed on GitHub.
- Next action: check the figures on GitHub, review the guides, then mark the PR ready
- Avoid: drawing a feature-flag change as a point on the commit line, because it isn't a commit

### docs/hashing-plan

- Task: #10 what hash functions are used for
- PR: #248, draft, holds only a plan
- Code checkpoint: 452ae2b
- State: plan filed; the six documents and hub not written
- Verification: `git diff --check` passed; the plan's external links returned 200; its sources haven't been read
- Next action: write the documents in `topics/hashing/`, then replace the plan with the hub
- Avoid: merging the plan alone, because the PR closes #10

### docs/session-handoff

- Task: carry this file and the handoff block in `AGENTS.md`
- PR: none yet
- Code checkpoint: adf5476, plus the `docs:` commits that update this file
- State: pushed, not merged, so `HANDOFF.md` isn't on `master` yet
- Verification: `git diff --check` passed
- Next action: answer P-02
- Pending: **P-02** open and merge a PR for this branch. Why: opening a PR needs approval. Blocks: finding this file from `master`.

## Ranked work

1. #249 Review the Git guides
2. #250 Review the C++ note
3. #212 Review and merge
4. #248 Write the hashing documents
5. #247 Write the A/B test guide
6. #245 Build the interactive sampled-sound page
7. #246 Write the inverse square root note with figures
8. Triage the remaining open issues, oldest first

## Pending

- **P-03** Delete the remote branch `codex/temp-skill-test`. Its report is replaced on `master`, and the later weekly template covers most of its skill rules. Only small points would be lost, such as sourcing each named system separately within a combined chapter. Why: deletion needs approval. Blocks: nothing else.
- **P-04** Decide each old draft PR. Suggested: #152 move to `learning-notes/` or close; #145 close and move anything useful to #143; #114 rework into a short note or close. All three add files under the old `researches/` path. Why: closing a PR needs approval. Blocks: nothing else.
- **P-05** Decide the report branch `comparing-codex-models`: three unread reports at the repo root, which someone else ran for the owner. Move them or delete the branch. Why: moving or deleting needs approval. Blocks: nothing else.
- **P-06** Decide `feat/handoff-pre-commit-hook` in the `pomodorozhong/skills` repository, which exists only locally and has its own worktree: open a PR or delete it. It adds a hook that keeps `HANDOFF.md` off the default branch. Why: opening a PR or deleting needs approval. Blocks: nothing else.
