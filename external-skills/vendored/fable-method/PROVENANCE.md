# Provenance — fable-method

- **Source:** https://github.com/Sahir619/fable-method (`b2a24d5b378a`, retrieved 2026-07-13)
- **Upstream license:** MIT (copy in this directory's `LICENSE`)
- **Tier at adoption:** NICE TO HAVE
- **Decision record:** `results/2026-07-13/external-skill-analysis/REPORT.md` + PR #2 (owner-approved 2026-07-13)
- **Modifications:** Vendored verbatim, no modifications.
- **Role:** Independent distillation of Fable session discipline; ~80% overlaps the governors - use where governors are not installed.

This is a vendored external skill. It is deliberately NOT under
`.claude/skills/` so it does not auto-load; install on demand via
`tools/install-external-skill.sh`. It follows its upstream's style, not this
library's house style — do not "fix" it to match skill-authoring; sync from
upstream instead (re-vendor at a newer commit and update this file).
