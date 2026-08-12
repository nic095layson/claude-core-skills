# Integrity audit — branch `claude/chat-error-verification-fix-flq49c` (2026-08-12)

Pre-merge validation of PR #14, run mechanically rather than by reading. Baseline
`9b389e2` (pre-patch `main`) → head `2e01ef6` + this commit.

**Verdict: MERGE-READY.** Three defects were found and fixed during the audit;
two pre-existing conditions are flagged and deliberately not fixed; one required
owner action is outstanding and is not fixable from inside the repo.

## Checks run

| # | Check | Result |
|---|---|---|
| A | Working tree clean; local == remote | PASS |
| B | Files touched confined to intended scope | PASS — 35 files, all in the patch's footprint |
| C | Files deleted or renamed | **0 / 0** |
| D | Every removed line accounted for | PASS — 13 removals, all replacement seams (below) |
| E | Frontmatter byte-identical to baseline, all 19 skills | PASS — trigger surface untouched |
| E2 | Description ≤ 1024 chars (INC-3 limit) | PASS — max 1000 (plan-gate, at the warn boundary as recorded) |
| F | Installed/synced copies vs repo | **DRIFT — 3 skills, expected, owner action** |
| G | Cross-references in When-NOT sections resolve | 2 dangling, **pre-existing** |
| H | Ledger numbering: no duplicates or collisions | PASS — INC-9, INC-10 appended cleanly |
| I | JSON parses (11 files); shell syntax (6 files); exec bits | PASS |
| J | `lint_skill.sh` on all 19 skills | **19 PASS, 0 FAIL, 0 warnings** |
| K | Documentation path references resolve | 1 dangling introduced → **fixed** |
| L | Paste-block markers intact; stated char count == measured | PASS — 3,972 == 3,972 |
| M | Transcript count stated == files on disk | **MISMATCH → fixed** |
| N | Every rate stated in RESULTS.md internally consistent | **MISMATCH → fixed** |
| O | Checksum manifest of all governed artifacts | recorded below |
| P | Hook pipe-test | **10/10 PASS, twice consecutively** |

## The three defects the audit found

All three were introduced by this branch. None was caught by reading.

1. **RESULTS.md claimed "21 transcripts"; 23 were on disk.** Two re-run
   transcripts were added after the sentence was written. A stated count
   disagreeing with the tree is invariant 7 and is the same defect class this
   whole PR exists to close. Fixed.
2. **RESULTS.md headline said "cued 2/2" while its own table said 4/4.** The
   table was updated after the re-run, the headline was not. A self-consistency
   failure of exactly the kind Step 4 is supposed to catch. Fixed.
