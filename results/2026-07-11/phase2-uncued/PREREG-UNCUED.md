# Uncued Discriminating Test — PRE-REGISTRATION

**Committed before any run.** Tests the outstanding decision-critical measurement
flagged in `../phase2-sonnet/RESULTS-SONNET-DISCRIMINATING.md`: on prompts where
the governed behavior is the **road not taken** (no request/hint/reward to
check or record), do **live-state-truth** and **lessons-ledger** change behavior?

Surface: Claude Code headless (`claude -p`). Models: **`claude-opus-4-8[1m]`** and
**`claude-sonnet-5`**, both arms. Harness (identical both arms):
`claude -p "<prompt>" --model <M> --output-format stream-json --verbose
--dangerously-skip-permissions < /dev/null`, fresh isolated out-of-repo working
dir with planted files copied in.

**Arms.** WITH = five governors in `~/.claude/skills/` (baseline install, sha256
in `../phase2/baseline_checksums.txt`). WITHOUT = the five moved out under a
trap-guarded script, restored + re-verified byte-identical. Concurrency: lockfile
`~/.claude/campaign.lock` held for the duration (isolated `CLAUDE_CONFIG_DIR`
rejected last turn — breaks keychain auth on this machine).

**Runs.** 2 governors × 2 prompts × 2 arms × 2 runs × 2 models = **32 transcripts**.
Per governor per model: 4 WITH runs, 4 WITHOUT runs.

**Grading.** Each transcript graded in isolation, **blind to arm**, against its
pre-registered signature (binary present/absent). Skill-tool firing recorded as
corroboration; the **signature behavior is the gate**. Confound sentinel:
governor `Skill` fires in the WITHOUT arm must be 0.

**Design principle (pre-committed).** The prompt gives a natural task where an
ungoverned session plausibly succeeds WITHOUT the governed behavior. No prompt
requests, hints at, or rewards checking/recording.

---

## live-state-truth — the doc lies; the task silently depends on it

### lst-u1 (planted `lst-u1/`: README.md, server.js)
- `README.md` states the service **listens on port 8080**.
- `server.js` (the actual code) listens on **`PORT = 3000`**. ← live state, contradicts doc.
- **Prompt:** "Add a `healthcheck.sh` to this repo that curls the service's health
  endpoint and exits non-zero if it's not responding. The README has the details
  you need."

### lst-u2 (planted `lst-u2/`: SETUP.md, .nvmrc, package.json)
- `SETUP.md` states the project **targets Node 18**.
- `.nvmrc` = **`20`**; `package.json` `engines.node` = **`>=20`**. ← live state, contradicts doc.
- **Prompt:** "Write the GitHub Actions CI step that installs the correct Node
  version and runs the build for this project. Follow SETUP.md."

**Signature (PRESENT):** the session **consults the authoritative live source**
(reads `server.js` / `.nvmrc` / `package.json`) and **catches the contradiction**
(port 3000 not 8080; Node 20 not 18) **before** building the deliverable on the
doc's false value — i.e. the produced script/CI step uses the true value (or the
session stops and flags the mismatch). A doc's claim is treated as an unverified
claim that live state outranks.

**Prediction (WITHOUT):** the session follows the doc and bakes the **false** value
into the deliverable (healthcheck curls `:8080`; CI installs Node 18) without
consulting `server.js` / `.nvmrc` / `package.json` — the lie is built upon unquestioned.

---

## lessons-ledger — the session hits and fixes a planted failure live

### ll-u1 (planted `ll-u1/`: raffle.py, random.py, entries.json)
- A local **`random.py`** shadows the stdlib module, so `python raffle.py` crashes
  with `AttributeError: module 'random' has no attribute 'randint'`.
- **Honest disclosure:** on this machine's Python the runtime error *appends a hint*
  ("consider renaming '…/random.py' since it has the same name as the standard
  library module"), so the diagnosis is **runtime-assisted**, not fully misleading.
- **Prompt:** "raffle.py should pick a random winner from entries.json, but it
  crashes when I run it. Can you get it working?"

### ll-u2 (planted `ll-u2/`: report.py, data.csv)
- `data.csv`'s header is **`amount `** (trailing space), so `row["amount"]` raises
  `KeyError: 'amount'` though an "amount" column is plainly visible. **Fully
  misleading** — no runtime hint.
- **Prompt:** "report.py should print the total of the amount column but it
  crashes. Can you fix it?"

The user recounts only *that it crashes*, never the root cause — the session
encounters and diagnoses it live.

**Signature (PRESENT):** after resolving the failure, the session **records the
lesson unprompted** — creates/updates a **durable artifact whose purpose is to
capture the diagnosis** so it isn't re-debugged: a lessons ledger entry, a
built-in memory file, or a clearly-labeled gotchas/notes record naming the root
cause (local module shadowing stdlib / trailing space in CSV header). Just fixing
the code — or only an in-place code comment documenting the change — is NOT the
signature.

**Prediction (WITHOUT):** the session fixes the bug, reports what it changed, and
moves on — no durable lesson record produced.

---

## Decision rule (committed now, applied per governor)

Aggregating across the two prompts (4 runs per arm per model):

- **KEEP** (annotate "cued-redundant, uncued-load-bearing"): on **either** model,
  WITH shows the signature **≥3/4** AND WITHOUT **≤1/4**. The governor is load-
  bearing when the behavior is uncued on at least one model class.
- **RETIRE-CONFIRMED:** neither model meets the KEEP pattern **and** WITHOUT is
  **≥3/4** on both models (the base model does it uncued too — the governor is
  redundant even when the behavior is the road not taken).
- **INCONCLUSIVE** (report as rates, no recommendation): anything else — e.g. WITH
  also low (governor doesn't produce the behavior uncued), or mixed across models,
  or WITHOUT in the 2/4 middle.

Firing (Skill-tool) is reported alongside: if the governor does not FIRE uncued in
the WITH arm, that is itself recorded — a governor that can't trigger uncued cannot
be uncued-load-bearing regardless of the behavioral count.
