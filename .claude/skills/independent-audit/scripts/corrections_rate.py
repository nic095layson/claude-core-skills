#!/usr/bin/env python3
"""corrections_rate.py — the outcome metric: wrong statements made to the owner, per ISO week, and who caught them.

Why it exists (audit of 2026-11-12): every gate in the library checks process — did a governor load, was a
plan shown. None counted how often the owner was told something false. One project kept a corrections log
(7 rows in two days, 2 caught through the owner); this script turns any project's log into a rate, so a
change to the rules can be judged by whether the rate falls.

Input: a markdown file whose table rows start with a date cell: | YYYY-MM-DD | said | records showed |
how it was caught | preventing check |. A row counts as owner-caught when its fourth cell names the owner.
A row whose first cell is not a date is counted as `unparsed`, never dropped. A missing or empty log is
zero rows and exit 0: "no log" and "no errors" are different facts, and the caller prints which it had.

Usage: corrections_rate.py LOG.md [--json]
"""
import datetime
import json
import os
import re
import sys

OWNER = re.compile(r"\bowner\b", re.I)


def parse(path):
    rows, unparsed = [], 0
    if not os.path.exists(path):
        return rows, unparsed, False
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not cells[0] or set(cells[0]) <= set("-: ") or cells[0].lower() == "date":
            continue
        try:
            d = datetime.date.fromisoformat(cells[0])
        except ValueError:
            unparsed += 1
            continue
        rows.append((d, bool(OWNER.search(cells[3] if len(cells) > 3 else ""))))
    return rows, unparsed, True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(2)
    rows, unparsed, exists = parse(args[0])
    weeks = {}
    for d, owner in rows:
        y, w, _ = d.isocalendar()
        k = f"{y}-W{w:02d}"
        e = weeks.setdefault(k, {"total": 0, "owner_caught": 0, "session_caught": 0})
        e["total"] += 1
        e["owner_caught" if owner else "session_caught"] += 1
    out = {"log": args[0], "exists": exists, "rows": len(rows), "unparsed": unparsed, "weeks": dict(sorted(weeks.items()))}
    if "--json" in sys.argv:
        print(json.dumps(out, indent=1)); return
    per = "; ".join(f"{k}: {v['total']} (owner caught {v['owner_caught']})" for k, v in out["weeks"].items()) or "none"
    note = "" if exists else " [no log file]"
    print(f"CORRECTIONS: {len(rows)} rows, {unparsed} unparsed{note} — {per}")


if __name__ == "__main__":
    main()
