#!/usr/bin/env python3
"""Preflight for an unattended run: check every declared precondition FIRST and fail loudly in one line.

Why it exists: an unattended run (a scheduled task, a nightly job, a fresh cloud session) that lacks what it
assumes does not fail — it quietly does nothing. In one project (2026-10-20/21) a scheduled prompt assumed a
repository checkout a fresh session did not have, a fix assumed a tool permission the classifier denied, and a
"Run now" path pushed nothing; each was discovered only when the owner noticed missing output. A preflight
turns "nothing happened" into "FAIL: repo checkout missing" at second zero.

Spec (JSON): {"name": "<run name>", "checks": [<check>, ...]} where each check has a "name" and ONE of:
  "cmd": "<shell command that must exit 0>"            e.g. "git rev-parse --is-inside-work-tree"
  "env": ["VAR", ...]                                  each must be set and non-empty
  "writable": "<path>"                                 must exist and be writable
  "exists": "<path>"                                   must exist
Optional per check: "hint" (printed on failure — say what to do).

    python3 preflight.py --spec preflight.json [--json OUT]
Prints 'PREFLIGHT: PASS — <name>: N checks' (exit 0) or 'PREFLIGHT: FAIL — <name>: '<check>' <why> [hint]'
(exit 1) and stops at the first failure. A missing or unreadable spec is a FAIL, never a pass. Stdlib only.
"""
import argparse
import json
import os
import subprocess
import sys


def run_check(c):
    if "cmd" in c:
        try:
            r = subprocess.run(c["cmd"], shell=True, capture_output=True, text=True, timeout=c.get("timeout", 60))
        except subprocess.TimeoutExpired:
            return False, "timed out"
        tail = (r.stderr.strip() or r.stdout.strip()).splitlines()[-1:] or [""]
        return r.returncode == 0, f"exit {r.returncode}: {tail[0][:160]}"
    if "env" in c:
        missing = [v for v in c["env"] if not os.environ.get(v)]
        return not missing, "unset: " + ", ".join(missing)
    if "writable" in c:
        p = c["writable"]
        return os.path.exists(p) and os.access(p, os.W_OK), f"not writable: {p}"
    if "exists" in c:
        return os.path.exists(c["exists"]), f"missing: {c['exists']}"
    return False, "check has none of cmd/env/writable/exists"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True); ap.add_argument("--json")
    a = ap.parse_args(argv)
    try:
        spec = json.load(open(a.spec, encoding="utf-8"))
        checks = spec["checks"]; name = spec.get("name", os.path.basename(a.spec))
        assert isinstance(checks, list) and checks
    except Exception as e:
        print(f"PREFLIGHT: FAIL — spec {a.spec} unreadable or empty ({type(e).__name__}); an unchecked run is not a pass")
        return 1
    rows = []
    for c in checks:
        ok, why = run_check(c)
        rows.append(dict(name=c.get("name", "?"), ok=ok, why="" if ok else why))
        if not ok:
            if a.json:
                json.dump(rows, open(a.json, "w"), indent=1)
            hint = f" — {c['hint']}" if c.get("hint") else ""
            print(f"PREFLIGHT: FAIL — {name}: '{c.get('name', '?')}' {why}{hint}")
            return 1
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1)
    print(f"PREFLIGHT: PASS — {name}: {len(rows)} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
