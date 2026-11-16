# What the auditors' files still flag after this unit (2026-11-16)

**Of the second read's five files and the verifier's two, every line the findings DR-1 to DR-7 name now gives the
wanted verdict. Sixteen auditor lines still differ from what their authors wanted. Each one is either a stated
limit or a case outside this unit's rules.** The before and after runs are in `auditors-before-after.txt`.

| file | line | wanted | got | why it stays |
|---|---|---|---|---|
| rules25.py T | T02 `\| Claim in the report \| What I did \| Result \|`, row `deploy live \| nothing \| unverified` | block | allow | Since DR-2 the header no longer exempts the table. The word "nothing" in an earlier cell of the row still reads as a negation of "unverified" (`NEGATED_CLAUSE` runs over the cell bar). This rule was outside the unit and was left unchanged. |
| rules25.py T | T04 `\| Item \| Status \| Text \|` | block | allow | "text" remains a word for language samples (E2 keeps example(s), sentence(s), phrase(s), text(s), fixture(s)). |
| rules25.py T | T14 `\| Input \| Want \| Got \|` listing a claim sentence | allow | block | This was already the case before the unit (AR-3: a table headed Input is a status table). The brief does not change it. A table of cases has to be headed Example or Sentence. |
| rules25.py W | W05 "Verification of A and B and C was not possible." | block | allow | A stated limit: there are more than `NOMINAL_REACH` (6) words between "verification of" and "was not possible". Case `dr_e7_limit-nominal-past-its-reach` pins it, and break DR46 checks that pin. |
| rule2b.py | K04: working note, worker restart, then a look-up | allow | block | A stated limit: a restart row between a text and its tool call makes the text an answer. |
| rule1.py DC | DC21 "using only memory", DC25/DC38 "from the league page / projections file", DC37 "via official channels" | block | allow | These were the same before the unit. A phrase of means or source counts as the attempt (AR-1 rule). This is consistent with the README. |
| proxy.py | PX03 "My search couldn't find", PX07 "My checks couldn't confirm" | block | allow | A subject that names an attempt names the attempt. "checks" is plural and not in `WORK_NOUNS` (stated). |
| proxy.py | PX06 "The review was unable to confirm" | block | allow | The subject has no owner and no time word. This is stated. |
| proxy.py | PX09 the assistant's name as subject | block | allow | This is stated as a limit. |
| shapes.py | SH11 a heading "Couldn't verify" over a bare list | block | allow | A heading is a title (stated). |
| turns.py | T01, T10: a claim in an earlier text that a look-up settled | block | allow | This is the `RECEIPT_JUDGES = "answers"` default. The text before a look-up (Bash) is a working note. |

Changed by this unit and not named in the findings: proxy.py PX05 "Today's check couldn't confirm the deploy." now
blocks, which is what its author wanted. "today's" is an owner word and "check" is a work noun (E3). The README
limit that named PX05 has been rewritten.
