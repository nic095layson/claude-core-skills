# Council trigger eval, 2026-11-12

Fresh headless sessions, Skill tool only, empty working directory, account plugin off, session model B,
N=2 per prompt (driver: `results/2026-10-19/red-team-trigger-evals/drivers/run_one_isolated.sh`). The copy
that loaded is the account-synced one; its description is byte-identical to the library copy.

| id | prompt (start) | expected | run 1 | run 2 |
|---|---|---|---|---|
| 1 | "Council: should I refinance…" | FIRES | fired | fired |
| 2 | "Convene the council on…" | FIRES | fired | fired |
| 3 | "…Get the council's take." | FIRES | fired | fired |
| 4 | "What's the city council's role…" | SILENT | silent | silent |
| 5 | "Can you double-check this SQL migration…" | SILENT | silent | silent |

Should-fire 6/6, should-not silent 4/4. Gate (>=5/6; 4/4): PASS. Every run exited 0 with result "success".
Raw transcripts stay in the session's scratch (they carry a model identifier; doctrine rule 6).
