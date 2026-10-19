#!/usr/bin/env bash
# run_one.sh <run_dir> <prompt_file> <settings_json|-> <max_turns> <allowed_tools> <disallowed_tools|->
set -u
d="$1"; pf="$2"; st="$3"; mt="$4"; at="$5"; dt="$6"; STOP="$(dirname "$d")/../STOP"
[ -e "$STOP" ] && { echo "skipped: STOP flag" > "$d/skipped.txt"; exit 0; }
args=(-p "$(cat "$pf")" --model claude-opus-5-5 --output-format stream-json --verbose --max-turns "$mt" --allowedTools "$at")
[ "$st" != "-" ] && args+=(--settings "$st")
[ "$dt" != "-" ] && args+=(--disallowedTools "$dt")
( cd "$d" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR timeout 1500 claude "${args[@]}" > out.jsonl 2> err.txt < /dev/null; echo $? > exit.txt )
if grep -qiE "session limit|usage limit|rate.?limit.*exceeded|hit your (session|usage) limit" "$d/err.txt" "$d/out.jsonl" 2>/dev/null; then touch "$STOP"; echo "LIMIT HIT in $d" >&2; fi
