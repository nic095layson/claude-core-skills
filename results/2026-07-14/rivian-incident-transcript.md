# Incident transcript — governors applied "in spirit," never loaded (claude.ai)

**Surface:** claude.ai (owner's account, governors uploaded + custom instructions
active). **Model:** Opus (owner-relayed). **Date of incident:** 2026-07-14
(owner-relayed into a `claude-core-skills` Claude Code session 2026-07-15; this
file is that archive). **Provenance/limitation, stated plainly:** this is the
owner's paste of a claude.ai conversation, transcribed verbatim below — it is
**owner testimony**, not a machine-exported transcript, and on claude.ai a skill
load is **not externally observable** (`results/2026-07-12/CLAUDE-AI-ACCEPTANCE.md`:
firing is "not observable on this surface"). So the central fact — that **zero**
governor skills loaded — is the **model's own self-report**, uncorroborated by a
tool-invocation log. Treat it as such (INC-5: reconcile self-report against
artifacts; here no artifact exists to reconcile against). This is the founding
evidence for `.claude/LESSONS.md` INC-8 and the 2026-07-15 instruction edits.

---

## Prompt 1 (owner → model)

> You are an expert stock analyzer - please analyze Rivian automotive and provide
> your best advice into when the stock will hit a share price of $27.50

## Response 1 (model, verbatim as relayed)

> Acknowledged limitations of stock prediction while preparing balanced analysis
> Acknowledged limitations of stock prediction while preparing balanced analysis
>
> I'll pull current data before giving you anything — a price prediction is only
> as good as where the stock actually sits today.
>
> Weighed predictability limits against analyst consensus data
> Weighed predictability limits against analyst consensus data
>
> Straight answer: no one — myself included — can tell you when RIVN will hit
> $27.50, and anyone who gives you a confident date is guessing. Stock timing
> depends on unknowable future events (earnings surprises, R2 sales, macro moves),
> so a specific price-by-date is not a forecast anyone can make honestly. What I
> can do is show you how far that target is from reality right now.
>
> Here's the picture as of July 14, 2026:
>
> * Current price: ~$16.80. Your $27.50 target is roughly 64% above today's
>   price. Over the past 52 weeks the stock has traded between a high of $22.69
>   and a low of $11.57 — meaning $27.50 is a price RIVN hasn't touched in at
>   least a year, about 21% above its own 52-week high. [Robinhood]
> * No analyst target reaches it. The median price target is $18.00, ranging from
>   $9.00 to $25.00, with a consensus rating of "Hold." Even the single most
>   bullish target on the Street ($25) falls short of $27.50. [Ticker Nerd]
>   [StockAnalysis]
> * Near-term headwinds. RIVN just announced a 75 million share secondary
>   offering, which led to dilution concerns and an 18% stock price drop on July
>   7. Q2 earnings land July 30, which is the next real catalyst either
>   direction. [Gotrade]
>
> What $27.50 actually requires: the bull case is entirely a bet on the R2 SUV
> ramp. This is a stock priced on a binary outcome — R2 works, or it doesn't —
> rather than on a settled earnings trajectory. For a 64% run to $27.50 you'd
> realistically need several consecutive quarters of R2 deliveries beating
> guidance, a path to positive gross margin, and no further dilution. That's a
> plausible multi-quarter-to-multi-year scenario if execution goes well — but
> it's a scenario, not a date. [WEEX]
>
> One honest flag: since Rivian is your employer, you may already have
> concentrated exposure through equity comp, which matters for how much more RIVN
> risk makes sense for you. I'm not a financial advisor, so treat this as context
> for your own decision rather than a recommendation.
>
> Want me to model a few R2-ramp scenarios (bear / base / bull) with the delivery
> and margin assumptions each would need to justify $27.50? That's the closest
> thing to a useful "when" I can build.

## Prompt 2 (owner → model)

> [asked whether it used its instructions and skills]

## Response 2 (model, verbatim as relayed) — the self-audit

> Honest answer: partially. I applied the standing principles and communication
> style, but I did not formally load or run any of the four governance skills.
> Here's the straight accounting:
>
> * Verify-current-state (standing principle) — used. I searched for RIVN's live
>   price and analyst targets instead of relying on training data. This is the one
>   discipline I clearly executed.
> * Communication style — used. Direct answer first, no preamble, concise, plus
>   the not-a-financial-advisor caveat.
> * scope-fence — applied in spirit, not loaded. The one-line flag about your
>   Rivian employer/concentration risk is a scope-fence move (flag the adjacent
>   issue, stay inside what you asked). But I didn't load the skill; I just
>   followed the principle.
> * adversarial-verify — arguably owed, not run. Your rule says to use it before
>   delivering analyses, and that answer was an analysis. I did the spirit of it —
>   I refuted the premise (that a date is knowable) and reported that $27.50
>   exceeds every analyst target and the 52-week high — but I never did a formal
>   grade-and-refute pass or load the skill. This is the real gap.
> * plan-gate — skipped, borderline. I treated the request as research/Q&A rather
>   than a build-or-costly task, so I didn't state goal/assumptions/success
>   criteria up front. Defensible, but you could reasonably say something you'll
>   rely on for a financial view crossed the threshold.
> * brand-standard, council — correctly not used. The answer wasn't
>   external-facing in your name, and you didn't say "council."
>
> So the truthful version: I leaned on the principles but didn't invoke the skill
> machinery, and adversarial-verify is the one I'd say I should have run in form,
> not just in spirit.
>
> Want me to run that adversarial-verify pass on the Rivian answer now — grade it
> against what a good analysis owes you and try to break my own claims?

---

## What this transcript does and does not establish

- **Establishes (as model self-report):** the model followed the *principles*
  (verified live price, refuted the premise, flagged concentration risk) while
  loading **no governor skill**; it itemized the skips per pointer when asked.
- **Does NOT establish:** that the model cited the fallback clause ("If a skill
  fails to load, follow the principle stated here anyway") as its license — it
  named no license; it simply did not attempt a load. Any INC-8/instructions
  claim that the model "used the clause" is an **inference**, not shown here.
- **Does NOT establish (unobservable on this surface):** the literal zero-load
  fact independent of the model's own word. No `Skill`-invocation log exists on
  claude.ai.
- **Note the model's own "employer" framing:** it wrote "since Rivian is your
  employer." The repo's dated record (`brand-standard/SKILL.md`) says David moved
  to Cutting Edge Communications in June 2026, so the employer framing may rest on
  stale employment info — the substance (Rivian holdings/concentration) still
  stands, the "employer" label may not.
