"""Done-when 2: in a scratch copy of the tree, run every wired command of .claude/settings.json as the program
would (the command string through bash -c, CLAUDE_PROJECT_DIR set) on a Bash, an Edit, a Write, a merge-tool,
a Stop and a prompt payload: once with the hooks folder emptied, once with only turngate.py removed.
Usage: python3 missing_script_runs.py TREE WORK"""
import json, os, re, shutil, subprocess, sys
tree, work = sys.argv[1], sys.argv[2]
def selects(m, n):
    if not m or m == "*": return True
    if re.match(r"^[a-zA-Z0-9_|, -]+$", m): return n in [x.strip() for x in re.split(r"[|,]", m)]
    return re.search(m, n) is not None
rows = [{"type": "user", "message": {"role": "user", "content": "Build a script that processes the three sample files."}, "origin": {"kind": "human"}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "id": "toolu_1", "name": "Bash", "input": {"command": "git add -A && git commit -qm x"}}]}},
        {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_1", "content": ""}]}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Committed."}]}}]
CASES = [("Bash", "PreToolUse", "Bash", {"tool_input": {"command": "ls"}}),
         ("Bash+gh", "PreToolUse", "Bash", {"tool_input": {"command": "gh pr " + "merge 5 --squash"}}),
         ("Edit", "PreToolUse", "Edit", {"tool_input": {"file_path": "/tmp/x/a.md", "old_string": "a", "new_string": "b"}}),
         ("Write", "PreToolUse", "Write", {"tool_input": {"file_path": "/tmp/x/b.md", "content": "b"}}),
         ("merge tool", "PreToolUse", "mcp__github__merge_pull_request", {"tool_input": {"owner": "acme", "repo": "lib", "pullNumber": 5}}),
         ("Stop", "Stop", None, {"stop_hook_active": False}),
         ("prompt", "UserPromptSubmit", None, {"prompt": "Please merge the three pull requests and push to main."})]
settings = json.load(open(os.path.join(tree, ".claude", "settings.json")))["hooks"]
for variant in ("hooks folder emptied", "only turngate.py removed"):
    proj = os.path.join(work, variant.split()[0] + "-" + variant.split()[1])
    shutil.rmtree(proj, ignore_errors=True)
    shutil.copytree(os.path.join(tree, "hooks"), os.path.join(proj, "hooks"), ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(proj, ".claude")); shutil.copy(os.path.join(tree, ".claude", "settings.json"), os.path.join(proj, ".claude"))
    if variant.startswith("hooks"):
        for n in os.listdir(os.path.join(proj, "hooks")): os.remove(os.path.join(proj, "hooks", n))
    else:
        os.remove(os.path.join(proj, "hooks", "turngate.py"))
    rec = os.path.join(proj, "record.jsonl"); open(rec, "w").write("".join(json.dumps(r) + "\n" for r in rows))
    print("== %s (hooks/ now holds %d files)" % (variant, len(os.listdir(os.path.join(proj, "hooks")))))
    for label, event, tool, fields in CASES:
        payload = {"session_id": "w-" + label.replace(" ", ""), "transcript_path": rec, "cwd": proj, "hook_event_name": event}
        if tool: payload["tool_name"] = tool
        payload.update(fields)
        verdicts = []
        for g in settings.get(event, []):
            if tool and not selects(g.get("matcher"), tool): continue
            for h in g["hooks"]:
                env = dict(os.environ, CLAUDE_PROJECT_DIR=proj, PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(work, "tmp"))
                env.pop("CLAUDE_CODE_REMOTE", None)
                os.makedirs(env["TMPDIR"], exist_ok=True)
                p = subprocess.run(["bash", "-c", h["command"]], input=json.dumps(payload), stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True, env=env, timeout=30)
                out = p.stdout.strip()
                if p.returncode == 2: v = "exit 2 = DENIED/BLOCKED (" + p.stderr.strip()[-70:] + ")"
                elif '"permissionDecision": "deny"' in out: v = "deny: " + json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"][:60]
                elif '"decision": "block"' in out: v = "block: " + json.loads(out)["reason"][:60]
                elif out: v = "exit %d, context only" % p.returncode
                else: v = "exit %d, silent" % p.returncode
                verdicts.append("%s -> %s" % (re.findall(r"/hooks/([\w.-]+)", h["command"])[-1], v))
        print("  %-10s %s" % (label, " | ".join(verdicts)))
