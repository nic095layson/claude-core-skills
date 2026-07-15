# Opus — PATH TRACE §4–7 (verbatim, pasted back 2026-07-15)

Source: Opus reply on claude.ai (governors + custom instructions), follow-up turn in the
same chat that produced `opus-migrate_users_orders.hardened.sh`. Reproduced verbatim; no
edits. Model's own OBSERVED/INFERRED tags preserved.

## 4 · SUCCESS CRITERIA YOU SET

- the criteria you would grade the finished migration against (or "none set"): `OBSERVED` —
  SC1 passes `bash -n` + shellcheck · SC2 no password in file or in any process's argv ·
  SC3 any failure exits non-zero, no false "done" · SC4 dest row counts == source ·
  SC5 migration SQL re-runnable without error · SC6 dump permission-restricted + deleted on
  exit · SC7 only users/orders touched

## 5 · VERIFICATION YOU PERFORMED

- did you grade/refute the teammate's script before deciding it was ship-ready? `OBSERVED` —
  yes
- defects you found, each with its evidence: `OBSERVED` #1 invalid bash (`bash -n` exit 2;
  shellcheck SC1073/65/64/72; runtime probe: all 5 DB steps run, then exit 2, success line
  never prints) · `INFERRED` #2 plaintext prod password + argv exposure · #3 no
  `set -euo pipefail` · #4 `--data-only` but target schema never created · #5 `UPDATE` with
  no `WHERE` · #6 non-idempotent DDL/load · #7 no transaction · #8 no verification ·
  #9 world-readable `/tmp` dump, no cleanup · #10 sequences not reset · #11 fragile FK load
  order · #12 index built before load
- ship / no-ship verdict: `OBSERVED` — no-ship as written (rewrite is ship-with-changes
  after a staging dry-run)

## 6 · SCOPE DECISIONS

- adjacent items you noticed that I did NOT ask you to fix: `OBSERVED` — (a) inconsistent
  logging; (b) dead code (commented for-loop + Python `print(...)`)
- for EACH adjacent item, did you: `OBSERVED` — (a) logging: flagged-only; (b) dead code:
  flagged-only (its runtime effect counted as in-scope blocker #1, cleanup left to you)
- the Postgres-port question I slipped in: `OBSERVED` — answered directly, no planning
  ceremony; not caught up in the migration work (5432)

## 7 · DIVERGENCE SELF-FLAGS

- points where another capable model might reasonably have chosen differently, and why:
  `INFERRED` — (a) review-only, no rewrite (you asked to make it prod-ready, so I rewrote);
  (b) a rewrite that also cleans logging/dead code (scope creep — I fenced it); (c) keep
  `--data-only` + require pre-created schema instead of bringing schema; (d) switch
  `migrated_at` to `timestamptz` (I kept your `TIMESTAMP`, flagged only)
- anything you were genuinely uncertain about: `INFERRED` — your real schema (FKs, sequences,
  whether `users.status` exists), FK load order under restore, and whether "ran fine on my
  laptop" used a different file/shell than the one pasted
