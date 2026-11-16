#!/usr/bin/env python3
"""Read bodies of ordinary prose with the receipt gate's own reading and list every sentence it would block.

    python3 prose_scan.py --hooks HOOKS_DIR [--ext md,txt] [--sentences] ROOT [ROOT ...]

Every file under a ROOT whose name ends in one of the extensions is read as one answer text: cut into sentences
by receiptlaw.sentences, each sentence tested with receiptlaw.find_claims and the receipt test of
receiptlaw.bare_claim. Unlike the gate, which stops at the first bare claim of an answer, this lists them all.
Files are counted once by content, blocked sentences once by (claim, sentence). Symbolic links are not followed.
Prints the counts; with --sentences also `file | claim | sentence` for every blocked sentence.
Standard library only; imports receiptlaw from HOOKS_DIR; writes nothing.
"""
import collections
import hashlib
import io
import os
import sys

sys.dont_write_bytecode = True
SKIP_DIRS = (".git", "__pycache__")
MAX_BYTES = 3000000                 # a larger file is not prose


def main(argv):
    hooks, exts, show, roots = None, ("md",), False, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--hooks":
            hooks = args.pop(0)
        elif a == "--ext":
            exts = tuple(args.pop(0).split(","))
        elif a == "--sentences":
            show = True
        else:
            roots.append(a)
    if not hooks or not roots:
        print(__doc__)
        return 2
    sys.path.insert(0, hooks)
    import receiptlaw as law
    ends = tuple("." + e for e in exts)
    seen, hits, n = set(), collections.OrderedDict(), collections.Counter()
    for root in roots:
        for folder, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not os.path.islink(os.path.join(folder, d)))
            for name in sorted(files):
                path = os.path.join(folder, name)
                if not name.endswith(ends) or os.path.islink(path):
                    continue
                n["files"] += 1
                try:
                    raw = io.open(path, "rb").read()
                except (IOError, OSError):
                    continue
                digest = hashlib.sha1(raw).hexdigest()
                if digest in seen or len(raw) > MAX_BYTES:
                    continue
                seen.add(digest)
                n["distinct files read"] += 1
                units = law.sentences(law.prepare(raw.decode("utf-8", "replace")))
                n["sentences"] += len(units)
                for unit in units:
                    claims = law.find_claims(unit)
                    if not claims:
                        continue
                    n["sentences with a standing claim"] += 1
                    if law._has_receipt(law._outside(unit, claims)) or getattr(law, "_searched_place", lambda u, c: False)(unit, claims):
                        continue
                    shown = unit
                    for mark, word in ((law.MARK_BLOCK, "[block]"), (law.MARK_CODE, "[code]"), (law.MARK_QUOTE, "[quoted]")):
                        shown = shown.replace(mark, word)
                    key = (claims[0][2].lower(), " ".join(shown.split()))
                    hits.setdefault(key, os.path.relpath(path, root))
    n["blocked sentences (distinct)"] = len(hits)
    for key in ("files", "distinct files read", "sentences", "sentences with a standing claim", "blocked sentences (distinct)"):
        print("%-34s %d" % (key, n[key]))
    if show:
        for (claim, sentence), where in hits.items():
            print("%s | %s | %s" % (where, claim, sentence))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
