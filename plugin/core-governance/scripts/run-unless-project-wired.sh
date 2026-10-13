#!/usr/bin/env bash
# run-unless-project-wired.sh — plugin entry point for every governance hook.
#
# Why: the same hooks ship two ways — at project scope (`.claude/settings.json` in a
# repository that carries the pack) and through this plugin (for sessions that do not
# read repository hooks, such as a cloud session with several repositories attached).
# A session that has both would run each hook twice. This wrapper yields to the project
# copy ONLY where repository hooks are known to run: a LOCAL session (CLAUDE_CODE_REMOTE
# unset) whose project settings wire this very hook under their "hooks" key. In a cloud
# session (CLAUDE_CODE_REMOTE=true) the plugin always runs: the harness there reads
# repository hooks in a one-repository session and not in a several-repository one, and
# a hook process cannot tell which it is in — so yielding could silence both copies in
# exactly the case this plugin exists for (INC-2026-10-13-01, verifier finding
# 2026-10-13). The cost is a duplicate trigger line in a one-repository cloud session
# that also carries the pack; the first-write reminders and the receipt-law gate keep
# their own per-session sentinels, so they do not double-fire.
#
# Yield = exit 0 with no output (fail-open: no context, no block). Otherwise exec the hook
# from this plugin's own scripts/ directory, stdin intact.
#
# Usage (from hooks/hooks.json): run-unless-project-wired.sh <hook-file-name>
set -u
here="$(cd "$(dirname "$0")" && pwd)"
hook="${1:-}"; shift || true
[ -n "$hook" ] || exit 0
[ -f "$here/$hook" ] || exit 0

wired_in_project() {  # true when <settings.json> wires <hook> under its "hooks" key
  python3 - "$1" "$2" <<'PY' 2>/dev/null
import json, sys
try:
    h = json.load(open(sys.argv[1], encoding="utf-8")).get("hooks", {}) or {}
except Exception:
    sys.exit(1)
for groups in h.values():
    for g in groups or []:
        for x in (g or {}).get("hooks", []) or []:
            if sys.argv[2] in str(x.get("command", "")):
                sys.exit(0)
sys.exit(1)
PY
}

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  proj="${CLAUDE_PROJECT_DIR:-$PWD}"
  if [ -f "$proj/.claude/settings.json" ] && wired_in_project "$proj/.claude/settings.json" "$hook"; then
    exit 0
  fi
fi

case "$hook" in
  *.py) exec python3 "$here/$hook" "$@" ;;
  *.sh) exec bash "$here/$hook" "$@" ;;
  *)    exit 0 ;;
esac
