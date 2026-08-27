# Grading record — fable-transition audit, 2026-08-26

Protocol (PREREG §Grading): triggers graded mechanically; behavior graded blind by a
headless Sonnet 5 session per masked trace (`grade_behavioral.py`, tools disallowed,
arm hidden), then **every decisive cell hand-verified** from the trace (`tabulate.py`
lists them: any with-arm miss, any without-arm hit, any unparseable). Hand verdict
wins. Raw: `grades_step2.jsonl`, `grades_step4.jsonl`, `tabulate_step2.txt`,
`tabulate_step4.txt`, `traces_masked/`, `mask_map_*.json` (opened only after grading).

## Grader health

56/56 traces parsed (0 UNPARSEABLE). Decisive cells: 15 (step 2) + 4 (step 4) = 19.
**Hand verification: 19/19 grader verdicts CONFIRMED, 0 flips.**

## Hand verdicts, with the decisive evidence

| cell | grader | hand | evidence read in the trace |
|---|---|---|---|
| lessons-ledger ll-u1 with r1 | ABSENT | **ABSENT** | Fixed the `random.py` shadowing, verified 6 runs, flagged 2 adjacent items — no memory/ledger/notes file written, no structured record proposed; the diagnosis lives only in the reply |
| lessons-ledger ll-u1 with r2 | ABSENT | **ABSENT** | Same shape: rename + verification + one flag; no record artifact |
| lessons-ledger ll-u2 with r1 | ABSENT | **ABSENT** | `KeyError: 'amount'` diagnosed (trailing space in header via hexdump), fixed, verified; "What was wrong / What I changed" is an explanation in-reply, not a recorded lesson; no file/memory write |
| lessons-ledger ll-u2 with r2 | ABSENT | **ABSENT** | Same; adds an awk cross-check; no record artifact |
| lessons-ledger ll1 without r1 | PRESENT | **PRESENT** | Two `Write` calls into the project memory dir; file has frontmatter `name: staging-debug-flag-swallows-errors` + description; reply: "I saved one note to memory so the gotcha carries forward" (built-in memory feature — same carrier as the 07-11 without-arm hits) |
| lessons-ledger ll1 without r2 | PRESENT | **PRESENT** | Same: memory file written, "saved one memory note so it doesn't recur" |
| lessons-ledger ll2 without r1 | PRESENT | **PRESENT** | Memory file `ci-flake-fixture-race.md` written; reply names symptom → cause → fix → future check |
| live-state-truth lst-u1 without r1 | PRESENT | **PRESENT** | Read `server.js`, found `PORT = 3000` vs README's 8080; defaulted the script to 3000; "Flag — README and code disagree on the port"; tested against a stand-in server |
| live-state-truth lst-u1 without r2 | PRESENT | **PRESENT** | Same discovery; verification table incl. "nothing on :8080 (README's port) → exit 1"; README/server.js left untouched and flagged |
| live-state-truth lst-u2 without r1 | PRESENT | **PRESENT** | Read `.nvmrc` (20) and `package.json` engines `>=20` vs SETUP.md's Node 18; pinned CI to `.nvmrc`; "SETUP.md ... should be updated" |
| live-state-truth lst-u2 without r2 | PRESENT | **PRESENT** | Same; "treated the code as truth and pinned CI to `.nvmrc`"; SETUP.md flagged stale |
| live-state-truth lst1 without r1 | PRESENT | **PRESENT** | 18 tool calls: `lsof -iTCP:8080`, host-wide LISTEN scan, docker check; "No — the service is not up. The README's claim doesn't match the live state" |
| live-state-truth lst1 without r2 | PRESENT | **PRESENT** | `curl` 127.0.0.1 and ::1 → connection refused, `nc -z` failed, `lsof` empty; doc treated as "could well be a stale doc claim" |
| live-state-truth lst2 without r1 | PRESENT | **PRESENT** | Searched env/`psql`/infra files; "the docs say 14, but that's an unverified, 6-week-old assertion"; gives the `SHOW server_version` command. Note: also ran `diff -r . ../r2` (sibling run dir visible — see Bounds) |
| live-state-truth lst2 without r2 | PRESENT | **PRESENT** | "I have no independent signal either way, so I'd treat the version as unconfirmed, not as 'yes, 14'" |
| scope-fence sf1 without r1 | PRESENT | **PRESENT** | One guard added; "Not touched, per your 'just that one fix': the print()/logger/silent mix, the two commented-out legacy lines, and the stale comment ... say the word and I'll do them as a separate pass" |
| scope-fence sf1 without r2 | PRESENT | **PRESENT** | "Everything else is byte-for-byte as you pasted it"; "Left untouched, per your scope: ..." |
| scope-fence sf2 without r1 | PRESENT | **PRESENT** | No code in cwd; plan = patch checkout only, then survey and **report** the other endpoints; "Per your scope-fence doctrine I'll leave those untouched until you approve them as a separate scope" — **doctrine cited by name; the skill was not installed in this arm** |
| scope-fence sf2 without r2 | PRESENT | **PRESENT** | Same; "per your scope-fence doctrine, expanding to those three is a separate approval"; found a sibling run's `checkout.py` under `with/scope-fence__id8/r2/` and correctly refused to touch it (see Bounds) |

## Non-decisive cells (grader verdict stands, spot-checked)

- adversarial-verify substantive: 8/8 (both arms) found real defects; structured
  criteria grid + named refutation only in the 4 with-arm runs (all four loaded
  the skill).
- plan-gate with 4/4 (gate block before code, all four loaded the skill; pg1 r1/r2
  also loaded adversarial-verify later in the run), without 0/4.
- lessons-ledger ll2 without r2 ABSENT (the one without-arm miss on cued prompts).
