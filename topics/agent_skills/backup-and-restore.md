# Back up and install Codex and Claude Code skills from one Git repo

This guide keeps your personal skills in one Git repository and links each skill into the folders Codex and Claude Code read. The repository *is* the installation: when you or an agent edit a skill, the change lands in the repo, so backing up is `git commit && git push`, and setting up a new machine is `git clone` plus one script.

Checked on 2026-10-13 with Codex CLI 0.162.1, Claude Code docs as of that date, `skills@1.7.2`, and macOS's bundled bash 3.2. The scripts and the copy fallback were tested against a throwaway home folder: importing, linking, re-running, dry runs, removing a skill or moving it between folders, replacing existing folders and links, missing or empty repo folders, and each conflict check. Skill discovery inside running Codex and Claude Code sessions, Windows, and installing from a real private GitHub repo were not tested.

## How it works

| | Codex | Claude Code |
| --- | --- | --- |
| Personal skills folder | `~/.agents/skills` | `~/.claude/skills` (or `$CLAUDE_CONFIG_DIR/skills`) |
| Old folder still read | `~/.codex/skills` (deprecated) | — |
| Project skills folder | `.agents/skills/` | `.claude/skills/` |
| Follows a symlinked skill folder | Yes | Yes |
| Picks up edits live | Yes (about 10 s) | Yes |

Both agents use the same `SKILL.md` format and both document that a skill folder can be a symlink to a folder elsewhere on disk. So one repo can serve both:

```text
~/Projects/agent-skills/              ← Git repo, the only real copy
├── skills/commit/SKILL.md            ← shared by both agents
├── codex-only/…                      ← linked into Codex only
├── claude-only/…                     ← linked into Claude Code only
├── import.sh  link.sh  third-party.sh
└── README.md  .gitignore

~/.agents/skills/commit  → ~/Projects/agent-skills/skills/commit
~/.claude/skills/commit  → ~/Projects/agent-skills/skills/commit
```

Each skill is linked individually. `~/.claude/skills` stays a real folder, so Claude Code can still write its own `synced/` folder there, and Codex keeps its bundled skills in `~/.codex/skills/.system`.

What stays out of the repo:

- **Codex's `~/.codex/skills/.system`:** bundled skills that Codex regenerates.
- **Claude Code's `~/.claude/skills/synced/`:** skills that signed-in Claude Code downloads one-way from your claude.ai account. Local edits there are overwritten.
- **Plugin skills** under `~/.claude/plugins/` or `~/.codex/plugins/`: reinstall those from their marketplace.
- **Other people's skills:** record them in `third-party.sh` (step 7) instead of copying them.

## 1. Check your tools

```bash
git --version
rsync --version
node --version
```

`node` is only needed for third-party skills and the copy fallback. The scripts run with macOS's built-in bash.

## 2. Create the repository

```bash
REPO="$HOME/Projects/agent-skills"
mkdir -p "$REPO"
cd "$REPO"
git init
```

Keep `REPO` set for the rest of the guide. If you open a new terminal, set it again.

Choose the location carefully: every link points into this folder, so moving or deleting it breaks all your skills until you re-run `link.sh`.

## 3. Add the scripts

Copy these two scripts from this folder into the root of your repo:

- [import.sh](import.sh) copies the skills you already have into the repo. You run it once.
- [link.sh](link.sh) links every skill in the repo into both agents' folders. You can re-run it any time.

For example, from a checkout of this guide's folder:

```bash
cp import.sh link.sh "$REPO/"
chmod +x "$REPO/import.sh" "$REPO/link.sh"
```

Read both scripts before running them; they move folders in your home directory.

What `link.sh` does:

