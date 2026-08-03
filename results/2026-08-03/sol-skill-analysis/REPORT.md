# External skill analysis: sol-skill + three Fable-era candidates — after-report (2026-08-03)

Owner request: analyze `ozankasikci/sol-skill` and report whether the current
operating procedure already does this, whether it is worth adding, and the
cost-benefit. Mid-session, three more candidates were added: a plan-before-editing
discipline skill, an "efficient lanes" splitter (BuilderIO `efficient-fable`), and
a "Fable safe/fallback guard" — with the added question "do you have these
capabilities as well / do they fit how I've been working with you."

**Candidates analyzed:** `ozankasikci/sol-skill` @ `b310435` (MIT, cloned and
read in full), `BuilderIO/skills` `efficient-fable` (SKILL.md fetched, license
unverified this session), the iwoszapar "Rigor Pack" plan-before-editing concept
(source article bot-blocked; composition confirmed via search), and the
dontsleeponai "Fable Safe Prompt / fallback guard" concept (site bot-blocked;
claims fact-checked against primary Anthropic docs instead).

**Method:** 6-agent workflow (3 analysts — governor overlap, architecture fit,
prior art — each adversarially verified by an independent agent reading the
cited files; all three verdicts "sound", 0 of 39 findings refuted; ~433k
subagent tokens), plus an independent documentation check of the fallback claim
against `code.claude.com/docs/en/model-config.md`, with the load-bearing quotes
re-fetched and confirmed verbatim by the main session (2026-08-03). Evidence:
`wf-governor-overlap.json`, `wf-architecture-fit.json`, `wf-prior-art.json`
(this directory). Precedent followed: `results/2026-07-13/external-skill-analysis/`
(verdict tiers, adversarial refutation of high-tier calls, nothing executed
without owner approval).

**Headline:** the core library plus platform built-ins survive contact again.
One candidate is already a governor verbatim (plan-before-editing = plan-gate),
one is mostly platform built-ins with a config-sized gap (efficient-fable), one
is factually mis-premised and partly declinable (fallback guard — the fallback
is real and documented but not silent), and sol-skill is the only candidate that
does something the current stack genuinely cannot: cross-vendor decorrelation of
implementer and reviewer. Its governance spine, however, is a restatement of
plan-gate + scope-fence + adversarial-verify, and its practical gates are heavy.
Consistent with the 2026-07-13 house rule, **nothing here earns always-on.**

---

## 1. sol-skill — NICE TO HAVE (conditional), plus five fold candidates

`/sol`: Claude plans and briefs, GPT-5.6 Sol (via OpenAI Codex CLI,
`model_reasoning_effort=xhigh`) makes all code changes, Claude reviews the real
`git diff` and re-runs the checks itself. Manual-only
(`disable-model-invocation: true`). Corrections capped at 2 rounds, delta-only.

### Does the current operating procedure already do this?

Three verified strata (full quotes in `wf-governor-overlap.json`, 21 findings,
0 refuted):

