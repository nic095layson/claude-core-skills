# Phase 1 Rewording — A/B Results (2026-07-11)

**Session:** research-methodology A/B rewording of the five governor descriptions,
run after Phase 1 (`RESULTS.md`) found all five FAILING the should-fire gate.
**Surface/model:** Claude Code **headless** (`claude -p`), personal-scope install
(`~/.claude/skills/`), fresh session per run, **`claude-opus-4-8[1m]`** (same model
as Phase 1, confirmed from each run's init event). One variant installed live at a
time; the live variant was grep-verified before every batch.

**Detection (unchanged from Phase 1):** FIRED := a `tool_use` with `name:"Skill"`,
`input.skill:"<governor>"` in the run's stream-json transcript. Cross-checked by an
independent re-parse of all raw transcripts (matches the run-time tally exactly).

**Scratchpad note:** this session runs each prompt in a **clean/empty** scratchpad
(Phase 1's had leftover probe files). For file-referencing prompts this changed
behavior, so OLD was **re-baselined in identical conditions** for every governor
except adversarial-verify (whose OLD was run fresh on new inline cases). All OLD-vs-NEW
comparisons below are therefore same-condition.

## Headline: OLD vs NEW should-fire rates (same-condition)

| governor | OLD should-fire | NEW should-fire | should-not-silent | gate ≥83% | verdict |
|---|---|---|---|---|---|
| **adversarial-verify** | 0/6 | **6/6 (100%)** NEW1 | 4/4 → 4/4 | ✅ PASS | **ACCEPTED** |
| **plan-gate** | 0/6 | **9/9 (100%)** NEW2 | 4/4 → 4/4 | ✅ PASS | **ACCEPTED** |
| **live-state-truth** | 6/9 (67%) | **9/9 (100%)** NEW1 | 6/6 → 6/6 | ✅ PASS | **ACCEPTED** |
| **scope-fence** | 1/6 | 4/6 (67%) NEW1 | 4/4 → 4/4 | ❌ FAIL | NOT ACCEPTED — reverted |
| **lessons-ledger** | 1/6 (17%) | 12/15 (80%) NEW2 | 4/4 → 4/4 | ❌ FAIL | DEAD END — reverted |

3 of 5 gates now PASS (were 0/5 after Phase 1). **Zero should-not regressions anywhere**
(no governor over-fired; the concept/trivia/named-work near-misses stayed silent under every
variant). Rates recorded as rates, dated — not rounded to "always fires".

## Per-governor detail (fires/runs, same-condition)

### adversarial-verify — ACCEPTED (NEW1)
Added the **user-handoff trigger surface** ("the user hands you something they made and asks
you to check it — confirm it's correct / double-check before prod / ready to ship? / sound
right?"). New inline-artifact cases id6/7/8 (append-only) test the H1 confound directly.

| variant | id6 | id7 | id8 | should-fire | id4 | id5 | should-not-silent |
|---|---|---|---|---|---|---|---|
| OLD | 0/2 | 0/2 | 0/2 | **0/6** | 2/2 | 2/2 | 4/4 |
| NEW1 | 2/2 | 2/2 | 2/2 | **6/6** | 2/2 | 2/2 | 4/4 |

**H1 (prompt confound) refuted:** OLD fired 0/6 even with the artifact inline — the base model
reviewed the code well but never loaded the skill. **H2 (description defect) confirmed & fixed.**

### plan-gate — ACCEPTED (NEW2, after NEW1 fell short)
NEW1 (abstract nouns → concrete task surfaces): 7/9 (id1 stayed a coin flip). NEW2 added an
anti-"just write the script" clause for data-migration tasks.

| variant | id1 | id2 | id3 | should-fire | should-not-silent |
|---|---|---|---|---|---|
| OLD | 0/2 | 0/2 | 0/2 | **0/6** | 4/4 |
| NEW1 | 1/3 | 3/3 | 3/3 | 7/9 (78%) — FAIL | 4/4 |
| NEW2 | 3/3 | 3/3 | 3/3 | **9/9 (100%)** | 4/4 |

### live-state-truth — ACCEPTED (NEW1)
Added the **live-confirmation surface** ("a request to confirm/verify something about the
running environment right now"). OLD same-condition exactly reproduced Phase 1 (6/9).

| variant | id1 | id2 | id3 | should-fire | id4 | id5 | should-not-silent |
|---|---|---|---|---|---|---|---|
| OLD | 0/3 | 3/3 | 3/3 | **6/9 (67%)** | 0/3 | 0/3 | 6/6 |
| NEW1 | 3/3 | 3/3 | 3/3 | **9/9 (100%)** | 0/3 | 0/3 | 6/6 |

### scope-fence — NOT ACCEPTED (reverted to OLD)
NEW1 fixed the two **abstract-description** should-fire prompts (id2 "make it better"
bundling, id3 "same bug elsewhere"): 0/2→2/2 each, no regression. But the governor stays at
**4/6** because the **id1-class ("restrain adjacent work while editing concrete code") is
unfireable in headless under any wording** — tested 4 framings, all 0/2 under BOTH OLD and
NEW1. When handed concrete code the model just codes; it never consults scope-fence. This is
a structural triggering ceiling, escalated (see below). Personal copy reverted to OLD.

| variant | id1 | id2 | id3 | should-fire | should-not-silent |
|---|---|---|---|---|---|
| OLD (same-cond) | 1/2 | 0/2 | 0/2 | **1/6** | 4/4 |
| NEW1 | 0/2 | 2/2 | 2/2 | **4/6** | 4/4 |

id1-class controls (all OLD & NEW1): id1 seeded 0/2 / 0/2; id6 inline-trivial 0/2 / 0/2;
id7 inline-named-work 0/2 / 0/2 (design error — named work is inside the fence, silence is
correct); id8 inline-dangled-nontrivial 0/2 / 0/2.

### lessons-ledger — DEAD END (2 honest rewords, reverted to OLD)
Both rewords lift triggering hugely (17%→80%) with no regression, but neither reaches ≥83%.

| variant | id1 | id2 | id3 | should-fire | should-not-silent |
|---|---|---|---|---|---|
| OLD (same-cond) | 0/2 | 0/2 | 1/2 | **1/6 (17%)** | 4/4 |
| NEW1 (markers) | 2/3 | 2/3 | 3/3 | 7/9 (78%) | 4/4 |
| NEW2 (lead w/ APPEND, N=5) | 4/5 | 3/5 | 5/5 | 12/15 (80%) | 4/4 |

**Failure mode:** residual run-to-run noise — the model often responds conversationally or
offers to log ("want me to jot a ledger entry?") without invoking the Skill tool. Escalated.

## Escalation — open architecture-contract question

Two governors (scope-fence's id1-class, lessons-ledger) plateau **below** the ≥83% gate after
honest wording work that produced large, regression-free gains elsewhere. The shared pattern:
**when the trigger depends on the model pausing mid-hands-on-work to consult a governance skill
(restraining itself while editing code; recording after a debug story), description wording has
a ceiling** — the model does the aligned behavior conversationally without a Skill-tool load.
This suggests **description-based triggering may have a ceiling for some behavior-governing
skills**, and mechanical enforcement (Claude Code hooks — architecture-contract weak-point 3)
may be the only lever past it. Owner decision pending; do not keep iterating the descriptions.

## Caveat — accepted descriptions now exceed the 1024-char limit (claude.ai risk)

The three accepted rewords lengthened their descriptions past the documented Agent-Skills
`description` limit (**1024 chars**): plan-gate **1322**, live-state-truth **1156**,
adversarial-verify **1144** (OLD were 965 / 863 / 827). **On the tested surface this is NOT a
problem** — all three demonstrably loaded and fired in Claude Code headless (6/6, 9/9, 9/9),
proving the full NEW text was in context and matched; the repo lint PASSes (it does not check
length). **But a strict validator on claude.ai may reject a >1024-char description at upload**,
which is the silent-non-registration class. This is flagged, not fixed: trimming now would ship
**untested** wording (violating research-methodology — ship the wording you measured). Owner
options before the claude.ai re-upload: (a) upload as-is and confirm it registers, or (b) trim
to ≤1024 and re-run the A/B to re-validate. Progressive-disclosure cost also rises (plan-gate is
now 232 words vs ~130 baseline).

**RESOLVED (2026-07-11, same day):** all five governors were trimmed to ≤1000 chars (969–1000),
preserving load-bearing surfaces + NOT clauses verbatim, and re-run — **all held their rates,
zero should-not regressions, zero co-fires**. Every description is now within the 1024 cap.
Notably scope-fence id1 fired 3/5 under the shorter description (0/2 under the over-length one) —
less dilution triggers more reliably. See `experiments/hypothesis-2026-07-11-length-compliance.md`.

## Disposition

- **Accepted (repo + personal updated, byte-identical):** adversarial-verify (NEW1),
  plan-gate (NEW2), live-state-truth (NEW1). **Their claude.ai `.skill` uploads are now STALE
  and need re-upload by the owner** (install-and-surfaces Runbook 2/3).
- **Reverted to OLD (not accepted):** scope-fence, lessons-ledger. Their NEW variants are
  documented in `experiments/` as owner-adoptable regression-free improvements.
- Eval sets extended (append-only, committed cases unchanged): `evals/adversarial-verify.json`
  (+id6/7/8), `evals/scope-fence.json` (+id6/7/8).
- Raw transcripts: `*__{OLD,NEW1,NEW2,...}__id*__r*.jsonl` in this directory.
