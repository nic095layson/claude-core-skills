#!/bin/bash
# Trap-guarded WITHOUT-arm for the 2026-08-26 fable-transition audit. Moves the three
# ACTIVE governors out of personal scope (the retired two must already be absent),
# holds the campaign lock (INC-4: never two jobs on one machine's ~/.claude/skills),
# runs one prompt set, restores under trap, verifies byte-identical vs baseline.
# Usage: without_arm.sh <prompts.json> [<prompts.json> ...]   (one toggle window, sets run in order;
#        run_set.py skips cells that already have a valid transcript, so re-runs are safe)
set -u
SKILLS="$HOME/.claude/skills"
BACKUP="$HOME/.claude/skills_fta_backup"
GOVS=(plan-gate adversarial-verify scope-fence)
RETIRED=(live-state-truth lessons-ledger)
HERE="$(cd "$(dirname "$0")" && pwd)"
LOCK=/private/tmp/fta-campaign.lock
export RUNROOT="${RUNROOT:-/private/tmp/fta_2026-08-26}"
PROMPT_SETS=("$@")

restore() {
  echo ">>> RESTORE (trap): moving governors back to $SKILLS"
  for g in "${GOVS[@]}"; do
    if [ -d "$BACKUP/$g" ] && [ ! -e "$SKILLS/$g" ]; then
      mv "$BACKUP/$g" "$SKILLS/$g" && echo "    restored $g"
    elif [ -e "$SKILLS/$g" ]; then echo "    $g already in place"
    else echo "    !! $g MISSING from both — MANUAL CHECK"; fi
  done
  rmdir "$BACKUP" 2>/dev/null
  rmdir "$LOCK" 2>/dev/null
  echo ">>> checksum verify vs baseline:"
  if (cd "$SKILLS" && find . -type f | sort | xargs shasum -a 256) | diff - "$HERE/baseline_checksums_personal_skills.txt"; then
    echo "    BYTE-IDENTICAL to baseline"
  else
    echo "    !! CHECKSUM MISMATCH — MANUAL CHECK REQUIRED"
  fi
}

mkdir "$LOCK" 2>/dev/null || { echo "!! lock held at $LOCK — another campaign job is running; ABORT"; exit 1; }
trap restore EXIT INT TERM

for r in "${RETIRED[@]}"; do
  [ -e "$SKILLS/$r" ] && { echo "!! retired $r present in $SKILLS — ABORT"; exit 1; }
done
mkdir -p "$BACKUP"
echo ">>> MOVE OUT active governors -> $BACKUP"
for g in "${GOVS[@]}"; do
  [ -d "$SKILLS/$g" ] && mv "$SKILLS/$g" "$BACKUP/$g" && echo "    moved out $g" || echo "    !! $g not in $SKILLS"
done
for g in "${GOVS[@]}"; do
  [ -e "$SKILLS/$g" ] && { echo "!! $g STILL PRESENT — ABORT"; exit 1; }
done
echo ">>> without-arm state, ~/.claude/skills: $(ls "$SKILLS" | tr '\n' ' ')"
for P in "${PROMPT_SETS[@]}"; do
  python3 "$HERE/run_set.py" "$P" without
  echo ">>> set $P finished rc=$?"
done
echo ">>> all sets finished; trap restores now"
