#!/usr/bin/env bash
# run_one.sh <out_dir> <prompt>  — fresh headless session in a fresh wired repo; account plugin OFF
# so only the candidate project hooks run. The model is $MODEL (recorded by label, not identifier).
set -u
o="$(mkdir -p "$1" && cd "$1" && pwd)"; p="$2"; bash "$(dirname "$0")/setup_repo.sh" "$o/repo"
sid=$(python3 -c 'import uuid;print(uuid.uuid4())'); echo "$sid" > "$o/session_id.txt"
( cd "$o/repo" && env -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
    -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
    timeout 900 claude -p "$p" --model "$MODEL" --output-format stream-json --verbose --include-hook-events \
      --max-turns 14 --session-id "$sid" --allowedTools "Skill,Write,Read,Bash,Edit" \
      --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$o/out.jsonl" 2> "$o/err.txt" < /dev/null; echo $? > "$o/exit.txt" )
