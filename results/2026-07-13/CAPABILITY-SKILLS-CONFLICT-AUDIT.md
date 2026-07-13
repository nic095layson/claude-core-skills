# Capability-skills conflict audit + claude.ai surface decisions — 2026-07-13

Scope: do the six capability skills added 2026-07-13 (frontend-design, pdf,
docx, pptx, xlsx, mcp-builder) conflict with the library as implemented through
2026-07-12 (13 governance/support skills + brand-standard + the claude.ai
custom instructions + the scope-fence hook)? And what must change for them to
operate on claude.ai?

Method: six independent adversarial reviewer agents (one per new skill, each
prompted to REFUTE clean coexistence across trigger overlap, boundary-map
symmetry, doctrinal contradiction, eval cross-fire, instructions text, hook
interaction) plus one claude.ai surface analyst grounded in current platform
docs. Full structured findings: session workflow `wf_65fc6a6f-fec` (7 agents,
0 errors). This file is the distilled record.

## Verdict

**Zero blocking conflicts.** No case found where a session following two
skills at once does the wrong thing. Every double-fire composes (plan-gate +
capability on builds; adversarial-verify + capability on delivery; capability
skills defer to brand-standard on identity, consistent with its hard rules).

Four **important** findings — all one-directional routing gaps, none
contradictions — plus assorted minors. Resolutions applied same-day (this
commit) unless marked deferred:

| Finding | Resolution |
|---|---|
| brand-standard (7/12) had no back-pointers to the format skills — "format my pitch deck to match my brand" could load it alone and hand-style textboxes | FIXED: When-NOT bullet + Part 4 step 2 handoff added to brand-standard (body-only edit; description enumeration change deferred to a gated pass) |
| skill-authoring never mentioned mcp-builder — "write a skill so Claude can query our DB" would produce the wrong artifact class | FIXED: When-NOT bullet added (description NOT-phrase deferred to a gated pass) |
| frontend-design's charts carve-out pointed at nothing (no dataviz skill exists) | FIXED: carve-out reworded — embedded charts take fd tokens/contrast; mark/axis design labeled unowned (candidate for a future dataviz skill); eval id 6 flipped accordingly, id 7 added |
| Capability skills had no slot in Decision 5's footprint taxonomy; eval surface declarations disagreed (docx/xlsx said personal-scope, siblings project-scope) | FIXED: architecture-contract Decision 8 added (project-scoped by default); docx/xlsx eval surfaces aligned pre-first-run, amendment dated in each _grading |

Minors fixed same-day: stale "all 13" counts (skill-authoring,
diagnostics-and-tooling, install-and-surfaces); brand-standard's ≈2.1:1 → the
computed 2.16:1; xlsx snippet's near-brand fill color labeled a generic
example; docx gained the style-object brand-customization snippet (tested,
round-trips) and a new-PDF trigger phrase; xlsx WHEN extended to reading
existing workbooks; pdf gained the restyle-a-PDF three-hop edge case;
mcp-builder's secrets rule no longer suggests keys in a checked-in .mcp.json;
fd↔pdf circular routing on new-PDF creation broken (fd now states the
docx-then-convert route); gate_note added to all six evals documenting the
small-N gate convention.

## claude.ai decisions (Decision 8)

Platform facts (doc-verified 2026-07-13 against
platform.claude.com/docs agent-skills overview; live-upload untested):
claude.ai ships built-in pdf/docx/pptx/xlsx skills behind file creation;
custom skills coexist with built-ins; `.skill` zips may bundle scripts and
references; same-name custom-vs-built-in precedence is UNDOCUMENTED; skill
runtime network access varies by user/admin settings; no cross-surface sync.

| Skill | Upload? | Reason |
|---|---|---|
| frontend-design | YES | No built-in equivalent; core claude.ai artifact surface; SKILL.md-only package |
| pdf | CONDITIONAL | Built-in pdf is generation-oriented; ours adds form-fill/extract/redact. Needs: multi-file package (Runbook 2 extension, added today), rename to avoid built-in name collision (`pdf-extract`), owner's network-setting check for pip |
| docx / pptx / xlsx | NO | Built-ins own the surface; same-name collision undocumented; duplication pays permanent context for shipped capability |
| mcp-builder | NO | Procedure inert there (no CLI, no localhost inspector); claude.ai takes remote connectors only |

Custom instructions: **no fifth pointer.** Capability skills self-trigger by
description (the same mechanism as the built-ins); pointers are reserved for
against-the-grain governance. Amend only if post-upload live-fire shows misses.

## Owner TODO (cannot be done from a container)

1. **Re-paste pending (pre-existing drift):** the claude.ai settings box still
   holds the three-pointer instructions; paste the four-pointer block from
   `instructions/claude-ai-custom-instructions.md`.
2. **brand-standard upload state is unrecorded:** the 7/12 acceptance covers
   only the three governors, yet pointer 4 assumes brand-standard is installed.
   Verify live; record the answer in a dated results/ entry.
3. Upload `frontend-design.skill` (packaged this session), toggle on, live-fire
   one should-trigger prompt, record acceptance.
4. For `pdf-extract.skill`: first check Settings → file creation network
   access allows package installs; upload; live-fire the extractor path.
   The package renames the skill (deliberate per-surface fork — repo copy
   under `pdf` stays canonical).
5. Before any of the above, confirm the three governor uploads still match
   HEAD (Runbook 3 parity; domain-reference A2 noted them STALE once already).

## Flagged, not fixed (out of this pass's scope)

- install-and-surfaces Runbook 1 still copies the five-governor set including
  the retired pair, while the README's install loop copies the active three +
  brand-standard — a pre-existing inconsistency between the two documents,
  surfaced during this audit; reconcile via a Decision 5/7-aware edit.
- Gated wording passes deferred (Decision 8 records them): brand-standard's
  artifact enumeration (+ workbooks), skill-authoring's description NOT phrase
  for mcp-builder.
- A dataviz skill remains a candidate; frontend-design's carve-out names the
  gap honestly until one exists.
