---
name: brand-standard
description: >-
  David Layson's personal brand standard — voice and tone distilled from his
  real correspondence and resumes, plus the official typography (Eurostile
  display, Poppins body) and color system (Space Blue, Muted Space Blue,
  black + greys) with exact CMYK/RGB/HEX/Pantone/Sherwin-Williams values. Load
  BEFORE drafting or formatting ANY external-facing artifact in David's name:
  resumes, cover letters, emails he will send, proposals, one-pagers, decks,
  personal-site copy, or styled PDFs/documents. Trigger phrasings: "format my
  resume", "draft an email/letter for me", "match my brand", "my colors/fonts",
  "external facing document", "make it look like mine". Do NOT load for
  internal repo docs, READMEs, commit messages, or code comments (the repo's
  house style wins), nor for text written in another party's voice (quoting a
  counterparty, filling their form), nor for clinical or client-owned
  documents about a third party (not David's brand); for how to author skills,
  see skill-authoring.
---

# Brand Standard

The single source of truth for how anything published in David Layson's name
sounds and looks. Two halves: **voice** (derived from evidence — his sent
email, his resumes, his working style) and **identity** (supplied verbatim by
David — typefaces and colors). When a future session produces an external-facing
document, it conforms to this file or names the deviation and why.

## Part 1 — Voice and tone

Two registers. Pick one deliberately; do not blend them.

### Register A: Correspondence (email, letters, messages he will send)

1. **Greet by name, warmly.** "Hi Joanne," / "Good evening All," / "Good
   afternoon!" — never a bare cold open.
2. **Gratitude before business.** The first sentence thanks or acknowledges the
   person before any ask. Observed: "Thank you for continuing to be a great
   candidate partner for me throughout this process!"
3. **Candor early, stated plainly.** Awkward facts go up front, not buried:
   "I wanted to be upfront and let you know that I have received an offer
   letter from another company."
4. **One clear ask per message**, usually closing the note: "Please let me know
   if this works, and if there is anything additional you need from me."
5. **Short paragraphs** — one to three sentences. Whole emails typically run
   under ~120 words.
6. **Enthusiasm is plain-spoken and genuine**: "I couldn't be more excited."
   Allowed and characteristic. Hype vocabulary is not (see hard rules).
7. **Warm close**: "Thank you," / "Thank you!" then "David" ("David Layson" on
   first contact). A light emoji (😊, :)) is fine in familiar threads only —
   never in formal documents.
8. **Follow-ups are brief and guilt-free**: "Following up to see the status of
   the transfer, and if there is anything additional you need from me. Thank you!"

### Register B: Formal documents (resume, proposal, one-pager, deck copy)

1. **Every claim quantified or cut.** Observed baseline: 98% on-time delivery,
   25% throughput gain, 12,000-case backlog eliminated, $65M→$180M revenue
   scale, 700+ purchase journeys, ~40 mentees. A bullet without a number must
   earn its place with a concrete noun.
2. **Action-verb bullets, no first person.** Led, built, designed, resolved,
   coordinated, eliminated.
3. **Honest approximation.** When a figure is inexact, David writes "around 40
   new hires" — keep the qualifier; never round up into a false precision.
4. **Systems vocabulary is native**: operational infrastructure, cross-functional
   execution, lifecycle, knowledge systems. Name real tools (Salesforce, Oracle
   Cloud Transportation Management), not categories.
5. **Identity themes to preserve** across any rewrite: systems thinking +
   operational discipline + customer-focused execution; builder of knowledge
   systems; mentor and team enabler.

### Hard rules (both registers)

- Numbers replace adjectives wherever a number exists.
- Banned vocabulary: world-class, best-in-class, cutting-edge*, synergy,
  passionate, results-driven, dynamic, guru. (*As a descriptor — his employer's
  proper name "Cutting Edge Communications" is obviously exempt.)
- Warmth is specific: thank named people for named things, never "thanks for
  everything."
- Claims track evidence. If the source material doesn't support it, it doesn't
  ship — same law as the governors.

## Part 2 — Typography

| Role | Typeface | Use for |
|---|---|---|
| Display | **Eurostile** | Headlines, section titles, key callouts, big stats — moments where the brand should make a bold, technical statement. Its geometric forms and engineering roots evoke precision and confidence. |
| Body | **Poppins** | Body copy, subheads, captions, navigation, longer passages. Clean, contemporary, readable in print and digital; a modern contrast to Eurostile. |

