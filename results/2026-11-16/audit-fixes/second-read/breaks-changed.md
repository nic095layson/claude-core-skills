# The break list after D4 and the second outside read (2026-11-16)

`hooks/selftest-mutations.py` before this unit: 462 breaks. After: 514, every one caught, none stale
(`mutations-after.txt`). On the tree as it was after the code change and before the list was edited, 17 breaks
survived and 38 were stale: the grant path of the word lists was replaced by the D4 grammar, so the breaks that
pinned it either lost their text or no longer changed a verdict.

## Deleted: they pinned code that D4 removed (15)

| break | the rule it pinned | why it goes |
|---|---|---|
| CD06 | "Merge after the audit" on a card is not the word to merge now (`DEFER_CUE`) | the list is gone; a card option is read by the plain-order grammar, whose tail rule is pinned by WD13 (cases `d4_n35`, `d4_n34`) |
| AM01, AM02, AM03 | "provided", "unless", a weekday put an order under a condition (`CONDITION_WORDS`) | `CONDITION_WORDS` is gone: an order is followed only by allowlisted tail words (WD13) |
| AM55, AM56, AM57 | "eventually"/"soon", a part of the day, a clock time put an order off (`CONDITION_WORDS`, `CONDITION_CLOCK`) | the same |
| AM06, AM07 | reported speech (`REPORT_CUE`) or a hold before the order holds it back | a clause before the order must be lead-in words (AM05, rewritten) |
| AM59 | a clause that puts something first holds back the order after it (`SEQUENCE_*`) | the same |
| AM18, AM19, AM21 | a yes on a question that offers a choice, holds a condition, or whose verb is followed by a statement grants nothing (`QUESTION_DOUBT`, `CONDITION_CUE`, the statement test of a question) | a yes needs a plain order question (AM17, rewritten) |
| AM53, AM54 | a line with a condition and no end mark goes on; list items under a colon are read with that line (`_line_goes_on`, `LIST_ITEM`) | a line break ends a sentence only after `.`, `!`, `?` (AM52, rewritten) |

Not added as breaks, with the reason: the auditor's N26 (a line with a hold and no end mark) pins `_line_goes_on`,
which is deleted; N27 ("still" as a statement word) no longer changes a verdict, because the grant path does not
read `STATEMENT_WORDS` (the case `d4_n31-still-fails` holds the verdict). N22 and N31 changed no verdict in the
second read either.

## Rewritten for the new code (same id, new text; the rule is the same or its D4 form)

WD05, WD10, WD13, WD14, CD07, CD08, CD09, CL22, AM04, AM05, AM11, AM12, AM14, AM17, AM22, AM23, AM40, AM41, AM52,
AM60, AS07, AS08, AS15. Cases named again (text unchanged, the old named cases no longer catch it alone): SC05, WD01,
WD02, WD06, WD07, WD08, WD15, WD16, WD17, CD02, CD11, AM08, AM09, AM10, AM13, AM15, AM51, AM58, AM61.

## New (67)

- DA01 to DA23: the D4 grammar (the length cap, closing sentences, refusals of other pull requests, lists after the
  order, affirmative clauses, words before a number, a refusal word in the list, the bracket, "let's", object words,
  free text typed into a card, a yes label's tail, a push order naming a pull request, the question's last sentence,
  the closing loop, the polite form, the count words of a card option; every word of `REFUSAL_START` reaches the revoking path).
- DB01 to DB14: the shell routes of DM-1, DM-6, DM-7, DM-8 (standard input, `cat FILE |`, `-s`, `/dev/stdin`, `+`
  options, `+o NAME`, `$PWD`, `$(pwd)`, `cp`/`mv`/`cat A > B`, body files from the written-file memory, wget).
- DB15 to DB30: the sixteen breaks of finding DM-10 that changed a verdict (N01, N03, N04, N05, N06, N08, N10, N11,
  N12, N13, N15, N16, N17, N18, N19, N21), each with the case that shows its verdict change (`d4_b5-...`).
- DC01 to DC14: the Stop gate: every block counts on a retry (DS-1), the idle note (DS-2, by time and by rows), the
  four denial leads and the leading blanks (DS-4, the auditor's MU03 to MU06), the "once" of the receipt gate and of
  the prompt-class rule (DS-5, MU18, MU19), the window of `HELPER_ACT_PLACED_BY_TIME = False` (DS-6, MU09), and the
  False path of `PROMPT_CLASS_SILENT_WITHOUT_OWNER_MESSAGE` (DS-7: the denied write, MU10, MU11, MU12).