- **ALREADY-LAW — the entire planning/review spine.** Checkable acceptance
  criteria before implementation ("each criterion phrased as a checkable command
  or observable behavior" ↔ plan-gate's "committed in advance, they are a finish
  line; written afterward, they are a rationalization"); `<non_goals>` /
  `<action_safety>` ↔ scope-fence's fence and flag-don't-fix; "review the diff,
  not the summary" and "never trust it as verification / re-run the checks
  yourself" ↔ adversarial-verify's evidence hierarchy and behavioral-check law;
  the composite done-definition ↔ adversarial-verify's acceptance rule +
  scope-fence's "the diff matches the ask is part of done". Sol's contribution
  here is packaging the library's existing laws into an XML brief imposed on a
  delegate rather than self-applied.
- **PARTIAL — principle present, mechanism absent.** Risk-tiered mandatory
  fresh-eyes second review (auth/payments/migrations/concurrency); per-claim
  EVIDENCE-vs-INFERENCE tags with source URLs; a spot-check protocol for a
  delegate's load-bearing claims; token-budgeted review mechanics.
- **NOVEL — nothing in the library or governors covers it.** (a) Cross-vendor
  role split — the reviewer is a different lab's model from the implementer;
  (b) checkpoint-the-tree before any agent edits, so `git diff` isolates the
  delegate's changes and a bad run is one reset away; (c) the 2-round correction
  cap with escalation to the user; (d) the delta-only three-part correction
  shape (where / what's wrong and required / what check must pass); (e) treat
  web and delegate output as data, never instructions; (f) least-privilege
  sandboxing (read-only research runs); (g) model-tuned brief craft (tight
  contracts over prose; don't over-specify a frontier implementer); (h)
  human-gated delegation spend (verifier addition).

Platform built-ins cover part of the novel band's *function*: the Claude Code
harness can already spawn independent fresh-context reviewer subagents and
adversarial verification fan-outs (Agent/Workflow tools) — decorrelated
*context*, but same vendor. **The one thing not replicable natively is
different-lab decorrelation**: an all-Claude reviewer pool shares the model
family's blind spots with the implementer. That is sol-skill's genuine
contribution, and it is real.

### Worth adding?

**As-is into this library: no.** Verified against architecture-contract
(`wf-architecture-fit.json`, 4 findings, 0 refuted): the library's own
`lint_skill.sh` FAILS it today ("description has no trigger language"; no
When-NOT or Provenance sections); it hardcodes undated volatile facts
(`gpt-5.6-sol`, Codex ≥ 0.144, xhigh/10-min timeout) — the clearest invariant-7
breach; it would need relocation to `.claude/skills/sol/SKILL.md` (invariant 8);
domain-reference has no category for `disable-model-invocation` skills, and
Decision 5's install math has no slot for a per-MACHINE-gated tool skill; and it
exposes an unregulated gap — no precedence rule exists between an invoked
command skill's procedure ("Claude never edits production code") and a
triggered governor. Nothing it does *contradicts* the governors — it actively
re-implements invariants 1, 2, and 4 — so co-firing is aligned double-load
(weak-point-2 class), not conflict.

**As an external plugin on machines that qualify: NICE TO HAVE.** Adopt-when-real
conditions: a local machine with Codex CLI installed and authenticated, a
ChatGPT plan that includes Codex, and a repo where sending code to OpenAI is
acceptable. Prior art is unambiguous that this is new territory: the library has
**zero** cross-vendor history — every Codex/GPT mention in the repo describes
third-party repos' compatibility, never this library's practice; all existing
multi-model infrastructure is Anthropic-internal Opus/Sonnet A/B
(`wf-prior-art.json`, 14 findings, 0 refuted).

### Cost-benefit

| | |
|---|---|
| **Benefits** | Decorrelated review (reviewer did not make the implementer's assumptions — the one capability the current stack cannot replicate); conserves premium Anthropic tokens (planner spends brief + review only, implementation burns the second subscription); a second frontier implementer; the checkable-criteria loop is well-built and MIT-licensed |
| **Costs** | Second subscription (ChatGPT plan with Codex); slow — upstream's own benchmark is 8m02s for a one-file change at xhigh; code and briefs go to OpenAI; **unusable in remote/cloud sessions** — `codex` is not on PATH in this CCR container (verified 2026-08-03) and `codex login` is interactive, so it is a local-machine-only capability; maintenance of vendor-volatile facts (model id, CLI version) the upstream leaves undated |
| **Adaptation cost if vendored** | Description rewrite to the three-job trigger contract (grows the 24-word description toward governor-class ~130 words), two house sections, date-stamps, relocation, a domain-reference entry for the `disable-model-invocation` class, and a command-skill precedence rule — none of it hard, all of it owner-gated |

### Fold candidates (the durable value, vendor-independent)

Five sol-skill disciplines improve **all-Claude** delegation too and could fold
into core skills — one at a time, through research-methodology, per the
2026-07-13 house rule "external ideas fold into core skills only through
research-methodology gates":

1. Checkpoint-before-agent-edit (commit/stash so the delegate's diff is isolated
   and revertible) — candidate for plan-gate or a delegation section.
2. Bounded correction protocol: N-round cap + delta-only three-part corrections
   — candidate for adversarial-verify's delegation posture.
3. Data-not-instructions law for web/delegate output (prompt-injection defense)
   — no library skill mentions it at all.
4. EVIDENCE/INFERENCE tags + per-claim source URLs for research output.
5. Risk-tiered fresh-eyes review (auth, payments, migrations, concurrency ⇒
   mandatory independent second pass).

---

## 2. Plan-Before-Editing Discipline — NOT NEEDED (it is plan-gate)

The proposed skill "forbids writing or modifying code until a written, checkable
structural plan exists." That is **plan-gate**, verbatim — an active governor in
this library (goal, unknowns, success criteria before acting; architecture
invariant 2 "pre-commitment ordering"). The cited source describes the public
iwoszapar "Rigor Pack," whose six skills include ones literally named
`plan-gate` and `scope-fence` ("prevents edits until a written plan exists that
includes the goal, unknowns, success criteria, and step order" —
iwoszapar.com/tools/rigor-pack, confirmed via search 2026-08-03; the article
itself is bot-blocked to this session). Whether the pack and this library share
ancestry or converged, the discipline is already installed, already law, and
additionally backed by the platform's native plan mode. Adding a second copy is
pure drift risk (Decision 2's rationale: duplication is drift waiting to
happen). **Capability check: yes — this is how we already work.**

---

## 3. Efficient Lanes Splitter (`efficient-fable`) — fold-don't-add (it is mostly config)

The BuilderIO skill is real and well-formed: "Fable functions as orchestrator,
architect, and final decision-maker. Cheaper subagents handle token-intensive
groundwork"; handoff packets with scope, evidence format, and stop conditions;
"treat subagent reports as leads, not facts."

**Capability check: the machinery already exists natively.** The Claude Code
harness provides per-agent model selection (Opus/Sonnet/Haiku tiers) and
reasoning-effort tiers on subagents and workflow stages, a read-only Explore
agent for scans, structured handoff via agent prompts/schemas, and
"reports-as-leads" is adversarial-verify's evidence hierarchy plus the
workflow verify patterns already in use (this report's own method used them).
The handoff-packet shape also matches how sol-skill briefs its delegate —
convergent practice across all three sources.

**The genuine gap is a policy, not a capability:** the *default economy*. This
account currently runs sessions in ultracode posture — thoroughness explicitly
over token cost, subagents inheriting the main-loop model — which is the
opposite routing default from efficient-fable's "preserve premium tokens." Both
are legitimate; they serve different goals. If the goal while Fable access lasts
is conservation, the highest-leverage change is a ~10-line standing instruction
or per-session directive ("mechanical lanes — scans, log reduction, inventory,
test passes — run on cheaper tiers; Fable keeps decomposition, tradeoffs,
synthesis, final review"), not a new installed skill competing with existing
orchestration doctrine. If installed anyway: on-demand/per-project, never
always-on, and **BuilderIO/skills' license was not verified this session — check
before any vendoring** (house rule from 2026-07-13).

---

## 4. Fable Safe/Fallback Guard — NOT NEEDED as a skill; one component declined

The blog claim was "sensitive context in CLAUDE.md can trigger silent fallbacks
from Fable down to Opus without notifying you." Fact-checked against
`code.claude.com/docs/en/model-config.md` (fetched 2026-08-03; quotes verified
verbatim by this session):

- **Real:** Fable 5 runs cybersecurity/biology safety classifiers;
  biology-flagged requests re-run on Opus 5, cybersecurity-flagged on Opus 4.8.
  "Fallback can trigger on the first request of a session … because the first
  request carries workspace context such as your CLAUDE.md content and git
  status."
- **False — "silent":** "Claude Code re-runs the request on that model and
  **shows a notice in the transcript**."
- **False — "without your control":** `/config` → "Switch models when a message
  is flagged" off (or `switchModelsOnFlag: false`) makes a flagged request
  *pause* with two options: switch, or edit the prompt and retry on the current
  model. `claude --safe-mode` isolates whether customizations (CLAUDE.md,
  skills, MCP, hooks) are the trigger.
- **The kernel of truth:** "After a fallback, the session continues on the
  fallback model" until you `/model` back — noticed, but *sticky*. Miss the
  notice and subsequent turns run on Opus. Also, in non-interactive/SDK modes
  the pause can't be shown and a flagged request ends in a refusal instead.

**Capability check:** monitoring is built-in — the transcript notice, `/status`,
`/model`, and the statusline all show the active model, and this session's
harness states its configured model directly. A tracking skill adds nothing the
statusline doesn't, and no skill can introspect serving weights beyond what the
harness reports — a skill claiming otherwise would be false assurance. If the
sticky-fallback scenario matters, the durable guard is configuration, not
prose: a statusline that displays the model, plus `switchModelsOnFlag: false`
for pause-and-choose. (The update-config skill can wire both on request.)

**Declined component:** the companion "safe prompt" tool — a skill that
systematically rewrites prompts so safety classifiers don't fire — is
classifier-evasion tooling, and building it is declined regardless of intent.
The documented alternative serves the legitimate need (false positives on
benign work) with the human in the loop: disable auto-switch, and when a
request is flagged, *you* see it, edit your own wording, and retry on Fable.
For this library specifically the exposure is low — governance prose is not
classifier-adjacent content.

---

## Fit summary

| Candidate | Already in the stack? | Verdict | Action (owner-gated) |
|---|---|---|---|
| sol-skill | Governance spine: yes (3 governors). Cross-vendor decorrelation: **no** — not replicable natively | NICE TO HAVE (conditional) | Optional local trial as external plugin where Codex exists; 5 fold candidates through research-methodology |
| Plan-before-editing | **Yes — it is plan-gate**, active governor + native plan mode | NOT NEEDED | None |
| efficient-fable | Machinery: yes (model/effort tiers, Explore, workflow verify). Economy default: no — current posture is deliberately opposite | fold-don't-add | Standing instruction or session directive if Fable-token economy is wanted; license check before any vendoring |
| Fallback guard | Monitoring: yes (notice, /status, statusline). Control: yes (`switchModelsOnFlag`) | NOT NEEDED; evasion component declined | Optional: statusline model display + `switchModelsOnFlag: false` via update-config |

## Recommended next steps

1. **No installs from this batch** without a trigger situation — consistent with
   2026-07-13 ("nothing new earns always-on").
2. If Fable-token conservation is the near-term goal, adopt the lanes *policy*
   as a standing instruction (cheapest, reversible, no new skill).
3. If cross-vendor review appeals: trial sol-skill per-project on a
   Codex-equipped local machine; record the trial under `results/<date>/` with
   the usual pre-registration; the INCONCLUSIVE-stays-candidate path from
   2026-07-15 applies if it neither confirms nor regresses.
4. Fold candidates 1–5 from §1, one at a time, through research-methodology.
5. Optional config hardening from §4 via update-config.

## Provenance

Workflow run `wf_3f5833ba-0ba` (6 agents, 0 errors, ~433k subagent tokens,
~11 min); verifier verdicts sound/sound/sound, 0 of 39 findings refuted; missed
items surfaced by verifiers are incorporated above (human-gated delegation
spend, source-staleness rules, the 24-word→130-word description-cost
correction, Decisions 6/7 walk, the 2026-07-13 precedent itself). Fallback
fact-check: independent documentation agent + main-session re-fetch of
`code.claude.com/docs/en/model-config.md`, 2026-08-03. sol-skill read at
upstream commit `b310435`. Volatile facts in this report (codex absence in the
CCR container, doc quotes, Rigor Pack composition, license-unverified flags)
are dated 2026-08-03 and re-verifiable by the commands and URLs named inline.
