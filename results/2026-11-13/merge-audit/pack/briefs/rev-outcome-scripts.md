# Brief: review the outcome-metric scripts

key: `rev-outcome-scripts` · finding ids: `OS-<n>` · scratch: `work/rev-outcome-scripts/` (private checkout: `work/rev-outcome-scripts/wt`)

**Objective.** Decide whether `corrections_rate.py` and `stale_rules.py` report true numbers on real inputs,
and whether their tests would notice if they did not.

**Targets** (under `lib/.claude/skills/independent-audit/`): `scripts/corrections_rate.py`,
`scripts/stale_rules.py`, `scripts/test_qa_loop.py`, `corrections-log.template.md`; the convention lines the
merge added to `lib/CLAUDE.md` ("Corrections") and `lib/README.md`; the recorded outputs in
`lib/results/2026-11-12/qa-loop/` (`p3-p4-p7-tests-*.txt`, `weekly-review-first-output.txt`).

**What they are meant to do:** `lib/experiments/hypothesis-2026-11-12-qa-loop.md` (rows P3 and P7);
`lib/results/2026-11-12/qa-loop/AUDIT.md` (proposals P3 and P7); the scripts' own docstrings;
`pack/pr34-and-claims.md` (PR body rows P3 and P7; chat claims 3 and 5).

**Method.**
1. **Real input first.** `kit-full/report/corrections-log.md` is a real corrections log. Read its rows and
   count by hand what the right answer is: rows, weeks, who caught each one. Then run the script on it. Any
   difference is a finding.
2. **stale_rules.py on the merged library.** Take its output. Open at least 10 of the items it lists and 10
   places it does not list, and decide for each whether "a rule still marked unmeasured after 60 days" is
   true of it. What is the unit the script counts, and is that the unit the documents name?
3. **Edge inputs for both scripts:** table shapes people really write in Markdown (pipes or links inside
   cells, alignment rows, blank cells, wrapped lines), dates (formats, week 1 and week 53, a year boundary,
   future dates, no date), an empty log, a missing file, two logs at once, non-ASCII text, a log that does not
   follow the template. For each: right answer, wrong answer, or crash; and the exit code.
4. **"Who caught it":** how is it decided, and on which real or plausible rows is it wrong?
5. **"Today":** where does each script get the current date, can it be set, and do the tests depend on the
   day they run?
6. **Tests.** For each test in `test_qa_loop.py` that covers these two scripts: does it fail when the
   behaviour it names is broken? (Mutation check, COMMON.md section 5.) Which behaviours have no test?

Run test suites only in your private checkout.

**Out of scope:** `weekly_review.sh` as an unattended run (another auditor); the registry.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
