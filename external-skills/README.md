# External skills — adopted layer (2026-07-13)

Skills and packs adopted from the external-library analysis
(`results/2026-07-13/external-skill-analysis/REPORT.md`, PR #2,
owner-approved 2026-07-13). Two mechanisms:

- **`vendored/`** — small, permissively-licensed skills copied into this repo
  with upstream `LICENSE` + `PROVENANCE.md` in each directory. Deliberately
  **not** under `.claude/skills/` so nothing here auto-loads: zero per-session
  context cost until installed (architecture-contract Decision 5).
- **`PACKS.md`** — install runbooks for the big or license-restricted packs
  that must NOT be vendored (Anthropic proprietary, Trail of Bits ShareAlike,
  149-skill collections). They install as plugins or checkouts on demand.

Install a vendored skill where you need it:

```bash
tools/install-external-skill.sh --list                    # what's available
tools/install-external-skill.sh systematic-debugging      # → ~/.claude/skills
tools/install-external-skill.sh --target /path/to/project/.claude/skills test-driven-development
tools/install-external-skill.sh --package avoid-ai-writing  # → dist/avoid-ai-writing.skill for claude.ai
```

Then **register-then-verify** per `install-and-surfaces`: files in place is
half an install; the skill appearing in a fresh session's list is the half
that counts.

## Vendored registry

| Skill | Source (commit) | License | Surfaces | Tier | Use when |
|---|---|---|---|---|---|
| `subagent-driven-development` | obra/superpowers (`d884ae04`) | MIT | Code only | HIGHLY RECOMMEND | Executing a written plan via fresh-context subagents; model-tier economics, review-package flow |
| `systematic-debugging` | obra/superpowers (`d884ae04`) | MIT | Both | NICE TO HAVE | Any nontrivial bug; the 3-strike fix counter + architecture escalation is the payload |
| `test-driven-development` | obra/superpowers (`d884ae04`) | MIT | Code (needs a test runner) | NICE TO HAVE | Feature/bugfix work in a dev repo; project-scope it there |
| `writing-plans` | obra/superpowers (`d884ae04`) | MIT | Code-leaning | NICE TO HAVE | Producing a zero-context executable plan document; pairs with subagent-driven-development |
| `receiving-code-review` | obra/superpowers (`d884ae04`) | MIT | Both | NICE TO HAVE | Acting on incoming review feedback |
| `finishing-a-development-branch` | obra/superpowers (`d884ae04`) | MIT | Code only | NICE TO HAVE | Merging/cleaning up worktree-based feature work |
| `using-git-worktrees` | obra/superpowers (`d884ae04`) | MIT | Code only | NICE TO HAVE | Isolation when harness worktree tooling is absent |
| `writing-skills` | obra/superpowers (`d884ae04`) | MIT | n/a | **REFERENCE ONLY** | Never install (competes with skill-authoring's trigger territory). Source for the gated fold — see REPORT §fold |
| `fable-method` | Sahir619/fable-method (`b2a24d5b`) | MIT | Both | NICE TO HAVE | Environments where the governors are NOT installed (a loaner discipline) |
| `fable-judge` | Sahir619/fable-method (`b2a24d5b`) | MIT | Code-leaning | NICE TO HAVE | Auditing another agent's/model's completion claims in multi-agent work |
| `avoid-ai-writing` | conorbronsdon/avoid-ai-writing (`500ff590`) | MIT | Both (text-only) | NICE TO HAVE | Sweeping external-facing prose for AI fingerprints; upload to claude.ai before big writing pushes |
| `youtube-transcript` | michalparkola/tapestry (`80e1dc56`) | MIT | Code only | NICE TO HAVE | Pulling YouTube transcripts (subs → Whisper fallback) |
| `owasp-security` | agamm/claude-code-owasp (`f5dfa3d6`) | MIT | Both | NICE TO HAVE | Security review checklists (OWASP 2025 / LLM / Agentic) when Trail of Bits pack isn't installed |

## Rules of the layer

1. **Nothing here goes always-on.** The always-on set stays plan-gate,
   adversarial-verify, scope-fence, brand-standard. Installing a vendored
   skill personally is a deliberate, reversible act — uninstall when the
   season of work ends.
2. **Name collisions are forbidden.** No vendored skill may share a name with
   a core skill; the installer enforces this.
3. **Vendored skills keep upstream style.** Don't rewrite them to house
   style — re-vendor from upstream to update (bump commit in PROVENANCE.md).
4. **Folding beats installing.** If a vendored skill's best idea belongs in a
   core skill, that graft goes through research-methodology + 
   architecture-contract (see REPORT §fold-don't-add); the vendored copy is
   the evidence source, not the mechanism.
5. **Volatile facts carry dates.** Registry rows state the vendored commit;
   upstreams move — re-check before assuming currency.
