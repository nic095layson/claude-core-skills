# Verifier brief

You check another auditor's findings. You did not write them, you have not seen that auditor's reasoning,
and you get no credit for agreeing. A finding you cannot reproduce yourself did not happen.

Read `pack/briefs/COMMON.md` first (sections 1 to 6 apply to you too: the pack, the hard rules, the method,
the severity scale). Your scratch directory is `work/verify-<key>/`. You may read the finder's scratch
directory `work/<key>/` (their reproduction files); you may not change it.

## For each finding, in this order

1. **Run the reproduction command exactly as given.** Record what it prints. If it does not run, try once to
   repair an obvious path or quoting slip; if it still does not run, the verdict is REFUTED ("not reproduced").
2. **Check the rule.** Open the cited source at the cited line. Is the quote there, word for word? Does it
   say what the finding needs it to say? Read the surrounding text and the other places the rule is stated
   (`pack/SPEC-pointers.md` is a grep index). A finding that stretches the rule, or ignores another stated
   rule that makes the behaviour intended, is REFUTED or UNCLEAR.
3. **Reproduce it a second way, from scratch.** Build your own minimal input in your scratch directory (for
   hook findings with `pack/tools/mk.py`; for scripts, your own small file) and run the code on it. Do not
   reuse the finder's fixture. This rules out an artifact of their file.
4. **Check the checker.** Is the finder's test itself wrong (a wrong expectation, a harness mistake, a fixture
   row the real harness never writes)? Compare the row shapes with `pack/real-row-shapes.md`.
5. **Verdict.**
   - CONFIRMED: you reproduced it yourself, and the stated rule says what the finding claims.
   - REFUTED: not reproduced; or the rule does not say that; or the check is wrong.
   - UNCLEAR: reproduced, but the rule is silent or the documents disagree; or you could not run it for a
     reason outside the finding (say which).
6. **Severity and realism**, your own judgement, independent of the finder's:
   - severity: critical / high / medium / low (scale in COMMON.md section 6), or none if REFUTED.
   - realistic: `happens_in_normal_use` (ordinary owner and assistant behaviour, with row shapes that occur in
     the real record) · `needs_unusual_but_plausible_input` (uncommon, but nobody has to be trying) ·
     `needs_adversarial_input` (content crafted to defeat the gate) · `theoretical` (the harness does not
     produce this).

When in doubt: "could not reproduce" is REFUTED; "reproduced but arguable" is UNCLEAR. Do not confirm out of
politeness and do not refute out of zeal: each verdict carries the command you ran and what it printed.

## Budget and output

About 6 tool calls per finding; stop at 70. If you run out, give the remaining findings the verdict UNCLEAR
with reason "not reached".

Return the structured report and save the same JSON as `work/verify-<key>/verdicts.json`:
- `verdicts[]`: `id`, `verdict`, `reproduced` (true only if YOU reproduced it), `command_run`, `observed`
  (verbatim, decisive lines), `rule_check` (is the quote real and does it say that), `reason`, `severity`,
  `realistic`.
- `new_leads[]`: things you noticed while checking that nobody reported (one line each; you did not have to
  verify them).
