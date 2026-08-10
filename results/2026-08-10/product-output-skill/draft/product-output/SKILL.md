---
name: product-output
description: >-
  The finish-line standard for any final deliverable a session hands over —
  classify the deliverable and audience, route to the owning format and
  standards skills, build against a template, run the validate-fix-repeat loop,
  and deliver a real, dated file with a short delivery manifest — never a chat
  blob where a file was asked for. Use when a session is about to produce or
  hand over a product output — trigger phrasings: "make me a deck / report /
  one-pager", "produce the final version", "package this up", "ship it",
  "export as docx/pdf/xlsx", "deliverable" — and when choosing which format or
  pipeline a deliverable should use. Do NOT use for voice/look in the user's
  name (brand-standard), the analysis-report contract (after-report),
  correctness grading (adversarial-verify), format mechanics (the installed
  document/design skills), job applications (application-tailor), or email
  (correspondence) — this skill owns only the finish line: format choice,
  composition of standards, and handover.
---

# Product Output

Sessions produce good content and then fumble the last mile: the wrong format
for the audience, an applicable standard skipped, the output pasted into chat
instead of written to a file, an unnamed artifact, a single ungraded
generation pass. Each owning skill governs its own layer — none owns the
moment of handover, so delivery quality depends on which session you happened
to get. This skill makes the finish line a procedure: it routes to the skills
that own the layers and adds only the step nothing else owns.

## Terms (defined once)

- **Product output (deliverable)** — an artifact the user will keep, send, or
  act on outside this conversation: document, deck, spreadsheet, PDF, report,
  page, image. Chat answers, code edits inside a repo, and intermediate drafts
  are not deliverables.
- **Owning skill** — the installed skill that owns a format's mechanics or a
  standard's content. This skill routes to owners; it never restates their
  rules.
- **Delivery manifest** — the 3–6 lines handed over with the artifact: what
  was delivered, where, in what format, which standards applied, what
  verification ran, and what was not checked.

## Procedure

1. **Classify before building.** One line each: what artifact, who consumes
   it, in whose name it speaks, and which format serves that audience — not
   which format is easiest to emit. If the user named a format, that format
   wins; substituting another without saying so is a delivery defect.
2. **Route to the owners.** Compose, never duplicate:

   | The deliverable is… | Route to |
   |---|---|
   | External-facing or in the user's name | the personal brand standard (voice, typography, color) |
   | An analysis or evaluation report | the house report-format skill |
   | A .docx / .pptx / .xlsx / .pdf file | the installed document skill for that format |
   | A web page, dashboard, or chart | the installed design / dataviz skills |
   | Lane-specific (job application, email) | the lane's own skill |

   If an owning skill is absent in this environment, say so and state the
   fallback — never silently degrade to an ungoverned version.
3. **Fix the shape before generating.** Build against a template or a worked
   example of "good" — a template beats a prose description of one, and an
   example beats both. For a recurring deliverable type, reuse the last
   accepted instance as the template.
4. **Run the validate-fix-repeat loop.** Before calling anything done: open or
   render the actual file, run the format's validator where one exists, and
   check against the template. Fix and re-check until clean. One generation
   pass is a draft, not a deliverable.
5. **Verify, then hand over.** Grade the artifact against the task's success
   criteria (adversarial-verify where loaded — it owns the grading). Then
   deliver the real file: descriptive dated filename, placed per the project's
   convention where one governs (instance wins) or sent to the user directly,
   with the delivery manifest.

## Output format — the delivery manifest

```
Delivered: <file(s), path or attachment>
Format: <format, + why in one clause if not user-specified>
Standards: <which owning skills applied — or "none installed, fallback: …">
Verified: <what actually ran — render check, validator, grading>
Not checked: <bounds and assumptions, stated plainly>
```

## Rules, each with its reason

1. **The file is the deliverable.** Content pasted into chat when a file was
   asked for is undelivered work — files outlive conversations; scrollback
   does not.
2. **One format decision, stated.** Silent substitution (asked for docx,
   delivered markdown) converts a delivery into a surprise the user discovers
   later, when it is most expensive.
3. **Compose standards, never restate them.** A copied rule drifts the moment
   its owner is updated; a route cannot drift.
4. **Nothing ships on one pass.** Generation defects cluster at the finish —
   broken layout, dead formulas, placeholder text left in. The validator loop
   is where they die; skipping it ships them.
5. **Say what was not checked.** An unqualified "done" claims more than one
   session can know; the manifest's last line keeps the handover honest.

## Proportionality (the anti-ceremony valve)

This skill fires on the handover of a final artifact, not on every response.
Chat answers stay chat answers; drafts stay drafts; a quick "jot this into a
file" needs a filename and a sentence, not a manifest. For small deliverables
the manifest may be two lines — the parts that never drop are the format
decision and what was verified.

## Volatile facts (dated)

- Authored 2026-08-10 as a proposal candidate; UNMEASURED — no trigger or
  behavioral evals have run (eval set authored same day beside this draft;
  moves to `evals/product-output.json` on adoption). *candidate*
- Document skills (docx/pptx/xlsx/pdf) and frontend-design present in the
  authoring environment's personal scope (`ls ~/.claude/skills`, 2026-08-10).
  Per-environment fact — re-enumerate live before routing. *verified, that
  environment only*

## When NOT to use this skill

- How the artifact sounds/looks in the user's name → **brand-standard**.
- The analysis-report contract itself → **after-report**.
- Grading correctness before handover → **adversarial-verify** (step 5 calls
  it; this skill never grades).
- Format mechanics (building the docx/pptx/xlsx/pdf/page) → the installed
  document and design skills.
- Job-application tailoring → **application-tailor**. Email → **correspondence**.
- Planning the work that produces the artifact → **plan-gate**.

## Provenance and maintenance

Proposed 2026-08-10 by the session of
`results/2026-08-10/product-output-skill/REPORT.md` (owner-requested research:
"most powerful and best product output skill"). The validator-loop, template,
and examples patterns generalize Anthropic's published skill-authoring
doctrine (platform.claude.com best-practices, fetched 2026-08-10 — ideas only,
no text vendored). The route-to-owners table generalizes the finish line
application-tailor already practices for its one lane ("file output to the
document skills"). Rules 1 and 5 restate architecture-contract invariants in
delivery form.

Re-verify: installed format owners — `ls ~/.claude/skills` on the running
surface; survey claims — re-fetch per the REPORT's source list. Update when:
the install footprint changes materially, a delivery the owner corrects
reveals a missing route, or first measured use grades against this skill's
eval set.