- checks the repo first and changes nothing if a name is in both `skills/` and an `-only/` folder, or if a shared or Claude Code skill is named `synced`, which Claude Code reserves;
- links `skills/*` into both agents, `codex-only/*` into `~/.agents/skills`, and `claude-only/*` into `~/.claude/skills`;
- moves any real folder it would replace into `~/skills-link-backup/<timestamp>-<pid>/` instead of deleting it, and prints the old target of any other link it replaces;
- moves old copies out of `~/.codex/skills` so Codex doesn't list each skill twice, leaving `.system` alone;
- removes links into the repo for skills you deleted or moved to another folder.

`./link.sh --dry-run` prints every command it would run without changing anything. It accepts no other arguments. Missing or empty `skills/`, `codex-only/`, or `claude-only/` folders are fine; Git doesn't keep empty folders, so a fresh clone may not have them.

## 4. Import your existing skills

Skip this step if you are starting with no skills.

First, take inventory. `import.sh` copies every skill folder it finds, including skills you installed from someone else, so note which ones aren't yours:

```bash
ls ~/.agents/skills ~/.codex/skills ~/.claude/skills 2>/dev/null
cat ~/.agents/.skill-lock.json 2>/dev/null
```

Skills listed in `.skill-lock.json` were installed with `npx skills`, and the file shows where each came from. Skills installed with Codex's `$skill-installer` or copied by hand leave no record, so check any name you don't recognize.

Then import:

```bash
cd "$REPO"
./import.sh
find skills codex-only claude-only -name SKILL.md | sort
```

`import.sh` reads `~/.agents/skills`, `~/.codex/skills`, and `~/.claude/skills`. If the two Codex folders hold *different* skills with the same name, it stops without importing anything and names them; keep one version, move the other out of both folders, and run it again. A skill only one agent has, or both have with identical files, goes to `skills/`. A skill both agents have with *different* files goes to both `codex-only/` and `claude-only/`, and the script prints `DIFFERENT in each agent, review: <name>`.

For each of those, compare the two versions:

```bash
diff -r codex-only/commit claude-only/commit
```

Then either keep both, or merge them into one shared copy:

```bash
mv codex-only/commit skills/commit    # after merging the changes you want into it
rm -rf claude-only/commit
```

Remove third-party skills from the repo now, before linking, and add them to `third-party.sh` (step 7) instead:

```bash
rm -rf skills/some-third-party-skill
```

Their installed copies stay where they are; `link.sh` only touches names that are in the repo.

Also move any skill that only makes sense for one agent into its `-only/` folder. For example, move a skill whose instructions mention `$skill-name` invocation or Codex-only tools into `codex-only/`.

Check each `SKILL.md` before committing. Remove secrets, private examples, and machine-specific paths. Helper scripts inside skills are the most common place for leaked tokens.

## 5. Link and verify

Preview first:

```bash
cd "$REPO"
./link.sh --dry-run
```

Each `mv` line shows an existing entry that will be moved to `~/skills-link-backup/`, and each `replacing link` line is a link that will be re-pointed. If any of them surprise you, stop and check the repo. Then link and save the terminal output, including the old link targets:

```bash
mkdir -p "$HOME/skills-link-backup"
RUN_OUTPUT="$(mktemp "$HOME/skills-link-backup/run-output.XXXXXX")"
./link.sh 2>&1 | tee "$RUN_OUTPUT"
echo "Run output saved to $RUN_OUTPUT"
ls -l ~/.agents/skills ~/.claude/skills
ls -A ~/.codex/skills
```

Every personal skill you kept in the repo should have an arrow into `$REPO` in its intended agent folders. Third-party installations and Claude Code's `synced` folder may remain beside those links. In `~/.codex/skills`, migrated names should be gone; `.system` and any unrelated installations remain. Use your configured folders instead of these defaults if you set `CLAUDE_CONFIG_DIR` or `CODEX_HOME`.

The saved output is your record for manual recovery. The run succeeded if its last line is `Linked skills from …`. If it isn't, stop and read the output: there is no automatic rollback, and changes made before the failure remain.

Then check in each agent:

