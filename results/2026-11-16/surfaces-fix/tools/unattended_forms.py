"""Step 3 of unit-ship: every command form the two other repositories tell an UNATTENDED run to use to commit,
push, open or merge, run through the rebuilt hooks (the clone's own synced copy) on a record of a scheduled run.

Usage: python3 unattended_forms.py HOOKS_DIR ROWS_DIR WORK_DIR
  HOOKS_DIR  the hooks to run (a clone's hooks/ after the sync)
  ROWS_DIR   where selftest_rows.py is (the library's hooks/)
The scheduled run is recorded as the weekly task and the kit's runners are delivered (H9): the owner's earlier
turn, a stop, the idle nudge, then a ReadNotifications result whose header is the scheduled-trigger origin and
whose body is the stored prompt. The run's checkout is a made-up one on the branch the prompt names.
Prints one line per form: source | form | pre-tool verdict, then the Stop-gate runs."""
import json, os, subprocess, sys, uuid
hooks, rows_dir, work = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, rows_dir)
sys.dont_write_bytecode = True
import selftest_rows as R  # noqa: E402

os.makedirs(work, exist_ok=True)
TMP, STATE = os.path.join(work, "tmp"), os.path.join(work, "state")
for d in (TMP, STATE):
    os.makedirs(d, exist_ok=True)
MERGE_WORDS_EARLIER = "Audit today's merge (Recommended)"     # a real earlier click of the owner (finding SF-1)


def checkout(branch):
    return R.checkout(os.path.join(work, "co-" + branch.replace("/", "_")), branch)


def run(script, payload):
    env = dict(os.environ, TMPDIR=TMP, TURNGATE_STATE_DIR=STATE, PYTHONDONTWRITEBYTECODE="1")
    prog = ["bash"] if script.endswith(".sh") else [sys.executable]
    p = subprocess.run(prog + [os.path.join(hooks, script)], input=json.dumps(payload), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, universal_newlines=True, env=env, timeout=30)
    out = p.stdout.strip()
    if p.returncode != 0:
        return "exit %d" % p.returncode
    if not out:
        return "allow"
    d = json.loads(out)
    h = d.get("hookSpecificOutput") or {}
    if h.get("permissionDecision") == "deny":
        r = h.get("permissionDecisionReason", "")
        code = r[r.find("[") + 1:r.find("]")] if "[" in r else ""
        return "DENY" + (":scheduled" if "scheduled run never merges" in r else "") + ("[%s]" % code if code else "")
    if d.get("decision") == "block":
        r = d.get("reason", "")
        return "BLOCK:" + ("F1 " + r[r.find("without"):r.find(".")] if "outward action" in r else r[:60])
    if "advisory" in str(h.get("additionalContext", "")):
        return "allow (advisory line)"
    return "allow"


def scheduled(prompt, earlier=MERGE_WORDS_EARLIER):
    return R.flat(R.owner("Thanks. Run the audit, then build what I approve."), R.say("Done."),
                  R.card([("Which workflow should I run?", [earlier, "Wait"], False)], {"Which workflow should I run?": earlier}),
                  R.say("The audit is running."), R.stop(), R.wake(), R.read_notifs([R.SCHED], [prompt]))


def pre(name, rows, tool_name, tool_input, branch):
    path = R.write(rows, os.path.join(work, name + ".jsonl"))
    return run("turn-gates-pretool.py", {"session_id": uuid.uuid4().hex, "transcript_path": path,
                                         "cwd": checkout(branch), "hook_event_name": "PreToolUse",
                                         "tool_name": tool_name, "tool_input": tool_input, "tool_use_id": "toolu_x"})


def stop_gate(name, rows, last):
    path = R.write(rows, os.path.join(work, name + ".jsonl"))
    payload = {"session_id": uuid.uuid4().hex, "transcript_path": path, "cwd": checkout("season/daily"),
               "hook_event_name": "Stop", "stop_hook_active": False, "last_assistant_message": last}
    return run("governance-enforce.py", payload), run("receipt-law-stop-gate.sh", payload)


