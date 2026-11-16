# CORE-SPEC: turn model, merge gate, Stop gate

One specification made from two unfinished designs (A and B) and the follow-up audit of the harness. Judge run 1,
2026-11-14. STATUS: see the last line of this file (a complete file ends with "END OF SPECIFICATION").

Paths: FIX = the fix's scratch folder (outside this repository), PACK = the audit's scratch folder (outside this repository), J = `FIX/design/core-judge` (the judge's
scratch directory). "Merged hooks" = `PACK/lib/hooks` (commit 1ce99d5). Design A = `FIX/design/core-design-a`,
design B = `FIX/design/core-design-b`. "Reference prototype" = `J/spec/proto/hooks`: design B's prototype with the
combined rules of this specification grafted on (`J/spec/grafts.py`). It is evidence, not the code to ship.

The three files this specification covers: `hooks/turngate.py`, `hooks/turn-gates-pretool.py`,
`hooks/governance-enforce.py`. Base: **design B** (its row model, its shell parser, its failure paths). From design
A: the decision tables, the bracketed denial codes, the reading of a yes-answer on a merge card, the free-text
answer form, the classification of messages typed mid-turn, the branch lookup without a subprocess. New in this
specification (neither design has it): the stretch rule of the Stop gate (1.3), the ordered reading of an owner
message with the open-negation rule (2.5), the rule for a slash command recorded as a harness row (2.2), the
deadline inside the hooks (2.8), the anchored matcher (3.3).

## 0. What was run for this specification

Every run was made by the judge on copies under `J/a` and `J/b` (the designs' folders were not written to), with
`PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` inside `J/tmp`. Output files are in `J/runs/`.

| # | what | command | result |
|---|---|---|---|
| R1 | design A's cases, merged and prototype | `python3 J/a/tests/run_tests.py` -> `a-tests.txt` | 241 cases: 241 pass on A's prototype; 147 red on the merged hooks; 94 controls |
| R2 | design B's cases, merged and prototype | `python3 J/b/tests/test_core.py` -> `b-tests.txt` | 254 cases: 253 pass on B's prototype, 1 fails (T16e); 143 red on the merged hooks |
| R3 | design A's deliberate breaks | `python3 J/a/tests/mutate.py` -> `a-mutate.txt` | 84 breaks: 84 caught, 0 survive |
| R4 | design B's deliberate breaks | `python3 J/b/tests/mutate.py` -> `b-mutate.txt` | 55 breaks: 55 caught, each by a case other than T16e; the control N00 shows 1 failing case (T16e), not the 0 its own footer requires |
| R5 | A's cases on B's hooks | `python3 J/tools/cross_a_on_b.py J/b/proto/hooks` -> `cross-a-cases-on-b-hooks.txt` | 12 of 241 differ |
| R6 | B's cases on A's hooks | `python3 J/tools/cross_b_on_a.py J/a/proto/hooks` -> `cross-b-cases-on-a-hooks.txt` | 29 of 254 differ |
| R7 | structure probe on the real record: row types, flags and prefix classes, no content | `python3 PACK/pack/tools/replay_real.py --hooks J/probe-struct --what stop` -> `probe-struct.jsonl` | the rows a blocked stop leaves, and their order (2.1, fact H2) |
| R8 | program text, card answers | `python3 PACK/work/followup-2/tools/bs.py -s 300000000 -m 2 -b 260 -a 420 'The user answered'` | three result texts (2.1, fact H10) |
| R9 | follow-up facts | `bash PACK/work/followup-2/facts.sh` | 35 quotes printed |
| R10 | which branch B's Stop gate takes at each real stop | replay with `J/probe-b` -> `probe-b-branches.jsonl`, `probe-b-replay.txt` | B's prototype as it stands blocks at 2026-11-02T22:43 like the merged hooks. B's own recorded replay (`runs/replay-fixed.txt`, made before its last edits) shows allow there and is out of date |
| R11 | the follow-up audit's reproductions on A and on B | `python3 J/fu2/repro_ab.py` -> `fu2-on-a-and-b.txt` | A: FU2-1, FU2-3b and FU2-5 not fixed. B: FU2-3b not fixed; FU2-1, FU2-4, FU2-5, FU2-6, FU2-7 fixed |
| R12 | reference prototype on both designs' cases | `python3 J/spec/tests/test_core.py` -> `spec-on-b-cases.txt`; `python3 J/tools/cross_a_on_b.py J/spec/proto/hooks` -> `spec-on-a-cases.txt` | B's cases: 251 of 254 agree; A's cases: 234 of 241 agree. The 10 that differ are decisions of this specification (section 8, last table) |
| R13 | the follow-up reproductions on the reference prototype | `python3 J/fu2/repro_spec.py` -> `fu2-on-spec.txt` | FU2-1, FU2-3b, FU2-4, FU2-5, FU2-6, FU2-7 print the required verdict; the rest is explained in section 5 |
| R14 | real-record replay of the reference prototype | `TURNGATE_NO_GIT=1 python3 PACK/pack/tools/replay_real.py --hooks J/spec/proto/hooks --what all` -> `replay-spec-final.txt` | Stop: 1 of 26 verdicts differs from `PACK/pack/replay-baseline.txt` (a block became an allow, F1-5). Pre-tool: 2 denials, both merges under a word that names no number (D1). Prompt: identical |
| R15 | what the record knows about pushes the gate cannot resolve | replay with `J/probe-branch` -> `probe-branch.jsonl` | 3 pushes in 2 real calls have no readable destination; the record's own branch field does not name one |
| R16 | run time on a 37.2 MB record (25,003 rows) | inline script, last lines of the R14 command block (output quoted in 7.2) | reference prototype 0.30 to 0.33 s per gated call; merged hooks 0.34 to 0.35 s |
| R17 | the two grammars on the reference prototype | `python3 J/tools/assemble.py` -> `spot-checks.txt` | 37 typed messages and 10 card answers; the readings quoted in 2.4 and 2.5 |
| R18 | the new cases of 6.2 that could be built, on the merged hooks and on the reference prototype | the same command -> `j-cases.txt` | 17 verdict pairs; the reference prototype gives the wanted verdict in 17 of 17 |

Not run: the library guard; the registry check; the plugin, kit and deck copies; anything on a Mac; any live
session; the shipped selftests against the reference prototype; a merged list of deliberate breaks against the
reference prototype. Specified here but in no prototype (each is marked "not run" where it is stated): the deadline
inside the hooks (2.8), the slash command recorded as a harness row (2.2), the branch lookup from `.git/HEAD` on
design B's parser (it runs in design A's prototype, R1), the anchored matcher (3.3), the ledger's time stamp (2.7).

---

## 1. The intended rules as decision tables

Sources: D1, D2, D3 = `FIX/OWNER-DECISIONS.md`. "README" = `lib/hooks/README.md`. "doctrine" = the doctrine block in
`lib/CLAUDE.md`. H1 to H12 = the harness facts of section 2.1. Q1 to Q6 = the open policy questions of section 9.
A row marked with a constant name has its hand-set value in that one constant.

### 1.1 Words

| word | meaning |
|---|---|
| merge-class call | a call that merges a pull request, switches auto-merge on, or pushes to a default branch (section 3) |
| owner word | text the owner typed (a message, a slash command's arguments, a message sent while the assistant works) or the answer to a card (AskUserQuestion) paired to its own call (2.4) |
| grant | the pull requests (number, and repository when the owner word names one), and separately "the default branch", that the owner words of the current window order merged or pushed |
| completed stop | a stop row with no hook errors. A stop row with hook errors is a blocked stop: the assistant was sent back to work (H2) |
| window | the rows after the latest of: a typed owner message, a completed stop, an interrupt, a wake row, a restart notice, a scheduled delivery. The merge word lives in one window (D2) |
| attended | the window is not a scheduled run and holds at least one owner word |
| scheduled run | work that starts at a genuine scheduled delivery (2.6) read while no owner turn was in progress |
| governance turn | the rows from the owner's latest typed message, or from the start of the latest scheduled run, whichever is later. Governor loads count inside it |
| stretch | the rows after the owner's latest typed message or the latest completed stop, whichever is later (the start of the file if neither). It is what one Stop still has to judge |
| helper call | a tool call made by a helper agent: the hook's input carries `agent_id` (H1) |

### 1.2 Merge gate (PreToolUse, `turn-gates-pretool.py`)

Evaluated top to bottom; the first matching row gives the verdict. Every denial reads
`TURN-GATE (merge word) [code]: ...`; the code lets a test tell the rows apart.

| # | input | verdict | from |
|---|---|---|---|
| M1 | the call is not merge-class | not judged here (table 1.5 may add a reminder) | D3 |
| M2 | merge-class call; the record path is empty or missing, the file is empty or holds no parsable row | DENY `no-record` | D1 "authorized only by"; COMMON-FIX 4; TB-1, F2-7; H8 |
| M3 | a push whose destination the gate cannot resolve (3.1), in a window that is not attended | DENY `branch-unknown`; the reason says to name the branch in the command. In an attended window the push is treated as an ordinary push | D3; Q2 (`PUSH_UNKNOWN_BRANCH_POLICY`) |
| M4 | merge-class call in a scheduled run, and no message typed by the owner since the delivery | DENY `scheduled` (the reason keeps the words "a scheduled run never merges") | D3 "In a scheduled run they are always denied" |
| M5 | merge-class helper call while `DELEGATE_MAY_MERGE` is False | DENY `delegate`. Default True: a helper call is judged like any call, on the main record, which is the record the hook is handed (H1) | D1; FU2-2 |
| M6 | merge-class call; the window holds no owner word (file restart, wake after a stop, restart notice, harness rows only) | DENY `no-owner-word` | D1; D2 "Work started by a later notification or wake-up starts with no authorization"; FU2-6 |
| M7 | pull-request merge or auto-merge whose number cannot be read from the call (the command-line merge with no number, a GraphQL mutation, a number that comes from standard input, a shell text the parser cannot read but that holds merge words and no readable number) | DENY `target-unknown` | D1 "names the pull request number" |
| M8 | merge or auto-merge of PR n; n is in the grant (and the repository matches when the owner word named one) | ALLOW | D1 (a), (b); D2 "covers only the pull requests named" |
| M9 | merge or auto-merge of PR n; n is not in the grant | DENY `merge-word`; the reason tells the assistant to ask with a card whose merge option names #n | D1 last sentence |
| M10 | push to a default branch; the grant holds "default branch" | ALLOW | D3 "the same word as a merge"; Q2 |
| M11 | push to a default branch; no such grant (a grant for PR n does not cover it) | DENY `default-branch` | D3 |
| M12 | the hook fails, or reaches its own deadline, after or before it has classified the call | DENY `gate-error` when a crude screen (tool name, command text) sees a merge route; otherwise allow | COMMON-FIX 4; H4 |

What ends the window (D2), and what does not:

| event | effect on the grant | from |
|---|---|---|
| a message the owner types while the assistant is idle (a typed slash command and an image-only message included) | new window; the earlier grant is gone | D2; FU2-5 |
| a completed stop; an interrupt | the grant is gone | D2 "It ends when the assistant stops" |
| a wake row (a notification, a task or a peer message that only an idle session receives) | the grant is gone | D2 second sentence; TB-6 |
| the restart notice of the worker process | the grant is gone (`RESTART_ENDS_WORD = True`) | D2, safest reading; H8 |
| a scheduled delivery read in the middle of an owner turn | the grant made before it is gone; a card the owner answers after it grants again (`SCHEDULED_READ_ENDS_WORD = True`) | Q1 |
| a blocked stop; a notification queued mid-turn; a GitHub notification read mid-turn; a skill load; hook feedback; a compaction | nothing: the grant stays | D2 "until I stop"; H2 |
| a later owner word that refuses (typed mid-turn, or a card answer) | the refused numbers leave the grant; a bare refusal empties it | D1; F2-1, FU2-4 |

What makes a grant (D1). The grammar is in 2.4 and 2.5.

| # | owner word | grant | from |
|---|---|---|---|
| G1 | typed message with an order that starts a clause and names numbers right after the verb: "Merge #34.", "ok, merge 34 and 141", "go ahead and merge PR 34", "No objections, merge #34.", "Can you merge #34?", a pull-request URL, `owner/repo#34` | those numbers (bound to the repository when the word names it) | D1 (b); F2-8 |
| G2 | the verb with no number: "merge it", "yes", "proceed and merge" | nothing | D1 last sentence |
| G3 | the verb negated, asked about, reported, or not at the start of its clause: "Don't merge #34" (straight or curly apostrophe), "You can't merge #34 yet", "Don't, under any circumstances, merge #34", "Is #34 safe to merge?", "Is #34 merged yet?", "#34 is ready to merge", "before you merge #34, run the guard" | nothing; a negated clause takes its numbers out of the grant (all numbers when it names none) | D1 "an order to merge"; RI-1, RI-2, F2-3 |
| G4 | "Merge #34, not #141" / "Do not merge #34. Merge #35." / "Merge 34. Leave 141 alone" / "Merge #34 and close #35." / "Merge everything except #141" | #34 only / #35 only / #34 only / #34 only / nothing | D2 "only the pull requests named"; F2-2, RI-4 |
| G5 | an order for later or under a condition: "Merge #34 once CI is green", "Merge #34 after you fix #35" | nothing, and nothing is taken back (`DEFER_CUE`) | D1: the gate cannot check the condition |
| G6 | card answer: the chosen option is an order ("Merge both", "Merge #34 now") or a yes ("Yes, both") on a card whose question asks for a merge; numbers named in the chosen option | the numbers in the chosen option | D1 (a) |
| G7 | as G6, the chosen option names no number: the question names exactly one PR; or it names several and the option says "both / all / every / each / everything" | the numbers in the question | D1 (a) "a card that names the pull request number"; F2-8 |
| G8 | as G6, the question names several PRs and the option names none and has no such word ("Merge library only", "Yes") | nothing | F2-2, RI-4: the gate cannot tell which |
| G9 | card answer that refuses or defers ("Wait", "Not yet", "Merge neither", "Merge after the audit"), or any other option of a merge card ("Show me the diff first") | nothing; the question's numbers leave the grant | D1; F2-1, F2-3 |
| G10 | card answer on a card that does not ask for a merge ("Which workflow should I run?" = "Audit today's merge (Recommended)") | nothing | D1 (a); F2-2 |
| G11 | card answered with free text | read as a typed message (G1 to G5). When the text is an order without a number ("merge it, squash please") it takes the question's numbers under the rule of G7 | D1 (a) and (b) |
| G12 | an order to push to the default branch: a clause that starts with push / merge / commit / land and names main, master or "the default branch", not negated, not deferred, naming no PR; or a card whose question asks it and whose chosen option is a yes or repeats it | "default branch" | D3; Q2 |
| G13 | the assistant's own text; a tool's output, whatever it quotes; a notification body; a stored prompt; a compaction summary; a helper agent's row; a harness row | nothing | D1 "typed by the owner", "the owner's click"; TB-2, F2-4, RI-3, F2-1 |
| G14 | a card answered inside a scheduled run | nothing (M4) | D3; doctrine: a scheduled run "shows no card"; Q1 |

### 1.3 Stop gate, outward-action rule (`governance-enforce.py`, first half)

| # | input | verdict | from |
|---|---|---|---|
| S1 | no outward action in the stretch | this half is silent | README:13 |
| S2 | outward actions in the stretch; in the governance turn each of them falls in, plan-gate was loaded before the first of them and adversarial-verify anywhere | allow | README:13-15 |
| S3 | as S2 but plan-gate was not loaded before the first, or adversarial-verify not at all | BLOCK; the reason names what is missing and what to do | same |
| S4 | the command only mentions the words (a search, an echo, a here-document, a commit message, a script written but not run), is a dry run or a help page, was denied before it ran, was rejected at the permission prompt, or is the last step of an and-chain that failed | not an outward action | F1-6, RI-8 |
| S5 | the stretch holds a scheduled-run start: the part before it and the part after it are judged separately, each on the loads of its own governance turn | BLOCK when either part misses | README:1-2; FU2-3, TB-3 |
| S6 | the retry flag (`stop_hook_active`) is set | it decides nothing by itself (H3). The gate counts its own earlier blocks in the stretch from the record (H2) | FU2-1, F1-2, PC-4 |
| S7 | this rule already blocked in the stretch; since then plan-gate was loaded (it can no longer come first) and adversarial-verify is loaded | allow | README "BLOCK once and force the load" |
| S8 | this rule already blocked in the stretch and the miss is still there, or a new outward action came without the governors | BLOCK again, at most `F1_MAX_BLOCKS` (2) times in one stretch, then allow | Q3 |
| S9 | the retry flag is set and the record shows no blocked stop in the stretch | allow (the gate cannot count: the documented single retry) | README; loop safety |
| S10 | the stretch starts at a completed stop and no owner message follows (a wake) | only the outward actions since that stop are judged; an earlier miss is not raised again; governor loads made since the owner's message still count (`WAKE_TURN_INHERITS_LOADS = True`) | F1-5; Q4 |
| S11 | a scheduled run | judged on its own rows: loads from before the run do not count | README:1-2 |
| S12 | the record holds no owner row (it restarts at a compaction boundary) | the stretch is judged like any other: from the latest completed stop, or from the start of the file | FU2-6, TB-1, PC-6 |
| S13 | an outward call by a helper agent | counts, at the point of the main record where it was made, from the note the pre-tool hook left (2.7). Rows of a helper that sit in the main record count the same way | F1-1, FU2-2 |
| S14 | a Skill call whose result is an error | not a load | F1-8 |
| S15 | a load made before a compaction boundary in the same governance turn | counts (`COMPACTION_VOIDS_LOADS = False`) | Q4 |
| S16 | the record is missing or unreadable, or the hook fails or reaches its deadline | allow: a Stop hook does not hold ordinary work on its own failure | COMMON-FIX 4 |

### 1.4 Stop gate, prompt-class rule (`governance-enforce.py`, second half)

| # | input | verdict | from |
|---|---|---|---|
| P1 | the governance turn is not an owner turn (scheduled run, no owner row in the record) | silent | PC-5, TB-7, PC-6 |
| P2 | a completed stop or a wake row lies between the owner's message and this stop | silent: the answer to that prompt was judged at its own stop | PC-5 |
| P3 | the owner prompts of the turn match no enforced class | allow | `govclass` |
| P4 | the primary governor of every matched enforced class was loaded in the governance turn | allow | README |
| P5 | the classes are exactly {review}, no tool other than Skill ran, and the answer is shorter than `TRIVIA_MAX_CHARS`. The answer is the recorded text of the turn plus the hook input's `last_assistant_message` when the record does not hold it (H7) | allow | README; FU2-9 |
| P6 | otherwise | BLOCK, at most `PROMPT_CLASS_MAX_BLOCKS` (1) time in a stretch. A block by the other rule or by another Stop hook does not use this up | README; PC-4; Q3 |
| P7 | the owner's message quotes a harness marker or starts with a hook's own words | it is the owner's prompt and is classified | PC-1, TB-4 |
| P8 | owner prompts are: the typed message that starts the turn; a slash command's arguments when the command starts the turn; every message the owner sent while the assistant worked | all are classified; the classes add up | FU2-4, FU2-5 |
| P9 | a governor loaded before the governance turn started | does not count | PC-7 |
| P10 | a build ordered by a card answer | not classified (`CLASSIFY_CARD_ANSWERS = False`); rule 1.3 still applies once the turn commits or pushes | PC-8; Q5 |

### 1.5 Plan-shown advisory (`turn-gates-pretool.py`)

| # | input | verdict | from |
|---|---|---|---|
| A1 | plan-gate not loaded in the governance turn | silent | README:16-18 |
| A2 | plan-gate loaded; this call is a real write outside scratch, an outward action or a scheduled-task change; the record holds no assistant text with the plan mark since the load | one advisory per load; its text says the record does not keep every message (H7) | ADV-1 |
| A3 | the command only mentions write words, or writes only to scratch | not a write; the advisory is not spent | ADV-4 |
| A4 | a helper call | silent: the helper's own plan-gate load and plan are not in the record the hook reads (H1) | FU2-2 |

---

## 2. The turn model

### 2.1 Established facts about the harness

H1 to H9, H11 are the follow-up audit's facts (program 2.1.325, read not run; quotes: `bash PACK/work/followup-2/facts.sh`;
real-file numbers: `PACK/work/followup-2/out/probe.txt`). H2's row order, H10 and the wake positions in H9 were
established by the judge (R7, R8, R10). The designers did not have the follow-up.

