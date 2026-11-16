# The receipt gate read against ordinary prose, before and after this unit (2026-11-16)

**On the two bodies of prose the builder had not read, the gate now blocks 22 sentences (25 before); by my reading
11 are true bare claims, 8 are false blocks and 3 are borderline.** The grammar was not tuned on these two bodies
beyond the unit's rules R1 to R5; what is still blocked wrongly is listed below by class and stated as a limit in
`hooks/README.md`.

Method, stated before the runs: the committed tool `results/2026-11-15/receipt-gate-fix/prose_scan.py` (each
file read as one answer text with the gate's own sentence cutter, claim families and receipt test; every bare
claim listed, not only the first) and `prose_probe.py`, run with `--hooks` set to the hooks as this unit found
them (commit 7a5f978, "before") and to the hooks of this unit ("after"). The working note rule (R2) decides
which texts of a stop are judged; a file is one text, so the scan does not see it.

    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md --sentences <repository Markdown at fc3539f>
    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md,txt --sentences <audit pack>/pack <audit pack>/work
    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md,rst,txt --sentences /opt /usr/local/lib /usr/lib/python3/dist-packages
    python3 results/2026-11-15/receipt-gate-fix/prose_probe.py --hooks <hooks>
    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md --sentences <audit pack>/kit-full
    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md --sentences <audit pack>/deck-full

## 1. Totals

| body | files (distinct) | sentences before -> after | standing claims before -> after | **blocked before -> after** | false blocks after (whose reading) |
|---|---|---|---|---|---|
| this repository's Markdown at fc3539f (the first build's body 1) | 209 | 10,384 -> 11,008 | 29 -> 30 | **9 -> 9** | 0 (the same 9 sentences the first build judged true bare claims) |
| the audit's briefs and reports, `pack/` and `work/` (body 2) | 880 | 18,975 -> 19,145 | 47 -> 48 | **17 -> 17** | 0 (the same 17; first build's judgement) |
| documentation of installed tools (probe 3) | 1,540 | 86,715 -> 86,733 | 3 -> 3 | **0 -> 0** | - |
| four hand-written lists, 199 ordinary sentences and 47 bare claims (probe 4) | - | - | - | **8 -> 7 of 199** ordinary; 2 -> 2 of 47 bare claims let through | the 7 are the first build's stated limits |
| **the domain kit, `kit-full` (new: the builder had not read it)** | 357 | 36,856 -> 39,164 | 43 -> 43 | **25 -> 22** | **8 false, 3 borderline, 11 true (mine)** |
| **the season deck, `deck-full` (new)** | 105 | 7,749 -> 7,809 | 1 -> 1 | **0 -> 0** | - |

More sentences are read after the change because a table headed Test, Case, Input, Expected or Verdict is no
longer a table of examples (R3): its rows are now sentences. Probe 4's one change: "The license terms cannot be
verified by a machine, so the checklist sends them to legal." now passes (a passive whose agent is somebody
else, R5).

## 2. The domain kit, every blocked sentence, judged

Before -> after: four left the list, one joined it.

