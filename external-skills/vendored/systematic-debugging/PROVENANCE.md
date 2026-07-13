# Provenance — systematic-debugging

- **Source:** https://github.com/obra/superpowers (`d884ae04edeb`, retrieved 2026-07-13)
- **Upstream license:** MIT (copy in this directory's `LICENSE`)
- **Tier at adoption:** NICE TO HAVE
- **Decision record:** `results/2026-07-13/external-skill-analysis/REPORT.md` + PR #2 (owner-approved 2026-07-13)
- **Modifications:** Dropped upstream dev artifacts: CREATION-LOG.md, test-academic.md, test-pressure-1.md, test-pressure-2.md, test-pressure-3.md
- **Role:** Four-phase root-cause methodology; net-new sliver: 3-strike fix counter with architecture escalation.

This is a vendored external skill. It is deliberately NOT under
`.claude/skills/` so it does not auto-load; install on demand via
`tools/install-external-skill.sh`. It follows its upstream's style, not this
library's house style — do not "fix" it to match skill-authoring; sync from
upstream instead (re-vendor at a newer commit and update this file).
