#!/usr/bin/env python3
"""Shared prompt classifier for the governance hooks (governance-trigger.py, governance-enforce.py).

One file so the advisory trigger and the blocking gate can never disagree about what counts as
governed work. Every pattern is pinned by hooks/selftest-governance-classify.py; change a pattern
and the fixture must still pass, including the should-stay-silent set.

Classes and the governor each one routes to:
  analysis    -> adversarial-verify   (an analysis, recommendation, forecast, backtest the owner will rely on)
  review      -> adversarial-verify   (check this / is this right / ready to ship / audit / validate)
  build       -> plan-gate            (build, create, implement, refactor, draft, apply fixes and push)
  dispute     -> adversarial-verify + scope-fence
                 (the owner questions or disputes the work's method, data or result; the answer is an
                  assessment, never a fix — INC-2026-10-13-01)
  requirement -> scope-fence          (advisory only: "X is critical" states a requirement, it does not
                  authorize building X — scope-fence rule 4; never enforced by the Stop gate)

Two kinds of pattern (calibrated 2026-10-13, results/2026-10-13/system-validation/):
  STRONG  words that are almost always a request when they appear (analyze, implement, double-check,
          "proceed with the fixes", "are we sure"); matched anywhere.
  FRAMED  words that are as often nouns or chat as requests (build, review, draft, write, update, push);
          matched only in a request frame: at the start of a clause, or after "please",
          "can you", "I need you to", "let's", "and", "then". "thanks, that build fixed it" and
          "Program review ran four hours" stop matching; "Build the deck" and "...and push" still do.
Guards, applied after matching: creative play (a limerick, a poem) is not governed build work; a message
that opens as a continuation ("looks good, carry on…", "ok sounds good, go ahead") is not enforced unless
it also orders a new consequential action (push, upload, package, build, apply…).

History: the 2026-07-15 classifier (three classes) stayed SILENT on three of the four owner messages of
the 2026-10-12 incident and FIRED on "what time zone is the draft in?". The 2026-10-13 morning version
fixed those; measured the same day on a held-out set it caught about 37% of governed requests and
enforced 17-22% of negatives (a limerick, "thanks, that build fixed it", "looks good, carry on").
"""
import re

_FRAME = (r"(?:^|[.!?;]\s+|:\s+|\n\s*"
          r"|\b(?:and|then|also|now|just|please|pls|plz)\s+|,\s*"
          r"|\b(?:can|could|would|will) you(?: please| also| just| now)?\s+"
          r"|\bi(?:'d| would)? (?:need|want|like) you to\s+|\bhelp me\s+|\blet'?s\s+|\bgo ahead and\s+"
          r"|\btime to\s+|\bwe (?:need|should|have) to\s+|\bneed to\s+|\bi want to\s+"
          r"|\b(?:are|were) you able to\s+|\bwould you be able to\s+|\bis it possible to\s+|\b(?:can|could) we\s+"
          r"|\bfeel free to\s+)(?:please\s+)?")


def _framed(verbs):
    return _FRAME + r"(?:" + verbs + r")\b"


