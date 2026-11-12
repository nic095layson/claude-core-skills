# System-wide QA audit: governors, hooks, Red Team, Council (2026-11-12)

**Owner's request.** "Audit system-wide operations and quality assurance measures (such as Council, Red team). Conduct integrity checks, and self-critical analysis … identify where you can implement recursive self-improvement … Provide detailed report on what can be improved and what you propose."

**What was analyzed (all read today, 2026-11-12).**
- The library `claude-core-skills` at main `bfedb3e`.
- The kit at main `1613629`.
- The deck's main branch.
- The installed plugin `core-governance` 0.1.4.
- The account-synced skill copies in this container.
- The incident ledger (28 entries).
- The kit's `report/corrections-log.md`.
- This session's transcript since 2026-10-29.

**Method.** Read-only commands. Nothing was changed. Skills loaded: plan-gate, council, red-team, after-report, adversarial-verify. Every table row below comes from a command run today, except the rows marked "not checked".

**Headline.** The machinery is installed and in sync on most surfaces. The weakness is that it measures process (did a skill load?) and never outcome (was the answer right?). The kit's own log shows the cost: 7 corrected statements in two days, and at least 5 of them were claims stated before the check was run. There are also 4 integrity gaps: a kit fix that was never upstreamed, a stale red-team registry, Council sitting outside the system, and independent-audit missing from your account.

## 1. Integrity checks

| Check | Result | Evidence |
|---|---|---|
| Library guard | PASS | `guard_essentials.sh` on main `bfedb3e` |
| Installed plugin vs library main | Identical, 0.1.4 | `diff -rq`; the only extras are the sync's own `.in_use` and meta files |
| Doctrine block: library, kit, deck | Identical | Checksum `494d07fd` on all three |
| Account skills vs library (the 9 that exist in both) | Text identical except one | Bodies and descriptions compared; frontmatter layout differs only |
| **red-team on your account** | **Stale** | Missing the paragraph that warns against a fingerprint that changes with every commit (6 body lines differ) |
| **independent-audit on your account** | **Missing** | Not in the synced skills folder. It loads only in sessions that have the library attached |
| **Kit hooks vs library** | **Kit is ahead** | Kit commit `b040962` (11-03) makes a scheduled run count as its own turn. The library, plugin and deck don't have it (0 matches for `scheduled_index`) |
| **Red-team registry for the hooks** | **Stale since 10-19** | 20 constants registered. 6 live hand-set values are unregistered: `TRIVIA_MAX_CHARS`, `CUE_MIN_WORDS`, `RECEIPT_WINDOW`, the negation window, the plan marker, the outward-action patterns. It also still lists two items that were fixed |
| Council | Outside the system | It exists only as an account skill. No repo copy, no eval set, no guard check, no mention in the instructions block or the doctrine block |
| Mac `~/.claude/CLAUDE.md` | Not checked | No tool here reads your Mac |
| Playwright in the runner's setup script | Not checked | Environment settings were not read |

## 2. What the quality record says

| Measure | Value | Source |
|---|---|---|
| This session since the turn gates shipped | 6 owner turns, 1 with outward actions; plan-gate and adversarial-verify both loaded in that one | Transcript, parsed today |
| Stop-hook governance blocks since 10-29 | 1 (11-02, a one-line confirmation) | Transcript |
| Kit corrections log, 11-11 to 11-12 | 7 wrong statements | `report/corrections-log.md` |
| How those 7 were caught | 2 through the owner (a screenshot; a run the owner asked for), 5 by the session's own later check | Same file |
| Pattern in those 7 | At least 5 were a lean or a count stated from memory before the run | Same file, "check that prevents it" column |

Six turns are too few to say whether the turn gates changed behaviour. The single block was on a turn I had judged trivial. The gate was mechanically right and the cost was one extra check.

## 3. Self-critical analysis

