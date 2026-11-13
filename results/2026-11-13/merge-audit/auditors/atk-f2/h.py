#!/usr/bin/env python3
"""Shared harness for the atk-f2 audit. Builds a fixture + a call file per case and runs the pre-tool hook.

Each case is kept as two files under fx/:  <id>.jsonl (transcript rows)  and  <id>.call.json
({"tool_name":..., "tool_input":...}).  run1.py replays one case from those two files.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PACK, "pack", "tools"))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
import mk  # noqa: E402

FX = os.path.join(HERE, "fx")
M = "mcp__github__merge_pull_request"
M2 = "mcp__GH__merge_pull_request"
GHM = "gh pr " + "merge"          # the three words, kept out of any shell command line


def pr(n, **kw):
    d = {"owner": "nic095layson", "repo": "claude-core-skills", "pullNumber": n}
    d.update(kw)
    return d


def case(cid, rows, tool_name, tool_input, expect, note="", hooks=None, keep=True):
    """Run one case; returns (got, detail). Prints one table line."""
    if keep:
        path = mk.write(rows, keep_dir=FX, name=cid + ".jsonl")
        with open(os.path.join(FX, cid + ".call.json"), "w") as fh:
            json.dump({"tool_name": tool_name, "tool_input": tool_input}, fh)
    else:
        path = mk.write(rows)
    got, detail = mk.run_pre(path, tool_name, tool_input, hooks=hooks, session_id="atkf2-" + cid)
    short = got if got.startswith(("allow", "deny", "advise")) else got
    flag = "ok      " if (expect is None or short == expect or (expect == "deny" and short.startswith("deny"))) else "MISMATCH"
    print("%-8s %-6s want=%-16s got=%-16s %s" % (flag, cid, expect, short, note))
    return got, detail
