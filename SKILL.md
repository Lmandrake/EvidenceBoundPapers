---
name: evidence-bound-papers
description: Author a high-stakes paper where every claim traces to a real source. USE WHEN writing or revising a white paper, decadal-survey or ESAS submission, RFI/RFP response, proposal, position or concept paper, standards or policy recommendation, or review article a hostile panel will score; when every claim needs a real citation, a reviewer found over-claiming, a page limit applies, or iteration must not quietly worsen it; or auditing a draft for unsupported claims or phantom citations. NOT for first drafts, emails or low-stakes writing.
---

# Evidence-bound papers

A claim-graph-primary, human-gated, checker-enforced way to write a document that has to
survive a panel. The argument lives in a typed graph of claims; the prose is a *rendering* of
that graph and has no independent authority. If prose and claims disagree, the prose is wrong.

This exists because naive iterative refinement fails in a specific, well-documented way:
when the same model writes and grades, the score climbs while real quality plateaus or
degrades, because author and judge share blind spots. A fluent revision loop will smooth a
sharp, correct sentence into fluent nothing, and a complicit judge will call it progress.

Three countermeasures do the heavy lifting, in order of importance:

1. **Move truth out of the judgment channel.** Restate as many quality properties as
   possible as *deterministic checks on the claim graph* rather than *opinions about prose*.
   A script, not a reviewer, is the dependable feedback channel.
2. **Blind the reviewers.** A reviewer sees the current draft and the frozen rubric. Nothing
   else — no revision history, no prior scores, no other reviewer's output, no claim table.
3. **Freeze the reward function.** The rubric, the spec and the checker are human-owned. The
   model may propose amendments to a queue. It may never edit them.

## When to use it, and when not

Use it when provenance and reviewer scrutiny dominate: a decadal white paper, a proposal, a
standards recommendation. The prerequisites are real — a committed expert who can rule at the
gates, a set of source documents you can actually ingest, a machine-checkable version of the
call's rules, and tolerance for iteration.

Skip it for first drafts, exploration, or anything where being wrong is cheap. The overhead
is only justified under scrutiny, and without an expert at the gates it degrades to ordinary
model writing with extra bookkeeping.

## The shape

Copy `template/` to a working directory. Five numbered layers, and the numbering is the
access-control model:

```
00-seed/     immutable. the human-authored origin, hash-locked. never edited by any agent.
01-spec/     the frozen reward function. amendments go to a queue, not to these files.
02-agents/   role briefs. nine roles. resist adding a tenth.
03-state/    the live artifacts. claims.md is the paper; draft.md is a rendering.
04-log/      append-only ledger. log before you act.
tools/       enforce.py (deterministic, no LLM), export_packet.py (blinded packets)
```

Inputs are immutable, the reward function is human-owned, the work product is what the model
may change, and the ledger records every decision *before* it is executed. An unlogged action
did not happen and must be reverted.

Read `template/CLAUDE.md` first — it is the operating contract, and its twelve hard rules are
halt conditions rather than preferences. Then `01-spec/claim-schema.md` and
`01-spec/stopping-rules.md`. `template/PORTING.md` says which files are venue-specific.

## The loop and its four gates

```
seed → EXTRACT claims → <G1 thesis & structure> → <G2 rubric lock>
     → GAP-SCOUT + EVIDENCE-BINDER → <G3 claim admission>
     → RENDER draft → ENFORCE (halts) → BLIND REVIEW ×3 (+ cross-family audit)
     → ADJUDICATE → back to render, or stop, or escalate → <G4 final>
```

Gates are human. Only a human writes `status: accepted`; agents propose. Every gate ruling
lands in `04-log/decisions.md`, and check E-18 fails if a claim became accepted without one —
which is what makes the rule real rather than aspirational.

**G2 comes before drafting on purpose.** Locking the rubric and the length/format rules
before any prose exists is what stops the target moving to fit the output.

**G3 is the gate people skip and the one that decides whether the paper is defensible.** It
is also the cheapest: reviewing sixty one-line claims in a table is faster and far more
accurate than finding the same problems buried in seven pages of fluent prose.

## The frozen reward function

`01-spec/` and `tools/enforce.py` are locked at G2. The checker is **deterministic and calls
no LLM**. It verifies structure and provenance: spans match sources character-for-character,
every citation and numeral traces to a bound claim, protected text is intact, the length
proxy holds, and no previously-passing check now fails.

