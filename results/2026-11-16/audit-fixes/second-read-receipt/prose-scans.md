# The receipt gate on ordinary prose, before and after the second read's fixes (2026-11-16)

**The domain kit still blocks 22 sentences, the same 22 as before. The season deck still blocks 0.** The rules of
this unit add no block and remove none on either body. The gate now reads 391 more sentences of the kit (table rows
under a header named Claim, Quote or Wording, and header rows that hold a date). None of those rows holds a bare
claim.

Method (the same as `results/2026-11-16/audit-fixes/receipt-gate/prose-scans.md`): the committed tool
`results/2026-11-15/receipt-gate-fix/prose_scan.py`. "Before" means the hooks as this unit found them (commit
94f503a). "After" means this unit's hooks. The working-note rule (E1) does not apply here, because each file is read
as one text.

    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md --sentences <audit pack>/kit-full
    python3 results/2026-11-15/receipt-gate-fix/prose_scan.py --hooks <hooks> --ext md --sentences <audit pack>/deck-full

| body | files (distinct) | sentences before -> after | standing claims before -> after | **blocked before -> after** |
|---|---|---|---|---|
| the domain kit, `kit-full` | 357 | 39,164 -> 39,555 | 43 -> 43 | **22 -> 22** (the same sentences; `diff` of the sorted lists is empty) |
| the season deck, `deck-full` | 105 | 7,809 -> 7,811 | 1 -> 1 | **0 -> 0** |

The 22 sentences, with the earlier reading of them (11 true bare claims, 8 false blocks, 3 borderline), are listed in
`results/2026-11-16/audit-fixes/receipt-gate/prose-scans.md`, section 2. The README's numbers are updated to match.
