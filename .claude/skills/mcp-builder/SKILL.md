---
name: mcp-builder
description: >-
  Scaffold a working Model Context Protocol (MCP) server from a plain-language description of the
  tools it should expose: extract the tool inventory, pick Python (FastMCP) or TypeScript
  (@modelcontextprotocol/sdk), choose stdio vs streamable-HTTP transport, generate the server,
  smoke-test it with no client attached, and register it with Claude Code or claude.ai. Load when
  the user wants Claude to gain external capabilities as callable tools: "build an MCP server",
  "expose my API/database as tools for Claude", "create a connector/tool server", "wrap this
  service so Claude can call it". Do NOT load for authoring a Claude skill — a skill teaches a
  workflow, an MCP server exposes tools (skill-authoring); installing or packaging skills
  (install-and-surfaces); fixing a misbehaving existing skill (debugging-playbook); or merely
  USING an already-connected MCP server, which needs no skill at all.
---

# MCP Builder

Turn "I want Claude to be able to call X" into a running MCP server. Skills teach
a session HOW to work; MCP servers give it new tools to work WITH. This skill
prevents the two ways scaffolds die: vague tool descriptions the model cannot route
to (it picks tools by description, nothing else), and servers shipped untested.

**Terms.** *Tool* — one callable function; its name, description, and input schema are
ALL a model sees. *Transport* — **stdio** (spawned subprocess) or **streamable HTTP** (a URL).

## Procedure

1. **Extract the tool inventory before writing code.** Table out each tool: name,
   one-line purpose, typed params, return shape. Make implicit tools explicit —
   "let Claude look up orders" usually means both `search_orders(query)` and
   `get_order(order_id)`. Confirm with the user; renaming tools later breaks clients.
2. **Pick a language.** Default Python: `pip3 install mcp` — FastMCP turns
   type-hinted, docstringed functions into tool schemas. TypeScript when the
   service's client library is JS-only: `npm install @modelcontextprotocol/sdk zod`,
   `McpServer` + `registerTool` (assumption 2026-07-13: TS path not run here).
3. **Pick a transport.** stdio for local use and Claude Code (zero network setup);
   streamable HTTP for remote or shared servers (one deploy, many clients — needs auth).
4. **Scaffold** from the template below: 2–3 tools, real docstrings, errors
   returned as data, secrets from env.
5. **Smoke-test with no client attached** — this exact script ran clean against
   the template on 2026-07-13 (mcp 1.28.1). (The block sits indented inside
   this list — dedent it when copying from the raw file.)

   ```python
   import asyncio
   from mcp.shared.memory import create_connected_server_and_client_session
   import server  # the import alone catches syntax and dependency errors

   async def main():
       # In-memory transport: full protocol round-trip, no subprocess, no client app.
       async with create_connected_server_and_client_session(server.mcp._mcp_server) as c:
           tools = await c.list_tools()
           print([t.name for t in tools.tools])  # every tool registered?
           result = await c.call_tool("search_tickets", {"query": "login", "status": "bogus"})
           print(result.content[0].text)  # expect the error-as-data message, not a crash
   asyncio.run(main())
   ```
6. **Register.** Local scope: `claude mcp add ticket-tools -e TICKETS_API_KEY=... -- python3 /abs/path/server.py`.
   Project scope (checked in, team-wide): `claude mcp add -s project ticket-tools -- python3 server.py`
   writes `.mcp.json` at the repo root (verified 2026-07-13):

   ```json
   { "mcpServers": { "ticket-tools": {
         "type": "stdio", "command": "python3", "args": ["server.py"], "env": {} } } }
   ```

   claude.ai is a different path: REMOTE servers only, added as connectors
   (Settings → Connectors) — deploy behind streamable HTTP first (assumption 2026-07-13).
7. **Hand the user the inspector**: `npx -y @modelcontextprotocol/inspector python3 server.py`
   — verified 2026-07-13 (v0.22.0): starts and serves its UI at `localhost:6274`.

## Output format — the template server