1. **The system measures loading, not correctness.** Every gate asks "did plan-gate load?" No number tracks how often you were told something false. The kit's corrections log is the first outcome metric in the system. It lives in one repo, and the library does not know it exists.
2. **The dominant error is not gated.** "State it, then run it" is the most common failure, in the kit this week and across the 21 failures audited on 10-21. The claim lint that targets it is advisory, with measured precision of 0.43.
3. **Fixes flow one way.** The kit improved a library hook on 11-03 and nothing carried the change back. This is the same drift shape as incidents INC-11 and INC-2026-10-19-02.
4. **Red Team is a one-off for the governance stack.** The skill's own rule says a record on a changed engine is stale. The hooks have changed repeatedly since 10-19, with no re-run.
5. **Council is unmeasured and unanchored.** Its verdicts are single-context role-play: one model, one context, five hats. Nothing checks that the vote is not theatre. Independent-audit exists because self-review fails, and the same critique applies to Council.
6. **Wording keeps growing; nothing is ever retired.** The instructions block went from 5,295 to 9,096 characters. Most additions are marked UNMEASURED. Two governors were retired on evidence in July; no retirement review has run since.
7. **My own record in this session:** 9 rule misses found on 10-28. I also wrote the "obvious defaults" exemption that later licensed the skipped decision cards.

## 4. Council verdict on the main proposal

🏛️ **Council convened** — Verdict: 4–1 for "a small standing loop driven by an outcome metric, paired with a pruning review".

- **Contrarian vs Executor:** more governance means more ceremony, and governance work already dominates this session. Executor prevailed because the loop proposed is one scheduled read-only run, and it comes with a rule that every addition retires something.
- **First Principles vs Expansionist:** the real defect is unverified claims, so measure those directly (the corrections log) and do not add gates. Both agreed, and this became the core of the proposal.
- **Outsider:** nine thousand characters of rules is itself a risk. That is where the pruning half comes from.
- **Dissent (Contrarian):** would flip to "for" if the first month shows that the loop's proposals get merged and the corrections rate falls.

## 5. Proposals, tiered

| Tier | Proposal | What it fixes | Evidence that would demote it |
|---|---|---|---|
| **MUST** | P1. Upstream the kit's scheduled-turn fix to the library, plugin (0.1.5) and deck | The integrity gap. The runner fix currently protects only the kit | The owner prefers the kit to stay forked |
| **MUST** | P2. Sync your account: upload independent-audit and the current red-team | A skill you rely on is absent outside library sessions | You only ever audit from library sessions |
| **HIGH** | P3. Corrections log in every project, as a library convention, with one outcome metric: wrong statements per week, split by who caught them | Gives the system a correctness measure. This is what makes self-improvement possible | The rate is already near zero in other projects |
| **HIGH** | P4. A weekly self-improvement run: a scheduled, read-only session runs independent-audit over the week's corrections logs and ledger, re-runs the hook registry check, and opens **one draft PR of proposals**. It never merges | The recursive loop: outcomes → findings → proposed rule or hook changes → your decision | Proposals go unmerged for a month |
| **HIGH** | P5. Re-run Red Team on the hooks and make the registry check part of the guard | The stale registry, 6 unregistered constants | — |
| **NICE** | P6. Bring Council into the library: a repo copy, a trigger eval, and a rule that a Council verdict on a decision you'll rely on gets one independent-auditor read | Council is unmeasured | You use Council only casually |
| **NICE** | P7. A pruning review each quarter: any rule still UNMEASURED after 60 days is measured or cut | Rule growth | — |
| **NOT NEEDED** | A blocking gate on "(Recommended)" lists or on unreceipted claims | You already chose advisory. Lint precision of 0.43 is too low to block | Precision measured above 0.8 on new reports |

**How P4 stays safe.**
- It proposes and never merges.
- The auditor is a fresh context that did not write the work.
- Every proposal must cite a corrections-log row or a ledger entry.
- It carries its own stop rule: if 3 runs in a row produce nothing you merge, it stops.

## 6. Bounds

**Out of scope by design.** Fantasy-engine correctness. Other sessions' transcripts. claude.ai chat behaviour beyond the instructions block.

**In scope and unverified.**
- The Mac file and the Playwright setup line (did not check).
- Whether the decision-cards reminder changes behaviour (NOT-ATTEMPTED: needs a two-turn live run).
- Whether the turn gates reduced misses (6 turns observed; too few to tell).
- Whether sessions in repos without the doctrine, such as Solo-Leveling-System, are covered by the plugin alone (did not check that repo).

## 7. Provenance

Session "Claude Global Operations", 2026-11-12, session model B. Nothing was committed or pushed.

Re-verify:
- `bash .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`
- `grep -c scheduled_index hooks/turngate.py`
- `ls ~/.claude/skills/synced/*/ | grep independent-audit`
