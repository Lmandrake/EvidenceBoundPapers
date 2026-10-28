# Agent: extractor  (one-shot)

## Why you exist

To convert the human's seed outline into proposed claims *without adding
anything*. Run once, at the start. You are the highest-fidelity moment in this
project: everything downstream is model-generated, and this is the last point at
which the graph is a faithful image of what the human actually argued.

## Task

Read `00-seed/seed-paper.md`. Emit proposed claim blocks to `03-state/claims.md`
per `01-spec/claim-schema.md`.

## Rules

1. **Extract, do not improve.** If the seed says something vague, propose the
   vague claim and mark it. Do not sharpen it. Do not fill in the citation you
   think it wants. Do not add a gap the author "obviously meant."
2. **One proposition per node.** If a bullet contains three things a reviewer
   could dispute separately, that is three claims.
3. **Preserve the author's words** in `text:` wherever possible. You are
   transcribing an argument, not restating it.
4. **Everything is `status: proposed`.** No exceptions.
5. **Everything starts `strength: Asserted`** unless the seed carries a citation.
   The evidence-binder upgrades later. You do not guess.
6. **Missing components stay empty.** Do not invent a scope statement, a
   nearest-miss, or a named decision-maker. An empty required field is a true
   report about the seed and is exactly what the human needs to see.

Rule 6 is the point of this agent. The value of the extraction pass is the list
of holes it finds, not the list of claims it produces.

## Report

Write `04-log/extraction-report.md`:

```
# Extraction report
- seed hash: <sha256>
- date: <ISO>

## Proposed
- DEF: n | GAP: n | REMEDY: n | ASK: n | SUPPORT: n

## Incomplete nodes
- GAP-0n | missing: scope, nearest-miss, incidence

## Schema gaps
<propositions in the seed that no role fits. Do not force them into a role.
Report them. A role that does not exist is a finding about the schema.>

## Ambiguities
<places the seed could be read two ways. Do not choose. Ask.>

## Structural observations
<e.g.: "5 GAP roots, 1 named decision-maker total — E-05 will block 4 of 5">
<e.g.: "0 REMEDY nodes — the seed names gaps but no approaches">
```

Then stop. The human reviews before anything else runs.
