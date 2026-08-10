# The image-output skill — survey and proposal (2026-08-10)

> **Addendum, same day:** the owner approved decision A ("Proceed with A").
> The draft was moved into the live tree — skill at
> `.claude/skills/photo-editing/`, eval set at `evals/photo-editing.json` —
> and the links below were updated to the live paths (single-copy law; no
> draft duplicate retained). Trigger evals remain the adoption gate for
> anything beyond project scope. Decision B (generation vendor) stays open.

**Owner request (near verbatim):** "research what is the most powerful and
best product output skill.md — propose to me what is the cleanest and most
legit for you to implement here", clarified same day: "IMAGE generation. Not
particularly animated, but particularly photo editing." This report re-scopes
`../product-output-skill/REPORT.md` per that clarification (its bounds
anticipated exactly this).

**What was analyzed:** the image-skill ecosystem from primary sources
(fetched 2026-08-10): the full official `anthropics/skills` repo (cloned at
commit `f17010c9`, every SKILL.md read), the strongest community
photo-editing and generation-API skills (actual SKILL.md/README files
fetched raw), and Anthropic's platform docs (vision, code-execution tool,
cloud environments) — against this library, the live install footprint, and
this container's measured capabilities.

**Method:** a 4-agent research workflow (165,915 subagent tokens, 37 tool
uses) under delegation-discipline briefs; every agent's claims graded
EVIDENCE/LEAD at source; the four most load-bearing claims re-fetched
first-hand before this report rests on them (peterkrueck SKILL.md rules, the
17-directory official tree, the vision-doc FAQ, the code-execution package
list). Live-fire verification ran in this container: toolchain probe,
Pillow bootstrap timing, and an end-to-end run of the proposed procedure.
Raw agent outputs are committed in [`survey/`](survey/). Proposals only —
nothing was installed.

**Headline:** Claude has no native image output anywhere — Anthropic's own
FAQ: "No, Claude is an image understanding model only. It can interpret and
analyze images, but it cannot generate, produce, edit, manipulate, or create
images" (EVIDENCE, vision docs, fetched 2026-08-10). Every image an agent
ships is made by tool-side code or an external model API. For **photo
editing** — the owner's stated priority — there is no official Anthropic
skill (all 17 enumerated; zero own photo editing), and the best community
implementation wins by doing exactly what this library's laws already
demand. The cleanest, most legit implementation is the attached
fresh-authored **`photo-editing`** draft: lints PASS, its measuring script
live-fired on three cases, and the full procedure demonstrated end-to-end in
this very container. **Generation** is an API-key decision that belongs to
the owner; it is tiered as options, not authored.

---

## 1. Ground truth — what any image skill can rely on (all EVIDENCE, 2026-08-10)

- **No native generation or editing, on any surface.** Vision-doc FAQ quoted
  above; re-fetched first-hand. Everything below is tool-side.
- **Vision input is strong but metadata-blind:** JPEG/PNG/GIF/WebP, max
  8000×8000 px, 10 MB (API/claude.ai); and "Claude does not parse or receive
  any metadata from images" — vision cannot see EXIF rotation, which is why
  the draft's measure-law exists.
- **Toolchains are per-environment** (install-and-surfaces law, now with
  image-specific measurements): the API code-execution container ships
  `pillow` pre-installed but "has no internet access, so Claude can't
  download or install additional packages at runtime"; this Claude Code
  cloud container shipped NO image tooling (no ImageMagick, no Pillow/
  numpy/OpenCV — probed live) but `pip install pillow` through the session
  proxy took **2.7 s** and edits ran (measured this session).
- **Artifacts block external hosts** (strict CSP) — images embed as data:
  URIs; observed from this running surface's own tool contract
  (support-center article unreachable through this proxy — egress-blocked,
  stated in bounds).

## 2. Photo editing — the survey (owner's priority)

