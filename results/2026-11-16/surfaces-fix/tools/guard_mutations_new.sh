#!/usr/bin/env bash
# The auditor's guard_mutations.sh (rev-surfaces), pointed at the fixed tree. Differences from the original,
# all forced by this unit's rules: the checkout is a plain scratch copy of the tree (no git command may create
# one), so only the guard's sections 8 and 9 run (they hold every check SF-4 and SF-6 are about; sections 1 to 7
# need git or do not read the wiring); the claude CLI is hidden from PATH as in the original. The mutations are
# the auditor's own, same code.
# Usage: bash guard_mutations_new.sh TREE WORK [M0 M1 M2 M3 M4 M5 M8]
set -u
TREE=$1; WORK=$2; shift 2
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONDONTWRITEBYTECODE=1
G="$TREE/.claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh"
sec=$(awk '/^# --- 8\. Enforcement pack/{f=1} /^echo "== RESULT/{f=0} f' "$G")
pyedit() { python3 - "$@"; }
one() {
  m=$1; C="$WORK/$m"; rm -rf "$C"; mkdir -p "$C"
  (cd "$TREE" && tar --exclude=.git --exclude=__pycache__ --exclude=results -cf - .) | (cd "$C" && tar -xf -)
  export TMPDIR="$WORK/tmp-$m"; mkdir -p "$TMPDIR"
  case "$m" in
  M0) d="control: untouched copy                                         -> expect PASS" ;;
  M1) d="control: one byte added to plugin/.../scripts/turngate.py       -> expect FAIL (plugin parity)"
      printf '#\n' >> "$C/plugin/core-governance/scripts/turngate.py" ;;
  M2) d="one byte added to plugin/.../scripts/selftest-reminders.sh      -> expected FAIL"
      printf '#\n' >> "$C/plugin/core-governance/scripts/selftest-reminders.sh" ;;
  M3) d=".claude/settings.json: merge-gate matcher cut to Edit|Write|NotebookEdit|Bash -> expected FAIL"
      pyedit "$C/.claude/settings.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
for g in d["hooks"]["PreToolUse"]:
    if any("turn-gates-pretool" in x["command"] for x in g["hooks"]): g["matcher"]="Edit|Write|NotebookEdit|Bash"
json.dump(d,open(p,"w"),indent=2)
PY
      ;;
  M4) d="plugin hooks.json: the same matcher cut                         -> expected FAIL"
      pyedit "$C/plugin/core-governance/hooks/hooks.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
for g in d["hooks"]["PreToolUse"]:
    if any("turn-gates-pretool" in x["command"] for x in g["hooks"]): g["matcher"]="Edit|Write|NotebookEdit|Bash"
json.dump(d,open(p,"w"),indent=2)
PY
      ;;
  M5) d=".claude/settings.json: receipt-law-stop-gate.sh removed from Stop -> expected FAIL"
      pyedit "$C/.claude/settings.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
for g in d["hooks"]["Stop"]: g["hooks"]=[x for x in g["hooks"] if "receipt-law" not in x["command"]]
json.dump(d,open(p,"w"),indent=2)
PY
      ;;
  M8) d="wrapper: yields when the project wires ANY hook                 -> expected FAIL"
      sed -i 's/            if sys.argv\[2\] in str(x.get("command", "")):/            if True:/' "$C/plugin/core-governance/scripts/run-unless-project-wired.sh"
      d="$d (mutated lines: $(grep -c 'if True:' "$C/plugin/core-governance/scripts/run-unless-project-wired.sh"))" ;;
  esac
  out=$(cd "$C" && FAIL=0 && ok() { :; } && bad() { printf "      FAIL  %s\n" "$*"; FAIL=1; } && eval "$sec" && echo "      == sections 8-9: $([ $FAIL -eq 0 ] && echo PASS || echo FAIL) ==")
  printf '%s  %s\n%s\n' "$m" "$d" "$out" > "$WORK/$m.out"
}
[ $# -gt 0 ] || set -- M0 M1 M2 M3 M4 M5 M8
mkdir -p "$WORK"
for m in "$@"; do one "$m" & done; wait
for m in "$@"; do cat "$WORK/$m.out"; done
