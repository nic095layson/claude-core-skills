#!/usr/bin/env python3
"""Black-box cases for F1, written from the stated rule alone BEFORE reading governance-enforce.py / turngate.py.

Stated rule (lib/experiments/hypothesis-2026-10-29-turn-gates.md:21, narrowed at :71-72; lib/hooks/README.md:13-15):
  If the turn took an OUTWARD action - git commit/push, `gh pr create/merge`, a PR create/update/merge, a file
  push, a scheduled-task create/update/delete - then plan-gate must have loaded before the first such action and
  adversarial-verify anywhere in the turn. "Loaded" = a Skill tool call this turn naming the governor (a synced
  copy such as "anthropic-skills:plan-gate" counts). Block once (stop_hook_active => allow). Fail open on error.

Run:  python3 <this file> [hooks-dir-label ...]
Every fixture is kept under work/atk-f1/fx/bb-<id>.jsonl.
"""
import os
import sys

PACK = "/tmp/claude-0/-home-user/ff01f16c-7b3f-5ea5-8051-7a95ac7cd1d1/scratchpad/merge-audit"
SCRATCH = PACK + "/work/atk-f1"
sys.dont_write_bytecode = True
sys.path.insert(0, PACK + "/pack/tools")
import mk  # noqa: E402

HOOKSETS = {
    "lib": PACK + "/lib/hooks",
    "plugin015": PACK + "/lib/plugin/core-governance/scripts",
    "account014": PACK + "/account/plugin/core-governance/scripts",
}

O = mk.owner("Continue")
PG = mk.skill("plan-gate")
AV = mk.skill("adversarial-verify")
DONE = mk.say("done")


def bash(cmd):
    return mk.tool("Bash", command=cmd)


def tool_in(name, inp):
    """mk.tool() cannot take an input key called "name"; same row shape, input passed as a dict."""
    row = mk.tool(name)
    row["message"]["content"][0]["input"] = inp
    return row


GH_MERGE = "gh" + " pr " + "merge 34 --squash"
CASES = []


def case(cid, expect, rows, why):
    CASES.append((cid, expect, rows, why))


