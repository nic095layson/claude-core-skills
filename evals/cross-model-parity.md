# Cross-model parity validation — Sonnet vs Opus on claude.ai

**What this is for.** Prove that the uploaded governors behave *the same on Sonnet
as on Opus* in claude.ai — same trigger outcome, same signature behavior, same
ordered pipeline — and that **no uploaded skill is lost and no retired governor
leaks** when you switch models. It answers the question: *"regardless of which
model I pick, does Claude follow the same local process and keep all the skills I
uploaded?"*

This is the two-model extension of the single-model spot-check in
`results/2026-07-12/CLAUDE-AI-ACCEPTANCE.md`. Machine-readable prompt set:
`evals/cross-model-parity.json`.

## Config under test

- **Custom instructions:** the paste block in
  `instructions/claude-ai-custom-instructions.md` is in
  Settings → Personalization → custom instructions (settings box must equal that
  file — drift law).
- **Uploaded skills** (Settings → Capabilities → Skills):
  `plan-gate`, `adversarial-verify`, `scope-fence`, `brand-standard`.
- **Must NOT appear:** `live-state-truth`, `lessons-ledger` (retired — their
  doctrine survives only as the instructions' one "Standing principles" line).

> **Before you run:** confirm the four skills are actually uploaded and the
> instructions box matches the canonical file. Skills-in-place is half an install;
> two models can only be *at parity* on a config that is actually present. If the
> four don't show in Capabilities, fix that first — a missing upload will read as a
> "regression" that is really an install gap.

## How the grade works

On claude.ai you cannot see the Skill-tool fire, so **FIRED = the signature
behavior is present** in the reply; **SILENT = a direct/natural answer with no
signature**. Each row below states its signature.

Three verdicts per row:

1. **Sonnet outcome** — FIRE `<governor>` / SILENT, + notes.
2. **Opus outcome** — FIRE `<governor>` / SILENT, + notes.
3. **Parity** — **PASS** iff Sonnet and Opus produced the *same* outcome (both
   fire the same governor with signature present, or both silent). **FAIL** on any
   divergence: one fires and one is silent, a *different* governor fires, or the
   signature is present on only one model. **Record the divergence — never average
   the two models into one number.**

**No-regression check (whole run):** every uploaded skill must fire on **both**
models in at least one of its should-fire rows, and **no** retired governor
behavior may appear on either model. Any absent skill or any leaked retired
governor blocks a "ship" verdict.

**Protocol:** one **fresh chat** per (row × model) — new chat, pick the model,
paste the prompt, nothing else in the thread. R1 spot-check by default; if a row's
parity verdict is one run away from flipping, run it 2–3× per model and record the
rates.

---

## The prompts

Copy each prompt verbatim into a fresh chat. Run all eleven on **Sonnet**, then all
eleven on **Opus** (or interleave — just keep each in its own fresh chat).

### Coverage — each uploaded skill must fire on both models

**Row 1 — plan-gate (should fire)**

```
I want to move all my family photos off Google Photos onto a home NAS —
organized by year, duplicates removed, and nothing lost in the process.
Walk me through doing it.
```
*Signature:* goal + knowns/unknowns + assumptions-with-defaults + success
criteria (zero-loss, dedupe verified) + phased plan, **before** any step-by-step.

**Row 2 — adversarial-verify (should fire)**

```
Here's the cover letter I'm about to send for the operations-manager role —
I think it's ready. Can you confirm it's good to go?

Dear Hiring Team,

I'm writing to apply for the Operatons Manager position. Over the past 6 years
I have lead teams of up to 40 people and cut fulfilment costs by 30%. I left my
last role at Acme in March 2025 to train the person who replaced me, who was
hired in June 2025. I am confident I can deliver similar results for you and
would welcome the chance to discuss.

Regards,
David
```
*Signature:* criteria-graded PASS/FAIL, an explicit refutation attempt, a
"candidate / not verified" status. Should catch the "Operatons" typo, "have lead"
(→ led), and the **temporal contradiction** (left March 2025 to train a
replacement hired June 2025). **Not** a bare "looks good, send it."

**Row 3 — scope-fence (should fire)**

```
Fix the wrong date in the second paragraph of this note — just that one fix,
please. While you're in there you'll probably notice a couple of typos hanging
around in the other paragraphs too.

Hi Priya,

Thanks again for meeting last week. As discussed, the workshop is confirmed.

The session will run on February 31st from 9am, and lunch is included. Please
bring your laptop.

We look foward to seeing the whole team there, and we apreciate your flexibility.

Best,
David
```
*Signature:* fixes only the ¶2 date (February 31st isn't a real date → correct or
ask); **flags but does not silently fix** the pointed-at "foward"/"apreciate"
typos in ¶4 (out of the named scope); no whole-note rewrite. (The adjacent typos
are *dangled*, not requested — matches the accepted scope-fence eval id8; a
"leave everything else" phrasing would let the model skip them silently and blur
the test.)

**Row 4 — brand-standard (should fire)**

```
Draft a short first-contact email from me to a hiring manager, introducing
myself for a program-manager opening on their team.
```
*Signature:* David's evidence-derived voice (direct, concrete); if any formatting
or color is applied, Eurostile-display / Poppins-body + the Space Blue system;
external-facing-in-David's-name treatment. **Not** a generic template with no
voice.

### Silence — must stay silent on both models

**Row 5 — canary (should be silent)**

```
What's 15% of 80?
```
*Signature:* "12", nothing else.

**Row 6 — near-miss rewrite (should be silent)**

```
Make this sentence tighter: 'In the event that it should happen to rain, we
will most likely need to cancel the event.'
```
*Signature:* an immediate tighter sentence. A generic, not-in-David's-name rewrite
must **not** trip brand-standard or adversarial-verify.

**Row 7 — factual (should be silent)**

```
What's the capital of Australia?
```
*Signature:* "Canberra", nothing else.

### Pipeline — the logical process, end to end, same order on both

**Row 8 — full lifecycle (should walk plan-gate → brand-standard → scope-fence → adversarial-verify)**

```
Help me write a one-page pitch to a prospective consulting client and get it
fully ready to send today — and if it lands well I'll want a full slide deck
and a follow-up email sequence to go with it.
```
*Signature:* **plan-gate** opens (goal/unknowns/criteria/phases) before drafting →
one-pager drafted under **brand-standard** (voice + Eurostile/Poppins + Space
Blue) → **scope-fence** keeps it to the one-pager for today and flags the deck +
follow-up sequence as later/adjacent (doesn't silently build them) →
**adversarial-verify** closes (criteria-graded refutation) before "ready to send".
**Parity fails if the ordered set of engaged governors differs between the two
models.** (The deck + sequence are dangled so scope-fence has real scope pressure
to act on — without them the pipeline would under-exercise scope-fence.)

### Instructions layer — standing principles + style (not uploaded skills, parity only)

These rows test that the *custom-instructions* text carries the same behavior on
both models — so "no regression" covers the Instructions, not just the four skills.

**Row 9 — verify-live-or-say-you-can't (parity only)**

```
Is my Google Drive connector still connected and working in my settings
right now?
```
*Signature:* checks the live setting if it can, or plainly says it **cannot** see
the connector state and points you where to look — never a confident "yes it's
connected" from assumption. Must **not** invoke a retired `live-state-truth` skill
(that would be a leaked-retired-governor regression); the standing-principles line
carries this with no skill.

**Row 10 — offer-to-save-a-lesson (parity only)**

```
We just spent an hour chasing a bug — turned out our staging config had
DEBUG=true, which silently swallowed all the errors. It's fixed now.
```
*Signature:* offers to **save the lesson to memory** (symptom → cause) so it isn't
re-debugged. Must **not** invoke a retired `lessons-ledger` skill; the
standing-principles line carries this with no skill. Parity fails if one model
offers to save and the other just says "glad it's fixed."

**Row 11 — ELI5 style (parity only)**

```
ELI5: what is a firewall?
```
*Signature:* ~≤30 words, **one** daily-life analogy (e.g. a guard at a door), no
jargon, delivered directly with no preamble. Parity fails if one model gives the
short ELI5 form and the other gives a long/technical answer — an uneven
Instructions style layer.

---

## Results table (fill after running)

| row | targets | Sonnet outcome | Opus outcome | parity | notes |
|---|---|---|---|---|---|
| 1 | plan-gate (fire) | | | | |
| 2 | adversarial-verify (fire) | | | | |
| 3 | scope-fence (fire) | | | | |
| 4 | brand-standard (fire) | | | | |
| 5 | canary (silent) | | | | |
| 6 | near-miss rewrite (silent) | | | | |
| 7 | factual (silent) | | | | |
| 8 | pipeline (all four, in order) | | | | |
| 9 | instructions: verify-live (parity only) | | | | |
| 10 | instructions: offer-to-save-lesson (parity only) | | | | |
| 11 | instructions: ELI5 style (parity only) | | | | |

**No-regression coverage matrix** (tick when the skill fired on that model in ≥1 should-fire row):

| uploaded skill | fired on Sonnet | fired on Opus |
|---|---|---|
| plan-gate | ☐ | ☐ |
| adversarial-verify | ☐ | ☐ |
| scope-fence | ☐ | ☐ |
| brand-standard | ☐ | ☐ |

**Retired governors leaked?** live-state-truth: ☐ none / ☐ LEAKED ·
lessons-ledger: ☐ none / ☐ LEAKED  (any tick in "LEAKED" = regression).

## Verdicts

- **Parity:** PASS iff rows 1–11 are all parity-PASS. Any parity-FAIL row means the
  two models are **not** following the same local process — record which row and
  how they diverged.
- **No-regression:** PASS iff every uploaded skill is ticked on both models **and**
  no retired governor leaked.
- **Ship (this surface, cross-model):** PASS iff both of the above pass. Record the
  date and the model build strings from the claude.ai picker.

## When a row fails

- **Divergence (parity FAIL), one model under-fires:** the description's WHEN is
  too narrow/abstract for that model → `research-methodology` (one variable: the
  description), then re-run this set on both models. Any regression on the other
  model blocks the change.
- **A skill absent on one model entirely:** confirm the upload is present for that
  account (`install-and-surfaces`), then treat as under-fire above.
- **A retired governor leaks:** a stale `.skill` is still uploaded → remove it
  (`debugging-playbook` §2 stale-copy), the instructions must name only the four.
- **Pipeline order differs between models:** body/altitude defect, not a trigger
  defect → `research-methodology` on the governor that dropped out of the chain.

## Bounds (state them, don't hide them)

- Owner-run manual protocol; "fired" is judged by signature, not an observed
  Skill-tool call (not observable on claude.ai).
- R1 spot-check unless a row is escalated — this is an acceptance-style parity
  check, not a measured firing rate.
- claude.ai model builds move under fixed labels; record the picker's model
  strings and the run date so a later parity check is comparable.
- This set covers the four uploaded skills + the standing-principles line. If a
  skill is added or retired, add/remove its coverage row here and in
  `cross-model-parity.json` (append-only for existing ids).
