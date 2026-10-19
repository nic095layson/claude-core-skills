#!/usr/bin/env bash
# run_one.sh <run_dir> <prompt_file> <model> <max_turns>
#
# One fresh headless session per run (research-methodology: fresh session, verbatim prompt, one variant).
# The session runs inside an empty work/ subfolder so it cannot read its own output log (a confound found
# 2026-10-13); the account plugin is disabled so no governance hook fires; the three project environment
# variables are unset so no repository's skills or settings leak in. The skill under test is the personal-scope
# copy at ~/.claude/skills/red-team/SKILL.md, byte-identical to the branch; its registration was confirmed in a
# probe session before any run (49 skills listed, red-team among them). Tools are read-only: the prompts name
# artifacts that do not exist, and the measurement is whether the Skill tool is invoked, not what is built.
set -u
d="$1"; pf="$2"; model="$3"; mt="$4"
mkdir -p "$d/work"
(
  cd "$d/work" && env -u CLAUDE_ADDITIONAL_DIRECTORIES -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_PROJECT_DIR \
    timeout 900 claude -p "$(cat "$pf")" --model "$model" --output-format stream-json --verbose \
    --max-turns "$mt" --allowedTools "Skill,Read,Glob,Grep" \
    --settings '{"enabledPlugins":{"core-governance@synced":false}}' > "$d/out.jsonl" 2> "$d/err.txt" < /dev/null
  echo $? > "$d/exit.txt"
)
