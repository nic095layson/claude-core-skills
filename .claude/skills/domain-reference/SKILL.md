---
name: domain-reference
description: >-
  Claude Skills domain knowledge for someone who has never authored one — what a
  skill/SKILL.md/.skill file is, how discovery and triggering actually work, where
  skills live on each surface (Claude Code project vs personal vs claude.ai vs
  cloud), what frontmatter does, why the description is the entire trigger, and
  this library's glossary and assumption register. Load when you (or the user) ask
  "what is a skill", "how does a skill get triggered", "why isn't the body enough",
  "where do skills go", "what's a .skill file", or when any glossary term below
  needs its definition of record. Do NOT load for authoring mechanics and house
  style (skill-authoring), fixing a skill that misbehaves (debugging-playbook), or
  install/packaging runbooks (install-and-surfaces) — this is the concepts layer
  only.
---

# Domain Reference

The domain knowledge a mid-level engineer or Sonnet-class model lacks on day one,
as it applies to operating this governance library — not a textbook.

## The mental model

A **skill** is a directory containing a `SKILL.md` file: YAML frontmatter (`name`,
`description`) plus a markdown body. The platform shows Claude every installed
skill's *name + description* at all times; the *body* is loaded only when the
description matches the situation. Three consequences that explain most skill
behavior:

1. **The description is the API; the body is the implementation.** Trigger quality
   lives entirely in the description. "Only use this when…" written in the body is
   dead text — the body is read only after the trigger already matched.
2. **Progressive disclosure bounds cost.** Descriptions are always in context
   (~130 words each as measured across this library, 2026-07-11 — this is why
   over-installing skills has a price); bodies load on demand; bundled `scripts/`
   and `references/` files load or execute only when the body directs.
3. **Discovery is by path, and path failures are silent.** A syntactically perfect
   SKILL.md at the wrong path is readable as a file and invisible as a skill, with
   zero error output (the founding incident: `nic095layson/claude` commit
   `6dc366f` — three days shipped-but-dead at repo root).

## Where skills live (as of 2026-07-11)

| Surface | Location | Scope |
|---|---|---|
| Claude Code — project | `<repo>/.claude/skills/<name>/SKILL.md` | Sessions opened in that repo |
| Claude Code — personal | `~/.claude/skills/<name>/SKILL.md` | Every session on that machine |
| claude.ai web/mobile | Uploaded `.skill` zip (Settings → Capabilities → Skills) | That account's claude.ai sessions |
| Cloud / plugin surfaces | Managed by the platform or plugin | Per the surface's own config |

A **`.skill` file** is a zip whose root contains exactly `<name>/SKILL.md`
(verified against the real artifact in `nic095layson/claude`, 2026-07-10). Same
prose, different transport.

**Corollary that costs people days:** these locations are independent copies.
Editing one does not update the others, and a session loads exactly one — the
"stale copy" failure class in debugging-playbook §4. Capabilities are equally
per-surface: a claude.ai integration grant does not exist on a local machine
(debugging-playbook §5).

## Glossary (definitions of record for this library)

| Term | Definition |
|---|---|
| **Trigger** | The match between a situation and a description that loads a skill body. Not a keyword list — the model matches by situation, which is why descriptions state situations AND quote phrases AND carry a NOT clause. |
| **Governor** | One of this library's five core skills (plan-gate, adversarial-verify, live-state-truth, scope-fence, lessons-ledger) — behavior-governing, surface-portable, project-agnostic. |
| **Instance** | A project-specific implementation of a governor's law (e.g. `failure-archaeology` in nic095layson/claude is the instance of lessons-ledger there). Instances win over governors inside their project — see architecture-contract. |
| **Drift** | Two things that must agree no longer do. See live-state-truth (detection) and lessons-ledger (chronicle). |
| **Ceremony** | Governance ritual applied where it adds nothing (planning ritual on trivia). The library's named self-failure-mode; every governor carries a triage/proportionality rule against it. |
| **Volatile fact** | A true statement a future action can silently falsify. Carries a date or carries nothing. |
| **Assumption register** | Numbered, falsifiably-stated unknowns (A1, A2…) carried through work. Format in plan-gate. |

