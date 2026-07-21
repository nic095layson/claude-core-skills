# After-Action Report — Perspective-Taking Stimulus Deck

**Session:** build an ABA perspective-taking stimulus deck from an uploaded clinical protocol, then compress it to 10 slides for Google Slides.
**Governance in force:** GAUNTLET always-on. plan-gate, adversarial-verify, scope-fence, brand-standard.
**Audience for this report:** Claude Code, for edits to the skills repo and to tooling.

---

## 1. What shipped

| Artifact | Size | State |
|---|---|---|
| `Perspective_Taking_Stimulus_Set.pptx` | 5.6 MB | 95 slides, validates clean |
| `perspective_taking_stimuli_PNG.zip` | 2.8 MB | 80 original stimulus illustrations |
| `Perspective_Taking_Reference_10.pptx` | 579 KB | 10 slides, validates clean |

Generator source: 1,296 lines across 7 files (illustration engine, scene composer, geometric verifier, two deck builders).

**One criterion failed:** the user asked for Google Slides. I delivered .pptx plus import instructions. Root cause in §2.3.

---

## 2. Churn ledger — ranked by cost

### 2.1 The pixel-forensics spiral — largest single waste

**What happened.** After rendering 80 illustrations I needed to verify no figure was clipped, occluded, or missing. I wrote **five successive pixel-analysis detectors**, each of which produced results I then had to debug:

| Attempt | Method | Outcome |
|---|---|---|
| 1 | Border darkness > 2% | Caught 1 real clip, missed 4 others |
| 2 | Skin/outline colors in a 14px ring, threshold 30 | **17 false positives** |
| 3 | Same, threshold 14 | Clean — 2 real defects found |
| 4 | Skin-blob area > 5000 = one head | **All 10 scenarios "failed"** |
| 5 | Skin-blob area > 1600 | 8/10 "failed" |
| 6 | Area + bounding-box fill ratio > 0.45 | **10/10 "failed"** |
| 7 | **Instrument the generator to emit bounding boxes** | Worked immediately; found 5 real defects |

Root causes of the false signals, each different:
- Attempt 2: the "home" floor color `#C08F5C` sits **Manhattan distance 28** from skin tone `#CE9366`. Threshold was 30. The floor registered as skin.
- Attempts 4–5: I was measuring *exposed skin*, not heads. Hair styles cover wildly different fractions of a face — one figure's visible face measured 2,472 px, another's 8,099 px. Any single area threshold is wrong for some hairstyle.
- Attempt 5 also: the adult figure renders at 1.2× scale, so its **arms** exceeded the head threshold.
- Attempt 6: heavy hair splits a face into non-compact fragments, so a compactness filter rejects real faces.
- Attempt 7 still needed one fix — it flagged the bed, swing, and door as "covering a face" because it had no z-order awareness. Those props are drawn *behind* the figure.

**Cost.** Roughly 8–10 tool calls and the largest reasoning block of the session, producing zero verified information until attempt 7.

**The generalizable failure.** *I was inferring, from rendered pixels, facts that the generator already knew exactly.* I wrote the code that placed every figure. The composer could simply report where it put them. Instead I tried to reverse-engineer that from the output image, and every heuristic I built was a lossy proxy for information I had upstream in exact form.

**Secondary failure — measurement-instrument validity.** After attempt 4 reported 10/10 scenarios broken, my prior should have flipped hard toward "my detector is wrong," not "my art is broken." A detector that says *everything* is broken is almost always the thing that's broken. I went two more rounds before switching.

> **Proposed skill change — highest value item in this report.**
> Add to `adversarial-verify` §2 (Behavioral check) or as a short standalone rule:
>
> *Verify at the source of truth, not downstream of it.* When you built the thing being checked, instrument the builder — have it report what it did — rather than inferring what it did from its output. Reverse-engineering your own output is a lossy proxy for information you already hold exactly.
>
> And a companion rule for detector sanity:
>
> *When a check fails broadly — most or all cases — suspect the check before the artifact. Validate the instrument on a case you already know the answer to before acting on its verdict.* Two consecutive rewrites of a detector that still disagrees with the artifact means stop and change measurement strategy, not thresholds.

---

### 2.2 Reading photographed documents — I destroyed the evidence first

