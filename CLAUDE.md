# claude-core-skills

David's governance library: the core skills under `.claude/skills/` auto-load
here; the adopted external layer under `external-skills/` does NOT auto-load
(by design — zero context cost until installed).

- **Operating procedure across surfaces:** `OPERATIONS.md`.
- **Need a domain capability mid-task** (documents, security, science, PM,
  career, transcripts…)? Consult `external-skills/README.md` (vendored,
  installable via `tools/install-external-skill.sh`) and
  `external-skills/PACKS.md` (plugin/checkout runbooks) before concluding a
  capability is missing or hand-rolling one.
- **Editing any core skill** gates through `architecture-contract` (invariants)
  and `research-methodology` (hypothesis → A/B → N=2 floor). Vendored external
  skills are never edited in place — re-vendor from upstream.
- Evidence conventions: results in `results/<date>/`, experiments in
  `experiments/`, volatile facts carry dates.