Pairing rules: never set long passages in Eurostile; never use Poppins for a
hero headline when Eurostile is available. Name fonts explicitly in every
deliverable and always attach fallbacks:

- Display stack: `Eurostile, "Eurostile Next", "Square 721", "Bank Gothic", "Arial Narrow", sans-serif`
- Body stack: `Poppins, "Century Gothic", Futura, Avenir, Helvetica, sans-serif`

Licensing: Poppins is free (Google Fonts, SIL OFL). Eurostile is commercial
(Monotype/Linotype); Square 721 is the common licensed clone.

**Volatile fact (verified 2026-07-12):** neither Eurostile nor Poppins is
installed on David's Mac. Documents will render in fallbacks locally until he
installs them — say so in the delivery note whenever it applies, and re-check
before assuming.

## Part 3 — Color

Brand-supplied values (verbatim from David, 2026-07-12):

| Name | HEX | RGB | CMYK | Pantone | Sherwin-Williams |
|---|---|---|---|---|---|
| **Space Blue** | `#0F436E` | 15, 67, 110 | 100 / 78 / 32 / 18 | 302 C | SW 6244 Naval — "a classic, deep nautical navy that anchors a space" |
| **Muted Space Blue** | `#9EB3C5` | 158, 179, 197 | 38 / 21 / 14 / 0 | 2121 C | SW 9143 Cadet — "a sophisticated, muted gray-blue; sleek, modern, calming" |
| Black + greys | — | — | — | — | Neutral foundation |

Derived grey ramp (Claude's defaults for consistency, not brand-supplied —
adjust freely if David specifies his own): near-black body text `#1A1A1A`,
secondary text `#4A4A4A`, captions/metadata `#767676`, hairlines `#D9D9D9`.

Usage rules:

- **Space Blue anchors.** Masthead/name, section headings, key stats. Contrast
  on white ≈ 10.7:1 — safe for text at any size.
- **Muted Space Blue is decorative.** Rules, dividers, table accents, background
  tints. Contrast on white ≈ 2.1:1 — **never body or heading text on white.**
  Dark text on a Muted Space Blue background is fine.
- Body text is near-black/grey, never blue, for anything longer than a callout.
- Print deliverables carry the CMYK/Pantone values; screen uses HEX.

## Part 4 — Applying it (procedure)

1. Load this skill before drafting; pick Register A or B and say which.
2. Style documents per Part 2/3: Eurostile + Space Blue for structure, Poppins
   + greys for content, Muted Space Blue for rules and accents only.
3. State in the delivery note if the render environment lacked the brand fonts
   (see the volatile fact).
4. Reformatting and rewriting are separate scopes: a "reformat" keeps content
   verbatim; flag stale or wrong content instead of silently editing it
   (scope-fence law).
5. Never apply David's brand to a third party's document (their form, their
   template, their letterhead).

## When NOT to use

- Internal repo documentation, commit messages, code comments — the repo's own
  house style governs (see architecture-contract).
- Text in another party's voice, or neutral/joint documents (contracts, shared
  vendor forms).
- Choosing what to SAY in a high-stakes negotiation — this file governs sound
  and look, not strategy.

## Provenance and maintenance

Typefaces and color values supplied verbatim by David, 2026-07-12. Voice
derived 2026-07-12 from: sent Gmail, June–July 2026 (~15 threads: recruiter
correspondence incl. Autodesk, new-employer onboarding, wedding-vendor
coordination); `DLayson_MasterResume_3.12.26` and `DLayson_AndurilPOA_Resume`
(Google Drive); and working-session history in this library's repos.

Description NOT-clause sharpened 2026-07-21 — third-party clinical/client-owned
documents named as a non-trigger, per the perspective-taking deck AAR
(`results/2026-07-21/AAR-perspective-taking-deck.md` §3: the skill loaded, then
correctly self-limited to *does not apply*; the boundary now lives in the
trigger). Adopted owner candidate, pre-registered in
`experiments/hypothesis-2026-07-21-brand-standard-third-party.md`.

Re-verify on use: (a) fonts installed yet? (b) resume employment currency —
as of June 2026 David is at Cutting Edge Communications, no longer Rivian;
resumes on file predate this. First demonstration artifacts: branded rebuilds
of both resumes, delivered 2026-07-12.
