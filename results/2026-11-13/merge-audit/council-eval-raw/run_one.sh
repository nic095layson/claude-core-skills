#!/usr/bin/env bash
# run_one_isolated.sh <run_dir> <prompt_file> <model> <max_turns>
# Replicate B (2026-10-19, after the refuters reviewed replicate A). Three isolation fixes: the parent session id
# is unset (A inherited it, the INC-14 class); every tool but Skill is disallowed, so a session can read nothing
# (A pre-approved four tools, which does not remove the rest: Bash ran in 23 of 24 A runs and three Write
# attempts were permission-denied); the account plugin stays disabled. Transcript: <run_dir>/out.jsonl.
set -u
d="$1"; pf="$2"; model="$3"; mt="$4"
mkdir -p "$d/work"
(
  cd "$d/work" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
    timeout 900 claude -p "$(cat "$pf")" --model "$model" --output-format stream-json --verbose \
    --max-turns "$mt" --allowedTools "Skill" --disallowedTools "Bash,Read,Glob,Grep,Write,Edit,NotebookEdit,WebFetch,WebSearch,Task,Agent,TodoWrite" \
    --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$d/out.jsonl" 2> "$d/err.txt" < /dev/null
  echo $? > "$d/exit.txt"
)
