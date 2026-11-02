# Decision cards — default exemption removed, advisory reminder added (2026-11-02)

**Owner's request.** An after-report from the Solo-Leveling-System session ("decision cards not offered")
and the owner's clickable answer: "Reword + advisory hook (Recommended)".

**Headline.** The owner's own rule text exempted "obvious defaults" from cards, and every one of the 5
missed cards in that session had a stated default. All three carriers now say a default goes first on
the card as "(Recommended)". The prompt trigger adds an advisory reminder when the previous reply posed a
"(Recommended)" list without a card. It never blocks.

## Evidence

| check | result |
|---|---|
| The exemption existed in all three carriers | EVIDENCE: claude.ai block line 155, doctrine block line 44, Mac doctrine line 61 (read 2026-11-02 on main `11b23f5`) |
| The report's E5 (no hook enforces cards) | EVIDENCE: no "(Recommended)" match in any non-test hook script on main |
| Fixture D1–D6 | red on main (36/39: D1, D5, D6 fail) → green 39/39 (`fixture-red-on-main.txt`, `fixture-green.txt`) |
| Existing self-tests | classifier 45/45; turn gates F1–F3 unchanged inside the same fixture |
| Replay over this session's 34 owner turns | 0 reminders. Every "(Recommended)" list this session came with a card. That is not proof of recall on real misses: the Solo session's transcript is not available here (did not check) |
| Guard | PASS; claude.ai block 9,096 characters; plugin 0.1.4 |

## Bounds

- **Out of scope by design:** a blocking version (owner chose advisory); the platform's autonomy
  guidance and the tool's own description, which this library cannot edit.
- **In scope, unverified:** whether the next turn actually re-poses the decision as a card after the
  reminder (UNMEASURED: needs a two-turn live run); the reminder misses lists whose text the long-session
  transcript failed to record (INC-2026-10-29-01's second finding).

## Decisions for the owner

1. Merge this PR and the kit/deck syncs.
2. Upload plugin 0.1.4; re-paste the claude.ai block; re-copy the Mac file.