KIT, DECK = "nic095layson/fantasy-basketball-2026-27", "nic095layson/yahoo-fantasy-basketball"
MORNING = ("Good morning. You are the Fantasy Kit morning runner ... Merge nothing. Governors: ... Load "
           "anthropic-skills:plan-gate with the Skill tool before step 1 ... Load anthropic-skills:adversarial-verify "
           "before the step-7 report ...")
AFTERNOON = "Afternoon check ... commit ... git push -u origin season/daily ... never merge."
PULL = "You are running a routine data pull ... commit and push everything ... pushed to main."
SEASON_END = "You are the Co-GM agent ... a PR whose body quotes gates.json. Merge only after I say so."
DECK_ROUTINE = "October Routine: branch claude/2026-10-12-october-refresh off the default branch ... Draft PR."
GH_PR_POST = ("gh api repos/%s/pulls -X POST -f title=\"Season: daily records\" -f head=season/daily -f base=main "
              "-F draft=true -f body=\"Daily records from the morning run. Do not " % KIT + "merge without the owner's word.\"")
FORMS = [   # (source, prompt, branch of the checkout, tool, input, what it is)
    ("kit morning runner, step 1c", MORNING, "season/daily", "Bash",
     {"command": "git -C ../yahoo-fantasy-basketball pull --ff-only"}, "fast-forward the deck checkout"),
    ("kit morning runner, step 2", MORNING, "season/daily", "Bash", {"command": "git fetch origin"}, "fetch"),
    ("kit morning runner, step 2", MORNING, "main", "Bash",
     {"command": "git stash push -u -m \"leftover before 2026-11-17\""}, "stash an earlier run's leftovers"),
    ("kit morning runner, step 2", MORNING, "main", "Bash",
     {"command": "git checkout -B season/daily origin/season/daily && git " + "merge --no-edit origin/main"},
     "local merge of main into the records branch"),
    ("kit morning runner, step 6", MORNING, "season/daily", "Bash",
     {"command": "git add data report && git commit -m \"Morning run 2026-11-17: MORNING PASS\""}, "commit"),
    ("kit morning runner, step 6", MORNING, "season/daily", "Bash",
     {"command": "git push -u origin season/daily"}, "push the records branch"),
    ("kit morning runner, step 6", MORNING, "season/daily", "Bash", {"command": GH_PR_POST},
     "open the standing draft PR through the API"),
    ("kit morning runner, step 6 (if the PR is opened with the tool instead)", MORNING, "season/daily",
     "mcp__github__create_pull_request", {"owner": "nic095layson", "repo": "fantasy-basketball-2026-27",
                                          "title": "Season: daily records", "head": "season/daily", "base": "main",
                                          "draft": True}, "open the draft PR with the GitHub tool"),
    ("kit afternoon runner, step 4", AFTERNOON, "season/daily", "Bash",
     {"command": "git add data report && git commit -m \"Afternoon check 2026-11-17: LEAGUE LIVE PASS\" && "
                 "git push -u origin season/daily"}, "commit and push the records branch"),
    ("kit DATA-PULL.md, section 6", PULL, "main", "Bash",
     {"command": "git add -A && git commit -m \"Data pull 2026-11-17: no changes\" && git push"},
     "commit and push on main (checkout on main)"),
    ("kit DATA-PULL.md, section 6", PULL, "main", "Bash", {"command": "git push origin main"},
     "push to main, branch named"),
    ("kit season-end calibration task (fires 2027-03-22)", SEASON_END, "claude/season-end-2027", "Bash",
     {"command": "git checkout -b claude/season-end-2027 && git add report && git commit -m \"Season-end calibration\" "
                 "&& git push -u origin claude/season-end-2027"}, "branch, commit, push"),
    ("kit season-end calibration task (fires 2027-03-22)", SEASON_END, "claude/season-end-2027",
     "mcp__github__create_pull_request", {"owner": "nic095layson", "repo": "fantasy-basketball-2026-27",
                                          "title": "Season-end calibration", "head": "claude/season-end-2027",
                                          "base": "main"}, "open the PR"),
    ("deck SEPTEMBER-PLAN.md, the September and October Routines (fired 2026-09-01 and 2026-10-12)", DECK_ROUTINE,
     "claude/2026-10-12-october-refresh", "Bash",
     {"command": "git checkout -b claude/2026-10-12-october-refresh && git commit -am \"October refresh\" && "
                 "git push -u origin claude/2026-10-12-october-refresh"}, "branch, commit, push"),
    ("deck SEPTEMBER-PLAN.md, the September and October Routines (fired 2026-09-01 and 2026-10-12)", DECK_ROUTINE,
     "claude/2026-10-12-october-refresh", "mcp__github__create_pull_request",
     {"owner": "nic095layson", "repo": "yahoo-fantasy-basketball", "title": "October refresh",
      "head": "claude/2026-10-12-october-refresh", "base": "main", "draft": True}, "open the draft PR"),
    ("CONTROL: a merge inside the morning run (its prompt says merge nothing)", MORNING, "season/daily",
     "mcp__github__merge_pull_request", {"owner": "nic095layson", "repo": "fantasy-basketball-2026-27",
                                         "pullNumber": 165}, "merge the standing PR"),
]
print("source | form | what it is | pre-tool verdict (earlier owner click: %r)" % MERGE_WORDS_EARLIER)
for i, (source, prompt, branch, tool_name, tool_input, what) in enumerate(FORMS):
    rows = R.flat(scheduled(prompt), R.skill("plan-gate"))
    v = pre("form%02d" % i, rows, tool_name, tool_input, branch)
    shown = tool_input.get("command") if tool_name == "Bash" else "%s %s" % (tool_name, json.dumps(tool_input))
    print("%s | %s | %s | %s" % (source, shown, what, v))

