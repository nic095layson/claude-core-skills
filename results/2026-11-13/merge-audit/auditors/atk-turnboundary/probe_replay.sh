#!/usr/bin/env bash
# atk-turnboundary: re-run every content-free probe over the real record (through the pack's replay tool) and print the results.
# Nothing but row indexes, counts, tool names, booleans and labels from a closed set is written. Usage: bash <this file>
W="$(cd "$(dirname "$0")" && pwd)"; PACK="$(cd "$W/../.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$W/tmp"; mkdir -p "$TMPDIR"
rm -f "$W/probe-log.tsv" "$W/probe-answers.tsv" "$W/probe-notif.tsv"
R="$PACK/pack/tools/replay_real.py"
python3 "$R" --hooks "$W/hooks-probe"  --what stop > "$W/probe-replay-stop.txt" 2>&1
python3 "$R" --hooks "$W/hooks-probe2" --what stop > /dev/null 2>&1
python3 "$R" --hooks "$W/hooks-probe3" --what stop > /dev/null 2>&1
echo "== probe-log.tsv: one line per real stop point"; cat "$W/probe-log.tsv"
echo "== probe-answers.tsv: tool results the gate reads as the owner's click, by originating tool"; cat "$W/probe-answers.tsv"
echo "== probe-notif.tsv: every real notification read"; cat "$W/probe-notif.tsv"
echo "== the receipt gate with the turn gates' owner filter as its boundary, replayed on the real stop points (totals line)"
python3 "$R" --hooks "$W/hooks-receipt-ownerturn" --what stop 2>&1 | tee "$W/out-replay-receipt-ownerturn.txt" | tail -1
echo "== the Stop gate as committed on 2026-10-20 (cad7aa7) replayed on today's file: first real stop point, then totals"
python3 "$R" --hooks "$W/hooks-2026-10-20" --what stop 2>&1 | tee "$W/out-replay-2026-10-20.txt" | sed -n '2p;$p'
