# Escalation queue

Everything the loop needs a human for. Append-only. Nothing here resolves itself.

Four kinds land here:

1. **HALT** — the enforcer stopped the loop
2. **Suspicious success** — see `01-spec/stopping-rules.md`. The loop is doing
   well in a way that is more likely to be self-deception than quality.
3. **CLAIM-REQUEST** — a drafter needed a fact that is not an accepted claim
4. **CORPUS-REQUEST** — an agent needs a paper that is not in the corpus

## Format

```
## ESC-00n — <ISO datetime>
- kind: HALT | SUSPICIOUS | CLAIM-REQUEST | CORPUS-REQUEST
- trigger: <which rule fired>
- ask: <the specific question a human must answer>
- packet:
  - draft: 03-state/versions/draft-vNNN.md
  - rubric: 01-spec/rubric.md
  - claims: 03-state/claims.md        (omit for external cross-family review)
  - internal scores: <table>
- NOT included: revision history, prior scores, adjudicator notes
- status: open | resolved
- resolution: <what the human decided, and the decisions.md entry>
```

The `NOT included` line is load-bearing for cross-family audits. The external
model must run in the same blind, offline configuration as the internal panel —
otherwise you are comparing an online judge to offline judges and measuring the
configuration rather than the model.

## Open

## Resolved