| Candidate | What it is | Verdict |
|---|---|---|
| **`image-edit`** — peterkrueck/Claude-Code-Development-Kit (repo 1,383★, MIT) | Pillow+numpy, bundled measuring + cropping scripts, and all three disciplines: see the image first, "Never guess crop coordinates from visual inspection", "Always save to a NEW file. Never overwrite the original" (quotes re-fetched first-hand) | **THE PATTERN TO MATCH** — ideas folded, no text vendored |
| `image-processing` — jezweb/claude-skills (962★, MIT) | Pillow via a bundled CLI (resize/trim/convert/optimise/thumbnails); no visual verify step | Strong second; confirms Pillow-plus-scripts as the winning shape |
| ImageMagick reference skills (TerminalSkills 126★, einverne 119★) | Copy-paste CLI recipe books; no verification loop, no originals-protection | Reference value only — recipes without laws |
| `image-enhancer` — ComposioHQ list (list repo 72k★) | Prompt-only: 99 lines naming no library, script, or API | **The anti-pattern** — intent without procedure |
| Official Anthropic repo | 17 skills enumerated at `f17010c9`; **none** owns photo editing (closest: slack-gif-creator loads uploads with PIL for GIF frames) | The lane is genuinely open — even Anthropic hasn't shipped it |

INFERENCE, stated: the community converged on Pillow + deterministic
scripts + a vision verify loop independently of this library — which is
this library's own doctrine (measure-instead-of-eyeball = live-state-truth;
exercise-over-inspect = adversarial-verify) applied to pixels. That
convergence is the "most legit" signal: the best external skill and the
house laws agree.

## 3. Generation — the survey (API-key territory)

| Path | Gen | Edits photos | Needs | Note |
|---|---|---|---|---|
| Nano Banana skills — kingbootoshi/nano-banana-2-skill (403★, MIT, updated 2026-08-09); kkoppenhaver/cc-nano-banana (365★) | ✓ | ✓ (reference-image edits) | `GEMINI_API_KEY` | The dominant community path |
| Replicate MCP (org-official) | ✓ | model-dependent | Replicate token | Vendor-official server |
| Stability MCP (tadasant, 85★) | ✓ | ✓ heavy: remove-background, outpaint, search-and-replace, upscale | Stability key (~$0.01/credit, its README) | The ML-edit ops photo-editing routes out |
| gpt-image-1 MCP / fal MCP / BFL Flux Kontext | ✓ | ✓ (masks/inpaint) | vendor keys | Present but thinner communities |
| Official Anthropic creation skills (canvas-design, algorithmic-art — Apache 2.0) | ✓ code-rendered art | ✗ | none | Key-free "designed image" route; overlaps installed frontend-design |

Star-count trap (EVIDENCE): the single most-starred "nano banana skill"
repo (1,818★) is a prompt-recommendation library, not a generator — raw
popularity rankings mislead in this niche.

## 4. Gap analysis for this library

- **Photo editing: wholly unowned and now evidenced.** No official skill, no
  installed skill, no governor covers it; the deterministic core
  (crop/resize/rotate/convert/color/composite) needs no keys and runs on
  every surface with Python.
- **ML edit operations** (background removal, real upscaling, generative
  fill): only via external APIs or local models — per-environment,
  key-gated; the draft routes these out honestly instead of faking them
  with resampling.
- **Generation from scratch:** designed images (posters, cards, OG images)
  are largely covered key-free by installed frontend-design + the artifact
  surface + a headless-browser screenshot; photographic/artistic generation
  is impossible without a vendor key — an owner spend decision.

## 5. The proposal — `photo-editing`, authored fresh and live-verified

Draft (now live at [`.claude/skills/photo-editing/SKILL.md`](../../../.claude/skills/photo-editing/SKILL.md)
per the adoption addendum above) —
lints **PASS, zero warnings**; description 995 chars (≤1000 house target);
149 lines. Ships one bundled script,
[`scripts/inspect_image.py`](../../../.claude/skills/photo-editing/scripts/inspect_image.py)
(dimensions, format, alpha, EXIF orientation, content bounds in PIL
crop-box convention). Trigger cases:
[`evals/photo-editing.json`](../../../evals/photo-editing.json) — 4
should-fire + 3 should-not with seeded image fixtures per INC-2/INC-8,
grading committed 2026-08-10, **NOT YET RUN**.

Three laws, all convergent with the best surveyed skill and with house
doctrine: (1) never overwrite the original; (2) measure before you cut —
numbers from the script, never from looking; (3) see-edit-verify — view
before, view after, re-edit from the original.

