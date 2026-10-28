# Iteration log

Append-only. **This is the main file to read to see what the loop is doing.**

One record per round. Written by the adjudicator at session end. Never edited,
never tidied, never summarized optimistically.

## How to read this

Read right-to-left: **verdict first, score last.**

- `enforcer` moving and `issues closed` rising = real progress
- `score` rising while `enforcer` is flat = **reward hacking.** Not progress.
- `diff` large with `closed` at zero = churn
- `variance` near zero across reviewers = shared blind spot, not quality

A score is a diagnostic, never a stop condition.

## Record format

```
## Iteration <n> — <ISO datetime>
- phase: extract | scout | bind | draft | review | coherence
- scope: <whole | §3>
- enforcer: HALT 0 | BLOCK 4 | WARN 2 | passed 14/18
- newly failing: <none, or REGRESSION>
- scores: R01 R02 R03 R04 R05 R06 R07 R08
  - program:     3  2  3  2  2  3  3  2
  - skeptic:     2  2  2  1  2  2  3  2
  - conformance: 3  2  3  2  3  3  2  3
  - variance: <per item, or "low across the board — see F7.3">
- issues: opened 6 | closed 2 | wont-fix 1 | open total 11
- new taxonomy classes this round: F4.4, F5.1
- diff vs previous: 0.18
- draft version: v003
- verdict: <one sentence. what actually changed. what did not.>
- escalations: <ESC-002> | none
```

`new taxonomy classes` is the stop signal. Zero new classes in a full round means
issue-class exhaustion. Three more instances of a class you already have is not
novelty and is not a reason to keep going.

---

## Records