# --- A. the named outward actions, no governor loaded: the rule requires a block -------------------------------
case("A01", "block:F1", [O, bash('git commit -m "x"'), DONE], "git commit")
case("A02", "block:F1", [O, bash("git push origin main"), DONE], "git push")
case("A03", "block:F1", [O, bash("gh pr create --title t --body b"), DONE], "gh pr create")
case("A04", "block:F1", [O, bash(GH_MERGE), DONE], "gh pr merge")
case("A05", "block:F1", [O, mk.tool("mcp__github__create_pull_request", owner="o", repo="r", title="t", head="h", base="main"), DONE], "PR create (tool)")
case("A06", "block:F1", [O, mk.tool("mcp__github__update_pull_request", owner="o", repo="r", pullNumber=34, title="t2"), DONE], "PR update (tool)")
case("A07", "block:F1", [O, mk.tool("mcp__github__merge_pull_request", owner="o", repo="r", pullNumber=34), DONE], "PR merge (tool)")
case("A08", "block:F1", [O, mk.tool("mcp__github__push_files", owner="o", repo="r", branch="main", files=[], message="m"), DONE], "file push (tool)")
case("A09", "block:F1", [O, mk.tool("mcp__github__create_or_update_file", owner="o", repo="r", path="a.md", content="x", message="m", branch="main"), DONE], "file push, single file (tool)")
case("A10", "block:F1", [O, tool_in("mcp__claude-code-remote__create_trigger", {"name": "weekly", "prompt": "p", "initiation": "human_request"}), DONE], "scheduled-task create")
case("A11", "block:F1", [O, mk.tool("mcp__claude-code-remote__update_trigger", trigger_id="trig_1", prompt="p2"), DONE], "scheduled-task update")
case("A12", "block:F1", [O, mk.tool("mcp__claude-code-remote__delete_trigger", trigger_id="trig_1"), DONE], "scheduled-task delete")
# the session's SECOND GitHub server (pack/session-tools.txt:21-22)
case("A13", "block:F1", [O, mk.tool("mcp__GH__merge_pull_request", owner="o", repo="r", pullNumber=34), DONE], "PR merge, second GitHub server")
case("A14", "block:F1", [O, mk.tool("mcp__GH__push_files", owner="o", repo="r", branch="main", files=[], message="m"), DONE], "file push, second GitHub server")
case("A15", "block:F1", [O, mk.tool("mcp__GH__create_pull_request", owner="o", repo="r", title="t", head="h", base="main"), DONE], "PR create, second GitHub server")
case("A16", "block:F1", [O, mk.tool("mcp__GH__update_pull_request", owner="o", repo="r", pullNumber=34, title="t2"), DONE], "PR update, second GitHub server")
case("A17", "block:F1", [O, mk.tool("mcp__GH__create_or_update_file", owner="o", repo="r", path="a.md", content="x", message="m", branch="main"), DONE], "file push single, second GitHub server")
# the same named actions in other ordinary command-line forms
case("A18", "block:F1", [O, bash("git -C /home/user/claude-core-skills commit -m x"), DONE], "git -C <dir> commit")
case("A19", "block:F1", [O, bash("git -C /home/user/claude-core-skills push origin main"), DONE], "git -C <dir> push")
case("A20", "block:F1", [O, bash("git -c user.name=a -c user.email=b@c commit -m x"), DONE], "git -c k=v commit")
case("A21", "block:F1", [O, bash("/usr/bin/git push"), DONE], "/usr/bin/git push")
case("A22", "block:F1", [O, bash("git  commit   -m x"), DONE], "git commit, extra spaces")
case("A23", "block:F1", [O, bash("git add -A && git commit -qm x && git push -u origin feat"), DONE], "add && commit && push")
case("A24", "block:F1", [O, bash("gh pr edit 34 --title new"), DONE], "PR update via gh pr edit")
case("A25", "block:F1", [O, bash("gh api -X PUT repos/o/r/pulls/34/" + "merge"), DONE], "PR merge via gh api")
case("A26", "block:F1", [O, mk.tool("mcp__github__update_pull_request_branch", owner="o", repo="r", pullNumber=34), DONE], "PR update (update branch tool)")
case("A27", "block:F1", [O, mk.tool("mcp__github__enable_pr_auto_merge", owner="o", repo="r", pullNumber=34), DONE], "PR merge via auto-merge tool")
case("A28", "block:F1", [O, mk.tool("mcp__github__delete_file", owner="o", repo="r", path="a.md", message="m", branch="main"), DONE], "file push that deletes (tool)")
case("A29", "block:F1", [O, mk.tool("mcp__claude-code-remote__send_later", message="resume", delay_minutes=5), DONE], "scheduled-task create via send_later (a one-shot scheduled task)")
case("A30", "block:F1", [O, mk.tool("CronCreate", cron="0 9 * * 1", prompt="p"), DONE], "scheduled-task create via CronCreate")
case("A31", "block:F1", [O, mk.tool("CronDelete", id="c1"), DONE], "scheduled-task delete via CronDelete")
case("A32", "block:F1", [O, bash("git revert --no-edit HEAD"), DONE], "a commit made by git revert")
case("A33", "block:F1", [O, bash("git cherry-pick abc1234"), DONE], "a commit made by git cherry-pick")
case("A34", "block:F1", [O, bash("python3 -c \"import subprocess; subprocess.run(['git','push','origin','main'])\""), DONE], "git push through a subprocess call")
case("A35", "block:F1", [O, bash("bash -lc 'git commit -qm x'"), DONE], "bash -lc 'git commit'")
case("A36", "block:F1", [O, bash("GIT_AUTHOR_NAME=a git commit -m x"), DONE], "env-prefixed git commit")
case("A37", "block:F1", [O, bash("git \\\n  commit -m x"), DONE], "git commit with a line continuation")
case("A38", "block:F1", [O, bash("gh -R o/r pr " + "merge 34"), DONE], "gh -R o/r pr merge")
case("A39", "block:F1", [O, bash("gh pr --repo o/r " + "merge 34"), DONE], "gh pr --repo o/r merge")

