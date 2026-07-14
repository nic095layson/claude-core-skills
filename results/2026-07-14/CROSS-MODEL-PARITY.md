# Cross-model parity run — Sonnet vs Opus on claude.ai

**Status: NOT YET RUN — owner-run required.** This is the results scaffold for the
prompt set in `evals/cross-model-parity.md` / `evals/cross-model-parity.json`. The
prompts were authored and design-checked 2026-07-14 in a Claude Code session, which
**cannot drive the claude.ai Sonnet/Opus UI** — so no behavior has been measured
here yet. Fill the tables below after running each prompt in a fresh claude.ai chat
on each model. Do not record a verdict from any source other than actual runs.

Config under test (confirm before running): custom instructions box == the paste
block in `instructions/claude-ai-custom-instructions.md`; four skills uploaded
(plan-gate, adversarial-verify, scope-fence, brand-standard); retired governors
(live-state-truth, lessons-ledger) absent from Capabilities.

- **Run date:** _____
- **Sonnet build (from claude.ai picker):** _____
- **Opus build (from claude.ai picker):** _____
- **Runner:** _____

## Per-row results

| row | targets | Sonnet outcome | Opus outcome | parity | notes |
|---|---|---|---|---|---|
| 1 | plan-gate (fire) | | | | |
| 2 | adversarial-verify (fire) | | | | |
| 3 | scope-fence (fire) | | | | |
| 4 | brand-standard (fire) | | | | |
| 5 | canary (silent) | | | | |
| 6 | near-miss rewrite (silent) | | | | |
| 7 | factual (silent) | | | | |
| 8 | pipeline (all four, in order) | | | | |
| 9 | standing principle (parity only) | | | | |

## No-regression coverage matrix

| uploaded skill | fired on Sonnet | fired on Opus |
|---|---|---|
| plan-gate | ☐ | ☐ |
| adversarial-verify | ☐ | ☐ |
| scope-fence | ☐ | ☐ |
| brand-standard | ☐ | ☐ |

**Retired governors leaked?** live-state-truth: ☐ none / ☐ LEAKED ·
lessons-ledger: ☐ none / ☐ LEAKED

## Verdicts (fill after running)

- **Parity (rows 1–9 all parity-PASS):** _____
- **No-regression (all skills ticked both models, nothing leaked):** _____
- **Ship — claude.ai cross-model:** _____

## Divergences and follow-ups

_Record any parity-FAIL row: which model diverged, the observed vs expected
signature, and the route taken (research-methodology reword / install fix /
stale-copy removal). Route per `evals/cross-model-parity.md` → "When a row fails."_

---

*Once filled and passing, cross-reference this file from
`governance-adoption-campaign` (claude.ai surface, currently OPEN) so the campaign
records cross-model parity as measured-with-date.*
