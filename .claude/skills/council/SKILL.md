---
name: council
description: Convene a five-expert internal deliberation (Contrarian, First Principles, Expansionist, Outsider, Executor) that peer-reviews itself, votes, and delivers a condensed verdict with a vote tally. Use this skill whenever the user's message contains the keyword "Council" or "Council verdict" — including phrases like "convene the council," "claude council," "council this," "run the council," "ask the council," "council verdict," or "what does the council think." Do NOT trigger on ordinary questions where the word "council" does not appear.
---

# Claude Council

A structured self-check that pressure-tests a recommendation from five deliberately different angles before answering. A single line of reasoning tends to fall in love with its first idea; the Council exists to catch blind spots, hidden assumptions, and missed options before the user ever sees the answer.

The user sees only a condensed result: the key tensions and the final verdict. The full deliberation stays internal unless they ask for it.

## The five roles

When the Council convenes, genuinely adopt each role in turn. Each must take a real position with real reasons — not a token one-liner. If a role honestly agrees with the emerging consensus, it should explain *why* in its own distinctive terms rather than manufacturing fake disagreement; manufactured conflict makes the synthesis worse, not better.

1. **Contrarian** — Argues against the obvious or emerging answer. What is the strongest honest case that the default recommendation is wrong? What is everyone else assuming that might not hold?
2. **First Principles** — Ignores convention and rebuilds the problem from basic facts and constraints. Is the question itself framed correctly? What does the problem reduce to when you strip away "how it's usually done"?
3. **Expansionist** — Widens the option space. What adjacent options, combinations, timing plays, or bigger moves is everyone missing? Is the user choosing between A and B when C exists?
4. **Outsider** — Brings zero domain baggage. How would a smart newcomer, or someone from a completely unrelated field, see this? Which pieces of insider "common knowledge" collapse under a fresh look?
5. **Executor** — Cares only about what actually happens Monday morning: cost, effort, timeline, dependencies, failure points, and the first concrete step. A brilliant plan that can't be executed loses to a decent plan that can.

## Deliberation procedure

Run three phases. **Phases 1 and 2 are internal** — work through them in your reasoning, not in the visible reply.

**Phase 1 — Independent positions.** Each role states its position and its single strongest argument, formed *before* reading the others (to avoid anchoring on the first voice).

**Phase 2 — Peer review and vote.** Stress-test the positions against each other. Which arguments survive contact? Which collapse? Where do two roles genuinely disagree, and which side has the better evidence or logic? Distill this to 2–4 *real* tensions.

Then take a **vote**: once the leading recommendation is clear, each of the five roles casts one vote — **for** or **against** that recommendation — based on where its argument honestly landed after peer review. Five roles means the tally is always decisive (5–0, 4–1, or 3–2); there are no ties. A close 3–2 is meaningful information: it signals a genuinely contested call, and the verdict should say so. Don't rig the vote to look unanimous — if two roles still dissent after review, they vote against, and the verdict names what would flip them.

**Phase 3 — Condensed verdict (the only visible output).** Use exactly this structure:

```
🏛️ **Council convened** — Verdict: [N]–[N]

**Key tensions**
- [Role] vs [Role]: one line on the genuine disagreement, and which side prevailed and why
- (2–4 bullets total)

**Verdict**
A clear, committed recommendation in a few sentences of prose, including the
first concrete step when relevant. If the vote was 3–2, name the dissent in one
line — what the two holdouts wanted and what would change their vote.
```

## Rules for the verdict

- **Commit.** "It depends" is only acceptable when immediately followed by the specific fork: "if X, do A; if Y, do B."
- Keep the entire visible output under roughly 200 words. The value of the Council is in the deliberation, not the word count.
- Weight the Executor's practicality heavily when the vote is close — the user needs something actionable, not just interesting.
- The vote must be honest. A role votes based on where its argument actually landed, not on social pressure to agree. A unanimous 5–0 should mean the recommendation genuinely survived every angle; a 3–2 should mean it barely did. Never inflate the tally toward consensus.
- If the user's question needs facts you don't have (prices, current events, their constraints), gather them *before* convening — the Council debates judgment, it doesn't guess at facts. Use available tools (web search, etc.) first, then deliberate.

## Edge cases

- **Trivial or purely factual questions** ("council: what's 15% of 80?"): note briefly that no deliberation is needed and simply answer. Don't perform ceremony on questions with no judgment in them.
- **"Show the full deliberation" / "show the council's work":** print each role's Phase 1 position and the Phase 2 peer review in full, then the verdict.
- **Follow-up questions after a verdict:** answer normally; only re-convene if the user invokes the Council again or the follow-up materially changes the decision.
- **The user disputes the verdict:** engage honestly. The Contrarian's losing arguments are often the right starting point — resurface them rather than defending the verdict reflexively.

## The outside read (added in this library, 2026-11-12)

The five roles are one model in one context wearing five hats: they share every fact the context got wrong.
When the owner will act on a verdict (money, a merge, a move that is hard to undo), say so in one line under
the verdict and offer one fresh-context read of it (the **independent-audit** skill's auditor: given the
question, the facts gathered and the verdict, never the deliberation). The Council debates judgment; the
auditor checks the facts the judgment stood on. Not for casual questions: no ceremony there.

## Volatile facts (dated)

- Body above "The outside read" is the owner's account skill, verbatim, as synced 2026-11-12; the
  description is byte-identical to it. *verified (diff)*
- Trigger eval 2026-11-12, fresh headless sessions, Skill tool only, N=2, session model B: see
  `results/2026-11-12/qa-loop/council-trigger/` for the measured rates. Whether a verdict is better than an
  undeliberated answer is UNMEASURED. *measured (trigger), candidate (value)*

## When NOT to use this skill

- The word "council" does not appear in the owner's message → answer normally.
- Checking finished work against its criteria → **adversarial-verify**.
- Attacking the model or constants behind a figure → **red-team**.
- A reader who did not write the work → **independent-audit** (the Council is not one).
- Planning the work → **plan-gate**.

## Provenance and maintenance

Brought into the library 2026-11-12 on the owner's answer to the system-wide QA audit of that day
("P6 + P7 Council and pruning"): until then the skill lived only on the owner's account, with no repository
copy, no eval set and no guard check. Lineage: the `claude-council` doctrine of `nic095layson/claude`, which
adversarial-verify's refutation step also cites. A support skill, not a governor (architecture-contract
Decision 5): it loads on its keyword and is not part of the enforced set.

Re-verify: `diff <(sed -n '1,/^## The outside read/p' .claude/skills/council/SKILL.md | head -n -1) <account copy>`
shows no difference above the added section. Update when: the account copy changes (re-diff first), the
trigger eval is re-run (replace the dated line), or a verdict's value is measured.
