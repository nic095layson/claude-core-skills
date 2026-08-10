# Instruction-and-skill review — proposed edits after a month of operation (2026-08-10)

Owner request (near verbatim): "In my last Fable task, and how we've been
working together this past month. Do you propose any edits to my Claude
instructions or skills to have everything operating pristinely?"

**Analyzed:** this repo at `aa3474d` (the last Fable task's merge, 2026-08-03,
Sol-skill analysis + proposals + four authored skills + first trigger
measurements) and the full 2026-07-11 → 2026-08-10 record (`results/`,
`experiments/`, `.claude/LESSONS.md` INC-1…INC-8, `evals/`); plus live checks
run this session (a Fable 5 cloud session, 2026-08-10): full library lint,
description-length measurement, the account-synced skill roster, and the
Decision-7 pointer state. architecture-contract was loaded before proposing
anything; this report follows the after-report contract and was
adversarially self-checked before delivery (every load-bearing claim re-run
or re-read this session).

**Headline:** nothing is broken — the live checks pass across the board — so
the proposals are few and mostly small. Two safe mechanical edits (README
status refresh, the INC-3 lint length check that was suggested a month ago
and never added), one gated wording cleanup (the Decision-7 pointer in
adversarial-verify's description), and then the real list, which is not
edits at all but pending measurements and owner decisions — the biggest
being the hook-enforcement A/B, pre-registered 2026-08-03 and still not run,
which is the library's own named lever past its two measured trigger
ceilings. One larger observation: the month's evidence is almost entirely
the library measuring itself; the highest-value next data is live use of the
daily lanes it was built to govern.

## What checks out — verified live this session, no edit needed

| # | Check | Result (2026-08-10) |
|---|---|---|
| 1 | Library lint (`diagnostics-and-tooling/scripts/lint_skill.sh`, all 18 skills) | **18/18 PASS** (command output in session transcript) — EVIDENCE |
| 2 | Description lengths vs the 1024-char limit (INC-3 class) | All ≤1024; max is plan-gate at **1003** — EVIDENCE |
| 3 | claude.ai instructions ↔ live roster | All six steered skills (plan-gate, adversarial-verify, scope-fence, brand-standard, application-tailor, after-report) present in the account-synced roster of this cloud session (`/root/.claude/skills/`, 16 skills + manifest) — EVIDENCE |
| 4 | Unpromoted candidates correctly not installed | `correspondence` and `delegation-discipline` are repo-only — matching their register status (rows 8, 11), not a drift — EVIDENCE |
| 5 | Fable-transition audit correctly parked | Fable 5 is still serving this account (this session runs on it, 2026-08-10); the runbook's trigger condition has not occurred — EVIDENCE |
| 6 | Over-fire discipline | Zero should-not over-fires in every 2026-08-03 measurement (16/16 silent) — the trust-eroding failure mode has not appeared — EVIDENCE (from `results/2026-08-03/trigger-evals/`) |

## Proposed edits, tiered

Tiers: **DO NOW** (safe mechanical/factual, no gated wording) ·
**GATED EXPERIMENT** (goes through research-methodology) ·
**OWNER ACTION** (primary-machine or settings-box work only David can do) ·
**OWNER DECISION** (a call, not a task). Nothing below was executed — this
report proposes only, per the 2026-08-03 precedent.

### DO NOW

**E1 — Refresh the README "Status" section (factual drift).** It is dated
"as of 2026-07-11", says "All 13 skills lint" (there are 18 — measured
today), and says "Trigger reliability and behavioral effect are
**unmeasured**" — false since the 2026-07-11 campaign (governors) and
2026-08-03 (candidates). Precedent for doing this ungated: commit `d413a07`
("skill-count accuracy fix"). Demotion condition: none — this is factual
accuracy, not doctrine. — claim EVIDENCE (README read + lint run today)

**E2 — Add the description-length check to `lint_skill.sh`.** Suggested in
INC-3 (2026-07-11: "Lint gained no length check yet (still suggested)"),
still absent (grepped the script today: no length/1024 check). A ~5-line
check — FAIL >1024, WARN >1000 — closes the recorded loose end and would
have caught INC-3 automatically. plan-gate sits at 1003, 21 chars from the
cliff; the warning band is not hypothetical. — EVIDENCE

### GATED EXPERIMENT

**E3 — Decision-7 pointer cleanup, now precisely scoped.** Measured today:
at the *description* level only **adversarial-verify** still routes to a
retired skill ("live-state-truth" in its NOT clause); plan-gate and
scope-fence descriptions are clean. Bodies still reference the retired pair
(plan-gate L74/L152–153, adversarial-verify L17/L79/L87/L132/L136,
scope-fence L82/L118). Body edits don't gate (bodies don't trigger); the
description edit goes through research-methodology with
`evals/adversarial-verify.json` as the instrument. Upside beyond hygiene:
removal shortens a 972-char description, and INC-3's bonus finding was that
shorter descriptions fire *more* reliably. Low urgency — a pointer to an
absent skill is a no-op (Decision 7 says so) — but it is the one cleanup the
contract itself flags as owed. — EVIDENCE (grep output today)

### OWNER ACTION

**E4 — Run the hook-enforcement A/B (the single highest-leverage pending
item).** `experiments/hypothesis-2026-08-03-hook-enforcement.md` is
REGISTERED, NOT RUN. The two hooks exist and pipe-test clean, but their
behavioral effect on the DEAD-1/DEAD-2 ceilings — which the ledger twice
recorded as immune to wording — is unmeasured, and the library has no other
lever there. Needs the primary machine (settings wiring + live-fire). Until
this runs, plan-gate's straight-to-edit blind spot and the ledger's ~80%
ceiling are known-open, not being worked. — EVIDENCE (experiment file status
line, hooks/README.md)

