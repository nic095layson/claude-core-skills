---
name: correspondence
description: >-
  The rules for email written in David's name — draft in his brand-standard
  voice, ALWAYS create a draft and never send unreviewed, stay quote-accurate
  when referencing a thread, and flag sensitive sends for his explicit call.
  Use when drafting, replying to, or triaging email David will send — trigger
  phrasings: "draft a reply to this email", "answer this thread", "respond to
  [person]", "help me with my inbox", "write an email to X". Do NOT use for
  external documents that are not email (brand-standard directly), for job
  applications (application-tailor), for the morning brief (its own skill), or
  for merely READING/summarizing mail with nothing to be written — no ceremony
  on a summary.
---

# Correspondence

Email is the highest-frequency artifact that leaves in David's name and the
easiest to get irreversibly wrong: a sent email cannot be unsent, and a wrong
tone, a misquoted thread, or a reply-all lands on a real recipient
immediately. This skill fixes the failure modes that matter — sending without
review, drifting out of David's voice, and misrepresenting what a thread
actually said.

**Status note (authored 2026-08-03):** authored ahead of confirmed need while
Fable-authoring was available — the repo records no recurring email lane the
way it records career and report lanes. Owner confirms or retires; see
register row 11.

## The procedure

1. **Read the whole thread before drafting a reply.** Reference only what the
   thread actually says; quote verbatim where a claim is attributed to a
   sender. Misquoting a counterparty in David's voice is the correspondence
   version of fabrication.
2. **Draft in David's voice** — brand-standard's voice/tone section governs;
   match register to the relationship (the thread itself is the evidence for
   formality level). No AI-tell phrasing in anything he will send.
3. **Always a draft, never a send.** Create the draft (or present the text)
   and stop. Sending is David's click, every time — including "just send it"
   follow-ups on *sensitive* sends (see 4), where the correct response is the
   draft plus the one-line flag, and send only on his explicit confirmation
   after the flag.
4. **Flag sensitive sends in one line** before the draft is treated as final:
   money, commitments, legal/HR matters, conflict, anything career-affecting
   (application email → application-tailor + this skill), or a recipient set
   larger than the thread (added CCs, reply-all).
5. **Triage requests** ("help with my inbox") get: what needs David's action,
   what can be drafted now (draft them), what is noise — as a short list, not
   a report.

## Rules, each with its reason

1. **Draft-never-send** — sent email is irreversible; review is the only
   safety that survives a bad draft.
2. **Quote-accurate or silent** — a paraphrase presented as what someone said
   creates commitments nobody made.
3. **Voice is brand-standard's, not the model's** — consistency of voice is
   the point of having a standard.
4. **Sensitive sends get the flag** — the one-line cost is trivial; the
   failure it prevents is not.

## Volatile facts (dated)

- Authored 2026-08-03; UNMEASURED and need-unconfirmed — candidate on both
  axes (`evals/correspondence.json`, register row 11). *candidate*
- Gmail access exists on claude.ai/cloud surfaces via connector as of
  2026-08-03; connectors do not carry to local sessions (INC-1 class —
  verify per session). *verified this session (cloud)*

## When NOT to use this skill

- Non-email external documents → **brand-standard** directly.
- Job-application email content → **application-tailor** (this skill still
  governs the send mechanics).
- The morning brief → its own skill.
- Reading or summarizing mail with nothing to draft → no skill; just answer.
- Verifying a high-stakes draft before David sends → **adversarial-verify**.

## Provenance and maintenance

Authored 2026-08-03 by the Fable 5 session of
`results/2026-08-03/skill-proposals/` (proposal 6, owner-approved with the
thin-evidence caveat recorded there). Grounds: brand-standard's voice was
distilled from real correspondence; Gmail connector present on cloud
surfaces; no recorded email-lane failure history (hence candidate status).
Draft-never-send generalizes the house write-boundary non-negotiable to the
send boundary.

Re-verify: connector present this session — attempt a Gmail tool listing;
need confirmed — owner statement, dated, folded in here. Update when: the
owner confirms/denies the lane (promote or retire), or a send-boundary
incident occurs (ledger first, then fold the lesson in).
