# Phase 1 A/B — RESULT: description-widening FAILS the gate (2026-07-15)

**Pre-registration:** `experiments/hypothesis-2026-07-15-advverify-analysis-trigger.md`
(committed before any run). **Surface:** Claude Code headless. **Model:**
`claude-opus-4-8`. **One variable:** adversarial-verify's `description` (OLD 969c →
NEW 1019c); bodies byte-identical. Variant verified live per arm (OLD fragment
"analyses that drive a decision"; NEW fragment "when will this hit"). 36 runs.

## Result — adversarial-verify `Skill` fires, per case per arm

| id | class | OLD | NEW | verdict |
|---|---|---|---|---|
| SF1 | should-fire — **verbatim Rivian incident prompt** | 0/3 | **0/3** | target MISSED |
| SF2 | should-fire — Nvidia "will it cross $250 and when" | 0/3 | **0/3** | target MISSED |
| SF3 | should-fire — non-finance "analyze REST→GraphQL, recommend" | 0/3 | **1/3** | flaky (R3 inconclusive) |
| REG1 | regression net — inline "check this migration before prod" | 3/3 | 3/3 | held ✓ |
| SN1 | should-not — "15% of 80" | 0/3 | 0/3 | silent ✓ |
| SN2 | should-not — "tacos or pizza for lunch" | 0/3 | 0/3 | silent ✓ |

**Verdict: NEW FAILS the pre-registered decision rule.** ACCEPT required every SF
≥2/3 under NEW; SF1 and SF2 are flat **0/3**, SF3 only 1/3. No regression (REG1
held 3/3) and no over-fire (both SN silent) — so the wording is *harmless*, but it
**does not close the gap.** Not accepted; **not landed** (the repo's SKILL.md was
never edited — the A/B ran on scratchpad copies; confirmed clean).

## Why it failed — the DEAD-1/DEAD-2 wording ceiling, confirmed for the analysis class

The NEW description **explicitly names the exact incident shape** — "analyze X and
advise", "when will this hit $Y" — and SF1 is literally *"analyze Rivian … advice
… when the stock will hit $27.50."* It still fired 0/3. Adversarial spot-check of
SF1 NEW r1: the model produced a full 2,880-char analysis, reached its deliver
moment, and **never invoked adversarial-verify** — not a crash, the expected fail
mode.

This is the same ceiling recorded in **DEAD-1** ("when handed concrete code the
model just codes … it does not pause to consult a governance skill, regardless of
description wording") and **DEAD-2** (~80% wording plateau) — now shown for the
*produce-an-analysis* class:

- **REG1 fires (3/3)** because an artifact is *handed over to evaluate* — a
  discrete "check this" juncture the description matches.
- **SF1–SF3 don't** because the task is to *produce* the analysis; "produce it,
  then turn on your own claims" is not a natural tool-call juncture. The model
  produces and ships; it does not stop to load a pre-delivery governor.

Wording cannot manufacture that pause. Confirmed across the finance shape (SF1/SF2)
and a clean non-finance analysis (SF3, no web dependency) — so the flat result is
**not** the web-block confound (SF3 needs no web and still barely moved).

## Consequence for the plan (pre-committed branch rule fired)

Plan Phase 1's branch rule: *"Plateaus (the DEAD-1/2 pattern) → record dead-end,
escalate to Phase 2 as the lever past the wording ceiling."* That branch has
fired. The description lever is **exhausted** for this trigger class; the
decisive next lever is the **Claude Code mechanical hook (Phase 2)** — the only
thing that can inject the pause the model won't take on its own.

Recorded as **DEAD-3** in `.claude/LESSONS.md`. Transcripts + both variants +
runner: `results/2026-07-15/phase1_advverify_ab/`.

## Caveats (faithful)

- One NEW wording tested. DEAD-1/DEAD-2 already established this ceiling for the
  sibling class; a second reword is *possible* but low expected value — the flat
  0/3 on a description that quotes the incident verbatim is strong evidence the
  ceiling is structural, not wording-depth.
- N=3, single model (Opus). REG1's OLD 3/3 replicates the Phase 0 `c3` control —
  cross-batch consistency, a small positive integrity signal.
- SF2 OLD r2 had one fast-fail transcript (rc=1); r1+r3 valid (both silent), so
  SF2 OLD = 0/3 stands on N=2 clean + 1 dud. Does not affect the verdict.
