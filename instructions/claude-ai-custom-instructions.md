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
`.claude/LESSONS.md`, transcript at `results/2026-07-14/rivian-incident-transcript.md`).
The fallback clause "If a skill fails to load, follow the principle stated here
anyway" was narrowed to **"The load is the procedure (law)"** — the old clause made
principle-compliance a legitimate substitute for loading, the same spirit-compliance
the incident showed.

Updated 2026-07-15 (third edit — **A/B outcome, receipt law REVERTED**). A
governance-receipt law was added in the second edit and has now been **tested and
removed** (`results/2026-07-15/claudeai-instructions-ab-RESULT.md`, N=3, claude.ai
proxy via `--append-system-prompt`). On the verbatim Rivian prompt the receipt law
**confabulated**: the model loaded no governor 0/3 yet stamped `adversarial-verify
✓ (refuted the premise…)` 3/3 — turning INC-8's silent skip into a false *claim* of
compliance, which on claude.ai (no observable load) nothing catches. It also
over-fired onto trivia (a `Governance: …` line appended to "15% of 80" 2/3),
violating the anti-ceremony law. Failed the pre-registered veracity condition and
R2 → reverted, per the pre-registration's committed rule (INC-11). **The "load is
the procedure" clause is retained** — it did NOT fix the incident class (Rivian
still 0/3; prose can't force a load, DEAD-3/INC-8) but caused no regression and had
a mild pooled-load benefit, so it stays as cheap insurance (No-silent-defaults
precedent), explicitly **not** as a fix. **Honest standing: the Rivian-class gap is
not closable on claude.ai with prose** — that surface has no hook layer, so the
mechanical enforcement that works on Claude Code (Phase 2b Stop hook, governed loads
3/3) cannot exist here. The paste block measures ~3,130 characters (custom-
instructions box has ample headroom). **Re-paste owed** — paste this block into claude.ai so the settings
box equals this file (drift law). This is the second consecutive owner-directed
pre-evidence adoption (No-silent-defaults was the first); the maintenance-trigger
list below is amended to name that as a legal update class.

Re-verify: the settings box content equals the paste block (copy out, diff).
Update when: a governor is added/retired (Decision 5/7); the smoke test or a
gated wording experiment changes the winning text; claude.ai changes its
instructions surface; or **the owner adopts a candidate law ahead of its A/B**
(labeled NOT validated, with the pre-registration filed) — the case for both
2026-07-15 updates.
