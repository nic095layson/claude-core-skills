#!/bin/bash
# Trap-guarded WITHOUT-arm (uncued test). Governors moved out of personal scope;
# run cwd OUTSIDE repo/~/.claude (RUNROOT). Always restores via trap.
set -u
SKILLS="$HOME/.claude/skills"
BACKUP="$HOME/.claude/skills_uncued_backup"
GOVS=(plan-gate adversarial-verify live-state-truth scope-fence lessons-ledger)
HERE="$(cd "$(dirname "$0")" && pwd)"
export RUNROOT="${RUNROOT:-/private/tmp/phase2uncued_run}"

restore() {
  echo ">>> RESTORE (trap): moving governors back to $SKILLS"
  for g in "${GOVS[@]}"; do
    if [ -d "$BACKUP/$g" ] && [ ! -e "$SKILLS/$g" ]; then
      mv "$BACKUP/$g" "$SKILLS/$g" && echo "    restored $g"
    elif [ -e "$SKILLS/$g" ]; then echo "    $g already in place"
    else echo "    !! $g MISSING from both — MANUAL CHECK"; fi
  done
  rmdir "$BACKUP" 2>/dev/null
  echo ">>> RESTORE complete. ~/.claude/skills:"; ls "$SKILLS"
}
trap restore EXIT INT TERM

mkdir -p "$BACKUP"
echo ">>> MOVE OUT 5 governors -> $BACKUP"
for g in "${GOVS[@]}"; do
  [ -d "$SKILLS/$g" ] && mv "$SKILLS/$g" "$BACKUP/$g" && echo "    moved out $g" || echo "    !! $g not in $SKILLS"
done
still=0
for g in "${GOVS[@]}"; do [ -e "$SKILLS/$g" ] && { echo "    !! $g STILL PRESENT"; still=1; }; done
[ "$still" -ne 0 ] && { echo ">>> ABORT: not cleanly removed"; exit 1; }
echo "    confirmed: none of the 5 present; ~/.claude/skills:"; ls "$SKILLS"

echo ">>> RUNNING without-arm (RUNROOT=$RUNROOT)"
python3 "$HERE/run_arm.py" without
echo ">>> without-arm finished (rc=$?); trap restores now"