You cannot game a grader you cannot edit. So:

- A wrong check is an **amendment request** in `04-log/rubric-amendments.md` (`AMD-nnn`),
  applied by a human. Not a fix you make.
- If the checker itself **crashes**, do not hand-write its outputs to simulate a clean run.
  Forging the reward function's verdict is the cardinal sin this whole design guards against.
  File the amendment, file a halt in `04-log/escalation-queue.md`, and verify read-only
  instead — `run()` has no side effects, so you can import it and inspect the checks directly
  to tell a human "the content is clean, only the report writer is broken."
- **A previously-passing check that now fails is a HALT and is never auto-fixed.** It is the
  primary evidence that the loop is making the paper worse while reporting that it is better.

The slowest loop in the system is the amendment queue, and it is the most valuable one: the
taxonomy and rubric outlive the paper. Every judgmental item (`R-nn`) you can convert into a
mechanical check (`E-nn`) is a permanent improvement.

## Closed corpus, and the ceiling of verification

A citation is legal only if its key is in `03-state/corpus.md`. A quoted span is checked
byte-for-byte against cached full text in `03-state/corpus-text/`. Unverifiable sources are
allowed but **cap the claim's strength at `Suggestive`**, so the provenance cost is explicit
rather than hidden. This converts citation hallucination from a detection problem into an
impossibility.

**Now the limit, which is the most important paragraph in this file.** A character-exact span
proves the words exist in the source. It proves nothing about whether the source supports the
claim's *scope*. Both papers built with this method shipped over-claims that a human expert
caught **while the checker read CLEAN**:

- A span was quoted verbatim — "calculations were only performed for data visualization
  purposes" — and rendered as "twins commonly stall at the visualization layer." The source's
  very next sentence says numerical simulation was the *most common* function. The claim
  contradicted the paper it cited.
- A market projection was attributed to the paper that quoted it, not to the vendor that
  produced it. Secondhand became primary.

The checker cannot catch either, because both are entailment failures, not provenance
failures. So adopt the remedy from the start: an **evidence audit** before prose
regeneration, one row per load-bearing claim — exact claim, type, scope, source and exact
passage, support level (`direct` / `partial` / `adjacent`), counter-evidence, revised
language, confidence. A claim may not enter if the cited source does not directly support its
scope. Rescoped claims are re-admitted by a human at a G3-revision gate.
`example-synthetic/04-log/evidence-audit.md` shows the format on an invented claim. See also the
`claim-provenance` skill.

## The checks that do the work

Node completeness is where most quality lives, because each requirement kills a specific
failure. From `01-spec/claim-schema.md`:

- A **GAP** needs a `scope` a reader could reproduce (corpus, window, queries, date), at
  least three `nearest-miss` entries *each with an exclusion rationale*, a `magnitude`, a
  **named** `incidence` (a person or a genuinely-callable office, plus the decision and the
  metric that moves — "decision-makers" is not a name), and `tractability`. You cannot cite a
  paper for the nonexistence of papers, so scope plus nearest-miss *is* a gap's evidence.
- A **REMEDY** needs a `mechanism` specific enough to write a solicitation from, at least two
  `alternatives` with exclusion rationales, and an `enabling-now` citation inside the recency
  window. `alternatives` is how community voice gets enforced structurally rather than
  stylistically; `enabling-now` is the defense against "they have been asking for this for
  fifteen years."
- A **DEFINITION** that a gap depends on needs at least two `competing` rival definitions and
  an `excludes`. A definitional gap with no rivals on the record is unfalsifiable — this is
  the single highest-severity check in the system.
- Every paragraph in `draft.md` carries `<!-- claims: ... -->`, and every numeral,
  comparative and citation marker in it must appear in a bound claim. Paragraphs with no
  claims are `FRAMING` and may contain no numerals, comparatives, proper nouns of
  programs/institutions, or citations. That closes the framing escape hatch mechanically.

## Blind review, and the audit you must not waste

Three reviewers (program, skeptic, conformance) score the same draft against the frozen
rubric in isolation. The reviewer and the reviser never share a context; an adjudicator
mediates. A reviewer that finds history or prior scores in its context must stop and report
contamination. A score with no located instance is void.

