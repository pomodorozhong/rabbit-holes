---
name: learning-session
description: Teach a topic through conversation, keep a session log of what the user asked, understood, and concluded, then write a topic guide from that log. Use when the user wants to start or resume a learning session, or asks to write up, draft, or turn a learning session into a document. Not for drafting a guide the user has not discussed; use explanatory-writing or ai-research-report for that.
---

# Learning sessions

The user learns a topic by talking with the agent first, then has the agent write the document from what they discussed. Because every claim in the draft comes from something the user already understood, the user can audit the draft with confidence. The finished document is still a guide for a stranger: the user's future self may have forgotten the topic and will read it like someone new to it.

The skill has two modes. The user chooses the mode explicitly, for example "start a learning session on X" or "write up the session". If the request is unclear, ask which mode they mean.

## Mode 1: learning session

1. Agree on the topic, what the user already knows, and what they want to understand. Choose the topic folder: an existing folder under `topics/`, or a new one named like the existing ones.
2. Create or reopen the session log at `topics/<topic>/sessions/YYYY-MM-DD-<slug>.md`, using [the session log template](assets/session-log-template.md). When resuming, read the existing logs for the topic first and pick up their open questions.
3. Teach by answering the user's questions. Follow [tutoring.md](references/tutoring.md). Do not draft the guide during this mode.
4. Update the log as the session goes: after each question is resolved, when the user states a view or pushes back, and before any long pause. Do not rely on the conversation to hold the details. Long conversations are summarized, and cloud sessions are discarded, so the log is the only durable record.
5. When the user ends the session, summarize the open questions and confirm the log is complete with them. Commit and push the log if the session runs in a cloud environment or the user asks for it.

## Mode 2: write-up

1. Read every session log for the topic, the topic README, and any existing documents the guide would sit beside.
2. Read [the explanatory-writing skill](../explanatory-writing/SKILL.md) and its guide references. Apply them, with the overrides in [write-up.md](references/write-up.md). Those overrides concern where the content comes from and whose views the guide states.
3. Propose an outline before drafting: the reader's question, the section headings in reading order, and the log entries each section draws on. Let the user change it. The order can differ from the order of the conversation when a stranger needs ideas in a different sequence.
4. Draft the guide from the log. Follow write-up.md for material the log does not cover.
5. Update the topic README index as explanatory-writing describes.
6. Deliver an audit list with the draft, as described in write-up.md, so the user can check every addition and judgment call.

## Delivery

In session mode, report where the log is and whether it was committed. In write-up mode, give the guide's path, the audit list, and the checks actually run: review the diff, run `git diff --check`, and check any links added. Do not describe a claim as verified unless it was checked against a source during the session or the write-up.
