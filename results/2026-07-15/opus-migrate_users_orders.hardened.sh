#!/usr/bin/env bash
#
# migrate_users_orders.sh — migrate `users` + `orders` from legacy -> new Postgres DB.
# HARDENED REVIEW DRAFT — do NOT run blind against prod. Dry-run in staging first.
#
# Auth: NO password lives in this file. Put credentials in ~/.pgpass (chmod 600):
#     host:port:dbname:user:password
# Connection info (no password) is passed via env vars set OUTSIDE this script:
#     export SRC_CONN="host=legacy.internal port=5432 dbname=legacy user=app"
#     export DST_CONN="host=newdb.internal  port=5432 dbname=app    user=app"
#
set -euo pipefail

# --- config / guards -------------------------------------------------------
: "${SRC_CONN:?set SRC_CONN (libpq keyword=value conninfo, no password)}"
: "${DST_CONN:?set DST_CONN (libpq keyword=value conninfo, no password)}"
TABLES=(users orders)

log() { printf '%s  %s\n' "$(date -u +%FT%TZ)" "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }

# Refuse to mutate the target unless a human re-types its dbname.
DST_DB="$(sed -n 's/.*dbname=\([^ ]*\).*/\1/p' <<<"$DST_CONN")"
log "target: ${DST_CONN}"
read -r -p "Type the target dbname (${DST_DB}) to proceed: " CONFIRM
[[ "$CONFIRM" == "$DST_DB" ]] || die "confirmation did not match; aborting."

# Secure, always-cleaned temp workspace (dump holds all user/order data).
umask 077
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
DUMP="$WORK/dump.fc"

# --- 1. dump schema+data for the two tables (custom format => ordered restore,
#        brings sequences + constraints; NOT --data-only, so target need not
#        be pre-created). ----------------------------------------------------
log "dumping ${TABLES[*]} from source..."
tbl_args=(); for t in "${TABLES[@]}"; do tbl_args+=(-t "$t"); done
pg_dump "$SRC_CONN" "${tbl_args[@]}" \
  --format=custom --no-owner --no-privileges --file="$DUMP"

# --- 2. restore into target in ONE transaction (all-or-nothing) ------------
log "restoring into target (single transaction)..."
pg_restore --dbname="$DST_CONN" \
  --single-transaction --exit-on-error --no-owner --no-privileges "$DUMP"

# --- 3. migration-specific changes: idempotent, single transaction ---------
log "applying migration-specific changes..."
psql "$DST_CONN" --set ON_ERROR_STOP=1 --single-transaction <<'SQL'
ALTER TABLE orders ADD COLUMN IF NOT EXISTS migrated_at TIMESTAMP NOT NULL DEFAULT now();
CREATE INDEX IF NOT EXISTS idx_orders_migrated ON orders (migrated_at);   -- after load = faster
UPDATE users SET status = 'migrated' WHERE status IS DISTINCT FROM 'migrated';  -- scoped + idempotent
SQL

# --- 4. reconcile row counts SRC vs DST (a gate, not a printout) -----------
log "reconciling row counts..."
fail=0
for t in "${TABLES[@]}"; do
  s="$(psql "$SRC_CONN" -tAc "select count(*) from $t")"
  d="$(psql "$DST_CONN" -tAc "select count(*) from $t")"
  if [[ "$s" == "$d" ]]; then log "  $t: OK ($s rows)"; else log "  $t: MISMATCH src=$s dst=$d"; fail=1; fi
done
[[ "$fail" -eq 0 ]] || die "row-count reconciliation failed — do not trust this migration."

log "migration completed and reconciled."
