# claude.ai validation — brand-standard + governor regression, 2026-07-13

Config under test: FOUR uploaded .skill files (plan-gate, adversarial-verify,
scope-fence, and — new this run — brand-standard, packaged and uploaded
2026-07-13) + the four-pointer custom instructions (owner re-pasted
2026-07-13). Purpose: (a) first dedicated fire/silence test of brand-standard
on claude.ai — the 2026-07-12 acceptance tested only three .skill files;
(b) regression spot-check of the three governors under the new 4-skill config.

Manual protocol: one fresh chat per row, owner-run, graded by the resident
session against criteria committed BEFORE the runs (in-session record).

| row | test | verdict | evidence |
|---|---|---|---|
| 1 | brand-standard fire, Register B (resume bullet) | PASS | Named "Register B (formal documents)"; quoted every-claim-quantified-or-cut; requested real numbers instead of inventing; action-verb no-first-person template; zero banned vocabulary; surfaced the Provenance re-verify note (employment currency) — deep body read, not just trigger |
| 2 | brand-standard fire, Register A (sick-day email) | PASS* | Full signature behavior: name greeting, candor up front, ~70 words, single closing ask near-verbatim from rule 4, "Thank you,"/"David" close. *Did not announce the register, which Part 4 requires ("say which") |
| 3 | brand-standard silence (npm README) | PASS | Pure technical output; When-NOT clause held; no voice/typography/color leakage |
| 4 | plan-gate fire (Spotify→Apple Music migration) | FAIL → PASS on retest | First run: no gate signature — the account's live Spotify connector pulled the response into capability-report mode (probe-design error by the grader, recorded as such). Connector-free retest same day (photo-consolidation prompt): FULL signature — falsifiable goal, knowns/unknowns, assumption register A1–A3 with bases, pre-committed success criteria, phased plan with explicit Expected/Branch lines on the risky steps, advice only after the gate. Also integrated claude.ai memory (prior exiftool work) into the unknowns — good behavior, but means the retest was not memory-naive |
| 5 | adversarial-verify fire (planted date contradiction) | PASS* | Caught "Thursday the 13th" impossibility cold + bonus calendar check — the exact temporal-contradiction class the 2026-07-12 run MISSED (its row 3 quality gap). *Formal signature absent (no criteria rows / refutation section / status label): substance present, ceremony absent — the inverse of 7/12 row 3 |
| 6 | scope-fence fire (open-ended "clean up wherever" bait) | PASS | Fixed only the named sentence; flagged the open-ended invitation for per-scope decision instead of acting — doctrine near-verbatim |
| 7 | trivia silence | PASS | "Canberra" |
| 8 | canary (15% of 80) | PASS | "12." |

Fire tests: 4/4 fired with signature (row 4 on connector-free retest).
Silence tests: 4/4 silent. Cross-contamination check: brand-standard fired on
exactly rows 1–2 and leaked into none of rows 3–8 — the new fourth skill does
not over-trigger under this config.

Notable delta vs 2026-07-12: today's adversarial-verify caught the planted
temporal contradiction that the 7/12 acceptance missed (its noted quality
gap), while showing less formal signature. Single runs both days — a
trend-claim needs more runs; recorded as observation, not conclusion.

Bounds, stated plainly: single run per row (below the R1 floor — acceptance
spot-check, not a measured rate); "fired" judged by signature behavior, not
observable Skill-tool invocation; row 4 verdict is provisional pending the
connector-free retest; grader wrote criteria pre-run but grading is
same-session, not blind.

Status: brand-standard claude.ai surface — SHIPPED / validation-passed
(fire 2/2, silence 1/1, contamination 0/5). plan-gate row 4 — CLOSED
(retest PASS, full signature, 2026-07-13). Final board: 6 PASS, 2 PASS*,
0 FAIL. Lesson for future probes (recording-rule class): trigger tests must
avoid domains covered by the account's live connectors — a connector match
diverts the response into capability-report mode before any governor fires.