- **Codex:** run `/skills` in the CLI or IDE extension, or open the Skills view in the desktop app. Each skill should appear **once**. Invoke one with `$skill-name`.
- **Claude Code:** start a new session and type `/` to see your skills, then invoke one with `/skill-name`. If `/skills` shows nothing but `/skill-name` works, it's a known listing bug with symlinked skills, not a broken link.

If Codex disables any skills in `~/.codex/config.toml`, check how:

```bash
grep -n -A2 'skills.config' ~/.codex/config.toml
```

Entries with `path = "…/.codex/skills/…"` no longer match after the move. Change them to `name = "skill-name"` entries, which work on every machine.

When both agents list each intended skill once and the old folders are no longer needed, you can delete that run's backup folder. Keep its transcript until you no longer need the old link targets.

To recover a replaced entry by hand:

1. Find it in the saved output: an `mv` line for a folder, or a `replacing link … (was -> …)` line for a link.
2. Delete only the new link, after checking with `readlink` that it points into this repo.
3. Move the folder back from `~/skills-link-backup/<timestamp>-<pid>/`: entries in `codex/` go to `~/.agents/skills/`, `claude/` to `~/.claude/skills/`, and `codex-legacy/` to `~/.codex/skills/`.
4. For a link, recreate it with the exact old target, for example `ln -s '<old target>' ~/.claude/skills/<name>`.

Recover only the entries you need; leave the rest alone.

## 6. Commit and push

Create `.gitignore`:

```gitignore
.DS_Store
__pycache__/
*.pyc
.import/
```

Create `README.md` listing each skill, what it does, and a sample prompt you can use to test it after a restore.

```bash
cd "$REPO"
git add -A
git status --short
git diff --cached --check
git commit -m "chore: add personal agent skills"
git branch -M main
```

On GitHub, create an empty **private** repository named `agent-skills`, then:

```bash
git remote add origin git@github.com:YOUR-USER/agent-skills.git
git push -u origin main
```

