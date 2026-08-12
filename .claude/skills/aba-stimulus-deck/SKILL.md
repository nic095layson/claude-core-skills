---
name: aba-stimulus-deck
description: >-
  Clinical build protocol for ABA stimulus decks and trial slides — from a
  client's program protocol to a verified .pptx: photographed-protocol intake,
  trial-count and delivery-format checks BEFORE building, clinical scope flags
  (mastered/in-acquisition overlap, cross-client data), generator-instrumented
  geometric QA, stimulus-vs-scoring-key consistency, and honest labeling of what
  only a human can verify (face-emotion legibility). Load this BEFORE building
  or editing any ABA/behavior-program material. Trigger phrasings: "build a
  stimulus deck", "make
  trial slides for my client's program", "perspective-taking / Theory of Mind
  slides", "here's the protocol (photo)", "targets and scoring key". Do NOT
  load for general presentations or non-clinical decks (pptx owns those),
  documents in David's name (brand-standard), or reading a protocol with
  nothing to build (plain file reading).
---

# ABA Stimulus Deck

The build-and-verify protocol for clinical stimulus materials produced for a
third party's client. It exists because a deck that *looks* right can still
corrupt clinical data: a scoring key that mismatches its stimulus marks correct
answers wrong and poisons percentage-of-opportunities data; re-teaching an
already-mastered item inflates mastery data; a face whose emotion no human has
confirmed cannot carry an emotion-labeling phase. Every rule below traces to a
real failure or save in the founding session (Provenance).

## Terms (defined once)

