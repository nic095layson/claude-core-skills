"""Follow Runbook 4 (install-and-surfaces SKILL.md) steps 1, 2 and 4 to the letter into an empty project.
Usage: python3 follow_runbook4.py LIBRARY_ROOT SKILL_MD PROJECT_DIR [--drop FILE]
Step 1: copy exactly the hooks/ files the step names (plus, for a step that says "the two self-tests" without
naming them, the self-tests step 4 names). Step 2: copy .claude/settings.json. Step 4: run every command the step
names, inside the project. Prints each command's last line and the step's verdict."""
import os, re, shutil, subprocess, sys
lib, skill, proj = sys.argv[1:4]
drop = sys.argv[sys.argv.index("--drop") + 1] if "--drop" in sys.argv else None
text = open(skill, encoding="utf-8").read()
step = lambda a, b: text[text.index(a):text.index(b)]
s1 = step("1. **Copy the hooks.**", "2. **Copy `.claude/settings.json`**")
s4 = step("4. **Self-test before committing:**", "5. **Verify live")
files = sorted(set(re.findall(r"hooks/([A-Za-z0-9_.-]+\.(?:py|sh))", s1)) - {"sync-copies.sh"})
commands = re.findall(r"`((?:python3|bash) hooks/[^`]+)`", s4)
if "two self-tests" in s1:
    files = sorted(set(files) | set(re.findall(r"hooks/([A-Za-z0-9_.-]+\.(?:py|sh))", s4)))
shutil.rmtree(proj, ignore_errors=True)
os.makedirs(os.path.join(proj, "hooks")); os.makedirs(os.path.join(proj, ".claude"))
for f in files:
    if f != drop:
        shutil.copy(os.path.join(lib, "hooks", f), os.path.join(proj, "hooks", f))
shutil.copy(os.path.join(lib, ".claude", "settings.json"), os.path.join(proj, ".claude", "settings.json"))
print("step 1 copied %d files%s: %s" % (len(files) - (1 if drop in files else 0),
      " (dropped %s)" % drop if drop else "", " ".join(f for f in files if f != drop)))
print("step 2 copied .claude/settings.json")
ok = True
for c in commands:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(["bash", "-c", c], cwd=proj, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       universal_newlines=True, env=env, timeout=900)
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    fails = [l.split("|")[0].strip() for l in lines if l.rstrip().endswith("FAIL")][:4]
    print("step 4 $ %s -> exit %d; %s%s" % (c, p.returncode, lines[-1][:120] if lines else "(no output)",
                                           ("; failing: " + ", ".join(fails)) if fails else ""))
    ok = ok and p.returncode == 0
print("== step 4 (the runbook's self-test): %s ==" % ("PASS" if ok else "FAIL"))
# what the copied settings wire that the project lacks
import json
missing = []
for ev, groups in json.load(open(os.path.join(proj, ".claude", "settings.json")))["hooks"].items():
    for g in groups:
        for h in g["hooks"]:
            for f in re.findall(r"/hooks/([A-Za-z0-9_.-]+\.(?:py|sh))", h["command"]):
                if not os.path.exists(os.path.join(proj, "hooks", f)):
                    missing.append("%s:%s" % (ev, f))
print("wired but missing in the project: %s" % (", ".join(sorted(set(missing))) or "none"))
