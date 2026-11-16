#!/usr/bin/env bash
# Link every yastack skill into the Claude Code and Codex user skill dirs.
# Usage: scripts/install.sh [--uninstall]
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd -P)
main=$(git -C "$repo" worktree list --porcelain | awk 'NR==1 {print $2}')
if [[ "$repo" != "$(cd "$main" && pwd -P)" ]]; then
  echo "run from the main checkout ($main), not a worktree: worktree links break when it is removed" >&2
  exit 1
fi

targets=("$HOME/.claude/skills" "$HOME/.agents/skills")
uninstall=false
[[ "${1:-}" == "--uninstall" ]] && uninstall=true

for target in "${targets[@]}"; do
  mkdir -p "$target"

  # Drop links into this repo whose skill no longer exists, or all of them on uninstall.
  for link in "$target"/*; do
    [[ -L "$link" ]] || continue
    dest=$(readlink "$link")
    [[ "$dest" == "$repo/skills/"* ]] || continue
    if $uninstall || [[ ! -e "$dest" ]]; then
      rm "$link" && echo "removed $link"
    fi
  done
  $uninstall && continue

  for skill in "$repo"/skills/*/; do
    skill=${skill%/}
    link="$target/$(basename "$skill")"
    if [[ -L "$link" && "$(readlink "$link")" == "$skill" ]]; then
      continue
    fi
    if [[ -e "$link" || -L "$link" ]]; then
      echo "skip $link: already exists and is not a yastack link" >&2
      continue
    fi
    ln -s "$skill" "$link" && echo "linked $link"
  done
done