| # | fact | where from |
|---|---|---|
| H1 | A hook that fires inside a helper agent gets the MAIN session's `session_id` and `transcript_path`, plus `agent_id`. The helper's rows go to `<session>/subagents/agent-<id>.jsonl`, not to the main file (real file: 0 helper rows). When the helper ends the event is SubagentStop, which nothing wires | follow-up fact 1 |
| H2 | A stop writes one `system` row, subtype `stop_hook_summary`. A blocked stop leaves, in this order: the assistant's last text; a `user` row flagged `isMeta` that starts "Stop hook feedback: " and carries the block reason; an `attachment` row of type `hook_blocking_error` (`hookEvent` "Stop", `blockingError` = {`blockingError`, `command`}); then the stop row with a non-empty `hookErrors` list holding the reason; then the continuation. A completed stop has an empty `hookErrors`. Real record: 26 stop rows, 2 blocked | R7: rows 1170 to 1174 of the real record |
| H3 | `stop_hook_active` is false when a turn starts, true after ANY Stop hook blocked, and stays true for the rest of the turn, for every Stop hook, across tool calls. After 8 blocks in a row with no tool call between, the program ends the turn | follow-up fact 2 |
| H4 | Exit status 2 from a hook is a blocking error: at PreToolUse the tool is denied. Any other non-zero status lets the tool proceed. A hook that hits its timeout is cancelled and the tool proceeds. Output that does not start with `{` is plain text and the tool proceeds. A missing script file makes the interpreter exit 2: at PreToolUse that blocks every matched call | follow-up fact 4 and its notes |
| H5 | A matcher made only of letters, digits, `_` and `\|` (for tool events also comma, space, hyphen) is a whole-name list. Anything else is `new RegExp(matcher).test(name)`: a search, not a whole-name match | follow-up fact 3 |
| H6 | The owner's input has four shapes. Typed while idle: a `user` row, string content, `origin.kind` "human" (17 of 17 real owner rows). Typed while the assistant works: an `attachment` row of type `queued_command` with `prompt`, `commandMode` "prompt" and `origin`. A typed slash command: a `user` row `<command-name>/NAME</command-name> <command-message>NAME</command-message> <command-args>ARGS</command-args>` (real: 3 rows for `/model`, with no `origin`); a skill started by a slash command shows as an `isMeta` row that starts `<command-message>` (real: 1; whether it carries the typed arguments is not established). An image-only message: a `user` row with no text block | follow-up fact 5; `PACK/pack/real-row-shapes.md` |
| H7 | Rows reach the file through a queue flushed every 100 ms, and written rows can be withdrawn. On 2026-11-12 the file missed 4 of 14 assistant texts. The Stop hook's input carries the final answer as `last_assistant_message`. PreToolUse has no such field | follow-up fact 6 |
| H8 | The restart notice of the worker process is an `isMeta` `user` row that starts "This session's worker process was restarted". Where local clean-up is on, the file is rewritten at a compaction: the real file begins at the `compact_boundary` row and holds no owner row for its first 67 rows. In the diskless launch mode `transcript_path` is the empty string | follow-up fact 8; quote F1-hook-input |
| H9 | A scheduled delivery is queued by the backend, the program nudges the model, and the stored prompt arrives in the result of a `ReadNotifications` call. One result can carry several notifications (real: up to 12). Each starts with a header line `--- Notification k of N · id: … · origin: LABEL · queued at: … ---`; the body follows verbatim and "may even imitate" the header; "only the count above is authoritative". The label of every trigger fire, a check-in the session set for itself with `send_later` included, is `scheduled trigger (the stored prompt of a routine or task on this account)`. The nudge an idle session gets is a `user` row that starts `<task-notification>` with `origin.kind` "task-notification" (real: 6, each directly after a stop row; one peer message, `isMeta` with `origin.kind` "peer", also directly after a stop row). The nudge a working session gets is a `queued_command` attachment with `commandMode` "task-notification" (real: 1) | follow-up fact 7; R7, R10 |
| H10 | An answered card returns one of three texts: `Your questions have been answered: "Q"="A", "Q2"="A2". You can now continue with these answers in mind.` when every answer is made of the card's own option labels; `The user answered: "Q"="A". Read the answers carefully — they may request clarification, changes, or that you not proceed — and follow what they actually say.` otherwise (free text); `The user did not answer the questions.` Real rows also carry `toolUseResult.answers`. Labels of a multi-select answer are joined by a comma with no space; a label may itself hold a comma | R8; `real-row-shapes.md` |
| H11 | A queued input of mode "task-notification" goes through the prompt-submit hooks like a prompt | follow-up fact 9 (first half) |
| H12 | Real rows carry `uuid`, `timestamp`, `cwd`, `gitBranch`, `isSidechain`; a `tool_result` row carries `toolUseResult` | R7; follow-up probe |

Where a design assumed something these facts show to be false:

| design | assumption | fact | consequence, with the run |
|---|---|---|---|
| A | a blocked stop is followed by the "Stop hook feedback" row | H2: the feedback row and the attachment come BEFORE the stop row | A takes every blocked stop for a completed one. Its fix for FU2-1, F1-2 and PC-4 does not work on the real shape (R11: both FU2-1 lines print allow; R6: F12, F13a, P07), and a merge the owner clicked is denied after any Stop-hook block (R6: M27) |
| A | the retry flag marks this hook's own retry unless the record shows a block | H3 | same runs |
| A | a slash command's arguments are never the owner's word, and a slash command or an image-only row starts no turn | H6; FU2-5 | R11: three of four FU2-5 lines unresolved |
| A | the owner's rows can be told from harness rows by how the text starts | H6: `origin.kind` | a peer message with no known prefix, and a row with no `origin` in a file whose owner rows have one, count as the owner's and grant a merge (R6: T28, T37) |
| A | the trivia allowance can be measured on recorded text | H7 | a long answer that is not in the record passes as trivia (R6: P14) |
| A | a helper's call is recognised as "a noted call whose id is not in the main record" | H1: `agent_id` is in the hook's input | A writes a note for every outward call and needs `tool_use_id`; B's note is written only for helper calls |
| A | listing full names makes the matcher safe "whether the harness anchors it or searches" | H5: it searches | true as far as it goes; this specification anchors the pattern instead (3.3) |
| A and B | a file without stop rows can keep the old boundary: a scheduled delivery closes what came before it | FU2-3 (second half) | the commit and push before a delivery read mid-turn are never judged (R11: both print allow). Resolved by the stretch rule (1.3 S5) |
| B | a wake row means the stretch before it was judged at a completed stop | H9 holds in the real record, but the Stop gate must not depend on it | same run; same remedy |
| B | a free-text card answer starts with the same words as a clicked one | H10 | B reads free text only when the row carries `toolUseResult` (R5: `m_d1_card_free_text_order`) |
| B | a typed slash command has `origin.kind` "human" | H6: the three real `/model` rows have no `origin`; the skill form is `isMeta` | B handles the follow-up's fixture (R11) and ignores the `isMeta` form. Rule in 2.2 |
| A and B | a hook that hangs or is missing cannot let a merge through | H4: a timeout lets the tool proceed | neither prototype has a deadline of its own. Rule in 2.8 |
| A and B | a check-in the owner asked for can be told from the weekly task | H9: same label | both deny (R11, FU2-8). Kept as the default; Q1 |

### 2.2 Every kind of row, and what it is to the gates

`row_events(rows)` gives one event per row. "Strict" file = at least one `user` row carries an `origin` object.
A row with `isSidechain` true is a helper's row whatever else it is.

