# Back up and restore personal skills with Git

A personal skills repository can hold the files your agents use every day. Link each skill folder into the agents' discovery folders, and edits made through those links land in the repository. Git then records the versions you want to keep, and a remote repository lets you restore them on another machine.

The runnable workflow is now maintained in [pomodorozhong/skills](https://github.com/pomodorozhong/skills). Use its [installation instructions](https://github.com/pomodorozhong/skills#install) to use the published skills, or [Maintaining these skills](https://github.com/pomodorozhong/skills/blob/main/docs/maintaining.md) to import, link, edit, back up, and recover your own collection. This guide explains the design and the choices to make when adapting it.

The maintained repository and the product documentation linked below were reviewed on 2026-10-14. Skill discovery and invocation were not tested in running agents.

## One source folder, two agents

For example, a checkout at `~/repo/skills` can serve both Codex and Claude Code:

```text
~/repo/skills/                          Git checkout
├── skills/commit/SKILL.md              Shared skill and its supporting files
├── scripts/import.sh                  Import existing installations
├── scripts/link.sh                    Create links and record recovery information
└── docs/maintaining.md                 Setup and maintenance instructions

~/.agents/skills/commit -> ~/repo/skills/skills/commit   Codex
~/.claude/skills/commit -> ~/repo/skills/skills/commit   Claude Code
```

Codex's personal discovery folder is `~/.agents/skills`; Claude Code's default is `~/.claude/skills`. Both document support for individual skill folders that are symlinks to directories elsewhere on disk. [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), [Claude Code skill locations](https://code.claude.com/docs/en/skills)

The links point to the same files. If an agent edits `~/.agents/skills/commit/SKILL.md`, Git sees a change to `skills/commit/SKILL.md` in the checkout. There is no second editable copy to synchronize. Keep each skill's references, assets, and helpers inside its folder so they travel with it.

Link each skill individually, leaving the agents' parent folders available for other installations and product-managed entries. Maintain your own source files in Git; reinstall bundled, synced, and plugin skills through the product that manages them. Record the source and reviewed revision of third-party skills separately.

## Choose links or installed copies

| Approach | Where edits land | How another machine gets the change |
| --- | --- | --- |
| Link directly to your Git checkout | In the source repository, including edits through an agent's skill path | Pull the saved revision and recreate links when skill folders change |
| Install independent copies | In the installed copy unless you edit the source explicitly | Reinstall the selected skills from the reviewed source revision |

Links suit a collection you actively maintain on your own machine. They depend on the checkout staying at the linked path and being accessible to the agent. Moving the checkout requires repairing the links. Copies suit environments where symlinks or access to the source checkout are a poor fit; decide how source edits will reach those installations. See [Install selected skills from a collection](storage-and-distribution.md#install-selected-skills-from-a-collection) for installation methods and version selection.

A symlink alone is not a backup. Commit the files you want to preserve and push them to your remote. Uncommitted edits remain local, and a source record or installer lock file cannot replace the skill's actual files.

## Decide which versions to share

Before importing, compare existing installations with the same name. Different instructions or executable permissions can change behavior. Merge the changes you want into one version if both agents should use it. If the instructions depend on one product's tools or invocation syntax, keep distinct versions and install each only for its intended agent.

The maintained example chooses **one shared version per skill**: every skill lives under `skills/` and is linked into both agents. Its [import script](https://github.com/pomodorozhong/skills/blob/main/scripts/import.sh) leaves existing repository entries alone and skips names whose installed copies differ, including differences in executable permissions. Resolve those names before importing them again.

This differs from the earlier workflow in [PR #207](https://github.com/pomodorozhong/rabbit-holes/pull/207), which put differing versions into `codex-only/` and `claude-only/`. The current scripts do not route those folders. If you need agent-specific variants, adapt the installation plan explicitly rather than putting them beside `skills/` and expecting the shared workflow to discover them.

## Keep the installed checkout on a reviewed version

The agent reads the files at the link target, including uncommitted edits. Switching branches in that checkout therefore changes the installed skill files. A separate Git worktree gives you another checkout where you can develop a change while the links keep pointing to the reviewed version.

For a collection reviewed through pull requests, keep the linked checkout on the branch containing accepted changes, develop in a separate worktree, and pull after a merge. If an agent edits through a link, inspect that diff and save it on a development branch before returning the linked checkout to its reviewed version. [Maintaining these skills: Keep main checked out](https://github.com/pomodorozhong/skills/blob/main/docs/maintaining.md#keep-main-checked-out)

A restore needs both the source files and the installation plan: clone the repository, recreate the links or copies, reinstall recorded dependencies, and try a sample request in each intended agent. A skill appearing in a selector checks discovery; a sample request checks whether its instructions and helpers work in that environment.

## Use the maintained scripts and recovery guide

The script copies formerly stored beside this guide have been removed. Get the scripts and their instructions together from the skills repository:

- [Maintaining these skills](https://github.com/pomodorozhong/skills/blob/main/docs/maintaining.md) covers machine setup, existing-skill imports, daily edits, branch management, and recovery.
- [scripts/import.sh](https://github.com/pomodorozhong/skills/blob/main/scripts/import.sh) copies existing personal skills into the shared collection.
- [scripts/link.sh](https://github.com/pomodorozhong/skills/blob/main/scripts/link.sh) previews and applies links, moves replaced folders aside, and records changes so a run can be undone.
- [Script fixture tests](https://github.com/pomodorozhong/skills/blob/main/tests/test_scripts.py) exercise the implementation in temporary folders.

Read the scripts and inspect the dry run before replacing installations. The current link script provides `--undo <run folder>`; follow [Undo a link run](https://github.com/pomodorozhong/skills/blob/main/docs/maintaining.md#undo-a-link-run) for its preview, ordering, and handling of entries changed since the run. The older scripts from PR #207 do not provide this option.

For a collection published to others, keep installation instructions and an example request for each skill in its README. [Storing and sharing skills](storage-and-distribution.md) covers repository layouts, selective installation, exports, and product distribution options.
