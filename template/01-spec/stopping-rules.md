# Stopping rules and escalation  (FROZEN — v1.0)

## Why not "run until the score is high"

Because that is the reward-hacking target. In iterative self-refinement the judge
and the author share a model, and so share blind spots: the score climbs while
human-judged quality plateaus or declines. Gains are largest in the first one or
two rounds and degrade after. A rising score late in a run is evidence of a
problem, not of progress.

**Score is never a stop condition here.** It is a diagnostic.

## Stop conditions

Stop when any of these is true:

1. **Issue-class exhaustion** — a full reviewer round surfaces no *new distinct
   taxonomy class*. Not "no new issues" — no new *classes*. Three more instances
   of F2.1 is not novelty.
2. **Round cap** — 3 rounds per section, 4 for the whole-document pass. Hard.
3. **Enforcer CLEAN + one blind round with no new classes.**
4. **Any HALT.** Stop immediately. Escalate. Do not work around it.
5. **Any regression (E-14).** Stop. Do not auto-fix.

On stop, write the reason to `04-log/iterations.md` and open
`04-log/escalation-queue.md`. Do not summarize optimistically. If the loop
stopped because it was going in circles, say that.

## Escalate on suspicious success

The counter-intuitive part, and the one to actually implement. Escalate when:

| Trigger | Why |
|---|---|
| Reviewers converge high with low variance | Three blind reviewers agreeing closely on a contested item means they share a blind spot, not that the draft is good |
| Rubric scores rise while enforcer findings are flat | Textbook reward hacking (F7.1) |
| Issue-class exhaustion in under 2 rounds | The rubric is not discriminating |
| Churn high, score delta low | The loop is rewriting, not improving (F7.2) |
| Any reviewer reports a rubric item they could not apply | Rubric defect. Feed the amendment queue. |
| Before every human gate | Cheap and mandatory |

## Cross-family audit

An external-model (non-Claude) review is a **manual, on-demand step**. It is
scarce, so do not spend it on "read my paper and tell me what you think."

**Spend it auditing the reviewers, not the draft.** A single external pass on the
draft is a weak quality check. A periodic external pass scored against the *same
frozen rubric* is a calibration audit of your entire review panel — and that
compounds, because a patterned divergence on a rubric item is a defect in the
*item*, not a fact about the draft. It feeds the amendment queue.

This is the main compensation for running a same-family panel day to day. Use it
deliberately.

### Escalation packet

When a trigger fires, the adjudicator assembles this into
`04-log/escalation-queue.md` and stops:

```
## ESC-00n  <ISO datetime>
- trigger: <which one above>
- ask: <the specific question a human or external model must answer>
- packet:
  - draft: 03-state/versions/draft-vNNN.md
  - rubric: 01-spec/rubric.md
  - claims: 03-state/claims.md   (omit for external review)
  - internal scores: <table, R-01..R-08, per reviewer>
- NOT included: revision history, prior scores, adjudicator notes
- status: open
```

The exclusion list is load-bearing. The external reviewer must be run in the same
**offline, blind** configuration as the internal panel, or the comparison means
nothing — you would be comparing an online judge to offline judges and measuring
the configuration, not the model.

### Reading the audit

Compare item by item. Record in `04-log/rubric-amendments.md`:

- **agreement** → the item is doing its job
- **one-off divergence** → note it, do nothing
- **patterned divergence across runs** → the rubric item is defective. Draft an
  amendment. A human applies it.

Do not "fix the draft" to close a divergence. The divergence is information about
the *measuring instrument*.

## Human gates

The loop halts and waits at each of these. Record every one in
`04-log/decisions.md`.

| Gate | What you are approving |
|---|---|
| **G1 · Thesis & structure** | the DEF and GAP roots, before any evidence work |
| **G2 · Rubric lock** | rubric + taxonomy + E-16 call constraints populated |
| **G3 · Claim admission** | every claim, in the table, before any prose exists |
| **G4 · Final** | the rendered draft |

G3 is the gate people skip and the one that determines whether the paper is
defensible. It is also cheap: reviewing 60 one-line claims in a table is faster
and far more accurate than finding the same problems buried in seven pages of
fluent prose.
