#!/usr/bin/env python3
"""Claim-receipt lint: find sentences that claim a mechanism runs, exists, is wired, verifies, supersedes,
keeps something green or changes nothing — with no receipt beside the claim.

Why it exists: in one project's two worst days (2026-10-19..21), 9 of 21 recorded failures were a confident
sentence about whether something runs or what it touches, written with nothing run behind it ("the weekly
pull keeps it green" — no script wrote that file; "it changes nothing either way" — it moved a headline by
2.2 points). The arithmetic was right every time; the sentences about the system were not. A receipt is
cheap to write and its absence is mechanically visible, so this lint looks for the absence.

What counts as a CLAIM (case-insensitive, outside code fences, blockquotes, quoted "…" and struck ~~…~~ text):
  runs / runs every / is (now) wired / live / enforced / scheduled / in place / verified ...; works unattended;
  will run / push / publish / catch / fire; keeps it green / current / fresh; supersedes / replaces / covers;
  changes nothing / no effect / nothing either way / makes no difference; is (this session's) own repository;
  still (only) yours / you need to attach|enable|install|connect.
What counts as a RECEIPT (within RECEIPT_WINDOW characters of the claim, in its own list item or table row when it
  sits in one, else its paragraph):
  inline `code`; a commit hash; a PASS/FAIL line; an exit code; a path with an extension; a run-ledger or
  record reference; a count "N of M"; or an honest status word: EVIDENCE, INFERENCE, NOT-ATTEMPTED,
  ATTEMPTED-FAILED, UNVERIFIABLE, UNVERIFIED, "did not check", "not yet observed", "proposal".

Modes: default ADVISORY (lists flags, exit 0); --strict exits 1 on any flag. Prints
'CLAIM RECEIPTS: PASS — ...', 'CLAIM RECEIPTS: ADVISORY — N unreceipted claims ...' or 'CLAIM RECEIPTS: FAIL — ...'.

    python3 claim_receipts.py [--strict] [--json OUT] FILE.md [FILE.md ...]
Stdlib only. A lint, not a judge: a flag means "show the receipt", never "this is false".
"""
import argparse
import json
import re
import sys

RECEIPT_WINDOW = 200

CLAIM = re.compile(
    r"\b(?:runs?\s+(?:every|each|daily|nightly|unattended|on\s+(?:its|their)\s+own|automatically)"
    r"|is\s+(?:now\s+)?(?:wired|live|enforced|scheduled|in\s+place|active|automated|guarded|verified|checked|covered)"
    r"|are\s+(?:now\s+)?(?:wired|live|enforced|scheduled|in\s+place|active|automated|guarded|verified|checked|covered)"
    r"|works\s+unattended|will\s+(?:run|push|publish|catch|fire|keep|work)\b"
    r"|keeps?\s+(?:it|them|this|that|the\s+\w+)\s+(?:green|current|fresh|up\s+to\s+date|in\s+sync)"
    r"|supersedes|replaces\s+(?:it|the\s+\w+)"
    r"|changes?\s+nothing|nothing\s+either\s+way|no\s+effect\s+on|makes\s+no\s+difference|moves?\s+nothing"
    r"|(?:this\s+session'?s\s+)?own\s+repository"
    r"|still\s+(?:only\s+)?yours|you\s+(?:still\s+)?need\s+to\s+(?:attach|enable|install|connect))", re.I)

RECEIPT = re.compile(
    r"`[^`\n]+`|\b[0-9a-f]{7,40}\b|\b(?:PASS|FAIL)\b|\bexit\s+\d|\b[\w./-]+\.(?:py|sh|json|jsonl|md|csv|html|txt|log)\b"
    r"|run-?ledger|\brecord\b|\b\d+\s+of\s+\d+\b|EVIDENCE|INFERENCE|NOT-ATTEMPTED|ATTEMPTED-FAILED|UNVERIFIABLE|UNVERIFIED"
    r"|did\s+not\s+check|not\s+yet\s+observed|\bproposal\b|\bchecked\b|\bmeasured\b|\bre-?ran\b|\breturned\b")


QUOTED = re.compile(r'"[^"\n]{3,300}"|“[^”\n]{3,300}”|~~[^~\n]{3,400}~~')
ITEM = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|\|)")


def _strip(text):
    """Blank out fenced code and blockquotes (keep line numbers), so text that only DISCUSSES a claim is skipped."""
    out, fence = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence; out.append(""); continue
        out.append("" if fence or ln.lstrip().startswith(">") else ln)
    text = "\n".join(out)
    # quoted ("…", “…”) and struck (~~…~~) text REPORTS a claim — usually a correction quoting the old false one —
    # it does not assert it (red-team RT-2, 2026-10-21). Blank it with spaces so line numbers and offsets hold.
    return QUOTED.sub(lambda m: " " * len(m.group(0)), text)


def scan_text(text):
    """Return [(line, claim_phrase, sentence)] for claims with no receipt within RECEIPT_WINDOW in the same paragraph."""
    clean = _strip(text)
    flags = []
    for m in CLAIM.finditer(clean):
        # the unit that holds the claim: its own list item or table row when it sits in one (a neighbouring item's
        # receipt vouches for a different sentence — red-team RT-1, 2026-10-21), else its paragraph
        ls = clean.rfind("\n", 0, m.start()) + 1
        le = clean.find("\n", m.end()); le = len(clean) if le < 0 else le
        if ITEM.match(clean[ls:le]):
            ps, pe = ls, le
        else:
            ps = clean.rfind("\n\n", 0, m.start()); ps = 0 if ps < 0 else ps + 2
            pe = clean.find("\n\n", m.end()); pe = len(clean) if pe < 0 else pe
        window = clean[max(ps, m.start() - RECEIPT_WINDOW):min(pe, m.end() + RECEIPT_WINDOW)]
        if RECEIPT.search(window):
            continue
        line = clean.count("\n", 0, m.start()) + 1
        s0 = max(clean.rfind(". ", 0, m.start()), clean.rfind("\n", 0, m.start())) + 1
        s1 = clean.find(".", m.end()); s1 = len(clean) if s1 < 0 else s1 + 1
        flags.append((line, m.group(0), clean[s0:s1].strip()[:200]))
    return flags


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any unreceipted claim")
    ap.add_argument("--json", help="write the flags here")
    a = ap.parse_args(argv)
    allf = []
    for f in a.files:
        try:
            text = open(f, encoding="utf-8").read()
        except OSError as e:
            print(f"CLAIM RECEIPTS: FAIL — cannot read {f}: {e}"); return 1
        for line, phrase, sent in scan_text(text):
            allf.append(dict(file=f, line=line, claim=phrase, sentence=sent))
            print(f"  {f}:{line}: '{phrase}' — {sent}")
    if a.json:
        json.dump(allf, open(a.json, "w", encoding="utf-8"), indent=1)
    n = len(allf)
    if n == 0:
        print(f"CLAIM RECEIPTS: PASS — {len(a.files)} file(s), every mechanism claim carries a receipt"); return 0
    if a.strict:
        print(f"CLAIM RECEIPTS: FAIL — {n} unreceipted claim(s) in {len(a.files)} file(s)"); return 1
    print(f"CLAIM RECEIPTS: ADVISORY — {n} unreceipted claim(s) in {len(a.files)} file(s); show a receipt or mark the status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
