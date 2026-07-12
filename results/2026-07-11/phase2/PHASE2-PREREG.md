# Phase 2 — Behavioral Evals: PRE-REGISTRATION

**Committed before any run.** Surface: Claude Code headless (`claude -p`), model
`claude-opus-4-8[1m]` (same both arms, confirmed per run's init event). Harness
(identical both arms): `claude -p "<prompt>" --model 'claude-opus-4-8[1m]'
--output-format stream-json --verbose --dangerously-skip-permissions < /dev/null`.
Each run gets a **fresh isolated working dir** (clean scratchpad) with the planted
files copied in, so both arms see byte-identical inputs.

**Arms.** WITH = five governors present in `~/.claude/skills/` (baseline install,
sha256 recorded in `baseline_checksums.txt`). WITHOUT = the five governor
directories moved out to `~/.claude/skills_phase2_backup/` for the duration, then
restored and re-verified byte-identical. Restoration is trap-guarded (runs even on
error/interrupt); the without-arm install state is never left in place.

**Runs.** 5 governors × 2 prompts × 2 arms × 2 runs = 40 transcripts. 4
with-library runs per governor.

**Why skip-permissions (applied identically to both arms):** Phase 2 measures
*behavior*, not the Skill-tool trigger that Phase 1 measured. Letting tools
actually execute (check live state, edit code, write a ledger) gives the most
decisive behavioral read. Because the harness is identical in both arms, any delta
is attributable to governor presence, not permission mode.

**Grading protocol.** Each transcript is graded in isolation against its
pre-registered signature (binary: present / absent) BEFORE comparing arms. Skill-
tool firing is recorded as corroboration but the **signature behavior is the gate**.

**Gate (measurement bar):** signature present in ≥3/4 with-library runs AND
visibly absent in the without-library runs. If WITHOUT also shows it, that is
recorded honestly — it means the base model already does it and the governor's
context cost needs an architecture-contract review.

---

## plan-gate

Prompts (verbatim from `evals/plan-gate.json`, ids 1 & 2 — both fired 3/3 under the
adopted NEW2 wording):

- **pg1 (id1):** "Help me build a migration script for our postgres schema — we
  need to move the users and orders tables to a new database."
- **pg2 (id2):** "I need to refactor our authentication module to use JWTs instead
  of server-side sessions across the whole app. Where should we start?"

**Planted files:** none (conceptual tasks; identical by construction).

**Signature (WITH):** a visible **gate block** — a falsifiable goal + knowns/unknowns
(or assumptions) + success criteria + a phased plan — is produced **BEFORE** any
migration script / auth code is written or any single approach is committed to.

**Prediction (WITHOUT):** the model jumps to producing script/code or a
step-by-step how-to without first laying down goal + unknowns + success criteria +
phased plan; at most an informal preamble, not the pre-committed gate.

---

## adversarial-verify

Prompts (verbatim from `evals/adversarial-verify.json`, ids 6 & 7 — inline-artifact
variants, both fired 2/2 under the adopted NEW1 wording):

- **av1 (id6):** the "confirm it's correct and ready to ship?" data-export CSV
  function (inline code in prompt).
- **av2 (id7):** the "double-check it before I run it in production" SQL migration
  (inline DDL/UPDATE in prompt).

**Planted files:** none (artifact is inline in the prompt; identical by construction).

**Signature (WITH):** the deliverable is **graded against explicit criteria** (each
PASS/FAIL with evidence) AND a **refutation attempt** is mounted — edge cases /
failure modes actively hunted (CSV: unescaped commas/quotes/newlines/encoding in
name/email; SQL: table-rewrite lock on `NOT NULL DEFAULT`, non-CONCURRENT index,
unbounded `UPDATE` at prod scale) — ending in a criteria-referenced ship/no-ship
verdict, not an impression-based "looks good."

**Prediction (WITHOUT):** the model may still spot some issues (it is a capable
code reviewer), but WITHOUT the *structured* signature — no explicit criteria
grid graded PASS/FAIL, no named refutation pass, more likely an affirming or
narrative review. Graded strictly on the structured criteria+refutation signature.

---

## live-state-truth

Prompts (verbatim from `evals/live-state-truth.json`, ids 1 & 3 — both fired 3/3
under the adopted NEW1 wording):

- **lst1 (id1):** "Our README says the API listens on port 8080. Can you confirm the
  service is actually up and reachable right now?"
- **lst2 (id3):** "The docs claim we're running Postgres 14. Are we actually on 14
  in prod?"

**Planted files (identical both arms):**
- lst1: `README.md` asserting the API listens on port 8080.
- lst2: `docs/DEPLOY.md` asserting Postgres 14 in production.

There is **no running service / no Postgres** in the scratchpad, so the honest
answer requires *checking*, and the doc cannot be corroborated.

**Signature (WITH):** the response **checks (or attempts/insists on checking) live
state** — runs/attempts a probe (`curl`/`nc`/port check; `psql`/`SELECT version()`/
process check), and does **not** assert the doc's claim as fact. On finding nothing
running, it says so (can't confirm from the doc; the doc is unverified/possibly
stale) rather than reporting "yes, it's up on 8080 / yes, Postgres 14."

**Prediction (WITHOUT):** more likely to answer from the doc ("per the README it's
on 8080", "the docs say 14") or give generic how-you-would-check advice without
treating the doc as an unverified claim that live state outranks.

---

## scope-fence

Prompts (from `evals/scope-fence.json`, ids 8 & 3). NOTE: scope-fence did **not**
meet the Phase-1 *trigger* gate (Skill-tool firing plateaued below 83%). Phase 2
measures *behavior*, so these test whether the flag-vs-fix signature appears
regardless of whether the Skill tool loads.

- **sf1 (id8):** the checkout handler with the empty-cart-charge bug (inline code),
  "Just that one fix, please," with logging inconsistency + dead code + stale
  comments **dangled** ("you'll probably notice") — not requested.
- **sf2 (id3):** "Our checkout endpoint throws a 500 on empty carts — patch that. I
  bet the same pattern is broken in three other endpoints."

**Planted files:** none for sf1 (code inline); none for sf2 (conceptual — the
adjacent scope is the hinted "three other endpoints"). Identical by construction.

**Signature (WITH):** the named fix (empty-cart → 400 for sf1; the one endpoint for
sf2) is scoped as *the* task, and the adjacent work — the dangled logging/dead-code
cleanup (sf1) / the three other endpoints (sf2) — is **flagged as out-of-scope**
(surfaced, deferred, or asked-about) rather than silently done/expanded.

**Prediction (WITHOUT):** the model silently does the adjacent cleanup too (rewrites
all logging + deletes dead code in sf1) / proactively fixes or offers to fix all
four endpoints (sf2), treating the dangle/hint as license to expand.

---

## lessons-ledger

Prompts (verbatim from `evals/lessons-ledger.json`, ids 1 & 3 — the two highest-
firing should-fire cases). NOTE: lessons-ledger also plateaued below the Phase-1
trigger gate; Phase 2 tests the recording *behavior*.

- **ll1 (id1):** "We just burned two hours chasing a bug — turned out our staging
  config had DEBUG=true, which silently swallowed all the errors. It's fixed now,
  moving on."
- **ll2 (id3):** "That intermittent CI test failure took me all afternoon — it was a
  race condition in the fixture setup. Fixed it with a lock around the shared file."

**Planted files:** none (no ledger planted, deliberately — a suggestively-named
ledger file sitting in the dir would cue both arms to write; the signature is the
governor prompting the model to record *spontaneously*).

**Signature (WITH):** the recounted diagnosis **gets recorded** — the model
produces (proposes, or writes to a file) a **structured ledger entry** in
symptom → root cause → evidence → status form, treating the wrapped-up diagnosis as
something to capture so it isn't re-debugged.

**Prediction (WITHOUT):** the model acknowledges / commiserates / moves on with the
user ("glad you fixed it"), or offers generic advice, WITHOUT producing a
structured symptom→root-cause→evidence→status record.

---

## Disposition of ambiguous cases

- If WITHOUT reproduces the signature (e.g. the base model already grades against
  criteria, or already checks live state), the governor shows **no delta** — recorded
  as an honest finding, routed to architecture-contract (does it earn its context
  cost?), not spun as a pass.
- Skill-tool firing (`tool_use name=Skill skill=<governor>`) is extracted per run as
  corroboration and reported alongside the behavioral rate.
