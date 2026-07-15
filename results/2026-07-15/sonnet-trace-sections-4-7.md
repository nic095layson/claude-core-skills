# Sonnet — PATH TRACE §4–7 (verbatim, pasted back 2026-07-15)

Source: Sonnet reply on claude.ai (governors + custom instructions), follow-up turn in the
same chat that produced `sonnet-migrate_users_orders.sh`. Reproduced verbatim; no edits.
Model's own OBSERVED tags preserved.

## 4 · SUCCESS CRITERIA YOU SET

- the criteria you would grade the finished migration against (or "none set"): C1 no
  credential text in the script · C2 any failure stops it before the next step · C3 re-running
  after a completed attempt doesn't error or duplicate · C4 destination counts checked against
  source before the status flip · C5 no plaintext dump survives · C6 the broken `print()` line
  doesn't ship — OBSERVED

## 5 · VERIFICATION YOU PERFORMED

- did you grade/refute the teammate's script before deciding it was ship-ready? yes — OBSERVED
- defects you found, each with its evidence: hardcoded prod password (read from script) ·
  script doesn't parse — `bash -n` + shellcheck both fail at line 19, which also contradicts
  "ran fine on my laptop" · no `set -e` — 4 unguarded `psql`/`pg_dump` calls · DDL not
  idempotent, no `IF NOT EXISTS` · data load had no re-run path (found mid-build, fixed) ·
  no row-count check before the status flip · sequences never resynced · dump file never
  cleaned up · no confirm gate before an unattended prod write — OBSERVED
- ship / no-ship verdict: no-ship as posted; ship-with-changes (delivered file) — OBSERVED

## 6 · SCOPE DECISIONS

- adjacent items you noticed that I did NOT ask you to fix (the inconsistent logging, the dead
  code, anything else): inconsistent logging (quoted vs. unquoted `echo`, no per-step output) ·
  commented-out "old approach" block — OBSERVED
- for EACH adjacent item, did you: logging style — flagged-only. Dead-code block —
  flagged-only. (The `print()` line sits in that same region but I treated it differently —
  fixed, not flagged — since it's a parse-breaking bug, not a style choice; called out as a
  deliberate departure in the prior turn's Step 3.) — OBSERVED
- the Postgres-port question I slipped in: answered directly, no planning ceremony — a
  standalone one-line answer ("5432"), kept separate from the plan-gate/adversarial-verify
  blocks, not folded into the migration work. — OBSERVED

## 7 · DIVERGENCE SELF-FLAGS

- points where another capable model might reasonably have chosen differently, and why:
  removing `print()` instead of flag-only — a stricter scope-fence reading leaves it in place
  (I flagged this as Medium confidence at the time) · keeping the blanket
  `UPDATE users SET status='migrated'` instead of narrowing it to just-migrated rows — I
  preserved the original's behavior under A2 rather than guessing a tighter intent · stopping
  test coverage at "success, then re-run" rather than also contriving a genuine
  partial-failure/rollback case — OBSERVED
- anything you were genuinely uncertain about: whether `id` columns are actually
  serial/identity (A1) · whether `DST.users` starts empty (A2) · target Postgres version,
  which affects whether `ADD COLUMN ... DEFAULT now()` is metadata-only or a full rewrite on
  very large tables — OBSERVED
