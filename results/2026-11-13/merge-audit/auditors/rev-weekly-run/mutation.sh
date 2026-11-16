#!/usr/bin/env bash
# mutation.sh — does anything pin what weekly_review.sh is said to do?
# Run: bash /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/mutation.sh
# Works only on a scratch copy of the merged library (work/rev-weekly-run/mut, its own throwaway git repo).
set -u
PACK=/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit
W=$PACK/work/rev-weekly-run
M=$W/mut
export TMPDIR=$W/tmp; mkdir -p "$TMPDIR"
cd /

fresh() {  # a clean copy of the merged library as its own git repo
  rm -rf "$M"; mkdir -p "$M"
  git -C "$PACK/lib" archive 1ce99d5 | tar -x -C "$M"
  git -C "$M" init -q; git -C "$M" add -A; git -C "$M" -c user.name=audit -c user.email=audit@example.invalid commit -qm base
}
S() { echo "$M/.claude/skills/independent-audit/scripts"; }
tests() {  # run only the WeeklyReview test class from the copy
  ( cd "$M" && python3 "$(S)/test_qa_loop.py" WeeklyReview 2>&1 | tail -4 | tr '\n' ' ' ); echo
}
pack_run() {  # run the evidence pack from the copy on the two project copies; print exit code and output
  bash "$(S)/weekly_review.sh" "$@" > "$W/out/mut.out" 2> "$W/out/mut.err"; echo "exit code: $?"
  sed 's/^/    | /' "$W/out/mut.out" | cut -c1-150 | head -${LINES_SHOWN:-9}
  [ -s "$W/out/mut.err" ] && { echo "    stderr:"; sed 's/^/    ! /' "$W/out/mut.err" | cut -c1-150 | tail -3; }
}

echo "### 0. known answer: unmodified copy, the whole test file"
fresh; ( cd "$M" && python3 "$(S)/test_qa_loop.py" 2>&1 | tail -3 | tr '\n' ' ' ); echo

echo; echo "### M1. mutation: every python call in weekly_review.sh is broken (python3 -> python3-absent). The pack has no content."
fresh; sed -i 's/python3 /python3-absent /g' "$(S)/weekly_review.sh"
echo "WeeklyReview tests on the mutant: $(tests)"
LINES_SHOWN=8 pack_run "$M" "$PACK/kit-full" "$PACK/deck-full"

echo; echo "### M2. mutation: weekly_review.sh WRITES: appends a row to every project's corrections log it is given and drops a file in an ignored path of the library"
fresh; mkdir -p "$W/proj-copy/report"; cp "$PACK/kit-full/report/corrections-log.md" "$W/proj-copy/report/corrections-log.md"
before=$(md5sum < "$W/proj-copy/report/corrections-log.md")
sed -i 's|^echo "== 2. Hook registry|for P in "$@"; do [ -f "$P/report/corrections-log.md" ] \&\& echo "\| 2026-11-16 \| mutant \| x \| y \| z \|" >> "$P/report/corrections-log.md"; done; mkdir -p "$LIB/hooks/__pycache__"; date > "$LIB/hooks/__pycache__/mutant.pyc"\n&|' "$(S)/weekly_review.sh"
echo "WeeklyReview tests on the mutant: $(tests)"
bash "$(S)/weekly_review.sh" "$M" "$W/proj-copy" > /dev/null 2>&1
echo "project log changed by the mutant run: $([ "$before" = "$(md5sum < "$W/proj-copy/report/corrections-log.md")" ] && echo no || echo YES); library file written: $(ls "$M/hooks/__pycache__/" | tr '\n' ' ')"

echo; echo "### P1. a part FAILS: one registered hook constant changed by one (TRIVIA_MAX_CHARS 400 -> 401)"
fresh; sed -i 's/^TRIVIA_MAX_CHARS = 400/TRIVIA_MAX_CHARS = 401/' "$M/hooks/governance-enforce.py"
( cd "$M" && python3 .claude/skills/red-team/scripts/registry_check.py --root . > /dev/null 2>&1; echo "registry_check.py alone exits: $?" )
LINES_SHOWN=7 pack_run "$M" "$PACK/kit-full" "$PACK/deck-full"

echo; echo "### P2. a part CRASHES: registry_check.py and stale_rules.py are missing, corrections_rate.py exits 3"
fresh; rm "$M/.claude/skills/red-team/scripts/registry_check.py" "$(S)/stale_rules.py"; printf 'import sys\nsys.exit(3)\n' > "$(S)/corrections_rate.py"
LINES_SHOWN=8 pack_run "$M" "$PACK/kit-full" "$PACK/deck-full"

echo; echo "### P3. the LIBRARY directory does not exist"
LINES_SHOWN=6 pack_run /nonexistent/claude-core-skills "$PACK/kit-full"

echo; echo "### P4. a project directory does not exist (unmodified script)"
fresh; LINES_SHOWN=4 pack_run "$M" /nonexistent/yahoo-fantasy-basketball

echo; echo "### L. the UNMODIFIED script on a fresh copy: what one run leaves behind (run as a real session would, bytecode writing not switched off)"
fresh; ( cd "$M" && find . -path ./.git -prune -o -type f -print | sort > "$W/out/files-before.txt" )
env -u PYTHONDONTWRITEBYTECODE bash "$(S)/weekly_review.sh" "$M" "$PACK/kit-full" "$PACK/deck-full" > /dev/null 2>&1
( cd "$M" && find . -path ./.git -prune -o -type f -print | sort > "$W/out/files-after.txt" )
echo "git status --porcelain, the only thing the test compares: '$(git -C "$M" status --porcelain)'"
echo "files the run created in the library tree:"; comm -13 "$W/out/files-before.txt" "$W/out/files-after.txt" | sed 's/^/    /'
rm -rf "$M" "$W/proj-copy"
