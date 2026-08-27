# trace e8867aadb2  (case: plan-gate__pg2)
served_model: claude-fable-5 | skills_loaded: ['plan-gate'] | stop_hook_blocks: 0 | scope_reminder_injected: False

ASSISTANT TEXT:
I'll start by loading the plan-gate governor (this is exactly the kind of migrate-Y-to-Z task it covers), then look at what's actually in this codebase before recommending a starting point.

[SKILL LOAD: plan-gate]

[TOOL RESULT: Launching skill: plan-gate]

ASSISTANT TEXT:
Before I plan, I'll convert the cheap unknowns into facts — let me look at what's actually in this directory.

[TOOL Bash: {"command": "ls -la && echo \"--- tree ---\" && find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' | head -100", "description": "List directory contents and file tree"}]

[TOOL RESULT: total 0
drwxr-xr-x@ 2 davidlayson  wheel   64 Aug 26 17:19 .
drwxr-xr-x@ 4 davidlayson  wheel  128 Aug 26 17:19 ..
--- tree ---
.]

ASSISTANT TEXT:
The working directory is empty. Let me check the parent and siblings in case the app lives nearby, and confirm there's no repo anywhere close.

[TOOL Bash: {"command": "ls -la /private/tmp/fta_2026-08-26/with/plan-gate__pg2/ /private/tmp/fta_2026-08-26/with/ /private/tmp/fta_2026-08-26/ 2>&1; echo \"--- any source files within 4 levels ---\"; find /private/tmp/fta_2026-08-26 -maxdepth 5 -type f 2>/dev/null | head -50; echo \"--- git repos ---\"; find /]

[TOOL RESULT: /private/tmp/fta_2026-08-26/:
total 0
drwxr-xr-x@   3 davidlayson  wheel    96 Aug 26 14:46 .
drwxrwxrwt  127 root         wheel  4064 Aug 26 17:20 ..
drwxr-xr-x@  24 davidlayson  wheel   768 Aug 26 1]

ASSISTANT TEXT:
The working directory (`/private/tmp/fta_2026-08-26/with/plan-gate__pg2/r2`) is empty, and the siblings are unrelated scratch folders (deploy scripts, a checkout.py) — there's no auth module, no app, and no git repo anywhere under this tree. So I can't ground this in your code yet; here's the gate on the information I have, and the answer to "where do we start" falls out of it.

**Goal** — Every authenticated request in the app is authorized by a verified JWT, no code path reads or writes a server-side session store, and logout/revocation still works — with the existing test suite green and no user forced to re-login mid-rollout (or that cost explicitly accepted).

**Knowns** — The target directory contains no source (checked: `ls`, `find` to depth 5, no `.git`). Everything else about the app is unknown to me.
**Unknowns that matter** — language/framework; what the session currently *holds* besides user identity (CSRF token, flash messages, cart, impersonation, feature flags — none of that belongs in a JWT); how many consumers read the session (middleware, decorators, templates, websockets, background jobs); whether there's a mobile/SPA client or server-rendered pages; whether "log out everywhere" / admin-forced logout is a product requirement.

**Assumptions** (unconfirmed until you point me at the repo)
- A1 — A single monolith with one login endpoint and one session-reading middleware/decorator that most routes go through. *Basis:* most apps with "the authentication module" are shaped this way; if it's several services, phase 3 becomes a per-service loop.
- A2 — Revocation matters (logout, password change, admin kill). *Basis:* nearly always a real requirement, and it's the thing stateless JWTs handle *worst*, so it must be designed in up front, not bolted on.
- A3 — Browser clients are involved, so token storage is httpOnly cookie (CSRF defence needed) rather than localStorage (XSS exposure). *Basis:* safer default; reverse it if it's API-only.

**Success criteria** — (1) `grep` for the session API returns zero hits in app code; (2) a tampered, expired, and revoked token each get 401 on every protected route (tested); (3) login → refresh → logout round-trip tested; (4) existing suite passes; (5) during the dual-accept window, an old session cookie still works.

**Plan**
1. **Inventory (read-only, no code changes).** Grep for every session read/write and every "current user" access point; list what's stored in the session and who reads it. *Expect:* a handful of writers (login/logout), many readers, and 1–3 non-identity things living in the session. *Branch:* if readers are scattered across dozens of files with no shared abstraction, insert phase 2b (introduce a `current_user` accessor first) before touching tokens.
2. **Decision doc — five questions, answered in writing before any token code:** access+refresh vs access-only; signing alg and key management (HS256 shared secret vs RS256/EdDSA keypair, rotation); lifetimes; **revocation strategy** (refresh-token rotation with server-side refresh store, or a short denylist — pick one); where non-identity session data moves to. *Expect:* one page. *Branch:* if A2 turns out false (no revocation needed), the design simplifies substantially — say so and drop the refresh store.
3. **Build the primitive behind the existing abstraction.** Issue/verify functions + a middleware that populates the *same* `current_user` object the app already uses, so downstream code doesn't change. Middleware accepts **either** a JWT or a legacy session during rollout. *Expect:* full suite still green with zero route edits.
4. **Flip the login endpoint** to issue JWTs (and refresh tokens per phase 2); migrate logout to revoke. *Expect:* new logins get tokens, old sessions still work.
5. **Remove the session path** after the longest session lifetime has elapsed: delete the session middleware/store, run the grep from criterion 1, verify criteria 2–4. *Branch:* any remaining hit is either a missed consumer (go back to phase 1) or non-identity data that never got a new home (phase 2).

**Fenced wrong paths** — Starting by writing the JWT library code (feels productive, but you'll rewrite it once phase 1 reveals what the session actually carries). Big-bang cutover with no dual-accept window (logs everyone out; no rollback). Putting authorization data (roles/permissions) in the token without a revocation plan (stale privileges until expiry).

**So, where to start: phase 1, the inventory — and the very first thing I need is the path to the repo.** Point me at it (or `cd` there and re-run me) and I'll do the inventory and the phase-2 decision doc, which are read-only and don't touch any code.