```python
"""MCP server exposing a ticket-lookup service as tools for Claude."""
import os

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ticket-tools")
API_BASE = os.environ.get("TICKETS_API_BASE", "https://api.example.com")
AUTH = {"Authorization": f"Bearer {os.environ.get('TICKETS_API_KEY', '')}"}  # env, never code


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Fetch one support ticket by ID (e.g. "TKT-1042"): status, title, assignee.

    Use search_tickets first if you only know keywords, not the ID.
    """
    try:
        r = httpx.get(f"{API_BASE}/tickets/{ticket_id}", headers=AUTH, timeout=10)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"ticket {ticket_id!r} not found (HTTP {e.response.status_code})."
                         " Check the ID or use search_tickets."}
    except httpx.RequestError as e:
        return {"error": f"could not reach ticket API at {API_BASE}: {e}"}


@mcp.tool()
def search_tickets(query: str, status: str = "open", limit: int = 10) -> list[dict]:
    """Search tickets by keyword; status is one of: open, closed, all.

    Returns up to `limit` matches (id, title, status) — pass an id to get_ticket.
    """
    if status not in ("open", "closed", "all"):
        return [{"error": f"invalid status {status!r}: use open, closed, or all"}]
    try:
        r = httpx.get(f"{API_BASE}/tickets", headers=AUTH, timeout=10,
                      params={"q": query, "status": status, "limit": limit})
        r.raise_for_status()
        return r.json()
    except httpx.RequestError as e:
        return [{"error": f"could not reach ticket API: {e}"}]


if __name__ == "__main__":
    mcp.run()  # stdio by default; mcp.run(transport="streamable-http") for remote
```

## Rules

- **Few well-described tools beat many vague ones** — the model routes by
  description alone, the same law that governs this library's skill descriptions.
- **Docstrings and schemas are the contract; write them for a model reader** —
  what comes back, when to prefer a sibling tool. It is the caller's only manual.
- **Return errors as data, never raise** — a raise hands the model a stack trace;
  a returned `{"error": "...use search_tickets"}` says what to do next.
- **No secrets in tool code or checked-in config** — a project-scope `.mcp.json`
  is committed, so its `env` block carries only non-secret config; real keys
  pass via `-e` at local scope or the machine's environment. Server code and
  repo config get checked in; keys must not.

## Edge cases and proportionality

If the capability already exists as a CLI the session can run (`gh`, `psql`, `curl`
against a documented API), no server is needed — a skill teaching the workflow, or
nothing, is enough; wrapping a working CLI in MCP is ceremony. A one-off task needs
one command, not a server. And an API with 40 endpoints does not get 40 tools —
expose the handful the model will actually use.

## Volatile facts (container-local — install, never assume)

- **verified 2026-07-13:** Python SDK `mcp` 1.28.1 installs; template + smoke test run
  here (plain `pip3 install mcp` hit a debian-owned PyJWT; `--ignore-installed pyjwt` fixed it).
- **verified 2026-07-13:** TS SDK latest 1.29.0 (`npm view`, not installed);
  inspector 0.22.0 starts against the template. `claude` CLI 2.1.207: `claude mcp
  add -s project` executed, wrote `.mcp.json`; local scope checked via `--help` only.
- **assumption 2026-07-13:** claude.ai connector flow (remote-only) — from
  platform docs, unverifiable in this container.

## When NOT to use this skill

- Authoring a Claude SKILL.md → **skill-authoring** (decide first which you are
  building: a skill teaches workflow; an MCP server exposes tools).
- Installing or packaging skills across surfaces → **install-and-surfaces**.
- An existing skill misbehaving → **debugging-playbook**.
- Merely USING an MCP server that is already connected — no skill needed.

## Provenance and maintenance

Authored 2026-07-13 for this library on the owner's request, modeled on the
corresponding Anthropic agent-skill concept (MCP-server scaffolding). Template,
smoke test, project-scope registration, and inspector launch were executed
in-container this date; TS-side and claude.ai facts are labeled above.

Re-verify: SDK — `python3 -c "from importlib.metadata import version; print(version('mcp'))"`;
TS SDK — `npm view @modelcontextprotocol/sdk version`; CLI — `claude mcp add --help`.
Update when FastMCP's API moves (`list_tools`, the in-memory session helper, `_mcp_server`),
`claude mcp` syntax or scopes change, or claude.ai gains stdio/local connector support.
