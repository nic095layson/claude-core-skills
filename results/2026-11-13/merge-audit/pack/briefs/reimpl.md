# Brief: re-implement the turn gates from the stated rules, then compare

key: `reimpl` · finding ids: `RI-<n>` · scratch: `work/reimpl/`

**Objective.** Write your own implementation of F1 (the Stop gate's outward-action rule) and F2 (the
merge-word gate, including the scheduled-run rule) from the STATED rules alone, run both implementations on
the same inputs, and report every input on which they differ.

**Why.** The people who wrote the code also wrote its tests, so the two agree whatever the rule says. An
implementation built only from the stated rule shows where the code does something the rule does not say,
and where the rule says nothing at all.

**The rule that makes this worth doing.** Until your first comparison run is saved, do NOT open these files,
in any copy (`lib/`, `lib-base/`, the plugin, `account/`, `kit/`, `kit-full/`, `deck/`, `deck-full/`, `sent/`):
`turngate.py`, `governance-enforce.py`, `turn-gates-pretool.py`, `selftest-turn-gates.py`. Do not open
`pack/diff.patch` or `pack/deck-pr141.patch`. You may copy these files without reading them. If you open one
by mistake, say so in `notes`.

**Your specification:** `pack/spec/turn-gates-spec.md` (verbatim extracts of every place the repository states
these rules, prose only), plus the other files it lists as allowed reading.

**Steps.**
1. Write `work/reimpl/READING.md`: every decision you had to make where the specification was silent or
   contradicted itself, and what you chose. Do this before coding.
2. From the specification write, in `work/reimpl/mine/`, two drop-in hooks with the same file names and the
   same stdin/stdout protocol as the originals (`pack/README.md`, "Hook events and payloads"):
   `governance-enforce.py` implementing ONLY the F1 rule (leave out the prompt-class rule), and
   `turn-gates-pretool.py` implementing ONLY F2 (deny or allow; leave out the F3 advisory).
3. Build a corpus of at least 300 synthetic transcripts with `pack/tools/mk.py`: systematic combinations
   (every row kind in `pack/real-row-shapes.md` × the relevant tool calls × governor loads before and after ×
   owner wordings × card answers × notifications), not random noise. Save the generator as
   `work/reimpl/corpus.py`.
4. Run both implementations on every transcript: the originals through `mk.run_stop` / `mk.run_pre` with the
   default hooks, yours with `hooks=<PACK>/work/reimpl/mine`. For the Stop gate compare only "block:F1" against
   anything else; for the pre-tool gate compare deny (and which deny) against anything else. Save the whole
   comparison as `work/reimpl/diff-run-1.txt`, one line per case: case id, original verdict, your verdict.
5. Run the real record too: copy `lib/hooks/turngate.py` and `lib/hooks/govclass.py` UNREAD into
   `work/reimpl/mine/` (the replay tool imports them for its own bookkeeping; your two hooks must not import
   them), then `python3 PACK/pack/tools/replay_real.py --hooks PACK/work/reimpl/mine --what stop` and
   `--what pre`, and compare with `pack/replay-baseline.txt` (ignore prompt-class blocks and advisories, which
   you did not implement). Append the result to `diff-run-1.txt`.
6. Only now read the original code. For every disagreement decide which it is: the code departs from the
   stated rule (a finding: `false_allow`, `false_block` or `wrong_result`); the rule is silent or contradictory
   and you and the code chose differently (`ambiguity`); or you misread the rule (not a finding: one line in
   `notes`). Exact agreement is the only pass; a near-miss is a finding.

In `notes`, give the agreement rate (cases agreed / cases run) for the synthetic corpus and for the real
replay separately.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8. Your budget is 100 tool calls.
