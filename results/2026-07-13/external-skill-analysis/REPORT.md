# External skill library analysis — after-report (2026-07-13)

Owner request: analyze three external repos for skills that would supplement the
core library without touching it; tier what's worth adding; note redundant
entries briefly and move on.

**Repos analyzed:** `BehiSecc/awesome-claude-skills` (a ~170-entry link
catalog — nothing installable in the repo itself), `obra/superpowers` v6.1.1
(14 skills + hooks, MIT), `Sahir619/fable-method` (3 skills + eval harness,
MIT). Per owner instruction, the awesome list's links were followed: 14 linked
skills/collections were cloned and deep-evaluated, chosen for domain spread
(documents, security, science, data, writing, personal ops, PM, IaC).

**Method:** 62-agent workflow — full inventory of every SKILL.md, per-candidate
comparison against (1) the 14 core skills, (2) platform built-ins on both
surfaces (Claude Code: plan mode, subagents, code-review/verify/deep-research
etc.; claude.ai: native docx/xlsx/pptx/pdf, artifacts, research mode), and
(3) the base-model standard that retired live-state-truth ("if the model
already does it uncued, the skill is dead weight"). Every MUST ADD / HIGHLY
RECOMMEND call was then adversarially refutation-tested by an independent
agent instructed to read the actual files plus architecture-contract, and to
downgrade when torn. **10 of 13 high-tier calls were downgraded by that pass;
3 survived.** Full verdicts, rationales, refutations, and the complete
awesome-list catalog: `analysis-result.json` (this directory).

**Headline:** the core library survives contact. Nothing found replaces or
improves any governor — 8 of 14 superpowers skills and 2 of 3 fable-method
skills are majority-restatements of plan-gate / adversarial-verify /
scope-fence or platform built-ins. The real gaps are all **domain
capability**, not governance: Office documents on Claude Code, security,
science/data, and a few engineering execution mechanics.

---

## MUST ADD (1)

### 1. Anthropic official document skills — docx, pdf, pptx, xlsx only
`anthropics/skills` · install as plugin (repo ships its own marketplace) ·
source-available license (use as plugin; check terms before vendoring text)

The single highest-leverage gap. Claude Code has **zero** Office-document
capability; these four are production-grade (unpack-XML-edit-repack with XSD
validation, tracked-changes acceptance via LibreOffice, comment plumbing,
AcroForm filling with bounding-box checks, xlsx recalc) — corruption-avoiding
mechanics a base model cannot reproduce freehand. Direct daily leverage:
brand-standard resumes/letters rendered to real .docx/.pdf in Code sessions.

Transparency note: the verifier UPHELD the *whole collection* at HIGHLY
RECOMMEND, discounting it because half the collection is redundant
(webapp-testing / web-artifacts-builder / internal-comms overlap built-ins and
brand-standard, and claude.ai already ships the document skills natively).
This report scope-promotes the **four document skills only** to MUST ADD —
the redundancy discount doesn't apply to that subset on the Claude Code
surface. Skip the rest of the collection. Owner can veto the promotion; the
verified collection-level grade stands in the evidence file.

Observed loose end (dated 2026-07-13): empty untracked dirs
`results/2026-07-12/{docx,pdf,pptx,internal-comms,mcp-builder,...}` exist
locally, matching anthropics/skills names — evidence a prior session began
evaluating these; nothing tracked, nothing adopted.

## HIGHLY RECOMMEND (2)

### 2. Trail of Bits security skills
`trailofbits/skills` · 75 skills, HEAD 2026-06-30 · CC BY-SA 4.0 ·
Claude Code plugin, on-demand

Security is the one owner-named domain with zero core coverage, and this is
the definitive vendor-official pack: differential-review (risk-first PR review
with git-history baselining and blast-radius calculation — far deeper than the
built-in security-review), fp-check (TRUE/FALSE-POSITIVE verdicts via
source-to-sink tracing), CodeQL/Semgrep orchestration, variant analysis,
fuzzing curriculum, constant-time/zeroize audits — with a documented real
upstream find (RustCrypto ML-DSA timing side-channel). **License caution:
ShareAlike — install as a plugin; do NOT copy its text into this repo.**

### 3. subagent-driven-development
`obra/superpowers` · MIT · Claude Code only · on-demand

The one superpowers skill that fully survived refutation. Built-ins provide
the dispatch mechanism; this supplies the operating discipline nothing in the
stack has: model-tier economics ("turn count beats token price"; an omitted
model silently inherits the expensive session model), the review-package
BASE-never-HEAD~1 trap, file-based handoffs that keep bulk artifacts out of
controller context, a 4-status implementer protocol with escalation ladder,
reviewer-integrity rules, and a compaction-survivable progress ledger.

## NICE TO HAVE — adopt when the trigger situation is real

**Engineering discipline (obra/superpowers, MIT).** Each has a genuinely
net-new sliver; none earns install until the situation recurs in practice:

| skill | the net-new sliver | placement if adopted |
|---|---|---|
| systematic-debugging | 3-strike fix counter with hard stop → architecture escalation; per-component-boundary instrumentation | see fold list below |
| test-driven-development | enforcement of test-BEFORE-code ordering (verify-RED, delete-means-delete, 11-row rationalization table) — everything in core is post-hoc | project-scoped in dev repos |
| writing-plans | the zero-context executable plan document (Interfaces Consumes/Produces, no-placeholders rule) | on-demand, pairs with #3 |
| receiving-code-review | verify-reviewer-claims-against-codebase checklist; all-or-nothing clarification rule | on-demand |
| finishing-a-development-branch | worktree/branch teardown ordering traps | project-scoped |
| using-git-worktrees | harness-tools-first doctrine; submodule/check-ignore guards | on-demand (harness already ships worktree tooling) |
| writing-skills | pressure-test toolkit (see fold list — don't install as competing skill next to skill-authoring) | fold only |

**Domain packs (all on-demand plugins/checkouts; zero always-on cost):**

- **claude-scientific-skills** (K-Dense-AI, MIT, 149 skills) — genuinely
  net-new science/data drivers (rdkit, scanpy, diffdock, database-lookup with
  real injection-hygiene). Adopt the day science/bio/data work appears.
- **claude-skills** (jeffallan, MIT, 66 stack personas) — value is the 366
  reference files (postgres-pro's ~1,900 lines of EXPLAIN/VACUUM/replication
  SQL, react migration guides), not the personas. Cherry-pick per stack.
- **hashicorp/agent-skills** (MPL-2.0, vendor-official, commit-fresh) —
  best-in-class, but IaC/Terraform is not currently in the owner's life.
  Bookmark; adopt on first Terraform task.
- **pm-skills** (product-on-purpose, Apache-2.0, 68 skills) — highest
  authoring quality of any third-party library evaluated (When-NOT
  cross-links, trigger-eval fixtures). PM lifecycle only matters if that work
  materializes.
- **career-ops** (MIT) — exceptional job-search application (~37K lines of
  tooling, ghost-job scoring, anti-fabrication fences) but ships its own
  voice/typography that **conflicts with brand-standard** — if adopted,
  project-scoped with brand-standard explicitly overriding its voice assets.
- **avoid-ai-writing** (MIT, 683 lines) — real mechanical detection (citeturn
  leaks, `utm_source=chatgpt.com`, placeholder regexes, cluster/density
  thresholds). Better folded than installed — see fold list.
- **tapestry-skills** (MIT) — only `youtube-transcript` earns (subs→Whisper
  fallback chain, VTT dedup); the rest fails the retirement standard.
- **OpenPaw** (MIT) — curated Mac-local personal-ops toolchain map (himalaya,
  imsg, openhue-cli, peekaboo…). Only useful on a local Mac, not cloud.
- **agnix** (MIT/Apache-2.0) — 432-rule agent-config linter, exceptionally
  maintained; but it validates surfaces (hooks/MCP/plugin schemas) this repo
  barely uses yet. Revisit when the config footprint grows.
- **owasp-security** (agamm, MIT) — most content is base-model-known;
  the framework-middleware false-positive rule is the one keeper.
- **sanjay3290/ai-skills** (Apache-2.0) — only the postgres/notebooklm/
  elevenlabs slices. **Trust flag: the Google Workspace block routes OAuth
  through a third party's cloud function with a hardcoded client ID
  (gmail/scripts/auth.py) and rejects personal Gmail accounts — do not use;
  the Gmail/Drive/Calendar connectors already cover it.**
- **fable-method + fable-judge** (Sahir619, MIT) — ~80% restates the
  governors (their own eval shows nulls for Sonnet-class models on the
  primary-sources rule — independently replicating the live-state-truth
  retirement). fable-judge's third-party-completion-audit angle is mostly
  inside adversarial-verify's existing third-party clause. The repo's real
  export is a methodology lesson (see fold list #4).

## NOT NEEDED — noted briefly, per instruction

From superpowers: `brainstorming`, `executing-plans` (plan-gate + plan mode),
`dispatching-parallel-agents` (harness-native), `requesting-code-review`
(built-in /code-review is strictly deeper), `using-superpowers` (bootstrap
injector for their plugin), `verification-before-completion` (near-total
overlap with adversarial-verify). From fable-method: `fable-loop` (restates
plan-gate + adversarial-verify over built-in orchestration). From the awesome
list: ComposioHQ collection (file-organizer etc. — the exact
etiquette-prose class that retired live-state-truth). The awesome list itself:
a bookmark to re-scan quarterly, not a dependency.

## Fold, don't add — graft candidates for existing core skills

Each of these is an idea worth stealing INTO a core skill rather than a skill
to install beside it. Every one gates through research-methodology
(hypothesis → A/B → N=2 floor) and architecture-contract before any edit:

1. **writing-skills → skill-authoring**: the Match-the-Form-to-the-Failure
   table (A/B-tested finding: prohibitions backfire on output-shaping
   problems), the rationalization-table technique, and the empirical SDO trap
   (workflow-summarizing descriptions cause agents to skip skill bodies —
   directly relevant to the description-as-trigger doctrine).
2. **avoid-ai-writing → brand-standard**: a short mechanical-fingerprint
   subsection (citeturn/oaicite leaks, utm params, placeholder regexes,
   banned-cluster density) for external-facing drafts.
3. **systematic-debugging → plan-gate branch-rule doctrine (or a future
   code-debugging governor)**: the 3-strike fix counter with mandatory
   architecture escalation.
4. **fable-method eval log → research-methodology**: citable external
   replication that a rule shipped as a *forced report artifact* outperforms
   the same rule as mid-list prose (their INTENT-gate: 0/4 → 1/4 → 4/4).

## Placement discipline (per architecture-contract Decision 5)

Nothing new earns always-on. The always-on set is unchanged: plan-gate,
adversarial-verify, scope-fence (+ brand-standard per the standing footprint,
commit 0b7ac4d). Every recommendation above is a plugin or on-demand install —
zero per-session context cost until invoked.

## Licenses at a glance

MIT: superpowers, fable-method, jeffallan, K-Dense, tapestry, OpenPaw,
career-ops, avoid-ai-writing, owasp, agnix (dual w/ Apache-2.0).
Apache-2.0: pm-skills, sanjay3290. MPL-2.0: hashicorp.
**CC BY-SA 4.0: Trail of Bits — plugin-only, never copy text into this repo.**
Anthropic document skills: source-available — consume via their plugin
marketplace.

## Bounds, stated plainly

Single-pass analysis (one compare agent + one refutation agent per candidate;
not the N=2 experiment floor — that floor governs *accepting skill edits*, and
no core skill was edited). ~170 awesome-list entries cataloged; 14 deep-dived;
the rest were deprioritized by domain spread and quality signals, not
evaluated — the full catalog with URLs is in `analysis-result.json` for future
sweeps. Tier calls on domain packs assume the owner's current work mix
(documents/writing/career daily; security/science/IaC latent). Workflow cost:
62 agents, ~3.0M subagent tokens, 54 min, 0 agent errors.

## Proposed next actions (pending owner approval — nothing executed)

1. Owner approves/amends the tier list above.
2. Install MUST ADD + approved HIGHLY RECOMMENDs as plugins in a fresh
   session; register-then-verify per install-and-surfaces.
3. Run fold candidates 1–4 through research-methodology one at a time.
4. Re-scan the awesome list quarterly (it updates ~monthly).
