---
name: domain-reference
description: >-
  Claude Skills domain knowledge for someone who has never authored one — what a
  skill/SKILL.md/.skill file is, how discovery and triggering actually work, where
  skills live on each surface (Claude Code project vs personal vs claude.ai vs
  cloud), what frontmatter does, why the description is the entire trigger, and
  this library's glossary and assumption register. Load when you (or the user) ask
  "what is a skill", "how does a skill get triggered", "why isn't the body enough",
  "where do skills go", "what's a .skill file", or when any glossary term below
  needs its definition of record. Do NOT load for authoring mechanics and house
  style (skill-authoring), fixing a skill that misbehaves (debugging-playbook), or
  install/packaging runbooks (install-and-surfaces) — this is the concepts layer
  only.
---

# Domain Reference

The domain knowledge a mid-level engineer or Sonnet-class model lacks on day one,
as it applies to operating this governance library — not a textbook.

## The mental model

A **skill** is a directory containing a `SKILL.md` file: YAML frontmatter (`name`,
`description`) plus a markdown body. The platform shows Claude every installed
skill's *name + description* at all times; the *body* is loaded only when the
description matches the situation. Three consequences that explain most skill
behavior:

1. **The description is the API; the body is the implementation.** Trigger quality
   lives entirely in the description. "Only use this when…" written in the body is
   dead text — the body is read only after the trigger already matched.
2. **Progressive disclosure bounds cost.** Descriptions are always in context
   (~100 words each — this is why over-installing skills has a price); bodies load
   on demand; bundled `scripts/` and `references/` files load or execute only when
   the body directs.
3. **Discovery is by path, and path failures are silent.** A syntactically perfect
   SKILL.md at the wrong path is readable as a file and invisible as a skill, with
   zero error output (the founding incident: `nic095layson/claude` commit
   `6dc366f` — three days shipped-but-dead at repo root).

## Where skills live (as of 2026-07-11)

| Surface | Location | Scope |
|---|---|---|
| Claude Code — project | `<repo>/.claude/skills/<name>/SKILL.md` | Sessions opened in that repo |
| Claude Code — personal | `~/.claude/skills/<name>/SKILL.md` | Every session on that machine |
| claude.ai web/mobile | Uploaded `.skill` zip (Settings → Capabilities → Skills) | That account's claude.ai sessions |
| Cloud / plugin surfaces | Managed by the platform or plugin | Per the surface's own config |

A **`.skill` file** is a zip whose root contains exactly `<name>/SKILL.md`
(verified against the real artifact in `nic095layson/claude`, 2026-07-10). Same
prose, different transport.

**Corollary that costs people days:** these locations are independent copies.
Editing one does not update the others, and a session loads exactly one — the
"stale copy" failure class in debugging-playbook §4. Capabilities are equally
per-surface: a claude.ai integration grant does not exist on a local machine
(debugging-playbook §5).

## Glossary (definitions of record for this library)

| Term | Definition |
|---|---|
| **Trigger** | The match between a situation and a description that loads a skill body. Not a keyword list — the model matches by situation, which is why descriptions state situations AND quote phrases AND carry a NOT clause. |
| **Governor** | One of this library's five core skills (plan-gate, adversarial-verify, live-state-truth, scope-fence, lessons-ledger) — behavior-governing, surface-portable, project-agnostic. |
| **Instance** | A project-specific implementation of a governor's law (e.g. `failure-archaeology` in nic095layson/claude is the instance of lessons-ledger there). Instances win over governors inside their project — see architecture-contract. |
| **Drift** | Two things that must agree no longer do. See live-state-truth (detection) and lessons-ledger (chronicle). |
| **Ceremony** | Governance ritual applied where it adds nothing (planning ritual on trivia). The library's named self-failure-mode; every governor carries a triage/proportionality rule against it. |
| **Volatile fact** | A true statement a future action can silently falsify. Carries a date or carries nothing. |
| **Assumption register** | Numbered, falsifiably-stated unknowns (A1, A2…) carried through work. Format in plan-gate. |

## This library's assumption register (as of 2026-07-11)

| # | Assumption | Basis | Status |
|---|---|---|---|
| A1 | The five-governor decomposition matches how David wants Claude governed holistically | His 2026-07-11 instruction naming exactly these five, plus "governing Claude wholistically" | unconfirmed in use — pending real-session evidence |
| A2 | Descriptions written here trigger reliably across surfaces | House trigger-design rules; NOT yet measured | unconfirmed — governance-adoption-campaign owns closing this |
| A3 | Personal-install of the five governors (not all 13 skills) is the right activation footprint | Progressive-disclosure cost argument in architecture-contract | unconfirmed — owner may prefer all or fewer |
| A4 | `nic095layson/claude` remains the live instance-repo whose project skills take precedence there | Its 15 skills verified present 2026-07-11 | verified 2026-07-11; volatile |

## When NOT to use this skill

- Writing or restructuring a skill → **skill-authoring**.
- A skill misbehaves → **debugging-playbook**.
- Installing, packaging, or verifying per surface → **install-and-surfaces**.
- Why this library is shaped the way it is → **architecture-contract**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`domain-reference` and `skill-authoring` (discovery paths, trigger mechanics,
`.skill` format — all verified there 2026-07-10 against live artifacts), plus the
platform docs at https://docs.claude.com/en/docs/agents-and-tools/agent-skills
(re-check for surface changes; details beyond the above are unverified here).

Re-verify: discovery paths — create a test skill under `~/.claude/skills/` and
confirm it appears in a fresh session's loaded list; `.skill` format —
`unzip -l` any known-good artifact. Update when: the platform adds frontmatter
fields or discovery paths, or any register row's status changes.
