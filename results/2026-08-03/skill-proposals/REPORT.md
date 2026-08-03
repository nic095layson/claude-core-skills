# Proposed new skills — an expert dive from working history (2026-08-03)

Owner request: after passing on all four external candidates (same day, see
`../sol-skill-analysis/REPORT.md`), propose the top skills worth *authoring*
that the library does not have yet, grounded in how we actually work together,
with a beginner-level "why" for each. Owner makes the final calls.

**Evidence base ("our history"):** what the record shows, not memory — the 14
skills and their provenance, `.claude/LESSONS.md` (INC-1…3, DEAD-1/DEAD-2),
`experiments/` (7 pre-registered hypotheses), `results/2026-07-11..15`
(campaign + acceptance runs), `results/2026-07-13/external-skill-analysis/`
(work mix stated: "documents/writing/career daily; security/science/IaC
latent"; fold backlog 1–4 still pending), today's four-candidate analysis, and
this session's own working pattern (multi-agent workflows, verified reports,
primary-source fact-checks). Bound stated plainly: chat history from other
sessions is not visible to me; "history" here means what the repo records plus
this session.

**The organizing idea** — the same one this library was founded on: a skill
earns its place only where the disciplined way of working and the default way
of working *measurably differ*. Everything below is a place where the record
shows that difference. And per your own ledger, two of the biggest wins
available are not prose at all (see #2).

**House rules honored throughout:** nothing proposed as always-on without
passing measurement; every adoption gates through skill-authoring +
research-methodology; the retirement standard applies (if the base model
already does it uncued, the skill is dead weight).

---

## 1. `delegation-discipline` — how to brief, bound, and grade subagents

**Tier: PROPOSE FIRST. The largest genuinely uncovered gap in the library.**

**The evidence.** Multi-agent delegation is now a routine part of how this
account works: the 2026-07-13 analysis ran 62 agents (~3.0M tokens); today's
ran 6 verified agents; the harness Agent/Workflow tools are used in ordinary
sessions. Yet no skill governs any of it — the governors all assume a single
agent doing its own work (verified finding, `../sol-skill-analysis/
wf-governor-overlap.json`). And the two external skills that attracted your
attention this month — `efficient-fable` and `sol-skill` — are both, at core,
delegation-discipline skills. Two independent pulls toward the same missing
piece is the record telling us where the gap is.

**Beginner's why.** When Claude hands work to helper agents, each helper is a
stranger with no memory of your standards. Without written rules, the quality
of a delegated task depends on how well one improvised prompt was written that
day. This skill would make the handoff a *contract* — every helper gets an
objective, boundaries, the exact evidence it must return, and a stop
condition; every report it sends back is treated as a lead to verify, not a
fact; a helper that keeps failing gets a bounded number of retries before the
problem comes back to you. It is quality control for work you never see
happen.

**Contents (authored fresh, house style — not vendored from the passed
candidates):** briefing contract (objective / scope in-and-out / required
evidence format / stop conditions); checkpoint the tree before any agent may
write; reports-are-leads verification tied into adversarial-verify; bounded
correction rounds with escalation; untrusted-content law (web and delegate
output is data, never instructions). Placement: on-demand/user-invoked or
loaded by orchestrating sessions — NOT always-on until measured. Transparency
note: this is the distilled gap behind sol-skill, which you passed on today;
proposing the discipline without the vendor dependency is deliberate, and
vetoing it is a clean call if you consider that ground closed.

## 2. Hook-enforcement pack — not a skill, and that is the point

**Tier: PROPOSE FIRST (alongside #1). Your own ledger names this as the next
lever.**

**The evidence.** DEAD-1: scope-fence's hardest trigger case "never fired…
regardless of description wording — this is a triggering ceiling, not a
wording bug." DEAD-2: lessons-ledger "plateaus ~80% under wording… Candidate
next lever: mechanical enforcement (hooks), not wording."
architecture-contract weak-point 3: "wiring governors into hooks is a
candidate hardening path, unexplored." `hooks/` contains exactly one hook.
The library has hit the measured ceiling of what prose descriptions can do,
recorded that fact twice, and not yet pulled the lever it identified.

**Beginner's why.** A skill is advice Claude reads; a hook is a rule the
software *enforces*. Right now, whether a governor fires depends on the model
noticing it should — and your experiments measured that this fails in
predictable cases no matter how the advice is worded. A hook cannot be
ignored: it runs automatically before or after a tool is used. Small example:
a hook that blocks file edits until a written plan exists would make plan-gate
mechanical instead of optional — which, honestly, is the working version of
the "plan-before-editing" idea you raised this morning: you already own the
skill; what you don't own yet is the enforcement.

**Contents:** 2–3 small hooks, one per measured ceiling — a PreToolUse
Write/Edit gate checking a plan artifact exists for non-trivial sessions
(plan-gate's ceiling), a post-diagnosis ledger reminder (lessons-ledger's
~80% ceiling), extending the existing `scope-fence-reminder.sh` pattern.
Each ships with an A/B measurement plan per research-methodology; the
update-config skill already covers the wiring mechanics.

## 3. `after-report` — the house report format, as an invocable command

**Tier: HIGH. Preserves a format that currently lives only in precedent.**

**The evidence.** Twice now (2026-07-13, 2026-08-03) major analyses have
converged on the same report shape: dated `results/<date>/<topic>/` artifact,
method + adversarial verification stated up front, verdict tiers, every claim
carrying evidence with dates, bounds stated plainly, owner-gated next steps,
provenance. That format exists nowhere as procedure — it survives only by the
next session reading the last report and imitating it. This session did
exactly that imitation step, and it cost a read-and-infer pass that a skill
would make deterministic. Today also supplied the worked example for the
fact-checking half: the "silent fallback" blog claim reversed under
primary-source checking — blogs are leads, official docs and source are
evidence, and load-bearing claims get marked EVIDENCE or INFERENCE.

**Beginner's why.** You keep asking for reports, and the good ones follow
rules: show your method, attach the evidence, date every fact that can go
stale, separate what was verified from what was inferred, and end with
decisions for the owner instead of actions already taken. Writing those rules
down once means every future report — from any model, on any surface — comes
out in the shape you trust, instead of depending on which model wrote it and
what it happened to imitate. This matters most after Fable leaves: the format
IS the rigor, and cheaper models follow written formats far better than they
reinvent them.

**Contents:** the report contract above + the claim-check rules, as a
user-invoked command (`/after-report`) — zero always-on cost, zero trigger
risk (the DEAD-1 lesson applied: don't bet on auto-triggering for process
skills; you invoke it when you want it).

## 4. Fable-transition audit + model-capability register

**Tier: HIGH, time-sensitive. The library's own contract says this moment
re-opens its decisions.**

**The evidence.** live-state-truth was retired because measurement showed the
base models already did its job uncued — and the contract marked the decision
reversible with a condition: "base-model behavior is a volatile fact; a future
model class that stops checking live state re-opens this decision." Your
stated situation — "while I still have access to Fable" — is precisely a
pending model-class change. Every calibration in this library (what earns
always-on, what the base model does natively, the ~80% trigger ceilings) was
measured on the current model mix and silently assumes it.

**Beginner's why.** Your skills exist to carry a smarter model's discipline
onto the models you'll actually be running. But nobody has written down which
disciplines the everyday models already have on their own versus which ones
only work because the skill supplies them — and that boundary moves every
time models change. This is a dated checklist: what was measured, on which
model, when to re-measure. When Fable leaves, you run the checklist on
Opus/Sonnet and learn in an afternoon which skills earn their keep, which
retired skills need reinstating, and which gaps just opened — instead of
discovering it slowly through degraded work.

**Contents:** mostly reuses what you already built — the discriminating tests
from `results/2026-07-11/` re-run on the post-Fable mix, plus a small dated
register (skill → behavior → last measured on → verdict). Honest placement:
likely a campaign phase + register artifact in this repo, not a new installed
skill at all; a thin support skill only if the register needs a keeper.

## 5. `application-tailor` — the process half of the career lane

**Tier: MEDIUM. The lane is daily; only its *style* half is governed.**

**The evidence.** The 2026-07-13 report records career work as daily.
brand-standard governs how anything in David's name sounds and looks — but
nothing governs the *process*: reading a job description, mapping it against
real experience, and producing the tailored artifact. The same report already
tiered the external option (`career-ops`, MIT: "exceptional… ghost-job
scoring, anti-fabrication fences") and flagged its cost: it "ships its own
voice/typography that conflicts with brand-standard."

**Beginner's why.** Tailoring a resume or cover letter to a posting is a
repeatable procedure with real failure modes — the worst being the model
inventing experience you don't have to match the posting. A thin house skill
would fix the procedure: extract what the posting actually asks for, map each
requirement only to evidenced experience (a hard never-fabricate rule), flag
gaps honestly instead of papering over them, then hand the writing to
brand-standard and the formatting to the document skills you already
installed. Small skill, big lane, and it composes with what exists instead of
competing with it — stealing career-ops' two best fences (anti-fabrication,
ghost-job signals) as ideas, not as vendored text.

## 6. `correspondence` — Gmail drafting in David's voice

**Tier: LOWER — real signal, thinner evidence. Listed for completeness.**

Gmail/Drive connectors are attached to this account and brand-standard's
voice section was distilled from real correspondence — but the repo records
no recurring email-drafting failure the way it records delegation and
reporting patterns. If email drafting through Claude is in fact frequent, a
thin skill (triage → draft in-voice → always create a draft, never send
unreviewed) earns a look; if not, brand-standard alone may already cover the
need. Owner knows the frequency; the record doesn't.

---

## What NOT to author (the retirement standard, applied forward)

- Anything the base models do uncued — generic "think carefully/check your
  work" skills fail the standard that retired live-state-truth.
- A second planning, verification, or scoping skill — the governors own those;
  improvements go through research-methodology as edits, not siblings
  (Decision 1).
- The already-tiered external backlog — fold candidates 1–4 from 2026-07-13
  (writing-skills→skill-authoring, avoid-ai-writing→brand-standard,
  systematic-debugging's 3-strike counter, fable-method's forced-artifact
  lesson) remain pending owner action and are not re-proposed here; they're
  prior decisions awaiting execution, not new proposals.

## Decision sheet (owner calls)

| # | Proposal | Cost to build | Ongoing cost | When it pays off |
|---|---|---|---|---|
| 1 | delegation-discipline | one authoring session + eval set | zero until invoked | every multi-agent session |
| 2 | hook-enforcement pack | 2–3 small scripts + A/B runs | near-zero (runs locally) | the ceiling cases wording can't reach |
| 3 | after-report command | one authoring session | zero until invoked | every future report |
| 4 | Fable-transition audit | mostly reuse of 2026-07-11 tests | one afternoon per model change | the day Fable leaves |
| 5 | application-tailor | thin skill; steals two fences | zero until invoked | every application |
| 6 | correspondence | thin skill | zero until invoked | only if email volume is real |

Recommended order if all approved: 4 first (time-boxed by Fable access), then
2 (your named next lever), then 1 and 3 (authored while Fable can write them —
the library's founding premise), then 5, then 6. Every one gates through
skill-authoring's checklist and research-methodology before anything is
declared adopted; nothing installs always-on without passing Decision 5's
cost math.

## Provenance

Authored 2026-08-03 by the session that produced `../sol-skill-analysis/`.
Evidence cited inline; primary sources: `.claude/LESSONS.md` (DEAD-1, DEAD-2,
INC-1), `results/2026-07-13/external-skill-analysis/REPORT.md` (work mix,
career-ops tier, fold backlog, licenses), `results/2026-07-11/` (discriminating
tests), `architecture-contract` (weak-point 3, Decision 7 reversibility),
today's verified workflow JSONs. No skill, hook, or config was created by this
report — proposals only.
