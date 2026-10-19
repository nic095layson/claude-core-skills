#!/usr/bin/env bash
# redteam-band-reminder — mechanical trigger aid for the red-team skill (rule 3: two error bars or none).
# PreToolUse on Write|Edit|NotebookEdit. Fires once per session, at the first write whose content quotes a
# figure with a sampling error (a ± or +/- between two numbers) and no band word (FRAGILE, SENSITIVE, ROBUST,
# "structural band"): injects one line asking for the structural band beside the figure, or a statement that
# the figure is measured from data or that the model's constants are uncalibrated. Advisory, never blocking:
# a hook cannot tell a modelled figure from a measured one, and a block on every number would violate the
# anti-ceremony invariant (architecture-contract, invariant 5). A write with no ± is silent; a write that
# already quotes a band is silent. Sentinel mechanics mirror plan-gate-first-write-reminder.sh. Shipped
# 2026-10-19, pipe-tested 7/7 (selftest-redteam-band-reminder.sh, red-first), UNMEASURED as an A/B:
# experiments/hypothesis-2026-10-19-redteam-band-hook.md. Fail-open: any parse error exits 0 silently.
set -u
input=$(cat)
verdict=$(printf '%s' "$input" | python3 -c '
import json, re, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if d.get("tool_name") not in ("Write", "Edit", "NotebookEdit"):
    sys.exit(0)
ti = d.get("tool_input") or {}
text = " ".join(str(ti.get(k) or "") for k in ("content", "new_string", "new_source"))
has_error_bar = re.search(r"[0-9][0-9.,]*\s*%?\s*(±|\+/-|\+/−)\s*[0-9]", text) is not None
has_band = re.search(r"\b(FRAGILE|SENSITIVE|ROBUST)\b|structural band", text) is not None
sid = re.sub(r"[^A-Za-z0-9_.-]", "_", str(d.get("session_id") or "nosession"))
print("fire " + sid if has_error_bar and not has_band else "")
' 2>/dev/null || true)
[ -n "$verdict" ] || exit 0
sid="${verdict#fire }"
sentinel="${TMPDIR:-/tmp}/redteam-band-reminder-${sid}"
if [ ! -e "$sentinel" ]; then
  touch "$sentinel"
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"Band check (red-team skill): this write quotes a figure with a sampling error and no structural band. If the figure comes from a model with hand-set constants (a simulator, projection, forecast, odds, scoring engine), quote the last sweep'"'"'s band beside it by constant name — two error bars — or name the constant as uncalibrated with the decision that will calibrate it; if there is no sweep yet, say so rather than quoting the sampling error alone. A figure measured from data, not modelled: proceed. This reminder fires once per session."},"suppressOutput":true}'
fi
exit 0
