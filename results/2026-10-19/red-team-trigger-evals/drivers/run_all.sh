#!/usr/bin/env bash
# run_all.sh <runs_root> <prompts_dir> <model> <n_runs> [parallel]
# Dispatches run_one.sh over ids 1-6 x runs 1..N for one model, <parallel> sessions at a time (default 4).
# Writes <runs_root>/<model>-id<N>-r<R>/{out.jsonl,err.txt,exit.txt}. Records wall-clock start and end.
set -u
root="$1"; prompts="$2"; model="$3"; n="$4"; par="${5:-4}"
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$root"
date -u +%Y-%m-%dT%H:%M:%SZ > "$root/$model.started.txt"
jobs=()
for id in 1 2 3 4 5 6; do
  for r in $(seq 1 "$n"); do
    jobs+=("$root/$model-id$id-r$r|$prompts/id$id.txt")
  done
done
printf '%s\n' "${jobs[@]}" | xargs -P "$par" -I{} bash -c 'IFS="|" read -r d p <<< "{}"; bash "'"$here"'/run_one.sh" "$d" "$p" "'"$model"'" 6'
date -u +%Y-%m-%dT%H:%M:%SZ > "$root/$model.finished.txt"
