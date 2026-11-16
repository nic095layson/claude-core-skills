# Weekend operations report: the merge audit, the gate fixes, and the handover (2026-11-13 to 2026-11-16)

**Owner's request (2026-11-16):** "Provide a full report of the operations you conducted over the past weekend -
findings, fixes, and results in plain language please."

**Window:** records dated Friday 2026-11-13 to Monday 2026-11-16, 21:00 UTC. The work began with the audit on
Friday and finished with Monday's merge and handover, so the window covers the whole weekend plus both edges.

**What was analysed:**
- Library `nic095layson/claude-core-skills`: main at `da81dc2`, plus the open audit pull request #35 (head `320ac53`).
- Kit pull request #277 and deck pull request #142.
- The account's scheduled tasks.
- This session's own checks of 2026-11-16.

**Method:** every number below was read in this session from a committed file, GitHub, or a tool result. The
source is named beside it. The old session's transcript was not re-read; where only it holds a fact, the report
says so.

---

## Headline

**The safety checks that guard your repositories were broken in ways that could let a merge through without your
say-so. They were audited, rebuilt, checked twice by outside reviewers, and merged on Monday. The new version now
runs in new cloud sessions.** About half of what the audit found is fixed or decided. The rest (61 of 128) waits
for a second pull request, which starts after 2026-11-20 14:00 UTC with a plan and a cost shown to you first.
**One loss to know about:** the detailed records of 80 of the 128 findings were never saved to the repository. They
lived only in the old session, which was archived today.

---

## 1. What the "gates" are (one paragraph)

Your repositories carry small programs ("hooks") that watch what Claude does and can stop it. Three matter here:

| Gate | Its job in one line |
|---|---|
| **Merge gate** | No pull request is merged, and nothing is pushed straight to main, without your word. |
| **Stop gate** | A turn that pushes, opens a PR or schedules something must have loaded plan-gate and adversarial-verify. |
| **Receipt gate** | "I couldn't verify X" must say what was tried and how it failed. |

---

## 2. Findings: what the audit discovered (Friday into Saturday)

On 2026-11-12, pull request #34 (the QA loop) was merged. The next day you ordered an outside audit of that merge
and of the gates. Fresh agents that had not built the code attacked it; a second agent re-ran each finding.

