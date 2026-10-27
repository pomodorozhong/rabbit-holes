# Writing up a session

## Reader and voice

Write for a stranger to the topic. That includes the user months later, who may have forgotten most of it. Apply explanatory-writing for structure, pacing, terminology, and evidence: introduce ideas in the order the reader needs them, define terms before using them, and keep sources beside claims.

The session log and session record shape the write-up in the following ways:

- **Views recorded in the log or record are the user's own.** State them as the user's views or in first person, as the repository's existing documents do. Do not neutralize them into generic advice. Views that are in neither still must not be attributed to the user.
- **The session sets the scope.** The document covers what the session covered. Turn the questions the user asked into the document's questions and its entry in the learning-notes index or the topic README.
- **Keep a learning note compact.** A learning note follows [the learning note template](../assets/learning-note-template.md): a bottom line that answers the main question, then one short block of bullets per session question, a table only when the session compared options or checked coverage, and open questions. Use bold labels instead of headings, and write each bullet as a complete sentence so it still makes sense months later. Leave a fuller treatment, with worked examples and broader context, for a topic guide. A topic guide follows explanatory-writing's guide guidance for length and depth, still within the scope of the session.
- **Give personal context a specific place and label.** Include user-stated goals, constraints, decisions, or hypotheses where they affect an answer or add a distinct conclusion. Place them beside the relevant explanation; use a label such as `Decision`, `Goal and fallback`, or `Hypothesis to test` when a separate block helps. Do not add a catch-all `For me` section or repeat the summary, next steps, or open questions. Keep proposed recommendations distinct from decisions the user actually made.

## Material the session does not cover

A stranger may need context the session skipped, such as a definition the user already knew or a step needed to connect two ideas. Add only what the reader needs to follow the document. Keep additions short, and list each one in the audit list.

Do not expand into subtopics the user did not discuss. List them as possible gaps in the audit list instead. Leave out topics the user explicitly set aside, or name them briefly as out of scope when a reader would expect them.

Carry unchecked claims into the document only with a qualification, or check them now and cite the source. Turn open questions into a short "Open questions" section when they help a reader know where the document stops.

## Audit list

Give the user the audit list in the chat reply, or in the pull request description if a PR is requested. Keep it out of the document itself. It contains:

- **Additions:** each passage not grounded in the log or record, with its location in the document and why a stranger needs it.
- **Reordering:** where the document's order departs from the conversation, and why.
- **Checks:** claims checked during the write-up, with sources, and any claims still unchecked.
- **Possible gaps:** subtopics a reader might expect that the session did not cover.

If an item cannot be grounded in the log, the record, or a source, raise it with the user rather than writing it in.
