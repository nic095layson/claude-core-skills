#!/usr/bin/env bash
# replay_kit_deck.sh <kit_copy> <date> — build that kit copy's Season Deck for a recorded real morning, then
# open it in headless Chromium. Exit 0 and 'DECK RENDER: PASS' only when the page builds AND draws itself.
# (Old deck versions print PASS for a page whose script crashes, so the render check is part of the step.)
set -u
k="$1"; d="$2"
cd "$k" && python3 scripts/season_deck.py --date "$d" >/tmp/rk_$$.log 2>&1; rc=$?
tail -1 /tmp/rk_$$.log
[ $rc -eq 0 ] || exit $rc
python3 scripts/deck_render_check.py "report/season/deck_$d.html"
