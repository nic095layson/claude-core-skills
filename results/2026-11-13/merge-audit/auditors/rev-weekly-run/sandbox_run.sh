#!/usr/bin/env bash
# sandbox_run.sh — what the stored prompt's own git commands do to a live checkout, and what three weeks leave behind.
# Run: bash /tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit/work/rev-weekly-run/sandbox_run.sh
# Everything happens in throwaway repositories under work/rev-weekly-run/sandbox (no network, no real checkout).
# The commands are the stored prompt's own (pack/trigger-prompt.md): step 1 "`git fetch origin main` and check out
# main at origin/main (stash leftovers and name the stash; never commit them)"; step 4 "`git worktree add <scratch>
# HEAD`"; step 6 "a new branch `claude/weekly-review-<today>` containing only that report folder".
set -u
PACK=/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit
SB=$PACK/work/rev-weekly-run/sandbox
rm -rf "$SB"; mkdir -p "$SB/tmp"; cd "$SB"
G() { git -c user.name=audit -c user.email=audit@example.invalid -c advice.detachedHead=false "$@"; }
q() { "$@" > /dev/null 2>&1; }

# --- a remote with main, and a "live checkout" as an owner-facing session leaves it mid-work
q git init -q --bare origin.git; q git -C origin.git symbolic-ref HEAD refs/heads/main
q G clone -q origin.git seed; ( cd seed; q git checkout -q -b main; mkdir -p hooks; echo "TRIVIA_MAX_CHARS = 400" > hooks/gate.py; echo notes > README.md
  q G add -A; q G commit -qm "main: base"; q git push -q origin main )
q G clone -q origin.git live; cd live
q git branch claude/owner-work-in-progress            # the owner's feature branch, cut from origin/main
echo "local fix, committed on main, not pushed" >> README.md; q G commit -qam "local-only commit on main"; LOCAL=$(git rev-parse --short HEAD)
q git checkout -q claude/owner-work-in-progress
echo "TRIVIA_MAX_CHARS = 350   # owner's uncommitted edit" > hooks/gate.py
echo "draft the owner has not added yet" > draft-notes.md

state() { echo "  branch:            $(git rev-parse --abbrev-ref HEAD)"
          echo "  uncommitted edit:  $(git status --short | tr '\n' ';')"
          echo "  hooks/gate.py:     $(cat hooks/gate.py)"
          echo "  stashes:           $(git stash list | wc -l)  $(git stash list | head -1)"
          echo "  main is at:        $(git log -1 --format='%h %s' main)   (commit $LOCAL on a branch: $(git branch --contains $LOCAL --format='%(refname:short)' | tr '\n' ' '))"; }

echo "### A. the live checkout BEFORE the Monday run (owner mid-work on a feature branch)"; state
echo
echo "### B. step 1 as stored: fetch, name a stash for the leftovers, check out main at origin/main"
q git fetch origin main
q git stash push -m "weekly-review leftovers 2026-11-16"
q git checkout -q main; q git reset -q --hard origin/main
state
echo "  untracked draft still in the tree, now on main: $(ls draft-notes.md 2>/dev/null)"
echo

week() {  # steps 4-6 of one run, with the prompt's own commands; $1 = date
  d=$1
  git worktree add -q "$SB/tmp/weekly-audit-$d" HEAD 2>&1 | sed 's/^/    /'
  mkdir -p results/$d/weekly-review; echo "# Weekly QA review $d" > results/$d/weekly-review/REPORT.md
  git checkout -q -b claude/weekly-review-$d 2>&1 | sed 's/^/    /'
  q G add results/$d/weekly-review; q G commit -qm "Weekly QA review $d"; q git push -q -u origin claude/weekly-review-$d
}
step1() { q git fetch origin main; git stash push -q -m "weekly-review leftovers $1" 2>/dev/null; q git checkout -q main; q git reset -q --hard origin/main; }

echo "### C. three Mondays, the owner merges none of the draft PRs (steps 1, 4, 5, 6 each week)"
week 2026-11-16
echo "  after run 1, the checkout is left on: $(git rev-parse --abbrev-ref HEAD)"
step1 2026-11-23; echo "  run 2, step 5 'compared with the previous weekly report if one exists' -> on main: $(ls -d results/*/weekly-review 2>/dev/null | wc -l) report(s); on unmerged branches: $(git branch -r --list 'origin/claude/weekly-review-*' | wc -l)"
week 2026-11-23
step1 2026-11-30; week 2026-11-30
echo "  worktrees registered:        $(git worktree list | wc -l) (1 = the checkout itself)"
echo "  local review branches:       $(git branch --list 'claude/weekly-review-*' | wc -l)"
echo "  remote review branches:      $(git branch -r --list 'origin/claude/weekly-review-*' | wc -l)"
echo "  stashes:                     $(git stash list | wc -l)  [$(git stash list | head -1)]   (never popped: no step restores it)"
echo "  owner's branch still exists: $(git branch --list 'claude/owner-work-in-progress' | tr -d ' ') ; checkout is on: $(git rev-parse --abbrev-ref HEAD)"
echo
echo "### D. the container's /tmp is cleared between runs (the worktree directories vanish)"
rm -rf "$SB/tmp"/weekly-audit-*
git worktree list | sed 's/^/  /' | sed "s|$SB|<sandbox>|g"
echo
echo "### E. the task fires twice on one day (a manual fire, or a retry after a failed run)"
q git checkout -q main
mkdir -p "$SB/tmp"; git worktree add -q "$SB/tmp/weekly-audit-2026-11-30" HEAD 2>&1 | sed 's/^/  /' | sed "s|$SB|<sandbox>|g"
git checkout -q -b claude/weekly-review-2026-11-30 2>&1 | sed 's/^/  /'
echo "  exit of 'git checkout -b claude/weekly-review-2026-11-30': ${PIPESTATUS[0]}"
echo
echo "### F. the stored prompt and the real checkout (read-only on the pack)"
echo "  words in the stored prompt that undo step 1 (pop, restore, switch back, return to, previous branch): $(grep -ciE 'stash pop|restore|switch back|return to|previous branch|original branch' "$PACK/pack/trigger-prompt.raw.txt")"
echo "  non-main branches the live library checkout carried on 2026-11-12 (lib/ was cloned from it): $(git -C "$PACK/lib" for-each-ref --format='%(refname:short)' refs/remotes | grep -v 'origin$\|origin/main\|origin/HEAD' | tr '\n' ' ')"
cd /; rm -rf "$SB"
