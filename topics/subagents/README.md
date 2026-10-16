# Subagents

A subagent takes a bounded piece of work from a parent agent, works in a separate conversation, and returns a result for the parent to check and combine. These notes explore how that arrangement works in Claude Code and Codex, and when its extra coordination is useful.

- [Configure subagents and decide when to delegate](configuration-and-effectiveness.md)
  - How do Claude Code and Codex define, invoke, and coordinate subagents?
  - Which instructions, context, models, tools, and permissions reach a worker?
  - When do independent tasks justify the extra time and usage?
  - Can moving subagent work to a cheaper model make subscription limits last longer?
  - What do vendor reports and broader evaluations establish?
- [A small single-agent versus subagent comparison](experiments/README.md)
  - How can the same review and repair tasks be run with and without delegation?
  - What happened in eight runs of the installed CLIs?
  - How were correctness, elapsed time, usage, and actual delegation checked?

Product documentation was reviewed on 2026-10-16. The experiment records its exact CLI versions and model settings; documented behavior on another surface is not a measurement of that surface.
