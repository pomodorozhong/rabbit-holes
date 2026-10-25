# Project guidance

This repository collects questions explored through topic READMEs, guides, research notes, notebooks, comparisons, and small experiments. Write for a curious reader who wants to understand the reasoning and return to the material later.

Reserve `topics/` for polished, fully reviewed documents and compact, interesting experiments. Keep shorter notes and material still being refined in `learning-notes/`. Notes distilled from existing research do not need a learning-session record.

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
