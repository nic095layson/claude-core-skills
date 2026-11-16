# The 128 findings of the merge audit: where each one stands at ed8ef13 (2026-11-16)

**63 are resolved or decided here, 3 wait for the owner's plugin upload, 1 is a stated limit and 61 are left for
the second pull request. Only 53 of the 63 were re-run by an outside auditor.**

The outside audit of this pull request could not find a list of which findings it resolves (its claims auditor,
"not verified" line on the sentence "60 resolved or decided, 3 ready, 65 left"). This file is that list, built
from the records. It changes no finding and judges no fix again.

## Sources

- The 128 findings: the merge audit's index of findings (id, area, kind, title); that audit's record is in pull request 35, not in this tree.
- Which findings each outside auditor re-ran, and its status word for each: the regression lists of the outside
  audit (merge gate 25 ids, receipt gate 9, Stop gate 19, surfaces 10, claims 0) and each auditor's "Regression"
  lines. These re-runs were made at c3c8615, the head the outside audit read.
- The surfaces area (10 ids) was read by no outside auditor: the owner's card of 2026-11-16 (about 15:36 UTC) left
  the wiring, plugin, runbook, registry and guard area unread and open. For those rows the builder's evidence is named.
- The three commits after c3c8615 (077c860, 7a5f978, ed8ef13) fixed what the outside audit found. No outside auditor
  re-ran the 128 findings on them. At ed8ef13 the break list, run for this file, gives
  `== 462 breaks: 462 caught, 0 survived, 0 stale; control: 0 failing of 1062 cases ==` (6 min 52 s, 2026-11-16).

## States

| state | meaning |
|---|---|
| FIXED HERE | an outside auditor re-ran the finding's reproduction on this pull request; its status word is quoted |
| CHANGED BY AN OWNER DECISION | the re-run differs from the finding's wanted verdict because an owner decision changed the rule (D1 to D3 of 2026-11-13, the six answers Q1 to Q6 of 2026-11-15) |
| FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR | the builder lists it as resolved and has evidence; nobody else re-ran it |
| STATED LIMIT | the rule's miss stays and is written down as a limit |
| READY, CLOSES WHEN THE OWNER UPLOADS THE PLUGIN | fixed in plugin 0.1.6, which the account does not serve yet |
| LEFT FOR THE SECOND PULL REQUEST | not fixed here; moved by the owner's card of 2026-11-16 (about 03:35 UTC) |

The audit's index names no unit for any finding. The unit in the last state is taken from the five units that card
names (prompt side; registry rest, advisory hooks and guard gaps; outcome scripts; documents and claims; weekly
task prompt), by the finding's area: that placement is this file's, not a record's. Two groups fit none of the five
and are marked "none named".

## Every finding

