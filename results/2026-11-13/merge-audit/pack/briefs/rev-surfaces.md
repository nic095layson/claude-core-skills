# Brief: review what actually runs where (wiring, copies, packages)

key: `rev-surfaces` · finding ids: `SF-<n>` · scratch: `work/rev-surfaces/` (private checkout: `work/rev-surfaces/wt`)

**Objective.** Establish, for each place these hooks and skills are supposed to run, which version runs
there today and whether the documents say the same. Report every place where a gate the owner believes is
active is absent, doubled, older, or different.

**The claims to test** come from: `lib/CLAUDE.md` ("Surfaces", and the doctrine's "Enforcement" paragraph);
`lib/hooks/README.md`; `lib/plugin/core-governance/README.md` (all of it, including "0.1.5"); `lib/instructions/`
(the install documents: how a .skill and a .plugin are installed and what their layout must be);
`pack/pr34-and-claims.md` (PR body rows P1 and P2 and its Follow-ups; chat claims 10 and 11).

**In scope.**
- **Wiring.** `lib/.claude/settings.json`, `kit-full/.claude/settings.json`, `deck-full/.claude/settings.json`,
  `lib/plugin/core-governance/hooks/hooks.json`. Which event and which tool names reach which script, with what
  timeout. Hook files that are wired nowhere. Tool calls the gates' code handles that the wiring never sends
  to them, and the reverse (`pack/session-tools.txt` lists the tool names that exist).
- **The wrapper** `lib/plugin/core-governance/scripts/run-unless-project-wired.sh` (and `selftest-wrapper.sh`):
  when does the plugin copy run, when does it stand down, and can both copies or neither copy run? Test it
  with the environment variables it reads, on scratch directories that imitate a project.
- **Copies.** Byte comparison of the hook scripts across `lib/hooks`, `lib/plugin/core-governance/scripts`,
  `kit-full/hooks`, `deck-full/hooks`, `account/plugin/core-governance` (installed on the owner's account
  today; its version is in its plugin.json) and the package sent to the owner today
  (`sent/core-governance.plugin`, a zip). Does the guard
  (`.claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`) catch a drifted copy? Change one byte
  in a copy inside your private checkout and run the guard there.
- **Skill packages** sent today (`sent/*.skill`, zips): contents against main; against the layout the install
  documents require; against what the account has now (`account/skills`).
- **The doctrine block:** identical in `lib/CLAUDE.md`, `kit-full/CLAUDE.md`, `deck-full/CLAUDE.md` and
  `lib/instructions/project-doctrine-block.md`?
- **Today's change to the deck:** `pack/deck-pr141.patch`. Did it carry over everything the library changed
  that the deck also holds?
- **The weekly run** described in `pack/trigger-prompt.md`: given what is installed today, which version of
  the gates will judge it?

**Out of scope:** whether the gate logic itself is right (other auditors).

**Evidence, stop, output:** as in COMMON.md sections 6 to 8.
