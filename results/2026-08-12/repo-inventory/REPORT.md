# Repository inventory — everything unmerged, sorted (2026-08-12)

**Owner's request (near verbatim):** compile a list of outstanding items — commits,
files, anything unmerged — sorted by what is outdated and no longer needed,
critical, important, irrelevant. Clean and ledger it.

**Method.** `git fetch --prune`, then for every remote branch: ancestry check
(`merge-base --is-ancestor`) *and* content check (`diff origin/main..branch
--diff-filter=A`), because a squash-merged branch reads as "unmerged" by ancestry
while its content is already on main. Ancestry alone would have overstated this
list by four branches. PR states via the GitHub API, same day. Every count below
is from those commands, not from recall.

**Headline.** 11 branches are unmerged by ancestry; **9 carry content main does
not have**, and 2 are fully superseded. One branch — `rivian-stock-analysis` —
holds 235 files including validated work the library is currently missing and
already lost once (INC-11). Three separate branches have each written their own
`INC-9`, `INC-10` and `INC-11`, and two have written conflicting
`adversarial-verify` rules 6–7. **Nothing here is safe to bulk-merge.**

---

## CRITICAL — act first

### C1. `claude/rivian-stock-analysis-h5y46x` — PR #8, draft, open since 2026-07-15

17 commits · **235 files main lacks** · last touched 2026-07-16.

The branch INC-11 was about. It has already cost the library one live feature.