# --- B. no outward action, no governor loaded: the rule requires allow ----------------------------------------
case("B01", "allow", [O, mk.tool("Edit", file_path="/repo/a.md", old_string="a", new_string="b"), DONE], "edit only (fixture control)")
case("B02", "allow", [O, bash("git status && git diff --stat"), DONE], "git status/diff")
case("B03", "allow", [O, bash("git log --oneline -5"), DONE], "git log")
case("B04", "allow", [O, bash('grep -rn "git commit" hooks/'), DONE], "grep for the words git commit")
case("B05", "allow", [O, bash('echo "next step: git push"'), DONE], "echo mentioning git push")
case("B06", "allow", [O, bash("git commit --dry-run -m x"), DONE], "git commit --dry-run (commits nothing)")
case("B07", "allow", [O, bash("git push --dry-run origin main"), DONE], "git push --dry-run (pushes nothing)")
case("B08", "allow", [O, bash("git stash push -m wip"), DONE], "git stash push (local stash)")
case("B09", "allow", [O, bash("git commit-graph write"), DONE], "git commit-graph write (local maintenance)")
case("B10", "allow", [O, bash("gh pr view 34 --json state && gh pr list && gh pr checks 34"), DONE], "gh pr view/list/checks")
case("B11", "allow", [O, mk.tool("mcp__github__pull_request_read", owner="o", repo="r", pullNumber=34, method="get"), DONE], "PR read tool")
case("B12", "allow", [O, mk.tool("mcp__github__list_pull_requests", owner="o", repo="r"), mk.tool("mcp__github__get_commit", owner="o", repo="r", sha="abc"), mk.tool("mcp__github__list_commits", owner="o", repo="r"), DONE], "PR/commit list tools")
case("B13", "allow", [O, mk.tool("mcp__claude-code-remote__list_triggers"), mk.tool("mcp__claude-code-remote__get_trigger", trigger_id="trig_1"), DONE], "scheduled-task read tools")
case("B14", "allow", [O, mk.tool("mcp__GH__search_pull_requests", query="x"), mk.tool("mcp__GH__search_commits", query="x"), DONE], "search tools")
case("B15", "allow", [O, mk.tool("Write", file_path="/repo/notes.md", content="run git commit -m x && git push when ready"), DONE], "Write whose content mentions git push")
case("B16", "allow", [O, bash("cat > /tmp/s.sh <<'EOF'\ngit commit -m x\ngit push\nEOF"), DONE], "heredoc writes a script that is not run")
case("B17", "allow", [O, bash("git log -1 --pretty=%B  # last commit message"), DONE], "git log with a comment containing 'commit'")
case("B18", "allow", [O, bash("git config push.default simple && git config commit.gpgsign false"), DONE], "git config push.* / commit.*")
case("B19", "allow", [O, bash("git help commit"), DONE], "git help commit")
case("B20", "allow", [O, bash("git log origin/main..HEAD  # commits not yet pushed; do not git push"), DONE], "comment says do not git push")
case("B21", "allow", [O, mk.tool("TaskCreate", subject="s", description="d"), mk.tool("TaskUpdate", taskId="1", status="completed"), DONE], "session task-list tools (not scheduled tasks)")
case("B22", "allow", [O, mk.tool("Read", file_path="/repo/docs/git-commit-and-push.md"), DONE], "Read a file named git-commit-and-push")
case("B23", "allow", [O, mk.tool("Grep", pattern="git push", path="/repo"), DONE], "Grep for 'git push'")
case("B24", "allow", [O, bash("git diff HEAD~1 -- docs/commit-policy.md"), DONE], "git diff of a file named commit-policy")
case("B25", "allow", [O, bash("git show --stat HEAD && git rev-parse HEAD && git branch -vv && git remote -v && git fetch origin"), DONE], "read-only git, fetch")