3. **`INC2unattemptedverificationfix.md` was cited but not in the repo.** The
   owner's source document was referenced as provenance while living only in a
   session upload. Fixed by vendoring it beside this report — after-report §2
   ("raw supporting artifacts are committed beside the report, not summarized
   away"). The record is now self-contained.

*Method note:* the first link-checker run reported 25 dangling references. It was
wrong — it resolved every path against the repo root, ignoring that a reference
inside `.claude/skills/x/SKILL.md` resolves relative to that skill. Corrected, the
real count was 11, of which 10 are pre-existing prose references to generic
filenames (`settings.json`, `lint_skill.sh`, `check_release_parity.sh` — the last
explicitly recorded as deliberately absent) and 1 was defect 3 above. Reporting
25 findings would have been its own version of the defect under repair.

## Flagged, not fixed (pre-existing — scope-fence)

- **`photo-editing` names `dataviz` and `frontend-design`** in its When-NOT
  section; neither is a skill in this repo. Present at baseline, so pre-existing.
  Arguably not a defect at all — both exist at account scope — but the repo's
  boundary map cannot verify them. Left alone.
- **Two unnumbered `### INC` entries** in `.claude/LESSONS.md` (2026-07-11).
  Harmless; renumbering them would break the never-renumber rule.

## Every removed line on the branch (13)

```
## The pass — run all five, in order                          -> "...all six..."
Deliver only when: every committed criterion passes...        -> + PARTIAL / gap clause
attempt found nothing unaddressed, and no regression...       -> (same sentence, extended)
   full table; skipping refutation entirely is the only...    -> + Step 6 sizing clause
  self-check, not this protocol.                              -> + no-gap-audit clause
   as the false frame.                                        -> + SUPPORTED basis rule
## Status (as of 2026-08-10)                                  -> 2026-08-11
All 18 skills lint with zero FAILs...                         -> 19 (count was stale)
re-run 2026-08-10). The lint now also enforces...             -> (same para, rewritten)
state (my accounts, settings...), verify now or say you       -> receipt-law rewrite
can't — observed behavior beats documentation. When I...      -> (same para)
or you learn one during our work, offer to save it...         -> (same para)
relearned.                                                    -> (same para)
```

Zero rules deleted. Zero rules renumbered. Every removal is the first or last
line of an in-place replacement.

## Outstanding — owner action, not fixable in-repo

**The account-synced copies are stale.** `/root/.claude/skills/synced/` carries
pre-patch `adversarial-verify`, `plan-gate`, and `after-report`:

| skill | synced copy | repo | has Step 6 |
|---|---|---|---|
| adversarial-verify | `188d48e5a01adb33` | `5fa9701a503fb7c1` | synced: **no** · repo: yes |
| plan-gate | `7e0c29156c9a8f6d` | `05be98bfc38c2225` | — |
| after-report | `6213cf98662bb6e0` | `febdff85204ad0fc` | — |

`application-tailor`, `brand-standard` and `scope-fence` are IN SYNC, which
confirms the drift is exactly the three patched skills and not a pre-existing
condition. Merging the PR does **not** update these. Until they are re-packaged
and re-uploaded, claude.ai keeps running the old text — the same stale-copy trap
recorded in debugging-playbook §4. Combined with the instructions re-paste, that
is two manual steps standing between this merge and the surface where INC-9
happened.

## Checksum manifest (sha256, first 16)

```
5fa9701a503fb7c1  .claude/skills/adversarial-verify/SKILL.md
febdff85204ad0fc  .claude/skills/after-report/SKILL.md
05be98bfc38c2225  .claude/skills/plan-gate/SKILL.md
39ce63e07b84c470  .claude/skills/application-tailor/SKILL.md
bec3e61fa52d553f  .claude/skills/architecture-contract/SKILL.md
2195da175f86fd5d  .claude/skills/brand-standard/SKILL.md
c1b3386238613b2d  .claude/skills/correspondence/SKILL.md
28b149b683f184b8  .claude/skills/debugging-playbook/SKILL.md
f4d5d6e9cb768db7  .claude/skills/delegation-discipline/SKILL.md
3e84e1e18e5a8d5f  .claude/skills/diagnostics-and-tooling/SKILL.md
bb527deb006b093f  .claude/skills/domain-reference/SKILL.md
89d2de8afceb9cea  .claude/skills/governance-adoption-campaign/SKILL.md
24802c11b7cf30b3  .claude/skills/install-and-surfaces/SKILL.md
221a06d1663aadfb  .claude/skills/lessons-ledger/SKILL.md
96f7a67fee5670af  .claude/skills/live-state-truth/SKILL.md
bd91940c55c6fe06  .claude/skills/photo-editing/SKILL.md
bf9d76bc18d45818  .claude/skills/research-methodology/SKILL.md
53566c0c38771c2a  .claude/skills/scope-fence/SKILL.md
32eefcb589224772  .claude/skills/skill-authoring/SKILL.md
557c456d961701ec  hooks/ledger-recount-reminder.sh
c948c996107521d3  hooks/plan-gate-first-write-reminder.sh
64a21e812d708c45  hooks/receipt-law-stop-gate.sh
e182a54e4e239df9  hooks/scope-fence-reminder.sh
3b5060e8c952336b  hooks/selftest-receipt-law.sh
7d6f60103fa3c674  evals/gap-provenance.json
1341abe1eb5925ca  instructions/claude-ai-custom-instructions.md
25e331ace2e1ae5f  .claude/LESSONS.md
511e8c01f2ebf2bf  experiments/hypothesis-2026-08-11-gap-provenance.md
349253d10df065ca  results/2026-08-11/gap-provenance-guards/INC2unattemptedverificationfix.md
```

`RESULTS.md` and this file are excluded — both changed after the manifest was
taken, and a self-referential hash would be false precision.

## Bounds of this audit

**Out of scope by design:** behavioral quality of the patched text (that is
`RESULTS.md`); claude.ai-side state, which cannot be read from here; whether the
owner's settings box matches the paste block.

**In scope and unverified:** the hook's live-fire behavior — pipe-tested 10/10
and validated against the verbatim INC-9 text, but never run inside a real
session (`NOT-ATTEMPTED`, by choice: it is a proposal, not installed). Uncued
firing of the patched skills remains `NOT-ATTEMPTED` for the same reason given in
`RESULTS.md`.

---

## Final pre-merge validation (2026-08-12, post-upload)

Re-run in full after the owner uploaded the three skills and re-pasted the
instructions block. **Result: full PASS, merged.**

| Check | Result |
|---|---|
| Working tree clean · local == remote · 4 commits ahead | PASS |
| Fast-forwardable onto `main`; merge conflicts | PASS · **0** |
| `lint_skill.sh` × 19 skills | **19 PASS**, 0 warnings |
| Frontmatter byte-identical to pre-patch baseline × 19 | **19/19 identical** |
| Files deleted / renamed on branch | **0 / 0** |
| Eval JSON valid (11) · shell syntax (6) · exec bits | PASS |
| Hook pipe-test | **10/10 PASS** |
| All 24 patch mechanisms present in shipped text | **24/24** |
| Document self-consistency (counts, rates, char totals) | PASS |
| Ledger numbering duplicates | **0** |
| **Install drift: synced == repo, all three skills** | **CLOSED** |
| **Three-way match: package == repo == synced** | **3/3 YES** |

**The drift is verified closed, live.** `/root/.claude/skills/synced/` re-synced
during this check (directory mtime within seconds of the read) and all three
patched skills now hash-match the repo — so the account-level copies carry Step 6,
the receipt law, and the corrected rule 7. `application-tailor`, `brand-standard`
and `scope-fence` remain untouched throughout, which is the control that makes
the three-way match meaningful rather than coincidental.

*Method correction, recorded because it would have produced two false failures:*
the mechanism sweep initially reported rule 7's bash-loophole clause and
plan-gate's cheap-unknown clause as **ABSENT**. Both were present; both grep
patterns spanned a line wrap. Re-run with whitespace-normalized matching: 24/24
present. This is the second time in this audit a mechanical check was itself the
defect — the first was the link checker's 25 false positives. Recorded as the
standing caveat: *a grep is only as good as its pattern, and a failing check
earns the same scrutiny as a failing artifact.*

**What this validation does NOT cover, stated per the law it enforces:** the
claude.ai **instructions box** cannot be read from here. Its contents are
`ATTEMPTED-FAILED` — no API path exists from this environment — and rest on the
owner's report that the paste was completed. The skill uploads, by contrast, are
`EVIDENCE`: hash-matched against the live synced copies above. The distinction is
the point of the patch.
