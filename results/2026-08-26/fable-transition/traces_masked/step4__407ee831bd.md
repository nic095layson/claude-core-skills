# trace 407ee831bd  (case: plan-gate__pg2)
served_model: claude-fable-5 | skills_loaded: ['plan-gate'] | stop_hook_blocks: 0 | scope_reminder_injected: False

ASSISTANT TEXT:
This is a migrate/refactor task, so per your doctrine I'll open it through plan-gate before touching anything, then survey the codebase to ground the plan in what's actually here.

[SKILL LOAD: plan-gate]

[TOOL RESULT: Launching skill: plan-gate]

ASSISTANT TEXT:
Gate loaded. Before I can write a goal that could be failed, the biggest cheap unknown is what's actually in this directory — let me survey it.

[TOOL Bash: {"command": "ls -la && echo \"---FILES---\" && find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -200 && echo \"---COUNT---\" && find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | wc -l", "description": "List directory contents and file tree"}]

[TOOL RESULT: total 0
drwxr-xr-x@ 2 davidlayson  wheel   64 Aug 26 17:19 .
drwxr-xr-x@ 4 davidlayson  wheel  128 Aug 26 17:19 ..
---FILES---
---COUNT---
       0]

ASSISTANT TEXT:
The working directory is empty. Let me check whether the app lives nearby (parent/siblings) before concluding there's no code to survey.