STRONG = {
    "analysis": re.compile(
        r"\b(analy[sz]\w*|advis\w*|advice|recommend\w*|forecast\w*|predict\w*|assess\w*|evaluat\w*|outlook"
        r"|backtest\w*|dissertation|compar(e|es|ing|ison)\b|pros and cons|thoughts on\b"
        r"|is this a (good|sound|bad)\b|worth (buying|investing|it)\b"
        r"|when will\b.{0,40}\b(hit|reach|cross|top|bottom)"
        r"|should (i|we)\b.{0,60}\b(invest|buy|sell|adopt|switch|migrate|choose|pick|hire|move)"
        r"|which (one )?(is|would be|are) (the )?(better|best|least|most|safer|safest|riskier|cheaper)"
        r"|break (it|this|that|them) (out|down) by"
        r"|(provide|give me|put together|prepare|write up|need) (a |an |the |me a |me an )?([\w-]+ ){0,2}(report|analysis|breakdown|write-?up|assessment|comparison)\b"
        r"|\bgo through\b.{0,80}\b(find|flag|list|identify|pull)"
        r"|\bwhat (happens|would happen|changes) (to|if)\b.{0,80}\b(if|when) (i|we)\b|\bwhat if (i|we)\b)", re.I),
    "review": re.compile(
        r"\b(double.?check|sanity.?check|is this (correct|right|safe|ready)|ready to ship"
        r"|before i (ship|run|deploy|merge|send)\b|(does|do|did) (this|it|that|they) look (right|good|correct)"
        r"|(?<![\w-])verify|(?<![\w-])validate|(?<![\w-])calibrate|audit (the|this|my|our|every|all)\b"
        r"|(conduct|run|do|perform) (a |an |the )?([\w-]+ ){0,3}(audit|review|validation|calibration|assessment|evaluation|investigation|test(ing)?)\b"
        r"|\bis (\S+[ -]){1,3}actually (firing|triggering|working|running|loading|being used|followed|enforced)"
        r"|\bline by line\b)", re.I),
    "build": re.compile(
        r"\b(implement\w*|refactor\w*|migrat(e|es|ing)\b|scaffold|configure|stand up|wire up"
        r"|draft (a|an|the|me|us|this|some|one|replies|responses|emails?|letters?|memos?|notes|slides|copy|language)\b"
        r"|write (a|an|the|me|us)\b|design (a|an|the)\b"
        r"|proceed with (the |all |these |those )?([\w-]+ ){0,2}(fix|fixes|changes|plan|implementation|updates?|edits|option \w+)\b"
        r"|apply (the |all |these |those )?([\w-]+ ){0,2}(fix|fixes|changes|patch|patches|edits)\b"
        r"|turn (it|this|that|these|those|everything|them)\b.{0,60}\binto\b"
        r"|need (the|a) new (deck|doc|document|version|draft|memo|report|board|plan|slides?)\b"
        r"|provide\b(?:\s+[\w,'-]+){0,6}\s+(instructions|document|doc|plan|memo|deck|guide|template|draft)\b"
        r"|take another pass\b"
        r"|\bneeds? (the|this|that|it|these|those) .{0,50}\b(folded|worked|baked|added|merged|pulled) in(to)?\b"
        r"|\bcan (the|this|that|our|my) [\w' -]{1,40}\b(lose|drop|shrink|fit (on|in|into)|be (cut|trimmed|shortened|tightened|reduced))\b)", re.I),
    "dispute": re.compile(
        r"(\bi (don'?t|do not|dont) agree\b|\bi disagree\b"
        r"|\b(not|n'?t|never) (being |been )?(taken|factored|accounted) (into account|in|for)\b"
        r"|\bconcerns? (about|with)\b.{0,80}\b(integrity|method\w*|data|model\w*|logic|test\w*|number\w*|result\w*|accuracy)"
        r"|\b(was|were|is|are) (this|that|it|these|those|the \w+)\b.{0,30}\bfollowed\b"
        r"|\bare you (still |actually |really )?(following|using|applying|taking)\b"
        r"|\b(your|the) (logic|method\w*|model\w*|test\w*|decision\w*|reasoning|numbers?|results?)\b.{0,50}\b(wrong|regress\w*|flawed|incorrect|off|irrelevant|damag\w*)"
        r"|\b(data|computational|system) integrity\b"
        r"|\bwhy (did|do|does|is|are|was|were|has|have) (you|it|the (model|method|board|system|tool|engine|projection\w*|rank\w*|card))\b"
        r"|\bwhy is (\S+ ){1,3}(sitting|ranked|rated|at \d|below|above|so (high|low)|still)\b"
        r"|\bare (we|you) (sure|certain|confident)\b|\b(don'?t|do not|dont) (buy|believe|trust)\b"
        r"|\b(look|looks|seem|seems) (too good|off|wrong|suspicious|fishy)\b"
        r"|\bfeels? like\b.{0,60}\b(different|wrong|off)\b"
        r"|\bi think (you|we|it|the \w+)\b.{0,40}\b(tuned|overfit\w*|double.?count\w*|leak\w*|wrong|biased|cherry.?pick\w*)"
        r"|\bdouble.?counting\b|\bisn'?t that the same\b|\bmeans nothing\b"
        r"|\bwhere (did|does|do) (the|that|this|your|our|these|those) .{0,50}\bcome from\b"
        r"|\b(says|said|claims|claimed|reports|reported) .{0,60}\bbut (i|we) (only )?(see|count|find|have)\b|\bwhere'?s the (second|other|missing)\b"
        r"|\bonly \d{1,2}(st|nd|rd|th)\b.{0,60}\?"
        r"|\bis (\S+[ -]){1,3}actually (firing|triggering|working|running|loading|being used|followed|enforced))", re.I),
    "requirement": re.compile(
        r"(\b(is|are) (critical|essential|non-?negotiable|mandatory|required|a hard requirement|a must)\b"
        r"|\b(that|it)'s (critical|essential|non-?negotiable|mandatory)\b"
        r"|\bmust stay\b|\bhas to (stay|match|remain)\b|\bmake sure (the|that|it|every)\b)", re.I),
}