| row | event | to the gates |
|---|---|---|
| `user`, no `tool_result` block, not `isMeta`, not `isCompactSummary`, `origin.kind` in `OWNER_ORIGIN_KINDS` ("human") | OWNER, may grant | typed by the owner: starts a window, a governance turn and a stretch; carries the owner's word; is the prompt. Text that starts with a command tag is replaced by the command's arguments (the command name when there are none) |
| the same with no `origin`, text that does not start with a harness lead; or no text and an image or document block | OWNER; may grant only in a file that is not strict | as above. In a strict file it starts the turn and can refuse, but grants nothing: the merge then needs a card |
| `user`, no `origin`, not `isMeta`, starts with `<command-name>` or `<command-message>` | ECHO when the name is in `LOCAL_COMMANDS` or a local-command echo or caveat row is within 2 rows; otherwise OWNER as the row above, text = the arguments | `/model` and its like are not the owner's prompt; `/gauntlet ship it` is |
| `user`, `isMeta`, starts with a command tag, and no assistant row, tool result or wake row lies between it and the latest completed stop, interrupt or start of file | OWNER, never grants | a slash command the owner typed while idle, recorded as a harness row (H6): it starts the governance turn and its arguments are classified. Anywhere else such a row is META. NOT RUN: in no prototype |
| `attachment` `queued_command`, `origin.kind` "human", not flagged meta | QUEUED_OWNER, may grant | sent by the owner mid-turn: no boundary; grants, refuses, is classified; in a scheduled run it makes the rest of the run attended |
| `attachment` `queued_command`, no `origin`, `commandMode` "prompt" | QUEUED_OWNER, never grants | can refuse, cannot grant |
| `attachment` `queued_command`, anything else | QUEUED_WAKE | a notification queued mid-turn: not the owner, no boundary |
| `user` with a `tool_result` block | RESULT | a tool's output. Never the owner, never a click by itself, whatever it quotes. A card answer or a notification read only through the pairing of 2.4 and 2.6 |
| `user`, no `tool_result`, `origin` present and not the owner's (any kind other than "human", or "human" on an `isMeta` row) | WAKE | a row only an idle session receives: ends the window |
| `user`, no `origin`, not `isMeta`, starts with one of `WAKE_LEADS` (`<task-notification>`, `[SYSTEM NOTIFICATION`, `<wake `, `<agent-message`, `<webhook-payload`, `<system-notification`, `<child-session-event`) | WAKE | the same, for a file without `origin` |
| `user`, `isMeta`, starts with `RESTART_LEAD` | WAKE while `RESTART_ENDS_WORD` is True, else META | H8 |
| `user`, `isMeta`, starts with `HOOK_FEEDBACK_LEAD`; `attachment` `hook_blocking_error` with `hookEvent` "Stop" | FEEDBACK | a Stop hook's block reason. Counted per hook by its mark; the two rows of one block are one block |
| `user`, not `isMeta`, starts with `INTERRUPT_LEAD` ("[Request interrupted by user") | INTERRUPT | ends the window |
| `user`, no `origin`, starts with one of `ECHO_LEADS` (local-command output, bash input and output, system reminder) | ECHO | nothing |
| any other `user` row flagged `isMeta` (skill text, re-invocation notes, caveats) | META | nothing |
| `user` `isCompactSummary` | SUMMARY | nothing. Never the owner, never the prompt |
| `system` `stop_hook_summary`, empty `hookErrors` | STOP_DONE | completed stop: ends the window and the stretch |
| `system` `stop_hook_summary`, non-empty `hookErrors` | STOP_BLOCKED | no boundary |
| `system` `compact_boundary` | COMPACT | no boundary; loads before it count or not by `COMPACTION_VOIDS_LOADS` |
| `assistant` | ASSISTANT | what the turn did (tool calls) and said (texts). Never the owner's word |
| any row with `isSidechain` true | SIDECHAIN | never the owner, never a governor load; its tool calls count as outward actions (S13) |
| everything else (`attachment` reminders, `mode`, `last-prompt`, `queue-operation`, other `system` rows) | OTHER | nothing |
| a line that is not JSON, or JSON that is not an object | BAD | kept and counted, never read |

A message the owner typed is the owner's whatever it quotes: a harness lead counts only at the START of a row
(TB-4, PC-1, RI-5). `harness_lead(text)` is the one test, and `govclass` uses it.

### 2.3 Windows, governance turns, stretches

`Model(rows)` computes all three from the events.

- **Window (the merge word, D2).** `auth_start` = the latest OWNER, WAKE, STOP_DONE or INTERRUPT row, or genuine
  scheduled read (while `SCHEDULED_READ_ENDS_WORD`). Owner words are read from there to the end, in order: the
  OWNER row at `auth_start` itself, QUEUED_OWNER rows after it, card answers after it.
  - The window is **scheduled** when it starts at a scheduled read that is not mid-turn. A read is mid-turn when
    the latest OWNER or WAKE row before it is an OWNER row and no completed stop lies between; this can be known
    only in a strict file or a file that has stop rows. A QUEUED_OWNER row that may grant ends the scheduled state.
  - "The assistant stops" (D2) = a completed stop, an interrupt, or the fact that a typed owner message, a wake row
    or a restart notice follows. A blocked stop is not a stop.
- **Governance turn (which loads count).** `run_starts` = for every scheduled read that is not mid-turn, the WAKE
  row that announced it when that row is later than the owner's latest message, else the read itself.
  `gov_start` = the later of the latest OWNER row and the latest run start; `gov_kind` = "owner", "scheduled" or
  "none". A wake after a completed stop does not start a governance turn (`WAKE_TURN_INHERITS_LOADS`).
- **Stretch (what a Stop judges).** `stretch_start` = the later of the latest OWNER row and the latest STOP_DONE
  row, -1 at the start of the file. The stretch is cut into parts at every run start inside it; the first part
  belongs to the governance turn in force at `stretch_start`, each later part to the run that starts it. The
  Stop gate, the receipt gate and the trigger all take the stretch from `stop_span()`, so they judge the same
  rows (TB-5).
- **No owner row** (the file restarts at a compaction boundary): the window holds no owner word, so M6 denies;
  the stretch runs from the latest completed stop or from the start of the file, so S12 judges; `gov_kind` is
  "none", so the prompt-class rule is silent.
- **A file without any stop row**: nothing counts as judged. The whole file after the owner's latest message is
  one stretch (a legacy fixture of the form "owner miss, then a governed scheduled run" is therefore blocked;
  the same fixture with the stop row between the two is allowed, as in a real file).

### 2.4 Card answers: pairing, reading, naming

1. **Pairing.** A `tool_result` block is a card answer only when its `tool_use_id` is the id of a `tool_use`
   block named `AskUserQuestion` that sits in the main thread after `auth_start`, and the block is not
   `is_error`. Nothing is paired by position, and no phrase is searched for in other results (TB-2, F2-4, RI-3).
2. **Reading.** The row's `toolUseResult.answers` (question -> answer; a list value is joined with ",") when
   present. Otherwise the result text when it starts with one of `ANSWER_LEADS` (both texts of H10): for each
   question of the card's OWN input, the text between `"<question>"="` and the last `"` before the next
   question's mark or the end. An answer to a question the card did not ask is dropped. "The user did not
   answer the questions." is no answer.
3. **Chosen options.** The answer is split into the card's own option labels, longest first, where labels are
   joined by ","; an answer that is not made of labels is free text (G11).
4. **`card_ops(question, answer, labels)`**, for each chosen label, after "(Recommended)" is removed and the text
   is normalised (2.5 step 1). `qrefs` = the PRs the question names; "merge question" = the question uses the
   verb as a verb (not "today's merge", "merge conflict", "the merge").
   - the label has a refusal cue (2.5) -> revoke the label's PRs, else `qrefs`, else everything when the label
     or the question is about merging;
   - the label has a deferral cue ("after", "once", "when", "if", "later", "tomorrow") -> revoke as above, grant
     nothing;
   - the label is an order (starts, after an optional "yes", with the verb) or it is a yes
     (`YES_LABEL`: yes, yep, yeah, approve(d), go ahead, proceed, do it, confirm(ed), ok, okay) on a merge
     question -> grant the label's PRs; if it names none: `qrefs` when there is exactly one, or when the label
     has an all-word (`CARD_ALL_WORD`); otherwise nothing;
   - the card names no PR, and the label is a push order or a yes on a question that asks to push, merge, commit
     or land on main, master or the default branch -> grant "default branch";
   - any other option of a merge question -> revoke the label's PRs, else `qrefs`.
   Unchosen options are never read. Free text: `typed_ops(text, fallback)` with fallback = `qrefs` when the
   question is a merge question and names exactly one PR, or the text has an all-word; a bare refusal in free
   text revokes `qrefs`.
5. **Naming a pull request**: `#34`, `PR 34`, `pull request 34`, `pull 34`, `owner/repo#34`, a
   `github.com/owner/repo/pull/34` URL, and lists that continue with "," / "and" / "&" / "+". The last two forms
   bind the repository: a call for another repository's #34 is not covered (F2-2). A word without a repository
   covers that number in any repository.

Spot checks on the reference prototype (R17):
"Shall I merge PR 34 and PR 141?" = "Yes, both (Recommended)" -> grant 34, 141; "Shall I merge #34?" = "Yes" ->
grant 34; "Merge #34 and #141?" = "Yes" -> nothing; "Merge #34?" = "Merge after the audit (Recommended)" ->
revoke 34; "Which workflow should I run?" = "Audit today's merge (Recommended)" -> nothing; "Merge PR #34?" =
free text "merge it, squash please" -> grant 34; "Merge #34 and #141?" = free text "merge it" -> nothing;
"Push the hotfix straight to main (no pull request)?" = "Yes" -> default branch; "Create the weekly
self-improvement task?" = "Yes, Mondays 6:43 am PT (Recommended)" -> nothing.

### 2.5 Typed orders (D1 b): `typed_ops(text, fallback=())`

The result is an ordered list of operations, applied in order to the grant of the window:
`("grant", PRs)`, `("revoke", PRs)`, `("revoke_all",)`, `("branch",)`. Order matters: "Merge #34. No wait."
grants and then empties; "No. Merge #35." empties and then grants.

1. **Normalise** (`normalize`): Unicode NFKC, curly quotes and dashes straightened, lower case. Then fenced code
   and lines that start with `>` are removed.
2. **Sentences**: split at `. ! ? ;` followed by white space, at line ends, and at "but" / "however"
   (`SENTENCE_SPLIT`). A sentence that ends with "?" is a question.
