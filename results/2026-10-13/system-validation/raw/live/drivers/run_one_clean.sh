#!/usr/bin/env bash
# run_one_clean.sh <run_dir> <prompt_file> <settings_json|-> <max_turns> <allowed_tools>
# Like run_one.sh, but the session runs in an empty subfolder so it cannot read its own output log.
set -u
d="$1"; pf="$2"; st="$3"; mt="$4"; at="$5"; mkdir -p "$d/work"
args=(-p "$(cat "$pf")" --model claude-opus-5-5 --output-format stream-json --verbose --max-turns "$mt" --allowedTools "$at")
[ "$st" != "-" ] && args+=(--settings "$st")
( cd "$d/work" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR timeout 900 claude "${args[@]}" > "$d/out.jsonl" 2> "$d/err.txt" < /dev/null; echo $? > "$d/exit.txt" )
