#!/usr/bin/env python3
"""stale_rules.py — the pruning list: rules still marked UNMEASURED or candidate long after they were written.

Why it exists (audit of 2026-11-12): the instructions block grew from 5,295 to 9,096 characters and most
additions were marked UNMEASURED; nothing has been retired on evidence since 2026-07. A rule nobody measured
is a cost with an unknown benefit. This lists each marker with the nearest date on its line (or the lines
just above), oldest first, so a review can measure it or cut it. It reports; it changes nothing.

Usage: stale_rules.py [--root DIR] [--days 60] [--today YYYY-MM-DD] [--json]
Scans: .claude/skills/*/SKILL.md and instructions/*.md under the root.
"""
import argparse
import datetime
import glob
import json
import os
import re

MARK = re.compile(r"UNMEASURED|\*candidate\*")
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="."); ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--today"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    files = sorted(glob.glob(os.path.join(a.root, ".claude", "skills", "*", "SKILL.md")) +
                   glob.glob(os.path.join(a.root, "instructions", "*.md")))
    stale, fresh, undated = [], 0, 0
    for f in files:
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        for i, line in enumerate(lines):
            if not MARK.search(line):
                continue
            ds = DATE.findall(line) or [d for back in lines[max(0, i - 3):i][::-1] for d in DATE.findall(back)]
            if not ds:
                undated += 1; continue
            try:
                d = max(datetime.date.fromisoformat(x) for x in ds[:1] if x)
            except ValueError:
                undated += 1; continue
            age = (today - d).days
            if age > a.days:
                stale.append({"file": os.path.relpath(f, a.root), "line": i + 1, "date": str(d), "age_days": age,
                              "text": line.strip()[:110]})
            else:
                fresh += 1
    stale.sort(key=lambda x: -x["age_days"])
    if a.json:
        print(json.dumps({"today": str(today), "days": a.days, "stale": stale, "fresh": fresh, "undated": undated}, indent=1)); return
    print(f"STALE RULES: {len(stale)} older than {a.days} days, {fresh} newer, {undated} undated (as of {today})")
    for s in stale:
        print(f"  {s['age_days']:>4}d  {s['file']}:{s['line']}  {s['text']}")


if __name__ == "__main__":
    main()
