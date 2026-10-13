# After-report — Fortifying Gauntlet and the operating process after the 2026-10-13 scope-fence breach

**Owner request (2026-10-13, verbatim):** "Hi Claude, attached for you is an incident report where
another Code session operated out of scope. I fear regression in operational excellence and the
Gauntlet procedure that we've created. Review incident report, learn from mistakes, and use skill
builder to fortify the gates we have built to ensure this does not occur." Attached: the kit's
`after-report-2026-10-13-scope-fence.md` and its `analysis-session-prompt.md` (eight questions,
answered in §5).

**What was analyzed (all read this session):**
- `nic095layson/claude-core-skills` at `3833334` (base of this branch); the kit
  `nic095layson/fantasy-basketball-2026-27` at `2df5b22` (main, 2026-10-12) including the incident's
  evidence folder `report/after-reports/scope-fence-2026-10-13/`; the deck
  `nic095layson/yahoo-fantasy-basketball` at `8ec736b`.
- This cloud container's user scope (`~/.claude/`), the account-synced skills, and the harness's
  own hook wiring.
- Claude Code documentation: settings, hooks guide, memory, plugin manifest reference (fetched
  2026-10-13; quotes in `raw/docs-quotes-2026-10-13.md`).
- Governors loaded through the Skill tool this run: gauntlet, plan-gate, scope-fence, after-report,
  delegation-discipline, architecture-contract, skill-creator, session-start-hook, adversarial-verify
  (before delivery).

**Method and verification:**
- The incident's three load-bearing claims were re-derived from its committed artifacts, not
  taken from its prose (§1).
- Every change was built against a pre-registered prediction
  (`experiments/hypothesis-2026-10-13-project-enforcement-pack.md`, written before any run), then
  measured: a 25-case fixture, pipe tests of every hook, and six live headless sessions (§3).
- Documentation claims from the delegated agent were re-fetched by this session before use
  (delegation-discipline rule 4); the quotes in `raw/` are from this session's own fetches.
- Guard (`guard_essentials.sh`) run before the change (PASS at `3833334`) and after (PASS, with
  three new assertions). Every edited skill lints PASS; every governor description is
  byte-identical to `HEAD`.

**Headline.** The incident was not a regression in the governors' text. It was a promise with no
mechanism: the kit's `CLAUDE.md` says the governors run on every session, but on the cloud surface
nothing could load them — the user doctrine file it points to does not exist there, the kit has no
settings file, and this library's validated enforcement hooks were wired nowhere. Worse, the
enforcement classifier as it stood would have stayed silent on three of the owner's four incident
messages. This change wires the enforcement pack at project scope (which cloud sessions started
inside one repository do read, and which fired live in this very session minutes after being
written), fixes and pins the classifier, adds a post-compaction protocol, puts the three unwritten
house rules into the governors and into a cloud-safe doctrine block, and measures the result on the
incident's own message. One gap stays open and is named plainly: a cloud session with **several**
repositories attached, which is the incident's exact configuration, does not read repository hooks;
the plugin route that would cover it is specified, not built.

## 1. The incident's claims, spot-checked

| claim in the after-report | what this session did | result |
|---|---|---|
| Census: no governor Skill load since 2026-09-23; 28 compactions; 28 plan-gate re-attachments with D51R args | Recounted from `out/timeline.json` (`raw/spotcheck-census-recount.json`) | EVIDENCE: 4 Skill loads (after-report ×3, pdf-extract ×1), 0 governors, 28 / 28 / 28 — matches |
| `~/.claude/CLAUDE.md` ABSENT; lessons-ledger, live-state-truth, research-methodology not synced | Read `out/integrity_check.txt`; ran the same checks in this container | EVIDENCE: ABSENT here too; same three skills absent from `~/.claude/skills/synced/` |
| Era not stable over the 20-season window (3PM/36: 0.90 → 1.98) | Re-ran `tools/league_per36.py` from its committed copy on the pinned CSV | EVIDENCE: output byte-identical to `out/league_per36.json`; 2006-07 = 0.90, 2025-26 = 1.98 |
| Both repos clean, nothing published | `git status` on fresh clones at the incident commits | EVIDENCE: clean at `89fe5a5`/`8ec736b` per the integrity file; the folder has since merged (kit now `2df5b22`) |

Nothing in the incident report was contradicted. Two of its root causes were sharpened by
measurement here (§6).

