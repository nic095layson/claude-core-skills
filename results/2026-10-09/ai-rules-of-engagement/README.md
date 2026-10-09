# Rules of Engagement for Operational AI — v1.0 (2026-10-09)

Owner-requested deliverable: a standardized, vendor-neutral "rules of engagement"
document in David's name, for presentation to his CEO. It generalizes this
library's governed order of operations (the GAUNTLET sequence) and the
handshakes and gates of the two fantasy-basketball repos into a standard any
AI-assisted workflow could adopt.

## Files

| File | What |
|---|---|
| `Rules-of-Engagement-Operational-AI_2026-10-09.docx` | The deliverable (13 pages, US Letter) |
| `Rules-of-Engagement-Operational-AI_2026-10-09.pdf` | Render of the .docx, for review and sending |
| `build_roe.js` | Generator (docx-js). Every claim in the document is a literal in this file; edit here, re-run `node build_roe.js` |

## Owner decisions recorded (2026-10-09, in-session)

- Deliverable: the rules-of-engagement document only (no one-pager, appendix pack, or deck).
- Sources: both fantasy repos, read in full where they carry instruction text.
- Positioning: **principles only, no vendor discussion.** No model or vendor is named in the document.
- "Resume" means a showcase of the system, honest about what is unmeasured.

## Revisions

- **2026-10-09, after v1.0 shipped:** Section 1 opens with a pull-quote of the
  owner's guiding principle, supplied by him in-session: "AI is a force
  multiplier. How can we use AI to solve faster, smarter, and to scale?"
  Verbatim except "Is" lowercased. Source per the owner: his own notes from an
  AI excellence seminar at Rivian. The seminar is deliberately **not** named in
  the document (principles-only decision above); add it if the owner asks. The
  sentence after the quote ("A multiplier works on whatever it is given…") is
  Claude's bridge, flagged to the owner to keep or cut. Pages 2-9 verified
  text-identical to the prior PDF.

- **2026-10-09, second owner note:** new **Section 2, Modernizing the
  Workflow**, built on the owner's notes: the four areas of context for an
  agent (Persona, Task, Context, Format), with his example ("You are a project
  manager…", "delivering a report to the CEO"), and "Workplace Intelligence and
  Knowledge Base" with his anchor question ("What are all the documents I have
  on ___ topic?"). Owner explicitly invited elaboration. Owner wording kept
  verbatim except two added articles ("a" project manager, "the" CEO). Everything
  else in Section 2 is Claude's elaboration, grounded in
  `fantasy-basketball-2026-27` `PROMPT.md` (persona, task, inputs file,
  deliverables spec, defaults listed as A1, A2…) and
  `instructions/claude-ai-project-instructions.md` (pull-first rule, Freshness
  Protocol step 5), both read this session at `00203c2`. **One elaboration has
  no basis in the repos:** knowledge-base rule 5, "Access follows the person, not
  the tool", added for the owner's industry and flagged to him. Sections 2-7
  renumbered to 3-8; every cross-reference updated and checked. Appendix A and B
  each gained rows for the new section. Document grew from 9 to 11 pages.

- **2026-10-09, third owner note:** Section 2 gained "Beyond finding
  documents" (his fragments "Generate insights on data across multiple
  documents" and "Data cleaning and charts") and a third subsection, **Agent
  Building: Skills**, built on his notes: "how does something work" with a
  four-step improvement loop (initial draft, investigate, find what works,
  CURATE) and three authoring rules (lead with description, keep main file
  lean, explain why, don't command). Owner wording verbatim apart from
  capitalization and punctuation ("Agent building - SKILLS" -> "Agent Building:
  Skills"; "investigate -" -> "Investigate:"; "Keep Main file" -> "Keep main
  file"). **Interpretation flagged to owner:** "Have agent write final tool call"
  read as "curation is the session's last action". **No repo basis:** the
  charts principle (no charting practice found; the repo "chart" hits are depth
  charts). Grounding read this session: the deck repo's two-outlet actuals
  record (`README.md`, `47deea3`); this library's skill-authoring standard,
  domain-reference (progressive disclosure), and the ledger. Counts measured
  2026-10-09: 21 modules, 21/21 with a do-not-use clause in the description,
  10 with a "Rules, each with its reason" section, 4 DEAD entries, 30 ledger
  entries. A cross-reference checker first reported four wrong targets; the
  checker was matching numbered list items as headings (adversarial-verify
  rule 9). Re-run against the source's H1 calls: all 17 references correct.
  Document grew from 11 to 13 pages.

## Sources read (commit at time of reading)

| Repo | Commit | Read |
|---|---|---|
| `nic095layson/claude-core-skills` | `11a760c` | plan-gate, adversarial-verify, scope-fence, gauntlet, architecture-contract, brand-standard, product-output; both instruction carriers; `hooks/README.md`; `.claude/LESSONS.md` INC-9, INC-11, INC-12, INC-13, WIN-2 |
| `nic095layson/fantasy-basketball-2026-27` | `00203c2` | `CLAUDE.md`, `README.md`, `INPUTS.md`, `PROMPT.md`, `DATA-PULL.md`, `instructions/claude-ai-project-instructions.md`, roster-audit postmortem |
| `nic095layson/yahoo-fantasy-basketball` | `47deea3` | `README.md`, both skills, `arena/README.md`, `LESSONS.md` lessons 1–12 |

## Counts in Section 8 (measured 2026-10-09; was Section 7 before the 2026-10-09 renumbering)

```
ls .claude/skills | wc -l                                              -> 21
grep -oE '^### (INC|DEAD|DRIFT|WIN)[^ ]*' .claude/LESSONS.md | wc -l   -> 30
ls experiments | wc -l                                                 -> 19
ls evals/*.json | wc -l                                                -> 20
# fantasy-basketball-2026-27
ls report/after-reports/*.md | wc -l                                   -> 84
grep -cE '^\| 20' report/pull-log.md                                   -> 70
ls report/check_*.py                                                   -> 3
# yahoo-fantasy-basketball
ls arena/results/debrief_*.md | wc -l                                  -> 49
grep -cE '^[0-9]+\. \*\*' LESSONS.md                                   -> 23
ls scripts | grep -E 'check|verify|build|freshness|range|identity|repeat|judgment' -> 8
```

All other figures in the document are quoted from the dated source entries
listed in its Appendix B, not re-measured here.

## Verification (adversarial-verify, this session)

- Built, validated (`validate.py`: all passed), rendered to PDF, and every page
  inspected as an image. Three render passes; defects fixed between them:
  a table split after one row, a heading stranded from its table, an
  out-of-order provenance row.
- Source check of every measured claim against its origin file. One correction
  made before render: the "about 83%" figure is 5 of 6 runs on a test harness,
  with 0 of 6 false triggers, not "the full sequence on qualifying tasks".
- Coverage check: Appendix B initially lacked origin rows for L9, Steps 2/5/7,
  H1, H7, H8. All added from their sources.
- Banned-vocabulary scan (brand-standard hard rules): none found.

## Not checked / bounds

- **Brand fonts.** Eurostile is commercial and not installed here. The .docx
  names Eurostile (display) and Poppins (body); the PDF was rendered with
  Poppins installed from Google Fonts and Eurostile mapped to Poppins SemiBold.
  On a machine without Eurostile, Word substitutes its own fallback for headings.
- **H8 date** is "by 2026-07-12": the shallow clone could not date the speed
  rule's first commit.
- Appendix A is illustrative and states so. Nothing about the owner's employer
  or its current AI system was available to this session or is claimed.
