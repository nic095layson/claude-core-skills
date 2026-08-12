# Full-tree npm license audit — 12 seed packages (2026-08-11)

**Owner request (near verbatim):** the owner shared a team-bound "dependency
licence audit" draft that checked 3 of 12 named packages (axios, lodash,
express) and guessed the remaining 9 (chalk, commander, dayjs, zod, pino,
undici, ws, yargs, nanoid) were "almost certainly MIT or ISC," then verdicted
"no copyleft risk, safe to proceed with the closed-source release." Asked to
adversarial-verify the draft first; that pass (this session, same day) graded
it **not ready to ship** — the verdict outran its evidence twice over: 9 of 12
top-level licenses were unverified when written, and even fully verified, the
draft only covered 12 top-level packages, not "the dependency tree" its own
verdict claimed to describe. The owner then asked to "run license checker
under full dependency tree" to close that second gap, clarified (this
session) that no real project exists for this — audit a synthetic install of
the 12 named packages — and asked the result saved to this repo.

**What was analyzed:** the full transitive runtime-dependency graph of
`axios`, `lodash`, `express`, `chalk`, `commander`, `dayjs`, `zod`, `pino`,
`undici`, `ws`, `yargs`, `nanoid`, each resolved from its npm `latest`
dist-tag as of 2026-08-11, walked to every transitive `dependencies` entry
(devDependencies, peerDependencies, and optionalDependencies excluded — see
Bounds).

**Method:** node/npm/Homebrew are not installed on this machine (`which node
npm npx brew` — all not found, this session), so the literal `license-checker`
CLI could not run. Substituted a registry-API equivalent: `audit.py` (this
directory) recursively fetches each package's manifest from
`registry.npmjs.org`, records its `license` field, and walks its declared
`dependencies` — the same data `license-checker` reads from an installed
`node_modules`, without requiring an install. Full run output: `full_tree_result.json`
(this directory, committed raw per the evidence rules — not summarized away).
Cross-checked: the top-level license claims independently match the 12
registry lookups already run in the adversarial-verify pass earlier the same
session (all 12 == MIT there too).

**Headline:** the full transitive tree resolves to **115 unique packages, 0
resolution errors, 0 copyleft licenses**. Breakdown: 105 MIT, 9 ISC, 1
BSD-3-Clause — all permissive, all compatible with closed-source
redistribution. This closes the specific gap the adversarial-verify pass
flagged (draft covered 12 packages, claimed "the dependency tree"); it does
**not** by itself clear the original draft for shipping, because the draft
still needs rewriting to state real scope and method (see Next steps).

## Evidence

**Full breakdown** (EVIDENCE — `full_tree_result.json`, this session):

| License | Count |
|---|---|
| MIT | 105 |
| ISC | 9 |
| BSD-3-Clause | 1 |

**The 10 non-MIT packages, named** (EVIDENCE — same file):

| Package | Version | License | Pulled in by |
|---|---|---|---|
| cliui | 9.0.1 | ISC | yargs@18.1.0 |
| get-caller-file | 2.0.5 | ISC | yargs@18.1.0 |
| inherits | 2.0.4 | ISC | http-errors@2.0.0 |
| once | 1.4.0 | ISC | express@5.2.1 |
| qs | 6.14.0 | BSD-3-Clause | body-parser@2.2.1, express@5.2.1 |
| setprototypeof | 1.2.0 | ISC | http-errors@2.0.0 |
| split2 | 4.0.0 | ISC | pino-abstract-transport@3.0.0 |
| wrappy | 1.0.2 | ISC | once@1.4.0 |
| y18n | 5.0.5 | ISC | yargs@18.1.0 |
| yargs-parser | 22.0.0 | ISC | yargs@18.1.0 |

ISC and BSD-3-Clause are both OSI-approved permissive licenses, materially
equivalent to MIT for closed-source redistribution purposes (no copyleft,
no source-disclosure obligation) — INFERENCE, standard open-source-license
reading, not a substitute for legal sign-off on a real release.

**Zero errors** (EVIDENCE — `full_tree_result.json`, `"errors": []`): every
one of the 115 packages resolved a license field on first fetch; none hit the
script's `FETCH_ERROR` / `NO_VERSIONS` / safety-cap paths.

## Bounds

**Out of scope by design:**
- devDependencies of any package in the tree — correct exclusion, since dev
  deps of a dependency never ship in a consuming closed-source build.
- peerDependencies (e.g. `ws`'s optional `bufferutil`/`utf-8-validate` peers,
  confirmed via direct registry fetch this session) — not auto-installed by
  npm and not part of what ships unless a consumer explicitly adds them.
- Legal review of what "permissive" requires for this specific release (attribution
  files, NOTICE bundling) — this is a license census, not legal advice.

**In scope and unverified** (should be resolved before this backs a real
release decision, not this audit's job to close):
- **Version drift.** Every package was resolved at its `latest` dist-tag on
  2026-08-11, not against a real project's lockfile. A real release's
  `package-lock.json` may pin different (older) versions with different
  license fields — DID NOT CHECK, because no real project/lockfile exists for
  this synthetic audit (owner-confirmed, this session).
- **Resolver fidelity.** `audit.py`'s range resolution (`best_version()`) is a
  rough regex-based approximation, not npm's real semver/hoisting/dedupe
  algorithm — flagged in the script's own docstring. For a tree this shallow
  and this permissively-licensed, the practical risk of a wrong resolution
  flipping the license verdict is low, but it is INFERENCE, not a guarantee.
  A real `npm install && npx license-checker` run against an actual lockfile
  would be the load-bearing version of this check.
- **Registry metadata trust.** The `license` field is self-reported by each
  package's publisher at publish time, not independently audited by npm or by
  this script — true of any registry-based check, including the literal
  `license-checker` tool.

## Next steps (owner decisions)

1. **Install a real Node/npm toolchain** (e.g. `brew install node`) if this
   machine needs to run literal `license-checker` / `npm audit` against real
   projects going forward — not done here since the request was scoped to
   this one audit and installing a language runtime is a bigger, less
   reversible change than the task asked for.
2. **Rewrite the original draft** using this report's numbers: swap the
   9-package guess for verified data, replace "the dependency tree" with
   accurate scope language ("12 seed packages and their 115 resolved
   transitive runtime dependencies, checked 2026-08-11"), and drop the
   now-redundant hedge language the adversarial-verify pass flagged.
3. **If this ever backs a real release** (not a synthetic exercise): re-run
   against the actual project's `package-lock.json` with the real
   `license-checker` CLI once Node is available, since lockfile-pinned
   versions can differ from today's `latest` resolutions.

## Provenance

- Session: this conversation, 2026-08-11, following an adversarial-verify
  pass on the owner's original draft (same session, no separate artifact
  saved — the verdict is summarized in the Owner request line above).
- Tooling: `audit.py` (this directory, ~100 lines, Python 3 stdlib only, no
  third-party dependencies); raw output `full_tree_result.json` (this
  directory).
- Sources: `registry.npmjs.org` manifest endpoints, fetched live 2026-08-11.
- Re-verify: `python3 audit.py` from this directory reproduces the run
  (network-dependent; package versions may have advanced past 2026-08-11 by
  the time of re-run, which is expected and not a defect in this report).
