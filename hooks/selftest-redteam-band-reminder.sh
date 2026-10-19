#!/usr/bin/env bash
# selftest-redteam-band-reminder.sh — pipe tests for hooks/redteam-band-reminder.sh (red-first, 2026-10-19).
# Written BEFORE the hook existed; the first run fails every case ("hook missing"), the run after the hook
# lands must print 7/7 PASS. Each case feeds one PreToolUse JSON to the hook with a fresh session id (the
# sentinel is per session) and checks whether a reminder came back.
#   expect JSON : a figure with a sampling error (± or +/-) in written content and no band word
#   expect empty: the same session again (once per session); band word present; no ±; a non-write tool;
#                 malformed input (fail-open, exit 0)
set -u
HOOK="$(cd "$(dirname "$0")" && pwd)/redteam-band-reminder.sh"
export TMPDIR="${TMPDIR:-/tmp}/redteam-selftest-$$"
mkdir -p "$TMPDIR"
pass=0; fail=0
run() {  # run <label> <expect:json|empty> <stdin>
  local label="$1" want="$2" input="$3" out code
  if [ ! -f "$HOOK" ]; then echo "  FAIL  $label (hook missing: $HOOK)"; fail=$((fail+1)); return; fi
  out=$(printf '%s' "$input" | bash "$HOOK" 2>/dev/null); code=$?
  if [ "$code" -ne 0 ]; then echo "  FAIL  $label (exit $code, must be 0)"; fail=$((fail+1)); return; fi
  case "$want" in
    json)  if printf '%s' "$out" | grep -q '"additionalContext"'; then echo "  ok    $label"; pass=$((pass+1)); else echo "  FAIL  $label (expected a reminder, got: ${out:-<empty>})"; fail=$((fail+1)); fi ;;
    empty) if [ -z "$out" ]; then echo "  ok    $label"; pass=$((pass+1)); else echo "  FAIL  $label (expected silence, got: $out)"; fail=$((fail+1)); fi ;;
  esac
}
write() { printf '{"session_id":"%s","tool_name":"%s","tool_input":{"file_path":"report.md","content":"%s"}}' "$1" "$2" "$3"; }
edit()  { printf '{"session_id":"%s","tool_name":"Edit","tool_input":{"file_path":"report.md","old_string":"x","new_string":"%s"}}' "$1" "$2"; }

run "t1 Write: figure ± sampling error, no band word -> reminder" json \
    "$(write s1 Write 'Title share 21.4 ± 0.4 (6,000 seasons). The swap is positive.')"
run "t2 same session again -> silent (once per session)" empty \
    "$(write s1 Write 'Another figure 18.0 ± 0.5 in the same session.')"
run "t3 Write: ± figure WITH the band quoted (FRAGILE) -> silent" empty \
    "$(write s2 Write 'Title share 21.4 ± 0.4; TEAM_SHOCK is FRAGILE: +3.4 / -2.3; headline within that band.')"
run "t4 Write: a number with no ± (a measured count, a percentage) -> silent" empty \
    "$(write s3 Write 'Revenue grew 4.2% last quarter; 12 teams; 17 weeks.')"
run "t5 Bash tool carrying a ± in its command -> silent (write-class tools only)" empty \
    "$(printf '{"session_id":"s4","tool_name":"Bash","tool_input":{"command":"echo 21.4 ± 0.4"}}')"
run "t6 malformed input -> silent, exit 0 (fail-open)" empty "this is not json"
run "t7 Edit: new_string with an ASCII +/- figure, no band word -> reminder" json \
    "$(edit s6 'Lift of 4.2% +/- 0.3 on the new tier.')"

rm -rf "$TMPDIR"
echo "== $pass passed, $fail failed =="
[ "$fail" -eq 0 ]
