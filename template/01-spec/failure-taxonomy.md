# Failure taxonomy  (FROZEN — v1.0)

The rubric derives from this file, not from generic quality dimensions.
Rubrics built from a failure taxonomy outperform generic agent-as-judge scoring
by a wide margin, because each item carries a **detection procedure** rather than
a description of goodness.

Every item below has: an ID, what the failure looks like, how to detect it, and
whether detection is mechanical (`E-nn`, enforcer) or judgmental (`R-nn`,
reviewer). Prefer mechanical. Every item that moves from R to E is a permanent
improvement to this system.

---

## F1 — Voice and standing

**F1.1 Institutional pitch in community clothing**
The paper argues for a program or an institution rather than for the field.
*Detect (R):* Would this sentence survive if the author's institution were
deleted from existence? If it becomes incoherent or loses its ask, flag.
*Detect (E-11):* institution/program proper nouns in ASK.action or in FRAMING.

**F1.2 Advocacy disguised as assessment**
A single approach is named and no alternatives are considered.
*Detect (E-08):* REMEDY with fewer than 2 `alternatives` entries.

**F1.3 Attributed exemplar leakage**
A named program is used as the worked example in a way that reads as a bid.
*Detect (R):* is the example carrying the argument, or carrying the flag?

## F2 — Stakes and specificity

**F2.1 Generic stakeholder**
"Decision-makers", "the community", "water managers", "end users".
*Detect (E-05):* GAP.incidence contains no named person, office, or program of
record; or contains no decisional metric.

**F2.2 Decision without a metric**
A named user is given, but nothing they measure changes.
*Detect (E-05):* incidence field lacks the `| metric` segment.

**F2.3 Impact asserted, not traced**
"This would transform X" with no path from the remedy to the stake.
*Detect (E-09):* REMEDY.yield does not name specific GAP components.

## F3 — Evidence integrity

**F3.1 Phantom citation**
A citation key that resolves to nothing, or a real paper that does not say it.
*Detect (E-01, E-02):* key not in corpus; `span` not found verbatim in source.

**F3.2 Overclaim beyond the span**
The claim says more than the quoted span supports.
*Detect (R):* read the span alone. Does it entail the claim text? If it needs a
step, the claim is `Suggestive` at best, not `Strong`.

**F3.3 Correlation asserted as causation**
*Detect (E-04):* `tag: causal` with no mechanism note, or with a cited span whose
own design is observational/correlational.

**F3.4 Comparative with no baseline**
"Outperforms", "state of the art", "better than existing methods".
*Detect (E-03):* `tag: comparative` lacking a named baseline or named metric.

**F3.5 Unbound assertion**
A numeral or comparative appears in prose with no claim behind it.
*Detect (E-06):* token in a bound paragraph not present in any bound claim.

## F4 — Gap discipline

**F4.1 Unscoped gap**
"Little work exists on X." Where did you look? When? With what query?
*Detect (E-07):* GAP.scope missing or lacking corpus/window/query/date.

**F4.2 Missing nearest-miss**
The three closest papers are not named, so the reader cannot tell whether the
author looked or simply did not know.
*Detect (E-07):* fewer than 3 `nearest-miss` entries, or any entry missing its
exclusion rationale.

**F4.3 Strawman exclusion**
The nearest-miss is dismissed on a property it does not claim.
*Detect (R):* does the exclusion rationale engage the work's actual claim, or a
weaker one?

**F4.4 Definitional gap presented as empirical**
The gap follows from the author's own definition and would vanish under a
different one, and this is not acknowledged.
*Detect (E-10 + R):* GAP whose parent is a DEFINITION, where the DEFINITION lacks
`competing` entries. **This is the highest-severity item in the taxonomy.**

**F4.5 Merely topical vs. genuinely novel**
The nearest-miss set lists papers that share vocabulary rather than papers that
share the problem.
*Detect (R):* would the nearest-miss author agree they were trying to do this?

## F5 — Remedy discipline

**F5.1 Perennial ask**
The remedy has been requested for a decade and nothing changed.
*Detect (E-12):* `enabling-now` has no citation inside the recency window.

**F5.2 Mechanism-free remedy**
"Invest in trustworthy AI." Not a mechanism.
*Detect (R):* could a program manager write a solicitation from this sentence?

**F5.3 Cost-class silence**
The paper asks without indicating scale, so the panel cannot place it.
*Detect (E-08):* `cost-class` empty.

**F5.4 Yield inflation**
The remedy claims to close more of the gap than the precedent supports.
*Detect (R):* compare `yield` against `precedent`. Is the extrapolation named?

## F6 — Argument structure

**F6.1 Buried lede**
The verdict is not in the first paragraph of its section.
*Detect (R):* read only the first sentence of each section. Do you have the
argument?

**F6.2 Orphan node**
A claim renders but reaches no gap; or a gap has no remedy; or a remedy has no ask.
*Detect (E-09):* graph reachability.

**F6.3 Asserted load-bearing path**
An ASK reaches its GAP only through an `Asserted` node.
*Detect (E-10):* path strength check.

**F6.4 Scope creep**
The paper argues a sixth gap in passing that it does not support.
*Detect (E-06 + R):* unbound comparatives in the discussion sections.

## F7 — Loop pathology

*These are failures of the system, not the paper. The adjudicator watches for them.*

**F7.1 Reviewer convergence without enforcer movement**
Rubric scores rise while `enforcer-report.md` findings are flat.
*This is reward hacking.* Escalate. Do not celebrate.

**F7.2 Churn**
Large diff, small score delta, no issues closed.
*Detect (E-13):* diff ratio above threshold with no `issues.md` transitions.

**F7.3 Unanimity**
Three blind reviewers agree closely on a contested item.
Treat as a red flag, not a green one. Escalate for cross-family audit.

**F7.4 Regression**
A previously-passing check fails.
*Detect (E-14).* Halt. Never auto-fix.

**F7.5 Register drift**
Successive revisions pull the prose toward generic LLM voice — hedged, balanced,
smooth, and saying less. This is the failure that judges reliably miss, because
generic prose scores well on every rubric item except the one nobody wrote down.
*Detect (R, style-anchor):* compare against `01-spec/style-anchor.md` exemplars.
Also *detect (E-15):* protected text silently dropped.
