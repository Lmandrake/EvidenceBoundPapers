---
name: grader-validation
description: >
  Validate the instrument that GRADES your work, not just the work itself — a scorer, oracle,
  guard, witness, or checker whose job is to certify correctness or detect fabrication. Use this
  whenever you are about to trust "0 lost", "0 violations", "0 spurious", "all tests pass", or
  any other clean verdict from a comparator you built; before adding a mutation-testing suite,
  a containment scorer, a fabrication witness, or an identity key used to match two structures;
  whenever a grading pipeline reports a suspiciously stable or suspiciously clean number across
  a change that should have moved it; and whenever you are designing the check itself rather
  than the thing it checks. Not for a descriptive query lying about the world (use
  confident-wrong-numbers) and not for scoring against reference data known to be incomplete
  (use incomplete-ground-truth) and not for keeping the builder away from the answer key (use
  evaluation-independence).
---

# Grader Validation

A scorer, oracle, guard, witness, or checker can be structurally blind to an entire class of
defect. When it is, it does not error and it does not warn — it reports **zero** for that class,
forever, and zero reads identically to clean. The failure is never in the code under test; it is
in the query that was supposed to catch the code under test failing. In one project this
happened at least **eight separate times**, each independently, each caught only by someone
asking what the check could not see rather than what it said.

## When this fires

The moment you write a comparator, oracle, guard, or witness — anything whose output is a
verdict about correctness rather than a fact about the world. It fires again every time that
instrument reports a clean result on a change that should plausibly have broken something. A
"0" from a grading pipeline is not evidence until you can say what shape of defect that zero
would still report if the defect were real.

## The protocol

**1. Give every identity key the same collision-freedom you would demand of a primary key.**
A containment scorer keyed families by `clause_number`; 182 of 255 structures had none at all,
so an entire fabrication class was invisible to the instrument built to certify its absence. Once
the key was fixed to something collision-free, the same corpus showed 156 children with more
than one parent — each one a fabricated citation the old key could never surface. A second
instance in the same codebase keyed child identity on the enumerator letter alone, so every
family's `a` collided with every other family's `a`, producing "225 contradictory parents out of
243 edges" — a number that measured nothing but the collision.

*Why:* a non-unique key does not fail loudly. It silently merges two things that should stay
distinct, and the merge looks exactly like agreement.

**2. A membership test cannot see cardinality.**
A scorer asked only "is each expected child present" — so a child emitted TWICE passed, reporting
0 lost, 0 spurious, when a duplicated edge is a fabricated containment claim. The fix was to
compare multisets and report duplication as its own column, not to fold it into the presence
check.

*Why:* presence and count are different questions. Whenever the failure mode you actually care
about is repetition rather than absence, a set-membership test is blind to it by construction.

**3. Name the dimension your invariants do not bound, before trusting "0 violations".**
A fabrication witness checked that an enumerator is printed at the child's own span, that the
child follows its parent, that no heading intervenes, that siblings share one family — all
strictly LOCAL properties. Nothing bounded DISTANCE. A parent that adopted a child 152 blocks and
twelve pages later satisfied every local invariant, and the witness reported clean on 304 and 121
edges. An independent third reader then refuted 6 of those exact edges.

*Why:* a bundle of local checks can be individually correct and jointly insufficient. Before
believing "0 violations", list what a violation would have to look like on the one axis — scope,
distance, ordering, cardinality — that none of the invariants constrain. That axis is where a
defect is invisible by construction, not by bad luck.

**4. Validate the property a guard protects, not the token it currently checks for.**
A read-only-source guard was implemented as "this module's text must not contain the string
`write_text(`". That guard could have been satisfied by a docstring containing the literal
string with no code change at all. The honest fix moved the I/O out of the module entirely, so
the property held regardless of what string search anyone ran against it.

*Why:* a guard that greps for a token is checking a proxy for the property, not the property.
Satisfying the grep and satisfying the intent are different acts, and the gap between them is
exactly where a "passing" guard stops meaning anything.

**5. Prove every guard fires — and confirm the mutation can reach the branch meant to catch it.**
An 11-mutation negative corpus drove each fabrication invariant with the shape that should
violate it. It earned itself immediately: a mutation that substituted a neighbouring stem for a
child escaped the first checker entirely, because that block recorded no printed enumerator, so
the comparison it needed was silently skipped — and the boundary scan ran strictly BETWEEN parent
and child, so it never inspected the child block itself. A guard never observed failing has not
been tested; a mutation that cannot reach the branch it targets proves nothing about that branch.

*Why:* a checker can hold a branch that looks like protection and is dead code with respect to
every input your test suite happens to generate. Only a deliberately-broken input, confirmed to
route through that exact branch, tells you the branch does anything.

**6. A clean pass is evidence against ONE failure class, not correctness.**
An invented item that is plausible, correctly labelled, and correctly placed satisfies every
invariant a witness can check. Pin that limitation in a test rather than leaving it implied, so
the next reader does not read "clean witness" as "verified true".

*Why:* a witness answers the question it was built to ask. Restating that scope in a test is what
stops a future reader from silently widening the claim to a question it never asked.

