#!/usr/bin/env bash
# run_all.sh <scratch_root>  -- every case in cases.txt x runs 1..2, 4 at a time, each in its own copy of the cwd
set -u
L="$(cd "$(dirname "$0")" && pwd)"; S="$1"
date -u +%FT%TZ > "$L/started.txt"
while read -r id cwd p plug dis; do for r in 1 2; do
  w="$S/runs/$id-r$r"; rm -rf "$w"; mkdir -p "$S/runs"; cp -r "$S/$cwd" "$w"
  echo "$L/runs/$id-r$r|$w|$L/prompts/$p.txt|$plug|$dis"
done; done < "$L/cases.txt" | xargs -P 4 -I{} bash -c 'IFS="|" read -r o w pf plug dis <<< "{}"; bash "'"$L"'/run_live.sh" "$o" "$w" "$pf" "$plug" "$dis"'
date -u +%FT%TZ > "$L/finished.txt"
