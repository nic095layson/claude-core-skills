#!/bin/bash
# Trap-guarded WITHOUT-arm run. Moves the 5 governors out, runs the arm, and
# ALWAYS restores them (even on error/interrupt) via trap. Never leaves the
# without-arm state installed.
set -u
SKILLS="$HOME/.claude/skills"
BACKUP="$HOME/.claude/skills_phase2_backup"
GOVS=(plan-gate adversarial-verify live-state-truth scope-fence lessons-ledger)
HERE="$(cd "$(dirname "$0")" && pwd)"

restore() {
  echo ">>> RESTORE (trap): moving governors back to $SKILLS"
  for g in "${GOVS[@]}"; do
    if [ -d "$BACKUP/$g" ] && [ ! -e "$SKILLS/$g" ]; then
      mv "$BACKUP/$g" "$SKILLS/$g" && echo "    restored $g"
    elif [ -e "$SKILLS/$g" ]; then
      echo "    $g already in place"
    else
      echo "    !! $g MISSING from both locations — MANUAL CHECK NEEDED"
    fi
  done
  rmdir "$BACKUP" 2>/dev/null
  echo ">>> RESTORE complete. Current ~/.claude/skills:"
  ls "$SKILLS"
}
trap restore EXIT INT TERM

mkdir -p "$BACKUP"
echo ">>> MOVE OUT: relocating 5 governors to $BACKUP"
for g in "${GOVS[@]}"; do
  if [ -d "$SKILLS/$g" ]; then
    mv "$SKILLS/$g" "$BACKUP/$g" && echo "    moved out $g"
  else
    echo "    !! $g not found in $SKILLS at move-out"
  fi
done

echo ">>> VERIFY governors absent from $SKILLS:"
still=0
for g in "${GOVS[@]}"; do
  if [ -e "$SKILLS/$g" ]; then echo "    !! $g STILL PRESENT"; still=1; fi
done
if [ "$still" -ne 0 ]; then echo ">>> ABORT: governors not cleanly removed"; exit 1; fi
echo "    confirmed: none of the 5 governors present"
echo ">>> ~/.claude/skills now:"; ls "$SKILLS"

echo ">>> RUNNING without-arm (20 runs)"
python3 "$HERE/run_arm.py" without
echo ">>> without-arm run finished (rc=$?); trap will now restore"