| Area | What the audit found (EVIDENCE: PR #35 description) |
|---|---|
| Merge gate | **Failed its purpose.** Eight reproduced defects could let a merge through, **even after you refused**: "Don't merge yet" with a curly apostrophe, a status question like "Is #34 merged yet?", or any tool output containing the words "questions have been answered". |
| Turn boundary (which messages count as yours) | Failed in ordinary use. When the record held no message from you, every gate switched off. |
| Stop gate | Worked on the plain case; bypassed several ways (e.g. `git -c … push` was not seen). |
| Weekly QA task | Not safe as stored. It was **paused 2026-11-13**, and is still off. |
| The gates' own tests | Did not pin the rules: at least 18 single changes to the code passed every test. |
| Statements made to you about the 11-12 merge | 81 checked: 50 held, **21 were wrong**, 10 were not checked. |

Final size: **128 findings in 16 areas of 8 each** (EVIDENCE: counted from `original-findings-status.md` on main,
128 rows).

**You decided three rules for the merge gate on 2026-11-13 (D1 to D3), and a fourth on 2026-11-16 (D4):**

| Rule | In plain words |
|---|---|
| D1 | Only a click on a card that names the PR number, or a typed order with the number, authorizes a merge. A bare "yes" does not. |
| D2 | That word covers only the PRs named, and expires when Claude stops. |
| D3 | Auto-merge and pushing straight to main need the same word. A scheduled run can never do them. |
| D4 | A typed order counts only if it is plain and comes last in the message. Anything wordier gets a card instead. |

## 3. Fixes: what was built (Saturday to Monday)

Pull request #36, "Gate fixes after the merge audit", **merged into main as `da81dc2` on 2026-11-16 at 20:01 UTC.**

| Step | When (commit) | What it did |
|---|---|---|
| Wrote the predictions before any code | 11-14 `7df03f2`, 11-15 `48c7bfc` | What each fix must make true, fixed in advance |
| Rebuilt the merge gate and Stop gate | 11-15 `c224c94` | They now read what actually ran, not words that appear in text, and they know whose message is whose |
| Rebuilt the receipt gate | 11-16 `9708c5d` | Judges the same turn as the other gates; reads each claim and its receipt sentence by sentence |
| Made the wiring survive a missing file | 11-16 `10461ae` | Before: one missing script denied **every** Bash, Edit and Write call. Now only merges are denied. Also: plugin 0.1.6 and an install runbook |
| First outside read: 29 findings | 11-16 `077c860` … `ed8ef13` | Fixed what was confirmed |
| Your D4 decision ("plain orders only") | 11-16 `94f503a` | Lists of words had leaked both ways in both rounds. Grants now pass only through a short allowlist; a miss costs you one extra card, never a wrong merge |
| Second outside read: 25 findings | 11-16 `008f04c`, `5061d5f` | Three of them were holes that the first round's fixes had opened |

**Your answers that set the gates' behaviour** (EVIDENCE: `hooks/README.md`, "The owner's answers, one constant each"):
- A scheduled notification ends a merge word; you are asked again.
- A push to main needs an order that names the branch.
- After a block, the gate blocks at most twice.
- Loads made before a compaction don't count after it.
- A clicked card label is not treated as a typed prompt.

On 2026-11-16 you also kept 11 defaults that had been chosen without asking you (listed in the handoff).

## 4. Results: where everything stands

### The 128 findings (EVIDENCE: `results/2026-11-16/fix-audit/original-findings-status.md`, tallied by script today)

| State | Count | Meaning |
|---|---|---|
| Fixed and re-run by an outside auditor | 48 | Proven fixed by someone who didn't build it |
| Fixed, but checked only by the builder | 10 | Probably fixed; not independently confirmed |
| Changed by your decision | 5 | The rule itself changed (D2, Q5, …) |
| Ready once plugin 0.1.6 was served | 3 | Now served (section 5) |
| A stated limit | 1 | Known miss, written down |
| **Left for the second pull request** | **61** | Prompt classifier and reminders; the registry of hand-set values; advisory hooks; outcome scripts; documents; the weekly task's prompt |

### The two outside reads of the fix (EVIDENCE: `results/2026-11-16/fix-audit/README.md`)

| Round | Findings | Confirmed by a second agent | Severity (high · medium · low) |
|---|---|---|---|
| 1 | 29 | 22 | 5 · 10 · 14 |
| 2 | 25 | 22 | 2 · 12 · 11 |
| Builder's own | 2 | – | – |

All 56 have a state. 34 are fixed outright; the rest are partly fixed, decided, documented or stated as limits.
None is open without a state.

**Pre-registered predictions** (EVIDENCE: `first-preregistration-outcomes.md`): of 16, **2 met, 4 missed, 3 could not
be measured, 7 deferred** to the second PR. The misses are written down, not hidden.

**Not read by any outside auditor (your choice, 2026-11-16, to limit cost):** the wiring, the plugin package, the
install runbook, the registry and the guard. Only the builder's evidence covers them.

## 5. Monday: the plugin, the sync PRs and the handover (this session, checked today)

| Item | Result | Evidence |
|---|---|---|
| Plugin core-governance 0.1.6 | **Running in new cloud sessions** | Container started 20:42 UTC: version 0.1.6; wiring selftest 6/6; the 4 gate scripts match main byte for byte; the hooks fired on their own |
| Why two earlier checks saw nothing | The account updated the plugin at 20:35 UTC, after those checks ran (20:27–20:33) | The account's plugin list in the container. Timing is INFERENCE |
| Kit #277, deck #142 (bring the new gates to those repositories) | At 20:45 UTC: open drafts, no conflicts, no reviews, no CI. **Kit #277 was then merged at 20:53 UTC**; deck #142 is still open | GitHub, 20:45 UTC; merge event 20:53 UTC |
| Their "Read before merging" warnings | **3 of the warnings are out of date.** The afternoon runner, the morning runner and the season-end task already load both governors, so the new gates let them through | Stored task prompts read via list_triggers today |
| Reminder for the second PR | Moved to this session, fires 2026-11-20 14:05 UTC | `trig_01UMCuQq…` |
| PR watch on #277/#142 | This session | subscribe_pr_activity |
| Prompt for the Fantasy Basketball session | Written and sent to you | scratch file |
| Old Global Operations session | Archived on your click | archive_session |

## 6. What went wrong along the way (corrections owed)

The old session drafted 7 corrections-log rows, scheduled for the second PR. **The library's corrections log itself
is not on main:** its first 12 rows sit in the unmerged audit PR #35 (`git show origin/main:report/corrections-log.md`
fails today). In plain words:

