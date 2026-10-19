---
name: red-team
description: >-
  Attack the MODEL a deliverable rests on, not just the deliverable: when a figure
  comes from a simulation, projection, scoring engine, ranking, forecast, odds, risk
  score or any system with hand-set constants and assumptions, and that figure will
  reach a decision-maker. Load it when you hear "red team this", "stress-test the
  model", "what would break this", "how sure are we of that number", "audit the
  assumptions", "post-mortem of the model / engine", "has the engine changed since",
  and on every engine or constant change in a standing system. It runs the
  known-answer re-implementation, the one-at-a-time assumption sweep with
  structural bands, the decision-robustness check, the engine fingerprint, and a
  numbered standing attack list whose records gate the report. Do NOT use for
  grading one deliverable against its own success criteria (adversarial-verify),
  checking a doc's claim against live state (live-state-truth), the report's
  format (after-report), or planning the work (plan-gate).
---

# Red-Team

The failure this skill exists for, from a recorded incident (kit post-mortem,
2026-10-19): a fantasy-basketball engine passed every audit for three months —
z-scores re-derived to the last digit, two implementations in exact parity, every
line fact-checked against two outlets — and still quoted a title share as
"21.4 ± 0.4" when a single hand-set constant inside the simulator (a shared
games-played shock of 0.06, never fit to anything) moved that figure by +3.4 and
−2.3 points. Every audit had tested **implementation against specification**. A
judgment constant cannot fail a test of itself; two copies of the same model agree
with each other whatever the model is worth; and "we checked" was true of the
arithmetic and false of the assumptions. Adversarial-verify grades the deliverable
against its criteria. This skill attacks the thing the deliverable is computed
*from*, and keeps attacking it as a standing fixture rather than a one-off.

## Terms (defined once)

- **Judgment constant** — a number in the system that someone chose rather than
  measured: a variance scale, a discount tier, a shock, a cap, a weight, a window.
- **Calibration status** — one of five, and every judgment constant carries one:
  `settings` (read from the governing settings page), `structural` (no judgment in
  it: a hash, a reporting band), `measured` (fit to a committed record, cited),
  `declared_band` (hand-set, its sweep band published), `uncalibrated` (hand-set,
  no band yet, carries the decision id where that will be decided).
- **Attack** — one scripted attempt to break the system, with a question it tries
  to answer in the negative, a record it writes, and the engine version it ran on.
- **Attack list** — the numbered, append-only register of every attack the system
  has faced. Rows are retired with a date, never deleted.
- **Assumption sweep** — each `declared_band` constant moved through its plausible
  range one at a time, everything else held, the headline figure re-run.
- **Structural band** — the range the headline moves across a constant's sweep.
  It is a second error bar, beside the sampling error, and usually the larger one.
- **Tier** — ROBUST / SENSITIVE / FRAGILE by the band's size against a
  pre-committed threshold (the kit uses 1 and 2 points of title share).
- **Engine fingerprint** — the commit (or version hash) of the system, written
  into every record; a record whose fingerprint differs from the live engine is
  STALE and fails the gate.
- **Separate attacker** — the known-answer re-implementation is written from the
  specification by someone, or some context, that has not read the code.

## Procedure

1. **Inventory the judgment calls.** List every constant, threshold, window and
   tier the system runs on, with its live value, its role, and its calibration
   status, in one registry file. A checker compares the registry to the live
   system: unregistered live constant, registered-but-gone, or value drift all
   fail. Reading the live code, not the docs, is how the list is made.
2. **Known-answer re-implementation.** Rebuild the core computation from the
   specification alone (a separate attacker: a subagent or fresh session given the
   spec, not the source) and compare to the engine on real inputs. Exact agreement
   is the only PASS; a near-miss is a finding.
3. **Consistency between instruments.** Where two instruments measure the same
   thing (a card's expected wins vs a simulator's realized rates; a projection vs
   a backtest), compare them and record the gap per category, not just the rank
   correlation.
4. **Assumption sweep.** For every `declared_band` constant, run its band one at
   a time on the real inputs with the baseline asserted within sampling error of
   the published reference first. Two seeds minimum. Tier each constant by its
   worst variant. Patch inside an isolated process and reload the module per job;
   a patch that leaks between jobs produced seed gaps of 3–4 points before the
   reload was added (2026-10-19).
5. **Decision robustness.** Re-run the headline recommendations (the swap, the
   pick, the buy) under every sweep variant; a verdict that flips sign under a
   plausible constant is reported as conditional, never as a verdict.
6. **Fingerprint every record.** Write the engine commit into each JSON the
   attacks produce; the runner fails any record made on a different engine.
7. **Register the attack.** Every script from steps 2–5 is a row on the attack
   list with its question, script, record path and date. The runner writes the
   numbered artifact that the report cites.
8. **Report with two error bars.** Every headline figure carries its sampling
   error and its structural band; every FRAGILE constant's band is quoted by
   name, or the report fails its gate. Uncalibrated constants are named with the
   decision that will calibrate them; the owner decides, the report does not.

## Output format

The attack artifact (numbered, one row per attack):

```
| id  | attack                         | question it tries to break        | record            | status  |
| A-1 | known-answer re-implementation | does the spec reproduce the code? | rt_math.json      | CURRENT |
| A-5 | assumption sweep               | which constants move the headline | sweep.json        | CURRENT |
```

The band sentence, verbatim shape, in any report quoting the headline:

```
<CONSTANT> is FRAGILE: +3.4 (no shock) / -2.3 (shock doubled); headline 21.4 ± 0.5 (MC) within that band.
```