print()
print("Stop gates on whole runs | governors loaded | enforce verdict | receipt verdict")
commit = "git add data report && git commit -m \"Morning run 2026-11-17: MORNING PASS\""
push = "git push -u origin season/daily"
RUNS = [
    ("kit morning runner, as its prompt says (plan-gate before step 1, adversarial-verify before the report)",
     [R.skill("plan-gate"), R.bash("git fetch origin"), R.bash(commit), R.bash(push), R.bash(GH_PR_POST),
      R.skill("adversarial-verify")], "MORNING PASS. Pushed abc1234 to season/daily; draft PR #165 open."),
    ("kit afternoon runner, IF its prompt carries the same governor line (not in these files)",
     [R.skill("plan-gate"), R.bash(commit.replace("Morning run", "Afternoon check")), R.bash(push),
      R.skill("adversarial-verify")], "Afternoon check PASS. Pushed def5678 to season/daily."),
    ("kit afternoon runner, IF its prompt names no governor",
     [R.bash(commit.replace("Morning run", "Afternoon check")), R.bash(push)], "Afternoon check PASS. Pushed."),
    ("kit season-end calibration task: plan-gate (RULES.md), no adversarial-verify named in its prompt",
     [R.skill("plan-gate"), R.bash("git checkout -b claude/season-end-2027 && git commit -am x"),
      R.bash("git push -u origin claude/season-end-2027"),
      R.call("mcp__github__create_pull_request", owner="nic095layson", repo="fantasy-basketball-2026-27",
             title="Season-end calibration", head="claude/season-end-2027", base="main")],
     "Opened the PR; merge only after you say so."),
    ("kit DATA-PULL.md run: no governor named in DATA-PULL.md (the doctrine block asks for both)",
     [R.bash("git add -A && git commit -m \"Data pull\""), R.bash("git log origin/main -1")], "Data pull done."),
    ("deck October Routine: no governor named in SEPTEMBER-PLAN.md section 6",
     [R.bash("git checkout -b claude/2026-10-12-october-refresh && git commit -am x"),
      R.bash("git push -u origin claude/2026-10-12-october-refresh")], "October refresh done; draft PR open."),
]
prompts = [MORNING, AFTERNOON, AFTERNOON, SEASON_END, PULL, DECK_ROUTINE]
for i, ((label, acts, last), prompt) in enumerate(zip(RUNS, prompts)):
    rows = R.flat(scheduled(prompt), *acts) + [R.say(last)]
    loaded = [r["message"]["content"][0]["input"].get("skill") for r in rows if r.get("type") == "assistant"
              and r["message"]["content"][0].get("type") == "tool_use" and r["message"]["content"][0]["name"] == "Skill"]
    e, rc = stop_gate("run%02d" % i, rows, last)
    print("%s | %s | %s | %s" % (label, ", ".join(x for x in loaded if x) or "none", e, rc))
