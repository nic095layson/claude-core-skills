#!/usr/bin/env bash
# ledger-recount-reminder — mechanical trigger aid for the lessons-ledger doctrine.
# UserPromptSubmit hook: when the user's message reads like a costly-diagnosis
# recount, inject a one-line ledger reminder. Targets the exact should-fire
# class that plateaued at ~80% under description wording and fired 0/16 uncued
# (DEAD-2 / architecture-contract weak-point 5): the model responds to the
# recount conversationally and never appends. The phrase list below is drawn
# from evals/lessons-ledger.json's should-fire prompts and the retired
# governor's own trigger enumeration (dated 2026-08-03; extend via the A/B, not
# ad hoc). Fires at most once per session (sentinel), advisory only.
# Shipped 2026-08-03, UNMEASURED — A/B plan:
# experiments/hypothesis-2026-08-03-hook-enforcement.md.
set -u
input=$(cat)
sid=$(printf '%s' "$input" | /usr/bin/jq -r '.session_id // "nosession"' 2>/dev/null || echo nosession)
prompt=$(printf '%s' "$input" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null || echo "")
sentinel="${TMPDIR:-/tmp}/ledger-recount-reminder-${sid}"
if [ -e "$sentinel" ]; then exit 0; fi
if printf '%s' "$prompt" | grep -qiE '(burned|wasted|spent|took me|took us) (an?|all|two|three|[0-9]+) (hour|day|afternoon|morning|night)|turned out (to be|the|it was)|finally (figured|cracked|found) (it|out)|root cause was|kept failing until|chas(ed|ing) (a|the|this) bug'; then
  touch "$sentinel"
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"Ledger check (lessons-ledger doctrine): this message reads like a costly-diagnosis recount. If a >=15-minute diagnosis, drift, or dead end was just described, append it to the project ledger (.claude/LESSONS.md) as symptom -> root cause -> evidence -> status, even if it is already fixed. Routine successes are NOT recorded. This reminder fires at most once per session."},"suppressOutput":true}'
fi
exit 0
