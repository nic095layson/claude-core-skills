#!/usr/bin/env bash
# run_live.sh <out_dir> <cwd> <prompt_file> <plugin:on|off> <extra disallowed tools or ->
# One fresh headless session (own --session-id), hook lifecycle events included in the stream.
set -u
o="$1"; cwd="$2"; pf="$3"; plug="$4"; dis="$5"
mkdir -p "$o"; sid=$(python3 -c 'import uuid;print(uuid.uuid4())'); echo "$sid" > "$o/session_id.txt"
args=(--model claude-opus-5-5 --output-format stream-json --verbose --include-hook-events --max-turns 8 --session-id "$sid"
      --allowedTools "Skill,Write,Read,Bash,Edit")
[ "$plug" = off ] && args+=(--settings '{"enabledPlugins":{"core-governance@synced":false}}')
[ "$dis" != - ] && args+=(--disallowedTools "$dis")
( cd "$cwd" && env -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
    -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
    timeout 900 claude -p "$(cat "$pf")" "${args[@]}" > "$o/out.jsonl" 2> "$o/err.txt" < /dev/null; echo $? > "$o/exit.txt" )