## 2. What was changed in this repository

All on `claude/trusting-curie-d2ft62` (draft PR 24), one commit per change, nothing merged.
Decision A1 (see §8): the owner's instruction to fortify was taken as superseding the attached
prompt's "change nothing"; the kit and deck receive proposed text only (§4), since this session has
no push access to them and the prompt fenced them.

| # | change | files | mechanism | measurement |
|---|---|---|---|---|
| F1 | **Shared classifier** with `dispute` and `requirement` classes; `draft` and `migration` patterns narrowed; harness notifications ignored | `hooks/govclass.py` | one file feeds both hooks, so they cannot disagree | fixture 27/27 (`raw/fixture-…log`); old-vs-new table (`raw/classifier-old-vs-new…txt`) |
| F2 | **Trigger and Stop gate rebuilt** on F1; gate reads list-style user content; skips harness-marked (`isMeta`) entries; counts only Skill calls after the owner's latest message (re-attached text cannot satisfy it) | `hooks/governance-trigger.py`, `hooks/governance-enforce.py` | advisory inject + blocking Stop, loop-safe | fixture (block/allow cases, incl. the live false-block shape); live A/B (§3) |
| F3 | **Compaction/resume hook**: post-compaction protocol injected, first-write reminders re-armed | `hooks/session-doctrine.sh` | SessionStart, matcher `compact\|resume` (documented route for re-injecting context) | pipe-tested: compact → context + 0 sentinels left; startup → silent |
| F4 | **Project-scope wiring** of all seven hooks | `.claude/settings.json` | travels with the clone; `$CLAUDE_PROJECT_DIR` paths | fired live in this session (§3.3); guard assertion |
| F5 | **Doctrine block** for cloud + the three house rules | `instructions/project-doctrine-block.md`, `CLAUDE.md`, `instructions/claude-code-global-doctrine.md` (surface note) | project `CLAUDE.md` is read on cloud and re-read after compaction | guard drift check (block in `CLAUDE.md` == canonical) |
| F6 | **Governor bodies**: plan-gate §3 method-parameters-are-assumptions + §5 phase-boundary line; scope-fence §2 question-gets-an-assessment + §4 stated-requirement-is-not-a-build-order; gauntlet §6 re-attached-is-not-loaded + Fired-line state | three `SKILL.md` | prose, provenance appended | lint PASS ×3; descriptions byte-identical to `HEAD`; **UNMEASURED** (pre-registered as such) |
| F7 | **Runbook 4** (cloud-safe pack install + multi-repo caveat) | `install-and-surfaces/SKILL.md` | — | lint PASS |
| F8 | **Guard assertions**: pack wired, fixture passes, doctrine block not drifted | `guard_essentials.sh` | fails the guard if the mechanism is ever unwired | guard PASS |
| F9 | **Ledger** entry INC-2026-10-13-01; **experiment** pre-registration | `.claude/LESSONS.md`, `experiments/…` | — | guard: no duplicate keys |

## 3. Measurements

### 3.1 Fixture (mechanical, `hooks/selftest-governance-classify.py`)

27 of 27 pass: the four incident messages classify as governed (23:41 and 23:51 →
adversarial-verify + scope-fence; 23:42 → scope-fence advisory only; 23:54 → all three); eight
should-stay-silent messages classify as nothing, including "what time zone is the draft in?",
"who did the Lakers draft last year?", "why is the sky blue?", and a harness task notification;
the Stop gate blocks the unloaded 23:41 message under both transcript content shapes, allows a
synced-copy load, allows a load that is followed by harness-marked skill-text and hook-feedback
entries (the shape that caused the live false block, §6), allows requirement-only and trivia, and
allows when `stop_hook_active` is set.

The old classifier on the same messages (`raw/classifier-old-vs-new-2026-10-13.txt`): silent on
23:41, 23:42, 23:51; fired on 23:54 (via "implement") and on "what time zone is the draft in?".

### 3.2 Live A/B (headless `claude -p` from this container; pre-registered P2)

