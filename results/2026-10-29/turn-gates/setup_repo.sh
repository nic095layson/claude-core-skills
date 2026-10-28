#!/usr/bin/env bash
# setup_repo.sh <dir>: a throwaway project wired with the candidate hooks, one staged change.
set -eu
d="$1"; rm -rf "$d"; mkdir -p "$d/.claude"
cp -r /home/user/claude-core-skills/hooks "$d/hooks"; rm -rf "$d/hooks/__pycache__"
cp /home/user/claude-core-skills/.claude/settings.json "$d/.claude/settings.json"
cd "$d"; git init -q; git config user.email t@t; git config user.name t
printf 'notes\n' > notes.md; git add -A; git commit -qm init
printf 'notes\nmore\n' > notes.md; git add notes.md