**E5 — One-minute drift check on the instructions box.** The canonical file's
own re-verify step ("copy out, diff") has no dated execution since the
2026-08-03 adoption confirmation. Cannot be done from any Claude session —
only David can see the settings box. — EVIDENCE (provenance section,
`instructions/claude-ai-custom-instructions.md`)

**E6 — Disconnect one of the two GitHub MCP servers.** This cloud session
carries two identically-instructed GitHub servers ("GH" and "github", ~40
tools duplicated; observed in this session's tool listing, 2026-08-10). Pure
config hygiene; every cloud session pays the duplication. — EVIDENCE

### OWNER DECISION

**E7 — correspondence: confirm the lane or park it explicitly.** Trigger
measured PASS at its committed gate (5/6 · 4/4, 2026-08-03) but the *need*
is still owner-unconfirmed (register row 11) and the skill is installed
nowhere outside this repo. Two clean states: confirm email-drafting is a
real lane → promote (package per install-and-surfaces Runbook 2, upload,
and only then consider an instructions pointer 7), or record "parked,
need-unconfirmed" and stop carrying it as an open question. — EVIDENCE
(register row 11; roster check today)

**E8 — delegation-discipline: decide the promotion path.** Multi-agent work
happens outside this repo (the 2026-07-13 analysis ran 62 agents; ordinary
sessions use Agent/Workflow), but the skill is repo-only, so exactly the
sessions it was written for run without it. Prerequisites before any
promotion: the behavioral phase-2 (does the brief contract actually appear)
and the INC-8 residual (possible DEAD-1-class ceiling — a model told to
delegate just delegates). Then Decision-5 cost math. — EVIDENCE (register
row 8; INC-8)

**E9 — Standing backlog, surfaced not re-proposed.** (a) Fold candidates 1–4
from 2026-07-13 (writing-skills→skill-authoring, avoid-ai-writing→
brand-standard, systematic-debugging's 3-strike counter, fable-method's
forced-artifact lesson) — still pending, no folding commit exists since.
(b) claude.ai live-fire for after-report and application-tailor — the
untested cell in register rows 9–10 (the 2026-07-12 acceptance pattern is
the template). — EVIDENCE (git log; register)

## The month, in one observation — INFERENCE, marked as such

The record from 2026-07-11 to today is overwhelmingly the library measuring
itself: eleven of the ledger's twelve entries (`grep -c '^### '` = 12,
today) are eval-campaign methodology traps — INC-1's environment-boundary
lesson is the lone exception — and every `results/` directory is
library-on-library work. The stated daily
lanes — documents, career, email (2026-07-13 work-mix finding) — have almost
no live-use records: no real application-tailor run on an actual posting, no
after-report on a non-library topic, no confirmed correspondence lane. The
instruments are built and measured; what is missing is field data. The
next month's most valuable "edit" is not to the skills — it is to run the
lanes and let live use generate the register's next rows. (This is
inference from absence of records; live use may have happened in sessions
this repo cannot see — see Bounds.)

## Bounds, stated plainly

Single session, cloud surface only. Not visible from here: the claude.ai
settings box (E5 exists because of this), the primary machine's `~/.claude`
(hook wiring state there unverified; hooks/README's 2026-07-12 live
verification is the last dated fact), chat history from other sessions
("the month" means what the repo records), and claude.ai triggering
behavior. No behavioral grading was run this session — trigger and
behavioral rates quoted are the dated 2026-07-11/2026-08-03 measurements,
not re-measured today. The lint and length checks are point-in-time
(2026-08-10, repo at `aa3474d`).

## Decision sheet

| # | Item | Tier | Effort | Blocked on |
|---|---|---|---|---|
| E1 | README status refresh | DO NOW | minutes | nothing |
| E2 | Lint length check | DO NOW | minutes | nothing |
| E3 | Decision-7 pointer cleanup | GATED | one A/B session | research-methodology run |
| E4 | Hook-enforcement A/B | OWNER ACTION | one primary-machine session | David's machine |
| E5 | Instructions box diff | OWNER ACTION | one minute | David's eyes |
| E6 | Duplicate GitHub MCP server | OWNER ACTION | one minute | David's settings |
| E7 | correspondence lane call | OWNER DECISION | a decision | David |
| E8 | delegation-discipline path | OWNER DECISION | phase-2 first | behavioral measurement |
| E9 | Fold backlog + claude.ai live-fire | OWNER DECISION | standing | David's priority call |

Recommended order if all approved: E4 first (it is the named next lever and
the only unstarted measurement), E1+E2 in the same sitting (trivial), E5+E6
whenever, E3 at the next wording pass, E7–E9 as the lanes come up live.

## Provenance

Produced 2026-08-10 by a Fable 5 cloud session on branch
`claude/review-instructions-z0fhnb`, repo at `aa3474d`. Method: full read of
the month's artifacts (reports, ledger, register, experiments,
instructions), then live checks executed this session — 18-skill lint run,
per-skill description-length measurement, `/root/.claude/skills/` roster
enumeration, retired-pointer greps. architecture-contract and after-report
loaded per house law; adversarial self-check applied before delivery. No
skill, hook, config, or instruction text was modified — proposals only.

Re-verify: lint — `for d in .claude/skills/*/; do bash
.claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh "$d"; done`;
lengths — measure each frontmatter `description`; roster — `ls
~/.claude/skills/` in a fresh cloud session; E3 scope — `grep -n
'live-state-truth\|lessons-ledger' .claude/skills/*/SKILL.md`. Update when:
any E-item executes (link its commit/results here, dated) or a register row
it cites is superseded.
