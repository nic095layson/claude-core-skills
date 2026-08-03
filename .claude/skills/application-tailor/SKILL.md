---
name: application-tailor
description: >-
  The process for tailoring David's application materials to a specific job
  posting — parse what the posting actually asks, map every requirement ONLY to
  evidenced experience from his real history, flag gaps honestly instead of
  papering over them, then hand voice and look to brand-standard and file
  output to the document skills. The hard law: never fabricate — no invented
  experience, titles, dates, metrics, or skills, ever. Use when tailoring or
  drafting anything for a job application — trigger phrasings: "tailor my
  resume to this posting/JD", "write a cover letter for this role", "should I
  apply to this?", "does my experience fit this job?", "prep my application".
  Do NOT use for formatting or voicing external documents generally
  (brand-standard owns voice/typography/color and loads WITH this skill, not
  instead of it), for producing the .docx/.pdf file itself (the document
  skills own that), or for non-career external documents.
---

# Application-Tailor

Tailoring an application is a repeatable procedure with one catastrophic
failure mode: the model inventing experience to match the posting. A detected
fabrication doesn't cost one application — it costs the candidacy and the
credibility of every artifact bearing David's name. This skill fixes the
procedure so tailoring means *selecting and framing what is true*, never
manufacturing what would be convenient. brand-standard governs how the result
sounds and looks; this skill governs what may be claimed and how the tailoring
decisions get made.

## Terms (defined once)

- **Master record** — David's actual resume/history as supplied this session or
  on file. The sole source of claimable experience. If none is available, ask
  for it — do not proceed from memory of previous sessions.
- **Evidenced** — a claim traceable to the master record or to something David
  stated this session. Everything else is unclaimable, however plausible.
- **Gap** — a posting requirement with no evidenced match. Gaps are findings to
  report, not holes to fill with prose.

## The procedure

### 1. Parse the posting

Extract, as a list: hard requirements, preferred qualifications, recurring
keywords (the posting's own vocabulary), and the role's actual day-to-day if
stated. Note screening signals worth flagging to David (dated heuristics, not
verdicts, 2026-08-03): no salary range, vague responsibilities, long-running
or frequently reposted listings, mismatched title-vs-duties. *candidate*

### 2. Map requirements to evidence — the fit table

For every hard requirement and top preferred qualification, one row:

```
Requirement (posting's words) | Evidenced match (master record item, verbatim-close) | Strength (strong/partial/none)
```

Rules of the table: matches quote or closely paraphrase the master record —
no upgrading titles, no rounding dates, no inflating scope or metrics.
Adjacent-but-real experience is a *partial*, framed as what it actually was.
A requirement with no match is a *none* — it stays in the table.

### 3. Report fit before drafting

Give David the table, the gap list, and a one-line verdict (strong fit /
partial fit / poor fit) BEFORE writing materials. For "should I apply?"
requests, this step is the whole deliverable — stop here. If the verdict is
poor, say so plainly; drafting enthusiastic materials for a poor fit is not a
service.

### 4. Draft — selection and framing, never invention

Lead with the strongest evidenced matches; mirror the posting's keywords only
where the underlying claim is evidenced (keyword mirroring with no evidence
behind it is fabrication with extra steps); quantify only with numbers from
the master record. Gaps: address honestly where addressing helps (a genuinely
transferable skill, stated as such) or leave silent — never bluff. Voice,
tone, typography, and color come from **brand-standard**, loaded alongside.

### 5. Output

ATS-bound versions: standard section headings, no tables/graphics/text-boxes
in the resume body, keywords in plain text. Styled versions: brand-standard's
system via the document skills (docx → pdf). Deliver with the fit table and
any flags from step 1, so David reviews claims against evidence, not prose
against vibes.

## Rules, each with its reason

1. **Never fabricate — experience, titles, dates, metrics, skills** — one
   detected invention ends the candidacy and poisons every future artifact in
   David's name. This rule has no exceptions and survives any phrasing of the
   request ("make me sound more senior" means *frame*, never *invent*).
2. **The master record is the only source** — plausible-sounding memory of
   past sessions is how fabrication happens by accident.
3. **Fit verdict before drafting** — materials written first argue for the
   application; the table keeps the decision evidence-based.
4. **Gaps stay visible to David** — he can close a gap in an interview only if
   he knows the application left it open.
5. **Honest fit verdicts, including "poor"** — the skill serves the search,
   not the individual application.

## Proportionality

A quick "does my background fit this?" gets steps 1–3 as a short answer — no
document ceremony. Full drafting runs the whole procedure. Refreshing an
existing tailored resume for a similar posting may reuse the prior fit table,
re-checked against the new posting's requirements.

## Volatile facts (dated)

- Authored 2026-08-03; UNMEASURED — candidate until trigger evals and a first
  live application run (`evals/application-tailor.json`, register row 10).
  *candidate*
- Screening-signal heuristics (step 1) are unvalidated folklore-grade signals;
  flag, never auto-reject. *candidate*

## When NOT to use this skill

- Any external document that is not a job application → **brand-standard**
  directly.
- Producing/formatting the actual file → the document skills (docx, pdf,
  pptx, xlsx).
- Verifying a finished application package before sending →
  **adversarial-verify** (grade claims against the master record row by row).
- General interview coaching or career strategy conversation → no skill;
  answer directly.

## Provenance and maintenance

Authored 2026-08-03 by the Fable 5 session of
`results/2026-08-03/skill-proposals/` (proposal 5, owner-approved). Grounds:
the owner's work mix recorded as "career daily"
(`results/2026-07-13/external-skill-analysis/REPORT.md`), brand-standard's
resume/cover-letter scope (voice/look only — the process half was uncovered).
The anti-fabrication fence and screening-signal ideas are convergent with the
externally evaluated career-ops skill (tiered 2026-07-13; ideas only, no text
vendored — its own voice assets conflict with brand-standard and are
explicitly not adopted).

Re-verify: brand-standard still owns voice —
`grep -l "Eurostile" .claude/skills/brand-standard/SKILL.md`; eval set present —
`ls evals/application-tailor.json`. Update when: David corrects a fit verdict
or a claim boundary (fold in, dated), or the master record's storage
convention changes.