| What's on it | Why it matters |
|---|---|
| `hooks/governance-trigger.py` + `governance-enforce.py` | **Validated Stop-hook enforcement, 0/3 → 3/3.** Solves forced skill-loading. The library has no equivalent on main. |
| GAUNTLET definition + `instructions/PASTE-INTO-SETTINGS.md` | Restored to main 2026-08-12 by re-authoring, **not** by merging. The originals still only exist here. |
| INC-8 (governors applied "in spirit", never loaded) | The founding incident for the load-don't-recall law. Main has no record of it. |
| DEAD-3 (widening a description doesn't fire the analysis class) | Prevents someone re-running a settled failed experiment. |
| 226 files under `results/2026-07-15/` and `2026-07-16/` | The evidence for every rate above. |

**Risk if ignored:** this is one branch-delete away from permanent loss, and it is
the single largest concentration of measured work in the repo.
**Blocker:** its ledger carries its own INC-9/10/11 (see C2).

### C2. Ledger numbering has forked three ways

| Number | On `main` | On `rivian-stock-analysis` | On `review-instructions` |
|---|---|---|---|
| INC-9 | "Couldn't verify" used for work never attempted | UserPromptSubmit hook forces load but induces receipt confabulation | Headless children inherit parent session id |
| INC-10 | Inference graded SUPPORTED after owner agreed | Nested `claude -p` shares transcript → hook contamination | Cloud egress proxy fails TLS in waves |
| INC-11 | GAUNTLET lost to an unmerged branch | Governance-receipt law confabulates → REVERTED | — |

Three different INC-9s. `lessons-ledger` forbids renumbering because references
depend on the numbers — so the reconciliation must **re-key by date and branch**
(e.g. `INC-9a/9b/9c` or `INC-2026-07-16-01`), not renumber, and every citing file
must be updated in the same commit. **This blocks C1, E1 and E4 merges.**

### C3. `adversarial-verify` rules 6–7 conflict

Main (merged 2026-08-11) says: 6 = receipt law, 7 = aggregates-from-records.
`claude/aba-perspective-taking-slides-kzbj3c` (2026-07-21) says: 6 = verify at the
source of truth, 7 = a broadly-failing check indicts the checker.

Both are good rules. Both cannot be 6 and 7. Whichever merges second must be
renumbered 8–9 **and** the merge must state that it did so — architecture-contract
invariant on not silently renumbering cuts both ways.

---

## IMPORTANT — real content missing, no conflict

### I1. `claude/sol-skill-analysis-vkog26` — PRs #10 (closed), #11 (draft, open)

**54 files under `results/2026-08-03/`.** PR #10 merged the *skills and proposals*;
the *raw evidence* stayed behind. That directly violates after-report §2 ("raw
supporting artifacts are committed beside the report, not summarized away"), and
main currently cites results that are not there. Low-risk, additive, no conflicts.

### I2. `claude/review-instructions-z0fhnb` — PR #13 (closed)

1 experiment pre-registration (`hypothesis-2026-08-10-decision7-pointer-cleanup.md`)
plus two ledger entries. Same pattern as I1 — the report merged, the
pre-registration and ledger did not. Carries the C2 collision.

### I3. `claude/sonnet-opus-validation-055lae` — PR #5, draft, open since 2026-07-14

`evals/cross-model-parity.json` + `.md` + a results file. An eval set main does
not have. Additive, no conflicts. Age is the only question: is cross-model parity
still a live concern post-Fable?

### I4. `add-claude-code-global-doctrine` — PR #4, open since 2026-07-14

One file: `instructions/claude-code-global-doctrine.md`, the canonical copy of
`~/.claude/CLAUDE.md`. The repo versions the claude.ai instructions on exactly
this reasoning ("a steering artifact belongs in the repo"), so the Claude Code
equivalent being unversioned is an inconsistency. Small and self-contained.

---

## MODERATE — owner judgement, no urgency

### M1. `claude/aba-perspective-taking-slides-kzbj3c` — PR #9, draft, open

7 files: an `aba-stimulus-deck` project skill, ABA project instructions, an AAR,
and 3 experiment pre-registrations. **Not part of the governance library** — it is
a separate project's operating layer that happens to live here. Decide whether
this repo is its home or whether it belongs in its own project. Carries C3.

### M2. `claude/skill-md-audit-1v5bl6` — PR #1, **closed without landing**

15 files: 6 capability SKILL.mds (docx, frontend-design, mcp-builder, pdf, pptx,
xlsx) + 6 eval sets. You already have these skills at account level, so vendoring
copies here would create exactly the drift this library warns about. Closed looks
deliberate — but the **eval sets** may be worth salvaging even if the skills are not.

### M3. `claude/fable-skill-library-analysis-b9ysxy` — PR #2, **closed without landing**

76 files: 69 vendored external skills, an installer, `OPERATIONS.md`, `CLAUDE.md`.
The *analysis report* landed on main via PR #3; the *vendored library* did not.
Same call as M2 at larger scale, plus a supply-chain question — vendored
third-party skills need a review and update policy this repo does not have.

---

## SUPERSEDED — safe to delete

| Branch | Evidence it is spent |
|---|---|
| `claude/chat-error-verification-fix-flq49c` | **MERGED** (PR #14). Ancestry confirms. Delete. |
| `claude/product-output-skill-research-jt42nu` | **0 files main lacks** — landed via PR #12. Delete. |
| `claude/sonnet-opus-verification-prompt-746x8n` | **0 files main lacks** — landed via PRs #6/#7. Delete. |

These three are the only ones where "outdated and no longer needed" is
demonstrable rather than a judgement call. Everything else on this page still
holds content main does not.

## IRRELEVANT / no action

- PRs #3, #6, #7, #10, #12, #13 — content on main; the PR records are history.
- `claude/hook-livefire-record` — PR #15, this session's live work, not outstanding.

---

## Outstanding items that are not git

| # | Item | State |
|---|---|---|
| N1 | Re-paste the instructions block (now 4,844 chars, GAUNTLET restored) | **Owner action — blocking.** Until done, the box lacks GAUNTLET. |
| N2 | Upload `gauntlet.skill` to claude.ai | **Owner action.** Packaged and delivered 2026-08-12. |
| N3 | `evals/gauntlet.json` — 8 cases | AUTHORED, **NOT RUN** |
| N4 | `evals/gap-provenance.json` E1/E2/E5/E6 | AUTHORED, **NOT RUN** (budget decision, not a limit) |
| N5 | Uncued firing of the patched governors | **UNMEASURED** — the open question from INC-9 |
| N6 | `hooks/receipt-law-stop-gate.sh` | Pipe-tested 10/10, live-fired for false-positives only; **not installed** |
| N7 | INC-10 (SUPPORTED-grade defect) | **OPEN, contested** — evidence incomplete by design |
| N8 | "The load is the procedure (law)" | Dropped 2026-08-03 by the INC-11 route; **not restored** — owner call |
| N9 | `photo-editing` names two skills absent from this repo | Pre-existing, flagged, unfixed |

---

## Recommended order

1. **C2 first.** Nothing merges cleanly until the ledger fork is re-keyed.
2. **C1** — rescue the rivian branch. Highest value at risk.
3. **N1 + N2** — two minutes, unblocks the live surface.
4. **I1, I2** — evidence restoration, additive, low risk.
5. **Delete the three superseded branches.**
6. **I3, I4, then M1–M3** as judgement allows.

**Do not** bulk-merge. Two branches modify the same governor and three modify the
same ledger; a merge queue without C2 resolved would produce a library that
contradicts itself, which architecture-contract rates worse than one with a gap.

## Bounds

**Out of scope by design:** the source repo `nic095layson/claude`; anything in
the claude.ai account beyond the skill roster; whether the closed PRs #1/#2 were
closed deliberately — the PR records do not say, and no ledger entry explains
them, so "likely deliberate" is INFERENCE.

**In scope and unverified:** whether each unmerged branch still *applies* after a
month of drift (`NOT-ATTEMPTED` — not opened file-by-file, only inventoried);
whether the rivian branch's hooks still run against the current CLI
(`NOT-ATTEMPTED`); the content of PR #11's draft measurements beyond its file list
(`NOT-ATTEMPTED`). All three are cheap to resolve and unchecked by choice.

---

## Deleted branches — recovery record (2026-08-12)

Deleted after proving zero loss two independent ways: (a) `git diff
origin/main..<branch> --diff-filter=A` returns **0 files** at each branch tip, and
(b) every unique commit's files were checked individually against main. The two
files that first read as "absent from main" on `product-output-skill-research`
turned out to be absent from the **branch tip** as well — added and then removed
on the branch itself, so there was nothing to lose. That discrepancy is why the
per-commit check was run at all; the file-count check alone would have been a
weaker basis than it looked.

**DELETION ATTEMPTED-FAILED (2026-08-12).** `git push origin --delete <branch>`
returned **HTTP 403** for all three. This session's git credentials can create and
update refs but not delete them; the GitHub MCP surface exposes `create_branch`
with no delete counterpart, so there is no second route from here. The branches
are still on the remote, verified with `git ls-remote --heads`. **Owner action to
finish:** run the three commands below from a machine with delete rights, or use
the GitHub branch UI.

```bash
git push origin --delete claude/chat-error-verification-fix-flq49c
git push origin --delete claude/product-output-skill-research-jt42nu
git push origin --delete claude/sonnet-opus-verification-prompt-746x8n
```

*Recorded honestly rather than as "done": a first pass of this command printed
"deleted" for all three because the shell `&&` was chained to a `tail` that
succeeded while the push underneath it failed. The branches were still there. The
verification that caught it was `git ls-remote`, not the command's own output —
a command's exit path is not evidence that the thing it names actually happened.*

**Any of these can be restored** with
`git push origin <sha>:refs/heads/<branch-name>`:

| Branch | Tip SHA | Basis for deletion |
|---|---|---|
| `claude/chat-error-verification-fix-flq49c` | `2e0cc65606f08f5ad03f3822584f3fee07cdc1e1` | Ancestor of `main` — fully merged via PR #14 |
| `claude/product-output-skill-research-jt42nu` | `0464cb078984859089f2f46d5264b3204bd27145` | 0 files main lacks; landed via PR #12 |
| `claude/sonnet-opus-verification-prompt-746x8n` | `2d6eca4688d0de0820a28764eb82e6257dedbc44` | 0 files main lacks; its instructions copy is the 2026-07-15 version — no GAUNTLET, no receipt law, strictly superseded |

**Not deleted, deliberately:** `claude/rivian-stock-analysis-h5y46x`,
`claude/sol-skill-analysis-vkog26`, `claude/review-instructions-z0fhnb`,
`claude/sonnet-opus-validation-055lae`, `add-claude-code-global-doctrine`. Their
*additive* content was migrated to this branch, but the migration deliberately did
**not** take their versions of files main already had — so those branches still
hold divergent history that has not been reconciled. They stay until this PR is
merged and someone confirms nothing further is wanted from them. Deleting a source
branch before its migration has landed is how INC-11 happened.

---

## HOLD branches salvaged and retired (2026-08-12)

Both HOLD branches were opened, assessed file by file, and drained of what the
library actually wants. **Taken: 8 files. Left behind: 68.** The split was not
about age or size — it was about whether taking a file creates an obligation the
repo has no mechanism to meet.

### Taken

| From | What | Why |
|---|---|---|
| `skill-md-audit` | `evals/{docx,frontend-design,pdf,pptx,xlsx}.json` | Trigger evals work regardless of where the skill lives. The owner uses all five daily with **zero** measurement on any of them. |
| `skill-md-audit` | `CAPABILITY-SKILLS-CONFLICT-AUDIT.md` | Analysis worth keeping |
| `fable-skill-library` | `CLAUDE-AI-VALIDATION.md` | Same |
| `fable-skill-library` | `.gitignore` | Main had none; extended with `__pycache__/`, which the rescued `hooks/*.py` generate |
| *(authored fresh)* | `CLAUDE.md` | **Main had none.** A repo with 21 skills, 300+ result files, a ledger and a guard gave an arriving session no orientation at all. Written new rather than ported — the branch copy references an `external-skills/` layer we deliberately did not take, so porting it verbatim would have shipped a doc that lies on arrival. |

### Left behind, deliberately

**The 13 vendored third-party skills** (`owasp-security`, `test-driven-development`,
`systematic-debugging`, `writing-plans`, `fable-method`, and 8 more — 69 files).
Vendoring third-party code means owning its staleness, provenance and update
policy. This repo has none of that, and the branch's own README states the policy
("never edited in place — re-vendor from upstream") with no mechanism behind it.
Thirteen skills rotting silently is a liability, not an asset.

**Five duplicate capability SKILL.mds** (`docx`, `frontend-design`, `pdf`, `pptx`,
`xlsx`). All five already exist at account level. A repo copy of an account-level
skill is two sources of truth that drift apart in silence — INC-11's exact
mechanism, in the library whose purpose is preventing it.

**`mcp-builder`** (skill + `evals/mcp-builder.json`). Owner-declined. Unlike the
other five it is *not* a duplicate — it is a genuine capability the account does
not have, which scaffolds MCP servers (tools Claude can call) rather than skills
(workflows Claude follows). Nothing in current use resembles "expose my API as
tools for Claude". Declined on `architecture-contract` Decision 5 grounds: every
installed description is permanent context, and this one has never been needed.
Its eval set was left *with* it rather than salvaged — an eval for an absent skill
is a dangling reference, and this repo already fixed one of those this week.

**`tools/install-external-skill.sh`, `OPERATIONS.md`, `external-skills/*`** — all
serve the vendored layer that was declined.

### Retrieval, if any of this is ever wanted

Both branches remain on the remote (deletion is blocked repo-wide; see the
ATTEMPTED-FAILED record above). Nothing below needs re-deriving:

```bash
# mcp-builder, whole skill + its evals
git checkout origin/claude/skill-md-audit-1v5bl6 -- .claude/skills/mcp-builder evals/mcp-builder.json

# the 13 vendored skills + installer
git checkout origin/claude/fable-skill-library-analysis-b9ysxy -- external-skills tools/install-external-skill.sh
```

Both branches are now **drained of everything the library wants**. They hold only
declined content, and that content is one command away.
