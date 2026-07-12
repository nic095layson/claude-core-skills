# Hypothesis: the A/B-accepted / owner-adopted descriptions can be trimmed to ≤1000 chars without losing their measured rates

**Status:** PRE-REGISTERED, NOT YET RUN. Written before any trim run this session.
research-methodology governs. One variable per experiment = the frontmatter
description (body verified byte-identical to OLD for all five).

## Why

Platform spec (verified 2026-07-11) caps frontmatter `description` at **1024 chars**.
Claude Code headless does not enforce it today (the A/B winners fired fine at
1144–1322), but claude.ai upload likely does. Five descriptions exceed the cap or
its safety margin: plan-gate 1322, lessons-ledger NEW2 1256, adversarial-verify 1144,
live-state-truth 1156, scope-fence NEW1 1109.

## Method

For each, ONE trimmed candidate **≤1000 chars** (margin under the 1024 cap). Cut only
never-implicated prose (procedural summaries, abstract WHEN lists, motivational
sentences, routing parentheticals). **Preserved verbatim:** the surfaces the A/B
proved load-bearing (below) AND each NOT clause (should-not protection). Re-run the
full eval set, grep-verified live variant, `claude -p` `claude-opus-4-8[1m]`, clean
scratchpad — the same protocol as the A/B session.

Final trimmed sizes: plan-gate 1000, adversarial-verify 969, live-state-truth 984,
scope-fence 986, lessons-ledger 972.

## Part 1 — the three A/B winners (must KEEP their gate)

- **adversarial-verify** (1144→969). Load-bearing kept verbatim: the user-handoff
  surface (`"confirm it's correct" … "ready to ship?" … "sound right?": grade and
  try to refute their artifact`). Cut: product-type list detail, the
  "smooth work is where unexamined errors live" aside, `"should work"`.
  **Predict:** should-fire (id6/7/8) hold **6/6**; should-not (id4/5) hold **4/4**.
- **plan-gate** (1322→1000). Kept verbatim: concrete task surfaces
  (`"refactor / rewrite / migrate / convert Y to Z" (e.g. move auth to JWTs)`,
  `"stand up a pipeline or service" / "set up CI/CD"`) and the anti-"just write the
  script" migration clause. Cut: procedural summary, abstract WHEN list, "Misread
  requirements…", triage explanation. **Predict:** should-fire (id1/2/3) hold
  **9/9** (N=3); should-not (id4/5) hold **4/4**.
- **live-state-truth** (1156→984). Kept verbatim: the live-confirmation surface
  (`OR any request to confirm/verify something about the running environment right
  now …`) and the `is X set up? / whether a service is up / what version is
  installed` cues. Cut: check-list item ("the current page"), unimplicated
  state-list items, NOT-clause parentheticals. **Predict:** should-fire (id1/2/3)
  hold **9/9** (N=3); should-not (id4/5, concept qs) hold **6/6**.

**Acceptance (Part 1):** gate still passes (≥5/6, ≥8/9 at N=3) AND should-not-silent
holds; ANY regression blocks → revert to the over-length version, record the dead end
(do NOT ship an under-limit description that lost its gate).

## Part 2 — owner-approved adoption (gate stays FAIL; rate must HOLD)

Owner decided to adopt these as running descriptions ("better wording while hooks are
explored", NOT a rollout claim). Both exceed 1024, so trim-and-retest per Part 1 rules;
acceptance is **measured rate holds vs the over-length variant** (no regression), rates
recorded as rates.

- **scope-fence** = NEW1 (1109→986). Kept verbatim: same-bug-elsewhere surface and the
  scoped-fix-bundled-with-whole-file surface; NOT clause (named work inside the fence).
  Cut: "dead code, a stale doc", "and when work-in-progress starts wanting to grow",
  routing detail. **Predict (rate hold, same-condition OLD was 1/6):** id1 0/2
  (unfireable inline-code class), id2 2/2, id3 2/2 = **4/6**; should-not (id4/5) **4/4**.
- **lessons-ledger** = NEW2 (1256→972). Kept verbatim: APPEND-first directive + the
  qualitative hard-diagnosis markers; NOT clause (no routine successes). Cut: opening
  detail, one "Also APPEND" example, two CONSULT examples, the "Load it at the END…"
  sentence, a parenthetical. **Predict (rate hold, NEW2 was 12/15=80% at N=5):**
  should-fire ~4/5,3/5,5/5-class ≈ **~80%** (N=3 here); should-not (id4/5) **4/4**.

**Acceptance (Part 2):** measured rate holds (no should-fire regression vs the
over-length variant) AND should-not holds; ANY should-not regression blocks. Gate
status remains FAIL — record the rate.

## Fenced (do not redo)

- Do NOT trim past load-bearing surfaces to hit the char target — a shorter
  description that lost its gate/rate is a dead end, not a win.
- Only `Skill`-tool invocation counts as a fire (same parser as Phase 1 / the A/B).

---

## OUTCOME — 2026-07-11 (same session, same protocol)

**All five trims HOLD; none regressed; zero should-not regressions; zero co-fires
across 64 runs.** Every description is now ≤1024 chars. All landed to repo + personal
(byte-identical). Predictions were confirmed (scope-fence id1 over-performed the
prediction — see note).

| governor | over-length | trimmed | final chars | should-fire (trim) | should-not | result |
|---|---|---|---|---|---|---|
| adversarial-verify | 1144 | 969 | 969 | **6/6** (id6/7/8 2/2 each) | 4/4 | gate HOLDS → **ACCEPTED** |
| plan-gate | 1322 | 1000 | 1000 | **9/9** (id1/2/3 3/3) | 4/4 | gate HOLDS → **ACCEPTED** |
| live-state-truth | 1156 | 984 | 984 | **9/9** (id1/2/3 3/3) | 6/6 | gate HOLDS → **ACCEPTED** |
| scope-fence | 1109 | 986 | 986 | id1 **3/5**, id2 2/2, id3 2/2 | 4/4 | rate held/↑ → **ADOPTED** (gate stays FAIL) |
| lessons-ledger | 1256 | 972 | 972 | **8/9** (id1 2/3, id2 3/3, id3 3/3) | 4/4 | rate held → **ADOPTED** (gate stays FAIL) |

**Surprise, re-diagnosed (adversarial-verify §5): scope-fence id1 fired under the
trim** (3/5) where it was 0/2 throughout the A/B under the longer NEW1. Transcripts
confirm a genuine `scope-fence` load (skills_fired=['scope-fence']) before the model
noted the empty scratchpad — i.e. the shorter, less-diluted description matches the
"while you're in that file" cue more reliably. id1 remains flaky (3/5), so scope-fence
stays a FAIL/inconclusive on the gate per R3 — but the trim is strictly better than the
over-length NEW1 (id1 0/2→3/5, others held). Recorded as a rate, not rounded up.

**No reverts** (the revert-to-over-length rule did not fire for any governor). Part 1
winners kept their gates at the shorter length; Part 2 adoptions held their measured
rates. The 3 accepted governors' claude.ai `.skill` uploads remain STALE (owner
re-upload) — but are now within the 1024-char upload limit.
