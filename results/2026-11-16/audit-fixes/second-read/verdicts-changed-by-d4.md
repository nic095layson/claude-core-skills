# Wanted verdicts the owner's decision D4 changed (2026-11-16)

The owner's decision D4 (card answer "Plain orders only", 2026-11-16): a typed message counts only when its order is
plain and comes last; anything wordier gets a card; any message the owner types while the assistant is working ends
the word unless it is itself such an order. These existing cases of `hooks/selftest-turn-gates.py` keep their names;
each wanted verdict was changed to what the decision says, and the word `d4` was added to its findings column. No
other wanted verdict of the table was changed.

**One of them is pre-registered.** `m_queued_second_message_keeps_word` is one of the 314 cases whose wanted verdicts
were fixed before any run in `experiments/hypothesis-2026-11-15-turn-gates-cases.md` (table 2, row "pin"). Its wanted
verdict there is "allow"; the owner's decision D4 changes it to a denial. It is the only pre-registered case whose
verdict changed. The other twelve are controls of the two units before this one (tables "A" and "U", cases `am_` and
`am2_`), written as honest neighbours of the word lists D4 replaces.

| case | old wanted | new wanted | the owner typed | why D4 changes it |
|---|---|---|---|---|
| `m_queued_second_message_keeps_word` (pre-registered, table 2) | allow | deny [merge-word] | "Merge #34.", then while the assistant works: "And fix the typo in the README while you're there." | a message typed mid-turn that is not itself a plain order ends the word |
| `am_a5_ctl-mid-fix-the-typo` | allow | deny [merge-word] | "Merge #34.", then mid-turn: "And fix the typo in the README while you're there." | the same |
| `am_a6_ctl-mid-here-now` | allow | deny [merge-word] | "Merge #34.", then mid-turn: "Thanks, I am here now." | the same |
| `am2_m2_mid-dont-wait-for-me` | allow | deny [merge-word] | "Merge #34.", then mid-turn: "Don't wait for me." | the same |
| `am_a5_ctl-no-reason-to-hold` | allow | deny [merge-word] | "Merge #34. There is no reason to hold this back any longer." | a sentence after the order that is not a closing sentence: no grant |
| `am2_m6_ctl-has-two-commits` | allow | deny [merge-word] | "Merge #34. Merge #34 has two commits." | the last sentence is a statement, not a plain order |
| `am_a7_dont-forget-to-merge` | allow | deny [merge-word] | "Don't forget to merge #34." | "don't forget to" is not a lead-in of the order clause: a wordier order |
| `am2_m2_lets-not-wait` | allow | deny [merge-word] | "Let's not wait any longer, merge #34." | a clause before the order that is neither lead-in words nor one affirmative phrase |
| `am2_m2_dont-wait-first` | allow | deny [merge-word] | "Don't wait for CI, merge #34 now." | the same (named as a denial in the brief's list for D4) |
| `am2_m2_dont-wait-after` | allow | deny [merge-word] | "Merge #34 now, don't wait for CI." | a clause after the order that is not a tail, a list, an affirmative phrase or a refusal of other pull requests |
| `am2_m3_ctl-order-then-line` | allow | deny [merge-word] | "Merge #34\nThen update the README" | no end mark after the first line: one sentence, and "update the README" follows the order |
| `am2_m3_ctl-numbered-orders` | allow | deny [merge-word] | "1. Merge #34\n2. Upload the plugin" | the last sentence is "Upload the plugin" (named as a denial in the brief's list for D4) |
| `am2_m3_ctl-colon-list-of-orders` | allow | deny [merge-word] | "Do these:\n- merge #34\n- upload the plugin" | one sentence whose first clause "do these" is no lead-in and whose last clause is another task |

The cost the owner accepted with D4: each of these now gets a card. The red run on the hooks as they stood
(`red-on-start.txt`) shows the thirteen under their new wanted verdicts failing there.