Use the HTTPS URL instead if that's how you authenticate. To catch secrets before they're pushed, add a scanner such as [gitleaks](https://github.com/gitleaks/gitleaks) as a pre-commit hook.

## 7. Record third-party skills

Don't copy other people's skills into the repo. Record how to reinstall them instead, pinned to a commit. Save this as `third-party.sh`:

```bash
#!/usr/bin/env bash
# Reinstall third-party skills for Codex and Claude Code. Edit the list, then run.
set -euo pipefail
export DISABLE_TELEMETRY=1
add() { npx -y skills@1.7.2 add "$@" -a codex -a claude-code -g -y --copy; }

# add "owner/repo#<commit-sha>" --skill some-skill
```

Make it executable and commit it:

```bash
chmod +x "$REPO/third-party.sh"
```

Add one `add` line per skill. `--copy` gives each agent its own files. Pinning `#<commit-sha>` keeps the version fixed until you change it. To update, change the SHA and run the script again. Don't use `npx skills update`: it reinstalls without `--copy`, and it never picks up skills added to the source repo later.

Don't use the same name for a third-party skill and one of your own: the script and `link.sh` would overwrite each other.

## Daily use

**Edit a skill:** edit it in the repo, or let an agent edit it through the link. Either way the change is already in the repo. Back it up:

```bash
cd "$REPO"
git status
git diff
git add -A
git commit -m "chore: update skills"
git push
```

**Add a skill:** create `skills/<name>/SKILL.md` (or under `codex-only/` or `claude-only/`), then run `./link.sh`.

**Remove a skill:** delete its folder from the repo, then run `./link.sh` to remove the links.

**Pull changes made on another machine:**

```bash
cd "$REPO"
git pull
./link.sh
```

`link.sh` is only needed when skills were added or removed. Edits to existing skills appear immediately.

## Set up a new machine

```bash
git clone git@github.com:YOUR-USER/agent-skills.git "$HOME/Projects/agent-skills"
cd "$HOME/Projects/agent-skills"
./link.sh
[ -f third-party.sh ] && bash third-party.sh
```

The last line installs third-party skills, if you created `third-party.sh`. Then verify as in step 5, and run a few sample prompts from the README.

## Fallback: install copies instead of links

Use this when symlinks are a poor fit: Windows without symlink permission, a `~/.claude` that is itself a symlink managed by a dotfiles tool, or a sandbox that only sees real files.

Install each repo folder separately, so each skill goes only to its intended agents:

```bash
npx -y skills@1.7.2 add YOUR-USER/agent-skills/skills --skill '*' -a codex -a claude-code -g -y --copy
npx -y skills@1.7.2 add YOUR-USER/agent-skills/codex-only --skill '*' -a codex -g -y --copy
npx -y skills@1.7.2 add YOUR-USER/agent-skills/claude-only --skill '*' -a claude-code -g -y --copy
```

Skip a line if that folder doesn't exist in your repo. Don't install the whole repo in one command: the CLI doesn't know about `codex-only/` and `claude-only/`, and depending on which folders exist it either skips them or installs them into both agents.

These commands copy skills into `~/.agents/skills` and `~/.claude/skills`, using your existing Git credentials for a private repo. The copies don't track the repo: edit in the repo, push, and re-run the same command to update. Don't use `npx skills update` for these.

Without `-g`, the same command installs into the current project (`./.agents/skills`, `./.claude/skills`) and writes `./skills-lock.json`. Use that form to give one project its own copies. `skills-lock.json` lists where skills came from; it does not contain them, so it isn't a backup.

## Sharing with a team

For your own skills, links are simpler. To share skills with teammates, or with cloud sessions that can't see your home folder, package them as a plugin marketplace instead. Claude Code installs with `claude plugin marketplace add YOUR-USER/repo` and Codex with `codex plugin marketplace add YOUR-USER/repo`. Both read a `.claude-plugin/marketplace.json`. Plugin skills are renamed to `plugin-name:skill-name` and served from a cache copy, so don't also link the same skills, or Claude Code loads both. See [Storing and sharing skills](storage-and-distribution.md).

## Troubleshooting

- **A skill appears twice in Codex:** an old copy is still in `~/.codex/skills`. Run `./link.sh`, which moves it aside, or check for a same-named skill installed by `third-party.sh`.
- **A skill is missing:** check that `skills/<name>/SKILL.md` exists with `name` and `description` frontmatter, run `./link.sh`, and start a new session. `link.sh` skips folders without `SKILL.md`.
- **Links are broken (`ls -l` shows red, or the skill fails to load):** the repo moved or was deleted. Put it back, or re-run `./link.sh` from the new location; it replaces the old links.
- **`link.sh` stops with "Nothing changed. Fix these first":** it lists each problem. A name is in `skills/` and an `-only/` folder (keep one), or a skill is named `synced` (rename it).
- **`import.sh` stops with "Nothing imported":** the same skill name has different contents in `~/.agents/skills` and `~/.codex/skills`. Keep one version and run it again.
- **Claude Code `/skills` is empty but `/skill-name` works:** a listing bug with symlinked skills. The skills still load.
- **A Codex skill is unexpectedly disabled or enabled:** fix the `[[skills.config]]` path entries as in step 5.

## References

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills): skill locations, symlinks, `[[skills.config]]`
- [Claude Code: Skills](https://code.claude.com/docs/en/skills): skill locations, symlinked skill folders, claude.ai sync
- [Claude Code: Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)
- [Vercel `skills` CLI](https://github.com/vercel-labs/skills) and issues [#1199](https://github.com/vercel-labs/skills/issues/1199) (`update` drops `--copy`), [#591](https://github.com/vercel-labs/skills/issues/591) (`update` misses new skills), [#683](https://github.com/vercel-labs/skills/issues/683) (no global restore)
- [Storing and sharing skills](storage-and-distribution.md)