- **Protocol** — the clinical implementation document (often a BCBA's), whose
  phase structure determines the deck's architecture.
- **Target / stimulus** — one scenario image (or image set) a learner responds to.
- **Trial slide** — one presentation of a target with its prompt.
- **Scoring key** — the accepted answers for a target; feeds
  percentage-of-opportunities data.
- **Item list** — the client's current program items, each *mastered*,
  *in acquisition*, or *not introduced*.

## Procedure

### 0. Intake — get a readable source before anything else

Protocols often arrive as phone photos of a screen (HEIC). **Ask for the
underlying export first** — one message, always cheaper than OCR-by-eye. If you
must read an image of text: crop and view at native resolution in tiles;
**never downscale a text-bearing image before reading it**. Toolchain facts
(verified 2026-07-21 in the founding session's environment): iPhone HEIC needs
`pillow-heif` (ImageMagick's libheif delegate fails with "too many auxiliary
image references"); rasterize SVG via Node `sharp` (no cairosvg/rsvg present).

### 1. Plan gate — three facts before the first render

Settle these in one short block, and ask rather than assume where sources
conflict (a full deck rebuild is the cost of guessing wrong):

1. **Count** — trials/slides per the protocol vs the request header; if they
   disagree, ask (founding session: a stale "12 slides" header vs an 80-stimulus
   build, later compressed to 10 — one question would have saved a build cycle).
2. **Delivery format, checked against real capability** — "Google Slides" has
   no direct write path from claude.ai (2026-07-21, schema-derived: Drive
   `create_file` accepts only inlined base64/text — a 579 KB .pptx ⇒ 772k
   base64 chars, not emittable; no Slides API tool). Plan for .pptx + import
   instructions and **say so before building**, not at delivery.
3. **Protocol structure** — read the full protocol first; its phases determine
   the deck architecture. Planning before reading produces a wrong design
   confidently.

### 2. Clinical scope check — before designing scenarios

- Cross-check every requested scenario against the client's current **item
  list**: flag *mastered* and *in-acquisition* overlaps in one line (re-teaching
  them corrupts mastery data). Flag, never silently drop or substitute.
- Scan the source protocol for **cross-client contamination** (another client's
  name, copy-pasted fields) — flag it; never fix a clinical source silently.
- Client data is confidential: never carry one client's details into another's
  materials or into examples.

### 3. Build — instrument the generator from the first render

If stimuli are generated programmatically, make the composer **emit its own
geometry** (bounding boxes, z-order, scale) alongside every render, and verify
placement from that exact data. Never verify placement by pixel heuristics on
the rendered output — the founding session burned five successive pixel
detectors (false positives from a floor color 28 Manhattan-units from skin
tone; hairstyle-dependent face areas; a scaled adult's arms flagged as heads)
before a 38-line generator-instrumented verifier found every real defect
immediately.

### 4. Verify — mechanical where possible, honest where not

1. **Stimulus-vs-scoring-key consistency, all targets** — the highest-value
   check on record: it caught a *surprised* face keyed "Scared. Afraid.
   Nervous.", which would have marked correct answers wrong in session.
2. **Content checks** — string-match every model answer/label against the built
   file; layout math from the generator's own coordinates.
3. **Geometric checks** — bounds, z-order-aware occlusion, face overlap, from
   the instrumented data (step 3).
4. **What cannot be machine-verified** — whether a drawn face reads as its
   intended emotion to a human. Label it **unverified** and name a human
   spot-check (specific targets) before session use. Do not generate inspection
   artifacts you cannot actually inspect (contact sheets for a check you can't
   resolve waste calls and prove nothing).

### 5. Deliver

```
**Deliverables** — <files, sizes, slide/stimulus counts>
**Verified** — key-consistency: all N targets; content: string-matched; geometry: exact (instrumented)
**Unverified (needs human)** — face-emotion legibility; spot-check targets <x, y, z> before session use
**Flags** — item-list overlaps / source-protocol issues found (or "none")
**Import** — .pptx → Google Slides: File → Import (no direct write path from here)
```

## Rules, each with its reason

1. **Ask for the source export of any photographed document** — reading photos
   is lossy and slow; the export is one message away.
2. **Count, format, and protocol-read before the first render** — each is cheap
   to settle and a full rebuild to get wrong.
3. **Flag clinical anomalies, never fix them** — the protocol is another
   professional's clinical document; silent fixes destroy the audit trail.
4. **Verify from the generator's own data, not its pixels** — you hold the
   facts exactly upstream; every downstream heuristic is a lossy proxy.
5. **Key-consistency is a blocking check** — a wrong key doesn't just look bad,
   it corrupts the client's data collection.
6. **Unverified clinical properties are labeled, never presented as done** —
   the deck's most important property (emotion legibility) is exactly the one
   no machine check can carry.

## Proportionality

A single stimulus swap or wording fix does not re-run the full protocol: verify
that target's scoring key + geometry, restate the unverified-faces label, done.
Questions about ABA concepts with nothing being built need none of this.

## When NOT to use this skill

- General presentations, pitch decks, any non-clinical .pptx → **pptx**.
- Documents in David's name/brand → **brand-standard** (third-party clinical
  material is explicitly outside it).
- Planning/verifying discipline in general → the governors (**plan-gate**,
  **adversarial-verify**, **scope-fence**); this skill is their instance for
  this domain and adds the clinical facts they must not carry.

## Provenance and maintenance

Authored 2026-07-21 from the perspective-taking deck AAR
(`results/2026-07-21/AAR-perspective-taking-deck.md`), owner-directed: intake
(§2.2 downscale incident, §2.6 toolchain), plan gate (§5.2–5.3 count and
format lessons), scope flags (§3.2 item-list and cross-client saves), build
instrumentation (§2.1 five-detector spiral), key-consistency (§3.1 the
surprised/scared save), honest-labeling (§2.4). Paired always-on steering:
`instructions/aba-project-instructions.md`. Volatile facts: the Drive/Slides
write-path limit is **schema-derived** (not behaviorally verified) as of
2026-07-21 — re-check when the claude.ai connector surface changes; toolchain
facts verified only in that session's environment. Trigger reliability
unmeasured — seed cases in `evals/aba-stimulus-deck.json`, zero runs as of
2026-07-21.