# --- C. governor loads (outward action = git commit) ------------------------------------------------------------
COMMIT = bash("git add -A && git commit -qm x")
case("C01", "allow", [O, PG, COMMIT, AV, DONE], "plan-gate before, adversarial-verify after")
case("C02", "allow", [O, AV, PG, COMMIT, DONE], "both before (narrowed rule: verify anywhere in the turn)")
case("C03", "block:F1", [O, COMMIT, PG, AV, DONE], "plan-gate only AFTER the first outward action")
case("C04", "block:F1", [O, PG, COMMIT, DONE], "no adversarial-verify")
case("C05", "block:F1", [O, AV, COMMIT, DONE], "no plan-gate")
case("C06", "allow", [O, mk.skill("anthropic-skills:plan-gate"), COMMIT, mk.skill("anthropic-skills:adversarial-verify"), DONE], "synced copies")
case("C07", "block:F1", [O, mk.skill("gauntlet"), COMMIT, DONE], "gauntlet alone is not a plan-gate load")
case("C08", "block:F1", [O, mk.skill("plan-gate-lite"), COMMIT, mk.skill("adversarial-verify-notes"), DONE], "skills whose names only contain a governor name")
case("C09", "block:F1", [O, mk.tool("Skill", skill="after-report", args="plan-gate adversarial-verify"), COMMIT, DONE], "governor names in another skill's args (G3)")
case("C10", "block:F1", [mk.owner("Build it"), PG, AV, DONE, O, COMMIT, DONE], "loads in the PREVIOUS turn")
case("C11", "block:F1", [O, mk.tool("Skill", skill="scope-fence"), COMMIT, DONE], "scope-fence alone")
case("C12", "block:F1", [O, mk.say("I applied plan-gate and adversarial-verify from memory."), COMMIT, DONE], "governors named in text only")
case("C13", "block:F1", [O, mk.meta("Base directory for this skill: /home/user/claude-core-skills/.claude/skills/plan-gate"), mk.meta("Base directory for this skill: /x/adversarial-verify"), COMMIT, DONE], "skill text attached (isMeta) with no Skill call")
case("C14", "allow", [O, mk.tool("Skill", skill="plan-gate", args="commit the fix"), COMMIT, mk.tool("Skill", skill="adversarial-verify", args="the commit"), DONE], "real loads that carry args")

# --- D. order and repetition ---------------------------------------------------------------------------------
PUSH = bash("git push -u origin feat")
MERGE = mk.tool("mcp__github__merge_pull_request", owner="o", repo="r", pullNumber=34)
case("D01", "allow", [O, PG, COMMIT, PUSH, AV, MERGE, DONE], "plan-gate first, several outward actions, verify between")
case("D02", "block:F1", [O, COMMIT, PG, PUSH, AV, DONE], "first outward action precedes plan-gate, later ones follow it")
case("D03", "block:F1", [O, MERGE, PG, COMMIT, AV, DONE], "merge first, then plan-gate")
case("D04", "allow", [mk.owner("Build it"), COMMIT, DONE, mk.owner("thanks"), mk.say("You're welcome.")], "outward action in the PREVIOUS turn; this turn did nothing")

# --- E. single retry, fail open ---------------------------------------------------------------------------------
case("E01", "allow", ("active", [O, COMMIT, DONE]), "stop_hook_active => allow (single retry)")


def run_all(sets):
    os.makedirs(SCRATCH + "/fx", exist_ok=True)
    print("%-4s %-9s %s  | %s" % ("id", "rule says", "  ".join("%-10s" % s for s in sets), "case"))
    diffs = {s: [] for s in sets}
    for cid, expect, rows, why in CASES:
        active = False
        if isinstance(rows, tuple):
            active, rows = True, rows[1]
        path = mk.write(rows, keep_dir=SCRATCH + "/fx", name="bb-%s.jsonl" % cid)
        got = []
        for s in sets:
            v, _ = mk.run_stop(path, active=active, hooks=HOOKSETS[s])
            got.append(v)
            if v != expect:
                diffs[s].append(cid)
        flag = "" if all(g == expect for g in got) else "   <-- DIFFERS"
        print("%-4s %-9s %s  | %s%s" % (cid, expect, "  ".join("%-10s" % g for g in got), why, flag))
    for s in sets:
        print("== %s: %d/%d as the rule states; differ: %s" % (s, len(CASES) - len(diffs[s]), len(CASES), " ".join(diffs[s]) or "-"))


if __name__ == "__main__":
    run_all(sys.argv[1:] or ["lib", "plugin015", "account014"])