FRAMED = {
    "analysis": re.compile(_framed(r"investigate|research|report on|summari[sz]e|estimate|project|rank"), re.I),
    "review": re.compile(_framed(r"review|check|test|proofread|trace|grade|audit"), re.I),
    "build": re.compile(_framed(
        r"build|create|make(?! sure)|write|draft|design|rewrite|update|add|include|incorporate|insert|cut|remove|fix|change|package|upload|deploy"
        r"|push|ship|publish|regenerate|produce|prepare|put together|set ?up|install|generate|convert|format|restructure"
        r"|elaborate|expand|flesh out|reply|respond|write back|follow up"), re.I),
}

# Kept for callers and documentation that read PATTERNS: the union view of STRONG.
PATTERNS = STRONG

_QUOTED = re.compile(r'"[^"\n]{1,300}"|\u201c[^\u201d\n]{1,300}\u201d|(?<![\w])\'[^\'\n]{8,300}\'(?![\w])|\u2018[^\u2019\n]{8,300}\u2019')

CREATIVE = re.compile(r"\b(limerick|haiku|poem|sonnet|joke|riddle|pun|rap|lyrics|bedtime story|short story)\b", re.I)
CONTINUATION_OPENER = re.compile(
    r"^\s*(?:ok(?:ay)?[,.!]?\s*(?:so\s+)?)?(?:looks good|sounds good|great|perfect|yes|yep|sure|go ahead|carry on"
    r"|keep going|continue|redo|again|try again|thanks)\b", re.I)
CONSEQUENTIAL = re.compile(
    r"\b(push|upload|deploy|merge|publish|ship|package|apply|implement|build|create|draft|write|fix|approve)\w*\b", re.I)

GOVERNORS_FOR = {
    "analysis": ("adversarial-verify",),
    "review": ("adversarial-verify",),
    "build": ("plan-gate",),
    "dispute": ("adversarial-verify", "scope-fence"),
    "requirement": ("scope-fence",),
}

# Classes the Stop gate may block on. "requirement" is advisory only: a requirement statement
# has no deliverable to gate, and blocking it would be ceremony (architecture-contract invariant 5).
ENFORCED = ("analysis", "review", "build", "dispute")

ORDER = ("analysis", "review", "build", "dispute", "requirement")

HARNESS_MARKERS = ("[SYSTEM NOTIFICATION", "<task-notification>", "<wake ", "<agent-message", "<webhook-payload")


def is_harness_text(text: str) -> bool:
    """True for harness-generated text (task notifications, wake envelopes, subagent hand-backs)."""
    t = (text or "").strip()
    return any(m in t for m in HARNESS_MARKERS)


def classify(prompt: str):
    """Return the list of matched class names, in a stable order.

    Harness-generated prompts are never owner requests, so they classify as nothing: on 2026-10-13
    the trigger fired on a task-failure notification whose text happened to contain a build verb."""
    p = (prompt or "").strip()
    if not p or is_harness_text(p):
        return []
    # Quoted text is not the owner's own ask (labeling policy, edge rule 3): "Have agent write 'what can
    # you make easier'" quotes a request to someone else. Double-quoted spans are blanked before matching.
    q = _QUOTED.sub(" ", p)
    found = set()
    for name in ORDER:
        if STRONG[name].search(q) or (name in FRAMED and FRAMED[name].search(q)):
            found.add(name)
    if "build" in found and CREATIVE.search(q):
        found.discard("build")
    if CONTINUATION_OPENER.search(q) and not CONSEQUENTIAL.search(q):
        found -= set(ENFORCED)
    return [n for n in ORDER if n in found]


def governors(classes):
    """Deduplicated governors for the given classes, in first-seen order."""
    out = []
    for c in classes:
        for g in GOVERNORS_FOR.get(c, ()):
            if g not in out:
                out.append(g)
    return out
