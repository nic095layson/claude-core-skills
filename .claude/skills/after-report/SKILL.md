---
name: after-report
description: >-
  The house format for analysis and evaluation reports — dated results/
  artifact, method and verification stated up front, verdict tiers, every
  load-bearing claim carrying dated evidence marked EVIDENCE or INFERENCE,
  primary sources outranking blogs, bounds stated plainly, and next steps left
  as owner decisions. Use when asked to produce a substantial written analysis,
  evaluation, comparison, or investigation report — trigger phrasings:
  "provide a report", "write up the findings/analysis", "expert dive",
  "analyze X and report back", "evaluate these options for me", "after-report"
  — and when fact-checking an external claim (a blog post, a tweet, a vendor
  page) that a report or decision will rest on. Do NOT use for ordinary
  conversational answers or quick questions (no ceremony — just answer), for
  verifying your own finished deliverable (adversarial-verify), for the
  planning that precedes the analysis (plan-gate), or for recording a
  diagnosis (the project ledger owns that).
---

# After-Report

A report is trusted for its method, not its prose. This library's major
analyses converged on one shape — evidence dated, verification shown,
decisions left to the owner — and that shape previously survived only by each
session imitating the last report. This skill makes the format procedure, so
any model on any surface produces reports in the shape the owner already
trusts, instead of reinventing one. The format IS the rigor: a fluent report
without dated evidence is an opinion with headings.

## Terms (defined once)

- **Load-bearing claim** — a claim the report's verdict or the owner's
  decision would change if it were false.
- **EVIDENCE / INFERENCE** — a claim directly supported by a checked source
  (quote, command output, measurement) versus your reasoning from evidence.
  Both are legitimate; presenting the second as the first is the defect.
- **Primary source** — official docs, source code, changelogs, specs, or your
  own measurements. Blogs, posts, and summaries are leads, never evidence.

## The report contract

### 1. Placement and header

A substantial report is a dated artifact: `results/<YYYY-MM-DD>/<topic>/REPORT.md`
in the governing repo (or the requesting project's convention if it has one —
instance wins). The header states, in order: the owner's request (near
verbatim), what was analyzed (with versions/commits/dates), the method
including what verification ran, and a one-paragraph headline a reader could
act on without reading further.

### 2. Evidence rules (non-negotiable)

- Every load-bearing claim carries its evidence inline or beside it: file path
  + quote, command + output, or source URL + fetch date.
- Volatile facts carry dates ("codex not on PATH, verified 2026-08-03"), and
  measured rates stay rates — never rounded to "always" or "never".
- External claims get the claim-check (below) before they appear as anything
  but a lead. Mark EVIDENCE vs INFERENCE wherever a reader could confuse them.
- Raw supporting artifacts (agent outputs, transcripts, JSON) are committed
  beside the report, not summarized away.

### 3. Verdicts, tiered

When the report grades options or candidates, use explicit tiers the owner can
veto line-by-line (the house set: MUST ADD / HIGHLY RECOMMEND / NICE TO HAVE /
NOT NEEDED / fold-don't-add — adapt labels to the domain, keep the monotonic
order). Every high tier states what evidence would have demoted it; a verdict
that nothing could change is not a verdict.

### 4. Bounds, stated plainly

One section on what the analysis did NOT cover and what was single-pass,
sampled, or assumed — silent truncation reads as "covered everything." Include
what you could not see (e.g., "chat history from other sessions is not
visible; 'history' here means what the repo records").

### 5. Next steps as owner decisions

Recommendations end as a decision sheet, not as actions taken: the report
proposes, the owner disposes. Anything already executed during the analysis is
reported as done with its evidence — never mixed into the proposal list.

### 6. Provenance

Last section: who/what produced the report (session, workflow runs, token
costs where known), sources cited, and the re-verification pointers for its
volatile claims.

## The claim-check (for external claims)

1. Treat the claim as a lead, whoever states it, however often repeated.
2. Find the primary source: official docs, the actual repo, the spec, or a
   measurement you run yourself. Quote it verbatim, dated.
3. Grade the claim SUPPORTED / UNSUPPORTED / PARTIAL — and say which parts are
   which; most viral claims are PARTIAL, and the true kernel matters as much
   as the false frame.
4. Spot-check borrowed verification: when another agent or source did the
   checking, re-fetch the 1–3 most load-bearing quotes yourself before the
   report rests on them.

## Proportionality (the anti-ceremony valve)

A quick question gets an answer, not a report — this skill fires on a request
for a *report*, not on every analysis-shaped sentence. Small-but-real
analyses may deliver the contract in one page: header, evidence-with-dates,
bounds, decisions. Length is not rigor; the contract's parts are.

## Volatile facts (dated)

- Authored 2026-08-03; UNMEASURED — candidate until first invoked uses are
  graded against this contract (`evals/after-report.json`, register row 9).
  *candidate*
- The house tier labels and `results/<date>/<topic>/` convention are as
  practiced in `results/2026-07-13/` and `results/2026-08-03/`. *verified*

## When NOT to use this skill

- Ordinary questions and conversation → just answer (see Proportionality).
- Verifying your own deliverable before handing it over →
  **adversarial-verify** (a report about work is still graded by it).
- Planning the analysis itself → **plan-gate**.
- Wording-experiment records → **research-methodology** owns that artifact
  shape (`experiments/hypothesis-*.md`).
- Costly-diagnosis records → the project ledger (`.claude/LESSONS.md`).

## Provenance and maintenance

Authored 2026-08-03 by the Fable 5 session of
`results/2026-08-03/skill-proposals/` (proposal 3, owner-approved).
Codifies the format practiced in `results/2026-07-13/external-skill-analysis/REPORT.md`
and `results/2026-08-03/sol-skill-analysis/REPORT.md`; the claim-check
generalizes the 2026-08-03 fallback fact-check (blog claim reversed by
`code.claude.com/docs/en/model-config.md` — the worked example). EVIDENCE/
INFERENCE marking is convergent practice from externally evaluated research
contracts (evaluated 2026-08-03, ideas only, no text vendored). The
evidence-strict and rates-stay-rates laws restate architecture-contract
invariants 1 and 7 in report form.

Re-verify: precedent reports present — `ls results/2026-07-13/ results/2026-08-03/`;
eval set present — `ls evals/after-report.json`. Update when: a report ships
that the owner corrects on format (fold the correction in, dated), or the
results/ convention changes.
