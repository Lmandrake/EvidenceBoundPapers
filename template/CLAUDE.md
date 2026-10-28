# Operating contract

Read this file first, every session. It overrides convenience.

## What this project is

A high-stakes, reviewer-scored paper (originally a Decadal Survey white paper), built claim-first. The claim graph in
`03-state/claims.md` **is** the paper. `03-state/draft.md` is a rendering of it
and has no independent authority. If prose and claims disagree, the claims win
and the prose is wrong.

## Hard rules

These are not preferences. Violating any of them is a halt condition.

1. **The seed is immutable.** `00-seed/seed-paper.md` is never edited, never
   rewritten, never "cleaned up." It is read-only input.
2. **The spec is frozen.** No agent edits anything in `01-spec/`. Proposed
   changes go to `04-log/rubric-amendments.md` as a request. A human applies them
   between sessions or not at all.
3. **No claim enters the paper without human admission.** Agents write claims
   with `status: proposed`. Only a human sets `status: accepted`. Only accepted
   claims may be rendered.
4. **Closed corpus.** A citation is legal only if its key exists in
   `03-state/corpus.md`. Agents may not cite from memory, from the web, or from
   a paper they believe exists. Corpus additions go to
   `04-log/escalation-queue.md` as a request.
5. **Drafters render, they do not assert.** No fact, number, comparison, or
   citation may appear in `draft.md` that is not traceable to an accepted claim.
   If the drafter needs a fact that does not exist as a claim, it stops and files
   a claim request. It does not write the fact.
6. **Reviewers are blind.** A reviewer receives: the current draft, the frozen
   rubric, and nothing else. No revision history. No prior scores. No other
   reviewer's output. No claim table. Never brief a reviewer on what changed.
7. **Reviewer and reviser never share a context.** The adjudicator mediates.
8. **The enforcer halts.** Its output is not advice. If it reports a HALT-class
   failure, the loop stops and the failure goes to
   `04-log/escalation-queue.md`.
9. **No regression.** A check that passed in a prior iteration may not fail in
   this one. If it does: halt, do not auto-fix, escalate.
10. **Everything is logged before it is done.** Append to `04-log/` first, act
    second. An unlogged action did not happen and must be reverted.
11. **Never discard protected text.** Anything listed in
    `03-state/protected.md` survives verbatim or goes to escalation. The seed's
    prose is the highest-value text in this project.
12. **Versions are kept.** Every render writes `03-state/versions/draft-vNNN.md`
    before overwriting `draft.md`. Improvement may be an illusion; the human
    needs to be able to pick.

## What "improving" is allowed to mean

Only two things improve autonomously:

- **the claim graph** — completeness of required components, binding coverage,
  strength grades
- **the rendering** — clarity, structure, voice, compliance with the call

The rubric, the taxonomy, the enforcer, and the definition of quality do **not**
improve autonomously. They are the reward function. Agents do not touch the
reward function.

## Session start procedure

1. Read `CLAUDE.md`, `01-spec/claim-schema.md`, `01-spec/stopping-rules.md`.
2. Run the enforcer. Read `04-log/enforcer-report.md`.
3. Read `04-log/issues.md` — respect `wont-fix`. Do not re-raise.
4. Read the tail of `04-log/iterations.md`.
5. State the plan. Then act.

## Session end procedure

1. Run the enforcer. Write the report.
2. Append an iteration record to `04-log/iterations.md`.
3. Write anything needing a human to `04-log/escalation-queue.md`.
4. Do not summarize optimistically. Report what failed.