| When | What was said | What was true |
|---|---|---|
| 11-13 | My audit "most likely" delayed a scheduled run | Possible, never shown |
| 11-14 | The audit would not drain your week | A second, model-specific weekly limit ran out; 6 hours blocked, two agents lost |
| 11-14 | The fix would go "at full pace" | Hit the 5-hour limit; account locked about 4 hours; agents lost again |
| 11-14 | Two size estimates | Both too small (the critic took 2.8M units, not 1.5M) |
| 11-15 | "23 cases" | 24 names, 30 rows |
| 11-14/15 | Whole fix about 55–65M units, 300–500 USD | 62.2M units and 336 USD spent with only 57 of 128 done (by 11-16 03:29 UTC) |
| 11-16 | PR 36 said "60 resolved, 65 left" | Records say 63 resolved, 61 left |

**And one from today (this session), owed as an 8th row:**

| When | What was said | What was true |
|---|---|---|
| 2026-11-16, about 20:50 UTC | Archiving the old session lost "nothing known" | Full records are saved only for the 48 findings in PR #35's areas. The other 80 findings exist on main only as id, title, area and state. Their reproductions most likely went with the archived container. I raised the risk but did not check before you clicked. |

**Cost** (EVIDENCE: the archived session's own record): the old session's meter showed **1,641.89 USD over its whole
life (2026-10-09 to 2026-11-16)**. The weekend's share cannot be separated from these records: did not check the
per-day breakdown.

## 7. Bounds

**Out of scope by design:**
- Fantasy decisions and the runners' daily output.
- PRs of other sessions (deck #143, kit #279).

**In scope and unverified:**
- **The 80 findings' detailed records** — `ATTEMPTED-FAILED`: searched main, PR #35's branch and every remote branch
  for their ids. Only the status table has them. The old transcript may still hold them (not re-read).
- Whether the archived container's scratch files can be recovered — did not check. The archive tool says
  unarchiving starts a fresh container.
- None for the guard: it ran today on main plus this report and printed `== RESULT: PASS ==` (about 21:00 UTC).
- The 7 drafted correction rows against the old transcript — did not check (that is a step in the second PR).

## 8. Decisions for you

| # | Decision | Options (recommended first) |
|---|---|---|
| 1 | **The 80 findings without records** | **(Recommended)** Have the second PR's first step rebuild them from the old session's transcript (still readable) before any fix. / Re-audit those areas fresh. / Fix from the titles alone (weakest). |
| 2 | Audit report PR #35 (open draft since 11-13; its description lists 48 findings, not 128) | **(Recommended)** Update it with the 128-row status and merge it, so the audit is on main. / Leave it open until the second PR. / Close it. |
| 3 | Deck #142 (kit #277 merged 20:53 UTC) | Merge it through the Fantasy Basketball session's card. |
| 4 | Second PR scope and cost | Shown to you after 2026-11-20 14:00 UTC; nothing starts before your pick. |
| 5 | Weekly QA task | Stays off unless you say otherwise. |

## Provenance

- Produced by the Global Operations session (`session_017XWgFJrJKXrM7XnXZ5uJjA`) on 2026-11-16.
- Sources:
  - `git log origin/main` (2026-11-12 onward);
  - `results/2026-11-16/fix-audit/{README,original-findings-status,findings-table,first-preregistration-outcomes}.md`;
  - `results/2026-11-16/surfaces-fix/{after-the-merge,other-repositories}.md`;
  - `experiments/hypothesis-2026-11-14-gate-fixes.md`, `hooks/README.md`;
  - PR #35 and the `claude/merge-audit-2026-11-13` branch;
  - list_triggers, list_sessions, the archive result;
  - this session's container checks.
- Re-verify the counts:
  `git show origin/main:results/2026-11-16/fix-audit/original-findings-status.md | grep -o '\*\*[A-Z ,]*\*\*' | sort | uniq -c`.
- A slip during this report: one command briefly switched the library checkout to a detached HEAD at the same commit
  (`da81dc2`). It was switched back at once and changed nothing.
