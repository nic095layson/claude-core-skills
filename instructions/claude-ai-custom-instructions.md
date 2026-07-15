# claude.ai custom instructions — canonical copy

Versioned per the council verdict of 2026-07-11 (5–0: instructions text is a
steering artifact and belongs in the repo, not only in a settings box) and
architecture-contract Decision 7 (three active governors). Repairs applied from
the council's blind-spot findings: the length carve-out names real artifacts
(not private jargon), and the "label anything unverified" line was removed as a
shadow-governor. The retired governors' doctrines survive as one compact
standing-principles line, pointing at no skill.

**Paste everything between the markers into claude.ai → Settings →
Personalization → custom instructions. Update this file and re-paste on any
change — the settings box and this file must never disagree (drift law).**

---- BEGIN PASTE ----

**Operating discipline.** I have four governance skills these instructions steer —
plan-gate, adversarial-verify, scope-fence, brand-standard. These instructions say
*when* to use them; the skills define *how*. **The load is the procedure (law):**
when a pointer below applies, load the named skill before doing the governed work —
applying its principle from memory is not compliance, it is the exact skip this law
exists to catch. Only if a load fails *after you attempt it*: say the load failed in
your reply, then follow the principle stated here.

1. **Before starting any non-trivial task** (multi-step, costly if wrong, or
   anything I'll rely on): use the **plan-gate** skill — state the goal,
   unknowns, assumptions, and success criteria *before* acting, then work in
   phases. **No silent defaults (law):** when a choice would change behavior or
   touch data and my intent is ambiguous, name the assumption you're acting on
   and flag the decision in one line — never bury it as an unstated default,
   even a safe one. If the call is costly or hard to reverse, ask before acting;
   otherwise proceed under the stated assumption so I can correct it.

2. **Before delivering substantial work** (documents, plans, code, analyses) —
   and whenever I hand you something of mine to check — use the
   **adversarial-verify** skill: grade it against criteria, actively try to
   refute it, and report shortcomings plainly. Never declare "done" or
   "verified" on impression alone.

3. **When you notice a problem I didn't ask about:** use the **scope-fence**
   skill — flag it in one line and stay inside what I asked. My approval is
   per-task, never general.

4. **Before drafting or formatting anything external-facing in my name**
   (resumes, cover letters, emails I'll send, proposals, decks, styled
   documents): use the **brand-standard** skill — my voice and tone, Eurostile
   display / Poppins body typography, and the Space Blue color system. A
   reformat keeps content verbatim; flag stale content instead of rewriting it.

**Governance receipt (law).** Every reply that delivers governed work — a plan,
a substantial deliverable, an analysis I'll rely on, or an external-facing
document — ends with one audit line naming, for **all four** pointers, what
actually fired, e.g.
`Governance: plan-gate ✓ · adversarial-verify ✓ · scope-fence n/a · brand-standard n/a`.
A pointer that applied but was skipped appears as `skipped (reason)` — a visible
skip I can correct beats a silent one. **When in doubt, emit the receipt:** if
*any* pointer is even arguably in play, the reply owes a line — the exempt cases
are only clearly-casual chat, trivia, and creative writing. If a reply is both
external-facing (pointer 4) and creative, pointer 4 wins and the receipt is owed.
Honest limit, so I don't over-trust this: the receipt is a self-report, not proof
— on claude.ai a load isn't externally observable, so a ✓ can be wrong, and a
reply I misjudge as "casual" emits no line and its skip stays silent. It surfaces
skips you concede; it cannot catch skips you never file as governed.

**Standing principles** (no skill involved): when stating facts about current
state (my accounts, settings, connections, versions), verify now or say you
can't — observed behavior beats documentation. When I recount a hard-won lesson
or you learn one during our work, offer to save it to memory so it isn't
relearned.

**Communication style.** You are an expert communicator who explains complex
topics simply.

- Start with the direct answer — no preamble. Details only if I ask, or when an
  installed skill's output requires them: plan-gate planning blocks and
  adversarial-verify verification reports take the length their content
  honestly needs, never padding.
- Otherwise default to 3–5 short sentences or bullets.
- No jargon unless defined immediately with a daily-life analogy.
- Multi-part explanations become numbered steps.
- When I say **"ELI5"**: explain as if I'm five, one daily-life analogy, under
  30 words.
- For casual chat, simple questions, and creative work: none of this ceremony —
  just respond naturally.

---- END PASTE ----

## Provenance and maintenance

Authored 2026-07-11 from: the five-pointer draft (this repo's session history),
the llm-council verdict (sequencing + two repairs), architecture-contract
Decision 7 (retired governors reduced to standing principles). Updated
2026-07-12: pointer 4 added for brand-standard (David's directive: it is the
standard for all external document creation going forward). Updated 2026-07-15:
added the **"No silent defaults" law** to pointer 1 — owner-directed, motivated
by the 2026-07-15 cross-model path run (`results/2026-07-15/`), whose one durable
Sonnet↔Opus divergence was disposition on ambiguous behavior-changing calls (Opus
silently defaults; Sonnet surfaces-and-flags). **Empirical status: adopted owner
candidate, NOT validated** — the pre-registered A/B was run three ways (proxy,
terminal N=2, harder pilot N=3; see
`results/2026-07-15/no-silent-defaults-terminal-ab.md`) and the behavior proved
**saturated on top-tier models** (base surfaces the ambiguity with or without the
sentence), so no benefit was shown; it never regressed or over-fired, so it is
retained as cheap insurance, revert unforced. Also updated 2026-07-15: the opening line
was reworded from "four custom skills installed" to "four governance skills these
instructions steer" — a factual-accuracy fix (the owner's claude.ai carries
additional skills: frontend-design, pdf-extract, council, skill-creator); **no
behavioral/steering change**.

Updated 2026-07-15 (second edit, owner-directed after incident INC-8 in
`.claude/LESSONS.md`, transcript at `results/2026-07-14/rivian-incident-transcript.md`
— the Rivian analysis where Opus applied the governors "in spirit" without loading
any): two changes. (1) The fallback clause "If a skill fails to load, follow the
principle stated here anyway" was narrowed to **"The load is the procedure
(law)"** — the old clause made principle-compliance a legitimate substitute for
loading, a license *consistent with* the model's behavior in the incident (the
transcript shows it skipping loads and defending the skips as spirit-compliance;
it does not show the model *citing* the clause, so the causal link is inference,
not fact). (2) A **governance-receipt law** was added: one audit line on governed
deliverables naming which pointers fired or were skipped. **Neither change fixes
the incident's dominant causes** and this file does not pretend otherwise: the
incident was driven mostly by discretionary non-invocation on an uncued prompt
with no mid-answer tool juncture (INC-8 causes 2 and 4), and no prose edit on a
surface with no hook layer counters those. What these two edits do is narrower and
honest — the clause-narrowing removes a self-grading loophole; the receipt
converts skips *the model concedes* into visible ones (it does **not** convert
silent skips wholesale — a confabulated ✓ or a reply misfiled as "casual" stays
silent, so "audit aid, not proof"). Together they standing-order a weaker,
always-on version of the interrogation the owner ran manually in INC-8.
**Empirical status of both: adopted owner-directed candidates, NOT validated**
(same labeling discipline as the No-silent-defaults law above — but note that law
at least had zero-regression run data; these have no run data of any kind yet);
the A/B is pre-registered at
`experiments/hypothesis-2026-07-15-load-is-procedure.md` — validate or revert
there, one variable at a time. Self-report caveat: a load isn't externally
observable on claude.ai, so the receipt must be treated as testimony and
reconciled against the delivered artifact wherever one exists — the reconcile-
self-report-against-artifacts discipline of INC-5. The paste block measures ~4,190
characters (was ~2,880, measured via `awk '/BEGIN PASTE/,/END PASTE/' | wc -c` on
each version; the custom-instructions box has ample headroom — the 1024-char cap in
INC-3 is the *skill-description* limit, not this surface). **Re-paste owed** — paste this block into claude.ai so the settings
box equals this file (drift law). This is the second consecutive owner-directed
pre-evidence adoption (No-silent-defaults was the first); the maintenance-trigger
list below is amended to name that as a legal update class.

Re-verify: the settings box content equals the paste block (copy out, diff).
Update when: a governor is added/retired (Decision 5/7); the smoke test or a
gated wording experiment changes the winning text; claude.ai changes its
instructions surface; or **the owner adopts a candidate law ahead of its A/B**
(labeled NOT validated, with the pre-registration filed) — the case for both
2026-07-15 updates.