**What happened.** The protocol arrived as two HEIC photos of a monitor (3024×4032). My first move was `im.thumbnail((1500,1500))` and then `view`. At that reduction the document text was not reliably legible. I began tiling at native resolution — and mid-turn the user manually uploaded clean JPEGs, which is what actually unblocked the task.

**Root cause.** Downscale-then-read is backwards for text-bearing images. Nothing forced the reduction; I did it reflexively to "make it viewable."

**Cost.** ~3 tool calls, plus the user had to intervene.

> **Proposed change.** In `file-reading` (or a new short skill for image-borne documents):
> *For any image that carries text — a photo of a screen, a scan, a whiteboard — crop and view at native resolution in tiles. Never downscale a text image before reading it. If the source is a photo of a screen, ask for the underlying export first; it is one message and always cheaper than OCR-by-eye.*

---

### 2.3 No Google Slides write path — hard blocker, tooling not skill

**What happened.** User asked for Google Slides. The available Drive connector exposes `create_file`, which accepts content only as **inlined `base64Content` or `textContent`**. There is no file-path parameter. The 10-slide deck is 579,273 bytes → **772,364 base64 characters** to inline. Not emittable.

There is no Google Slides API tool available — only Drive.

**Honesty flag on this finding.** This conclusion is **derived from the tool schema, not observed**. I did not empirically attempt the upload, because attempting it requires emitting the payload that makes it impossible. I also declined to probe the connector with a throwaway file, since that would litter the user's Drive. So: *schema-derived, unverified behaviorally.* Under the standing "verify or say you can't" principle, this is a "say you can't."

> **Proposed tooling asks, in priority order:**
> 1. A Drive/Slides upload that takes a **container file path** rather than inlined base64. This single change makes every binary deliverable (pptx, xlsx, docx, pdf, images) deliverable directly into Drive. Right now the connector can only create files small enough to type out.
> 2. A native Google Slides tool (create/append slides), so decks can be built where the user will edit them rather than converted.
> 3. Failing both: have the environment surface this limit **up front**, so the plan-gate branch rule fires before the deck is built rather than after.

---

### 2.4 Visual QA I could not actually perform

**What happened.** The `pptx` skill mandates visual QA — render slides to images and inspect every one. I rendered contact sheets and full-size slides and called `view` on them. I could not resolve fine visual detail from the returned images reliably enough to make confident judgments about, for example, whether a drawn face reads as "frustrated" versus "angry."

I reported this honestly in both deliveries and labeled expression legibility as **unverified/candidate**. But I still spent tool calls generating contact sheets whose only purpose was a check I could not complete.

**What I substituted, and it worked:** exact geometric verification (bounds, z-order-aware occlusion, face-overlap), mechanical content checks (string-match every model answer against the built file), and layout math computed from the generator's own coordinates. Those caught every defect that was actually caught.

**What remains genuinely unverified:** whether the illustrated faces communicate the intended emotion to a human. That is the single most clinically important property of the deliverable and no mechanical check can substitute for it.

> **Proposed change.** The `pptx` skill's Visual QA section says *"a subagent works well for this if you have one."* In chat there is no subagent. Suggest the skill state the fallback explicitly:
> *If you cannot perform reliable visual inspection, say so in the delivery, name precisely which properties remain unverified, and substitute exhaustive geometric and content checks. Do not generate inspection artifacts you cannot inspect.*

---

### 2.5 Compaction versus the load-the-skill law

Two friction points, both from the interaction between the **"the load is the procedure (law)"** rule and long sessions:

1. **Compaction wiped plan-gate's text mid-task.** When the second request arrived I re-loaded it. Correct, but the law creates a real, repeating token cost on any long task, proportional to skill length.
2. **I re-loaded `adversarial-verify` when its full text was already in context** from four turns earlier — about 5K tokens of pure ceremony. The law as written cannot distinguish *"in context verbatim"* from *"from memory."* I chose redundancy over any appearance of non-compliance.

> **Proposed wording change to the preferences block:**
> *The load is the procedure. A skill counts as loaded if its text was read in the current context window and has not been compacted away; if you cannot see its text, load it again. Never apply a skill from recollection.*
>
> This preserves the law's purpose — no application from memory — without charging for re-reads of a file already open. Secondary suggestion: keep governance skills short, since every one is a tax on long sessions. `adversarial-verify` at ~157 lines is near the practical ceiling.

---

### 2.6 Minor friction — low value, listed for completeness

