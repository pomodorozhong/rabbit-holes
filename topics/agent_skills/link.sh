#!/usr/bin/env bash
# Link every skill in this repo into the Codex and Claude Code personal skill folders.
# Safe to re-run. Real folders it would replace are moved to ~/skills-link-backup/<timestamp>-<pid>/.
# Usage: ./link.sh [--dry-run]
set -euo pipefail

DRY=0
if [ "$#" -gt 0 ]; then
  if [ "$#" -eq 1 ] && [ "$1" = --dry-run ]; then
    DRY=1
  else
    echo "Usage: $0 [--dry-run]" >&2
    exit 2
  fi
fi

REPO="$(cd "$(dirname "$0")" && pwd)"
CODEX_DIR="$HOME/.agents/skills"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
LEGACY_CODEX_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
BACKUP="$HOME/skills-link-backup/$(date +%Y%m%d-%H%M%S)-$$"

run() {  # print and run a command, or only print it in dry-run mode
  echo "+ $*"
  [ "$DRY" = 1 ] || "$@"
}

# List skill folders (folders with SKILL.md) in one repo folder. Missing or empty folders are fine.
skills_in() {
  local d
  [ -d "$REPO/$1" ] || return 0
  for d in "$REPO/$1"/*/; do
    [ -f "$d/SKILL.md" ] && basename "$d"
  done
  return 0
}

# Check everything before changing anything.
problems=""
for n in $(skills_in skills); do
  [ -d "$REPO/codex-only/$n" ] && problems="$problems\n  '$n' is in skills/ and codex-only/"
  [ -d "$REPO/claude-only/$n" ] && problems="$problems\n  '$n' is in skills/ and claude-only/"
done
for n in $(skills_in skills) $(skills_in claude-only); do
  # Claude Code reserves 'synced' (any capitalization) for skills synced from claude.ai.
  [ "$(echo "$n" | tr '[:upper:]' '[:lower:]')" = "synced" ] &&
    problems="$problems\n  '$n' is reserved by Claude Code; rename it or move it to codex-only/"
done
if [ -n "$problems" ]; then
  printf "Nothing changed. Fix these first:$problems\n" >&2
  exit 1
fi

# Desired links: one "<agent folder>/<name> <TAB> <repo skill folder>" per line.
PLAN=""
plan() { PLAN="$PLAN$2/$1	$REPO/$3/$1
"; }
for n in $(skills_in skills);      do plan "$n" "$CODEX_DIR" skills; plan "$n" "$CLAUDE_DIR" skills; done
for n in $(skills_in codex-only);  do plan "$n" "$CODEX_DIR" codex-only; done
for n in $(skills_in claude-only); do plan "$n" "$CLAUDE_DIR" claude-only; done

move_aside() {  # $1 = path, $2 = label
  [ "$DRY" = 1 ] || mkdir -p "$BACKUP/$2"
  run mv "$1" "$BACKUP/$2/"
}

# Remove links into this repo that are not in the plan (deleted or moved skills).
for root in "$CODEX_DIR" "$CLAUDE_DIR"; do
  [ -d "$root" ] || continue
  for l in "$root"/*; do
    [ -L "$l" ] || continue
    case "$(readlink "$l")" in
      "$REPO"/*) printf '%s' "$PLAN" | cut -f1 | grep -qxF "$l" || run rm "$l" ;;
    esac
  done
done

# Create or fix planned links.
while IFS="$(printf '\t')" read -r dest src; do
  [ -n "$dest" ] || continue
  if [ -L "$dest" ]; then
    [ "$(readlink "$dest")" = "$src" ] && continue
    echo "replacing link $dest (was -> $(readlink "$dest"))"
  elif [ -e "$dest" ]; then
    case "$dest" in "$CODEX_DIR"/*) move_aside "$dest" codex ;; *) move_aside "$dest" claude ;; esac
  fi
  [ -d "$(dirname "$dest")" ] || run mkdir -p "$(dirname "$dest")"
  run ln -sfn "$src" "$dest"
done <<EOF
$PLAN
EOF

# Codex still reads the deprecated ~/.codex/skills and would list these skills twice.
for n in $(skills_in skills) $(skills_in codex-only); do
  if [ -e "$LEGACY_CODEX_DIR/$n" ] || [ -L "$LEGACY_CODEX_DIR/$n" ]; then
    move_aside "$LEGACY_CODEX_DIR/$n" codex-legacy
  fi
done

[ "$DRY" = 1 ] && echo "Dry run: nothing changed." || echo "Linked skills from $REPO"
