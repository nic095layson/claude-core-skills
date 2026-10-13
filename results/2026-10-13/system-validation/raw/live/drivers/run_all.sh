#!/usr/bin/env bash
# run_all.sh <jobs_file> <parallelism> — runs each job line "dir|prompt|settings|turns|allowed|disallowed" via run_one.sh
set -u
J="$1"; P="${2:-6}"; HERE="$(cd "$(dirname "$0")" && pwd)"
while IFS='|' read -r d pf st mt at dt; do
  [ -n "$d" ] || continue
  while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do wait -n; done
  "$HERE/run_one.sh" "$d" "$pf" "$st" "$mt" "$at" "$dt" &
done < "$J"
wait
