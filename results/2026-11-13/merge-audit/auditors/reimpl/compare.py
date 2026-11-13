#!/usr/bin/env python3
"""compare.py — run the ORIGINAL hooks and MINE on every corpus case and write one line per case.

  python3 compare.py --out diff-run-1.txt            both implementations, whole corpus
  python3 compare.py --mine-only                     my implementation against the hand-written answers only
  python3 compare.py --orig DIR --out FILE           compare against another hook set (e.g. a mutated copy)
  python3 compare.py --only PREFIX                   restrict to case ids starting with PREFIX

Stop gate: only "block:F1" against anything else is compared. Pre-tool gate: deny (and which deny) against
anything else. The raw verdicts are printed too.
"""
import argparse
import concurrent.futures as cf
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["TMPDIR"] = os.path.join(HERE, "tmp")
os.makedirs(os.environ["TMPDIR"], exist_ok=True)
sys.path.insert(0, os.path.join(PACK, "pack", "tools"))
sys.path.insert(0, HERE)
import mk  # noqa: E402
import corpus  # noqa: E402

MINE = os.path.join(HERE, "mine")


def norm(gate, verdict):
    if gate == "stop":
        return "block:F1" if verdict == "block:F1" else "pass"
    return verdict if verdict.startswith("deny") else "pass"


def run_one(case, hooks):
    if case["gate"] == "stop":
        return mk.run_stop(case["path"], active=case["active"], hooks=hooks)[0]
    return mk.run_pre(case["path"], case["tool_name"], case["tool_input"], hooks=hooks)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--orig", default=mk.DEFAULT_HOOKS)
    ap.add_argument("--mine-only", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()

    cases = [c for c in corpus.write_all() if c["id"].startswith(a.only)]
    with cf.ThreadPoolExecutor(8) as ex:
        mine = list(ex.map(lambda c: run_one(c, MINE), cases))
        orig = ["-"] * len(cases) if a.mine_only else list(ex.map(lambda c: run_one(c, a.orig), cases))

    lines, differ, hand_bad_mine, hand_bad_orig, hand_n = [], 0, 0, 0, 0
    per_gate = {"stop": [0, 0], "pre": [0, 0]}
    for c, o, m in zip(cases, orig, mine):
        g = c["gate"]
        same = a.mine_only or norm(g, o) == norm(g, m)
        per_gate[g][0] += 1
        per_gate[g][1] += bool(same)
        differ += not same
        hand = ""
        if c["hand"]:
            hand_n += 1
            mo = norm(g, m) == norm(g, c["hand"])
            oo = a.mine_only or norm(g, o) == norm(g, c["hand"])
            hand_bad_mine += not mo
            hand_bad_orig += not oo
            hand = " | hand=%s mine:%s orig:%s" % (c["hand"], "ok" if mo else "WRONG", "-" if a.mine_only else ("ok" if oo else "WRONG"))
        lines.append("%-58s | orig=%-18s | mine=%-18s | %s%s | %s" % (c["id"], o, m, "AGREE " if same else "DIFFER", hand, c["note"]))

    head = ["# compare.py  orig hooks: %s   mine: %s" % ("(not run)" if a.mine_only else a.orig, MINE),
            "# cases: %d   agree: %d   differ: %d" % (len(cases), len(cases) - differ, differ),
            "# stop: %d cases, %d agree   pre: %d cases, %d agree" % (per_gate["stop"][0], per_gate["stop"][1], per_gate["pre"][0], per_gate["pre"][1]),
            "# hand-written known answers: %d   mine wrong: %d   original wrong: %s" % (hand_n, hand_bad_mine, "-" if a.mine_only else hand_bad_orig),
            "# line: case id | original verdict | my verdict | AGREE/DIFFER | note"]
    text = "\n".join(head + lines) + "\n"
    if a.out:
        with open(os.path.join(HERE, a.out) if not os.path.isabs(a.out) else a.out, "w") as fh:
            fh.write(text)
    print("\n".join(head))
    if a.mine_only:
        for ln in lines:
            if "WRONG" in ln:
                print(ln)
    else:
        for ln in lines:
            if "DIFFER" in ln or "WRONG" in ln:
                print(ln)


if __name__ == "__main__":
    main()
