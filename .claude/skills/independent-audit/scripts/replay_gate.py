#!/usr/bin/env python3
"""Replay gate: run one step over every recorded REAL input and FAIL if any input breaks it.

Why it exists: tests built from hand-made fixtures pass while the first real input breaks the code in
production. In one project (2026-10-19..21) a page lost its tabs the first morning with real data, a build
crashed on the first morning an optional input was missing, and a test passed only because it read live
data — all three passed every test and broke on real inputs. Replaying the change over inputs that really
happened, before merge, is the cheapest test that cannot be written to fit the code.

A step PASSES on an input only when it exits 0 AND prints a line matching --pass-re (an exit 0 with no PASS
line is a FAIL). No inputs found is a FAIL: a replay that replayed nothing proved nothing.

    python3 replay_gate.py --cmd 'python3 build.py --date {input_stem}' --inputs 'records/deck_record_*.json' \\
        --pass-re '^BUILD: PASS' [--last N] [--json OUT] [--cwd DIR] [--timeout 600]
Placeholders: {input} (the path), {input_stem} (basename without extension), {input_date} (first
YYYY-MM-DD in the basename). Prints 'REPLAY: PASS — N of N inputs ...' or 'REPLAY: FAIL — ...'. Stdlib only.
"""
import argparse
import glob
import json
import os
import re
import shlex
import subprocess
import sys


def fill(cmd, path):
    stem = os.path.splitext(os.path.basename(path))[0]
    m = re.search(r"\d{4}-\d{2}-\d{2}", os.path.basename(path))
    return (cmd.replace("{input}", shlex.quote(path)).replace("{input_stem}", shlex.quote(stem))
               .replace("{input_date}", m.group(0) if m else ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmd", required=True); ap.add_argument("--inputs", required=True, action="append")
    ap.add_argument("--pass-re", required=True); ap.add_argument("--json"); ap.add_argument("--cwd")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--last", type=int, help="replay only the N most recent inputs (sorted by name; date-stamped names sort by date)")
    a = ap.parse_args(argv)
    paths = sorted({p for g in a.inputs for p in glob.glob(g)}, key=os.path.basename)
    if a.last:
        paths = paths[-a.last:]
    if not paths:
        print(f"REPLAY: FAIL — no recorded inputs match {a.inputs}; a replay of nothing proves nothing"); return 1
    rx = re.compile(a.pass_re, re.M)
    rows = []
    for p in paths:
        c = fill(a.cmd, p)
        try:
            r = subprocess.run(c, shell=True, cwd=a.cwd, capture_output=True, text=True, timeout=a.timeout)
            out = r.stdout + "\n" + r.stderr; code = r.returncode
        except subprocess.TimeoutExpired:
            out, code = "timed out", -1
        ok = code == 0 and bool(rx.search(out))
        tail = [ln for ln in out.splitlines() if ln.strip()][-2:]
        rows.append(dict(input=p, cmd=c, exit=code, verdict="PASS" if ok else "FAIL", tail=tail))
        print(f"  {'PASS' if ok else 'FAIL'} {p}" + ("" if ok else f" (exit {code}) — " + " | ".join(tail)))
    if a.json:
        json.dump(rows, open(a.json, "w", encoding="utf-8"), indent=1)
    bad = [x for x in rows if x["verdict"] == "FAIL"]
    if bad:
        print(f"REPLAY: FAIL — {len(bad)} of {len(rows)} recorded inputs break the step: " +
              ", ".join(os.path.basename(x['input']) for x in bad)); return 1
    print(f"REPLAY: PASS — {len(rows)} of {len(rows)} recorded inputs pass"); return 0


if __name__ == "__main__":
    sys.exit(main())
