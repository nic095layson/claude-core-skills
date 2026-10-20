#!/usr/bin/env bash
# run_one.sh <out_dir> <cwd> <prompt_file>  — fresh headless session on the NEW pack, plugin off,
# own --session-id, hook events in the stream. Model pinned to claude-fable-5-1 (pre-registered).
set -u
o="$1"; cwd="$2"; pf="$3"
mkdir -p "$o"; sid=$(python3 -c 'import uuid;print(uuid.uuid4())')
( cd "$cwd" && env -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
    -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
    timeout 900 claude -p "$(cat "$pf")" --model claude-fable-5-1 --output-format stream-json --verbose \
    --include-hook-events --max-turns 8 --session-id "$sid" --allowedTools "Skill,Write,Read,Bash,Edit" \
    --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$o/out.jsonl" 2> "$o/err.txt" < /dev/null
  echo $? > "$o/exit.txt" )
