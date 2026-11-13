# Brief: review the weekly unattended run

key: `rev-weekly-run` · finding ids: `WR-<n>` · scratch: `work/rev-weekly-run/` (private checkout: `work/rev-weekly-run/wt`)

**Objective.** Decide whether the weekly task, exactly as stored (`pack/trigger-prompt.md`), will do what the
owner was told it does when it fires with nobody watching. List every way it can silently do nothing, do the
wrong thing, or do more than it should.

**What the owner was told:** `pack/pr34-and-claims.md` (PR body row P4; chat claims 4, 9 and 10);
`lib/results/2026-11-12/qa-loop/AUDIT.md` section 5 ("How P4 stays safe");
`lib/experiments/hypothesis-2026-11-12-qa-loop.md` (row P4 and its outcome).

**Method.** This is a preflight review (`lib/.claude/skills/independent-audit/SKILL.md`, step 4 and rule 5:
"An unchecked run is a failed run").
1. **Assumptions.** Write down everything each of the seven steps assumes: directories, branches and their
   state, tools and connectors (the task stores none: see the header of `pack/trigger-prompt.md`), permissions,
   GitHub state, files that must exist, what "today" and "this week" mean, what a previous run left behind.
   For each: holds / does not hold / unknown, with evidence from the pack. `kit-full/` and `deck-full/` are the
   two projects at their main branches; your private checkout is the library.
2. **Run the evidence-pack script for real, on copies:**
   `bash PACK/work/rev-weekly-run/wt/.claude/skills/independent-audit/scripts/weekly_review.sh PACK/work/rev-weekly-run/wt PACK/kit-full PACK/deck-full`.
   Check its sections against the truth. Check its exit code when a part of it fails (make a part fail in a
   scratch copy). Check whether it leaves anything behind. Run it twice. Run it with a project path that does
   not exist.
3. **The gates during the run.** The session it fires into runs the governance hooks. Build the run as a
   transcript with `pack/tools/mk.py` (the notification row with `mk.notif`, then the tool calls the seven
   steps make, in order) and run each gate on it: once with the hooks installed today
   (`hooks=PACK/account/plugin/core-governance/scripts`) and once with the merged ones. Which steps are
   blocked, denied or left ungated? Does the prompt's own sentence about the gates ("The turn gates will
   block the run otherwise") hold? What do the gates do to the owner's next ordinary turn after a run?
4. **The stop rule (step 2).** Can a session decide it from the data it will have? Write three concrete
   pull-request histories and say what the rule does on each. What does "disable this scheduled task" do to a
   task that is bound to the session it is running in?
5. **The promises:** "proposes, never merges"; "at most THREE proposals"; "no proposal without a cited
   record"; "ONE draft pull request ... containing only that report folder". For each: what enforces it (a
   hook, a tool limit, or only the sentence)?
6. **Repetition.** What does the tenth run find that the first did not (leftover copies, branches, stashes,
   open pull requests, a transcript that keeps growing)?
7. **Platform fit.** The session's platform instructions (not in the repository) name one development branch
   per repository, say to push to no other branch without explicit permission, and say to open a draft pull
   request after every push. Does the stored prompt's step 6 fit that?

Never run the real task. Never call scheduling or GitHub tools.

**Out of scope:** whether the numbers in the evidence pack are computed correctly (another auditor reviews
the scripts).

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
