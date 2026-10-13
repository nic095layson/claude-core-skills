export const meta = {
  name: 'heldout-classifier-set',
  description: 'Author a held-out prompt set blind to the governance classifier, label it with two independent labelers, adjudicate disagreements',
  phases: [
    { title: 'Author', detail: 'two blind authors, different angles' },
    { title: 'Label', detail: 'two independent labelers per prompt set, blind to author intent' },
    { title: 'Adjudicate', detail: 'third agent settles disagreements' },
  ],
}

const POLICY = `LABELING POLICY (the only definition of the labels; apply it literally).

A message is one owner turn sent to an AI assistant (Claude) that works for the owner, David: an aerospace/defense professional who uses Claude for compliance and proposal documents, a CEO-facing operations write-up, a fantasy-basketball draft analytics kit (Python, CSV data, z-scores, backtests), resumes and cover letters, clinical ABA stimulus decks, email, and a governance library of Claude "skills" (plan-gate, scope-fence, adversarial-verify, after-report, gauntlet) with hooks and CI-like checks.

Each message gets exactly one LABEL and, when the label is GOVERNED, one or more CLASSES.

LABEL = GOVERNED when the message starts NEW non-trivial work the owner will rely on: multi-step, produces or changes a deliverable, code, data, a document, an analysis, a plan, a configuration, or a decision; or costly if wrong. Also GOVERNED when the owner questions, doubts, or disputes the work's method, data, or result (even politely, even phrased as a question).
LABEL = REQUIREMENT when the message only states a constraint or requirement on work already under way ("X is critical", "make sure Y", "Z must stay"), without asking for new work.
LABEL = CONTINUATION when the message continues, retries, approves a step of, or acknowledges a task ALREADY in progress, without adding new consequential work ("continue", "try again", "looks good, keep going", "yes", "go ahead with option B" when option B was already planned in detail). A message that approves a list of fixes AND asks for new consequential actions (pushing changes, uploading, building) is GOVERNED, not CONTINUATION.
LABEL = SILENT when the message is trivial (one-step factual question, arithmetic, a one-line lookup, a rename), casual chat, thanks, a pure preference call, creative play (a poem, a joke), or text that is clearly machine/harness output rather than the owner's words.

CLASSES for GOVERNED (one or more):
- build: create, implement, draft, write, set up, configure, fix, apply, migrate, package, upload, deploy, refactor, produce a document/deck/code/plan.
- analysis: analyze, evaluate, compare, investigate, research, report on, forecast, backtest, assess data.
- review: check, verify, validate, audit, test, calibrate, confirm correctness, review something.
- dispute: the owner questions or disagrees with the work's method, data, assumptions, or result.

Edge rules: (1) length does not decide; a short imperative ("Proceed with all fixes and push") can be GOVERNED. (2) a trigger-looking word inside a trivial question stays SILENT ("what time zone is the draft in?", "who did the Lakers draft?", "is review spelled with an e?"). (3) quoted or pasted text the owner did not write as a request does not make a message GOVERNED by itself; judge the owner's own ask.`

const PROMPTS_SCHEMA = { type: 'object', properties: {
  prompts: { type: 'array', items: { type: 'object', properties: {
    text: { type: 'string' }, intended_label: { type: 'string', enum: ['GOVERNED','REQUIREMENT','CONTINUATION','SILENT'] },
    intended_classes: { type: 'array', items: { type: 'string', enum: ['build','analysis','review','dispute'] } },
    angle: { type: 'string' } }, required: ['text','intended_label','intended_classes','angle'] } } },
  required: ['prompts'] }

const LABEL_SCHEMA = { type: 'object', properties: {
  labels: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, label: { type: 'string', enum: ['GOVERNED','REQUIREMENT','CONTINUATION','SILENT'] },
    classes: { type: 'array', items: { type: 'string', enum: ['build','analysis','review','dispute'] } },
    confidence: { type: 'string', enum: ['high','medium','low'] }, reason: { type: 'string' } },
    required: ['id','label','classes','confidence','reason'] } } }, required: ['labels'] }

const ADJ_SCHEMA = { type: 'object', properties: {
  decisions: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, label: { type: 'string', enum: ['GOVERNED','REQUIREMENT','CONTINUATION','SILENT'] },
    classes: { type: 'array', items: { type: 'string', enum: ['build','analysis','review','dispute'] } }, reason: { type: 'string' } },
    required: ['id','label','classes','reason'] } } }, required: ['decisions'] }

const BLIND = `HARD RULE: do NOT open, read, grep, or search for any file under /home/user (no repository files, no hooks, no classifier code, no skills). Do not use Bash, Read, Grep or Glob at all. Work only from this message. This keeps the set held-out from the system it will test.`

