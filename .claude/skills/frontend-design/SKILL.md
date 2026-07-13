---
name: frontend-design
description: >-
  Concrete, checkable rules for building web UIs and HTML artifacts that don't
  look AI-generated: a 4/8px spacing grid, a fixed modular type scale, semantic
  color tokens defined once, WCAG AA contrast minimums with a runnable checker,
  line-length limits, restrained radius/shadow scales, and a list of AI tells
  to avoid. Load BEFORE writing any HTML/CSS for a landing page, dashboard,
  app screen, or styled HTML artifact, and when polishing an existing one.
  Trigger phrasings: "build a landing page", "design a UI", "make this look
  professional", "make it look less AI-generated", "style this
  artifact/dashboard/page". Do NOT use alone for artifacts in David's name —
  brand-standard wins on identity, palette, and typography (this skill keeps
  spacing and layout); existing Office/PDF files go to docx, pptx, xlsx, or
  pdf (a NEW PDF: docx then convert, or HTML here); embedded charts take these
  tokens and contrast checks, but mark/axis design is out of scope; for
  authoring skills, see skill-authoring.
---

# Frontend Design

Default model output has a recognizable visual signature — purple gradients,
uniform rounded cards, arbitrary spacing, emoji headers — and readers discount
content wrapped in it. "Make it clean and modern" is a vibe; this skill
replaces vibes with mechanical checks: fixed spacing and type scales, tokens
defined once, contrast computed (never eyeballed), a tells scan before shipping.

**Terms.** *Token* — a CSS custom property in `:root`, the only place a raw
value may appear. *Measure* — text line length (in `ch`). *Tell* — a visual
pattern strongly correlated with default AI output.

## Procedure

1. **Tokens first.** Paste the block below into `:root` before any component
   CSS. Every spacing, size, weight, color, radius, and shadow in component
   rules references a token — a raw hex or arbitrary `px` there is a defect.
2. **Type.** Only the five sizes and three weights in the block. Body 16px /
   line-height 1.5. Cap prose at `max-width: var(--measure)` (≤70ch — longer
   lines are measurably harder to read).
3. **Layout.** All gaps from the spacing scale. Left-align text; align blocks
   to a consistent grid. Space between sections ≥ 2× the space within them —
   whitespace, not boxes, carries hierarchy.
4. **Color.** Neutrals carry the page; one accent, used sparingly (links,
   primary action, one key stat). Swap the placeholder accent, re-run checker.
5. **Verify contrast.** Run the checker with every foreground/background pair
   actually used. AA minimums: 4.5:1 normal text; 3:1 large text (≥24px, or
   ≥~18.7px bold) and meaningful UI parts (WCAG 2.1 SC 1.4.3 / 1.4.11).
6. **Tells pass.** Scan against the tells list; fix each hit or say why it stays.

## Output format — the token block (template)

```css
:root {
  /* Spacing — 4px base grid. Use ONLY these steps; never 13px/22px/etc. */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px;  --space-8: 32px;  --space-12: 48px; --space-16: 64px;

  /* Type — 1.25 modular scale from 16px. Five sizes, three weights, total:
     captions 12.8, body 16, subheads 20, titles 25, page title 31.25 (px). */
  --text-sm: 0.8rem;    --text-base: 1rem;    --text-lg: 1.25rem;
  --text-xl: 1.563rem;  --text-2xl: 1.953rem;
  --weight-regular: 400; --weight-medium: 500; --weight-bold: 700;
  --leading-body: 1.5;   --leading-tight: 1.2;
  --measure: 70ch;       /* max line length for prose blocks */

  /* Color — semantic tokens. Raw hex lives HERE and nowhere else.
     Ratios computed 2026-07-13 with the checker below (WCAG 2.1 math). */
  --color-bg: #FAFAF9;  --color-surface: #FFFFFF;
  --color-text-primary: #1A1A1A;   /* 16.7:1 on bg */
  --color-text-secondary: #4B4B4B; /* 8.4:1 on bg */
  --color-text-muted: #6E6E6E;     /* 4.9:1 on bg — the AA floor for small text */
  --color-border: #E0DEDA;         /* decorative hairlines only, never text */
  --color-accent: #1A5E52;   /* PLACEHOLDER — swap, re-run checker. 7.3:1 on bg */
  --color-on-accent: #FFFFFF;      /* 7.6:1 on accent */

  /* Radius and shadow — two steps each; restraint reads as intent. */
  --radius-sm: 4px;  --radius-md: 8px;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06); --shadow-md: 0 2px 8px rgb(0 0 0 / 0.10);
}
```

