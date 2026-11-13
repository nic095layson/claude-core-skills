# Brief: review the standing hook registry

key: `rev-registry` · finding ids: `RG-<n>` · scratch: `work/rev-registry/` (private checkout: `work/rev-registry/wt`)

**Objective.** Decide whether the registry does what is claimed for it: that every hand-set value in
`lib/hooks/` is registered, that the guard fails when one changes or a new one appears, and that each entry's
status is honest.

**The claims:** `lib/CLAUDE.md` ("Hand-set values in `hooks/` are registered ... the guard fails on an
unregistered or changed one"); `lib/hooks/README.md` lines 1-4; `lib/redteam/README.md`;
`lib/.claude/LESSONS.md` entry INC-2026-11-12-01; `pack/pr34-and-claims.md` (PR body row P5; chat claims 2
and 8). The standard the registry says it follows: `lib/.claude/skills/red-team/SKILL.md` (Terms; Procedure
steps 1, 6 and 7; Rules 4, 5 and 7).

**Targets:** `lib/redteam/constants_registry.json`, `lib/redteam/live.py`, `lib/redteam/attacks.json`,
`lib/redteam/records/constants.json`, `lib/redteam/README.md`; `lib/.claude/skills/red-team/scripts/registry_check.py`
and `attacks_check.py` as used here; the guard line that calls them
(`lib/.claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`); the recorded outputs
`lib/results/2026-11-12/qa-loop/p5-*.txt`.

**Method.** Change files only in your private checkout.
1. **Independent inventory.** Before you open the registry, list every hand-set value in `lib/hooks/*.py` and
   `*.sh` yourself: numbers, thresholds, windows, word lists, patterns, markers, tool-name lists, paths,
   timeouts, anything a person chose. Save the list. Then compare it with the registry: registered and live;
   live and unregistered; registered and gone. Say how you decided what "hand-set" means.
2. **Mutation.** For at least 10 values of different kinds (a number, a pattern, a list, a string, a value
   inside a shell script, a value in a wiring file), change the value in your checkout and run the registry
   check and the guard. Caught or not? Then: add a new constant; rename one; move one to another file; change
   one only in the plugin copy.
3. **How `live.py` finds a value.** Can it report a value the hook does not actually use (a shadowed name, a
   fallback copy, a later redefinition, a value inside a string)?
4. **Statuses.** Open every entry's status and basis. For "measured": is the cited record there, and does it
   measure that value? For entries that cite a decision id or a record path: does it resolve to something in
   the repository? For "uncalibrated": is the decision that will calibrate it named and findable?
5. **The red-team skill's own requirements** for a registry and an attack list (fingerprint, an append-only
   list, records that go stale when the engine changes): which are met here? Was anything from the earlier
   registry (`lib/results/2026-10-19/system-red-team/`) deleted or retired without a date?
6. **The recorded outputs.** Do `p5-old-registry-on-live.txt` and `p5-guard-catches-drift.txt` show what the
   pull request says they show? Re-run them (`lib-base/` is the library before the merge).

**Out of scope:** whether the gates' logic is right; the outcome scripts.

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
