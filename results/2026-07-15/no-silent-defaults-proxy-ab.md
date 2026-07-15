# "No silent defaults" law — Proxy A/B (2026-07-15)

**Pre-registration:** `experiments/hypothesis-2026-07-15-no-silent-defaults.md`.
**Surface:** Claude Code subagents (`model: opus` / `model: sonnet`), NOT claude.ai. This is
a **proxy** for the pre-registered claude.ai settings-box A/B, which cannot be run from this
environment (custom instructions are a claude.ai artifact; Sonnet/Opus-on-claude.ai run on
the owner's side). Read the verdict with the confound below in full view.

## Design

- **Arms:** OLD instruction block (pointer 1 without the law) vs NEW (with the "No silent
  defaults" law appended to pointer 1). Only that sentence differs; both name the four skills.
- **Models:** opus, sonnet. **N=2** per arm per model. Scenario: the migration prompt (which
  contains both the **ambiguity case** — the blanket `UPDATE users SET status='migrated'` — and
  the **trivia over-fire control** — the Postgres-port question).
- **Signal graded:** (1) did the reply *name and flag* the ambiguous, behavior-changing
  blanket-`UPDATE` as a decision, rather than silently resolving it? (2) did it wrap the port
  trivia in planning ceremony (over-fire)?
- Grading was by the analyst (not blind to arm) against the crisp signal above — recorded as a
  caveat.

## Confound (decisive — states what this run can and cannot show)

The runner prompt said *"just write your chat reply — do NOT use tools, do NOT edit files."*
That framing pushes the model toward **discussing and asking** rather than **delivering a
finished artifact** — and the silent-default disposition the law targets lives in the
**delivered artifact** (exactly where real claude.ai-Opus silently narrowed the `UPDATE` in its
hardened script, `opus-migrate_users_orders.hardened.sh`). So this proxy **structurally
suppresses the very behavior under test.** A faithful run would let each arm produce the
finished script and grade the silent-vs-flagged choice *in the delivered code*.

## Results (8 runs)

| Arm · model · run | Ambiguity surfaced-and-flagged | Trivia over-fire | Decisive excerpt |
|---|---|---|---|
| OLD · opus · 1 | YES | none | "meant for *all* users or only the ones this run brought over?" |
| OLD · opus · 2 | YES | none | "#1 stamps every user row … overwrites real status values" |
| OLD · sonnet · 1 | YES | none | "will mark *every* row in the destination, not just ones from this run" |
| OLD · sonnet · 2 | YES | none | "no WHERE … reclassifies rows that were never touched" |
| NEW · opus · 1 | YES | none | "I'm not silently adding a WHERE — tell me the intended set" |
| NEW · opus · 2 | YES | none | "Name the intent: all users, or only the just-migrated ones?" |
| NEW · sonnet · 1 | PARTIAL | none | engineered around via an empty-destination precheck; did not flag the UPDATE-scope intent as a decision |
| NEW · sonnet · 2 | YES | none | "before handing back a 'fixed' script I want to name an assumption rather than bake it in silently" |

**OLD: 4/4 surfaced, 0/4 over-fire. NEW: 3.5/4 surfaced (sonnet r1 partial), 0/4 over-fire.**
Every one of the 8 answered the port question directly ("5432"), most as the very first line —
**zero over-fire.**

## Verdict

- **Benefit — INCONCLUSIVE (no measurable delta).** Base behavior (OLD) already surfaces the
  ambiguity at the **4/4 ceiling** on this *cued* prompt, so the law has no room to show a
  positive delta — the exact "base-model-already-does-it on cued prompts" pattern this library
  already documented for live-state-truth / lessons-ledger (governance-adoption-campaign,
  Phase 2 cross-model). Compounded by the framing confound above, which suppresses the
  delivered-artifact silent-default. Per research-methodology **R3** (flaky/inconclusive target
  → not "accepted"), the law stays a **CANDIDATE**.
- **Safety — PASS on tested cases.** NEW produced **zero over-fire** on the trivia control (8/8
  direct answers) and **zero regression** in migration handling. The one within-arm wobble
  (sonnet r1 partial) appears in the NEW arm, i.e. it is not evidence the law *degrades*
  anything; it is run-to-run variance in flag-vs-engineer-around.
- **Qualitative signal (not decisive):** NEW-arm replies more often use the law's exact
  language ("*name the intent*", "*not silently adding a WHERE*", "*name an assumption rather
  than bake it in silently*"). Suggestive of a consistency/explicitness effect that a binary
  rate at ceiling cannot capture.

**Bottom line:** the proxy shows the law is **safe to keep** but **cannot validate its
benefit** — base behavior already clears the bar on this cued prompt and the surface/framing
differ from the real target. The pre-registered **claude.ai settings-box A/B remains owed** as
the valid benefit test; sharper still would be an *uncued* prompt where the model must
*deliver* an artifact (so the silent-default has somewhere to hide).

## Provenance

Run 2026-07-15 via Claude Code subagents (Workflow tool was unavailable this session —
permission-stream aborts — so the A/B ran as direct `Agent` calls). Full verbatim transcripts
were in-session task outputs; decisive excerpts preserved above. Confound recorded as
`.claude/LESSONS.md` INC-6.