- **HEIC toolchain.** ImageMagick failed with `Invalid input: Unspecified: Too many auxiliary image references (2.0)` — an outdated libheif delegate. Fixed by `pip install pillow-heif --break-system-packages`. Worth preinstalling if HEIC uploads are common; iPhone photos are the default input for a lot of real work.
- **No SVG rasterizer in Python.** No `cairosvg`, no `rsvg-convert`, no `inkscape`. Worked around via Node's `sharp`, which handled it fine. Worth a one-line note in any illustration-related skill so the next session doesn't hunt.
- **My own bug.** A helper function `txt(pres, slide, ...)` used its *first* argument as the slide. Caught on first execution. Cost: 1 tool call. No process change warranted — this is what running the code is for.

---

## 3. Where the governance actually paid — do not over-correct

A post-mortem that lists only friction will produce bad edits. Three concrete saves:

1. **`adversarial-verify` caught a clinical scoring defect.** Stimulus 6.5 rendered a *surprised* face while its scoring key read "Scared. Afraid. Nervous." A behavior interventionist would have marked a correct answer wrong, and the error would have propagated into percentage-of-opportunities data. Found only because the refutation pass forced a systematic check of stimulus-versus-answer consistency across all 10 targets rather than trusting the design. **This is the single highest-value output of the entire governance stack this session.**

2. **`scope-fence` produced the two most valuable content flags.** Two of the five scenarios the user requested were already on the client's item list — one mastered, one actively in acquisition. Teaching them again would have inflated mastery data. Also caught a copy-paste error in the source protocol (another client's name appearing in one field). Neither was asked for; both were flagged and not silently fixed.

3. **`plan-gate`'s "convert cheap unknowns into facts first"** drove converting and reading the protocol *before* planning around it. The protocol's three-phase structure completely determined the deck architecture. Planning first would have produced a wrong design confidently.

**Also worth noting:** `brand-standard` loaded and correctly resolved to *does not apply* — a clinical document about a third party's client is not an artifact in the user's name, and the skill's own rule bars applying his brand to a third party's material. The skill self-limited correctly. Arguably it should not have triggered at all; its description could add "not for clinical or client-owned documents about third parties" to sharpen the boundary.

---

## 4. Consolidated change list

**Skills repo**

| Priority | Target | Change |
|---|---|---|
| **High** | `adversarial-verify` | Add: *verify at the source of truth* — instrument the builder rather than inferring from its output |
| **High** | `adversarial-verify` | Add: *suspect the instrument when a check fails broadly*; validate the detector on a known case; two failed rewrites = change strategy, not thresholds |
| **Medium** | preferences block | Reword the load-law to accept "text present in current context" as loaded |
| **Medium** | `file-reading` | Add: never downscale a text-bearing image before reading; tile at native resolution; ask for the source export |
| **Low** | `pptx` (public) | State the fallback when visual inspection is unavailable |
| **Low** | `brand-standard` | Sharpen the description to exclude third-party clinical/client documents |

**Tooling / environment**

| Priority | Ask |
|---|---|
| **High** | Drive upload that accepts a container file path instead of inlined base64 |
| **Medium** | Native Google Slides tool |
| **Low** | Preinstall `pillow-heif`; note `sharp` as the SVG rasterizer |

---

## 5. What I would do differently

1. **Instrument the generator from the start.** The geometric verifier is 38 lines and found every real defect. It should have been written before the first render, not after five failed detectors.
2. **Ask about the slide count before building 95 slides.** The user's original spec header said "12 slides"; I flagged it as stale and built 80 stimulus slides. That was the right reading of the request, but the later "max 10 slides" suggests one clarifying question would have saved a full build cycle. plan-gate's own rule — *ask when the call is costly or hard to reverse* — arguably applied and I proceeded on a labeled assumption instead.
3. **Establish delivery-format constraints during plan-gate, not at delivery.** "Google Slides" was requested only in the second message, but "what format does this need to end up in, and can I actually produce that?" belongs in the first gate for any deliverable.
4. **Not generate artifacts for a check I cannot run.** The contact sheets cost calls and delivered little.

---

## 6. Open item carried forward

**Unverified:** whether the 80 illustrated faces read as their intended emotions to a human observer. Phase 2 of the clinical protocol depends entirely on this. Recommended: a human spot-check of targets 3, 6 and 9 before the deck is used in a session. This is stated in the delivery and is not a silent gap.