**7. Measure paired directions together, or a fix in one direction reads as success alone.**
A duplicate-suppression fix on child identity became a similarity test and started absorbing
genuine siblings whose bodies opened with the same long phrase — closing the fabrication
direction while opening the loss direction. It was caught only because zero-duplication and
zero-loss were asserted in the same test, side by side.

*Why:* almost every fix to a checker has two failure directions it could now produce — one it
closes and one it can newly open. Testing only the direction you were fixing hides the other one
completely.

**8. An aggregate is not a check on the thing beneath it.**
A corpus-wide binding total moved 549 → 548 across a real fix, while roughly 55 individual items
changed class underneath it — over-attribution and under-attribution present together and nearly
cancelling. Assert the specific thing you care about; a stable summary statistic can sit directly
on top of significant churn.

*Why:* summaries compress by design. A number that looks unchanged tells you the sum is
unchanged, never that the parts are.

**9. The measuring harness gets the same scepticism as the thing it measures.**
A bisect loop chained `git worktree add && cd` but ran its measurement after a bare `;`, so when
the checkout step failed, the measurement silently ran in whatever directory was already
current — nearly publishing a false regression from a commit that had touched nothing but
documentation. It was caught only because that commit could not possibly have changed behaviour.

*Why:* a harness is code, and code that computes the number you are about to trust needs the same
"what would make this lie" question as the grader it drives. Print the state it believes it is
in, and assert that belief before trusting the output.

## Rationalizations that mean stop

| Thought | What is actually true |
|---|---|
| "It reports 0, so nothing is wrong" | Zero is what a blind instrument says too. Name the failure class the check would report as zero if it were real, before believing the zero. |
| "The tests all pass, the suite is solid" | A suite that has never seen a wrong implementation has been run, not tested. Mutate the code and require it to notice. |
| "The invariants all hold, so the structure is real" | Local invariants bound local properties. Say which global property — distance, scope, cardinality — nothing checks. |
| "The key looks fine, it's just a label" | A label reused as an identity key is a collision waiting for two things that share it. Check for collisions before trusting a comparison built on it. |
| "The aggregate didn't move, so nothing changed" | It can hide equal and opposite churn. Assert the specific thing, not the number standing next to it. |
| "I fixed the false positive, ship it" | Check whether the fix opened a false negative. Assert both directions in the same test. |
| "The guard's been there for months, it must work" | A guard nobody has watched fail has not been proven to fire. Break the thing on purpose and confirm the rejection. |

## Worked example: eight weak-link failures in one grading pipeline

This comes from one project's containment-scoring and fabrication-witness work — a system that
had already measured its own component against seven independent oracles and a third-reader
probe, and whose grading machinery, not the parser under test, was the repeat point of failure.
Read it as a single instance of the general shape: every rule above traces to a distinct incident
in this one pipeline, discovered in this order.

- A `clause_number`-keyed scorer that could not see 156 fabricated multi-parent edges (rule 1).
- An enumerator-letter-keyed comparator that manufactured "225 contradictory parents" of noise
  (rule 1, second instance).
- A presence-only scorer that passed a duplicated child edge as zero loss, zero spurious (rule 2).
- A fabrication witness whose local invariants were silent on distance, reporting clean on two
  edges an independent reader then refuted (rule 3).
- A read-only guard satisfiable by a string in a comment (rule 4).
- A checker branch for "unclassified content intervenes" that upstream filtering made
  structurally unreachable, discovered only once a mutation corpus tried to hit it (rule 5).
- A duplicate-identity fix that traded fabrication for loss, caught only by asserting both
  directions together (rule 7).
- A bisect harness that silently measured the wrong checkout after a failed `cd`, nearly
  publishing a false regression (rule 9).

No single fix generalized to the next incident. What did generalize is the standing question:
*before believing this check's zero, what would this check still report if the defect it exists
to catch were real?*

## Boundaries with neighbouring skills

- **`confident-wrong-numbers`** — a query lying about a fact in the world (a count, a census, a
  `grep`). This skill is the case where the lying query is itself the grading instrument for a
  correctness claim, not a fact-finding one — the distinction that decides which skill to reach
  for, and the two compound: a grader built from a bad query inherits both failure classes.
- **`incomplete-ground-truth`** — the reference data your grader compares against is honestly
  incomplete, and the grader must not read "not asserted" as "refuted". This skill is about the
  grader's own logic being blind to a defect class regardless of how complete its reference is;
  a perfect oracle can still be scored by a broken comparator.
- **`evaluation-independence`** — keeps the material that builds a thing separate from the
  material that judges it, so the grade is not circular. This skill assumes independence already
  holds and asks whether the independent grader itself is *correct* — a non-circular grader can
  still be structurally blind.
- **`falsifiable-claims`** — brackets what a comparative claim is entitled to say given the
  evidence. This skill is upstream of that: it is about whether the evidence-producing instrument
  itself can be trusted before any claim is worded.

## Provenance of this skill

This is engineering practice from one project's containment-scoring and fabrication-detection
work, where the grading machinery — not the extractor it was built to check — was demonstrably
the weaker link at least eight separate times, each found by a different route (a review, a
held-out oracle, a third-reader probe, a deliberate mutation, a bisect gone wrong). It is not a
general theorem about graders; it is what survived one project's repeated discovery that its own
checking code needed checking as much as the thing it checked.
