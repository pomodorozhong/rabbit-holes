---
name: learning-session
description: Teach a topic through conversation, keep a session log of what the user asked, understood, and concluded, then write a short learning note or a topic guide from that log. Use when the user wants to start or resume a learning session, or asks to write up, draft, or turn a learning session into a document. Not for drafting a guide the user has not discussed; use explanatory-writing or ai-research-report for that.
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

The write-up records what the session established so the user can come back to it. It takes one of two forms:

- **Learning note** (the default): a short, simple note in `learning-notes/`. It suits a session that settled a few questions, and it can be promoted to a topic guide later.
- **Topic guide:** a full guide under `topics/`, written with explanatory-writing. It suits a session that covered enough to teach the topic to a stranger.

1. Choose the form. Use the one the user named. Otherwise, suggest one based on how much the session covered and ask the user to confirm.
2. Choose the location and move the logs:
   - **Learning note:** write it at `learning-notes/<slug>.md`. Reuse the session's slug, or the existing note when the topic already has one. Move the topic's session logs from `.agents/learning-session/` to `learning-notes/sessions/`.
   - **Topic guide:** ask which folder under `topics/` it belongs in, or whether to create a new one named like the existing ones. Move the topic's session logs to `topics/<topic>/sessions/`.

   Put the document elsewhere only when the user asks.
3. Read every session log for the topic and the index the document will join: [the learning-notes index](../../../learning-notes/README.md) for a note, or the topic README for a guide. Also read the existing note, or the documents the guide would sit beside.
4. Read [the explanatory-writing skill](../explanatory-writing/SKILL.md) and its guide references. Apply them, with the overrides in [write-up.md](references/write-up.md). Those overrides concern where the content comes from, whose views the document states, and how long it runs.
5. Propose an outline before drafting: the reader's question and the headings in reading order. For a guide, also name the log entries each section draws on. Let the user change it. The order can differ from the order of the conversation when a stranger needs ideas in a different sequence.
6. Draft the document from the log. Follow write-up.md for material the log does not cover.
7. Update the index: add or update the note's entry in `learning-notes/README.md`, with a link and the questions it answers, or update the topic README index as explanatory-writing describes.
8. Deliver an audit list with the draft, as described in write-up.md, so the user can check every addition and judgment call.

## Promoting a note to a topic

When the user asks to promote a note, ask which folder under `topics/` it belongs in, or whether to create a new one named like the existing ones. Move the note there and its session logs to `topics/<topic>/sessions/`. Remove its entry from `learning-notes/README.md`. Then revise it into a full guide as the write-up describes for a topic guide, and add it to the topic README index, keeping the log as the source of the user's views.

## Delivery

In session mode, report where the log is and whether it was committed. In write-up mode, give the document's path, the audit list, and the checks actually run: review the diff, run `git diff --check`, and check any links added. Do not describe a claim as verified unless it was checked against a source during the session or the write-up.