| id | title (first clause) | area | state at ed8ef13 | basis |
|---|---|---|---|---|
| TB-1 | When the transcript holds no owner message, every turn gate is off | atk-turnboundary | **FIXED HERE** | merge-gate auditor: "fixed" |
| TB-2 | Any tool result containing the words "questions have been answered" is read as the owner's click, so showing the library's own test file, or a rela... | atk-turnboundary | **FIXED HERE** | merge-gate auditor: "fixed" |
| TB-4 | An owner message that only mentions a harness marker, or begins with a hook's own words, is dropped | atk-turnboundary | **FIXED HERE** | merge-gate auditor: "fixed" |
| TB-3 | A line of the notification-header form in any tool result starts a new turn | atk-turnboundary | **FIXED HERE** | merge-gate auditor: "fixed" for the merge part; the Stop-gate part was not judged by an outside auditor (builder's table cases F17, F18, F19a) |
| TB-5 | The receipt gate starts its turn at the last user row with string content, harness rows included, so it disagrees with the turn gates at 18 of 26 r... | atk-turnboundary | **FIXED HERE** | receipt-gate auditor: "fixed: 14/14" |
| TB-6 | Work started by a harness wake after the assistant has stopped still counts as the owner's earlier turn, so a click given for two pull requests kee... | atk-turnboundary | **CHANGED BY AN OWNER DECISION** | D2: "now DENY, as D2 decides" |
| TB-7 | The Stop gate's prompt-class half ignores the scheduled-run boundary | atk-turnboundary | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| TB-8 | The selftests pin little of the turn boundary | atk-turnboundary | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `hooks/selftest-mutations.py` (breaks whose origin names it); `results/2026-11-15/turn-gates-fix/mutations.txt`; 7 of its 9 surviving changes are named by a break; M8 and M9 (the old receipt gate's turn start) by none |
| F2-1 | A merge passes after the owner refuses it ("No, wait.", "Do not merge yet", a click on "Wait"), because the assistant's own earlier text naming the... | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed"; its control ctl3 (no number) is now denied by D1 |
| F2-2 | Once the word is typed or clicked, every merge passes until the owner types again | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed, 8/8 DENY" |
| F2-6 | The copy of the hooks that runs where the weekly task fires (account plugin 0.1.4) lets a scheduled run merge | atk-f2 | **READY, CLOSES WHEN THE OWNER UPLOADS THE PLUGIN** | `results/2026-11-16/surfaces-fix/after-the-merge.md` |
| F2-3 | Ordinary refusals and non-orders are read as the owner's word | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed, 23/23 DENY" |
| F2-5 | Ways to merge a pull request or to put a change on main that the gate never judges, in an owner turn and in a scheduled run alike | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed for routes 1-3 and 5-8"; route 4 (a script that is not on disk) is a stated limit |
| F2-4 | Any tool result that contains the words "questions have been answered" is taken as the owner's click | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed, 4/4 DENY" |
| F2-7 | When the transcript holds no owner message the hook exits before the merge check and every merge passes | atk-f2 | **FIXED HERE** | merge-gate auditor: "fixed, all DENY" |
| F2-8 | Honest merges are refused: a yes to "Shall I merge PR 34?" (number written without #), "No objections, merge it.", a click on "Yes, both (Recommend... | atk-f2 | **CHANGED BY AN OWNER DECISION** | D1, D2, the 2026-11-15 answer Q1 and the 2026-11-15 card-in-a-scheduled-run answer: "c and g ALLOW as required; the 10 mismatches are all changed by owner decisions" |
| RI-1 | The merge gate lets a merge through when the owner writes "Don’t merge yet" with a curly apostrophe, or "can't / cannot / shouldn't merge", or puts... | reimpl | **FIXED HERE** | merge-gate auditor: "fixed"; its control is now denied by D1 |
| RI-2 | The merge gate takes "merged" and "merging" for the owner's word, so a status question such as "Is #34 merged yet?" authorises a merge. | reimpl | **FIXED HERE** | merge-gate auditor: "fixed" |
| RI-3 | Any tool output that contains the phrase "questions have been answered" counts as the owner's click | reimpl | **FIXED HERE** | merge-gate auditor: "fixed" |
| RI-4 | The owner's word is not tied to the merge it is used for | reimpl | **FIXED HERE** | merge-gate auditor: "fixed" |
| RI-5 | An owner message that merely contains a harness marker string is thrown away, and when no owner message is left both gates switch off. | reimpl | **FIXED HERE** | merge-gate auditor: "fixed" |
| RI-6 | The Stop gate does not see a commit or push written with a git option before the subcommand (git -c ..., --no-pager, a quoted -C path), nor a sched... | reimpl | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| RI-7 | "A scheduled run never merges" holds for two spellings only | reimpl | **FIXED HERE** | merge-gate auditor: "fixed" |
| RI-8 | Both gates match words, not commands: the only merge denial in the real-session replay falls on a 14-line command that runs cd, grep and python3, a... | reimpl | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| F1-1 | An outward action taken by a delegate is invisible to F1 | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED via the ledger" |
| F1-2 | Once any Stop hook has blocked in a turn, F1 does not look again | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| F1-3 | Five tools in the session's own tool list do what the rule names (merge a PR, update a PR, create or delete a scheduled task) and F1 does not count... | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| F1-4 | F1 does not recognise ordinary shell spellings of commit, push and PR update or merge | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED for all git/gh/curl/Monitor forms"; two stated limits (python3 -c, a script not on disk) |
| F1-5 | A turn that missed plan-gate before its first outward action is blocked again at every later stop of the same owner turn, after doing exactly what ... | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| F1-6 | F1 reports 'this turn took an outward action' for turns that took none | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| F1-7 | The fixture does not pin most of F1: nine single changes to the rule pass 44/44, and with two of them the whole guard still prints RESULT | atk-f1 | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `hooks/selftest-mutations.py` (breaks whose origin names it); `results/2026-11-15/turn-gates-fix/mutations.txt`; all 9 surviving changes are named by a break |
| F1-8 | A Skill call that returned an error, and a load made before a compaction in the same turn, both count as loaded | atk-f1 | **FIXED HERE** | Stop-gate auditor: "FIXED with paired ids" |
| WR-1 | On the hooks installed in the target session today (plugin 0.1.4) the weekly run is not a turn of its own, so a merge call inside it is allowed on ... | rev-weekly-run | **READY, CLOSES WHEN THE OWNER UPLOADS THE PLUGIN** | `results/2026-11-16/surfaces-fix/after-the-merge.md` |
| WR-2 | With the merged hooks, "a scheduled run never merges" stops two spellings only | rev-weekly-run | **FIXED HERE** | merge-gate auditor: "fixed" |
| WR-3 | The stop rule as stored counts pull requests, not runs, and exempts any pull request the owner "touched" | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| WR-4 | Step 1 rewrites three live checkouts every Monday (stash, switch to main, hard-move main) and nothing puts them back | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| WR-5 | The weekly task has no preflight step and the library has no preflight spec, against the library's own rule for unattended runs. | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| WR-6 | The evidence pack hides its own failures | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| WR-7 | The test behind "prints its three sections and changes nothing (tested)" passes when the pack has no content and when the script writes into the pr... | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| WR-8 | At Monday 06:43 Pacific the run's own ISO week is under seven hours old and the pack counts by ISO week, so "the week" in steps 4, 5 and 7 has two ... | rev-weekly-run | **LEFT FOR THE SECOND PULL REQUEST** | unit: weekly task prompt |
| CB-1 | The hook does not stop the weekly task from merging | aud-claims-b | **FIXED HERE** | merge-gate auditor: "fixed on the fixed library and its plugin copy (14/14)"; the account serves the old plugin until the owner uploads 0.1.6 |
| CB-2 | The registry does not hold every hand-set value in hooks/, and the guard passes when an unregistered value changes or a new one is added. | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| CB-4 | "20 rules, oldest 124 days" counts marker lines, not rules | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| CB-3 | "15 unregistered" cannot be reproduced: the re-run gives 13, and the committed record shows none. | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CB-6 | Two records are not raw evidence: the council eval has only a summary table, and the green test record is the 8-test output with a bare "OK" appended. | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CB-8 | All three commits of the merge name the model in their trailer, against doctrine rule 6. | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CB-5 | The PR body says 8 new tests; the merged file has 10. | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CB-7 | The ledger dates the kit's fix 2026-11-03 | aud-claims-b | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| RL-1 | The gate never matches the contraction "can't verify / confirm / determine" | atk-receipt | **FIXED HERE** | receipt-gate auditor: "fixed" |
| RL-2 | When the other Stop hook forces the retry, the receipt gate skips the retried answer | atk-receipt | **FIXED HERE** | receipt-gate auditor: "fixed" |
| RL-3 | Thirty-seven of 37 natural bare claims outside the nine hard-coded patterns pass, including "not available", one of the four phrases the rule itsel... | atk-receipt | **FIXED HERE** | receipt-gate auditor: "fixed: 40/40" |
| RL-4 | A receipt that quotes the command and its error is invisible to the gate | atk-receipt | **FIXED HERE** | receipt-gate auditor: "fixed: 12/12 allowed" (with the auditor's own finding AR-1 beside it) |
| RL-5 | Sentences that are not claims of inability are blocked | atk-receipt | **FIXED HERE** | receipt-gate auditor: "fixed: 17/17" |
| RL-6 | Any of about 25 words within 400 characters counts as the receipt, including the very thing that was not verified ("couldn't verify whether the cro... | atk-receipt | **FIXED HERE** | receipt-gate auditor: "R 12/12 fixed"; Q01 and Q02 (claim in a block quote or inline code) still allowed, a stated limit |
| RL-7 | The two Stop hooks start the turn at the same row at only 8 of 26 real stops, and after this merge a scheduled run is a turn of its own for governa... | atk-receipt | **FIXED HERE** | receipt-gate auditor: "6 as wanted"; S05 (scheduled run, record without a stop row) still blocks, a stated limit |
| RL-8 | Neither the gate's selftest nor the library guard notices when the gate is changed to read only the last transcript row, fire once per session and ... | atk-receipt | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `hooks/selftest-mutations.py` breaks RC01 to RC16; `results/2026-11-15/receipt-gate-fix/mutations.txt`; all 11 surviving changes are named |
| ADV-1 | On the real session the plan-shown advisory fires on 6 of 7 plan-gate loads, among them turns where the records say a plan was shown | atk-advisory | **STATED LIMIT** | CORE-SPEC section 5: the advisory states that the record does not keep every message (break AD02); the miss itself is not removed |
| ADV-2 | The guard prints PASS when the compaction hook does nothing, when both first-write reminders never fire, when the plan-shown advisory fires once pe... | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| ADV-3 | The registry said to hold every hand-set value in hooks/ leaves out the advisory's exempt locations, its write-tool list and the ledger phrase list... | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| ADV-4 | The advisory takes a read-only shell command that only mentions `git commit`, `git push`, `sed -i` or `git checkout -b` for the first write and spe... | atk-advisory | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| ADV-5 | The two once-per-session reminders are spent on a scratch write under /tmp, or on a helper agent's write, and are then silent at the main session's... | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| ADV-6 | Fifteen of sixteen behaviour changes to the advisory hooks pass all three shipped self-tests, among them an advisory that fires once per session an... | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| ADV-7 | With the temp directory missing or unwritable the plan-shown advisory never fires while the two reminders fire on every write | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| ADV-8 | In a one-repository cloud session that also has the account plugin the post-compaction protocol is injected twice every time, and the first-write r... | atk-advisory | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| PC-1 | An owner message that quotes a harness marker, or begins with the gate's own text, is skipped as harness text | atk-promptclass | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| PC-2 | A dispute worded 'that doesn't look right' or 'is this right??' is classified review, gets the trivia allowance, and a one-line acquiescence passes | atk-promptclass | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| PC-3 | Chat, status questions, one-word answers, pasted error text and a negated order ('don't build anything yet') match an enforced class, and the one-l... | atk-promptclass | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| PC-4 | After one block by either Stop hook, the next stop of the turn is allowed with no check | atk-promptclass | **FIXED HERE** | Stop-gate auditor: "D3 and D5b fixed"; case D2 now allowed by Q3 of 2026-11-15 |
| PC-5 | The prompt-class half does not use turn_start | atk-promptclass | **FIXED HERE** | Stop-gate auditor: "FIXED on real row shapes" |
| PC-6 | When the transcript holds no owner message (a file that begins at a compaction boundary, as the real record does) the gate exits without checking a... | atk-promptclass | **FIXED HERE** | Stop-gate auditor: "F1 half fixed"; the prompt-class half is still silent (the auditor's finding AS-7) |
| PC-7 | Eleven rule-breaking mutations of the Stop gate and the classifier pass both fixtures, and four of them also pass the registry check, so nothing th... | atk-promptclass | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `hooks/selftest-mutations.py` (breaks whose origin names it); `results/2026-11-15/turn-gates-fix/mutations.txt`; 5 of its 11 surviving changes are named by a break (M2 through PS21/PS22); the 6 classifier changes belong to the prompt side, second pull request |
| PC-8 | A build the owner orders by clicking a card answer is never classified | atk-promptclass | **CHANGED BY AN OWNER DECISION** | Q5 of 2026-11-15 ("No, only what you type") |
| TR-1 | A disagreement typed with a curly apostrophe (I don’t agree) is not recognised as a dispute | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-2 | Good news, plain questions and acknowledgements are classified as disputes or reviews | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-3 | For a message that is both a dispute and a build request the trigger names two governors, and the Stop gate then blocks the session that loaded exa... | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-4 | A card clicked at any point since the owner's last typed message switches the reminder off for everything after it, a scheduled run's report included | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-5 | The reminder recognises one way of writing a decision as text | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-6 | Both selftests stay green when the reminder scans the whole session instead of the previous reply, when review and analysis prompts are told to loa... | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-7 | The reminder is also injected when the prompt is a harness notification (finished background task, wake, system notification), not only on the owne... | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| TR-8 | When the owner sends the same text twice in a row (ok, continue) the reminder judges the reply before last | atk-trigger | **LEFT FOR THE SECOND PULL REQUEST** | unit: prompt side |
| CA-1 | The guard prints that every hand-set value in hooks/ is registered and unchanged, but the pattern that decides which Bash commands are a PR merge i... | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| CA-2 | P5 as the owner approved it says 'Re-run Red Team on the hooks' | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CA-3 | corrections_rate.py counts cut-short dated rows as caught by the session, loses an owner catch when the last cell contains a pipe, and counts a wee... | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| CA-4 | The outcome says the old registry had '15 unregistered' values | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CA-5 | stale_rules.py is described as listing every unmeasured marker older than 60 days | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| CA-6 | Three recorded outputs do not match their commands on the merged commit | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CA-7 | The audit report's registry row says 6 unregistered values and 'two items that were fixed' | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| CA-8 | The audit report dates kit commit b040962, and the kit's hook improvement, to 11-03 | aud-claims-a | **LEFT FOR THE SECOND PULL REQUEST** | unit: documents and claims |
| FU2-6 | After a compaction the file the hooks read holds no owner message, and then every turn gate lets everything through, a merge included. | followup-2 | **FIXED HERE** | merge-gate auditor: "fixed" |
| FU2-1 | Once any Stop hook has blocked, the program sends stop_hook_active=true at every later stop of that turn, so both Stop gates stop checking | followup-2 | **FIXED HERE** | Stop-gate auditor: "FIXED" |
| FU2-2 | Outward actions a helper agent takes are written to a separate file that the Stop gate never reads, and no hook runs when the helper ends, so F1 ca... | followup-2 | **FIXED HERE** | Stop-gate auditor: "The ledger fixes it when the pre-tool hook sees the helper's calls"; live delivery of helper calls "not verified" |
| FU2-3 | Any tool result that contains a line shaped like the scheduled header restarts the turn as a 'scheduled run' | followup-2 | **CHANGED BY AN OWNER DECISION** | D2: the fixture's wake row ends the word, so spoof and control are both denied; a header imitated without a wake is allowed (A08). Stop-gate part not judged |
| FU2-4 | A message the owner types while the assistant is working is recorded as an attachment row, which the owner filter never reads | followup-2 | **FIXED HERE** | merge-gate auditor: "fixed" |
| FU2-5 | A slash command the owner types (arguments included) and an image-only message do not start a turn for the gates, so the new turn's outward actions... | followup-2 | **FIXED HERE** | merge-gate auditor: "fixed" |
| FU2-9 | The receipt gate judges only assistant text it finds in the file, although the program hands the final answer over in the Stop payload and the real... | followup-2 | **FIXED HERE** | receipt-gate auditor: "fixed: 2/2 block" |
| FU2-8 | A check-in the owner asked for arrives with exactly the same header as the weekly task, so the two stated merge rules give opposite answers and the... | followup-2 | **CHANGED BY AN OWNER DECISION** | Q1 of 2026-11-15 ("No, ask me again"): "DENY:SCHEDULED, as the owner's Q1 answer decides" |
| CN-1 | The trigger eval's only record is a 16-line summary by its author | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-2 | The eval ran against the account copy, so the 36 lines the merge added, including the one new rule, were never loaded by any test, and no eval case... | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-3 | With the hooks on, the eval's own should-fire prompt id 2 gets an order to load plan-gate before answering, and a Council-only verdict is blocked a... | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-4 | The added "outside read" section cannot be followed as written | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-5 | Eval case 4 expects silence on a message that contains the keyword, the opposite of the description's stated rule, and the silence was graded as a ... | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-6 | The record cannot show the predictions came before the runs | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-7 | The skill's own re-verify command prints a difference today, and will print 35 differing lines once the owner uploads the package the PR asks for. | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| CN-8 | Nothing in the lint or the guard pins the council skill | rev-council | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the council skill is in no unit of the 2026-11-16 card) |
| OS-1 | The figure "20 rules still untested after 60 days, oldest 124 days" counts lines, not rules | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-2 | stale_rules.py leaves out dated UNMEASURED statements whose date is more than three lines above the marker or on the line below it | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-3 | test_qa_loop.py stays green under 20 of 20 changes to what the two scripts compute | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-4 | A table row whose date cell is blank or a hyphen is dropped without being counted anywhere, although the script and the pre-registered prediction b... | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-5 | Who caught a row is read from the second-to-last cell, so a pipe in the fourth or fifth cell, or one column added after the fifth, moves rows betwe... | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-6 | The date stale_rules.py attaches to a marker is the first date on the nearest dated line, which for three markers in the library belongs to somethi... | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-7 | Owner-caught is decided by whether the word "owner" appears in one cell | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| OS-8 | A corrections log the parser cannot read as pipe-led rows, and a stale-rules root that holds no files, both print the same clean zero with exit 0 a... | rev-outcome-scripts | **LEFT FOR THE SECOND PULL REQUEST** | unit: outcome scripts |
| RG-1 | The registry does not hold every hand-set value in hooks/ | rev-registry | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `redteam/live.py` reads the four gate modules whole; `results/2026-11-15/receipt-gate-fix/registry-proof.txt`. Values in the other hook files are still read by name (registry rest, second pull request); the audit's 16 changes were not re-made |
| RG-2 | A new hand-set constant added to a hook is not reported as unregistered | rev-registry | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `redteam/live.py`; `results/2026-11-15/receipt-gate-fix/registry-proof.txt` (a new word in a gate module fails the check) |
| RG-3 | Regex flags are not part of a registered pattern's value | rev-registry | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `redteam/live.py` (gate modules read whole, flags included); no separate red run found |
| RG-4 | live.py reports registered values the hooks no longer use | rev-registry | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| RG-5 | REMINDER_JQ_PATH is registered as "/usr/bin/jq" although both first-write reminders read the session id with python3 | rev-registry | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| RG-6 | The committed registry record says PASS on commit 111fc60, a commit with no redteam/ and with hooks on which the check cannot run | rev-registry | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| RG-7 | Eleven of the 23 'uncalibrated' entries cite decision D-QA-1, which no file in the repository defines | rev-registry | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| RG-8 | "6 drifted, 15 unregistered" is not what the recorded output or a re-run shows | rev-registry | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| SF-1 | The weekly task runs in a several-repository cloud session that is judged by plugin 0.1.4, where a scheduled run can merge on an earlier owner "mer... | rev-surfaces | **READY, CLOSES WHEN THE OWNER UPLOADS THE PLUGIN** | `results/2026-11-16/surfaces-fix/after-the-merge.md` |
| SF-2 | The install runbook tells you to copy a settings file that calls a hook it never tells you to copy | rev-surfaces | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `results/2026-11-16/surfaces-fix/README.md` and its `raw/` files; the auditor's wrapper case W11 stays open (it needs the wrapper's rule, SF-5/SF-8) |
| SF-3 | Tool names the session really has fall between the wiring and the code | rev-surfaces | **FIXED HERE** | Stop-gate auditor: "FIXED in the wiring" |
| SF-4 | The guard passes when the merge gate is cut off from the PR tools or the receipt gate is unwired, in the project settings and in the plugin's hooks... | rev-surfaces | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `results/2026-11-16/surfaces-fix/README.md` and its `raw/` files; breaks WI05 to WI26 in `hooks/selftest-mutations.py` |
| SF-5 | In a one-repository cloud session that carries the pack, two copies answer four of eight events, and today they are different versions, so the fals... | rev-surfaces | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |
| SF-6 | Two parity checks have holes: the guard does not compare the plugin's selftest-reminders.sh, and the wrapper self-test passes on a wrapper that yie... | rev-surfaces | **FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR** | `results/2026-11-16/surfaces-fix/README.md` and its `raw/` files |
| SF-7 | Two of the three skill packages sent for upload do not have the layout the install runbook says a .skill must have. | rev-surfaces | **LEFT FOR THE SECOND PULL REQUEST** | unit: none named (the skill packages; the surfaces unit's brief lists them as waiting) |
| SF-8 | The wrapper's yield test is looser and narrower than its rule | rev-surfaces | **LEFT FOR THE SECOND PULL REQUEST** | unit: registry rest, advisory hooks and guard gaps |

## Totals

| state | findings |
|---|---|
| FIXED HERE (re-run by an outside auditor) | 48 |
| CHANGED BY AN OWNER DECISION (re-run by an outside auditor) | 5 |
| FIXED HERE, NOT RE-RUN BY AN OUTSIDE AUDITOR | 10 |
| STATED LIMIT | 1 |
| READY, CLOSES WHEN THE OWNER UPLOADS THE PLUGIN | 3 |
| LEFT FOR THE SECOND PULL REQUEST | 61 |
| UNPLACED | 0 |
| **all** | **128** |

**The pull request's sentence "60 resolved or decided, 3 ready, 65 left" does not hold as written.** The records
give 63 resolved or decided (48 + 5 + 10), 3 ready, 1 stated limit and 61 left. The 3 ready ones agree. The other
two numbers cannot be matched id by id, because no file lists the 60: the decisions record says 57 at 2026-11-16
about 03:35 UTC, and the surfaces commit adds SF-2, SF-4 and SF-6 (57 + 3 = 60), while the regression lists hold
63 ids. Read either way, the sentence leaves out that 10 of the resolved ones were checked by their builder only.

Notes on single rows:

- Re-run with part of the finding still open: F2-5, F1-4, RL-6 and RL-7 carry stated limits; PC-6's prompt-class
  half is the outside auditor's finding AS-7; FU2-2 was not verified with a live helper agent; TB-3's and FU2-3's
  Stop-gate parts were not judged by an outside auditor.
- PC-7 and TB-8 are only partly pinned: 5 of PC-7's 11 recorded changes and 7 of TB-8's 9 are named by a break
  (`first-preregistration-outcomes.md`, row G7).
- RG-1 is resolved for the four gate modules only (`redteam/live.py` reads `turngate.py`, `turn-gates-pretool.py`,
  `governance-enforce.py` and `receiptlaw.py` whole); hand-set values elsewhere in `hooks/` are still read by name.
