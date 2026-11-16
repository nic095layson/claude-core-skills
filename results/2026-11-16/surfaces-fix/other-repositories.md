# The two other repositories: ready to sync, not synced

**Both are prepared and nothing is pushed.** The kit (`fantasy-basketball-2026-27`) and the deck
(`yahoo-fantasy-basketball`) carry their own copies of these hooks. Fresh clones at their default branches were
brought to this library's hooks with `bash hooks/sync-copies.sh <clone>`, and their settings to this library's
wiring. The owner opens and merges one pull request per repository; until then their sessions run the hooks of
2026-11-12.

## What the sync changes (the same in both)

| file | change |
|---|---|
| `hooks/govclass.py`, `governance-enforce.py`, `receipt-law-stop-gate.sh`, `selftest-receipt-law.sh`, `selftest-turn-gates.py`, `turn-gates-pretool.py`, `turngate.py` | updated to this library's (the rebuilt merge gate, Stop gate and receipt gate, and their table) |
| `hooks/receiptlaw.py`, `selftest-mutations.py`, `selftest_rows.py` | added (the receipt gate's module, the break list, the table's row builder) |
| `hooks/governance-trigger.py`, `plan-gate-first-write-reminder.sh`, `scope-fence-reminder.sh`, `selftest-governance-classify.py`, `selftest-reminders.sh`, `session-doctrine.sh` | unchanged (already equal) |
| `.claude/settings.json` | the `hooks` key becomes this library's wiring: every command runs its script only when the file is there; the merge tools get a group of their own whose missing script denies the merge; the turn-gate names of `CORE-SPEC.md` 3.3, anchored, replace the old matcher, which was not anchored and did not reach `Monitor`, the scheduling tools or auto-merge. Neither file held anything else under `hooks`, and nothing outside `hooks` changes. After the change each file equals this library's |

`sync-copies.sh` prints the settings change as a diff and never applies it. Here it was applied by hand, by
copying the proposal it wrote.

## The selftests, run inside each clone after the sync

| command | kit | deck |
|---|---|---|
| `python3 hooks/selftest-turn-gates.py` | 740 cases: 740 pass, 0 fail | 740 cases: 740 pass, 0 fail |
| `python3 hooks/selftest-mutations.py` | 352 breaks: 343 caught, 0 survived, 0 stale, 9 not run (their wiring file is not in this layout) | the same |
| `bash hooks/selftest-receipt-law.sh` | 15 passed, 0 failed | 15 passed, 0 failed |
| `python3 hooks/selftest-governance-classify.py` | 45 passed, 0 failed | 45 passed, 0 failed |
| `bash hooks/selftest-reminders.sh` | 8 passed, 0 failed | 8 passed, 0 failed |
| `python3 hooks/selftest-turn-gates.py --needs` | 16 files, none missing | 16 files, none missing |
| the repository's own checks that touch hooks | none found (`scripts/`, `gates.json`, the Markdown at the root and under `report/` were searched for the hook files' names) | none found |

The 9 breaks not run are those of the plugin's `hooks.json`, which neither repository has. Raw output:
`raw/kit-selftests.txt`, `raw/deck-selftests.txt`.

## What the unattended runs do under the new gates

Source of the command forms: the kit's saved copy of the morning runner's stored prompt
(`report/after-reports/flaim-2026-10-21/runner-prompt-current.txt`), its prompt diff of 2026-10-26 for the
afternoon runner, `report/plans/in-season-runbook-2026-10-19.md`, `DATA-PULL.md`,
`report/plans/season-end-calibration-prompt.md`, and the deck's `arena/results/SEPTEMBER-PLAN.md`. The stored
prompts themselves live on the account; the saved copies can be older than what fires. Each form was run through
the clone's own synced `turn-gates-pretool.py` on a record of a scheduled run: your earlier turn ending with a
real click that holds the word "merge" ("Audit today's merge (Recommended)"), a stop, the idle nudge, then the
notification read with the scheduled-trigger origin, then `plan-gate` loaded. The checkout is a made-up one on
the branch the prompt names. Both clones give the same verdicts. Raw output: `raw/kit-unattended-forms.txt`,
`raw/deck-unattended-forms.txt` (made by `tools/unattended_forms.py`).