## Rules, each with its reason

1. **A constant is attacked by moving it, never by re-reading it** — a test of a
   judgment constant against itself always passes; only the headline's response
   to the constant says anything.
2. **The attacker has not read the code** — an author re-implementing their own
   code reproduces their own misreading of the spec, and the parity reads as
   proof.
3. **Two error bars or none** — a sampling error quoted alone says "we ran it many
   times", which the reader hears as "we are sure"; the structural band is what
   they needed.
4. **Fingerprint or STALE** — an attack record without the engine version is a
   claim about an engine nobody can name; the engine changing under a report was
   the second-largest finding of the incident this skill comes from.
5. **The list is append-only** — an attack that was deleted was never run, as far
   as the next reader can tell.
6. **The sweep reruns when the engine or its inputs change, not per question** —
   bands belong to a configuration; a report quotes the last sweep's bands and
   says which configuration they were made on.
7. **Uncalibrated is a status, not a verdict** — a hand-set constant may ship;
   shipping it unnamed, or named without the decision that will calibrate it, is
   the defect.

## Proportionality (the anti-ceremony valve)

- A question answered from a figure the system already published: quote the last
  sweep's band beside it, nothing more.
- A new report with a headline figure: steps 7–8 (registry check, attack runner,
  band quoted) — minutes, as gates.
- A new model, a changed constant, a changed input set, or a post-mortem: the
  full pass, steps 1–8.
- A system with no judgment constants (a pure lookup, a deterministic transform):
  this skill does not apply; adversarial-verify does.

## Tooling (shipped beside this skill, `scripts/`)

Dependency-free Python, generalized from the reference implementation (named in
each script's docstring as lineage only; nothing in the procedure depends on that
project); `<skill>` is this skill's directory (`.claude/skills/red-team`
in a project that carries it, or `~/.claude/skills/red-team`):

```
python3 <skill>/scripts/redteam_init.py --root .      # scaffold redteam/: registry, attacks, live.py, README, examples
python3 <skill>/scripts/registry_check.py --root . --json redteam/records/constants.json
python3 <skill>/scripts/attacks_check.py  --root . --out  redteam/records/attacks.json
python3 <skill>/scripts/bands_check.py    --report <report> --sweep <sweep record>
```

The scaffold passes all three checks as shipped. `sweep_template.py` is the sweep's
contract (reload the model per job, one constant at a time, baseline within 3 SE of
the reference before any tier is read, two seeds, tiers on the unrounded mean,
fingerprint and tier rule in the record) and runs a toy model end to end with
`--demo`; the real sweep is the project's. Tests: `scripts/test_redteam_scripts.py`.

## Volatile facts (dated)

- Authored 2026-10-19 from one incident and one implementation. **Trigger evals run
  2026-10-19** on Claude Code headless, N=2 per prompt: `claude-fable-5-1` fired
  6/6 on ids 1–3 and 2/2 on id 6, silent 4/4 on ids 4–5; `claude-opus-5-5` the
  same (`results/2026-10-19/red-team-trigger-evals/`). Behavioral value and
  claude.ai triggering UNMEASURED; not in the install footprint until Decision-5
  review. *measured (trigger), candidate (value)*
- The reference implementation: `nic095layson/fantasy-basketball-2026-27`
  `scripts/redteam/` (registry, drift check, sweep, bands check, attack runner,
  29 red-first tests) and `scripts/gates.py --redteam`, after-reports
  `after-report-2026-10-19-draft-postmortem.md` and
  `after-report-2026-10-19-redteam-standing.md`. *verified 2026-10-19 (the
  sweep ran: 6,000 seasons × 2 seeds, one FRAGILE, two SENSITIVE, three ROBUST)*
- Tier thresholds 1 / 2 points and the 3-SE baseline assertion are that project's
  conventions, not fitted values. *assumption*

## When NOT to use this skill

- Grading a finished deliverable against its pre-committed criteria →
  **adversarial-verify** (this skill feeds it the structural band; it does not
  replace the pass).
- A documented claim about a live system → **live-state-truth**.
- The shape of the report that carries the findings → **after-report**.
- Planning the attack campaign itself → **plan-gate** (the sweep's parameters are
  register rows there, stated before the run).
- Recording what the attack cost or what dead-ended → **lessons-ledger**.

## Provenance and maintenance

Authored 2026-10-19 by the Fable 5.1 session of the fantasy-basketball kit, on
the owner's request ("Is there a way to implement a 'red team' type check, audit
and validation with every task where applicable? I'd like this in fantasy
basketball and my Claude operations as a whole") after the draft post-mortem of
the same day. Lineage: adversarial-verify's refutation attempt (§3) and rules
8–9 (verify at the source of truth; a broadly-failing check indicts the checker),
generalized from one deliverable to the system beneath it; the red-first and
gates-or-no-merge laws of that project's `RULES.md` (rules 5 and 7).

Re-verify: the reference implementation exists —
`ls scripts/redteam/` in the kit (expect `constants_registry.json`,
`check_constants.py`, `sweep.py`, `check_bands.py`, `attacks.json`,
`run_attacks.py`); the gates flag —
`python3 scripts/gates.py --help | grep redteam`; the toolkit here —
`python3 .claude/skills/red-team/scripts/test_redteam_scripts.py` (expect every
test ok). Update when: the kit's
registry statuses change shape, a second project adopts the pattern (fold its
instance differences in, dated), or trigger evals run (update the status line).