[TOOL Bash: {"command": "ls -la /private/tmp/fta_2026-08-26/with/plan-gate__pg2/ /private/tmp/fta_2026-08-26/with/ /private/tmp/fta_2026-08-26/ 2>&1; echo \"---GREP---\"; grep -rliE 'session|jwt|passport|express-session|django.contrib.sessions|auth' /private/tmp/fta_2026-08-26 2>/dev/null | head -20", "descript]

[TOOL RESULT: /private/tmp/fta_2026-08-26/:
total 0
drwxr-xr-x@   3 davidlayson  wheel    96 Aug 26 14:46 .
drwxrwxrwt  127 root         wheel  4064 Aug 26 17:20 ..
drwxr-xr-x@  24 davidlayson  wheel   768 Aug 26 1]

ASSISTANT TEXT:
Survey complete — and the first finding is the important one: **this working directory (`.../plan-gate__pg2/r1`) is empty, and nothing in the parent tree contains an app.** There's no auth module here for me to read, so every codebase-specific fact below is an unknown, not a known. The gate output is the deliverable for your question; the answer to "where do we start" is Phase 0.

---

**Goal** — Every authenticated request in the app is authorized by a verified JWT (no `session` lookup on the request path), login/logout/refresh work end-to-end, and the session store can be removed with no test or user-facing behavior regressing.

**Knowns** (verified this session)
- Working dir has 0 files; `grep` for `session|jwt|passport|auth` across `/private/tmp/fta_2026-08-26` finds no application code. Basis: `ls`/`find`/`grep` above.
- Stack, framework, session store, and existing tests: **not knowable from here.**

**Unknowns that matter** (each would change the approach)
- Stack/framework (Express + `express-session`? Django? Rails? Spring?) — determines the middleware seam.
- Which code reads session state *besides* auth: CSRF tokens, flash messages, cart/wizard state, "remember me", admin impersonation. These are the migration's real surface, not the login handler.
- Whether you need **immediate revocation** (logout everywhere, ban user, password change). This is the single biggest design fork.
- Clients: browser only, or also mobile/API consumers? Any SSR pages that rely on cookie-session?
- Whether there's a load balancer with sticky sessions (a hint that this is what's motivating the change).

**Assumptions** (proceeding on these; correct any and I'll re-derive what depends on it)
| # | Content | Basis | Status |
|---|---|---|---|
| A1 | Revocation matters (at minimum logout + password change must invalidate access). | Nearly every real app needs it; assuming "no" is the costly mistake. | unconfirmed |
| A2 | Primary client is a browser; JWT is delivered as an `HttpOnly; Secure; SameSite` cookie, not `localStorage`. | XSS exposure of `localStorage` tokens; cookie keeps existing CSRF posture mostly intact. | unconfirmed |
| A3 | Access-token TTL short (5–15 min) + refresh token stored server-side (rotating, revocable). | Only design that satisfies A1 without a per-request DB hit on every access token. | unconfirmed |
| A4 | Non-auth session usages exist and must be re-homed, not dropped. | Empirically true in every app older than a few months. | unconfirmed |

One concern before you commit to "JWTs instead of sessions across the whole app": if A1 holds, you cannot go fully stateless — revocation forces you to keep *some* server-side state (a refresh-token table or a denylist). That's fine and normal, but it means the win is "no session lookup on the hot path + horizontal scalability," not "zero server state." Worth being explicit about with whoever set the goal, so the finish line doesn't quietly move.

**Success criteria** (pre-committed; adversarial-verify grades against these)
1. `grep` for the session middleware / `req.session` (or framework equivalent) in the request path returns zero hits outside the deletion commit.
2. Integration tests pass for: login → protected route; expired access token → 401; refresh → new pair; logout → refresh rejected; password change → all outstanding refresh tokens rejected.
3. Every non-auth session usage found in Phase 0 has a named replacement, and its existing tests still pass.
4. Token verification pins algorithm and issuer/audience (no `alg: none`, no key confusion); secrets/keys live in config, not source.
5. A rollback exists: feature flag or dual-read path so a bad deploy doesn't lock everyone out.

**Plan**

0. **Inventory (start here — this is the answer to your question).** Point me at the repo (or run this in its root). I'll map: the login/logout handlers, the auth middleware, and *every* read/write of session state, with a per-usage classification (auth / CSRF / transient UI / other).
   *Expected observation:* a table of ≤ a few dozen call sites, mostly in 2–4 files plus scattered "other."
   *Branch rule:* if session reads are spread across dozens of files, the migration needs a compatibility shim (Phase 3 gets bigger, timeline changes) — report before proceeding. If there are zero non-auth usages, A4 is refuted and Phase 3 drops.

1. **Design decision doc (one page).** Token claims, TTLs, signing (HS256 with rotated secret vs RS256/EdDSA if multiple services verify), storage (per A2), refresh + revocation (per A1/A3), key rotation.
   *Expected observation:* you confirm or correct A1–A3 here.
   *Branch rule:* if you say "no revocation needed," simplify to access-token-only with long TTL and delete the refresh table from the plan.

2. **Build the JWT path alongside sessions, behind a flag.** New issue/verify/refresh module + middleware that accepts *either* a valid JWT *or* a valid session. Unit tests for token lifecycle first.
   *Expected observation:* all existing tests still green with the flag off; new token tests green.
   *Branch rule:* if existing tests depend on session fixtures in ways the dual-path breaks, add a test helper that mints a token — don't rewrite the tests yet.

3. **Re-home non-auth session usages** (from Phase 0). CSRF → double-submit cookie or framework's token-in-form; flash messages → short-lived cookie or client state; multi-step state → DB or signed cookie.
   *Expected observation:* one small PR per usage class; each independently revertable.

4. **Flip the flag on, then cut over.** Login issues JWT; middleware stops accepting sessions after one refresh-TTL of overlap so live users aren't logged out; then delete session middleware, store, and config.
   *Expected observation:* criterion 1 hits zero; criterion 2 suite green; session store connections drop to zero in monitoring.
   *Branch rule:* any spike in 401s post-flip → flag off (criterion 5), diagnose, re-attempt.

5. **Verify** — adversarial-verify against criteria 1–5 before I call it done.

**Fenced wrong paths**
- Starting by rewriting the login handler — it's the most visible file and the least important; the scattered session consumers are what break.
- Storing tokens in `localStorage` for convenience — trades a solved problem (CSRF) for an unsolved one (XSS token theft).
- Long-lived access tokens with no refresh "to keep it stateless" — makes logout a lie.
- Big-bang cutover without the dual-accept window — logs out every active user at deploy.

---

**Recap:** The directory you launched me in has no code, so I couldn't survey the actual auth module — everything above is the plan shape plus four labeled assumptions rather than findings. The concrete starting point is **Phase 0: inventory every session consumer, not just the auth handlers**, and **the one decision that shapes everything else is whether you need revocation** (A1). Run me in the repo root (or tell me the path) and I'll execute Phase 0 and come back with the call-site table and a confirmed stack.
