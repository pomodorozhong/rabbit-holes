---
name: learning-session
description: Teach a topic through conversation, keep a session log of what the user asked, understood, and concluded, then write a short learning note from that log. Use when the user wants to start or resume a learning session, or asks to write up, draft, or turn a learning session into a document. Not for drafting a guide the user has not discussed; use explanatory-writing or ai-research-report for that.
---

# Learning sessions

The user learns a topic by talking with the agent first, then has the agent write the document from what they discussed. Because every claim in the draft comes from something the user already understood, the user can audit the draft with confidence. The finished document is still a guide for a stranger: the user's future self may have forgotten the topic and will read it like someone new to it.

The skill has two modes. The user chooses the mode explicitly, for example "start a learning session on X" or "write up the session". If the request is unclear, ask which mode they mean.

## Mode 1: learning session

1. Open the session as a conversation, one short question per message, as described in [tutoring.md](references/tutoring.md#opening-the-session). Find out the topic, what the user already knows, and what they want to understand. Do not ask where the guide will live; that decision waits for the write-up.
2. Work on a branch whose name starts with `learning-session/`, for example `learning-session/<slug>`, even if the environment suggests another branch name.
3. Create or reopen the session log at `.agents/learning-session/YYYY-MM-DD-<slug>.md`, using [the session log template](assets/session-log-template.md). When resuming, read the existing logs for the topic in that folder first and pick up their open questions.
4. Teach by answering the user's questions. Follow [tutoring.md](references/tutoring.md). Do not draft the guide during this mode.
5. Update the log as the session goes: after each question is resolved, when the user states a view or pushes back, and before any long pause. Do not rely on the conversation to hold the details. Long conversations are summarized, and cloud sessions are discarded, so the log is the only durable record.
6. When the user ends the session, summarize the open questions and confirm the log is complete with them. Commit and push the log if the session runs in a cloud environment or the user asks for it.

## Mode 2: write-up

The write-up is a short, simple learning note, not a full topic document. It records what the session established so the user can come back to it, and it may be promoted to a topic document later.

1. Write the note at `learning-notes/<slug>.md`, outside `topics/`. Reuse the session's slug, or the existing note when the topic already has one. Move the topic's session logs from `.agents/learning-session/` to `learning-notes/sessions/`. Put the note elsewhere only when the user asks.
2. Read every session log for the topic, [the learning-notes index](../../../learning-notes/README.md), and the existing note if the topic already has one.
3. Read [the explanatory-writing skill](../explanatory-writing/SKILL.md) and its guide references. Apply them, with the overrides in [write-up.md](references/write-up.md). Those overrides concern where the content comes from, whose views the note states, and how short it stays.
4. Propose a brief outline before drafting: the reader's question and the headings in reading order. Let the user change it. The order can differ from the order of the conversation when a stranger needs ideas in a different sequence.
5. Draft the note from the log. Follow write-up.md for material the log does not cover.
6. Add or update the note's entry in `learning-notes/README.md`: a link and the questions it answers.
7. Deliver an audit list with the draft, as described in write-up.md, so the user can check every addition and judgment call.

## Promoting a note to a topic

When the user asks to promote a note, ask which folder under `topics/` it belongs in, or whether to create a new one named like the existing ones. Move the note there and its session logs to `topics/<topic>/sessions/`. Remove its entry from `learning-notes/README.md`. Then revise it into a full guide with explanatory-writing and add it to the topic README index, keeping the log as the source of the user's views.

## Delivery

In session mode, report where the log is and whether it was committed. In write-up mode, give the note's path, the audit list, and the checks actually run: review the diff, run `git diff --check`, and check any links added. Do not describe a claim as verified unless it was checked against a source during the session or the write-up.
