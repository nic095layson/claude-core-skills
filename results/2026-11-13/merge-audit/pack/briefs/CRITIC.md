# Completeness critic brief

key: `critic` · scratch: `work/critic/`

Fifteen auditors examined a merged change set and a second auditor re-ran each finding. You get the
summary of what they found and what they said they covered. Your question is the opposite of theirs: **what
did nobody look at?**

Read `pack/briefs/COMMON.md` (sections 1 to 4) and `pack/README.md` first. The summary is
`work/critic/SUMMARY.json` (findings with verdicts; each auditor's covered / not covered / not verified lists).
The assignments are the other files in `pack/briefs/`.

## What to do

1. **Coverage map.** For every file in `pack/diff.stat` and every hook in `lib/hooks/`, name the auditor(s)
   whose `covered` list shows a test run against it (not merely "read"). List what has none.
2. **Claims nobody tested.** Read `pack/pr34-and-claims.md` and the headline of
   `lib/results/2026-11-12/qa-loop/AUDIT.md`. Which statements to the owner have no PASS, FAIL or UNCHECKED
   from anyone?
3. **Angles nobody ran.** Each brief lists angles. Which angles have no test in the matching `covered` list?
   Which whole kinds of check were not run at all (for example: a real end-to-end run, a concurrency case, a
   different operating system or shell, an old transcript format)?
4. **Weak confirmations.** Which CONFIRMED findings rest on a fixture row the real harness may never write, or
   on a rule quote that does not say what the finding needs? Which REFUTED findings were refuted too cheaply?
5. **Duplicates.** Which findings from different auditors are the same defect?

## Output

Return the structured report and save it as `work/critic/critique.json`:
- `gaps[]`: `title`, `why_it_matters`, `what_would_test_it`, `files`.
- `duplicates[]`: `ids`, `note`.
- `doubtful[]`: `id`, `why`.
- `followups[]`: AT MOST TWO. The two uncovered areas where a further auditor is most likely to find something
  that matters to the owner. Each: `key` ("followup-1" or "followup-2"), `title`, and `brief`: a complete
  assignment in the form the other briefs use (objective, the rule as stated with file pointers, in scope,
  out of scope, method). The auditor will also read COMMON.md, so do not repeat it. If nothing deserves a
  further auditor, return an empty list and say why in `notes`.
- `notes`.

Budget: 40 tool calls. You run no attacks yourself; you read and map.
