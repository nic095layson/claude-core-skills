# Row-parity check: every bolded lead in the generator source must appear in the rendered PDF's text.
# Added 2026-10-09 after LibreOffice silently dropped laws L2-L10 where the laws table split across a page.
# Usage: python3 check_row_parity.py build_roe.js Rules-of-Engagement-Operational-AI_2026-10-09.pdf  (exit 1 on any miss)
import re, subprocess, sys
src, pdf = sys.argv[1], sys.argv[2]
s = open(src).read()
leads = {l for l in re.findall(r'\*\*([^*]{6,60})\*\*', s) if '&&' not in l}  # skip the markup parser's own code
txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
norm = lambda x: re.sub(r'\s+', ' ', x.replace('\\u201C','\u201c').replace('\\u201D','\u201d').replace('\\u2019','\u2019').replace('\\"','"')).strip()
t = re.sub(r'\s+', ' ', txt)
t2 = t.replace('\u2019', "'")
missing = [l for l in sorted(leads) if norm(l) not in t and norm(l).replace('\u2019', "'") not in t2]
print(f"leads checked: {len(leads)}  missing from PDF: {len(missing)}")
for m in missing: print("  MISSING:", m)
sys.exit(1 if missing else 0)
