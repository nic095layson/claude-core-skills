# Hypothesis — brand-standard NOT-clause excludes third-party clinical/client documents (2026-07-21)

**Pre-registered at adoption; the A/B is owed, not run.** Motivated by the
perspective-taking deck AAR (`results/2026-07-21/AAR-perspective-taking-deck.md`
§3): building a clinical stimulus deck for a third party's client, brand-standard
**loaded and then correctly resolved to "does not apply"** — the body's rule 5
(never apply David's brand to a third party's document) did the work after the
context cost was already paid. The AAR: "Arguably it should not have triggered at
all." This edit moves the boundary from the body to the trigger.

This IS a **description/trigger** edit — the class research-methodology most
strictly gates. Landed per the No-silent-defaults precedent (owner-directed
adoption via the AAR, honest status, revert unforced); the trigger A/B remains
owed before this can be called validated.

## The change (one variable)

Changing the `description` of `.claude/skills/brand-standard/SKILL.md`

FROM (exact):
> …nor for text written in another party's voice (quoting a counterparty, filling
> their form); for how to author skills, see skill-authoring.

TO (exact):
> …nor for text written in another party's voice (quoting a counterparty, filling
> their form), nor for clinical or client-owned documents about a third party (not
> David's brand); for how to author skills, see skill-authoring.

(987 chars after edit, measured — within the ≤1000 house target, under the 1024 cap.)

**will** cause sessions asked to produce clinical/client-owned material about a
third party (protocols, stimulus decks, session documents for someone else's
client) to **not load** brand-standard at all, while all existing should-fire
phrasings ("format my resume", "draft an email for me", …) keep firing.

## Pre-registered predictions (per case)

No `evals/brand-standard.json` exists yet — **case gap** (skill-authoring step 5);
these cases become the seed set when the A/B runs. Fresh session per run, N=2 per
case per arm.

| # | Case (prompt) | OLD prediction | NEW prediction (target) |
|---|---|---|---|
| 1 | "Build a visual stimulus deck for my ABA client's perspective-taking program per this protocol" | Loads, then self-limits to does-not-apply (context cost paid) | **Stays silent** — never loads |
| 2 | "Format my resume for the Anduril posting" | Fires | **Unchanged** — fires |
| 3 | "Draft an email to my recruiter about the offer" | Fires | **Unchanged** — fires |
| 4 | "Write a README for this repo" | Silent | **Unchanged** — silent |

## Evidence bar (research-methodology R1–R3)

R1: N=2 floor per case per arm. R2: any should-fire regression (cases 2–3)
blocks — a narrower trigger that stops firing on David's own documents is worse
than the context cost it saves. R3: flaky case-1 = inconclusive.

## Status

**ADOPTED OWNER CANDIDATE 2026-07-21 — NOT A/B-VALIDATED; trigger run owed.**
On confirm: promote, note in Provenance, and create `evals/brand-standard.json`
from the case table. On fail (case 2 or 3 regresses): revert the description,
append a DEAD entry to `.claude/LESSONS.md` — the body's rule 5 already carries
the boundary as a fallback.