**Live-fire evidence (this container, 2026-08-10):** the inspect script
returned exact bounds on a padded test image and degraded gracefully on
flat/transparent edge cases; the full procedure then ran end-to-end —
measured crop box `(50,40,151,111)` → new file `…-cropped-101x71.png` at
exactly the computed size with zero residual border, the output visually
confirmed, and the original's MD5 unchanged. The procedure is not just
plausible; it executed.

Composition note: `photo-editing` plugs into the `product-output` draft's
route table as the image-lane owner (if both are adopted); each stands alone
if not.

## 6. Bounds — what this analysis did NOT cover

- Egress blocks from this environment: skillsmp.com, support.claude.com,
  replicate.com, ai.google.dev, docs.anthropic.com (platform.claude.com and
  code.claude.com worked). Vendor model docs (Gemini/OpenAI/Stability
  official pages) were not fetched — key requirements and pricing come from
  the wrapper repos' own READMEs, single-source.
- Star counts are as displayed on fetch date; GitHub rounds.
- Single-pass survey; the claude.ai in-chat analysis environment was not
  verified (distinct from the API code-execution tool that was).
- No trigger or behavioral evals ran — the draft's value is argued and
  live-fired once, not measured across sessions. One end-to-end run is an
  anecdote by the house's own standard; the eval set exists to fix that.
- Delegate outputs beyond the four re-fetched claims were spot-checked at
  the summary level only.

## 7. Decision sheet (owner calls — nothing below was executed)

| # | Option | Cost | When it pays off |
|---|---|---|---|
| A | **Adopt `photo-editing` as a candidate**: move draft + script → `.claude/skills/photo-editing/`, evals → `evals/`, README row; run the trigger protocol | one move + one eval session | every image edit, on every surface with Python |
| B | Generation: pick a vendor path — B1 install kingbootoshi/nano-banana-2 (MIT, needs `GEMINI_API_KEY`); B2 author a thin house `image-generation` skill around whichever API you provision; B3 rely on the key-free programmatic-render route already covered; B4 defer until a recorded need | B1/B2 need a key + spend decision | only if from-scratch photographic/artistic generation is a real lane |
| C | Fold the "vision is metadata-blind" fact into any future vision-adjacent skill work | trivial, gated edit | avoids a whole class of rotated-image bugs |
| D | Do nothing | zero | the pieces stay per-session improvisation |

Recommended: **A**, with B left genuinely open — B is a spend-and-vendor
choice the record cannot make for you (the survey found no key already
provisioned in this environment; none of `GEMINI_API_KEY`/`REPLICATE_API_TOKEN`/
`STABILITY_API_KEY`/`FAL_KEY`/`OPENAI_API_KEY` is set here, checked live
2026-08-10).

## 8. Provenance

Produced 2026-08-10 by the Claude Code cloud session on branch
`claude/product-output-skill-research-jt42nu` (owner-clarified request),
using a 4-agent research workflow (results committed in `survey/`;
165,915 subagent tokens and 37 tool uses reported for the completed run —
an earlier partial run, interrupted by a session pause and resumed from
cache, consumed additional unreported tokens) plus first-hand re-fetches
and live-fire runs by the orchestrating session. Primary sources, all fetched
2026-08-10: `github.com/anthropics/skills` (clone at `f17010c9`),
`platform.claude.com` vision + code-execution + best-practices docs,
`code.claude.com` cloud-environments docs, raw SKILL.md/README files of
peterkrueck/Claude-Code-Development-Kit, jezweb/claude-skills,
TerminalSkills/skills, einverne/dotfiles, ComposioHQ/awesome-claude-skills,
kingbootoshi/nano-banana-2-skill, kkoppenhaver/cc-nano-banana,
replicate/replicate-mcp-code-mode, tadasant/mcp-server-stability-ai,
luminarylane/fal-mcp-server, CLOUDWERX-DEV/gpt-image-1-mcp,
agentic-ai-forge/bfl-flux-mcp. Re-verify volatile claims by re-fetching
those sources and re-probing the live environment (`python3 -c "import
PIL"`, `env | grep -iE 'gemini|replicate|stability|fal|openai'`). No skill,
eval, hook, or config was installed by this report — draft and proposals
only.
