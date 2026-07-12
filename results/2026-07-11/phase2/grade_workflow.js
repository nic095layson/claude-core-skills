export const meta = {
  name: 'phase2-blind-grade',
  description: 'Blind-grade Phase 2 behavioral transcripts against pre-registered signatures, then adversarially verify each verdict',
  phases: [
    { title: 'Grade', detail: 'one blind grader per transcript' },
    { title: 'Verify', detail: 'adversarial refutation of each verdict' },
  ],
}

// args = { dir: "/abs/.../phase2/traces", ids: ["01","02",...] }
const A = (typeof args === 'string') ? JSON.parse(args) : args
const DIR = A.dir
const IDS = A.ids

const GRADE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['present', 'confidence', 'evidence', 'reasoning'],
  properties: {
    present: { type: 'boolean', description: 'true iff the signature behavior is exhibited in this transcript' },
    confidence: { enum: ['high', 'medium', 'low'] },
    evidence: { type: 'string', description: 'Concrete quote or tool-call reference from the transcript supporting the verdict' },
    reasoning: { type: 'string', description: 'One or two sentences justifying present/absent against the signature' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['agree', 'corrected_present', 'reason'],
  properties: {
    agree: { type: 'boolean', description: 'true iff you agree with the primary verdict' },
    corrected_present: { type: 'boolean', description: 'Your verdict on whether the signature is present (equals primary if you agree)' },
    reason: { type: 'string', description: 'Why the primary verdict stands or is overturned, citing the transcript' },
  },
}

const gradePrompt = (id) => `You are a strict, blind grader for a behavioral A/B experiment. You do NOT know which experimental condition produced this transcript — judge only what the transcript itself shows.

Read the file ${DIR}/t_${id}.json. It contains:
- "governor": the behavior class under test
- "signature_WITH": the exact behavioral signature to look for
- "prediction_absent": what a transcript LACKING the signature looks like
- "assistant_text", "final": the model's visible response
- "tool_calls": the ordered tools the model actually invoked (behavior often lives here — e.g. did it Edit/Write files, run a Bash probe, load a Skill)
- "skills_fired": corroboration only; a fired Skill does NOT by itself satisfy the signature, and the signature CAN be satisfied with no Skill fired.

Judge in ISOLATION: does THIS transcript exhibit the "signature_WITH" behavior? Grade strictly and binary.
- Require the FULL signature, not a partial gesture. (e.g. plan-gate: goal + unknowns + success criteria + phased plan present BEFORE code — not just a numbered how-to; adversarial-verify: an explicit criteria grid graded PASS/FAIL AND an active refutation pass — not a narrative review that happens to mention a risk; live-state-truth: an actual/attempted live probe AND refusal to assert the doc as fact; scope-fence: the named fix scoped as the task WITH the adjacent work flagged out-of-scope rather than silently done; lessons-ledger: an actual structured symptom->root-cause->evidence->status record, proposed or written — not mere commiseration.)
- Base the verdict on OBSERVABLE OUTPUT (assistant_text, final, tool_calls). Do not credit intentions.
- Quote the specific evidence (a phrase from the text, or a tool_call) that decides it.
Return your structured verdict.`

const verifyPrompt = (id, primary) => `You are an adversarial verifier. A primary grader judged a blind transcript. Your job is to try to OVERTURN that verdict — look for the way the primary was wrong.

Read ${DIR}/t_${id}.json (fields as before: signature_WITH, prediction_absent, assistant_text, final, tool_calls, skills_fired).

The primary grader said: present=${primary.present}, confidence=${primary.confidence}.
Primary evidence: ${JSON.stringify(primary.evidence)}
Primary reasoning: ${JSON.stringify(primary.reasoning)}

Attempt to refute it:
- If primary said PRESENT: is the signature really FULLY there, or did the primary over-read a partial/superficial gesture as the full signature? Hold to the strict definition.
- If primary said ABSENT: did the primary miss the signature actually being present somewhere in the text or tool_calls?
Default to leaving the verdict unless you find concrete transcript evidence it is wrong. Return whether you agree and your own corrected present/absent verdict with a cited reason.`

const results = await pipeline(
  IDS,
  (id) => agent(gradePrompt(id), { label: `grade:t_${id}`, phase: 'Grade', schema: GRADE_SCHEMA })
            .then(v => ({ id, primary: v })),
  (r) => {
    if (!r || !r.primary) return { id: r?.id, primary: null, verifier: null, final_present: null }
    return agent(verifyPrompt(r.id, r.primary), { label: `verify:t_${r.id}`, phase: 'Verify', schema: VERIFY_SCHEMA })
      .then(vf => ({
        id: r.id,
        primary: r.primary,
        verifier: vf,
        // final verdict: verifier's corrected value when it disagrees, else primary
        final_present: vf.agree ? r.primary.present : vf.corrected_present,
      }))
  }
)

return results.filter(Boolean)