## Contrast checker (copy-paste; Python stdlib, nothing to install)

```bash
python3 - <<'PY'
def lum(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)
def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x+0.05)/(y+0.05)
# EDIT this list: every (foreground, background, minimum) pair your UI uses.
# Minimum: 4.5 for normal text, 3.0 for large text and UI components.
pairs = [("#1A1A1A", "#FAFAF9", 4.5), ("#4B4B4B", "#FAFAF9", 4.5),
         ("#6E6E6E", "#FAFAF9", 4.5), ("#1A5E52", "#FAFAF9", 4.5),
         ("#FFFFFF", "#1A5E52", 4.5)]
fails = 0
for f, b, m in pairs:
    r = ratio(f, b); fails += r < m
    print(f"{f} on {b}: {r:.2f}:1 (need {m}:1) {'ok' if r >= m else 'FAIL'}")
print("RESULT:", "FAIL" if fails else "PASS - all pairs meet WCAG AA")
PY
```

## AI tells — do not ship these

- Gradient-on-everything, especially a purple→pink hero gradient.
- Purple/indigo default palette (`#6366F1`/`#8B5CF6` family) for no reason.
- A uniform grid of identical rounded cards, each icon + title + two lines.
- Emoji as section headers or bullet points.
- Centered everything — headline, paragraphs, and buttons all centered.
- Arbitrary spacing values (13px, 22px, 37px) mixed freely.
- Border + shadow + large radius stacked on every element.
- Type sizes/weights improvised per component instead of taken from a scale.
- Filler superlatives as copy: "Blazingly fast", "Supercharge your workflow".
- Container `border-radius` above 16px "for friendliness".

## Rules

- **Tokens defined once; components reference only tokens** — consistency is
  what reads as designed; scattered raw values drift apart silently.
- **No spacing off the 4/8 grid** — a shared rhythm is invisible when present,
  obvious when absent; arbitrary values are the fastest tell.
- **Compute every contrast ratio you claim** — mid-greys pass or fail AA
  within a few RGB points; eyes cannot resolve that, the checker can.
- **One accent color** — restraint reads as intent; three read as a default theme.
- **Left-align body text; center only short display lines** — long centered
  text rags on both edges and reads worse.

## Edge cases and proportionality

- **Trivial case — step aside.** A plain-markdown answer, a code snippet, a
  debug page, or anything the user calls throwaway gets no token ceremony. Do
  not inflate a ten-line HTML answer into a design system.
- **Existing design system.** A project's own tokens/components win; this
  skill fills gaps only (the architecture-contract Decision 2 precedence law).
- **Narrow edit to an existing stylesheet.** Fix only the asked property; flag
  off-token values in one line rather than sweeping them (scope-fence law).
- **David's brand.** brand-standard palette/typography replace the placeholder
  color/type tokens; spacing, layout, and contrast procedure still apply —
  re-run the checker (Muted Space Blue `#9EB3C5` is 2.16:1 on white: never text).
- **Dark theme.** Same procedure, new arithmetic: recompute every pair —
  ratios never carry over between themes.

## Volatile facts

- Verified 2026-07-13: every ratio quoted in the token block computed this
  session; the checker runs as-is on python3 3.11.15 and prints `RESULT: PASS`.
- Assumption (2026-07-13): `python3` exists on the target machine — check with
  `python3 --version`; any CPython ≥3.8 works, nothing to pip-install.
- Candidate (2026-07-13): the tells list reflects 2024–2026 default model
  output; defaults shift, so treat the list as reviewable, not eternal.

## When NOT to use this skill

- Artifacts in David's name → **brand-standard** supplies palette/typography
  and wins on identity; this skill keeps governing spacing, layout, contrast.
- Existing Word / PowerPoint / Excel / PDF files → **docx**, **pptx**, **xlsx**,
  **pdf**. A NEW PDF is authored via **docx** then converted, or as HTML here.
  MCP servers → **mcp-builder**.
- Chart mark/axis design — unowned in this library (candidate 2026-07-13 for a
  future dataviz skill); charts embedded in a page still take this skill's
  tokens and contrast checks.
- Authoring or restructuring a skill → **skill-authoring**.

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic agent-skill concept (frontend design for web
artifacts). Contrast math is WCAG 2.1 relative luminance (SC 1.4.3 / 1.4.11);
every quoted ratio computed 2026-07-13 in this container.

Re-verify: contrast — run the checker above (expect `RESULT: PASS`);
interpreter — `python3 --version`. Update when: WCAG 3 replaces the 2.x
formula, the placeholder palette becomes standing, brand-standard's colors
change, or the tells list ages (~6-month review — model defaults move).
