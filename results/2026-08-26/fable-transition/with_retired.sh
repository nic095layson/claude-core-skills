#!/bin/bash
# Trap-guarded WITH-RETIRED arm for step 2: the two RETIRED governors are copied
# from the repo into personal scope for the batch, diff-verified, removed under
# trap, absence verified, install checksummed against baseline. Active governors
# stay installed (deployed state). Usage: with_retired.sh <prompts.json>
set -u
REPO=/Users/davidlayson/claude-core-skills
SKILLS="$HOME/.claude/skills"
RETIRED=(live-state-truth lessons-ledger)
HERE="$(cd "$(dirname "$0")" && pwd)"
LOCK=/private/tmp/fta-campaign.lock
export RUNROOT="${RUNROOT:-/private/tmp/fta_2026-08-26}"
PROMPTS="$1"

cleanup() {
  echo ">>> CLEANUP (trap): removing retired governors from personal scope"
  for r in "${RETIRED[@]}"; do
    rm -rf "$SKILLS/$r" && echo "    removed $r"
  done
  for r in "${RETIRED[@]}"; do
    [ -e "$SKILLS/$r" ] && echo "    !! $r STILL PRESENT — MANUAL CHECK"
  done
  rmdir "$LOCK" 2>/dev/null
  echo ">>> checksum verify vs baseline:"
  if (cd "$SKILLS" && find . -type f | sort | xargs shasum -a 256) | diff - "$HERE/baseline_checksums_personal_skills.txt"; then
    echo "    BYTE-IDENTICAL to baseline"
  else
    echo "    !! CHECKSUM MISMATCH — MANUAL CHECK REQUIRED"
  fi
}

mkdir "$LOCK" 2>/dev/null || { echo "!! lock held at $LOCK — ABORT"; exit 1; }
trap cleanup EXIT INT TERM

for r in "${RETIRED[@]}"; do
  [ -e "$SKILLS/$r" ] && { echo "!! $r already present — ABORT"; exit 1; }
  cp -R "$REPO/.claude/skills/$r" "$SKILLS/$r" && echo "    installed $r (temporary)"
done
for r in "${RETIRED[@]}"; do
  diff -q "$REPO/.claude/skills/$r/SKILL.md" "$SKILLS/$r/SKILL.md" >/dev/null || { echo "!! $r copy differs from repo — ABORT"; exit 1; }
done
echo ">>> with-retired state, ~/.claude/skills: $(ls "$SKILLS" | tr '\n' ' ')"
python3 "$HERE/run_set.py" "$PROMPTS" with
echo ">>> runs finished rc=$?; trap cleans up now"
