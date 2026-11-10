#!/usr/bin/env bash
# Turn on GitHub's "Automatically delete head branches" for repos you pick.
#
#   ./auto-delete-branches.sh list  [repo-dir] [list-file]   # write repos that have it off
#   (edit the list file: delete any line you want to skip)
#   ./auto-delete-branches.sh apply [list-file]              # turn it on for every line left
#
# Defaults: repo-dir = ~/repo, list-file = ./auto-delete-repos.txt
set -euo pipefail

cmd=${1:-}
case "$cmd" in
  list)
    dir=${2:-$HOME/repo}
    out=${3:-./auto-delete-repos.txt}
    : > "$out"
    for d in "$dir"/*/; do
      url=$(git -C "$d" remote get-url origin 2>/dev/null) || continue
      repo=$(sed -nE 's#.*github\.com[:/]([^/]+/[^/]+)$#\1#p' <<<"${url%.git}")
      [ -n "$repo" ] || continue
      # Only repos you admin, not archived, with the setting off.
      if gh api "repos/$repo" --jq 'select(.permissions.admin and (.archived|not) and (.delete_branch_on_merge|not)) | .full_name' 2>/dev/null; then :; fi
    done | sort -u >> "$out"
    echo "Wrote $(wc -l < "$out" | tr -d ' ') repos to $out. Delete lines to skip, then run: $0 apply $out"
    ;;
  apply)
    in=${2:-./auto-delete-repos.txt}
    [ -f "$in" ] || { echo "No list file: $in" >&2; exit 1; }
    grep -vE '^\s*(#|$)' "$in" | while read -r repo; do
      if gh api -X PATCH "repos/$repo" -F delete_branch_on_merge=true --jq '"\(.full_name): \(.delete_branch_on_merge)"'; then :; else echo "$repo: FAILED" >&2; fi
    done
    ;;
  *)
    echo "Usage: $0 list [repo-dir] [list-file] | apply [list-file]" >&2
    exit 2
    ;;
esac
