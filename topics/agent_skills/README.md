# Agent Skills

An agent skill is a folder of instructions and supporting files that helps an AI agent carry out a particular task. These guides explain what goes in that folder, how agents find and use skills, and how to share them. A document-generation example shows how the pieces fit together.

## What each guide answers

- [Basics](basics.md)
  - What belongs in a skill folder, and what are `SKILL.md`, `scripts/`, `references/`, and `assets/` for?
  - How does an agent find a skill and read its files as needed?
  - How do you write, test, review, and improve a skill?
- [How many skills are too many?](managing-skills.md)
  - What happens when the agent's skill list becomes crowded?
  - Is there a safe number, and what limits do products document?
  - How do you trim, scope, disable, and test a collection?
- [Using scripts in a skill](scripts-and-mcp.md)
  - When is a script useful, and when would you use MCP instead?
  - Which languages and dependencies can a script use?
  - How should an agent run a helper and check its result?
- [How different products use skills](provider-differences.md)
  - What do Codex, Claude Code, Gemini CLI, Cursor, and Copilot share?
  - How do discovery, activation, permissions, and sharing differ?
  - How do local skills differ from skills attached through an API?
- [Storing and sharing skills](storage-and-distribution.md)
  - How do you store one skill or manage several skills in a Git repository?
  - Which existing templates and example repositories can you adapt?
  - How do you install selected skills, choose links or copies, and track versions?
  - How do you export a skill and install it for Codex?
  - When should you use plugins, team sharing, or a public directory?
- [Back up and restore personal skills with Git](backup-and-restore.md)
  - How do links let Codex and Claude Code use the same source files?
  - When should you share one version, keep agent-specific variants, or install copies?
  - How do branch changes affect installed skills, and what does a restore need?
- [Maintaining a personal skills repository](https://github.com/pomodorozhong/skills/blob/main/docs/maintaining.md) (in `pomodorozhong/skills`)
  - How do you import existing skills, preview links, and set up a machine?
  - How do you edit, add, remove, and synchronize skills?
  - How do you undo a link run and test the maintained scripts?
- [Document generation example](document-generation-example.md)
  - When should a task use a template, a generator, or a separate formatting skill?
  - Where should you put the document rules, template, and helper scripts?
  - How do you check the document's contents and page layout?

The [Agent Skills specification](https://agentskills.io/specification) defines the shared file format. Each product has its own rules for finding, starting, installing, and sharing skills. Check the linked documentation and the review date noted in each guide for current behavior.