| run | arm | governor Skill loads (in order) | GOV-ENFORCE blocks | assistant turns | cost USD |
|---|---|---|---|---|---|
| off-1 | no pack (the kit's actual state) | none | 0 | 7 | 0.093 |
| off-2 | no pack | none | 0 | 6 | 0.083 |
| on-1 | pack, first build of the gate | adversarial-verify, scope-fence on the trigger; then adversarial-verify, plan-gate, scope-fence after a block | 1, **false** (see §6) | 45, hit `--max-turns`, exit 1 | 0.364 |
| on-2 | pack, first build of the gate | adversarial-verify, scope-fence on the trigger; adversarial-verify again after a block | 1, **false** | 19 | 0.170 |
| on-triv-1 | pack, "what's 15% of 80?" | none | 0 | 1 ("15% of 80 is **12**.") | 0.055 |
| on-triv-2 | pack, "what time zone is the draft in?" | none | 0 | 4 | 0.071 |
| on-3 | pack, gate fixed | adversarial-verify, scope-fence on the trigger; Stop gate allowed | 0 | 15 | 0.147 |
| on-4 | pack, gate fixed | adversarial-verify, scope-fence on the trigger; Stop gate allowed | 0 | 13 | 0.165 |

Eight runs, 1.15 USD in total (from the result events in `raw/ab/*/out.jsonl`). Tallies are the
driver's (`raw/ab/summary.json`, `summary2.json`), re-read from the stream files, never from recall.

**Against the pre-registered predictions (P2):** OFF 0/2 governor loads — predicted 0/2, **held**.
ON (incident message) 4/4 runs loaded adversarial-verify and scope-fence, every time on the
trigger alone — predicted 2/2, **held** in both batches. Trivia ON 0/2 loads, 0 blocks, direct
one-line answers — predicted 0/2 and no over-fire, **held**. The blocking path: not observed
legitimately live, because the trigger alone produced the load in 4 of 4 runs; it fired twice as a
**false positive** in the first build (the gate mistook a loaded skill's own text for the owner's
prompt), which the harness honoured and the model answered by loading again — so `decision:
"block"` is proven to reach the model, and the fixed gate allowed 2 of 2 compliant runs. The
blocking decision logic itself is proven by the fixture, not by a live run. **Any-regression
check:** the false block was a regression against P2's own wording and blocked acceptance until
fixed and re-run; nothing else regressed (receipt-law self-test 10/10 before and after).

Bound: these are Claude Code CLI sessions inside the same cloud container class, started inside
one scratch project carrying the kit's `CLAUDE.md` verbatim plus the three governors as project
skills. They are not the web-session harness itself. The harness evidence is §3.3.

### 3.3 Observed in this web session (EVIDENCE, 2026-10-13)

Within minutes of `.claude/settings.json` being written, this session's own harness ran the
project hooks: the first `Edit` call returned the plan-gate and scope-fence first-write reminders as
hook context, and a later prompt returned the trigger's "Governance auto-trigger" line. That prompt
was a background-task notification, not an owner message — an over-fire fixed the same hour by
ignoring harness markers in the classifier (fixture case added). So project-scope hooks run in a
single-repository cloud session, by direct observation and not only by documentation.

## 4. Proposed for the kit and the deck (exact text; nothing applied)

### 4.1 Kit `CLAUDE.md` — full replacement (MUST ADD; demoted if the owner prefers the plugin route alone)

```markdown
# fantasy-basketball-2026-27 — a domain-layer project

Governed by the operating doctrine of `nic095layson/claude-core-skills`. The block
below is that doctrine's cloud-safe copy (`instructions/project-doctrine-block.md`
there); `~/.claude/CLAUDE.md` does not exist in cloud containers, so nothing here
depends on it.

Within the governed process, this project's domain rules apply: the 9-cat z-score
engine, the July-2026 projections baseline, and the edit-CSV → rerun →
board-regenerates workflow. Core on top, domain within.

Three domain instances of the general rules (architecture-contract Decision 2 —
these win here):
- Historical analyses state their seasons and run the era check
  (`league_per36.py`) before any conclusion rests on a multi-season window; a
  window inherited from a file's first season is an assumption, named as such.
- Every method choice that will reach the board, the deck, or a work order is
  stated to the owner in one line before the run that uses it.
- A question about the board's method gets an assessment and the decision
  options; a candidate (WO-5b class) is built only on an owner go.

<paste the block from claude-core-skills/instructions/project-doctrine-block.md
between its ---- BEGIN BLOCK ---- / ---- END BLOCK ---- markers here>
```

### 4.2 Kit and deck enforcement pack (MUST ADD for single-repo sessions)

Copy from this library into each repo, unchanged: `hooks/govclass.py`,
`hooks/governance-trigger.py`, `hooks/governance-enforce.py`, `hooks/session-doctrine.sh`,
`hooks/plan-gate-first-write-reminder.sh`, `hooks/scope-fence-reminder.sh`,
`hooks/receipt-law-stop-gate.sh`, `hooks/selftest-governance-classify.py`,
`hooks/selftest-receipt-law.sh`, and `.claude/settings.json`. Run both self-tests. Verify in a fresh
session per install-and-surfaces Runbook 4 step 5. The deck's existing `.claude/skills/` is untouched.

### 4.3 Deck `LESSONS.md` entry (HIGHLY RECOMMEND; the incident's D-SF-2 default was to leave it to this analysis)

```markdown
## 2026-10-13 — Scope-fence breach on the career-averages question (kit after-report of the same date)

24. **A `CLAUDE.md` that says the governors run is a promise; the mechanism has
    to exist on the surface.** Three weeks of cloud sessions loaded no governor:
    `~/.claude/CLAUDE.md` is absent in cloud containers, this repo and the kit had no
    `.claude/settings.json`, and the library's enforcement hooks were wired nowhere.
    The 20-season window chose itself from a file's first season and was never
    stated; a WO-5b candidate was built to answer a question. Countermeasures live
    in `claude-core-skills` (`results/2026-10-13/gauntlet-fortification/`): the
    project enforcement pack, the doctrine block, and three rules now written into
    plan-gate and scope-fence. Portable rule: before trusting "governed", run
    `test -f ~/.claude/CLAUDE.md && cat .claude/settings.json` on the surface.
```

### 4.4 Multi-repository cloud sessions — the plugin route (HIGHLY RECOMMEND; not built)

The settings documentation (fetched 2026-10-13): *"In an Anthropic-hosted environment, a session
with several repositories starts above the clones and reads only the `enabledPlugins` and
`extraKnownMarketplaces` keys from each repository's `.claude/settings.json`, not permission
rules, hooks, `env`, or other keys."* The incident session had both the kit and the deck. So the
pack in §4.2 covers single-repo sessions only. What the documentation does say those sessions read
is the plugin keys — and plugins carry hooks (`hooks/hooks.json`, paths through
`${CLAUDE_PLUGIN_ROOT}`; plugin manifest reference, fetched 2026-10-13). Proposed: package the
seven hooks as a plugin in this library (`plugin/governance/.claude-plugin/plugin.json` +
`hooks/hooks.json`), publish this repository as its marketplace, and add to each repo's settings
`"extraKnownMarketplaces"` + `"enabledPlugins"`. **Demoted to NOT NEEDED if** a live multi-repo
session is observed running repo-settings hooks after all; **cannot be verified from this
session**, which has one repository attached.

## 5. The eight questions

| # | question | answer | tier |
|---|---|---|---|
| 1 | Loading without the keyword | The Stop gate is the only lever that *forces* a load (3/3 vs 0/3 in 2026-07-15; §3.2 here); the trigger is advisory and classifier-gated so trivia is never injected into; a `CLAUDE.md` instruction alone was the incident's state. A per-turn "Fired" line is a receipt and receipts confabulate (INC-13, 4 vs 0). Description edits did not move this class (DEAD-3). | pack: MUST ADD · Fired line: NOT NEEDED · description edits: NOT NEEDED |
| 2 | Doctrine on the cloud surface | The repo's own `CLAUDE.md` (read, and re-read after compaction) plus repo `.claude/settings.json` hooks (read in single-repo sessions). Skills sync covers only the five synced governors. | doctrine block: MUST ADD |
| 3 | Compaction | A `SessionStart` hook with matcher `compact` is the documented re-injection route; `PreCompact` can block or run a command but adds no context, and summaries are not in the owner's control. Built: the protocol (open objections listed; disputed stays disputed; reload governors; reminders re-armed). | F3: MUST ADD |
| 4 | Method choices inside the fence | Both: plan-gate §3 (a parameter inherited from a file is an assumption, stated before the run) and the kit's `CLAUDE.md` domain instance (seasons + era check first). | F6 + §4.1: HIGHLY RECOMMEND |
| 5 | Dry runs and stated requirements | A scratch dry run is a fix under scope-fence (now §2); a mid-turn "X is critical" is a requirement, not authorization (now §4); the trigger's `requirement` class says so at the moment it arrives. The house rule is written in three places: scope-fence, the doctrine block, the kit proposal. | F6: HIGHLY RECOMMEND |
| 6 | Long silent stretches | plan-gate §5 phase-boundary line; the dispute trigger text asks for the window in one line before the run. Checking it: not from the session log (it drops most assistant text); from the owner's screen, and from the plan-gate block the Stop gate now forces into the transcript. | fold-don't-add (folded into plan-gate) |
| 7 | Gauntlet's own gaps | Named firing cannot catch an un-keyworded skip; the Stop gate can and now does (measured). Gauntlet gained the re-attached state. Its trigger evals remain authored, not run. | evals run: NICE TO HAVE |
| 8 | Beyond the governors | (a) the library ledger got INC-2026-10-13-01; the project ledger proposal is §4.3 — two ledgers by design, the skill's `.claude/LESSONS.md` pointer means "the ledger of the repo you are in"; (b) session-only rules are now committed; (c) the session log is not an audit source for owner-visible text (bound, below); (d) found here: the classifier's "draft" over-fire in a fantasy-draft project, and its silence on disputes. | — |

## 6. Surprises and corrections during the work

- **The classifier was worse than the incident assumed.** The report treated "hooks unwired" as
  the gap; measured, the wired classifier would also have been silent on 3 of 4 messages and noisy
  on "draft". Both fixed and pinned before any live run.
- **A documentation fact changed the design.** Multi-repo cloud sessions do not read repo hooks.
  Recorded as the open part of the ledger entry rather than absorbed.
- **The harness fired the trigger on a task notification** (§3.3). Fixed by ignoring harness
  markers; a fixture case pins it.
- **Two edit misses of my own**: a `sed` and then a Python replacement each failed to match the
  pattern they targeted; the fixture caught both before the live runs (the driver is gated on it).
- **The Stop gate's first build blocked compliant runs.** The harness records loaded skill text and
  hook feedback as user entries marked `isMeta`; the gate took the latest such entry as the owner's
  prompt, so the Skill calls fell before it and were not counted. Diagnosed from the run's own
  transcript, fixed by skipping harness-marked entries, pinned by two fixture cases that reproduce
  the exact shape, and re-run (on-3, on-4: 0 false blocks).
- **Un-inheriting `CLAUDE_CODE_SESSION_ID` did not change the reported session id** in the reruns
  (ledger INC-14 names that variable). Each run still wrote its own transcript under its own project
  directory, so the gate read the right file and the result stands. Flagged for the ledger's owner;
  not chased here (scope-fence).

## 7. Bounds

**Out of scope by design**
- The kit and deck repositories: proposed text only (no push access; the prompt's fence).
- Running `evals/gauntlet.json` and the governors' trigger evals (NICE TO HAVE above).
- The content of the 10/12 dissertation answer and the WO-5 decision (a)/(b)/(c).
- Building the plugin route (§4.4).

**In scope and unverified**
- Whether the web-session harness runs project hooks in a **multi-repository** session:
  `UNVERIFIABLE` from here (this session has one repository); the documentation says it does not.
- Behavioural value of the governor body edits (F6): `NOT-ATTEMPTED` by design — a data-analysis
  fixture A/B is the next experiment; the edits are labelled UNMEASURED in their provenance.
- Whether `SessionStart`'s `additionalContext` on `compact` reaches the model as well as plain
  stdout does: `ATTEMPTED-FAILED` to observe live (no compaction occurred in this session); the
  documentation names both forms, and the hook emits the JSON form.
- Why the incident session's log kept text for only a minority of assistant messages:
  `NOT-ATTEMPTED` (inherited bound from the incident report).

## 8. Decision sheet (owner disposes)

| id | decision | default if silent |
|---|---|---|
| D-GF-1 | Merge PR 24 (this fortification together with the Rules of Engagement work it shares a branch with), or ask for the governance commits to be split onto their own branch first | unmerged; nothing changes |
| D-GF-2 | Apply §4.1 + §4.2 to the kit (CLAUDE.md replacement + pack) — (a) I open a kit PR if given push access; (b) you paste | (b) |
| D-GF-3 | Apply §4.2 to the deck | not applied |
| D-GF-4 | Add §4.3 to the deck `LESSONS.md` | not added |
| D-GF-5 | Build the plugin route for multi-repo cloud sessions (§4.4) | not built |
| D-GF-6 | Run the pre-registered behavioural A/B for the F6 body edits | not run; edits stay UNMEASURED |
| D-GF-7 | A1: keep the applied-on-branch reading of your instruction, or revert to analysis-only | keep (nothing merges without you) |

## 9. Provenance

- **Produced by:** this Claude Code cloud session, 2026-10-13. Documentation facts: one delegated
  `claude-code-guide` agent (12 fetches), re-verified by four fetches of this session.
- **Sources:** the incident report and its evidence folder; the three repositories at the commits
  above; `~/.claude/` of this container; the documentation pages in `raw/docs-quotes-2026-10-13.md`.
- **Re-verify:** `python3 hooks/selftest-governance-classify.py`; `bash
  .claude/skills/diagnostics-and-tooling/scripts/guard_essentials.sh`; re-run the A/B driver
  (`raw/ab/driver.sh <dir>`); `test -f ~/.claude/CLAUDE.md` on any new surface.
- **Fired:** gauntlet · plan-gate (loaded; full block emitted pre-work, as its own message) ·
  scope-fence (loaded) · after-report (loaded) · delegation-discipline (loaded before the docs
  agent) · architecture-contract (loaded before editing governors) · skill-creator and
  session-start-hook (loaded; used for mechanics) · adversarial-verify (loaded before delivery; its six-step pass is the Criteria / Refutation / Gaps block in the delivery message).

## In plain language

Your other session broke two rules because nothing was there to remind it of them. The file that
is supposed to carry the rules into every session does not exist on the web version of Claude
Code, and the hooks that can force a rule to load were written months ago but never switched on
anywhere. Even if they had been, the part that recognizes "this is serious work" would not have
recognized your own messages that night.

This change switches the hooks on inside the governing repository, fixes the recognizer so it
responds to disagreements and questions the way it responds to "build me X", teaches it to ignore
the word "draft" in a fantasy-draft project, adds a reminder that runs every time the conversation
is compressed, and writes the three rules you had to state by hand into the rulebooks. I tested it
on your exact message from that night: without the pack, neither run opened a rule-book; with it, all four runs opened two rule-books before answering, and the two trivia questions got plain one-line answers with nothing loaded. The test also caught a bug in my own gate (it blocked a run that had complied), which is fixed and now covered by a test.

One honest limit: when a web session has two repositories attached at once, which is how that
session ran, Claude Code does not read hooks from either repository. The fix for that case is a
plugin, and it is described but not built. Nothing is merged until you say so.

---

## Correction and application record (2026-10-13, later the same day)

**Correction to §4.4 (the plugin route).** The settings-page sentence quoted in §4.4 continues:
"The marketplaces and plugins those two keys declare still don't load in a cloud session." The
cloud-environments page's carry-over table says the same ("Plugins and marketplaces declared in your
repo's `.claude/settings.json` — No"), and the plugin loading reference gives the reason: adding a
repository-declared marketplace needs the workspace trust dialog, which a cloud session never shows
(all three pages re-read 2026-10-13). §4.4's proposal — enable the plugin from each repository's
settings — rested on the first sentence alone and is withdrawn. What caught it: re-fetching the page
for the exact JSON shape before building, one sentence further on the same page. Runbook 4 (steps
6–7), `hooks/README.md`, `README.md` and the ledger entry carry the correction.

**What replaces it — the account route.** A plugin enabled on claude.ai (Customize → Plugins → Add →
Upload plugin; `.plugin` or `.zip` holding one `.claude-plugin/plugin.json`) "downloads as a synced
plugin the next time you start a session signed in to the same account" (claude.com plugins page);
in terminal sessions a synced plugin's hooks load (loading reference). EVIDENCE from this container:
`claude plugin list` shows a claude.ai-synced plugin `loaded` in this cloud session, and the
governors sit under `~/.claude/skills/synced/`. INFERENCE: a synced plugin's hooks therefore reach
cloud sessions too — **not yet observed** (the synced plugin at hand carries no hooks).

**Built (D-GF-5, re-specified).** `plugin/core-governance/` + `.claude-plugin/marketplace.json`
(commit `14eabf7` and the follow-up on this branch). `claude plugin validate --strict` passes for
both. Scripts are byte-identical copies of `hooks/` (guard section 9). Wrapper
`run-unless-project-wired.sh` yields only in a local session whose project hooks key wires the same
hook; in a cloud session it always runs (the verifier found the first rule could silence both
copies in a several-repository cloud session; pinned by `selftest-wrapper.sh`, 9/9).
`--plugin-dir` smoke, one headless run per arm (mechanism check, N=1, stated before the run):
incident message → trigger context once, `adversarial-verify` + `scope-fence` loaded, no block,
0.28 USD; "what time zone is the draft in?" → nothing fired, direct answer, 0.08 USD. Attribution of
the fired hooks to the plugin comes from a separate `--debug-file` run, not from the smoke stream,
which names events but not commands (`raw/plugin-smoke/attribution-debug-2026-10-13.txt`:
"Registered 6 hooks", no project settings file named).

**Applied (D-GF-2, D-GF-3, D-GF-4).** Kit: branch `claude/governance-pack-2026-10-13`, draft
PR 105 (`CLAUDE.md` per §4.1 with the block between its markers, the nine hooks, settings).
Deck: same branch name, draft PR 106 (pack, new `CLAUDE.md` with the block, `LESSONS.md` lesson 24
per §4.3, `.claude/skills/` untouched). Both branches based on their `main` tips of the day, one
commit each. Verification: a Workflow applied each in parallel and ran independent read-only
refuters — kit **PASS, 0 defects, 9 checks**; the deck refuter **did not run** (the account's
session limit was hit before it started), so the authoring session ran the same checks itself
(byte-identity, modes, both self-tests, append-only ledger diff, untouched skills, base, trailers,
no CRLF — all PASS). The plugin refuter returned **FAIL** on three findings, each dispositioned
above or below. No kit/deck setting declares plugin keys (inert on cloud by the documentation).

**Verifier findings not fixed here.**
- `hooks/plan-gate-first-write-reminder.sh:14` and `hooks/scope-fence-reminder.sh:9` call
  `/usr/bin/jq` by absolute path (`session-doctrine.sh` uses `jq` from PATH). On a host without
  `/usr/bin/jq`, `sid` falls back to `nosession` and the once-per-session sentinel becomes
  machine-wide. Present on this host; pre-existing in `hooks/` since 2026-07-12; inherited
  byte-for-byte by the plugin, the kit and the deck. Outside this task's fence; one-word fix,
  then re-copy to all three. **D-GF-8 below.**
- Governance hooks would run twice in a one-repository cloud session that carries the pack once
  the plugin is enabled (duplicate trigger line; same Stop verdict twice). Accepted cost of the
  fail-safe rule; a per-session sentinel in `governance-trigger.py` would remove it. **D-GF-9.**

**Delivered to the owner (this session):** `plan-gate.skill`, `scope-fence.skill`,
`gauntlet.skill` (each exactly `<name>/SKILL.md`, byte-identical to this branch) and
`core-governance.plugin` (the plugin directory zipped; one `.claude-plugin/plugin.json`).

**Decision sheet, continued**

| id | decision | default if silent |
|---|---|---|
| D-GF-8 | Fix the `/usr/bin/jq` path in the two reminders (PATH `jq`), then re-copy to plugin, kit, deck | not fixed; works wherever `/usr/bin/jq` exists |
| D-GF-9 | De-duplicate the trigger when plugin and pack both run (per-session sentinel) | not built; duplicate line accepted |
| D-GF-10 | Upload `core-governance.plugin` to the claude.ai account, then observe one several-repository cloud session (`claude plugin list`, a disputed question) and record the result against INC-2026-10-13-01 | the ledger entry stays OPEN |
| D-GF-11 | Merge PR 105 (kit) and PR 106 (deck), separately from PR 24 | unmerged; nothing changes in those repos |

**Applied pack exercised in the clones (added after the PRs opened, 2026-10-13).** One headless run
per clone at the PR heads, incident message, nothing present but the committed files
(`raw/applied-smoke/`): kit — trigger context once, `adversarial-verify` + `scope-fence` loaded, no
block, run ended on the 12-turn cap (0.52 USD); deck — trigger once, same two loads, no block,
assessment delivered ("I partly agree with you. Career averages enter the projections only in a
narrow way…", 0.25 USD). Three hook events each (one UserPromptSubmit, two Stop), as the settings
wire. N=1 per clone; a mechanism check.
