# Coverage map — the 21 recorded failures (fantasy kit, 2026-10-19..21) against the safeguards

Basis: each row is a failure from the kit's own records (after-reports of 10/19–10/21, the run ledger, git
history; inventory assembled 2026-10-21 in this session). "Caught by" says what would have caught it before
the owner, and how that is known: **MEASURED** (the safeguard was run on the real incident this session),
**INFERRED** (reasoning about what the auditor brief would do — not run on this incident), **EXISTING**
(a gate built before today already covers it), **NONE**.

| # | failure (record) | caught by | basis |
|---|---|---|---|
| 1 | Deck showed 8 rostered players as free agents — exact-string join (season-deck-audit 10/19) | NONE — the page renders fine; only a person reading it sees the wrong names | — |
| 2 | "21.4 ± 0.4" quoted with no structural band (draft-postmortem 10/19) | EXISTING — red-team bands gate (10/19) | — |
| 3 | Scheduled run did nothing, no checkout (10/20 evening) | claim_receipts flagged the 10/19 promise "tomorrow at 6:52 … it updates itself" | MEASURED (M1 flag) |
| 4 | `add_repo` assumed to work unattended; classifier denies it | NONE — a runtime permission; preflight cannot pre-test it | — |
| 5 | "live verification supersedes it" (D-INT-1 c) | claim_receipts | MEASURED (test I1) |
| 6 | "the weekly in-season pull keeps it green" | claim_receipts | MEASURED (test I1) |
| 7 | "a mechanical pass that stamps today's ESPN verification" — the pass never existed | auditor (would find no such script); the lint misses this wording | INFERRED |
| 8 | "Still only yours: attach the FantasyBot connector" — already attached | claim_receipts | MEASURED (test I1) |
| 9 | check_claims detector blind to argparse-default writers | NONE new — its own known-answer control caught it | — |
| 10 | Roster join read `name`, field is `player` → 0 of 168 | NONE new — implausible result, self-caught | — |
| 11 | Tier classifier substring-matched whole notes | NONE new — self-caught | — |
| 12 | Report claimed adversarial-verify loaded; it was not | EXISTING — governance Stop hook | — |
| 13 | Invalid comparison (tier-only ÷ tier-plus-games ratio) | auditor (re-derives the cited figure) | INFERRED |
| 14 | Wrong counts "27 / 5 / 5" (true 22 / 2 / 4) | auditor (re-counts) | INFERRED |
| 15 | "the board applies both the tier and avail(gp)" — no board does | auditor (reads the code) | INFERRED |
| 16 | "changes nothing either way" — moved title share 21.1 → 23.3 | claim_receipts | MEASURED (test I1) |
| 17 | Attack records STALE after the engine changed | EXISTING — run_attacks gate | — |
| 18 | Board test read live data; would go red on merge | EXISTING — the kit's test suite caught it | — |
| 19 | Deck crashed with no matchup pull | replay_gate (code before #152 FAILs on the real 10/21 morning) | MEASURED (I3) |
| 20 | "Run now" path pushed nothing | preflight's remote check + the proposed prompt guard line | INFERRED |
| 21 | Deck lost its tabs on the first real movers (`x.toFixed`) | replay_gate (code before #154 FAILs on the real 10/21 morning) | MEASURED (I3) |

**Totals (from the table):** new safeguards, MEASURED on the incident: 7 (rows 3, 5, 6, 8, 16, 19, 21).
New safeguards, INFERRED only: 5 (rows 7, 13, 14, 15, 20) — the auditor's planted-claim test (E1) is the
evidence for that class, not these incidents. EXISTING gates: 4 (2, 12, 17, 18). NONE: 5 (1, 4, 9, 10, 11).