The **cross-family audit** runs a different model family over a blinded packet. It is scarce,
so do not spend it on "read my paper and tell me what you think." **Spend it auditing the
reviewers, not the draft.** Scored against the same frozen rubric, it becomes a calibration
audit of your whole panel, and that compounds: a patterned divergence on a rubric item is a
defect in the *item*, not a fact about the draft, and it feeds the amendment queue. Run it in
the same blind, offline configuration as the internal panel, or you are measuring the
configuration rather than the model.

Do not fix the draft to close a divergence. The divergence is information about the
measuring instrument.

## Escalate on suspicious success

Score is never a stop condition. It is a diagnostic. Read an iteration record
right-to-left — verdict first, score last — and escalate when:

| Trigger | Why |
|---|---|
| Scores rise while checker findings stay flat | Textbook reward hacking. Not progress. |
| Reviewers converge high with low variance | Three blind reviewers agreeing closely on a contested item share a blind spot. |
| Large diff, small score delta, no issues closed | The loop is rewriting, not improving. |
| Issue-class exhaustion in under two rounds | The rubric is not discriminating. |
| A reviewer reports a rubric item it could not apply | A rubric defect. Feed the queue rather than guessing a 3. |

Stop on **issue-class exhaustion** — a full round surfacing no new *taxonomy class*. Three
more instances of a class you already have is not novelty. Also stop on any halt and any
regression. When you stop, say why, and do not summarize optimistically. If the loop stopped
because it was going in circles, write that down.

## The finals build

Order matters: **filter, render, then judge.**

1. Filter the prose tells first (em-dashes especially). Changing a protected line's
   punctuation is a human-authorized protected-text change, and the pin gets updated to the
   new wording so the check keeps guarding it.
2. Render at the smallest allowed font via a pinned reference document, so formatting is
   reproducible rather than incidental.
3. Render a real PDF **headlessly**. Do not drive a word processor through GUI automation: it
   steals focus and will capture keystrokes into the document.
4. **Then** measure the page limit against the rendered PDF. Word-count estimates were badly
   wrong in practice — roughly 5.6 estimated pages against about 7 actual. Measure the number
   the call actually constrains, which usually excludes references and figures.

## Starting a new paper

1. Copy `template/` to the working directory. Read `PORTING.md` and re-populate the
   venue-specific parts: rubric item R-08, enforcer check E-16, the style-anchor exemplars.
2. Decode the solicitation first — `template/SOLICITATION-DECODING.md`. Mechanical gates and
   merit rubric, before any drafting.
3. Write the seed essay yourself. Hash-lock it. Pin its sharpest formulations in
   `03-state/protected.md`.
4. Fill `03-state/corpus.md` and cache full text for span verification.
5. Run the extractor against the seed. **Read the holes, not the claims.** Then G1.

`example-synthetic/` is a small invented instance that reads CLEAN on every check; run
`python3 template/tools/enforce.py --root example-synthetic`, then break it on purpose and
watch the check that catches it. The two real instances the method came from are submitted
papers and are not distributed here; `template/PORTING.md` records what diffing them showed.

## Honest limitations

- **It is slow, and the human is the bottleneck by design.** The gates need a domain expert.
- **The checker cannot judge quality.** It verifies structure and provenance, not whether the
  argument is good. Semantic quality is delegated to blind review and to the human. That is a
  division of labor, not an oversight.
- **Verification has a ceiling** — see above. Provenance is checkable; entailment is not.
- **Closed-corpus friction is real.** You cannot cite what you have not ingested, so evidence
  gaps surface as explicit work items instead of silent paraphrases.
- **Claim-first authoring feels rigid.** Rewriting a paragraph may mean editing the graph
  first. The payoff is traceability; the cost is spontaneity.
- **It does not remove bias or error. It makes them auditable.** A determined human can still
  admit a weak claim, and the log will show that they did.

## Provenance of this skill

This comes from one project: two ESAS 2028 Decadal Survey white papers written between
2026-07-16 and 2026-08-24, 36 and 46 logged iterations, both submitted. The method note the
authors wrote at the time is `docs/process_document.md`. External review of the Retrievals
paper scored 4/4 on both of the call's highest-weighted content metrics with all six gates
passing.

Treat it as engineering practice that held up under one project's own scrutiny, not an
established empirical finding. The portable/venue-specific seam is the best-evidenced claim
here, because the two instances were diffed: the operating contract, failure taxonomy and
stopping rules were byte-identical across both, and the amendment load fell from eleven to
four on the second run. The weakest claim is that the method *caused* the review scores; there
was no control, no unaided draft of the same paper to compare against, and n=2.
