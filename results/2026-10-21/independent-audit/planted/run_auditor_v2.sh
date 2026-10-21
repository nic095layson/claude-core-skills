#!/usr/bin/env bash
# run_auditor_v2.sh <out_dir> <copy_dir> — the final brief, run against a disposable copy of the fixture.
set -u
o="$1"; c="$2"; mkdir -p "$o"; rm -rf "$c"; cp -r "$(dirname "$0")/fixture" "$c"; sid=$(python3 -c 'import uuid;print(uuid.uuid4())')
( cd "$c" && env -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID timeout 900 claude -p "$(cat "$(dirname "$0")/auditor_prompt_v2.txt")" \
    --model claude-opus-5-5 --output-format stream-json --verbose --max-turns 40 --session-id "$sid" \
    --allowedTools "Bash,Read,Glob,Grep" --disallowedTools "Write,Edit,NotebookEdit,Skill,Agent,Task,WebFetch,WebSearch" \
    --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$o/out.jsonl" 2> "$o/err.txt" < /dev/null; echo $? > "$o/exit.txt" )
