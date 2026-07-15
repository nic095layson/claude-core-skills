#!/usr/bin/env bash
# migrate_users_orders.sh — move users + orders to the new DB.
# Hardened for a single production run: no inline secrets, fails loudly,
# safe to re-run after a failed attempt, verified before the status flip.
#
# Usage:
#   SRC_DB_URL='postgresql://app:***@localhost:5432/legacy' \
#   DST_DB_URL='postgresql://app:***@newdb.internal:5432/app' \
#   CONFIRM=yes ./migrate_users_orders.sh
#
# Assumptions this script makes (confirm before running — see A1-A3 in the
# chat this came from):
#   A1. users.id / orders.id are the serial/identity primary keys.
#   A2. It's fine for the final UPDATE to mark ALL rows in DST.users as
#       migrated (this matches the original script's behavior; if DST.users
#       can have pre-existing rows that should NOT be touched, scope the
#       WHERE clause below before running).
#   A3. This runs once, interactively, by a human — not from CI/cron.

set -euo pipefail

: "${SRC_DB_URL:?Set SRC_DB_URL, e.g. postgresql://user:pass@host:5432/legacy}"
: "${DST_DB_URL:?Set DST_DB_URL, e.g. postgresql://user:pass@host:5432/app}"

if [[ "${CONFIRM:-}" != "yes" ]]; then
  echo "Refusing to run against a production database without CONFIRM=yes." >&2
  echo "Set CONFIRM=yes once you've confirmed A1-A3 above." >&2
  exit 1
fi

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*" >&2; }

DUMP_FILE="$(mktemp /tmp/migrate_users_orders.XXXXXX.sql)"
chmod 600 "$DUMP_FILE"
cleanup() { rm -f "$DUMP_FILE"; }
trap cleanup EXIT

log "starting migration: users, orders"

# --- pre-flight: connectivity + source row counts ---
psql "$SRC_DB_URL" -c "select 1" >/dev/null
psql "$DST_DB_URL" -c "select 1" >/dev/null

SRC_USERS=$(psql "$SRC_DB_URL" -tA -c "select count(*) from users")
SRC_ORDERS=$(psql "$SRC_DB_URL" -tA -c "select count(*) from orders")
log "source counts: users=$SRC_USERS orders=$SRC_ORDERS"

# --- idempotent re-entry: the dump/load below is wrapped in one transaction,
# so a mid-load failure rolls back cleanly and a retry just redoes it. But if
# an EARLIER run's transaction already committed and a LATER step (sequence
# resync, verification) is what failed, naively redoing the load would hit
# duplicate-key errors. Detect that case and skip straight past it.
DST_USERS_PRECHECK=$(psql "$DST_DB_URL" -tA -c "select count(*) from users")
DST_ORDERS_PRECHECK=$(psql "$DST_DB_URL" -tA -c "select count(*) from orders")

if (( DST_USERS_PRECHECK >= SRC_USERS && DST_ORDERS_PRECHECK >= SRC_ORDERS && SRC_USERS > 0 )); then
  log "destination already has >= source row counts ($DST_USERS_PRECHECK/$DST_ORDERS_PRECHECK vs $SRC_USERS/$SRC_ORDERS) — dump/load looks already done, skipping to sequence resync"
else
  # --- dump (data only), private permissions, cleaned up on exit via trap ---
  pg_dump "$SRC_DB_URL" -t users -t orders --data-only --no-owner > "$DUMP_FILE"
  log "dump complete ($(wc -l < "$DUMP_FILE") lines)"

  # --- destination: schema change + data load in ONE transaction, idempotent DDL ---
  psql "$DST_DB_URL" -v ON_ERROR_STOP=1 -1 <<SQL
ALTER TABLE orders ADD COLUMN IF NOT EXISTS migrated_at TIMESTAMP NOT NULL DEFAULT now();
CREATE INDEX IF NOT EXISTS idx_orders_migrated ON orders(migrated_at);
\i $DUMP_FILE
SQL
  log "schema change + data load committed as one transaction"
fi

# --- resync id sequences so future inserts don't collide with migrated rows ---
# (assumes A1: the PK column is named "id"; safe no-op if there's no sequence)
for tbl in users orders; do
  seq=$(psql "$DST_DB_URL" -tA -c "select pg_get_serial_sequence('$tbl','id')")
  if [[ -n "$seq" ]]; then
    psql "$DST_DB_URL" -v ON_ERROR_STOP=1 -c \
      "select setval('$seq', (select coalesce(max(id),1) from $tbl))" >/dev/null
    log "resynced sequence for $tbl ($seq)"
  else
    log "no serial/identity sequence found for $tbl.id — skipped resync"
  fi
done

# --- verify before flipping status — abort rather than mark bad data "migrated" ---
DST_USERS=$(psql "$DST_DB_URL" -tA -c "select count(*) from users")
DST_ORDERS=$(psql "$DST_DB_URL" -tA -c "select count(*) from orders")
log "destination counts: users=$DST_USERS orders=$DST_ORDERS"

if (( DST_USERS < SRC_USERS || DST_ORDERS < SRC_ORDERS )); then
  log "ABORT: destination row counts are lower than source — NOT flipping status"
  log "  users:  src=$SRC_USERS dst=$DST_USERS"
  log "  orders: src=$SRC_ORDERS dst=$DST_ORDERS"
  exit 1
fi

# Assuming A2 — see header. Narrow this WHERE clause if DST.users can have
# pre-existing rows that should not be marked migrated.
psql "$DST_DB_URL" -v ON_ERROR_STOP=1 -c "UPDATE users SET status = 'migrated';"

log "migration done"