| source | command form | pre-tool verdict |
|---|---|---|
| kit morning runner, step 1c | `git -C <deck> pull --ff-only` | allow |
| kit morning runner, step 2 | `git fetch origin` | allow |
| kit morning runner, step 2 | `git stash push -u -m "leftover before <date>"` | allow (advisory line) |
| kit morning runner, step 2 | `git checkout -B season/daily origin/season/daily && git merge --no-edit origin/main` (a local merge) | allow (advisory line) |
| kit morning runner, step 6 | `git add … && git commit -m "Morning run <date>: …"` | allow (advisory line) |
| kit morning runner, step 6 | `git push -u origin season/daily` | allow (advisory line) |
| kit morning runner, step 6 | `gh api repos/<kit>/pulls -X POST … -f head=season/daily -f base=main -F draft=true` | allow (advisory line) |
| kit morning runner, step 6, if the PR is opened with the GitHub tool | `create_pull_request` (draft, `season/daily` into `main`) | allow (advisory line) |
| kit afternoon runner, step 4 | `git add … && git commit -m "Afternoon check <date>: …" && git push -u origin season/daily` | allow (advisory line) |
| kit `DATA-PULL.md` section 6 | `git add -A && git commit … && git push` on `main` | **DENY (scheduled)** — owner |
| kit `DATA-PULL.md` section 6 | `git push origin main` | **DENY (scheduled)** — owner |
| kit season-end calibration task (fires 2027-03-22) | `git checkout -b <branch> && git commit … && git push -u origin <branch>` | allow (advisory line) |
| kit season-end calibration task | `create_pull_request` | allow (advisory line) |
| deck September and October Routines (fired 2026-09-01 and 2026-10-12; no later firing found in the repository) | `git checkout -b claude/2026-10-12-october-refresh && git commit -am … && git push -u origin …` | allow (advisory line) |
| deck Routines | `create_pull_request` (draft) | allow (advisory line) |
| control: a merge inside the morning run (its prompt says "Merge nothing") | `merge_pull_request` #165 | DENY (scheduled), as wanted |

"Advisory line" is the plan-shown reminder: one context line, never a denial. It appears when the record holds
no plan text since the plan-gate load; whether the runner's one-line statement of its plan counts as plan text
was not checked.

Stop gates on whole runs (outward-action rule of `governance-enforce.py`; the receipt gate allowed every run):

| run | governors loaded | Stop verdict |
|---|---|---|
| kit morning runner, as its saved prompt says (plan-gate before step 1, adversarial-verify before the report) | plan-gate, adversarial-verify | allow |
| kit afternoon runner, if its prompt carries the same governor line | plan-gate, adversarial-verify | allow |
| kit afternoon runner, if its prompt names no governor | none | **BLOCK (outward action without plan-gate and adversarial-verify)** — owner |
| kit season-end calibration task (plan-gate by `RULES.md`; its prompt names no adversarial-verify) | plan-gate | **BLOCK (without adversarial-verify)** — owner |
| kit `DATA-PULL.md` run (it names no governor) | none | **BLOCK** — owner |
| deck October Routine (`SEPTEMBER-PLAN.md` section 6 names no governor) | none | **BLOCK** — owner |

## Lines the owner must read before syncing

1. **`DATA-PULL.md` cannot finish unattended.** It tells a run to commit and push to `main`. In a scheduled run
   that push is always denied (your decision D3), and the Stop gate blocks a run that names no governor. If a
   scheduled task still runs this protocol, it must push to a branch and open a pull request instead, and its
   prompt must load plan-gate before the first commit and adversarial-verify before it ends. Whether any
   scheduled task still runs it was not checked (the tasks live on the account). The file describes the
   pre-draft pulls.
2. **The season-end calibration task (fires 2027-03-22) would be blocked once at its stop.** Its prompt asks for
   plan-gate through `RULES.md` and opens a pull request, but never names adversarial-verify. Add "load
   adversarial-verify before the report" to the stored prompt. Until then the run is blocked once, loads it, and
   goes on: the Stop gate blocks at most twice.
3. **The afternoon runner's governor line was not seen.** Only its save step is in the kit's files. If its stored
   prompt has no line like the morning one, every afternoon run is blocked once at its stop. Read the stored
   prompt, and add the morning prompt's "Governors:" line if it is missing.
4. The deck's two Routines have already fired, and no later firing is recorded in the repository. If they are
   reused, they need the same governor line.

What was not checked: the stored prompts as they are on the account today (only the saved copies in the kit),
a live run of either runner under the new hooks, and the row shape of a fresh-session firing (the saved morning
prompt says its session is a persistent one that receives the prompt every morning, which is the shape tested).
