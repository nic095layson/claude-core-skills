#!/usr/bin/env python3
"""Grade photo-editing trigger evals per the committed operationalization:
FIRED := the photo-editing Skill tool is invoked in the stream-json
transcript. Corroboration flags recorded, not graded."""
import glob
import json
import os
import re

TDIR = '/home/user/claude-core-skills/results/2026-08-10/trigger-evals-photo-editing/transcripts'
EXPECT_FIRE = {1, 2, 3, 4}
EXPECT_SILENT = {5, 6, 7}

rows = []
for f in sorted(glob.glob(TDIR + '/photo-editing-id*-r*.jsonl')):
    m = re.search(r'id(\d+)-r(\d+)', f)
    eid, run = int(m.group(1)), int(m.group(2))
    fired = False
    inspect_ran = False
    new_file = False
    with open(f) as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = ev.get('message')
            if not isinstance(msg, dict):
                continue
            content = msg.get('content')
            if not isinstance(content, list):
                continue
            for c in content:
                if not isinstance(c, dict) or c.get('type') != 'tool_use':
                    continue
                inp = json.dumps(c.get('input', {}))
                if c.get('name') == 'Skill' and 'photo-editing' in inp:
                    fired = True
                if 'inspect_image.py' in inp:
                    inspect_ran = True
                if c.get('name') in ('Write', 'Bash') and re.search(
                        r'(save|output|-cropped|-resized|-rotated|\.jpg|new)', inp, re.I):
                    new_file = True
    rows.append((eid, run, fired, inspect_ran, new_file, os.path.getsize(f)))

fire_runs = [(e, r, f) for e, r, f, *_ in rows if e in EXPECT_FIRE]
silent_runs = [(e, r, f) for e, r, f, *_ in rows if e in EXPECT_SILENT]
fire_ok = sum(1 for *_, f in fire_runs if f)
silent_ok = sum(1 for *_, f in silent_runs if not f)

print(f"{'id':>3} {'run':>3} {'FIRED':>6} {'inspect':>8} {'newfile':>8} {'bytes':>8}")
for eid, run, fired, ins, nf, sz in rows:
    exp = 'FIRE' if eid in EXPECT_FIRE else 'SILENT'
    ok = (fired and exp == 'FIRE') or (not fired and exp == 'SILENT')
    print(f"{eid:>3} {run:>3} {str(fired):>6} {str(ins):>8} {str(nf):>8} {sz:>8}  expect={exp} {'OK' if ok else '** MISS **'}")

print(f"\nshould-fire: {fire_ok}/{len(fire_runs)} fired (gate >=7/8)")
print(f"should-not:  {silent_ok}/{len(silent_runs)} silent (gate >=5/6)")
gate = fire_ok >= 7 and len(fire_runs) == 8 and silent_ok >= 5 and len(silent_runs) == 6
print("GATE:", "PASS" if gate else "FAIL/INCOMPLETE")
