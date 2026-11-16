# Breaks this unit rewrote, and the breaks it added (2026-11-16)

**After this unit, all 571 breaks are caught and the control is clean (`mutations-after.txt`). 57 breaks are new
(DR01 to DR57). Fifteen older breaks were rewritten: thirteen because their text was gone, two because they
survived the new rules.** In every rewrite the rule the break removes is the same rule as before. Only the text it
replaces moved, or the case that catches it changed.

| break | why it changed | now |
|---|---|---|
| RC48 | the header test became an `elif` (header rows that hold a date come first) | the same break on the `elif` line |
| RE61, RE62 | the count of runs now also reads a number in words and one word in between | the same breaks on the new text |
| AR03 | `MEANS_END` now also ends what was not verified at a number in words | the same break on the new text |
| AR12 | the bare-"tried" rule is a lookahead built from `TRIED_NAMES_NOTHING` | "tried" put back as a plain word: caught by `ar_r5_fk11...` |
| AR13 | "claim" is no longer in `EXAMPLE_TABLE_WORDS` | test / case / input added at the head of the tuple |
| AR15 | a tally's label may stand in any cell | the count test on the new expression |
| AR16, AR17 | the work-as-subject rule now needs a verb of verifying and reads five words | the same two rules on the new lines |
| AR20 | the passive's agent is tested by `_other_agent` | the same break on the new call |
| AR21 | "by me" is a claim without `NOT_AGENTS` now (no plural), so dropping "me" and "us" changed nothing and the break SURVIVED | drops "ourselves", caught by the new case `dr_e4_by-ourselves` |
| AR24, AR25, AR26 | a card, a Skill call and a notification read are no longer named in the code: any call that is not a look-up leaves the text judged | each one is added to `NOTE_TOOLS`, which turns it into a look-up |
| AR27 | `BLOCKED_STOP_ENDS_ANSWER = False` SURVIVED: the old case follows the blocked stop with a Skill call, which judges the text anyway | its case is now `dr_e1_answer-of-a-blocked-stop-then-a-look-up`, where a Bash call follows the blocked stop |

New: DR01 to DR07 cover which texts are judged (E1, DR-7). DR08 to DR15 cover the table-of-examples words in both
directions (E2). DR16 to DR24 cover the work as subject (E3). DR25 to DR30 cover the passive's agent (E4). DR31 to
DR35 cover "tried" (E5). DR36 to DR45 cover numbers in words, tally cells and header rows of data (E6). DR46 and DR47
cover `NOMINAL_REACH` both ways (E7). DR48 to DR51 cover the elliptical claim (E8). DR52 to DR57 cover the merge
gate's brackets, and DR53 puts back "any bracket is a label".
