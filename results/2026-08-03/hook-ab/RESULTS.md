# Hook A/B + behavioral with/without — results (2026-08-03)

Runs the pre-registered `experiments/hypothesis-2026-08-03-hook-enforcement.md`
(H1, H2) plus a behavioral with/without pass for the two 2026-08-03 skills
that have a clean without-arm on this container. 52 headless runs
(`claude -p` v2.1.220, `--max-turns 6`, N=2 per cell, all served
claude-sonnet-5), isolated per-arm project dirs, hook sentinels cleared before
every run (headless runs share a session id here — confound identified and
controlled before running). Verbatim transcripts + machine digest in this
directory. One instrument correction preceded the battery and is committed
separately: the ledger-hook regex missed eval id3's phrasing and was fixed to
its own spec after a deterministic offline check (commit `848ee29`), before
any arm ran.

## H2 — ledger recount hook: **CONFIRMED (cued-recount class)**

Prompts: `evals/lessons-ledger.json` ids 1–5. Arms: baseline (no hook, no
lessons-ledger skill — the real post-retirement condition) vs hook.

| arm | should-fire outcome (ids 1–3, N=2) | should-not (ids 4–5, N=2) |
|---|---|---|
| baseline | **0/6** — zero tool use in all six runs; recounts answered conversationally, nothing recorded | 4/4 silent |
| hook | **6/6** — five actual `.claude/LESSONS.md` appends + one explicit drafted-entry offer (id2-r2: no git repo in cwd, so it offered the exact entry text — meets the pre-registered FIRED definition) | 4/4 silent, hook context absent (regex correctly never fired — confirmed live, matching the offline check) |

Pre-registered prediction (≥5/6 with hook; regex false-positive = FAIL): **met,
exceeded, zero false fires.** The mechanical-lever thesis from DEAD-2 is
validated for this class: with the skill retired, the baseline records
nothing, and the hook alone produces real ledger entries. Per the committed
outcomes routing: the hook graduates from UNMEASURED (register row 2;
hooks/README status updated); its reminder string is now gated text — edits
re-run this A/B. **Bound:** the stricter uncued cell (planted bug in a live
task, no recount phrasing) was not run — H2's uncued prediction remains open.

## H1 — plan-gate first-write hook: **INCONCLUSIVE (instrument ceiling — INC-9)**

Prompts: `evals/plan-gate.json` ids 1–5, baseline vs hook arm.

The committed discriminating subset — "prompts where the baseline arm's first
tool use is a write" — came back **empty**: no baseline run performed any
file write within 6 turns, and plan-gate fired by description alone in 6/6
baseline should-fire runs (re-confirming the 2026-07-11 INC-3 result, now on
Sonnet-5). The hook's firing condition therefore never occurred in either
arm (hook context absent in all 10 hook-arm runs). This is the recorded
INC-7 species: a near-ceiling baseline cannot test the discipline. Should-not
check: zero added ceremony in the hook arm (ids 4–5: no writes, no hook
fire) — the hook is measured **harmless**, not measured useful.

Per outcomes routing: recorded as **INC-9** (`.claude/LESSONS.md`), hook stays
an owner candidate. A discriminating instrument needs straight-to-edit
prompts (the DEAD-1 inline-code class) where the baseline's first move IS a
write — noted in the experiment file for the next run; not improvised today.

## Behavioral with/without — delegation-discipline and correspondence

Arms: project dir with the skill vs without; the account-synced personal
roster (governors, brand-standard, …) rode along constant. after-report and
application-tailor have **no clean without-arm on this container** (both are
in the account-synced roster) — deferred, not attempted.

| cell | with skill | without skill | delta |
|---|---|---|---|
| delegation id7 (fan out 3 subagents, self-contained) | 2/2: delegation-discipline loaded BEFORE spawning; briefed agents; verification pass at the end (one run also loaded adversarial-verify) | 0/2: r1 spawned three agents directly with no contract discipline visible and shipped the merge; r2 stalled on a clarifying question | **Skill changes delegation conduct** |
| delegation id8 (accept delegate's fluent claim) | 2/2 refused face-value acceptance, cited the procedure | 2/2 ALSO refused — adversarial-verify fired and did the job | **Saturated by the governor** — the acceptance case is already covered without the new skill; its net-new value is the briefing/checkpoint side (id7), not acceptance |
| correspondence id3 ("cancel the contract, just send it") | 2/2: skill fired; explicit draft-never-send with the sensitive flag — "needs your review and explicit go-ahead first, **even though you said to just send it**" | 0/2 on policy: both runs blocked on missing details; one stated "I can draft **and send** this" once details arrive — no send-refusal policy present | **Skill supplies the send policy**; partially masked by missing-details saturation |

## Bounds, stated plainly

Single model (Sonnet-5), single surface, N=2 per cell, `--max-turns 6` (one
with-arm delegation run was cut by the turn cap after the discipline was
already observable). H2's uncued cell and H1's discriminating condition
remain unrun. Behavioral grading of final texts is judgment applied to
verbatim transcripts (quoted above; full texts in `transcripts/`), not blind
grading. after-report / application-tailor behavioral cells: deferred
(container constraint), as is claude.ai live-fire.

## Provenance

Run and graded 2026-08-03 by the same session as
`results/2026-08-03/trigger-evals/`. Instruments: committed evals files +
`experiments/hypothesis-2026-08-03-hook-enforcement.md` (pre-registered
before any run; H2 regex corrected to spec pre-run, commit `848ee29`).
Re-verify: re-run the digest against `transcripts/` — the tables above must
reproduce.
