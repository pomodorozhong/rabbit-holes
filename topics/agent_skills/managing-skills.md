# How Many Skills Are Too Many?

Product details checked on 2026-09-29.

There is no universal maximum number of skills. A collection becomes too large for a particular setup when useful descriptions are cut short, relevant skills disappear from the model's initial list, or the agent keeps choosing the wrong skill. Count the skills the agent can see in this session, not just the folders stored on your computer.

## What happens when you install a lot of skills?

Installing a skill does not immediately load all its instructions and supporting files. With [progressive disclosure](basics.md#how-an-agent-reads-a-skill), the agent first sees a list of names and descriptions. Full instructions load when it uses a skill, and supporting files are accessed as needed. But the initial list still takes up context. [Agent Skills specification](https://agentskills.io/specification#progressive-disclosure)

There are two different problems:

- **The list gets crowded.** A product may shorten or remove descriptions, or leave some skills out of the list. The agent then has less information for choosing the right skill.
- **The choices overlap.** Several skills described as "write reports" or "review code" can be hard to tell apart even when the whole list fits. A larger context budget does not fix unclear descriptions. OpenAI's skill guidance recommends concise descriptions with specific triggers. [OpenAI skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

Loading many full skills during a task is a separate cost. Their instructions, references, and tool results also use context. A small catalog can still lead to a large conversation if the selected skills load extensive material. Keep both the initial list and the active workflow focused.

## How many is too many?

The documentation gives budgets for some products, rather than one safe skill count:

| Product | Documented behavior | What to watch for |
| --- | --- | --- |
| Codex | The initial skill list uses at most 2% of the model's context window, or 8,000 characters when the window size is unknown. Descriptions are shortened first; some skills may be omitted with a warning. | Truncated descriptions, omitted entries, and selection failures. The limit is for the initial list, not a selected skill's full instructions. [Codex guide](https://developers.openai.com/codex/skills) |
| Claude Code | The listing budget scales at 1% of the context window. All skill names remain listed, but some descriptions may be dropped, starting with less-used skills. | `/doctor` estimates the listing cost; `/context` shows its size after the budget is applied. [Claude Code guide](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) |
| Cursor and Gemini CLI | The documentation consulted for this guide does not give a comparable numerical catalog budget. | Check what the agent sees and test selection. Do not assume Codex's limit applies. [Cursor guide](https://prod.cursor.com/help/customization/skills), [Gemini CLI guide](https://geminicli.com/docs/cli/skills/) |

For a rough estimate, divide the available listing budget by the average size of a complete entry, including its name, description, path, and formatting where applicable. Keep the units consistent: tokens with tokens, or characters with characters.

For example, **if** a setup has an 8,000-character budget, an average entry of 200 characters would fit about 40 entries; an average of 800 characters would fit about 10. These are arithmetic examples before other overhead. They are not tested capacity limits, and the 8,000-character Codex fallback applies only when the model's context size is unknown. Actual trimming behavior can differ.

A description that fits can still be vague. Treat selection quality and product warnings as the deciding evidence, rather than aiming for a fixed number such as 20 or 100.

## How to prevent the problem

1. **Keep project skills with their project.** Use personal installations for skills you need across projects. Keep a larger library in Git, then install or enable only the relevant subset. See [Organizing skills in a repository](organizing-skills.md) and [Installing and sharing skills](installing-and-sharing-skills.md).
2. **Make descriptions short and distinct.** Put the task and its main trigger first. Move the steps, long examples, and background material into `SKILL.md` or references. For example, "Write a release briefing from approved change records; not for deployment" gives a clearer choice than "Help with releases."
3. **Remove duplicate installations.** Check project folders, personal folders, and plugins for copies of the same skill. Keep a reviewed source and a clear update process. Products handle duplicate names differently; see [Product differences](provider-differences.md).
4. **Group variants of one task.** If several skills do the same job for different formats, consider one skill that directs the agent to the right reference. Keep separate skills when they have different tasks or triggers. This reduces repeated descriptions without creating one giant skill for unrelated work.
5. **Disable skills you do not need.** Keep their files if you want to use them later. Making a skill manual-only controls automatic selection, but do not assume that setting removes it from every product's listing or saves a particular amount of context.
6. **Test after adding skills.** Try a request that names the skill, one that describes its task, and a related request that should not select it. If the direct request works but ordinary selection fails, inspect the description, competing skills, and listing budget before changing the workflow itself.

These are practical recommendations based on the loading model and authoring guidance. They are not a measured ranking of collection sizes.

## Codex: disable a skill without deleting it

In `~/.codex/config.toml`, add an entry using the installed skill's absolute path:

```toml
[[skills.config]]
path = "/absolute/path/to/release-brief/SKILL.md"
enabled = false
```

Replace the example path with the real one, then restart Codex. This disables that skill; `allow_implicit_invocation: false` instead keeps explicit invocation available while turning off automatic selection. [Codex configuration](https://developers.openai.com/codex/skills#enable-or-disable-local-codex-skills)

Do not increase a product's budget as the first fix. Trim and separate descriptions, remove duplicates, and narrow the active collection first. If you later raise a supported budget, retest selection and remember that the listing now takes more space from the rest of the conversation.

## Sources

- [Agent Skills specification: progressive disclosure](https://agentskills.io/specification#progressive-disclosure)
- [OpenAI: Build skills](https://developers.openai.com/codex/skills)
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Cursor: Skills](https://prod.cursor.com/help/customization/skills)
- [Gemini CLI: Agent Skills](https://geminicli.com/docs/cli/skills/)

No catalog-size benchmark was run for this guide. Product budgets can change; the example counts above are estimates, not guarantees.
