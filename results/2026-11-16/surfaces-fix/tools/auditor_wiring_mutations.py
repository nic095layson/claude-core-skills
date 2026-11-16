"""Apply the auditor's recorded wiring changes (rev-surfaces M3, M4, M5; verifier N1, N2, N3, N6) one at a time to
a scratch copy of a tree and run the table's wiring cases on each. Usage: python3 this.py TREE WORKDIR"""
import json, os, shutil, subprocess, sys
tree, work = sys.argv[1], sys.argv[2]
def pre_groups(d):
    return [g for g in d["hooks"]["PreToolUse"] if any("turn-gates-pretool" in x["command"] for x in g["hooks"])]
def m3(d):
    for g in pre_groups(d): g["matcher"] = "Edit|Write|NotebookEdit|Bash"
def m5(d):
    for g in d["hooks"]["Stop"]: g["hooks"] = [x for x in g["hooks"] if "receipt-law" not in x["command"]]
def n1(d):
    for g in pre_groups(d): g["matcher"] = "NoSuchTool"
def n2(d):
    for g in d["hooks"]["Stop"]: g["hooks"] = [x for x in g["hooks"] if "governance-enforce" in x["command"]]
    for g in d["hooks"]["PreToolUse"]: g["hooks"] = [x for x in g["hooks"] if "plan-gate-first-write" not in x["command"]]
def n6(d):
    d["hooks"]["PreToolUse"] = [g for g in d["hooks"]["PreToolUse"] if g not in pre_groups(d)]
SETTINGS, PLUGIN = (".claude", "settings.json"), ("plugin", "core-governance", "hooks", "hooks.json")
MUTS = [("M0", "control: no change", None, None), ("M3", "settings: turn-gates matcher cut to Edit|Write|NotebookEdit|Bash", SETTINGS, m3),
        ("M4", "plugin hooks.json: the same cut", PLUGIN, m3), ("M5", "settings: receipt gate removed from Stop", SETTINGS, m5),
        ("N1", "settings: turn-gates matcher -> NoSuchTool", SETTINGS, n1),
        ("N2", "settings: Stop keeps only governance-enforce; PreToolUse loses the plan-gate reminder", SETTINGS, n2),
        ("N3", "plugin hooks.json: turn-gates matcher -> NoSuchTool", PLUGIN, n1),
        ("N6", "settings: loses turn-gates-pretool entirely", SETTINGS, n6)]
want = sys.argv[3:] or [m[0] for m in MUTS]
for mid, what, place, fn in MUTS:
    if mid not in want: continue
    root = os.path.join(work, mid); shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(os.path.join(tree, "hooks"), os.path.join(root, "hooks"), ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(root, ".claude"))
    shutil.copy(os.path.join(tree, *SETTINGS), os.path.join(root, *SETTINGS))
    shutil.copytree(os.path.join(tree, "plugin", "core-governance"), os.path.join(root, "plugin", "core-governance"), ignore=shutil.ignore_patterns("__pycache__"))
    if fn:
        p = os.path.join(root, *place); d = json.load(open(p)); fn(d); json.dump(d, open(p, "w"), indent=2)
    out = subprocess.run([sys.executable, os.path.join(root, "hooks", "selftest-turn-gates.py"), "W"], stdout=subprocess.PIPE, universal_newlines=True).stdout
    fails = [l.split("|")[0].strip() for l in out.splitlines() if l.rstrip().endswith("FAIL")]
    print("%-3s %-88s -> failing W cases: %s" % (mid, what, ", ".join(fails) or "none"))
