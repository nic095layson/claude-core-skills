#!/usr/bin/env bash
# weekly_review.sh LIBRARY_DIR [PROJECT_DIR ...] — the read-only evidence pack for the weekly improvement run.
# Prints three sections and changes nothing: (1) corrections per week for each project that keeps a log,
# (2) the hook registry check, (3) rules still unmeasured after 60 days. The run that calls this hands the
# output to ONE fresh-context auditor (auditor-brief.md) and opens one draft PR of proposals; it never merges.
set -u
LIB="${1:?library dir}"; shift || true
S="$LIB/.claude/skills/independent-audit/scripts"
echo "== 1. Corrections (wrong statements to the owner, per ISO week)"
for P in "$LIB" "$@"; do
  [ -d "$P" ] || { echo "$P: project directory not found"; continue; }
  for L in "$P/report/corrections-log.md" "$P/corrections-log.md"; do
    [ -f "$L" ] && { printf "%s: " "$(basename "$(cd "$P" && pwd)")"; python3 "$S/corrections_rate.py" "$L"; continue 2; }
  done
  echo "$(basename "$(cd "$P" && pwd)"): no corrections log"
done
echo "== 2. Hook registry (hand-set values registered and unchanged)"
( cd "$LIB" && python3 .claude/skills/red-team/scripts/registry_check.py --root . 2>&1 | tail -3 )
echo "== 3. Stale rules (unmeasured for more than 60 days)"
python3 "$S/stale_rules.py" --root "$LIB" | head -40
exit 0
