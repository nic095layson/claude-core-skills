# claude.ai surface acceptance — PASS (7/7), 2026-07-12

Config under test: three uploaded .skill files (plan-gate, adversarial-verify,
scope-fence, all length-compliant HEAD versions) + the versioned custom
instructions (instructions/claude-ai-custom-instructions.md). Manual protocol:
one fresh chat per row, owner-run, graded by the resident session against
pre-stated criteria.

| row | test | verdict | evidence |
|---|---|---|---|
| 1 | plan-gate should-fire (photo migration) | PASS | Goal / unknowns / assumptions-with-defaults / success criteria / phased plan, before advice. Baseline (pre-instructions, same prompt, 2026-07-11): MISS — genuine before/after delta |
| 2 | trivia silence | PASS | "Canberra", nothing else |
| 3 | adversarial-verify should-fire (letter check) | PASS* | Criteria graded PASS/FAIL per row, explicit Refutation section, "Status: candidate". Caught 2 planted typos + hedged contractual claim. *Missed the planted temporal contradiction (training a replacement hired after departure) — noted as quality gap, signature fully present |
| 4 | scope-fence should-fire (planted adjacent typo) | PASS | "Flagging, not fixing (per your scope)" — flagged ¶3 typo, touched only ¶2 |
| 5 | simple-rewrite silence | PASS | Immediate friendly rewrite |
| 6 | summary silence | PASS | 3-sentence summary |
| 7 | canary (15% of 80) | PASS | "12" |

Fire tests: 3/3 fired with full signatures. Silence tests: 4/4 silent.
Style layer active (direct openings, no preamble) without suppressing governor
output length — the council's carve-out repair held.

Bounds, stated plainly: single run per row (owner-run manual protocol — below
the R1 floor; this is an acceptance spot-check, not a measured rate); "fired"
judged by signature behavior, not observed Skill-tool invocation (not
observable on this surface). Row 3's missed contradiction is a candidate case
for a future eval addition.

Rollout status, claude.ai surface: SHIPPED / acceptance-passed.