3. **Clauses**: split each sentence at ", ", ": ", " - ", "then", and at "and" when an order follows it
   (`CLAUSE_SPLIT`). In each clause the phrases of `AFFIRMATIVE_PHRASES` ("no objections", "no problem", "why
   not", "no rush", "nothing else", ...) are blanked first: they are not refusals.
4. For each clause, in order:
   a. **Branch order**: the clause starts (after lead-in words) with push / merge / commit / land, names main,
      master or the default branch, names no PR, has no refusal cue and no deferral cue, and the sentence is
      not a question -> `branch`.
   b. **Open negation**: if an earlier clause of the same sentence left a negation open (d) and this clause
      holds any form of "merge" -> revoke the clause's PRs (bare numbers included), or everything when it names
      none; the negation is closed; next clause.
   c. **Order**: the clause starts, after optional lead-in words (`ORDER_LEADIN`: yes, ok, please, now, go ahead
      and, you can, can you, looks good, lgtm, ...), with the bare verb "merge" (also "squash merge",
      "auto-merge", "rebase merge"), and the verb is not a noun use. Then:
      - a deferral cue after the verb -> nothing at all (G5);
      - a question that is not a polite request ("can / could / would / will you ...") -> nothing;
      - the PRs are the list that directly follows the verb (`_object_refs`): PR references, bare numbers that
        end the clause or are followed by a list word or one of `OBJECT_TAIL_WORDS` (now, please, first, ...),
        a parenthesis after a reference is skipped ("#34 (library) and #141 (deck)"), at most
        `OBJECT_FILLER_MAX` other words may come first, and a stop word ends the list ("merge #34 and close
        #35" names 34; "merge the 3 PRs" names none);
      - a refusal cue after the verb splits the rest: PRs before it are granted, PRs after it are revoked and
        not granted ("merge #34, not #141"; "merge everything except #141"); a cue with no PR on either side
        ("merge nothing") -> `revoke_all`;
      - no PR named and no cue: the fallback PRs if any (card free text); otherwise the list stays open, and a
        following clause made only of numbers and list words completes it ("merge both, #34 and #141").
   d. **Refusal**: any other clause with a refusal cue (`REFUSAL_CUE`: no, not, never, none, neither, nothing,
      without, cannot, stop, wait, hold, pause, later, except, skip, leave, until, unless, cancel, abort, any
      word ending in n't, ...): revoke its PRs (after the cue, bare numbers count); if it names none and holds
      a form of "merge" -> `revoke_all`; if it names none, holds no form of "merge", is at most
      `STANDALONE_REFUSAL_MAX_WORDS` (6) words long and starts with a refusal word (`REFUSAL_START`) ->
      `revoke_all` ("No, wait.", "stop", "not yet"). If the clause holds a verb-seeking negator
      (`OPEN_NEGATOR`: do not, don't, never, cannot, can't, won't, shouldn't, mustn't) with no form of "merge"
      after it, the negation stays open for the following clauses of the sentence (b).
5. A revoke only removes. Revoking a number that was never granted does nothing. In a row that may not grant
   (2.2) the grant and branch operations are dropped and the revokes kept.

Spot checks on the reference prototype (R17): "Merge #34." -> grant 34; "merge it", "yes" ->
nothing; "ok, merge 34 and 141" -> grant 34, 141; "Can you merge #34?" -> grant 34; "Is #34 safe to merge?",
"Is #34 merged yet?", "#34 is ready to merge", "why was #26 merged?", "before you merge #34, run the guard" ->
nothing; "Don’t merge #34." (curly), "You can't merge #34 yet.", "Do not merge #34 until I say merge.", "I would
not merge #34", "Please never merge #34" -> revoke 34; "Don't, under any circumstances, merge #34." ->
revoke_all, revoke 34; "Merge #34 once CI is green." -> nothing; "Merge #34, not #141" -> grant 34, revoke 141;
"Merge everything except #141" -> revoke 141; "Merge #34 and close #35." -> grant 34; "merge both, #34 and
#141" -> grant 34, 141; "Merge 34 now" -> grant 34; "merge the 3 PRs" -> nothing; "No objections, merge #34.",
"Yes, why not, merge #34", "Merge #34, no rush", "LGTM - merge #34" -> grant 34; "Merge #34. No wait." -> grant
34, revoke_all; "Merge 34. Leave 141 alone" -> grant 34, revoke 141; "Merge #34 (library) and #141 (deck)." ->
grant 34, 141; "push this to main" -> branch; "don't push to main" -> revoke_all.

### 2.6 Scheduled deliveries

A result is a **notification read** when it is paired by id with a main-thread `tool_use` named in
`NOTIF_READ_TOOLS` (`ReadNotifications`) and is not `is_error`; or when its call row is not in the file at all
(the file was rewritten) and its text starts with `NOTIF_RESULT_LEAD` ("[SYSTEM NOTIFICATION - NOT USER INPUT]").
No other tool's output is ever a notification read, whatever it prints (TB-3, FU2-3).

Inside a notification read, `scheduled_origins(text)` reads the header lines (`NOTIF_HEADER`, the form of H9,
anchored at the start and the end of a line). A header counts only when its number is the next expected one (1,
2, 3, ...) and its total equals the first header's total; a line of the header form anywhere else is body text.
The read is a **scheduled delivery** when a counted header's origin starts with `SCHEDULED_ORIGIN_PREFIX`
("scheduled trigger"). A row or a queued command whose `origin` has kind or subkind "scheduled-trigger" is a
scheduled delivery too (design A reports that pair from the program text; the judge did not re-check it; if the
harness never writes it the rule never fires).

Stated limit: a body that imitates exactly the NEXT expected header takes that header's place. It can make a
GitHub batch look scheduled (the owner's word ends: fail closed), or hide a scheduled header that is not the
first of its batch (the run is then a plain wake: merges stay denied by M6; its commits are judged on the
owner turn's loads). Both need a comment on a subscribed pull request placed in the right batch.

### 2.7 Helper agents

- **Merge gate.** The harness runs the pre-tool hook for a helper's call with the main record (H1), so the
  owner's grant, the window and the scheduled state apply to the helper as to the main session. A helper's rows
  in the main record (older harness) are never the owner's.
- **Stop gate.** When the hook's input carries `agent_id` and the call holds an act the Stop gate counts, the
  pre-tool hook appends one line to the ledger `<state dir>/delegate-<sha1 of the transcript path, 20 hex>.jsonl`:
  `{"t": <epoch seconds>, "rows": <rows in the main record now>, "agent": <agent_id>, "tool": <name>, "kinds": [...]}`.
  The line is written after the merge decision and only when the call was not denied. State dir =
  `$TURNGATE_STATE_DIR`, else `$TMPDIR/turn-gates`, else `/tmp/turn-gates`.
- At Stop, a ledger line counts as an outward act of the stretch when its `t` is later than the `timestamp` of
  the stretch's first row (when that row has one), else when its `rows` is greater than `stretch_start`. It is
  placed at row `rows - 1`. (The time stamp keeps the note usable after the file was rewritten at a compaction;
  NOT RUN: the prototypes place by `rows` only.)
- Limits: a helper's call that was let through and then failed still counts; if the ledger cannot be written
  nothing is counted and nothing is blocked; the ledger is lost with the container. The follow-up's own
  reproduction of FU2-2 runs the Stop hook without first passing the helper's calls through the pre-tool hook,
  so its first line stays "allow" (section 5).
- No SubagentStop hook is wired by this specification.

### 2.8 Which way each failure goes

| failure | merge-class call | any other call | Stop |
|---|---|---|---|
| the hook's input is not JSON | DENY `gate-error` if the raw text matches `CRUDE_MERGE` | allow | allow |
| `turngate` cannot be imported | DENY `gate-error` if tool name or command matches `CRUDE_MERGE` | allow | allow |
| the record path is empty (diskless mode), missing, a directory, empty, or holds no parsable row | DENY `no-record` | allow | allow |
| an exception anywhere after the input was read | DENY `gate-error` if `looks_like_merge()` | allow | allow |
| a shell command the parser cannot read | the text screen `FALLBACK_MERGE_TEXT` decides: a hit is a merge act (number read from the text if there is one), judged by M7 to M9; a hit of `FALLBACK_OUTWARD_TEXT` is an outward act for the Stop gate | no hit: nothing | - |
| the hook is still running `HOOK_DEADLINE_SECONDS` (8) after it started | print the DENY `gate-error` when the crude screen sees a merge route, then exit 0 | exit 0 | exit 0 |
| the script file is missing | decided by the wiring, not by this code (H4): interface in section 4 | | |

Every path of both hooks ends with exit status 0 and either one JSON object or nothing. A hook never exits 2 (it
would block ordinary work, H4) and never relies on a non-zero status to deny (it would not, H4). The deadline is
an alarm set first thing (`signal.alarm` where it exists; a timer thread that prints and calls `os._exit(0)`
elsewhere), shorter than the wired timeout of 10 s. NOT RUN: in no prototype. Test-only switches are not shipped:
no environment variable and no input key changes a verdict; fault tests run a temporary copy of the hooks in
which one function is replaced.

---

## 3. Deciding what a tool call does

`classify_call(tool_name, tool_input, cwd)` returns `(acts, parsed_ok)`. An act has a kind, a route, and where
known a PR number, a repository and a branch.

| kind | meaning | merge gate | Stop gate counts it | advisory treats it as a write |
|---|---|---|---|---|
| `merge` | merges a pull request or switches auto-merge on | gated | yes | yes |
| `push_default` | puts commits or files on a default branch | gated | yes | yes |
| `push` | a push to another branch (note `branch-unknown` when the destination cannot be resolved: M3) | M3 only | yes | yes |
| `commit` | makes a commit | - | yes | yes |
| `pr_write` | creates or updates a pull request, runs a workflow | - | yes | yes |
| `file_push` | writes a file through the GitHub API to a named branch | - | yes | yes |
| `schedule` | creates, changes, deletes or fires a scheduled task or a wake-up | - | yes | yes |
| `outward_other` | other things that leave the machine (comments, reviews, issues, mail, sessions) | - | no (Q6) | no |
| `write` | a local change outside scratch | - | no | yes |

Constants: `MERGE_GATED_KINDS = ("merge", "push_default")`,
`F1_COUNTED_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "file_push", "schedule")`.

### 3.1 Shell commands (tools in `SHELL_TOOLS`: `Bash`, `Monitor`)

The command text is parsed, never pattern-matched as a whole. `parse_shell(text, cwd)` is design B's lexer and
parser (R2: cases R01 to R17 and N01 to N11). It yields every simple command the text would run:

- separators: newline, `;`, `|`, `|&`, `&`, `&&`, `||`, `(`, `)`; a backslash-newline joins lines; `#` at the
  start of a word starts a comment;
- a quoted string is one word and never a command; `$( )`, backticks and `<( )` are parsed as nested commands,
  inside double quotes too; `$VAR` and `${VAR}` are replaced when an earlier `VAR=value` in the same text set
  them (`G=gh; $G pr merge 34`), otherwise the word is marked unresolved;
- here-documents: the body is data, unless the command it feeds is a shell (`bash <<EOF`), then it is parsed; an
  unquoted here-document still runs its `$( )`;
- in front of a command: assignments, shell keywords (`SHELL_KEYWORDS`), and wrappers with their own options
  (`WRAPPERS_WITH_VALUE`: sudo, env, command, exec, nohup, time, nice, timeout N, xargs, ...) are stripped;
- `bash -c "..."`, `sh -c`, `eval ...`, `echo ... | bash`, `cat <<EOF | sh`, `bash <<< "..."`: the text is parsed
  as commands, to depth `MAX_SHELL_DEPTH`;
- `bash file`, `sh file`, `source file`, `. file`, and a command word that ends in `.sh`: the file is read (a
  regular file of at most `SCRIPT_MAX_BYTES`) and parsed. Only shell scripts are read;
- `cd dir` followed by `&&`, `;` or a newline moves the directory for what follows;
- text the lexer cannot read (an unterminated quote, an unmatched parenthesis) raises `ShellParseError`; the
  text screens of 2.8 then decide.

Each simple command is classified by its first word:

| command | reading | act |
|---|---|---|
| `git [global options] <verb>` | global options are skipped (`GIT_GLOBAL_WITH_VALUE`: `-C dir`, `-c k=v`, `--git-dir`, `--work-tree`, ... with their value; any other `-x`); `--help` / `-h` after the verb -> nothing | |
| `commit`, `revert`, `cherry-pick`, `am` (`GIT_COMMIT_VERBS`) | not with `--dry-run`; not `revert` / `cherry-pick` with `-n`, `--no-commit`, `--abort`, `--quit` | `commit` |
| `push` | not with `--dry-run` / `-n`. `--all`, `--mirror`, `--branches` -> `push_default`. Destinations are each refspec's right side (`+` and `refs/heads/` dropped); a default name (`DEFAULT_BRANCHES`, plus the name in the checkout's `refs/remotes/<remote>/HEAD`) -> `push_default`; other named branches -> `push`; `--tags` alone -> `push`. No refspec, `HEAD` or `@`: the current branch, taken in this order: a branch checked out or switched to earlier in the same command text; the `HEAD` file of the checkout in the effective directory (`cd` / `-C` / the hook input's `cwd`; a worktree's `.git` file is followed; no subprocess). If none can be read the act is `push` with note `branch-unknown` | `push_default` / `push` |
| `checkout -b/-B`, `switch -c/-C`, and `GIT_WRITE_VERBS` (add, rm, mv, apply, stash, reset, restore, merge, rebase, tag, clean) | `git merge origin/main` is a local branch sync, not a pull-request merge | `write` |
| `gh [flags] pr [flags] merge [n or URL]` | flags before and between the words are skipped (`GH_GLOBAL_WITH_VALUE`); `--help` -> nothing; the number is the first positional (a URL names the repository too; a branch name or nothing -> number unknown); `--auto` is the same act; `--disable-auto` -> `pr_write` | `merge` |
| `gh pr create / edit / close / reopen / ready / update-branch` (`GH_PR_WRITE_SUBS`); `gh workflow run` | | `pr_write` |
| `gh pr comment / review / lock / unlock`; `gh issue / release / repo / label / secret / variable / gist / ruleset <verb that is not a read>` | | `outward_other` |
| `gh api [flags] <path>`; `curl` / `wget` to a host in `GITHUB_API_HOSTS` or a path with `/api/v3/` | method from `-X` / `--method` / `--request` (also `--method=`), else POST when a body flag is present (PUT for an upload), else GET. GET and HEAD -> nothing | |
| path `repos/o/r/pulls/N/merge` | | `merge` (PR N, repository o/r) |
| path `graphql` | body with `GRAPHQL_MERGE` (mergePullRequest, enablePullRequestAutoMerge, enqueuePullRequest), or a body that cannot be read -> `merge`, number unknown; body with `GRAPHQL_REF` (mergeBranch, createCommitOnBranch, updateRef, createRef, deleteRef) -> `push_default`; any other mutation -> `outward_other` | |
| path `repos/o/r/merges`, `.../git/refs[/heads/b]`, `.../contents/...` | branch from the path or from the body's `branch` / `base` / `ref`; none or a default name -> `push_default`, else `push` / `file_push` | |
| path `repos/o/r/pulls` or `pulls/N[/update-branch]` | | `pr_write` |
| any other write method on the API | | `outward_other` |
| `SHELL_WRITE_COMMANDS` (cp, mv, install, rsync, tee, touch, mkdir, rm, rmdir, ln, truncate, patch); `sed -i`, `perl -i`; a `>` / `>>` redirection | unless every target is under scratch: `SCRATCH_DIRS` (`/tmp/`, `/var/tmp/`, `/dev/`, `/proc/`) and `$TMPDIR`, after the path is made absolute and normalised (`/tmp/../home/...` is not scratch) | `write` |
| a command word that is an unresolved expansion; anything else (`grep`, `echo`, `cat`, `python3`, ...) | | nothing |

`xargs` in front of the merge command: the number comes from standard input -> number unknown (M7).

Was the act taken? (Stop gate only, `Model.outward`.) A counted act is dropped when the call's result shows it
did not happen: the result row has `toolDenialKind`, or its text starts (first 600 characters) with a denial
phrase (`DENIAL_TEXT`: this gate's own "TURN-GATE", a hook block, the permission prompt's rejection); or the
result is `is_error` and the tool is not a shell tool; or the result is `is_error`, the command is one and-chain
and the act is its last step. A call with no result yet counts.

Stated limits: a program in another language that merges through a library or a subprocess is not seen; a script
that changed between the call and the stop is read as it is at the stop; a `for` loop over directories is not
unrolled, so a push inside it has no readable destination (R15: 3 such pushes in the real record; M3 and Q2).

### 3.2 Tools by name (every name in `PACK/pack/session-tools.txt`)

For a name that starts with `mcp__` the leaf (the part after the last `__`) is matched exactly, so both GitHub
servers (`mcp__github__` and a second GitHub connector) and any later server with the same leaves are covered. Built-in names
match exactly.

| class | tools | constant | act |
|---|---|---|---|
| merge routes | `merge_pull_request`, `enable_pr_auto_merge` (number from `pullNumber` / `pull_number`, repository from `owner` + `repo`) | `MERGE_TOOL_LEAVES` | `merge` |
| file pushes | `push_files`, `create_or_update_file`, `delete_file` | `FILE_PUSH_LEAVES` | `file_push`, and `push_default` when `branch` is absent or a default name |
| pull-request writes | `create_pull_request`, `update_pull_request`, `update_pull_request_branch`, `disable_pr_auto_merge`, `actions_run_trigger` | `PR_WRITE_LEAVES` | `pr_write` |
| scheduling | `create_trigger`, `update_trigger`, `delete_trigger`, `fire_trigger`, `send_later` (leaves); `CronCreate`, `CronDelete`, `ScheduleWakeup` (built-in) | `SCHEDULE_LEAVES`, `SCHEDULE_TOOLS` | `schedule` |
| other outward, not counted (Q6) | GitHub: `create_branch`, `create_repository`, `fork_repository`, `delete_repository`, `issue_write`, `sub_issue_write`, `add_issue_comment`, `update_issue_comment`, `pull_request_review_write`, `add_comment_to_pending_review`, `add_reply_to_pull_request_comment`, `request_copilot_review`, `resolve_review_thread`, `unresolve_review_thread`. Sessions: `create_session`, `send_message`. Mail and drive: `send_message`, `reply`, `forward`, `create_draft`, `create_file`, `update_file`, `share_file`, `trash_file`, `copy_file` | `OTHER_OUTWARD_LEAVES` | `outward_other` |
| file writes | `Edit`, `Write`, `NotebookEdit`, outside scratch | `WRITE_TOOLS` | `write` |
| shell tools | `Bash`, `Monitor` | `SHELL_TOOLS` | parsed (3.1) |
| read by the turn model, never gated | `AskUserQuestion` (cards), `ReadNotifications` (deliveries), `Skill` (governor loads; the name after the last ":" must be in `GOVERNORS`) | `CARD_TOOL`, `NOTIF_READ_TOOLS`, `GOVERNORS` | - |
| everything else | every `get_*`, `list_*`, `search_*`, `*_read`, `read_*` tool, `Read`, `Grep`, `Glob`, `WebFetch`, `WebSearch`, `ToolSearch`, `Agent`, `Task`, `Workflow`, artifact, environment and connector tools | | nothing |

### 3.3 The matcher in the settings files

The turn-gate group of PreToolUse in `lib/.claude/settings.json`, in the kit's and the deck's settings, and in the
plugin's `hooks/hooks.json` must read (one line):

```
^(Edit|Write|NotebookEdit|Bash|Monitor|CronCreate|CronDelete|ScheduleWakeup|mcp__.*__(merge_pull_request|enable_pr_auto_merge|disable_pr_auto_merge|create_pull_request|update_pull_request|update_pull_request_branch|push_files|create_or_update_file|delete_file|actions_run_trigger|create_trigger|update_trigger|delete_trigger|fire_trigger|send_later))$
```

The pattern holds `^ ( ) . * $`, so by H5 the program applies it as a regular expression, and the anchors make
the search a whole-name match: a tool whose name merely contains "Edit" or "Bash" is not selected. NOT RUN
against the program's own matcher code; the follow-up's `PACK/work/followup-2/tools/matcher.js` re-types that
rule and is the tool for the wiring test (W01 in section 6). The first PreToolUse group (the two reminders) is
unchanged. No new hook event is wired.

---

## 4. The module interface (`hooks/turngate.py`)

Three layers, each testable alone: rows -> events; events -> `Model`; call -> acts. Decisions read only the
last two. Nothing raises to the caller on bad input except `parse_shell` (caught inside `shell_acts`).

| name | arguments -> result | note |
|---|---|---|
| `load(path)` | -> list of rows; `[]` on any error; a line that is not a JSON object becomes `{"type": "BAD"}` | |
| `normalize(text)` | -> the normal form used by every word test | `govclass` uses it too |
| `harness_lead(text)` | -> True when the text STARTS with a harness lead | the one test for "is this a harness text"; `govclass` and the trigger use it |
| `command_args(text)` | -> a slash command's arguments, or its name when it has none | |
| `row_events(rows)` | -> `(events, uses, results, facts)`. `uses`: tool_use id -> (row, block index, block, is_helper). `results`: id -> (row, block, result row), paired by id only. `facts`: `strict`, `bad`, `has_stop_rows` | design B's `classify(rows)`, renamed; no pairing by position |
| `scheduled_origins(text)` | -> origins of the counted headers of one notification read | 2.6 |
| `typed_ops(text, fallback=())` | -> ordered operations | 2.5 |
| `card_answers(use_block, result_block, row)` | -> `[(question, answer, labels)]` | 2.4 steps 1 to 3 |
| `card_ops(question, answer, labels)` | -> ordered operations | 2.4 step 4 |
| `Model(rows)` | attributes `evs`, `uses`, `results`, `facts`, `owner_rows`, `last_owner`, `stops_done`, `sched_reads`, `run_starts`, `auth_start`, `window` ("owner", "scheduled", "unattended"), `gov_start`, `gov_kind`, `stretch_start` | 2.3 |
| `Model.authorization()` | -> `{"prs": set of (repo or None, number), "default_branch": bool, "scheduled": bool, "attended": bool, "log": [...]}` | the fold of 2.5 over the window |
| `Model.loads(after, before=None)` | -> `[(row, block index, governor)]`, error results excluded | S14, S15 |
| `Model.outward(after, ledger=())` | -> `[(row, block index, act)]` of counted acts that the record does not show failed; sets `Model.dropped` | 3.1, 2.7 |
| `Model.feedback(after, mark=None)` | -> rows where a Stop hook's block was fed back and work followed; with `mark`, only blocks whose reason satisfies it; the two rows of one block count once | H2 |
| `Model.prose(after, last_message=None)` | -> the assistant's texts after `after`, plus `last_message` when the record does not hold it | H7 |
| `Model.owner_prompts()` | -> texts the prompt-class rule classifies | P8 |
| `stop_span(rows_or_model)` | -> `(first row of the stretch, row count)` | TB-5 |
| `parse_shell(text, cwd=None)` | -> simple commands; raises `ShellParseError` | 3.1 |
| `shell_acts(text, cwd=None)`, `classify_api(method, path, body)`, `classify_call(name, input, cwd=None)` | -> acts (the first and last with `parsed_ok`) | 3 |
| `looks_like_merge(name, input)` | -> bool, the crude test of the error paths | 2.8 |
| `merge_decision(model, acts, agent_id=None)` | -> `(allow, code, reason)`; codes `ok`, `no-record`, `branch-unknown`, `scheduled`, `delegate`, `no-owner-word`, `target-unknown`, `merge-word`, `default-branch` | table 1.2; the one place the merge rule lives |
| `f1_decision(model, ledger=(), stop_hook_active=False)` | -> `(block, missing, kinds)` | table 1.3 |
| `ledger_path(transcript_path)`, `ledger_add(...)`, `ledger_read(transcript_path)` | | 2.7 |
| `python3 turngate.py span <transcript> [last message]` | prints `{"start", "rows", "gov_start", "gov_kind", "texts", "blocks": {"any": n, "by_mark": {...}}}` | for shell hooks |
| kept names: `owner_index`, `turn_start`, `scheduled_index`, `owner_text`, `events`, `skill_name`, `is_merge`, `is_outward`, `is_write`, `merge_target`, `says_merge`, `answer_choices`, `merge_authorized`, `_text`, `HARNESS_MARKERS` | same call shapes, answered from the model | `PACK/pack/tools/replay_real.py` and `governance-trigger.py` import them |

How the hooks call it. Pre-tool: read the input; `classify_call`; nothing gated and nothing to remind -> exit
without reading the record; `load`, `Model`, `merge_decision`; on allow, `ledger_add` for a helper call; then the
advisory from `Model.loads` and `Model.prose`. Stop: `load`, `Model`, `ledger_read`, `f1_decision`; then the
prompt-class rule from `Model.owner_prompts`, `govclass.classify`, `Model.loads`, `Model.prose(…,
last_assistant_message)`, `Model.feedback`.

What the other assignments get, and what they must do with it:

| who | interface | must |
|---|---|---|
| receipt gate | `stop_span` and `Model.prose(start - 1, last_assistant_message)`, or the `span` command line | judge that stretch (TB-5, RL-7); read the answer from the hook input when the record lacks it (FU2-9); count its own blocks with `Model.feedback(stretch, mark)` on its own mark "Receipt law" and never treat `stop_hook_active` alone as "my retry" (FU2-1, RL-2) |
| trigger | `Model.gov_start`, `Model.gov_kind`, `harness_lead(prompt)` | stay silent for a prompt that is a harness notification (H11); follow the scheduled-run boundary (TR-4) |
| classifier | `harness_lead`, `normalize` | drop only a prompt that STARTS with a harness lead; keep one list of leads (import it); fix the word lists of PC-2 and PC-3 (disputes worded as reviews must classify as dispute so that P5 does not reach them; chat, status questions and negated orders must classify as nothing); keep `classify(text) -> list`, `ENFORCED`, `GOVERNORS_FOR` |
| registry | every upper-case module-level name of the three files (7.4) | read them from the code; regular-expression flags are part of the value |
| wiring | the matcher of 3.3 in four files; one ledger file and the advisory's marker files in the state dir | decide what a missing script does (H4). Recommended: two groups, the merge-route tool names with the bare command (a missing file then denies those calls) and every other name behind a file test that exits 0 when the script is missing |
| weekly task and plugin | nothing from this module | F2-6, WR-1, CB-1 and FU2-7 stay true until the account serves the fixed plugin (section 5) |

---

## 5. Every finding in scope: what resolves it, and its red-first test

Test names: `T.. M.. R.. N.. S.. G.. X.. F.. P.. A..` are design B's cases (`J/b/tests/test_core.py`, fixtures in
`FIX/design/core-design-b/fx/`); `m_.. s_.. p_.. a_..` are design A's (`J/a/tests/cases.py`, fixtures in
`FIX/design/core-design-a/fixtures/`); `J..` and `W01` are new and listed in 6.2. "Red" = the merged hooks give
another verdict than the one wanted (R1, R2). A case of design B is red unless it is named in 6.1 as not red.

| finding | resolved by | red-first tests |
|---|---|---|
| TB-1, F2-7, FU2-6 | M2 and M6: a record with no owner word denies a merge instead of leaving the hook; S12: the stretch is judged without an owner row | T22, T23a, T23b, T23c, T21b; F20. Follow-up reproduction: all FU2-6 lines print the required verdict (R13) |
| TB-2, F2-4, RI-3 | 2.4 step 1: a card answer is the result of its own AskUserQuestion call, paired by id; no phrase is searched for | M09, M10, M11, M18, M19 |
| TB-3, FU2-3 | 2.6: only a real notification read can hold a scheduled header, and only a counted header counts; S5: nothing before a delivery read mid-turn is left unjudged | S08, S09, F17, F18, F19a, J02. The follow-up's two merge lines still print deny: their fixture puts the idle-session nudge (a wake row) after the owner's order, and D2 ends the word there. The denial code is `no-owner-word`, not `scheduled`. With the mid-turn shape of H9 the merge is allowed (S09) |
| TB-4, RI-5, PC-1 | 2.2: a harness lead counts only at the start of a row; `origin.kind` where the file has it | T17, T18, F21, P02a, P02b, P03 |
| TB-5 | not in these three files. Interface: `stop_span`, `Model.prose` (section 4) | J17 (the span equals the stretch the Stop gate judges); the receipt gate's own test belongs to its assignment |
| TB-6 | D2 decides it: a wake row ends the window | M16, T30, G02 |
| TB-7, PC-5 | P1 and P2 | P04a, P04b, P05 |
| TB-8, F1-7, PC-7 | the standing list of deliberate breaks (6.3) | one break per recorded mutation: table in 6.3 |
| F2-1 | G13: the assistant's text grants nothing (the third route is withdrawn by D1); a refusal revokes | T03, T04, M04, M24 |
| F2-2, RI-4 | grants are sets of named PRs (and repositories); G4, G8; the window ends at a stop (D2) | T01b, T05a, T11a, M02, M03a, M03c, M05, M13b, T16d, T35, M16 |
| F2-3, RI-1 | 2.5: normalised apostrophes, refusal cues, the open-negation rule, deferral, questions | T05e, T06, T07, T08, T10, M06, M25, `m_ri1_far_negation` |
| RI-2 | the verb is the bare word "merge"; "merged" and "merging" never grant | T09, M26 |
| F2-5, RI-7, WR-2 | D3: auto-merge and pushes to a default branch are merge-class; the shell parser reads commands, flags, REST and GraphQL routes, scripts | R01a, R02, R03, R05, R06, R07, R08, R09a, R09b, R10a, R10c, R13; in a scheduled run S02 to S07 |
| F2-6, WR-1, CB-1 (first half), FU2-7 | NOT FIXED BY THESE FILES: the account serves plugin 0.1.4, which has no scheduled-run rule. It is fixed when the owner uploads the plugin built from the fixed hooks ("Once, after the fix"). Until then "a scheduled run never merges" does not hold in the session the weekly task fires into | S01 to S07 run against the plugin copy after the re-sync (surfaces assignment); the weekly task stays off until the owner's word |
| CB-1 (second half) | as F2-5 | S02 to S07 |
| F2-8 | (c) a search is not a merge: the parser; (d, e, f) a "no" or "not" in another clause does not negate the order: 2.5 step 3 and 4d; (g) a yes on a merge card that names the PRs: G6, G7; number without "#": 2.4 step 5. (a, b) a bare "yes" after the assistant's offer, and (h) an order followed by a second typed message: NOT allowed any more, by D1 and D2. (j) an order followed by a scheduled reminder: denied by default, Q1 | N01, N10; `m_f2_8d_no_objections_merge`, `m_f2_8f_yes_why_not_merge`, `m_f2_8g_card_yes_both` (red in R1; pass on the reference prototype, R12); T13, T34, M08 pin the number forms |
| RI-6, F1-3, F1-4, SF-3 | 3.1 and 3.2: git options before the verb, revert and cherry-pick, the command-line PR verbs, API writes, script files, a second shell tool; auto-merge, branch update, workflow run and every scheduling tool are counted; the matcher of 3.3 sends them to the hook | F02, F03a, F03b, F04, F05-send-later, F05-cron-create, F05-cron-delete, F05-auto-merge, F05-update-pr-branch, F05-fire-trigger, F06a, F06b, `s_f1_4_monitor_tool_push`, `s_f1_3_tool_actions_run_trigger`, W01 |
| RI-8, F1-6, ADV-4 | commands are parsed: a mention is not an act; dry runs, help pages, denied and failed calls are not acts; the scratch test normalises paths; the advisory is spent only on a real write | N01 to N06, N10, F07a to F07e, F08a, F08b, A02a, A02b, A03a, A03b, A04, A05, A06 |
| F1-1, FU2-2 | 2.7: the pre-tool hook notes a helper's outward call (it has `agent_id`, H1); the Stop gate counts the note; helper rows in the main file count | F09, F10, G01a, G01b, G02, G03. The follow-up's first FU2-2 line runs the Stop hook without passing the helper's calls through the pre-tool hook, so it still prints allow (R13); F09 does both steps |
| F1-2, PC-4, FU2-1 | S6 to S9, P6: the retry flag decides nothing; own blocks are counted from the record in its real order (H2) | F12, F13a, P07, J01. Follow-up reproduction: both governance lines of FU2-1 print block:F1 (R13). P06 pins the single retry of the prompt-class rule (Q3) |
| F1-5 | S10: the stretch starts at the latest completed stop; an earlier miss is not raised again | F11c, F11d, F34. Real record: the second stop of 2026-10-21T23:26 turns from a block into an allow (R14) |
| F1-8 | S14 (an errored Skill call is no load); S15 keeps loads across a compaction (Q4) | F14; F15 pins the default |
| PC-2, PC-3 | NOT IN THESE FILES: the classifier's word lists. What the gate needs from them is in section 4 | P10a and P10b pin the gate's side of the allowance |
| PC-6 | S12 for the outward rule; P1 for the prompt-class rule (with no owner row there is no prompt to classify) | F20; P12 pins P1 |
| PC-8 | P10, Q5 | P13 pins the default |
| ADV-1 | A2: the advisory says the record does not keep every message; it stays advisory, because PreToolUse has no copy of the unrecorded text (H7). The miss itself is not removed | `a_adv1_advisory_states_its_limit` |
| FU2-4 | 2.2: a message sent mid-turn is the owner's; it grants, refuses and is classified | T19, T20, T20c, T20b, J13. Follow-up reproduction: all lines print the required verdict (R13) |
| FU2-5 | 2.2: a typed slash command and an image-only message start a turn; the arguments are the owner's word | T21a, P15, T36, J03. Follow-up reproduction: all four lines print the required verdict (R13) |
| FU2-8 | default: the check-in is a scheduled run and a wake-up (D2, D3): denied. Q1 | the follow-up's fixture `fu8-send-later.jsonl` as S16-check-in: deny `scheduled` (R13) |
| FU2-9 | P5 uses `last_assistant_message`; the receipt gate's own reading is its assignment (interface in section 4) | P14 |

Not fixed, in one list: F2-6, WR-1, CB-1 (first half), FU2-7 (the account plugin; needs the owner's upload);
PC-2, PC-3 (classifier word lists); TB-5 and FU2-9 for the receipt gate itself (interface only); ADV-1 (the
advisory cannot see unrecorded text); F2-8 parts a, b, h, j, FU2-8 and the two merge lines of FU2-3 (the wanted
verdict was "allow" under the old rule; D1, D2 and D3 make it "deny").

---

## 6. The test plan

### 6.1 The test table

One table, design B's (`test_core.py`), in the real row shapes of H2, H6, H9, H10 and H12. Its builder
(`J/b/tests/mkx.py`: `owner`, `slash`, `wake`, `queued`, `stop`, `blocked_stop`, `say`, `tool`, `res`, `call`,
`bash`, `skill`, `card`, `read_notifs`, `compaction`) is built on `PACK/pack/tools/mk.py` and ships as
`hooks/selftest_rows.py`. Two changes to the builder: `blocked_stop` writes its rows in the order of H2
(feedback row, attachment, stop row), and a card answered with free text writes the second text of H10.
Each case is: name, findings, wanted verdict, rows, call. Each runs on the merged hooks and on the fixed
hooks; both verdicts are recorded (R2 is that record for design B's prototype).

Design B's 254 cases stay, with these wanted verdicts changed by this specification:

| case | was | is | why |
|---|---|---|---|
| M07-click-yes-both-strict-reading | deny | allow | G6, G7; F2-8 |
| R09h-bare-push-branch-unreadable | deny | allow (attended); J09 covers the unattended twin | M3, Q2 |
| F19c-legacy-owner-push-then-scheduled-run-loads-both | allow | block:F1; J11 covers the twin with the stop row | S5; FU2-3 |
| M23, M09b, S13, F16c, P04b and the other cases built from unpaired `mk.answer` / `mk.notif` rows | as they are | the same verdicts, rebuilt with paired ids; an unpaired card answer is no click | 2.4 step 1 |
| X05a to X05d | fault by environment variable | fault by a temporary copy of the hooks with one function replaced | 2.8 |

Design B's cases that are NOT red on the merged hooks although not marked control (R2; 78 cases), kept as pins of a rule that already held or of a default: M07-click-yes-both-strict-reading, M08-number-without-hash-in-question, M27-blocked-stop-is-not-a-stop, M12-card-dismissed, M13-multiselect-two-merge-labels, M14-free-text-answer-merge-it, M15-free-text-answer-not-yet, M20-card-click-inside-scheduled-run, M21-card-click-after-github-wake, T05c-dont-merge-26-comma-merge-27, T13-please-merge-pr-34-and-pr-141, T14-can-you-merge-34, T16c-merge-34-before-141-names-both, T16e-merge-34-library-and-141-deck, T20b-queued-notification-is-not-owner, T21a-slash-command-args-order, T24-compaction-midturn-keeps-order, T25-compact-summary-is-not-owner, T26-meta-row-is-not-owner, T27-task-notification-is-not-owner, T33-interrupt-after-order, T34-url-names-the-pr, R04a-gh-number-last, R09d-git-push-main-with-word, R11-gh-merge-auto, R14a-bash-c, R14b-eval, R14c-command-substitution, R14d-echo-piped-to-shell, R14e-heredoc-to-shell, R15a-wrappers, R15b-and-chain-subshell, R17-unparseable-with-route-words, N07-view-json-mergeable, N09-api-get-merged-state, N11-unparseable-without-route-words, S10a-midturn-scheduled-read-ends-earlier-word, S11-owner-types-after-scheduled-run, S14-origin-words-in-body-not-header, G01a-helper-merge-with-live-word, G01b-helper-merge-without-word, X01b-payload-not-json-plain, X02b-transcript-is-a-directory-edit, X04b-shared-module-missing-bash-ls, X05b-internal-error-edit-is-allowed, X05d-internal-error-commit-is-allowed, F10-sidechain-rows-in-main-file, F11b-chain-stop2-remedied, F13b-third-stop-is-let-go, F13c-retry-flag-without-any-block-on-record, F15-loads-before-compaction-count-by-default, F19c-legacy-owner-push-then-scheduled-run-loads-both, F22-loads-of-previous-turn-do-not-count, F23-commit-and-push, F24a-git-C-commit, F24b-gh-pr-create, F24c-push-files, F24c-create-or-update-file, F24c-delete-file, F24c-create-trigger, F24c-update-trigger, F24c-delete-trigger, F24c-update-pull-request, F24c-create-pull-request, F24c-merge-pull-request, F25-skill-args-mention-governor, F26-block-reason-carries-the-remedy, F28-two-scheduled-runs-latest-governs, F29-owner-message-after-scheduled-run, F33-wake-turn-inherits-owner-turn-loads, P06-single-retry-understood, P08-compact-summary-is-not-the-prompt, P09-every-class-needs-its-governor, P10a-allowance-is-review-only, P11-loads-before-the-prompt-do-not-count, P12-no-owner-row-two-writes, P13-build-ordered-by-click, P17-owner-prompt-after-a-scheduled-run. Of these, T16e-merge-34-library-and-141-deck fail(s) on design B's own prototype (R2) and pass(es) on the reference prototype (R12). That list is by design B's own wanted verdicts. With the verdicts changed in the table above, M07 and F19c become red on the merged hooks (it denies the click, and allows the legacy file) and R09h stops being red (the merged hooks allow it).

Added from design A (rebuilt with the builder above; all red in R1 unless marked control there):
`m_f2_8d_no_objections_merge`, `m_f2_8f_yes_why_not_merge`, `m_f2_8g_card_yes_both`,
`m_d1_card_free_text_order`, `m_d1_card_free_text_refusal`, `m_same_clause_not_141`, `m_ri1_far_negation`,
`m_conditional_order_is_not_for_now`, `m_bare_number_quantity_is_no_pr`, `m_question_form_is_no_order`,
`m_ready_statement_is_no_order`, `m_card_several_prs_label_names_none`, `m_card_result_is_error`,
`m_queued_stop_revokes_all`, `m_queued_second_message_keeps_word`, `m_d2_midturn_notification_keeps_word`,
`m_d3_local_merge_then_push_main` (the branch switched earlier in the same command), `m_d3_cli_global_repo_flag`,
`m_cli_merge_through_monitor_tool`, `s_f1_4_monitor_tool_push`, `s_f1_4_release_script`, `s_f1_4_cherry_pick`,
`s_f1_3_tool_actions_run_trigger`, `s_f1_3_tool_disable_pr_auto_merge`, `s_f1_6_single_push_failed`,
`s_f1_6_commit_rejected_at_prompt`, `p_queued_message_is_classified`, `p_ctl_assistant_skill_args_are_not_a_prompt`,
`p_ctl_review_with_tool_is_not_trivia`, `a_adv1_advisory_states_its_limit`. Design A's cases whose wanted verdict
this specification does not take: `m_slash_args_never_grant` (FU2-5),
`s_s1_owner_miss_then_scheduled_run_governed` (S5), `s_pc4_d2_understood_loads_nothing` (Q3).

Of the design A cases named above, these are not red in R1 (controls or pins): `m_d1_card_free_text_refusal`, `m_queued_second_message_keeps_word`, `m_d2_midturn_notification_keeps_word`, `p_ctl_assistant_skill_args_are_not_a_prompt`, `p_ctl_review_with_tool_is_not_trivia`, `s_s1_owner_miss_then_scheduled_run_governed`.

### 6.2 New cases (written first; "before" = merged hooks)

| case | fixture, in builder terms | before | after | status |
|---|---|---|---|---|
| J01-blocked-stop-real-order | pre-tool: `owner("ok")`, card "Merge #34?" = "Merge #34", `say`, the feedback row, the attachment, `stop(reason)` in that order (H2), `say`; merge #34. Stop twin: `owner("Continue")`, `say`, the same three rows with a receipt reason, commit, push, `say`; retry flag true | allow / allow | allow / block:F1 | R18 |
| J02-midturn-delivery-with-idle-nudge | the follow-up's `fu3b-real-sched-f1.jsonl`: `owner("Continue")`, commit and push, a `<task-notification>` wake row, a scheduled read, `say("done")` | allow | block:F1 | R18; R11 (A and B allow); R13 |
| J03-meta-slash-command-starts-turn | a governed turn ending in `stop()`; an `isMeta` row `<command-message>go</command-message>…<command-args>build the exporter</command-args>`; a Write; `say` | allow | block:prompt-class; with a commit instead of the Write: block:F1 | NOT RUN |
| J04-deadline | a copy of the hooks whose `load` sleeps 20 s; merge tool / Edit / Stop | (no such path) | deny `gate-error` within 9 s / allow / allow | NOT RUN |
| J05-open-negation, J06-order-then-refusal, J07-affirmative-no | `owner("Don't, under any circumstances, merge #34.")` / `owner("Merge #34. No wait.")` / `owner("Merge #34, no rush")`; merge #34 | allow / allow / allow | deny / deny / allow | R18. A case whose two verdicts are equal is a pin, not a red-first test |
| J08-yes-on-card-with-two-prs | card "Merge #34 and #141?" = "Yes"; merge #34 | deny | deny | R18 |
| J09-unresolved-push-unattended | a scheduled run, then `cd "$REPO"` and a bare push. Attended twin (design B's R09h): `owner("ok")`, the same command | allow / allow | deny / allow | R18 |
| J10-push-main-needs-branch-word | card "Merge #34?" = "Merge #34"; a push of HEAD to main | allow | deny | R18; design B's R09g |
| J11-run-after-owner-miss | `owner("push it")`, a push, `say`, then a governed scheduled run. First verdict: with `stop()` and the wake row between. Second: with the wake row only, no stop row in the file | allow / allow | allow / block:F1 | R18 |
| J12-free-text-answer-second-form | card "Merge PR #34?" answered with the second text of H10 (`The user answered: ...`), no `toolUseResult`; merge #34 | deny | allow | R18 |
| J13-queued-prompt-is-classified | `owner("status?")`, `say`, `queued("Build a script that ...")`, a Write, `say` | allow | block:prompt-class | R18 |
| J14-helper-advisory-silent | plan-gate loaded, no plan text; Edit with `agent_id` in the input | advise | allow | NOT RUN |
| J15-diskless | `transcript_path` = ""; merge tool / Edit | allow / allow | deny / allow | R18 |
| J16-ledger-after-rewrite | a ledger line whose `rows` is larger than the record, with `t` later than the stretch's first row | allow | block:F1 | NOT RUN |
| J17-span-equals-stretch | for every Stop fixture: `stop_span` = the stretch `f1_decision` judged | - | equal | NOT RUN |
| J18-imitation-of-the-next-header | a 2-notification read whose first body holds a line of the form "Notification 2 of 2 … scheduled trigger" | - | scheduled (pins the stated limit of 2.6) | NOT RUN |
| W01-matcher | from the constants of 3.2, every classified name in `session-tools.txt` matches the pattern of 3.3 and no read-only name does, under the rule of H5 (`matcher.js`) | 12 classified names are not selected. Read from the merged matcher's text (its alternation names six leaves, and by H5 it is a search, so `update_pull_request_branch` is selected): Monitor, CronCreate, CronDelete, ScheduleWakeup, enable_pr_auto_merge, disable_pr_auto_merge, actions_run_trigger, create_trigger, update_trigger, delete_trigger, fire_trigger, send_later. The follow-up's table (`PACK/work/followup-2/out/matcher.json`) confirms the built-in ones: Monitor, CronCreate, CronDelete, ScheduleWakeup | all selected | NOT RUN |

### 6.3 Keeping the tests honest: the standing list of deliberate breaks

`hooks/selftest-mutations.py` holds the list. Each break is one text replacement in one of the three files; the
guard applies each alone to a copy and runs the test table; a break that leaves every case passing fails the
guard, and so does a break whose text is no longer found. The control (no change) must show 0 failing cases:
design B's run does not meet that today (R4), because T16e fails on its prototype.

The list is the union of design B's 55 (`J/b/tests/mutate.py`, R4) and design A's 84 (`J/a/tests/mutate.py`,
R3), re-targeted at the final code, plus one break for every rule new in this specification. One break for
every mutation recorded in the findings:

| recorded mutation | break (B's list / A's list) | a case that catches it (R3, R4) |
|---|---|---|
| TB-8 M1, reimpl M10: no owner row, merge allowed | N01 / B01, B01a | T22; `m_f2_7x_record_missing` |
| TB-8 M2, PC-7 M4: a summary or a meta row is the owner | N02a, N02b / B02, B35 | T26, F15; `m_tb1_file_starts_at_compaction` |
| TB-8 M3: the first scheduled run governs | N03 / B03b | F28 |
| TB-8 M4, reimpl M8: header form dropped | N04 / B04 | S09, M21 |
| TB-8 M5: a past run outranks a later owner message | N05 / B05, B05b | P17; `s_tb8_m5_owner_message_after_scheduled_run` |
| TB-8 M6, reimpl M7: any tool result is a click | N06, N41 / B06 | M09b, M18; `m_tb2_read_of_selftest_file` |
| TB-8 M10: the prompt-class half ignores the run boundary | N07 / B71 | P04b |
| TB-8 C2: a notification row is the owner | N51 | M20 |
| TB-8, the receipt gate's mutations | not in these files | the receipt assignment |
| F1-7 M1a, M1b, M1c: tool families no longer outward | N08, N09, N10 / B20, B21, B21b, B22 | R10a, F05-send-later, F05-update-pr-branch |
| F1-7 M2: the command-line PR create no longer outward | N11 / B23 | F24b, F06a |
| F1-7 M3, reimpl M13: git options hide the verb | N12 / B19 | F02 |
| F1-7 M4, PC-7 M11: a governor named in a Skill input counts | N13 / B25 | F25 |
| F1-7 M5: the Stop hook's error handler re-raises | N14 / B26 | X05c |
| F1-7 M6: the block no longer names the remedy | N16 / B27 | F26 |
| F1-7 M7: skipped with more than one outward act | N17 / B28 | F12, F23 |
| F1-7 C1 to C4: plan-gate anywhere; adversarial-verify order; commit not outward; prefix not stripped | B29, B30, B30b, B24, B70 / N28 | `s_ctl_plan_gate_after_push`, `s_ctl_no_adversarial_verify`, F01, `s_ctl_synced_names` |
| PC-7 M1: the allowance is not review-only | N18 / B33 | P10a |
| PC-7 M3: loads before the prompt count | N19a, N19b / B34 | P11, F22 |
| PC-7 M5: only the first class's governor | N20 / B36 | P09 |
| PC-7 K1: the allowance although a tool ran | B69 | `p_ctl_review_with_tool_is_not_trivia` |
| PC-7, the classifier's and the registry's mutations | not in these files | their assignments |
| reimpl M1, M2: refusals, clicks not read | N21, N22 / B43, B44 | T20, M01 |
| reimpl M3, M4, M5, M6: merged counts; verb anywhere; apostrophes | N23, N24 / B10, B08, B09 | M26, T20c; `m_ri1_curly_apostrophe` |
| reimpl M9: a marker anywhere hides a message | N25 / B07 | F21 |
| reimpl M11: a number needs "#" | N26 | M08, T13 |
| reimpl M12: the assistant's text grants | B11 | `m_f2_1c_card_wait` |
| reimpl M14: commits or file pushes not outward | N28, N08 / B20, B24 | F01 |

New breaks for the new rules (each must be caught by the case named): the stretch starts at the governance
turn again (J02); `hookErrors` is ignored (J01); the open negation does not carry (J05); operations are
applied as sets, not in order (J06); the affirmative phrases are refusals (J07); a yes on a two-PR card grants
both (J08); an unresolved push is allowed unattended (J09); a PR word covers a push to main (J10); the `isMeta`
command row is never a turn start (J03); the deadline is removed (J04); the second answer text is not read
(J12); queued prompts are not classified (J13); the helper advisory is not silenced (J14); the ledger ignores
the time stamp (J16); the matcher loses its anchors or a name (W01); the repository is not bound (T35).

---

## 7. Risks

### 7.1 Where this could block honest work

| risk | evidence | what is done about it |
|---|---|---|
| D1 itself: a merge under "yes" or "merge it" is denied | R14: 2 of the 17 real merges (both in the turn of 2026-10-21T23:25) would be denied; the other 15 are allowed. These two are the only denials in the replay. Named by F2-2 and RI-4 and ordered by D1 | the denial tells the assistant how to word the card |
| an order worded in a way the grammar does not take as an order ("I think you should merge #34") | not measured on real text; the 17 real owner messages are short orders and clicks | the cost is one card. Every refusal reading fails closed |
| a refusal read where none was meant ("I have no idea, merge #34" revokes) | reading by construction: the clause has a refusal cue that is not in `AFFIRMATIVE_PHRASES` | one card; the phrase list is one constant |
| a push with no readable destination | R15: 3 real pushes in 2 calls. With `PUSH_UNKNOWN_BRANCH_POLICY = "deny"` both calls would be denied (design B's replay, and the reference prototype before the second graft, show them); with the default "deny-unattended" neither is (R14) | Q2 |
| a restart notice in the middle of the owner's turn ends the word | the rule is on in the reference prototype and R14 shows no denial but the two D1 ones, so no real merge rested on a word given before a restart. One of the two real restart rows sits in the middle of an owner turn (follow-up probe: 3 merges follow it); since those merges are allowed with the rule on, the word for them was given after it (an inference from R14, not a reading of the record) | `RESTART_ENDS_WORD`, listed in section 9 under the defaults taken without a question |
| the Stop gate blocks a second time | only when its first block was not answered (S8); never more than twice in a stretch; the harness itself stops after 8 | Q3 |
| a file without stop rows is judged as never judged | real files have a stop row at every stop (26 of 26); hand-built fixtures must carry the row | 2.3 |
| replay on the real record | R14: Stop 25 of 26 verdicts equal the baseline, the one change is a block that becomes an allow (F1-5); prompt hook 17 of 17 equal; pre-tool: the baseline's one false denial (RI-8) is gone, the two D1 denials are new | list above |

The replay could not test: a blocked stop followed by a merge, a message sent mid-turn, a scheduled delivery, a
helper's outward call. The real record holds none of them.

### 7.2 Run time

R16, three runs each, best time, on a synthetic record of 37.2 MB and 25,003 rows:

```
merged     Stop 0.34s | pre merge tool 0.35s | pre Bash commit+push 0.35s | pre Bash ls 0.02s | pre Edit 0.35s
reference  Stop 0.33s | pre merge tool 0.30s | pre Bash commit+push 0.30s | pre Bash ls 0.05s | pre Edit 0.30s
```

The pre-tool hook reads the record only when the call holds an act. The cost is one pass over the file. The
branch lookup reads two small files and starts no process. The deadline of 2.8 bounds the worst case below the
wired timeout of 10 s.

### 7.3 What changes for the copies

- `hooks/` is copied byte for byte into the plugin's scripts, the kit and the deck. Three files change, one test
  helper and one break list are added, the shipped `selftest-turn-gates.py` is replaced by the table of 6.1.
- The matcher of 3.3 changes in four wiring files; the plugin version is raised; the owner uploads it once.
- `govclass.py` changes in two lines for this specification (the lead test); its word lists are another
  assignment's.
- `hooks/README.md` changes wherever a rule changes: the merge word (D1 to D3, the grant tables of 1.2), the
  outward-action rule (what counts, the stretch, the second block), the prompt-class rule (P1, P2, P8), the
  advisory (A2, A4), the failure directions (2.8).
- New state: one ledger file per session and the advisory's marker files, in the state dir.
- The pack's `mk.answer` and `mk.notif` build unpaired rows; under 2.4 an unpaired card answer is no click, so
  the auditors' control lines that rely on one print deny. The follow-up reproductions were run as they are
  (R13); the others were not re-run by the judge.

### 7.4 Constants the registry must list

Every upper-case module-level name of the three files is a hand-set value; flags of a pattern are part of it.

- rows: `OWNER_ORIGIN_KINDS`, `WAKE_LEADS`, `ECHO_LEADS`, `COMMAND_LEADS`, `LOCAL_COMMANDS`, `INTERRUPT_LEAD`,
  `HOOK_FEEDBACK_LEAD`, `RESTART_LEAD`, `OUR_BLOCK_MARK`, `F1_BLOCK_MARK`, `HARNESS_MARKERS`
- cards and notifications: `CARD_TOOL`, `ANSWER_LEADS`, `NOTIF_READ_TOOLS`, `NOTIF_RESULT_LEAD`, `NOTIF_HEADER`,
  `SCHEDULED_ORIGIN_PREFIX`, `YES_LABEL`, `CARD_ORDER`, `CARD_ALL_WORD`, `CARD_PUSH_ORDER`, `RECOMMENDED`
- the owner's word: `DEFAULT_BRANCHES`, `MERGE_VERB`, `MERGE_ANY`, `MERGE_NOUN_BEFORE`, `MERGE_NOUN_AFTER`,
  `ORDER_LEADIN`, `TYPED_ORDER`, `PUSH_ORDER`, `PUSH_VERB`, `DEFAULT_BRANCH_WORD`, `REFUSAL_CUE`, `REFUSAL_START`,
  `OPEN_NEGATOR`, `AFFIRMATIVE_PHRASES`, `DEFER_CUE`, `SENTENCE_SPLIT`, `CLAUSE_SPLIT`, `POLITE_REQUEST`,
  `PURE_LIST`, `STANDALONE_REFUSAL_MAX_WORDS`, `OBJECT_FILLER_MAX`, `OBJECT_STOP_WORDS`, `OBJECT_TAIL_WORDS`,
  `PR_REF`, `PR_LIST_MORE`, `BARE_NUMBER`
- policy switches (section 9): `SCHEDULED_READ_ENDS_WORD`, `RESTART_ENDS_WORD`, `PUSH_UNKNOWN_BRANCH_POLICY`,
  `DELEGATE_MAY_MERGE`, `F1_MAX_BLOCKS`, `PROMPT_CLASS_MAX_BLOCKS`, `WAKE_TURN_INHERITS_LOADS`,
  `COMPACTION_VOIDS_LOADS`, `CLASSIFY_CARD_ANSWERS`, `F1_COUNTED_KINDS`, `MERGE_GATED_KINDS`
- calls: `MERGE_TOOL_LEAVES`, `FILE_PUSH_LEAVES`, `PR_WRITE_LEAVES`, `SCHEDULE_LEAVES`, `SCHEDULE_TOOLS`,
  `OTHER_OUTWARD_LEAVES`, `WRITE_TOOLS`, `SHELL_TOOLS`, `SCRATCH_DIRS`, `GIT_COMMIT_VERBS`, `GIT_WRITE_VERBS`,
  `GIT_GLOBAL_WITH_VALUE`, `GIT_PUSH_WITH_VALUE`, `GH_GLOBAL_WITH_VALUE`, `GH_MERGE_WITH_VALUE`,
  `GH_API_WITH_VALUE`, `GH_PR_WRITE_SUBS`, `GH_OUTWARD_GROUPS`, `GH_READ_SUBS`, `CURL_WITH_VALUE`,
  `CURL_DATA_FLAGS`, `GITHUB_API_HOSTS`, `GRAPHQL_MERGE`, `GRAPHQL_REF`, `SHELLS`, `SHELL_KEYWORDS`,
  `SHELL_NO_COMMAND`, `WRAPPERS_WITH_VALUE`, `SHELL_WRITE_COMMANDS`, `MAX_SHELL_DEPTH`, `SCRIPT_MAX_BYTES`,
  `FALLBACK_MERGE_TEXT`, `FALLBACK_OUTWARD_TEXT`, `DENIAL_TEXT`
- hooks: `CRUDE_MERGE`, `HOOK_DEADLINE_SECONDS`, `TRIVIA_MAX_CHARS`, `PLAN_MARK`, `GOVERNORS`, `LEDGER_DIRNAME`,
  and the matcher string of 3.3 (in the wiring files)

---

## 8. Where the two designs differed and what was chosen

### 8.1 The grades

Design A is its document (sections 0 to 4) with its prototype, cases and breaks. Design B is its prototype, test
table, break list and notes; its document is a stub. Sections 5 to 7 of this specification were written by the
judge for both.

| criterion | A | B | evidence |
|---|---|---|---|
| Obeys D1, D2 and D3 exactly as worded | FAIL | FAIL | A lets merges through that the owner did not order: "Don't, under any circumstances, merge #34." allows #34; "Merge #34 and close #35." allows #35; a peer session's "Merge #34." allows; a wrapped command-line merge with no word allows (R6: T05e, T16d, T28, R15a, R16, R14d). B refuses words D1 accepts: a click on "Yes, both (Recommended)" on a card that names both PRs; "No objections, merge #34."; its own T16e (R5: `m_f2_8g_card_yes_both`, `m_f2_8d_no_objections_merge`; R2). B's failures are all on the closed side |
| Resolves each finding in scope (the table) | FAIL | FAIL | neither wrote the table. By run: A leaves FU2-1, FU2-3 (second half) and FU2-5 unresolved (R11) and F2-2 open in two wordings (R6); B leaves FU2-3 (second half) unresolved (R11) and F2-8 d, f, g (R5) |
| Adds no block on honest work | FAIL | FAIL | A: on the real row order (H2) a merge the owner clicked is denied after any Stop-hook block (R6: M27), and a governed owner turn that reads a scheduled notification mid-turn is blocked (R6: F19b). B: its replay holds 2 denials of real pushes with no readable destination (`runs/replay-fixed.txt`; R15), beside the F2-8 refusals above. Both replays otherwise match the baseline except the two D1 denials and one block that becomes an allow |
| Fails safe on an unreadable record, no owner row, a restart at a compaction boundary | PASS | PASS | A: `m_f2_7c_empty`, `m_f2_7d_json_string_line`, `m_tb1_file_starts_at_compaction`, the fault cases (R1); B: T22, T23a to T23c, X01 to X05 (R2); the FU2-6 lines print the required verdict on both (R11). Caveats: A allows an unparseable command that holds merge words and a non-JSON input that names the merge tool (R6: R17, X01a); neither has a deadline (H4) |
| Can be tested: every rule has a named test with a fixture | PASS | PASS | A: 241 named cases with fixtures, 84 of 84 breaks caught (R1, R3); its fixtures for a blocked stop pin a row order the real record contradicts (R7). B: 254 named cases with fixtures, 55 of 55 breaks caught (R2, R4); one case fails on its own prototype and its control break shows 1 failing case; its rules are written nowhere but in the table |
| Is the simpler of the two where both are correct | PASS | FAIL | A: `turngate.py` 1,267 lines, one way to pair results, no legacy mode. B: 1,674 lines, a second pairing mode for hand-built files, three environment switches that change verdicts (`TURNGATE_NO_GIT`, `TURNGATE_ASSUME_BRANCH`, `TURNGATE_FAULT`). Where A is simpler and wrong (the shell parser, R6) B's size is the price of being right |

Base: design B. It is right in more places that the follow-up's facts decide (who the owner is, what a blocked
stop looks like, what the retry flag means, what a helper call carries, where the final answer is), and its
errors fail closed. Design A supplies the document form and seven grafts.

### 8.2 The differences

| # | difference | A | B | chosen | reason or run |
|---|---|---|---|---|---|
| 1 | who the owner is | rows whose text does not start with a harness prefix | `origin.kind` "human" where the file has `origin`; the prefix test otherwise | B | H6; R6: T28, T37 allow on A |
| 2 | what a blocked stop is | a stop row followed by the feedback row | a stop row with `hookErrors`; feedback rows counted wherever they sit | B | R7: the feedback row precedes the stop row |
| 3 | the retry flag | trusted unless the record shows a blocked stop (which A cannot see, #2) | blocks counted from feedback rows | B | R11: A prints allow on both FU2-1 lines, B block:F1 |
| 4 | a typed slash command | arguments are classified, never grant; the row starts no turn | the row is the owner's when `origin` says so; arguments grant | B, plus the rule for the `isMeta` form (2.2) | FU2-5; R11 |
| 5 | an image-only message | ignored | starts a turn | B | FU2-5; R11 |
| 6 | a yes on a merge card ("Yes, both") | grants the question's PRs | grants nothing (the label must start with the verb) | A | F2-8 names this click as wrongly refused; D1 (a); R5 |
| 7 | a card answered with free text | read as a typed message; needs the number; both result texts read | "merge it" takes the card's PRs; only the first result text read | both: B's fallback under the one-PR-or-all-word limit, A's second text | R8; R5 `m_d1_card_free_text_order`; R6 M14 |
| 8 | negation in a typed message | per clause: misses a negation split from its verb by commas | per sentence: a "no" anywhere refuses the whole sentence | new: clauses, with the open-negation rule and the affirmative phrases (2.5) | R6: T05e allows on A; R5: `m_f2_8d`, `m_f2_8f` deny on B; R12, R17: the combined rule passes all of them |
| 9 | which numbers an order names | every number in the clause | the list right after the verb | B | R6: T16d allows #35 on A |
| 10 | several effects in one message | sets (grant, revoke) | sets, the refusal applied first | new: an ordered list | "Merge #34. No wait." must end with no grant, "No. Merge #35." with one (R17) |
| 11 | the repository | number only | bound when the word names it | B | F2-2 lists another repository's PR; R6: T35 |
| 12 | pairing a card answer | by id only | by id; by position in a file without `uuid` | A | one rule; a real file always has ids. Cost: the pack's unpaired `mk.answer` rows are no clicks (7.3) |
| 13 | a notification result whose call row is gone | accepted by its lead | accepted by its lead only in a file without `uuid` | A | the real file is rewritten at a compaction (H8) |
| 14 | the restart notice | no boundary | ends the word | B | safest reading of D2; R14: no real merge is denied by it |
| 15 | a wake row | ends the word only in a file without stop rows | always ends the word | B | D2 second sentence |
| 16 | a card answered after a scheduled delivery read mid-turn | never grants | grants when the owner started the turn | B | the click is D1 (a); a run that the delivery started still grants nothing (G14). Q1 |
| 17 | the Stop gate and a delivery read mid-turn | the turn is split at the read (and not at all in a file without stop rows) | never split when the read is mid-turn; split at the wake row otherwise | new: the stretch rule (1.3 S5, 2.3) | R6: F19b blocks a governed turn on A, F19a allows on A; R11: the follow-up's fixture allows on both; R13: blocks on the reference prototype |
| 18 | a file without stop rows | old boundaries kept | old boundaries kept | new: nothing counts as judged | FU2-3; R12: F19c and A's S1 control now block, their twins with the stop row allow |
| 19 | the shell parser | one pass, never fails | lexer and parser, fails on unreadable text | B | R6: R14d, R15a, R16, R17 allow on A |
| 20 | the current branch of a bare push | read from `.git/HEAD`; a branch switched earlier in the command; the remote's default name | a `git` subprocess; two environment switches | A's lookup on B's parser | no process, no switch that weakens the gate. NOT RUN on the reference prototype (it runs in A's prototype, R1) |
| 21 | a push with no readable destination | an ordinary push | denied, with the instruction to name the branch | new: denied only where the owner is not present | R15 and R14: "deny" costs 2 real calls, the default none. Q2 |
| 22 | tools the Stop gate counts | also the workflow run and `ScheduleWakeup` | also `am`; counts command-line PR comments and reviews | A's two; B's `am`; comments and reviews are not counted in either spelling | SF-3 names the workflow run; the MCP comment tools are not counted, so the command-line ones are not. Q6 |
| 23 | a second block | both rules, up to 2 | the outward rule up to 2, the prompt-class rule 1 | B | the prompt-class rule rests on a word classifier with known false hits (PC-3). Q3 |
| 24 | a message sent mid-turn and the prompt-class rule | classified | not classified | A | FU2-4 names the Stop gate too; R12 |
| 25 | the length of the answer (trivia allowance) | recorded text | recorded text plus `last_assistant_message` | B | H7; R6: P14 |
| 26 | a helper's outward call | every outward call is noted; a helper's is the one whose id is not in the main record | only a call with `agent_id` is noted, with the row count | B, plus a time stamp | H1 |
| 27 | a helper's rows in the main file | ignored | never the owner, but their outward calls count | B | the merged hooks count them; R6: F10 |
| 28 | failure paths | a non-JSON input is "no call" | a crude screen on the raw text | B | COMMON-FIX 4 |
| 29 | fault tests | a key in the hook's input | an environment variable | neither: a temporary copy with one function replaced | nothing shipped may change a verdict |
| 30 | the denial text | a bracketed code per rule | prose only | A's codes on B's reasons | a test can tell the rows apart |
| 31 | a hook that runs out of time | - | - | new: a deadline inside the hook | H4 |
| 32 | the matcher | full names, not anchored | not designed | new: anchored pattern | H5 |

### 8.3 The cases that differ on the reference prototype (R12), each a decision above

| case | wanted there | reference | decision |
|---|---|---|---|
| B: M07-click-yes-both-strict-reading | deny | allow | #6 |
| B: R09h-bare-push-branch-unreadable | deny | allow | #21 |
| B: F19c-legacy-owner-push-then-scheduled-run-loads-both | allow | block:F1 | #18 |
| A: `m_slash_args_never_grant` | deny | allow | #4 |
| A: `s_pc4_d2_understood_loads_nothing` | block:prompt-class | allow | #23 |
| A: `s_s1_owner_miss_then_scheduled_run_governed` | allow | block:F1 | #18 |
| A: `p_slash_command_args_are_classified` | block:prompt-class | allow | the `isMeta` command row of 2.2 is specified but not in the reference prototype |
| A: `s_f1_1_delegate_commits` | block:F1 | allow | #26: A's case writes its note without `agent_id` |
| A: `a_adv1_advisory_states_its_limit` | the advisory names its limit | wording differs | the reference text says "may be a false alarm"; the case looks for A's words. The final text follows A2 and the case is rebuilt on it |
| A: `s_fault_stop_gate_allows` | allow | block:F1 | #29: the fault key is not read |

---

## 9. Open policy questions for the owner

Each default is what this specification builds. Each sits behind the named constants, so one answer changes one
line. The safe side was taken: closed for merges and other outward actions, and no new block on honest work.

| # | question | default (constants) | alternative | what each costs |
|---|---|---|---|---|
| Q1 | A scheduled notification and your merge word. Three cases: it is read while the assistant is still working on your order; the assistant shows a card afterwards in that same turn; a check-in you asked for ("check back in ten minutes") arrives later | The word given before the read is gone. A card you answer afterwards in your own turn counts. In work that a scheduled notification started, a check-in included, nothing merges unless you type the order while it runs; a card shown there grants nothing (`SCHEDULED_READ_ENDS_WORD = True`; M4, G14) | The word survives a notification read mid-turn; a card answered inside a check-in grants | Default: you repeat an order, or click once more, when a scheduled notification lands between order and merge; after a check-in you type "merge #34". Alternative: a stored prompt read mid-turn runs while a merge word is open (for the PRs you named only), and unattended work that shows a card against the doctrine can end in a merge |
| Q2 | A direct push to main has no PR number. What is "the same word as a merge", and what about a push whose branch the gate cannot read | An order that names the branch ("push this to main"), or a card that asks exactly that. A merge word for PR n does not cover pushing n's branch to main by hand. A push with no readable destination is denied only where you are not present (`PUSH_UNKNOWN_BRANCH_POLICY = "deny-unattended"`) | (a) never allowed: always a pull request; (b) the word for PR n also covers a hand push of its branch; (c) "deny" everywhere, or "allow" everywhere, for the unreadable case | Default: a session that lands work by fast-forward and push is denied once and told to use the PR or ask; an attended bare push from a directory the gate cannot read passes as an ordinary push. (a) costs any hotfix straight to main. (b) cannot be checked: the hook cannot map a branch to a PR. (c) "deny": 2 push calls of the real record would have been denied once each (R15) |
| Q3 | After a Stop block that was not answered, does the gate block again | The outward-action rule: yes, at most twice in one stretch. The prompt-class rule: once, as documented; a block by another rule or hook does not use it up (`F1_MAX_BLOCKS = 2`, `PROMPT_CLASS_MAX_BLOCKS = 1`) | 1 and 1; or 2 and 2 | Default: a session that ignores the outward block is stopped a second time, then let go; a prompt-class block answered with "Understood." passes. 1 and 1: after one block, a commit or push in the continuation with no governor passes (the hole of F1-2). 2 and 2: a chat message the classifier takes for governed work (PC-3) costs two forced continuations |
| Q4 | Which governor loads count for what a Stop judges | Work woken by a notification after a completed stop keeps the loads made since your message. Loads made before a compaction inside the same turn count. A scheduled run keeps nothing (`WAKE_TURN_INHERITS_LOADS = True`, `COMPACTION_VOIDS_LOADS = False`) | A wake is judged on its own loads; a compaction voids earlier loads (the doctrine's "reload the governors before the next consequential action") | Default: follow-up commits after a notification, and a push after a mid-turn compaction, ride on the earlier loads. Alternative: a new block at every wake that commits and at every compacted turn that did not reload. How often that happens on the real record: not run |
| Q5 | What is your prompt, for the rule that governed work needs its governor | What you type: a message, a slash command's arguments, a message sent while the assistant works. Not a card answer: a build you order by a click is not classified (`CLASSIFY_CARD_ANSWERS = False`); the outward-action rule still applies once the turn commits or pushes | Classify the chosen label too | Default: local work ordered by a click is not gated by this rule. Alternative: new blocks on click-ordered work with no governor; the label's "(Recommended)" must be removed first |
| Q6 | Which actions make a turn "outward" for the Stop gate | Counted: commit, push, PR create / update / merge / auto-merge / branch update, file pushes, a workflow run, every scheduling change, the session's own wake-ups included. Not counted: comments, reviews, issues, creating a branch or a repository, mail, drive, messages to other sessions (`F1_COUNTED_KINDS`, `OTHER_OUTWARD_LEAVES`) | Count the second group; or exempt the session's own wake-ups | Default: a turn that only comments or mails needs no governor; a turn that only sets its own check-in does. Alternatives: more blocks on light turns; or a check-in can be set with no governor loaded |

Defaults taken without a question, each one constant or one rule, listed so that none is silent:
`RESTART_ENDS_WORD = True` (a worker restart ends the merge word); `DELEGATE_MAY_MERGE = True` (a helper may
merge a PR you named while your word stands); an order for later or under a condition grants nothing
(`DEFER_CUE`); the repository is bound when your word names it; a slash command's arguments are your word when
the row is yours by `origin`; a free-text card answer takes the card's PR only when the card names exactly one
or the text says both / all; a row without `origin` grants nothing in a file whose owner rows carry one.

---

## 10. Order of implementation

Each step names its files, the tests written first, and the check that ends it. Nothing is run before step 0 is
committed. Commit, push and merge commands are kept in files, not typed into the shell, while the old hooks
are installed.

0. **Pre-register.** File: `experiments/hypothesis-2026-11-14-turn-gates-fix.md`. Content: the wanted verdict of
   every case of 6.1 and 6.2; the replay prediction (Stop: 25 of 26 equal to `PACK/pack/replay-baseline.txt`, the
   second stop of 2026-10-21T23:26 becomes an allow; pre-tool: exactly the two merges of the 2026-10-21T23:25
   turn denied; prompt: 17 of 17 equal); run time under 1 s on a 37 MB record; every break caught. Run the guard
   and keep its output. Check: the file is committed before any test run.
1. **The test table, red.** Files: `hooks/selftest_rows.py` (the builder of 6.1), `hooks/selftest-turn-gates.py`
   (the table of 6.1 and 6.2; it takes `--hooks DIR` and prints name, wanted, got). Run it on the merged hooks.
   Check: every case not listed as a pin or a control in 6.1 is red; no case errors; the output is saved as
   `results/2026-11-14/turn-gates-fix/red-on-merged.txt`.
2. **Rows and the model.** File: `hooks/turngate.py`: `load`, `normalize`, `harness_lead`, `command_args`,
   `row_events`, `scheduled_origins`, `Model` (window, governance turn, stretch, `loads`, `feedback`, `prose`,
   `owner_prompts`), `stop_span`, the `span` command line. Tests first: T17 to T37, S08 to S15, G03, J03, J18,
   and unit tests of `row_events` on one row of every kind of 2.2. Check: those cases pass with a stub that
   treats only the merge tool as merge-class and "merge #n" as the only order.
3. **The owner's word.** File: `hooks/turngate.py`: `typed_ops`, `card_answers`, `card_ops`,
   `Model.authorization`. Tests first: T01 to T16, M01 to M28, J05 to J08, J12, design A's word cases of 6.1,
   and the two spot-check lists of 2.4 and 2.5 as unit tests. Check: all pass; every sentence of the lists
   gives the operations stated.
4. **What a call does.** File: `hooks/turngate.py`: the lexer, `parse_shell`, the git, command-line and API
   readers, the branch lookup, `classify_call`, `looks_like_merge`. Tests first: R01 to R17, N01 to N11, the
   command halves of F02 to F08 and A02 to A06, `m_d3_local_merge_then_push_main`, and a unit test with a
   made-up checkout (a `.git/HEAD` file) for the branch lookup. Check: all pass; no test needs a `git` binary.
5. **The pre-tool hook.** File: `hooks/turn-gates-pretool.py`: `merge_decision` (in `turngate.py`), the denial
   reasons with their codes, the failure paths and the deadline of 2.8, the ledger note, the advisory. Tests
   first: X01 to X05 (fault copies), J04, J09, J10, J14, J15, G01, G02, A01 to A08. Check: every pre-tool case
   of the table passes; every path exits 0.
6. **The Stop hook.** File: `hooks/governance-enforce.py`: `f1_decision` (in `turngate.py`), the prompt-class
   rule. Tests first: F01 to F34, P01 to P17, J01, J02, J11, J13, J16, J17. Check: every Stop case passes; the
   follow-up reproductions print what section 5 says (`python3 PACK/work/followup-2/repro.py` on a copy pointed
   at the new hooks, as in R13).
7. **Interfaces.** Files: `hooks/govclass.py` (the lead test, two lines), the kept names of section 4. Check:
   `PACK/pack/tools/replay_real.py --hooks <new hooks> --what all` runs; the shipped
   `selftest-governance-classify.py` still passes its 45 cases; the receipt gate's and the trigger's
   assignments have the `span` output they need.
8. **Wiring.** Files: the four wiring files (owned by the surfaces assignment); test W01 here. Check: W01
   passes; the first PreToolUse group is unchanged.
9. **The break list.** File: `hooks/selftest-mutations.py`; one line in the guard that runs it. Check: the
   control shows 0 failing cases; every break is found in the code and caught by at least one case; the guard
   fails when one is not.
10. **Evidence and records.** Replay against the baseline with every differing line listed beside its finding
    id; the timing run; the constants of 7.4 in `redteam/constants_registry.json`; the sentences of
    `hooks/README.md` named in 7.3; a `.claude/LESSONS.md` entry `INC-2026-11-14-nn`; the guard after; the
    copies re-synced and the plugin version raised. Check: the predictions of step 0 are compared one by one
    and every miss is written down; the outside audit gets the table of section 5 with a command per row.

END OF SPECIFICATION
