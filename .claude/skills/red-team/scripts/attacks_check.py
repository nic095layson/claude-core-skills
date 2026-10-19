#!/usr/bin/env python3
"""Attacks check: the standing attack list against its records and the live engine fingerprint, written as a
numbered artifact (red-team skill, steps 6 and 7). Generalized 2026-10-19 from the fantasy-basketball kit's
run_attacks.py (ledger INC-2026-10-19-01).

Why it exists: the incident's second finding was that the engine changed between a report's records and the
report, and nothing said so. A record that does not name the engine it ran on is a claim about an engine
nobody can name; a record made on another engine is STALE and fails. The list is append-only: a row is
retired with a date, never deleted, so the next reader can see every attack the system has faced.

Inputs
  --attacks PATH      redteam/attacks.json (default), {"attacks": [row, ...]}
                      row: {"id", "name", "question", "script", "record", "commit_field", "added", "retired"}
                      commit_field: dotted path to the fingerprint inside the record JSON, or null
  --root DIR          the project root (default: the current directory); script and record paths resolve here
  --fingerprint X     the live engine fingerprint (default: `git rev-parse --short HEAD` at root)
  --out PATH          write the numbered artifact here

Row statuses: CURRENT (script and record present, fingerprints agree); MISSING (script or record absent, or
the record lacks its commit field); STALE (record fingerprint differs from the live one, or no live
fingerprint is available to compare); DUPLICATE (an id used twice); UNFINGERPRINTED (commit_field null:
allowed and counted); RETIRED (kept, skipped). MISSING, STALE and DUPLICATE fail; an empty list fails.
Prints 'ATTACKS CHECK: PASS — N attacks on <fingerprint>; <counts>' or 'ATTACKS CHECK: FAIL' + problems.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys


def live_fingerprint(root, explicit=None):
    if explicit:
        return str(explicit).strip()
    try:
        return subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def _dig(rec, dotted):
    cur = rec
    for part in str(dotted).split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()[:12]


def _same_engine(recorded, live):
    """True when both carry at least 7 characters (git's shortest abbreviation) and one is a prefix of the
    other (short vs long hashes). A shorter value never matches: a two-character --fingerprint must not
    read a STALE record as CURRENT."""
    r, l = str(recorded or "").strip(), str(live or "").strip()
    if len(r) < 7 or len(l) < 7:
        return False
    n = min(len(r), len(l))
    return r[:n] == l[:n]


def check(attacks, root, fingerprint):
    rows, problems, seen = [], [], set()
    for a in attacks.get("attacks", []):
        row = dict(id=a.get("id"), name=a.get("name"), question=a.get("question"), script=a.get("script"),
                   record=a.get("record"), added=a.get("added"), status="CURRENT", why="")
        if a.get("id") in seen:
            problems.append(f"duplicate attack id {a.get('id')}")
            row["status"], row["why"] = "DUPLICATE", "id used twice"
            rows.append(row)
            continue
        seen.add(a.get("id"))
        if a.get("retired"):
            row["status"], row["why"] = "RETIRED", str(a["retired"])
            rows.append(row)
            continue
        sp = os.path.join(root, a.get("script") or "")
        rp = os.path.join(root, a.get("record") or "")
        if not a.get("script") or not os.path.exists(sp):
            row["status"], row["why"] = "MISSING", f"script {a.get('script')} not found"
        elif not a.get("record") or not os.path.exists(rp):
            row["status"], row["why"] = "MISSING", f"record {a.get('record')} not found"
        else:
            row["record_sha256"] = _sha(rp)
            if a.get("commit_field"):
                try:
                    with open(rp, encoding="utf-8") as f:
                        c = _dig(json.load(f), a["commit_field"])
                except ValueError as e:
                    c, row["why"] = None, f"record unreadable: {e}"
                if not c:
                    row["status"], row["why"] = "MISSING", row["why"] or f"record has no {a['commit_field']}"
                elif not fingerprint:
                    row["status"], row["why"] = "STALE", (f"record made on engine {c}; no live fingerprint "
                                                         "to compare (pass --fingerprint or run inside git)")
                elif not _same_engine(c, fingerprint):
                    row["status"], row["why"] = "STALE", f"record made on engine {c}, live engine is {fingerprint}"
                else:
                    row["fingerprint"] = c
            else:
                row["status"] = "UNFINGERPRINTED"
        if row["status"] in ("MISSING", "STALE"):
            problems.append(f"{row['id']} {row['status']}: {row['why']}")
        rows.append(row)
    active = [r for r in rows if r["status"] != "RETIRED"]
    if not active:
        problems.append("no active attacks registered")
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return dict(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                fingerprint=fingerprint, attacks=rows, by_status=counts, problems=problems,
                verdict="PASS" if not problems else "FAIL")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--attacks", default="redteam/attacks.json")
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--fingerprint")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    path = a.attacks if os.path.isabs(a.attacks) else os.path.join(root, a.attacks)
    with open(path, encoding="utf-8") as f:
        attacks = json.load(f)
    rec = check(attacks, root, live_fingerprint(root, a.fingerprint))
    if a.out:
        out = a.out if os.path.isabs(a.out) else os.path.join(root, a.out)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1, ensure_ascii=False)
            f.write("\n")
    if rec["verdict"] == "PASS":
        print(f"ATTACKS CHECK: PASS — {len(rec['attacks'])} attacks on {rec['fingerprint'] or 'no fingerprint'}; "
              + ", ".join(f"{k} {v}" for k, v in sorted(rec["by_status"].items())))
    else:
        print("ATTACKS CHECK: FAIL")
        for p in rec["problems"]:
            print("  " + p)
    return 0 if rec["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
