# Acme Orders API

A small service that exposes order data over HTTP.

## Running

The service listens on **port 8080**. Once it's running, point your client at
`http://localhost:8080` and hit `/health` for a liveness check.

## Deploy

Deploys run the release phase, then start the server with `node server.js`.
