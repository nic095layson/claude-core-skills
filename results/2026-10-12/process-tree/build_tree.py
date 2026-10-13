#!/usr/bin/env python3
"""Generates the Operational Process Tree as SVG (and an HTML wrapper for rendering).

Every node below traces to Rules of Engagement for Operational AI v1.0
(results/2026-10-09/ai-rules-of-engagement): S3 laws, S4 order of operations,
S5 handshakes, S6 controls. The content lists are the auditable part; layout is
computed from them. Run: python3 build_tree.py && node render_tree.js
"""
import html, os

# ---- Brand tokens (brand-standard) ----
SPACE = "#0F436E"; MUTED = "#9EB3C5"; INK = "#1A1A1A"; SEC = "#4A4A4A"
CAP = "#767676"; HAIR = "#D9D9D9"; TINT = "#EEF2F6"; ZEBRA = "#F6F8FA"; WHITE = "#FFFFFF"
DISPLAY = "Eurostile, 'Poppins SemiBold', Poppins, sans-serif"
BODY = "Poppins, 'Century Gothic', Futura, Avenir, Helvetica, sans-serif"

W, H = 1800, 1790
# Columns
LX, LW = 60, 310                  # laws
SX = 660; GW = 460; GX = SX - GW // 2   # spine / gate boxes
FX, FW = 920, 420                 # fail/outcome boxes beside the spine
LOOPX = FX + FW + 14              # vertical channel for loop-back arrows
RX, RW = 1380, 360                # controls

out = []
def E(s): out.append(s)
def esc(t): return html.escape(t, quote=True)

def wrap(t, max_chars):
    words = t.split(); lines = []; cur = ""
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > max_chars: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    if cur: lines.append(cur)
    return lines

