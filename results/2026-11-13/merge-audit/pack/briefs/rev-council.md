# Brief: review the council skill as brought into the library

key: `rev-council` · finding ids: `CN-<n>` · scratch: `work/rev-council/` (private checkout: `work/rev-council/wt`)

**Objective.** Check every statement made about the council skill's arrival (copied word for word, one rule
added, trigger eval 6/6 and 4/4, lint pass, package matches main), and decide whether the skill as merged is
consistent with itself, with the house rules for skills, and with the copy on the owner's account.

**The claims:** `pack/pr34-and-claims.md` (PR body rows P6 and P2; chat claims 6 and 11);
`lib/results/2026-11-12/qa-loop/council-trigger/GRADE.md`; `lib/experiments/hypothesis-2026-11-12-qa-loop.md`
(row P6 and its outcome); `lib/results/2026-11-12/qa-loop/AUDIT.md` (integrity row "Council", self-critical
point 5, proposal P6).

**Targets:** `lib/.claude/skills/council/SKILL.md`; `lib/evals/council.json`; `account/skills/council` (the
owner's account copy, where the skill came from); `sent/council.skill` (the zip sent today); the lines of
`lib/README.md` that mention council.

**House rules to check against:** `lib/.claude/skills/skill-authoring/SKILL.md` (the description contract, the
size limit, the required sections, checklist steps 5 to 8); `lib/.claude/skills/research-methodology/SKILL.md`
(what a trigger eval must record; the evidence floor; pre-registration); `lib/CLAUDE.md` (conventions:
evidence, volatile facts carry dates; doctrine rule 6 on model identifiers);
`lib/.claude/skills/architecture-contract/SKILL.md` (the invariants; Decision 5 on what is installed where);
`lib/.claude/skills/independent-audit/SKILL.md` (the outside-read idea the new section borrows).

**Method.**
1. **"Word for word".** Compare the library body with the account copy byte for byte and list every
   difference. Is the description identical?
2. **The added "outside read" section.** Can it be carried out as written (who does what, when, with which
   tool, on which surface)? Does it contradict the skill's own procedure or output format, or another skill?
3. **The trigger eval.** What exactly was run, against which copy of the skill, in how many sessions, and
   what was recorded? Are the raw outputs in the repository? Do the cases in `evals/council.json` test what
   the description promises (read the description's trigger rule literally, then read each case)? You cannot
   re-run live sessions: grade the record.
4. **Lint.** Run `bash PACK/work/rev-council/wt/.claude/skills/diagnostics-and-tooling/scripts/lint_skill.sh`
   on the skill in your private checkout; then check by eye what the lint does not check.
5. **The package.** Unzip `sent/council.skill` into your scratch directory; compare with main and with the
   layout the install documents in `lib/instructions/` require.
6. **Copies.** List every copy of a skill named council that a session can see (`pack/session-tools.txt` has
   the session's skill list) and how they differ.

**Out of scope:** whether a council verdict is any good (not measured by anyone; say so if a document claims
otherwise).

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
