#!/usr/bin/env bash
# run_auditor.sh <out_dir> <fixture> — one fresh headless auditor session: the brief only, write tools removed.
set -u
o="$1"; f="$2"; mkdir -p "$o"; sid=$(python3 -c 'import uuid;print(uuid.uuid4())')
( cd "$f" && env -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID timeout 900 claude -p "$(cat "$(dirname "$0")/auditor_prompt.txt")" \
    --model claude-opus-5-5 --output-format stream-json --verbose --max-turns 40 --session-id "$sid" \
    --allowedTools "Bash,Read,Glob,Grep" --disallowedTools "Write,Edit,NotebookEdit,Skill,Agent,Task,WebFetch,WebSearch" \
    --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$o/out.jsonl" 2> "$o/err.txt" < /dev/null; echo $? > "$o/exit.txt" )
