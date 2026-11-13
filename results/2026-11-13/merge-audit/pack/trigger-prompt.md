# The weekly scheduled task created on 2026-11-12 (read live from the scheduler, 2026-11-12)

- name: Weekly QA self-improvement review (proposes, never merges)
- schedule: CRON_TZ=America/Los_Angeles 43 6 * * 1  (Mondays 06:43 Pacific); next run 2026-11-16T14:43:00Z
- delivery: fires into ONE persistent, long-running cloud session (the library's "operations" session), not a fresh one.
  That session has three repositories checked out side by side under /home/user/ (claude-core-skills,
  fantasy-basketball-2026-27, yahoo-fantasy-basketball) and runs the governance hooks from the account plugin
  `core-governance` (version installed on the account today: 0.1.4; 0.1.5 was sent to the owner for upload).
- no connectors are stored on the task (mcp_connections: []); model: session default.
- A scheduled trigger reaches a persistent session as a notification that the session reads with its
  ReadNotifications tool (see pack/real-row-shapes.md and kit/after-report-2026-11-04-turn-gate-scheduled.md).

## Stored prompt (verbatim)

Weekly QA self-improvement review (owner David approved this on 2026-11-12: "Yes, Mondays 6:43 am PT"). This is an unattended run: nobody is there to click, so ask no questions; record open decisions in the report. You PROPOSE; you never merge anything and never change a hook, a rule or a skill on main.

Governors: load plan-gate with the Skill tool before step 1 (the numbered steps are the plan; state it in one compact table, do not re-plan) and adversarial-verify before step 6. The turn gates will block the run otherwise.

1. Sync. In /home/user/claude-core-skills, /home/user/fantasy-basketball-2026-27 and /home/user/yahoo-fantasy-basketball: `git fetch origin main` and check out main at origin/main (stash leftovers and name the stash; never commit them). If a directory is missing, say so and continue with what exists.

2. Stop rule first. List the library's pull requests whose title starts "Weekly QA review" (GitHub tools, repo nic095layson/claude-core-skills). If the three most recent ones are all closed without merge or still open and untouched by the owner, do not open a fourth: disable this scheduled task (update_trigger, enabled=false, find its id with list_triggers by name), tell David in one short message that the weekly review stopped itself because three runs in a row produced nothing he merged, and end.

3. Evidence pack (read-only): `bash .claude/skills/independent-audit/scripts/weekly_review.sh /home/user/claude-core-skills /home/user/fantasy-basketball-2026-27 /home/user/yahoo-fantasy-basketball` from the library. Also run the library guard (`bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`) and check that the hook files and the doctrine block are identical across the three repos (cmp / checksum). Keep every output.

4. Outside read. Load the independent-audit skill. Make a disposable copy of the library (`git worktree add <scratch> HEAD`) and spawn ONE fresh-context read-only agent with `auditor-brief.md` as its contract. Its artifact: the evidence pack, this week's new rows in each project's corrections log, and any ledger entries (.claude/LESSONS.md) dated in the last 7 days. Its question: which recorded errors of the week would a specific, small change to a rule, hook or check have prevented, and which existing rule on the stale list has no evidence it earns its place? It returns findings only. Treat its report as leads: re-run the 2 most load-bearing findings yourself.

5. Proposals. Write `results/<today>/weekly-review/REPORT.md` in the library (after-report shape, short): the week's corrections rate per project and who caught them, compared with the previous weekly report if one exists; registry and parity results; at most THREE proposals, each citing the corrections-log row or ledger entry it answers, each stating what it would retire or what test would show it worked; and the oldest three stale rules with a recommendation (measure or cut). No proposal without a cited record. If the week has no new corrections and nothing drifted, say so in five lines and propose nothing. Use neutral model labels, never a model identifier.

6. Open ONE draft pull request in the library on a new branch `claude/weekly-review-<today>` containing only that report folder, titled "Weekly QA review <today>", body = the report's headline and the proposals as a decision list, ending "Do not merge without David's word." Do not build any proposal. Do not open PRs in the kit or deck.

7. Message David in the house shape: one bold outcome line, one table (rate this week vs last, registry, parity, proposals), only the caveats that matter, and what he needs to decide. If nothing needs him, say that in two lines.
