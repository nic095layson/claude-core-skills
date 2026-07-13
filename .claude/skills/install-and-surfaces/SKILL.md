---
name: install-and-surfaces
description: >-
  How to get this library running on each surface and PROVE it is running — install
  paths for Claude Code project and personal scopes, packaging a governor as a
  .skill for claude.ai, the register-then-verify procedure, and what does and does
  not carry between environments (credentials, connectors, installs). Load when you
  need to "install the skills", "set this up on another machine", "package for
  claude.ai", "why do I have the skill here but not there", "update the installed
  copies", or check that an install actually took. Do NOT load for concepts of
  where skills live (domain-reference has the map; this is the runbook), authoring
  (skill-authoring), or debugging a completed install that misbehaves
  (debugging-playbook §1/§2/§4).
---

# Install and Surfaces

The runbook for deploying this library. Its one law, inherited from the founding
incident: **an install is not done when the files are in place; it is done when
the surface demonstrably loads them.** Placement failures are silent — the only
proof is registration observed in a fresh session.

## The install matrix (as of 2026-07-11)

| Surface | Install action | Scope | Verify |
|---|---|---|---|
| Claude Code, this repo | Nothing — project skills auto-discover from `.claude/skills/` | Sessions in this repo | Fresh session lists every skill in `.claude/skills/` (20 as of 2026-07-13) |
| Claude Code, any machine | Copy governor dirs to `~/.claude/skills/<name>/` | All sessions on that machine | Fresh session lists the governors |
| claude.ai web/mobile | Upload a `.skill` zip per skill (Settings → Capabilities → Skills), toggle on | That account | Fire a should-trigger prompt; check it loads |
| Other/managed surfaces | Per that surface's plugin/skill config | Varies | Same principle: observe registration |

Default footprint per architecture-contract Decision 5: the **five governors**
personally installed; the eight support skills stay project-scoped (they
auto-load when working in this repo). Owner-adjustable (assumption A3).
Capability skills (2026-07-13) are project-scoped by default and upload to
claude.ai selectively — Decision 8 and `results/2026-07-13/` record which.

## Runbook 1 — personal install (Claude Code machine)

```bash
# from this repo's root
for s in plan-gate adversarial-verify live-state-truth scope-fence lessons-ledger; do
  mkdir -p ~/.claude/skills/$s && cp .claude/skills/$s/SKILL.md ~/.claude/skills/$s/
done
ls ~/.claude/skills/   # expect the five governor directories
```

(This loop is also quoted in the README's Install section — update both on
change; the README copy is the one newcomers run.)

Then **verify registration**: open a fresh session anywhere outside this repo and
confirm the five appear in the available-skills list. Files present + skills
absent = debugging-playbook §1.

## Runbook 2 — package a skill for claude.ai

The `.skill` format (verified against the source repo's real artifact,
2026-07-10): a zip whose root contains exactly `<name>/SKILL.md`.

```bash
cd "$(mktemp -d)"                       # never build inside the repo
mkdir <name> && cp <repo>/.claude/skills/<name>/SKILL.md <name>/
zip -q <name>.skill <name>/SKILL.md
unzip -l <name>.skill                   # expect exactly: <name>/SKILL.md
```

Upload via Settings → Capabilities → Skills, toggle on, then live-fire one
should-trigger prompt. (Candidate 2026-07-13: current platform docs say
Settings → Features — verify the live UI path on next upload and update here.)

**Multi-file skills (added 2026-07-13).** The platform `.skill` format accepts
bundled scripts and reference files, not only SKILL.md — doc-verified 2026-07-13
against platform.claude.com/docs agent-skills overview; no live multi-file
upload has been run yet. Package the whole directory when the skill ships
companions (pdf: `scripts/`, `forms.md`):

```bash
cd "$(mktemp -d)" && cp -r <repo>/.claude/skills/<name> . && zip -qr <name>.skill <name>/
unzip -l <name>.skill    # expect SKILL.md plus every companion under <name>/
```

The one-file zip above remains the minimal form for body-only skills.
**Name collisions:** claude.ai ships built-in pdf/docx/pptx/xlsx skills
(doc-verified 2026-07-13); custom-vs-built-in same-name precedence is
undocumented — rename the packaged directory AND its frontmatter `name`
(e.g. `pdf-extract`) when uploading a same-named skill. A rename is a
deliberate per-surface fork: record it in a dated `results/` entry.

## Runbook 3 — update installed copies after an accepted edit

Installed copies do not follow the repo — every install is a fork until re-copied
(the stale-copy class, debugging-playbook §4). After any accepted change:

```bash
# re-run Runbook 1; then prove freshness:
for s in plan-gate adversarial-verify live-state-truth scope-fence lessons-ledger; do
  diff -q .claude/skills/$s/SKILL.md ~/.claude/skills/$s/SKILL.md || echo "STALE: $s"
done
```

Silence = in sync. claude.ai: rebuild and re-upload the affected `.skill` —
testing new wording against an old upload voids the run
(research-methodology's protocol table).

## The environment-boundary rules (what does NOT carry)

Verified the hard way, 2026-07-11 (this repo's ledger, `.claude/LESSONS.md`
INC-1; triage form in debugging-playbook §5):

1. **Credentials and grants are per-environment.** A claude.ai integration grant
   lives on Anthropic's servers; a local machine needs its own (`gh auth login`,
   local keys). Never assume access travels; enumerate it live
   (live-state-truth's boundary rule).
2. **Installs are per-surface copies.** No mechanism syncs them; Runbook 3 is
   manual by design — treat it as part of any change's definition of done.
3. **Skill *content* must therefore be surface-portable:** governors contain no
   machine paths, no credentials, no surface-specific commands in their
   procedures (architecture-contract, Decision 2 corollary) — this is what makes
   the copies safe to fork.

## When NOT to use this skill

- The conceptual map of surfaces → **domain-reference**.
- An install that verifiably completed now misbehaves → **debugging-playbook**.
- Deciding WHAT to install where → **architecture-contract** (Decision 5).
- Lint before installing → **diagnostics-and-tooling**.

## Provenance and maintenance

Generalized 2026-07-11 from `nic095layson/claude` (commit `df6e198`)
`build-and-env` and `release-and-packaging`: the register-then-verify law
(their INC-1), the `.skill` zip format (verified artifact), the
never-build-inside-the-repo rule, and the copies-must-match parity discipline
carry over; that repo's `files.zip` mechanics stay behind (this library ships no
zip artifact yet). The environment-boundary rules are this library's own,
evidenced by its founding session (2026-07-11 GitHub-auth incident).

Re-verify: install matrix paths — create a canary skill in `~/.claude/skills/`
and confirm a fresh session lists it; `.skill` format — `unzip -l` any built
artifact. Update when: a surface changes its discovery mechanism, the library
ships bundled artifacts (add a parity script per diagnostics-and-tooling), or
the personal-install footprint changes (Decision 5 / A3).
