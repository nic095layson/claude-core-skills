#!/usr/bin/env bash
# Real-session replays with the switchable probe copy (verdict labels only). Usage: bash run_replays.sh [pre|stop|all]
set -u
W="$(cd "$(dirname "$0")" && pwd)"
P="$(cd "$W/../.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$W/tmp"; export TMPDIR="$W/tmp"
what="${1:-all}"
run() {  # label, section, env assignments...
  local label="$1" section="$2"; shift 2
  echo "---- $label   [$*]"
  env "$@" python3 "$P/pack/tools/replay_real.py" --hooks "$W/hooks-probe" --what "$section" | grep -v "^== "
}
if [ "$what" = pre ] || [ "$what" = all ]; then
  echo "######## REAL MERGE CALLS (and write-class calls): which route authorises"
  run "all routes (as shipped, advisory off)" pre ATK_NO_F3=1
  run "route 1 only: owner's latest message" pre ATK_NO_F3=1 ATK_ROUTES=1
  run "route 2 only: clickable answer (as shipped)" pre ATK_NO_F3=1 ATK_ROUTES=2
  run "route 2 only, strict: the result must belong to an AskUserQuestion call" pre ATK_NO_F3=1 ATK_ROUTES=2 ATK_STRICT_ANSWERS=1
  run "route 3 only: assistant's last text + this PR's number" pre ATK_NO_F3=1 ATK_ROUTES=3
  echo "######## PHANTOM: every real write-class call judged as a merge of PR #999999 (a PR nobody named)"
  run "phantom, all routes" pre ATK_NO_F3=1 ATK_PHANTOM=1
  run "phantom, route 1 only" pre ATK_NO_F3=1 ATK_PHANTOM=1 ATK_ROUTES=1
  run "phantom, route 2 only (as shipped)" pre ATK_NO_F3=1 ATK_PHANTOM=1 ATK_ROUTES=2
  run "phantom, route 2 only, strict" pre ATK_NO_F3=1 ATK_PHANTOM=1 ATK_ROUTES=2 ATK_STRICT_ANSWERS=1
  run "phantom, route 3 only, any #number in the assistant's last text" pre ATK_NO_F3=1 ATK_PHANTOM=1 ATK_ROUTES=3 ATK_R3_ANY=1
fi
if [ "$what" = stop ] || [ "$what" = all ]; then
  echo "######## STOP PROBE: at each real stop point, would a merge of PR #999999 pass? (BLOCK:F1 = yes, allow = no, BLOCK:receipt = scheduled turn)"
  for spec in "ATK_ROUTES=123" "ATK_ROUTES=1" "ATK_ROUTES=2" "ATK_ROUTES=2 ATK_STRICT_ANSWERS=1" "ATK_ROUTES=3 ATK_R3_ANY=1"; do
    echo "---- stop probe [$spec]"
    env ATK_STOP_PROBE=1 $spec python3 "$P/pack/tools/replay_real.py" --hooks "$W/hooks-probe" --what stop | grep -v "^== " | awk -F'|' '{ if ($0 ~ /totals/) print $0; else { split($3,a,"/"); gsub(/ now: /,"",a[1]); gsub(/ +$/,"",a[1]); printf "%s:%s  ", substr($1,3,16), a[1] } } END { print "" }'
  done
fi
