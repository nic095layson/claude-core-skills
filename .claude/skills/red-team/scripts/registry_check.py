#!/usr/bin/env python3
"""Registry check: the project's judgment constants, registered with a calibration status, against the live
system (red-team skill, step 1). Generalized 2026-10-19 from the reference implementation in the
fantasy-basketball kit (check_constants.py; ledger INC-2026-10-19-01), named here as lineage only: nothing
in this script depends on that project, and the live values come from yours.

Why it exists: a hand-set constant cannot fail a test of itself. The incident's engine passed three months
of audits while one unregistered shock constant moved the headline by three points. Nothing could fail,
because nothing recorded what each constant was FOR or what vouched for it. This check makes that a gate.

Inputs
  --registry PATH   redteam/constants_registry.json (default), {"constants": [entry, ...]}
                    entry: {"name", "value", "role", "status", "record", "decision", "band"}
  --live SPEC       where the live values come from, default redteam/live.py. One of:
                      a .py file defining live_values() -> {name: value}
                      a .json file holding {name: value}
                      a JSON object literal on the command line
  --root DIR        the project root (default: the current directory); relative paths resolve here and the
                    fingerprint is `git rev-parse --short HEAD` run here
  --fingerprint X   use X as the engine fingerprint instead of git
  --json OUT        write the check record (verdict, fingerprint, counts, problems) here

Fails (exit 1, 'CONSTANTS CHECK: FAIL' + one line per problem) on: a registry value that differs from the live
value (drift); a live constant that is not registered; a registered constant the live system no longer has;
a status outside the five; a measured, declared_band or settings entry with no record; an uncalibrated
entry with no decision id; a declared_band entry with no band; an entry with no role.
Passes with 'CONSTANTS CHECK: PASS — N registered = N live on <fingerprint>; <counts by status>'.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

STATUSES = ("settings", "structural", "measured", "declared_band", "uncalibrated")
NEEDS_RECORD = ("settings", "measured", "declared_band")


def _plain(v):
    """JSON-comparable form: tuples -> lists, dict order ignored, floats rounded."""
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in sorted(v.items(), key=lambda kv: str(kv[0]))}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, float):
        return round(v, 9)
    return v


def check(registry, live):
    """(ok, problems) for a registry dict against a {name: value} map of the live system."""
    problems, seen = [], set()
    for e in registry.get("constants", []):
        name = str(e.get("name") or "")
        if not name:
            problems.append("an entry has no name")
            continue
        if name in seen:
            problems.append(f"{name}: registered twice")
        seen.add(name)
        status = e.get("status")
        if status not in STATUSES:
            problems.append(f"{name}: status {status!r} is not one of {', '.join(STATUSES)}")
        else:
            if status in NEEDS_RECORD and not str(e.get("record") or "").strip():
                problems.append(f"{name}: status {status} needs a record (the file or note that vouches for it)")
            if status == "uncalibrated" and not str(e.get("decision") or "").strip():
                problems.append(f"{name}: uncalibrated needs a decision id (where the calibration is decided)")
            if status == "declared_band" and not e.get("band"):
                problems.append(f"{name}: declared_band needs a band (the variants the sweep runs)")
        if not str(e.get("role") or "").strip():
            problems.append(f"{name}: no role stated")
        if name not in live:
            problems.append(f"{name}: registered but not found in the live system")
        elif _plain(live[name]) != _plain(e.get("value")):
            problems.append(f"{name}: registry {e.get('value')!r} != live {live[name]!r}")
    for name in sorted(live, key=str):
        if name not in seen:
            problems.append(f"{name}: live constant not registered (value {live[name]!r})")
    return not problems, problems


def load_live(spec, root):
    """{name: value} from a .py module (live_values()), a .json file, or a JSON literal."""
    text = str(spec).strip()
    if text.startswith("{"):
        return json.loads(text)
    path = text if os.path.isabs(text) else os.path.join(root, text)
    if path.endswith(".py"):
        mod_spec = importlib.util.spec_from_file_location("redteam_live", path)
        mod = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(mod)
        values = mod.live_values()
        if not isinstance(values, dict):
            raise TypeError("live_values() must return a dict of {name: value}")
        return values
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fingerprint(root, explicit=None):
    """The engine fingerprint: --fingerprint if given, else git's short HEAD at root, else ''."""
    if explicit:
        return str(explicit).strip()
    try:
        return subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", default="redteam/constants_registry.json")
    ap.add_argument("--live", default="redteam/live.py")
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--fingerprint")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    reg_path = a.registry if os.path.isabs(a.registry) else os.path.join(root, a.registry)
    with open(reg_path, encoding="utf-8") as f:
        reg = json.load(f)
    live = load_live(a.live, root)
    ok, problems = check(reg, live)
    fp = fingerprint(root, a.fingerprint)
    counts = {}
    for e in reg.get("constants", []):
        counts[str(e.get("status"))] = counts.get(str(e.get("status")), 0) + 1
    with open(reg_path, "rb") as f:
        reg_sha = hashlib.sha256(f.read()).hexdigest()[:12]
    rec = {"verdict": "PASS" if ok else "FAIL", "fingerprint": fp, "registry_sha256": reg_sha,
           "registered": len(reg.get("constants", [])), "live": len(live), "by_status": counts,
           "uncalibrated": [e["name"] for e in reg.get("constants", []) if e.get("status") == "uncalibrated"],
           "declared_band": [e["name"] for e in reg.get("constants", []) if e.get("status") == "declared_band"],
           "problems": problems}
    if a.json:
        out = a.json if os.path.isabs(a.json) else os.path.join(root, a.json)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1)
            f.write("\n")
    if ok:
        print(f"CONSTANTS CHECK: PASS — {rec['registered']} registered = {rec['live']} live on "
              f"{fp or 'no fingerprint (pass --fingerprint or run inside git)'}; "
              + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    else:
        print("CONSTANTS CHECK: FAIL")
        for p in problems:
            print("  " + p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
