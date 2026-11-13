#!/usr/bin/env python3
"""Orchestrator's own re-run of every finder's reproduction command (no agents). One line per finding:
id | exit | seconds | how many of the finder's 'observed' lines appear verbatim in my output."""
import json, subprocess, sys, os, time, re, tempfile, concurrent.futures as cf
PV = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(PV + "/all-results.json"))
groups = {}
for f in R["findings"]:
    groups.setdefault(f["_finder"], []).append(f)
def norm(s): return re.sub(r"\s+", " ", s).strip()
def run_group(key):
    out = []
    for f in groups[key]:
        t0 = time.time()
        cwd = tempfile.mkdtemp(prefix="rerun-")
        try:
            p = subprocess.run(["bash", "-c", f["repro_command"]], capture_output=True, text=True, timeout=240, cwd=cwd,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            rc, txt = p.returncode, (p.stdout + ("\n--- stderr ---\n" + p.stderr if p.stderr.strip() else ""))
        except subprocess.TimeoutExpired as e:
            rc, txt = "TIMEOUT", (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        open(f"{PV}/rerun/{f['id']}.txt", "w").write(txt)
        obs = [norm(l) for l in f["observed"].split("\n") if len(norm(l)) >= 12]
        mine = norm(txt)
        hit = sum(1 for l in obs if l in mine)
        out.append((f["id"], rc, round(time.time() - t0, 1), hit, len(obs), len(txt)))
    return out
with cf.ThreadPoolExecutor(max_workers=5) as ex:
    res = [r for g in ex.map(run_group, list(groups)) for r in g]
print("%-6s %-8s %6s  %s  %s" % ("id", "exit", "secs", "observed lines found", "bytes"))
for i, rc, secs, hit, n, nb in res:
    print("%-6s %-8s %6s  %2d / %-2d %s  %d" % (i, rc, secs, hit, n, "" if n and hit == n else ("  <-- look" if n else "  (no long lines to match)"), nb))
