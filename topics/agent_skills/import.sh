#!/usr/bin/env bash
# One-time import: copy existing Codex and Claude Code skills into this repo.
# Skills only one agent has, or both have identically, go to skills/.
# Skills both agents have with different contents go to codex-only/ and claude-only/ for review.
# Stops without importing if ~/.agents/skills and ~/.codex/skills hold different skills with the same name.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
CODEX_SRC="$HOME/.agents/skills"
LEGACY_CODEX_SRC="${CODEX_HOME:-$HOME/.codex}/skills"
CLAUDE_SRC="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
STAGE="$REPO/.import"
EXCLUDES=(--exclude='/.system/' --exclude='/synced/' --exclude='.git/'
          --exclude='.DS_Store' --exclude='__pycache__/')

rm -rf "$STAGE"
mkdir -p "$STAGE/agents" "$STAGE/legacy" "$STAGE/claude"
[ -d "$CODEX_SRC" ]        && rsync -aL "${EXCLUDES[@]}" "$CODEX_SRC/" "$STAGE/agents/"
[ -d "$LEGACY_CODEX_SRC" ] && rsync -aL "${EXCLUDES[@]}" "$LEGACY_CODEX_SRC/" "$STAGE/legacy/"
[ -d "$CLAUDE_SRC" ]       && rsync -aL "${EXCLUDES[@]}" "$CLAUDE_SRC/" "$STAGE/claude/"

# Codex reads both of its folders. Merge them only when they don't disagree.
conflicts=""
for d in "$STAGE"/legacy/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  if [ -d "$STAGE/agents/$name" ]; then
    if diff -rq "$d" "$STAGE/agents/$name" >/dev/null; then
      rm -rf "$d"
    else
      conflicts="$conflicts $name"
    fi
  else
    mv "$d" "$STAGE/agents/"
  fi
done
if [ -n "$conflicts" ]; then
  rm -rf "$STAGE"
  echo "Nothing imported. These skills differ between $CODEX_SRC and $LEGACY_CODEX_SRC:$conflicts" >&2
  echo "Keep one version of each (move the other out of both folders), then run this again." >&2
  exit 1
fi

mkdir -p "$REPO/skills" "$REPO/codex-only" "$REPO/claude-only"

place() {  # $1 = staged skill folder, $2 = destination folder
  local name; name="$(basename "$1")"
  if [ -e "$2/$name" ]; then
    echo "already in repo, not overwritten: $2/$name" >&2
  else
    mv "$1" "$2/"
    echo "imported: ${2#$REPO/}/$name"
  fi
}

for d in "$STAGE"/agents/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  other="$STAGE/claude/$name"
  if [ ! -d "$other" ]; then
    place "$d" "$REPO/skills"
  elif diff -rq "$d" "$other" >/dev/null; then
    place "$d" "$REPO/skills"; rm -rf "$other"
  else
    place "$d" "$REPO/codex-only"; place "$other" "$REPO/claude-only"
    echo "DIFFERENT in each agent, review: $name"
  fi
done
for d in "$STAGE"/claude/*/; do
  [ -f "$d/SKILL.md" ] && place "$d" "$REPO/skills"
done

rm -rf "$STAGE"
echo "Done. Remove any third-party skills from the repo before running link.sh."
