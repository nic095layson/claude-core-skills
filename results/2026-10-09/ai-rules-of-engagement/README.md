# Rules of Engagement for Operational AI — v1.0 (2026-10-09)

Owner-requested deliverable: a standardized, vendor-neutral "rules of engagement"
document in David's name, for presentation to his CEO. It generalizes this
library's governed order of operations (the GAUNTLET sequence) and the
handshakes and gates of the two fantasy-basketball repos into a standard any
AI-assisted workflow could adopt.

## Files

| File | What |
|---|---|
| `Rules-of-Engagement-Operational-AI_2026-10-09.docx` | The deliverable (9 pages, US Letter) |
| `Rules-of-Engagement-Operational-AI_2026-10-09.pdf` | Render of the .docx, for review and sending |
| `build_roe.js` | Generator (docx-js). Every claim in the document is a literal in this file; edit here, re-run `node build_roe.js` |

## Owner decisions recorded (2026-10-09, in-session)

- Deliverable: the rules-of-engagement document only (no one-pager, appendix pack, or deck).
- Sources: both fantasy repos, read in full where they carry instruction text.
- Positioning: **principles only, no vendor discussion.** No model or vendor is named in the document.
- "Resume" means a showcase of the system, honest about what is unmeasured.

## Sources read (commit at time of reading)

| Repo | Commit | Read |
|---|---|---|
| `nic095layson/claude-core-skills` | `11a760c` | plan-gate, adversarial-verify, scope-fence, gauntlet, architecture-contract, brand-standard, product-output; both instruction carriers; `hooks/README.md`; `.claude/LESSONS.md` INC-9, INC-11, INC-12, INC-13, WIN-2 |
| `nic095layson/fantasy-basketball-2026-27` | `00203c2` | `CLAUDE.md`, `README.md`, `INPUTS.md`, `PROMPT.md`, `DATA-PULL.md`, `instructions/claude-ai-project-instructions.md`, roster-audit postmortem |
| `nic095layson/yahoo-fantasy-basketball` | `47deea3` | `README.md`, both skills, `arena/README.md`, `LESSONS.md` lessons 1–12 |

## Counts in Section 7 (measured 2026-10-09)

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
