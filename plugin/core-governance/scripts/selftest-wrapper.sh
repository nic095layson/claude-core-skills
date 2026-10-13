#!/usr/bin/env bash
# selftest-wrapper.sh — pipe-test for run-unless-project-wired.sh (plugin-only file).
# The yield rule is the one place this plugin can silence governance by mistake, so it is
# pinned: yield only in a LOCAL session whose project "hooks" key wires the hook; run in
# every other case. Usage: bash plugin/core-governance/scripts/selftest-wrapper.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W="$(cd "$HERE/.." && pwd)/scripts/run-unless-project-wired.sh"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
export TMPDIR="$T"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf "  ok   %s\n" "$1"; }
bad() { FAIL=$((FAIL+1)); printf "  FAIL %s — got: %s\n" "$1" "$2"; }
INC='I don'"'"'t agree that career averages are being taken into account. Please provide dissertation response.'
mkdir -p "$T/wired/.claude" "$T/allowonly/.claude" "$T/bare"
cat > "$T/wired/.claude/settings.json" <<'J'
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"python3 \"$CLAUDE_PROJECT_DIR\"/hooks/governance-trigger.py"}]}],
         "Stop":[{"hooks":[{"type":"command","command":"python3 \"$CLAUDE_PROJECT_DIR\"/hooks/governance-enforce.py"}]}]}}
J
cat > "$T/allowonly/.claude/settings.json" <<'J'
{"permissions":{"allow":["Bash(python3 hooks/governance-trigger.py)"]}}
J
prompt() { printf '{"session_id":"%s","prompt":"%s"}' "$1" "$2"; }
run_local() { env -u CLAUDE_CODE_REMOTE CLAUDE_PROJECT_DIR="$1" bash "$W" "$2"; }
run_cloud() { env CLAUDE_CODE_REMOTE=true CLAUDE_PROJECT_DIR="$1" bash "$W" "$2"; }

# 1. local + wired -> yield (silent)
out=$(prompt s1 "$INC" | run_local "$T/wired" governance-trigger.py); rc=$?
[ $rc -eq 0 ] && [ -z "$out" ] && ok "local + project wires the hook -> yields silently" || bad "local+wired should yield" "rc=$rc out=$out"
# 2. local + only a permissions.allow entry names the hook -> runs
out=$(prompt s2 "$INC" | run_local "$T/allowonly" governance-trigger.py)
printf '%s' "$out" | grep -q "Governance auto-trigger" && ok "local + hook named only in permissions.allow -> runs" || bad "allow-only should run" "$out"
# 3. local + bare project -> runs
out=$(prompt s3 "$INC" | run_local "$T/bare" governance-trigger.py)
printf '%s' "$out" | grep -q "Governance auto-trigger" && ok "local + no settings -> runs" || bad "bare should run" "$out"
# 4. cloud + wired -> runs (never yield where repo hooks may not be read)
out=$(prompt s4 "$INC" | run_cloud "$T/wired" governance-trigger.py)
printf '%s' "$out" | grep -q "Governance auto-trigger" && ok "cloud + project wires the hook -> still runs" || bad "cloud+wired should run" "$out"
# 5. cloud + trivia -> runs the trigger, which stays silent on trivia
out=$(prompt s5 "what time zone is the draft in?" | run_cloud "$T/wired" governance-trigger.py); rc=$?
[ $rc -eq 0 ] && [ -z "$out" ] && ok "cloud + trivia -> trigger runs and is silent" || bad "trivia should be silent" "rc=$rc out=$out"
# 6. Stop path: stdin reaches the gate; unloaded governed turn -> block
tr="$T/t.jsonl"; python3 - "$tr" "$INC" <<'PY'
import json,sys
open(sys.argv[1],"w").write(json.dumps({"type":"user","message":{"role":"user","content":sys.argv[2]}})+"\n"+json.dumps({"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"Answer."}]}})+"\n")
PY
out=$(printf '{"session_id":"s6","transcript_path":"%s","stop_hook_active":false}' "$tr" | run_cloud "$T/bare" governance-enforce.py)
printf '%s' "$out" | grep -q '"decision": "block"' && printf '%s' "$out" | grep -q GOV-ENFORCE && ok "Stop path: stdin passes through, unloaded governed turn -> block" || bad "Stop path should block" "$out"
# 7. no hook name -> silent exit 0
out=$(echo '{}' | bash "$W"); rc=$?
[ $rc -eq 0 ] && [ -z "$out" ] && ok "no argument -> silent exit 0" || bad "no-arg" "rc=$rc out=$out"
# 8. unknown hook file -> silent exit 0
out=$(echo '{}' | run_cloud "$T/bare" does-not-exist.py); rc=$?
[ $rc -eq 0 ] && [ -z "$out" ] && ok "unknown hook file -> silent exit 0" || bad "unknown hook" "rc=$rc out=$out"
# 9. unparseable settings in a local session -> runs (fail toward governance)
printf 'not json' > "$T/allowonly/.claude/settings.json"
out=$(prompt s9 "$INC" | run_local "$T/allowonly" governance-trigger.py)
printf '%s' "$out" | grep -q "Governance auto-trigger" && ok "local + unparseable settings -> runs" || bad "unparseable should run" "$out"
echo "== $PASS passed, $FAIL failed =="
[ $FAIL -eq 0 ]