## This library's assumption register (as of 2026-07-11)

| # | Assumption | Basis | Status |
|---|---|---|---|
| A1 | The five-governor decomposition matches how the owner wants Claude governed holistically | The owner's 2026-07-11 instruction naming exactly these five, plus "governing Claude wholistically" | **measured 2026-07-11 (Phase 2 behavioral evals, Claude Code headless, `claude-opus-4-8[1m]`), partially confirmed.** 40 paired with/without `claude -p` A/B runs, signatures pre-registered, graded in isolation, cwd outside the repo & `~/.claude` so the without-arm truly lacked all five (fired 0/20; governors restored byte-identical). Signature present with-lib / without-lib: **plan-gate 4/4 / 0/4 (clean delta — the gate block appears only with it)**; **scope-fence 4/4 / 0/4 (clean delta — fixes only the named bug + flags adjacent only with it; without, it silently did the dangled cleanup)**; **adversarial-verify 4/4 / 0/4 structured (the criteria-grid+refutation form appears only with it, but the base model catches the same bugs — value is discipline on these cued prompts)**; **lessons-ledger 4/4 / 2/4 (base model records ~half the time via the built-in Claude Code memory feature — partial overlap)**; **live-state-truth 4/4 / 4/4 (NO delta — base model already probes live state and refuses the doc on these prompts)**. So the decomposition is behaviorally real for plan-gate & scope-fence, structurally real for adversarial-verify, and **for lessons-ledger & live-state-truth the base model / harness already supplies much of the behavior** — both routed to architecture-contract for a context-cost review. Prompt-set limitation: 3/5 signatures were tested with behavior-cueing prompts (a should-verify-but-uncued prompt is the sharper next test). Evidence: `results/2026-07-11/phase2/` (`RESULTS-PHASE2.md`, `PHASE2-GRADES.md`). **Reconciliation (2026-07-11):** this Phase 2 collided with a second concurrent campaign job (INC-4); the clean out-of-repo dataset (`transcripts_v2/`) was **independently blind-regraded + adversarially verified** with cell-for-cell agreement (0 verifier flips), and the contaminated 5/20 with-arm was excluded — authoritative summary `results/2026-07-11/phase2/RECONCILED-PHASE2.md`. Findings above are unchanged by the reconciliation. **Cross-model discriminating test (Sonnet, 2026-07-11):** the two overlap findings were re-run on `claude-sonnet-5` (both arms, exact Phase 2 prompts/planted/signatures, 16 fresh `claude -p`, cwd out-of-repo, lockfile held, restored byte-identical, without-arm sentinel 0/8, blind-graded) to test the founding premise that *smaller* models lack the native behavior. **Premise not borne out — hypothesis REFUTED for both:** **live-state-truth Sonnet 4/4 with · 4/4 without (no delta, same as Opus)**; **lessons-ledger Sonnet 3/4 with · 4/4 without (the partial Opus delta 4/4·2/4 does NOT reproduce — Sonnet base records *more* reliably via the built-in memory feature)**. Both → RETIRE-CANDIDATE under the committed rule → architecture-contract owner decision. Cued-prompt caveat still bounds it (uncued test outstanding). Evidence: `results/2026-07-11/phase2-sonnet/RESULTS-SONNET-DISCRIMINATING.md`. **Uncued discriminating test (2026-07-11) — the outstanding measurement, now done:** 32 fresh runs on newly-designed uncued prompts (doc makes a FALSE checkable claim the task depends on / session hits+fixes a planted live failure), both models, blind-graded, without-arm sentinel 0/16, pre-registered before any run. Governors barely fire uncued (live-state-truth 2/8, lessons-ledger 0/8). **live-state-truth 4/4·4/4 (Opus) / 4/4·4/4 (Sonnet) → RETIRE-CONFIRMED** — no delta in any of 8 cells; the base model reads the authoritative source (server.js/.nvmrc/package.json) and catches the doc's false port/version even uncued. The premise that live-state checking needs a governor is **refuted** for this governor. **lessons-ledger 0/4·0/4 both models → INCONCLUSIVE** — governor didn't fire on a self-encountered failure and base model didn't spontaneously record the quick fixes, so the test couldn't discriminate; earns its cost in no test but no clean RETIRE. Recorded at architecture-contract weak-point 5. Evidence: `results/2026-07-11/phase2-uncued/RESULTS-UNCUED.md`. Other surfaces OPEN. |
| A2 | Descriptions written here trigger reliably across surfaces | House trigger-design rules; measured Phase 1, 2026-07-11 | **measured 2026-07-11 (Claude Code headless only), trending FALSIFIED for this surface** — fresh-session should-fire trigger rates: plan-gate 1/6 (17%), scope-fence 2/6 (33%), adversarial-verify 0/6 (0%, prompt-confounded — see results), lessons-ledger 2/6 (33%), live-state-truth 6/9 (67%); all five FAIL the ≥83% gate. should-not-silent 100% across all (no over-fire, no co-fire). Triggering is phrasing-deterministic: some phrasings fire every run, others never. Other surfaces (interactive Claude Code, claude.ai) OPEN. Evidence: `results/2026-07-11/`; rewording hypotheses pre-registered in `experiments/`. **Update 2026-07-11 (A/B rewording session, same model `claude-opus-4-8[1m]`, same-condition OLD re-baselines):** after description-only rewords, headless should-fire rates are now **adversarial-verify 6/6 (100%, ACCEPTED), plan-gate 9/9 (100%, ACCEPTED), live-state-truth 9/9 (100%, ACCEPTED)** — 3/5 governors now PASS the ≥83% gate (were 0/5); **scope-fence 4/6 and lessons-ledger 12/15 (80%) still FAIL** and were reverted to OLD (their rewords were regression-free improvements but hit a triggering ceiling — escalated to architecture-contract). should-not-silent remained 100% for all (zero regressions). So A2 is now **partially confirmed for headless: reliable triggering IS achievable via description wording for 3/5 governors, dated; 2/5 appear ceiling-bound. Evidence: `results/2026-07-11/RESULTS-AB.md`. claude.ai still OPEN and the 3 accepted uploads are now STALE.** **Update 2 (length-compliance, 2026-07-11):** the platform spec caps descriptions at 1024 chars; the accepted/adopted wordings exceeded it, so all five were trimmed ≤1000 (969–1000) preserving load-bearing surfaces verbatim and **re-passed with no rate loss** — adversarial-verify 6/6, plan-gate 9/9, live-state-truth 9/9 (gates hold); scope-fence and lessons-ledger adopted as owner-approved better wording (gate stays FAIL — scope-fence id1 improved 0/2→3/5 but flaky, lessons-ledger ~80%). All five descriptions are now within the claude.ai upload limit. See `experiments/hypothesis-2026-07-11-length-compliance.md`. |
| A3 | Personal-install of the five governors (not all 13 skills) is the right activation footprint | Progressive-disclosure cost argument in architecture-contract | unconfirmed — owner may prefer all or fewer |
| A4 | `nic095layson/claude` remains the live instance-repo whose project skills take precedence there | Its 15 skills verified present 2026-07-11 | verified 2026-07-11; volatile |

## When NOT to use this skill

- Writing or restructuring a skill → **skill-authoring**.
- A skill misbehaves → **debugging-playbook**.
- Installing, packaging, or verifying per surface → **install-and-surfaces**.
- Why this library is shaped the way it is → **architecture-contract**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`domain-reference` and `skill-authoring` (discovery paths, trigger mechanics,
`.skill` format — all verified there 2026-07-10 against live artifacts), plus the
platform docs at https://docs.claude.com/en/docs/agents-and-tools/agent-skills
(re-check for surface changes; details beyond the above are unverified here).

Re-verify: discovery paths — create a test skill under `~/.claude/skills/` and
confirm it appears in a fresh session's loaded list; `.skill` format —
`unzip -l` any known-good artifact. Update when: the platform adds frontmatter
fields or discovery paths, or any register row's status changes.
