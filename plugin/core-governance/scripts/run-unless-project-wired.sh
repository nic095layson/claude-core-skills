#!/usr/bin/env bash
# run-unless-project-wired.sh — plugin entry point for every governance hook.
#
# Why: the same hooks ship two ways — at project scope (`.claude/settings.json` in a
# repository that carries the pack) and through this plugin (for sessions that do not
# read repository hooks, such as a cloud session with several repositories attached).
# A single-repository session that has both would run each hook twice. This wrapper
# makes the plugin yield: if the project's settings already wire the named hook, it
# exits 0 with no output (fail-open: no context, no block). Otherwise it execs the
# hook from this plugin's own scripts/ directory, stdin intact.
#
# Usage (from hooks/hooks.json): run-unless-project-wired.sh <hook-file-name>
set -u
here="$(cd "$(dirname "$0")" && pwd)"
hook="${1:-}"; shift || true
[ -n "$hook" ] || exit 0
[ -f "$here/$hook" ] || exit 0
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
if [ -f "$proj/.claude/settings.json" ] && grep -qF "$hook" "$proj/.claude/settings.json" 2>/dev/null; then
  exit 0
fi
case "$hook" in
  *.py) exec python3 "$here/$hook" "$@" ;;
  *.sh) exec bash "$here/$hook" "$@" ;;
  *)    exit 0 ;;
esac
