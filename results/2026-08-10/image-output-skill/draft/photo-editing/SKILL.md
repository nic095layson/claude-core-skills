---
name: photo-editing
description: >-
  Deterministic editing of EXISTING images and photos — crop, resize, rotate,
  straighten, trim padding, convert formats, adjust color/contrast, composite,
  watermark, annotate — under three laws: never overwrite the original,
  measure before you cut (run the bundled inspect script; never guess
  coordinates from looking), and see-edit-verify (view the image before, view
  the result after, iterate until it matches the ask). Use whenever a session
  must modify an image file the user supplies or names — trigger phrasings:
  "crop/resize/rotate this image", "remove the padding", "make it a square
  thumbnail", "convert this PNG to JPG", "fix the colors", "watermark these
  photos", "edit this screenshot". Do NOT use for creating images from
  scratch (generation routes live outside this skill), charts (dataviz),
  UI/page design (frontend-design), brand look decisions (brand-standard), or
  documents that merely embed images (the document skills) — this skill owns
  only edits to pixels that already exist.
---

# Photo Editing

Editing a photo is the one task where a session can silently destroy
something irreplaceable: the original. It is also a task models fumble in a
predictable way — planning crops by eye from a rendered preview, which hides
padding, EXIF rotation, and alpha. This skill fixes both with the discipline
this library already applies to code: originals are immutable inputs,
coordinates are measured facts (never impressions), and an edit is verified
by looking at the actual output, not by trusting the command that produced
it.

## Terms (defined once)

- **Original** — the image file as received. Immutable for the whole task.
- **Measured fact** — a number produced by a tool (the inspect script,
  `identify`, PIL) — dimensions, bounds, orientation. The opposite of a
  coordinate estimated by looking at a preview.
- **The loop** — see → measure → edit → see again. Vision judges *content and
  intent*; tools supply *numbers*; neither substitutes for the other.

## Procedure

1. **See it.** Read the image with vision first: what is in it, what the user
   wants changed, what could be lost (faces at the crop edge, text near
   borders, transparency).
2. **Measure it.** Run the bundled script — every edit decision starts from
   its numbers:

   ```bash
   python3 scripts/inspect_image.py photo.jpg
   ```

   Returns JSON: dimensions, format, mode, alpha, EXIF orientation, content
   bounds in PIL crop-box convention (directly usable by `Image.crop()`).
   If `exif_orientation` is any value but 1/null, apply
   `ImageOps.exif_transpose()` before any geometry math — phone photos lie
   about which way is up.
3. **Bootstrap if bare.** The toolchain is Pillow; where absent,
   `pip install pillow` (measured ~3 s in a bare cloud container,
   2026-08-10). Prefer Pillow scripts over ImageMagick one-liners: the same
   code runs on every surface with Python, and intermediate values are
   printable facts.
4. **Edit a copy.** Compute the operation from measured numbers and write to
   a NEW descriptively named file (`photo-cropped-1200x630.jpg`), converting
   deliberately: alpha needs a chosen background before JPEG; quality set
   explicitly; LANCZOS for resampling. The original is never the output path.
5. **See it again.** Read the output with vision and check it against the
   ask; confirm the numbers (re-run the inspect script) where the ask was
   numeric. Wrong → adjust parameters and re-run from the original — never
   stack lossy edits on lossy edits. Repeat until it matches.
6. **Deliver.** Hand over the new file (original untouched, and say so),
   stating what was done: operations, before → after dimensions, format and
   quality choices.

## Rules, each with its reason

1. **Never overwrite the original.** An edited-over photo cannot be
   recovered by any amount of apology; every other mistake in this skill is
   retryable only while this rule holds.
2. **Never guess coordinates from looking.** Previews hide padding, EXIF
   rotation, scaling, and alpha; a crop planned by eye inherits every one of
   those errors. Numbers come from the inspect script.
3. **Verify by looking at the output**, not at the command that made it — a
   successful exit code proves the tool ran, not that the ellipse is centered
   or the face survived the crop.
4. **Re-edit from the original, not from the output.** Each JPEG save is a
   generation loss; parameter iteration must not compound it.
5. **State honest limits.** Pillow resampling enlarges pixels, it does not
   invent detail — upscaling, background removal, and object removal are ML
   jobs; route them (see When NOT) instead of shipping a blurry LANCZOS
   upscale as "enhanced".

## Proportionality (the anti-ceremony valve)

A format conversion or a stated-size resize is steps 2/4/6 in three commands
— no ceremony beyond the three laws, which are cheap precisely so they are
never skipped. Batch jobs run the full loop on the FIRST image, then apply
the settled parameters to the rest and spot-check a sample of outputs.

## Volatile facts (dated)

- Authored 2026-08-10 as a proposal candidate; UNMEASURED — no trigger or
  behavioral evals have run (eval set beside this draft; moves to
  `evals/photo-editing.json` on adoption). *candidate*
- Toolchain per environment, verified 2026-08-10 in one Claude Code cloud
  container: no ImageMagick, no Pillow preinstalled; `pip install pillow`
  through the session proxy took 2.7 s and edits ran. Enumerate live before
  promising (`python3 -c "import PIL"`, `which magick`). *verified, that
  container only*
- ML routes (upscaling, background removal, generative fill) require either
  local models or external APIs with keys — per-environment capabilities
  that do not travel. *verified doctrine; specific routes unmeasured*

## When NOT to use this skill

- Creating images from scratch → generation routes: programmatic rendering
  (HTML/SVG/canvas → headless-browser screenshot), or an external
  image-model API where this environment carries keys — neither is owned
  here.
- Charts and data graphics → **dataviz**. UI and page design →
  **frontend-design**. How anything in the user's name looks →
  **brand-standard**.
- Reading or extracting from images inside PDFs/documents → the document
  skills.
- Animated output (GIF/video) → ffmpeg-based work, not owned here.
- Delivering the finished file to the user → the finish-line standard
  (product-output draft), which routes back here for the editing itself.

## Provenance and maintenance

Proposed 2026-08-10 by the session of
`results/2026-08-10/image-output-skill/REPORT.md` (owner-clarified request:
image generation, "particularly photo editing"). The three laws are
convergent with the strongest surveyed community skill (`image-edit`,
peterkrueck/Claude-Code-Development-Kit, MIT — "Never guess crop coordinates
from visual inspection", "Always save to a NEW file. Never overwrite the
original", verified by direct fetch 2026-08-10; ideas only, no text
vendored) and restate this library's own laws in pixel form: measure-
instead-of-eyeball (live-state-truth doctrine) and exercise-over-inspect
(adversarial-verify). `scripts/inspect_image.py` was authored fresh and
live-fired on three cases (bounds exact, edge cases graceful) before
proposal. The official Anthropic skills repo contains no photo-editing skill
(all 17 directories enumerated at commit `f17010c9`, 2026-08-10).

Re-verify: script runs — `python3 scripts/inspect_image.py <any image>`;
toolchain per surface — enumerate live; survey claims — re-fetch per the
REPORT's source list. Update when: a surface changes its preinstalled
toolchain, an ML route (upscale/background removal) gets a measured local or
keyed path, or first measured use grades against this skill's eval set.