const AUTHORS = [
  { key: 'A', angle: `Realistic owner phrasing across ALL of David's domains, in many styles: terse imperatives, polite multi-sentence asks, questions, multi-part bulleted notes, voice-to-text run-ons, typos. Include messages like an owner sends mid-project: approvals with new actions, "provide X", "proceed with Y", "conduct Z", status questions, objections to results.` },
  { key: 'B', angle: `Adversarial edge cases for a keyword-based detector: trivial questions that contain work words (build, draft, review, validate, analyze, fix, test, migrate, report, plan), non-trivial requests phrased with NO obvious work verb ("thoughts on whether we should switch the projection baseline?", "the board needs the injury data now"), disputes phrased softly ("hmm, are we sure the 20-year window makes sense?"), requirements, continuations ("again", "keep going", "redo it"), casual chat, creative asks, and harness-like text (system notifications, tool output pasted alone).` },
]

phase('Author')
const authored = await parallel(AUTHORS.map(a => () => agent(
  `${BLIND}\n\nYou are writing test messages for evaluating a detector that decides which owner messages need a governed (planned, verified) response from an AI assistant.\n\n${POLICY}\n\nYOUR ANGLE: ${a.angle}\n\nWrite exactly 36 distinct messages: 18 GOVERNED (spread across build, analysis, review, dispute; some with two classes), 4 REQUIREMENT, 4 CONTINUATION, 10 SILENT. Each message must read as something a real person would send; vary length from 2 words to about 80 words. Do not number them inside the text. For each give your intended label and classes under the policy, and a 3-6 word angle note. Return only the StructuredOutput.`,
  { label: `author:${a.key}`, phase: 'Author', schema: PROMPTS_SCHEMA })))

const items = []
authored.forEach((r, ai) => (r && r.prompts || []).forEach((p, pi) => items.push({ id: `${AUTHORS[ai].key}${String(pi + 1).padStart(2, '0')}`, author: AUTHORS[ai].key, ...p })))
log(`${items.length} prompts authored`)

phase('Label')
const listing = items.map(it => `[${it.id}] ${it.text}`).join('\n\n')
const labelers = await parallel([1, 2].map(n => () => agent(
  `${BLIND}\n\nYou are labeler ${n}. Label every message below under the policy. You do not see anyone else's labels and must not guess them; apply the policy literally, message by message, judging each in isolation.\n\n${POLICY}\n\nMESSAGES (id in brackets):\n\n${listing}\n\nReturn one label object per id, every id exactly once. Return only the StructuredOutput.`,
  { label: `label:${n}`, phase: 'Label', schema: LABEL_SCHEMA })))

const L1 = new Map((labelers[0] && labelers[0].labels || []).map(x => [x.id, x]))
const L2 = new Map((labelers[1] && labelers[1].labels || []).map(x => [x.id, x]))
const same = (a, b) => a && b && a.label === b.label && (a.label !== 'GOVERNED' || JSON.stringify([...a.classes].sort()) === JSON.stringify([...b.classes].sort()))
const sameLabel = (a, b) => a && b && a.label === b.label
const disagreements = items.filter(it => !sameLabel(L1.get(it.id), L2.get(it.id)))
log(`label agreement: ${items.length - disagreements.length}/${items.length} on the top-level label`)

phase('Adjudicate')
let adjudicated = []
if (disagreements.length) {
  const dl = disagreements.map(it => `[${it.id}] ${it.text}\n  labeler1: ${JSON.stringify(L1.get(it.id))}\n  labeler2: ${JSON.stringify(L2.get(it.id))}`).join('\n\n')
  const adj = await agent(`${BLIND}\n\nYou are the adjudicator. Two labelers disagreed on the top-level label of the messages below. Decide each under the policy, citing the policy clause that decides it. Do not split the difference; pick the label the policy requires.\n\n${POLICY}\n\nDISAGREEMENTS:\n\n${dl}\n\nReturn only the StructuredOutput.`,
    { label: 'adjudicate', phase: 'Adjudicate', schema: ADJ_SCHEMA })
  adjudicated = (adj && adj.decisions) || []
}
const A = new Map(adjudicated.map(x => [x.id, x]))
const final = items.map(it => {
  const a = L1.get(it.id), b = L2.get(it.id)
  let gold
  if (sameLabel(a, b)) {
    const classes = a.label === 'GOVERNED' ? [...new Set([...(a.classes || []), ...(b.classes || [])])] : []
    gold = { label: a.label, classes, source: same(a, b) ? 'agree' : 'agree-label-union-classes' }
  } else if (A.get(it.id)) gold = { label: A.get(it.id).label, classes: A.get(it.id).classes, source: 'adjudicated' }
  else gold = { label: null, classes: [], source: 'unresolved' }
  return { ...it, labeler1: a || null, labeler2: b || null, gold }
})
return { n: items.length, agreement_top_label: items.length - disagreements.length, disagreements: disagreements.length, items: final }