# Decoding a solicitation before you write

Do this first, before the seed, before the corpus, and long before any prose. The output is
two things the loop needs and cannot invent for itself:

- **mechanical gates** — everything about your submission that a script can check, which
  becomes enforcer check E-16
- **a merit rubric** — what a skillful response looks like to *this* venue, which becomes
  rubric item R-08

Both are frozen at gate G2. Getting them from the call rather than from intuition is what
stops the target moving later to fit whatever you produced.

## Why a separate step

A rubric assembled from generic quality dimensions scores fluent prose well. A rubric
assembled from a venue's own stated criteria, and from a taxonomy of how submissions to that
venue *fail*, discriminates. Every rubric item should carry a **detection procedure**, not a
description of goodness — that is the difference between "is the gap credible?" and "does the
scope statement name the corpus, the window, the queries and the date?"

## Assemble the source set

Collect into one directory, then read it as a set rather than one document at a time:

1. **The call itself** — the RFI/RFP/CFP text. Authoritative for content structure and
   format. Quote its content requirements verbatim into your notes; paraphrase drifts.
2. **The venue's FAQ or Q&A** — usually where eligibility, page-count exclusions, and *how
   submissions are actually evaluated* are stated more plainly than in the call.
3. **The organizing body's own framing document** — study approach, task statement, terms of
   reference. Tells you what the committee thinks its job is.
4. **The prior cycle's output** — the last report, or its report-in-brief. This is the
   framework a new submission is expected to build on, and the vocabulary the panel already
   has.
5. **Lessons-learned or best-practice literature** for this class of venue. How committees
   actually prioritize, what decision rules they use, what they discount.
6. **"How not to write one"** community guidance, if it exists. Failure lists are worth more
   than success lists.
7. **Exemplars — real accepted submissions from a prior cycle.** These are the highest-value
   item and the most commonly skipped. They are your few-shot samples for structure, register
   and the traceability chain, and they populate the style anchor.

## Produce three artifacts

Write these as files next to the source set, and cite the source document for every
requirement so a later reader can check you did not invent one.

**1. Definition of a skillful response.** A distilled statement of what the venue wants:
purpose and audience, the response types and how to label one, the required content points
quoted from the call, the framing that lands well here, and the framing that lands badly.
Name the audience precisely — writing to be *usable by a committee* is different from writing
to be published.

**2. Reviewer metrics.** The venue's own scoring definition, made explicit: hard gates that
disqualify, then weighted merit metrics. Keep gates and merit strictly separate — a
submission that busts the page limit is not a low-scoring submission, it is an inadmissible
one. Reserve this file for the final gate and the cross-family audit; do not hand its numeric
bands to a blind reviewer mid-loop, because it is a second rubric and will contaminate the
panel.

**3. Prose quality metrics.** How this venue's prose reads when it is working. Feeds the
style anchor's exemplars and the register-drift check.

## Then translate into the two frozen objects

**Into E-16 (mechanical, in `01-spec/enforcer-spec.md`).** Everything checkable:

- length, in the unit the call actually constrains — note carefully what is *excluded* from
  the count (references, figures, tables, cover page), because that exclusion is usually the
  binding detail
- required sections, keyed to your own `03-state/structure.md`
- any declaration the call demands (response type, topic area, category) as a literal string
  the checker can find
- reference and citation rules, including whether closure is required
- addressee correctness, if the call targets a specific body
- content-safety strings the venue forbids, given that submissions may be posted publicly

**Into R-08 (judgmental, in `01-spec/rubric.md`).** Everything that needs a reader: whether
the submission reads as community consensus rather than parochial advocacy, whether it is
realistic about cost and portfolio position, whether it argues the need rather than mandating
an implementation, whether the ask is actionable and self-contained. Write four behavioural
anchors, not numeric descriptions.

## The test

You are done when a person who has not read the call could take your three artifacts and
correctly reject a non-compliant draft. If a requirement lives only in your head, it is not
in the reward function, and the loop cannot enforce it.
