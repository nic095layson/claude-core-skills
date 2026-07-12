# Deployment Notes

## Database

We run **Postgres 14** in production. Connection string is provided via the
`DATABASE_URL` environment variable.

## Migrations

Migrations are applied on deploy via the release phase.
