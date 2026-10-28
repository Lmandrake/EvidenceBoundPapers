# Rubric amendment queue

Agents propose. **A human applies, between sessions, or never.**

No agent edits `01-spec/`. The rubric, the taxonomy, and the enforcer are the
reward function. Models game flawed specifications at high rates when given the
chance — the fix is not a better-behaved agent, it is not handing over the
specification.

This is where meta-improvement happens, at human cadence. It is the slowest loop
in the system and the most valuable: the taxonomy and rubric outlive this paper.

## What belongs here

- a reviewer's `meta` block reported an item it could not apply
- **patterned divergence** between internal panel and a cross-family audit on the
  same item, across runs — that is a defect in the *item*, not a fact about the
  draft. Do not fix the draft to close it.
- a check that fires on correct text (false positive) or misses a real failure
- a taxonomy class observed repeatedly that has no rubric item
- **a judgmental item (R-nn) that could become a mechanical check (E-nn)** —
  every one of these that lands is a permanent improvement

## Format

```
### AMD-00n — <ISO date>
- target: rubric R-04 | taxonomy F4.4 | enforcer E-07
- observed: <the evidence, across which runs>
- proposal: <the specific change>
- proposed-by: <agent>
- status: proposed | applied | rejected
- human ruling: <date, decision, why>
```

## Proposed

## Applied

## Rejected
