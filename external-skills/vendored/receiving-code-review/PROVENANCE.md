# Provenance — receiving-code-review

- **Source:** https://github.com/obra/superpowers (`d884ae04edeb`, retrieved 2026-07-13)
- **Upstream license:** MIT (copy in this directory's `LICENSE`)
- **Tier at adoption:** NICE TO HAVE
- **Decision record:** `results/2026-07-13/external-skill-analysis/REPORT.md` + PR #2 (owner-approved 2026-07-13)
- **Modifications:** Vendored verbatim, no modifications.
- **Role:** Verify incoming review feedback against the codebase before implementing.

This is a vendored external skill. It is deliberately NOT under
`.claude/skills/` so it does not auto-load; install on demand via
`tools/install-external-skill.sh`. It follows its upstream's style, not this
library's house style — do not "fix" it to match skill-authoring; sync from
upstream instead (re-vendor at a newer commit and update this file).