| left the list | why |
|---|---|
| `\| Unconfirmed \| 0 \|` (a roster audit's tally table) | a count, not a claim (R3) |
| "... UNVERIFIABLE from the state file; the export carries no build stamp." | "from the state file" names the source (lead) |
| "Waiver players vs free agents: UNVERIFIABLE from the kit's records." | "from the kit's records" names the source (lead) |
| "I didn't find an official box score, so exact minutes for Lillard and Holiday remain unconfirmed." | "didn't find" names a failed attempt (lead) |
| **joined**: the Lonzo Ball row of a search table headed `player \| query run (2026-10-13) \| dated finding \| verdict` | "verdict" no longer makes a table of examples (R3); the row's attempt is the quoted query, and quoted words are no receipt |

The 22 blocked after the change (file names under `kit-full/report/after-reports/` unless given; a connector's
name and a web site's name are replaced by `<connector>` and `<a news site>`):

| # | file | sentence (shortened where marked ...) | my reading | class |
|---|---|---|---|---|
| 1 | `after-report-2026-07-27.md` | I could not determine whether that was an oversight or a deliberate exclusion (...). | true bare claim | - |
| 2 | `after-report-2026-08-13.md` | The weakest parts of this report, in order: ..., and the two FA rows I could not verify at all (§4). | true bare claim | (receipt in another section) |
| 3 | `after-report-2026-08-25-live-mock-49.md` | Cannot be confirmed - see Bounds. | true bare claim | - |
| 4 | `after-report-2026-08-26.md` | CANNOT VERIFY. | true bare claim | - |
| 5 | `after-report-2026-09-02.md` | `\| Cam Whitmore \| traded ..., now a UFA \| CANNOT VERIFY closed - he is on no pool row, so correctly absent \|` | **false block** | a status label of an item that is closed, with its reason in free words |
| 6 | `after-report-2026-09-15.md` | DRAFT DATE SET: Tuesday 2026-10-14, 7 PM owner-local (timezone unconfirmed - worth stating once). | true bare claim | - |
| 7 | `after-report-2026-09-15.md` | Draft-time timezone is unconfirmed. | true bare claim | - |
| 8 | `after-report-2026-09-28.md` | CANNOT VERIFY: Giannis Antetokounmpo [quoted] appears only as a CBS injury-tracker line with no article behind it, and Miami's 9/28 media-day coverage mentions no health concern - no action. | **false block** | the attempt and its result in free words ("appears only as", "mentions no") |
| 9 | `after-report-2026-10-13-scope-fence.md` | The governors' load state before 2026-09-23: UNVERIFIABLE here. | true bare claim | - |
| 10 | `after-report-2026-10-13-uploads.md` | And the Bleacher Report piece, which I cannot reach from here; paste it and it becomes a role-context source ... | true bare claim | - |
| 11 | `after-report-2026-10-13.md` | `\| Lonzo Ball \| [quoted]; [quoted] \| 2024 - 25 items only (...; a 2026-27 team option noted by NBA.com in 2025, its exercise unconfirmed); no signing on the ledger \| HELD, unsigned \|` | **false block** (new) | a search table: the attempt is in the header ("query run") and a quoted query |
| 12 | `after-report-2026-10-15-co-gm-settings.md` | The schedule runs change the draw order, so they cannot be verified that way. | **false block** | a statement about a method, its reason in free words |
| 13 | `after-report-2026-10-19-season-deck.md` | ... whether that fresh session holds the Artifact tool is UNVERIFIABLE until it runs (...). | borderline | "unverifiable until <an event>": not yet, not cannot |
| 14 | `after-report-2026-10-21-<connector>.md` | Whether the runner's session has the `<connector>` tools: UNVERIFIABLE from this session. | true bare claim | - |
| 15 | `after-report-2026-10-21-gauntlet.md` | The cause stays unverified. | true bare claim | - |
| 16 | `after-report-2026-10-21-gauntlet.md` | Whether the daily cron fire lands in the runner: UNVERIFIABLE until 2026-10-22 12:53Z. | borderline | "unverifiable until <a time>" |
| 17 | `after-report-2026-10-21-pickups-file.md` | How much leaving Drummond out of the season simulation moves the title odds: UNVERIFIABLE with the simulator as it is. | **false block** | the means named and why it cannot settle it, in free words ("as it is") |
| 18 | `after-report-2026-10-21-week-matchup.md` | The card's to-date totals against Yahoo's scoreboard: UNVERIFIABLE in this session. | true bare claim | - |
| 19 | `after-report-2026-10-21-week-matchup.md` | A live pickup scan ...: UNVERIFIABLE until 2026-10-24, because those box scores don't exist yet. | **false block** | a reason in free words ("don't exist yet" is not on the failure list; "doesn't exist" is) and a time |
| 20 | `after-report-2026-10-21-zscore-assessment.md` | How the five sources split the observed spread: UNVERIFIABLE with this file, which holds one team's totals with no weekly rosters. | **false block** | the source named and why it cannot settle it, in free words |
| 21 | `usage-2026-10-13/web_checks_2026-10-13.md` | Caveat on sources: The Miami trade and ... claims come from `<a news site>`, a site I can't verify as reliable. | borderline | an idiom of doubt about a source ("can't vouch for") |
| 22 | `usage-2026-10-13/web_checks_2026-10-13.md` | Digest (verbatim): "I couldn't find any 2026 reporting on Joel Embiid's knee or preseason status. | **false block** | a quotation the reader does not close (it runs on past the sentence): reported speech read as the assistant's |

Classes of the 8 false blocks: a reason or result in free words (#5, #8, #12, #17, #19, #20: 6), the attempt
named only in a table header and a quoted query (#11: 1, new with R3), an unclosed quotation (#22: 1). The 3
borderline: "unverifiable until <time or event>" (#13, #16: 2), an idiom of doubt (#21: 1).

The season deck (`deck-full`): 7,809 sentences, one standing claim, which carries its receipt; nothing blocked
before or after.