def text(x, y, lines, size=13, fill=INK, weight=400, anchor="start", family=BODY, lh=None, italic=False):
    lh = lh or size * 1.32
    style = f"font-family:{family};font-size:{size}px;font-weight:{weight};fill:{fill};" + ("font-style:italic;" if italic else "")
    E(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{style}">')
    for i, ln in enumerate(lines):
        E(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(ln)}</tspan>')
    E('</text>')

def gate(y, num, title, lines):
    """Solid Space Blue step box on the spine. Returns bottom y."""
    h = 46 + 16 * len(lines) + 6
    E(f'<rect x="{GX}" y="{y}" width="{GW}" height="{h}" rx="6" fill="{SPACE}"/>')
    text(GX + 16, y + 26, [f"{num}  {title}"], size=15, fill=WHITE, weight=600, family=DISPLAY)
    text(GX + 16, y + 48, lines, size=12, fill="#DCE6F0", lh=16)
    return y + h

def check(cx, cy, w, h, lines, size=11.5):
    pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    E(f'<polygon points="{pts}" fill="{WHITE}" stroke="{SPACE}" stroke-width="2"/>')
    n = len(lines); start = cy - (n - 1) * 7.5 + 4
    text(cx, start, lines, size=size, fill=INK, weight=500, anchor="middle", lh=15)

def outcome(x, cy, w, lines, kind="fail", size=11.5):
    """Tinted outcome box, vertically centred on cy. Returns (top, bottom)."""
    lh = 15.5; h = 14 + lh * len(lines) + 6
    y = cy - h / 2
    bar = SEC if kind == "fail" else SPACE
    E(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{TINT}"/>')
    E(f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{bar}"/>')
    text(x + 16, y + 19, lines, size=size, fill=INK, lh=lh)
    return y, y + h

def arrow(x1, y1, x2, y2, kind="pass", label=None):
    stroke = SPACE if kind == "pass" else SEC
    dash = "" if kind == "pass" else ' stroke-dasharray="6,5"'
    E(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#ah-{kind})"/>')
    if label:
        text((x1 + x2) / 2, min(y1, y2) - 6, [label], size=11, fill=stroke, weight=600, anchor="middle")

def path(d, kind="pass"):
    stroke = SPACE if kind == "pass" else SEC
    dash = "" if kind == "pass" else ' stroke-dasharray="6,5"'
    E(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#ah-{kind})"/>')

def pill(cx, cy, w, h, label):
    E(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{WHITE}" stroke="{SPACE}" stroke-width="2"/>')
    text(cx, cy + 5, [label], size=14, fill=SPACE, weight=600, anchor="middle", family=DISPLAY)

def caption(y, t):
    text(SX + 12, y, [t], size=11, fill=SPACE, weight=600)

# =====================================================================
E(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
E(f'''<defs>
<marker id="ah-pass" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 z" fill="{SPACE}"/></marker>
<marker id="ah-fail" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 z" fill="{SEC}"/></marker>
</defs>''')
E(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')

# ---- Title band ----
text(60, 58, ["OPERATIONAL PROCESS TREE"], size=30, fill=SPACE, weight=700, family=DISPLAY)
text(60, 86, ["Gates, checks, and where a failed check sends the work. A standard for AI-assisted work, independent of project, model, or vendor."], size=13, fill=SEC)
text(W - 60, 58, ["David Layson"], size=13, fill=INK, weight=600, anchor="end")
text(W - 60, 78, ["Companion to Rules of Engagement for Operational AI v1.0  |  October 12, 2026"], size=11.5, fill=CAP, anchor="end")
E(f'<line x1="60" y1="104" x2="{W-60}" y2="104" stroke="{MUTED}" stroke-width="2"/>')

# ---- Column headers ----
def colhead(x, w, y, title, sub, anchor="start"):
    text(x if anchor == "start" else x + w / 2, y, [title], size=13, fill=SPACE, weight=700, family=DISPLAY, anchor=anchor)
    text(x if anchor == "start" else x + w / 2, y + 17, [sub], size=11, fill=CAP, anchor=anchor)
    E(f'<line x1="{x}" y1="{y+26}" x2="{x+w}" y2="{y+26}" stroke="{HAIR}"/>')
colhead(LX, LW, 140, "THE LAWS", "bind every step of the sequence (Section 3)")
colhead(GX, GW, 140, "THE ORDER OF OPERATIONS", "one sequence for every non-trivial task (Section 4)", anchor="middle")
colhead(RX, RW, 140, "MECHANICAL CONTROLS", "they refuse the work; they never merely remind (Section 6)")

# ---- Laws column ----
laws = [
    ("L1", "Current facts come from current sources"),
    ("L2", "Never invent data; every number names its origin"),
    ("L3", "Load-bearing facts need two independent sources"),
    ("L4", "“Can’t” needs a receipt; otherwise say “did not check”"),
    ("L5", "Totals are built from records, never from memory"),
    ("L6", "No theatrical language, no uncalibrated confidence"),
    ("L7", "No silent defaults; assumptions are numbered"),
    ("L8", "Stay inside the fence; flag, don’t fix"),
    ("L9", "Push back, then commit to one recommendation"),
    ("L10", "Proportionality: no ceremony on trivia"),
]
y = 190
for i, (k, t) in enumerate(laws):
    lines = wrap(t, 38)
    rh = 14 + 15 * len(lines) + 2
    if i % 2 == 0:
        E(f'<rect x="{LX}" y="{y-12}" width="{LW}" height="{rh}" fill="{ZEBRA}"/>')
    text(LX + 8, y + 5, [k], size=12, fill=SPACE, weight=700)
    text(LX + 44, y + 5, lines, size=11.5, fill=INK, lh=15)
    y += rh
ey = y + 36
text(LX, ey, ["HOW THE RULES ARE ENFORCED"], size=12, fill=SPACE, weight=700, family=DISPLAY)
E(f'<line x1="{LX}" y1="{ey+8}" x2="{LX+LW}" y2="{ey+8}" stroke="{HAIR}"/>')
layers = [
    ("Instructions", "steer when a rule applies"),
    ("Skills", "define how; loaded, never recalled"),
    ("Machine checks", "refuse an artifact that fails"),
    ("Hooks", "block an unreceipted claim; force a missed step"),
]
ly = ey + 30
for name, what in layers:
    text(LX, ly, [name], size=11.5, fill=INK, weight=600)
    text(LX + 124, ly, wrap(what, 30), size=11.5, fill=SEC, lh=15)
    ly += 20 if len(wrap(what, 30)) == 1 else 35
text(LX, ly + 14, ["Enforce the action. Never ask the AI", "to certify its own compliance."], size=11, fill=SPACE, weight=600, lh=15)
text(LX, ly + 56, ["If a gate refuses: fix the data,", "never the gate."], size=11, fill=SPACE, weight=600, lh=15)

# ---- Spine ----
Y = 196
pill(SX, Y, 180, 34, "REQUEST")
cur = Y + 17

# 0 Triage
cy = cur + 58
arrow(SX, cur, SX, cy - 36)
check(SX, cy, 240, 70, ["0  Triage:", "trivial, or non-trivial?"])
outcome(FX, cy, FW, ["Trivial: answer directly, no ceremony.", "Ceremony on trivia trains people to switch governance off (L10)."], kind="exit")
arrow(SX + 120, cy, FX - 2, cy, kind="pass", label="trivial")
caption(cy + 54, "non-trivial")
cur = cy + 35

# 1 Plan gate
gy = cur + 34
arrow(SX, cur, SX, gy - 2)
g1_top = gy
cur = gate(gy, "1", "PLAN GATE", [
    "Goal stated so that it could fail  ·  verified facts vs. guesses",
    "Numbered assumptions A1, A2…  ·  success criteria set in advance",
    "Phased plan: an expected result and a fallback for each phase",
])
cy = cur + 46
arrow(SX, cur, SX, cy - 36)
check(SX, cy, 260, 70, ["Can the goal be failed?", "Cheap unknowns converted?"])
t, b = outcome(FX, cy, FW, ["No: investigate, or ask. Never plan around a question", "that one lookup could settle."], kind="fail")
arrow(SX + 130, cy, FX - 2, cy, kind="fail", label="no")
path(f"M{FX+FW},{cy} L{LOOPX},{cy} L{LOOPX},{g1_top+46} L{GX+GW+2},{g1_top+46}", kind="fail")
caption(cy + 54, "yes: the plan is shown to the person before any work starts")
cur = cy + 35

# 2 Pre-flight
gy = cur + 34
arrow(SX, cur, SX, gy - 2)
cur = gate(gy, "2", "PRE-FLIGHT", [
    "Every input the work depends on is verified from a dated source",
    "Freshness card: verified  ·  changed since stored  ·  could not verify",
    "(with the attempt named)",
])
cy = cur + 46
arrow(SX, cur, SX, cy - 36)
check(SX, cy, 260, 70, ["Every input verified", "live, this session?"])
outcome(FX, cy, FW, ["No: verify now, or write “did not check.” A claim of", "“can’t” names the attempt and how it failed (L4).", "Capability unavailable: stop and say so. Never from memory."], kind="fail")
arrow(SX + 130, cy, FX - 2, cy, kind="fail", label="no")
caption(cy + 54, "yes")
cur = cy + 35

# 3 Execute in the fence
gy = cur + 34
arrow(SX, cur, SX, gy - 2)
g3_top = gy
cur = gate(gy, "3", "EXECUTE IN THE FENCE", [
    "The work itself, inside the request as written",
    "State handshake before every write (H3)",
    "One authority per decision; divergence named in one clause (H4)",
])
g3_bottom = cur
text(GX, cur + 16, ["the three checks on the right run continuously during the work"], size=10.5, fill=CAP, italic=True)
bx = GX + GW
checks3 = [
    (["Adjacent", "problem found?"], None, wrap("Yes: flag it in one line. Do not fix it (L8). Approval is per task, never general.", 36)),
    (["Result differs", "from prediction?"], None, wrap("Yes: STOP. Re-diagnose before patching. A surprise means the model of the work is wrong somewhere.", 36)),
    (["State matches", "before the write?"], None, wrap("No: nothing is written. The actual state is shown and reconciled, then resend (H3).", 36)),
]
dcx = bx + 40 + 80; dw = 164; ox = dcx + dw / 2 + 18; ow = FX + FW - ox
row_y = g3_top + 34; rows = []
for i, (q, lab, a) in enumerate(checks3):
    cyy = row_y + i * 66
    rows.append(cyy)
    E(f'<line x1="{bx+28}" y1="{cyy}" x2="{bx+40}" y2="{cyy}" stroke="{SPACE}" stroke-width="2"/>')
    check(dcx, cyy, dw, 56, q, size=11)
    outcome(ox, cyy, ow, a, kind="fail", size=10.5)
    arrow(dcx + dw / 2, cyy, ox - 2, cyy, kind="fail", label=lab)
E(f'<path d="M{bx},{g3_top+30} L{bx+28},{g3_top+30} L{bx+28},{rows[-1]}" stroke="{SPACE}" stroke-width="2" fill="none"/>')
cur = max(cur + 24, rows[-1] + 30)

# 4 Adversarial verification
gy = cur + 30
arrow(SX, g3_bottom, SX, gy - 2)
cur = gate(gy, "4", "ADVERSARIAL VERIFICATION", [
    "1  Grade each criterion PASS or FAIL; PARTIAL is FAIL",
    "2  Exercise, don’t inspect      3  Attempt refutation",
    "4  Self-consistency      5  Surprise handling      6  Gap audit",
    "The author is the worst grader of their own work: switch roles.",
])
cy = cur + 54
arrow(SX, cur, SX, cy - 41)
check(SX, cy, 310, 82, ["All criteria PASS?", "No regression? No load-bearing", "gap left unattempted?"])
outcome(FX, cy, FW, ["No: back to the work. A PARTIAL ships nothing.", "A load-bearing gap that was not attempted is resolved", "now, or the conclusion it supports is withdrawn.", "Any regression blocks acceptance, even an “unrelated” one."], kind="fail")
arrow(SX + 155, cy, FX - 2, cy, kind="fail", label="no")
path(f"M{FX+FW},{cy} L{LOOPX},{cy} L{LOOPX},{g3_top-16} L{bx-26},{g3_top-16} L{bx-26},{g3_top-2}", kind="fail")
caption(cy + 60, "yes, with evidence beside every verdict")
cur = cy + 41

# 5 Report
gy = cur + 34
arrow(SX, cur, SX, gy - 2)
cur = gate(gy, "5", "REPORT", [
    "Method first  ·  every claim dated, marked EVIDENCE or INFERENCE",
    "Bounds stated  ·  next steps left as the owner’s decisions",
])
# 6 Land it
gy = cur + 28
arrow(SX, cur, SX, gy - 2)
cur = gate(gy, "6", "LAND IT", [
    "Committed and pushed; the downstream artifact republished (H10)",
])
cy = cur + 48
arrow(SX, cur, SX, cy - 34)
check(SX, cy, 240, 66, ["Persistence", "confirmed?"])
outcome(FX, cy, FW, ["No: say so and stop. Work that did not land did not", "happen; it counts as not done (H10)."], kind="fail")
arrow(SX + 120, cy, FX - 2, cy, kind="fail", label="no")
caption(cy + 52, "yes")
cur = cy + 33

# 7 Name what fired
gy = cur + 36
arrow(SX, cur, SX, gy - 2)
cur = gate(gy, "7", "NAME WHAT FIRED  ·  RECORD LESSONS", [
    "Which gates actually ran, stated honestly; a missed gate is named",
    "Failures logged as symptom, root cause, evidence, status",
])
py = cur + 42
arrow(SX, cur, SX, py - 19)
pill(SX, py, 200, 36, "DELIVERED")
spine_bottom = py + 18

# ---- Controls column ----
controls = [
    ("Provenance gate", "Refuses to build when any record asserting a real-world fact lacks a source and a verification date.", "binds step 2"),
    ("Publication gate", "Refuses a report in which a named fact lacks two sources or a single-source label.", "binds step 5"),
    ("Receipt gate", "Blocks a response that claims inability without naming the attempt and its failure.", "binds steps 2 and 5"),
    ("Verification enforcement", "Blocks a governed task from finishing if the verification step never loaded.", "binds step 4"),
    ("Outside-reference check", "Flags a recommendation that repeats across runs while sitting far from an independent reference.", "binds step 4"),
    ("Fail-closed build", "Refuses to regenerate the published artifact except through the validated pipeline, verified the same day.", "binds step 6"),
    ("Reproducibility pins", "Refuses when a dated analysis cannot be rebuilt byte-for-byte from the input hashes it names.", "binds step 6"),
]
y = 190
for i, (name, what, binds) in enumerate(controls):
    lines = wrap(what, 50)
    hgt = 30 + 15.5 * len(lines) + 8
    E(f'<rect x="{RX}" y="{y}" width="{RW}" height="{hgt}" rx="4" fill="{ZEBRA if i%2==0 else WHITE}" stroke="{HAIR}"/>')
    E(f'<rect x="{RX}" y="{y}" width="5" height="{hgt}" fill="{SPACE}"/>')
    text(RX + 16, y + 20, [name], size=12.5, fill=SPACE, weight=700)
    text(RX + RW - 10, y + 20, [binds], size=10.5, fill=CAP, anchor="end", italic=True)
    text(RX + 16, y + 40, lines, size=11.5, fill=INK, lh=15.5)
    y += hgt + 8
text(RX, y + 14, wrap("Each control exists because the failure it prevents happened once and was then converted into a check. If the gate refuses, fix the data, never the gate.", 58), size=10.5, fill=SEC, italic=True, lh=14)

# ---- Legend ----
lyy = H - 62
E(f'<line x1="60" y1="{lyy-24}" x2="{W-60}" y2="{lyy-24}" stroke="{HAIR}"/>')
E(f'<rect x="60" y="{lyy-10}" width="26" height="16" rx="3" fill="{SPACE}"/>'); text(94, lyy + 3, ["Step of the sequence"], size=11, fill=INK)
E(f'<polygon points="300,{lyy-12} 314,{lyy-2} 300,{lyy+8} 286,{lyy-2}" fill="{WHITE}" stroke="{SPACE}" stroke-width="2"/>'); text(322, lyy + 3, ["Check: the question answered before the work continues"], size=11, fill=INK)
E(f'<line x1="720" y1="{lyy-2}" x2="760" y2="{lyy-2}" stroke="{SPACE}" stroke-width="2" marker-end="url(#ah-pass)"/>'); text(768, lyy + 3, ["Pass"], size=11, fill=INK)
E(f'<line x1="830" y1="{lyy-2}" x2="870" y2="{lyy-2}" stroke="{SEC}" stroke-width="2" stroke-dasharray="6,5" marker-end="url(#ah-fail)"/>'); text(878, lyy + 3, ["Fail, and where the work goes instead"], size=11, fill=INK)
E(f'<rect x="1140" y="{lyy-10}" width="26" height="16" rx="3" fill="{TINT}"/><rect x="1140" y="{lyy-10}" width="4" height="16" fill="{SEC}"/>'); text(1174, lyy + 3, ["Outcome of a failed check"], size=11, fill=INK)
text(60, lyy + 34, ["Source: Rules of Engagement for Operational AI v1.0 (D. Layson, 2026-10-09), Sections 3 to 6. Every node on this page traces to a numbered law, step, handshake, or control in that document."], size=10.5, fill=CAP)

E('</svg>')

here = os.path.dirname(os.path.abspath(__file__))
svg = "\n".join(out)
open(os.path.join(here, "Operational-Process-Tree_2026-10-12.svg"), "w").write(svg)
open(os.path.join(here, "tree.html"), "w").write(
    f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:#fff}}svg{{display:block}}</style></head><body>{svg}</body></html>')
assert spine_bottom < H - 100, f"spine overflows: {spine_bottom} vs page {H}"
print(f"wrote SVG {W}x{H}; spine bottom y={spine_bottom}; legend at y={lyy}")
