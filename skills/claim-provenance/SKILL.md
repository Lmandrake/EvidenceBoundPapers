---
name: claim-provenance
description: >
  Decide whether a claim may be encoded as knowledge: its source is real, was read, and says (and
  scopes) what you think. Use whenever writing a rule, weight, statistic or citation into a
  knowledge base, registry, rubric or skill; citing a famous work from memory; a source is
  paywalled or unobtained; claiming "true even if I can't source it"; auditing citations; a
  reviewer says a claim over-generalizes or misattributes; a figure was quoted second-hand; or a
  span checker says all verified. Not registry structure (knowledge-registry) or wording
  (falsifiable-claims).
---

# Claim Provenance

A claim's weight comes entirely from its source being real and saying what you think it says.
Strip that away and an encoded rule is just an assertion wearing a citation. The failure this
skill guards against is quiet: you recall a canonical work, you write it down as authority, and
the record now implies a verification that never happened. The claim may even be true — that is
what makes the shortcut tempting and what makes it fabrication anyway.

The expensive version is not "I made something up." It is "I encoded something I half-remembered,
tagged it with a real DOI, and a reader six months later trusted it *because* it was cited." A
dangling or unread citation is worse than no citation, because it manufactures confidence.

## When this fires

Any moment you are about to move a claim from "I believe this" into a durable artifact someone
else will trust as sourced — a principle with a `sources:` field, a weight, a threshold, a
statistic in prose, a "[Author, Year]" in a document. It fires the instant you notice you are
citing from memory rather than from a file open in front of you. It also fires when the file *is*
open: having the exact passage does not settle whether the passage supports the claim you are
about to write on top of it. And it fires **backwards**: when a knowledge base already exists and
you are asked whether its citations hold, audit them against what was actually acquired and read.

## The protocol

**1. Verify before you encode — read the source, do not recall it.**
Before a claim earns a citation, retrieve the source and confirm the specific claim is present in
the returned text: the title/venue/authors/year, or the exact result you are leaning on.

*Why:* recalling a famous work from memory and citing it is fabrication even when the work exists,
because you have not checked it supports *this* claim. Reputation is not evidence. The lineage
ledger states the standard plainly: verification means the claim "was actually present, not on a
search snippet," and search hits that returned unrelated results "are treated as NON-evidence."

**2. A verbatim quote proves the words exist, not that the source supports your claim's scope.**
Having the exact passage in front of you is where verification *starts*. Read the quote alone,
then read the claim alone, and ask whether the passage entails the claim at the scope the claim
asserts. Grade the support `direct` / `partial` / `adjacent`, and read the sentences around the
quote before you accept it.

*Why:* this is the ceiling of provenance checking, and it is easy to mistake for the floor. In
the source project a machine checker verified every quoted span byte-for-byte against cached
source text and reported CLEAN, while a human expert found systematic over-claiming underneath
it. One claim quoted a systematic review exactly — "calculations were only performed for data
visualization purposes" — and rendered it as the field "commonly stalling at the visualization
layer." The source's *next sentence* says numerical simulation was the most common function.
The quote was real, the attribution was right, and the claim contradicted the paper it cited.
A second claim attributed a market projection to the paper that quoted it rather than to the
vendor that produced it, turning secondhand into primary. Neither is a provenance failure, so
no provenance check can catch either.

Three specific shapes to refuse: a subset clause generalized to the population; an aggregate
result used for a per-case guarantee; and a quote whose own sentence is fine but whose section
is arguing the opposite. When a source supports something narrower than you want to say, the
move is to narrow the claim, not to soften the citation.

**3. Record acquisition status, not just a citation.**
For every source, log whether you actually obtained it. A source you could not get is
`reference_only`: usable to acknowledge a lineage, never as authority for a rule.

*Why:* a citation with no acquisition record is indistinguishable from a fabricated one after the
fact. In this project S14 and Cleveland & McGill (1984) sat behind a paywall and were "marked
`reference_only`. Their ideas are used only where an accessible Tier-A source corroborates them"
— the marking is what lets a later reader tell borrowed authority from earned authority.

**4. Mark the unverified explicitly, and leave it unencoded.**
When you cannot confirm a source, say so in the record and encode nothing from it — do not invoke
it on reputation because "everyone knows it."

*Why:* this is the load-bearing precedent. A canonical, universally-cited work was logged NOT
VERIFIED and, per the rule, "left unverified and is **not encoded** anywhere in the taxonomy or
rubric." The honest move is to record the gap and add a re-verify note, not to let a well-known
title borrow authority it did not earn in this record.

When you are auditing *backwards* — a record already exists and claims a source is "not
encoded" — do not trust that self-report. Grep the unverified title (and any id derived from it)
across the encoded artifacts — taxonomy, rubric, principle registry — and confirm it truly
appears nowhere as authority. A record's claim about its own discipline is itself a claim, and
verifying it is the whole job of the backward pass.

**5. Tier your evidence and let the tier govern the force.**
Attach an evidence tier at the point of encoding (peer-reviewed / institutional practice / expert
synthesis / example) and let it decide how hard the claim may push. A hard rule needs a strong
tier; expert synthesis and examples support preferences, not mandates.

*Why:* it "prevents taste from masquerading as law." Stating the tier where the claim lives means
a later reader can re-weigh it instead of inheriting your confidence blind. Reserve the hard force
for the claims whose sourcing can carry it.

**6. Distinguish evidence from inference from assumption — in the text itself.**
Write which is which. "The source shows X" and "X plausibly follows" and "we assume X" are three
different objects and must read as three different objects.

*Why:* collapsing the three is exactly how an assumption acquires the authority of a finding. Once
the seams are invisible, a downstream reader cannot tell what was measured from what you guessed,
and will cite your guess as though it were the study.

**7. Make every cited id resolve — check it with a script, not by reading.**
Before the artifact is trusted, mechanically confirm every citation and every internal id points
at something real. Grep the ids against the registry; do not eyeball them.

*Why:* a knowledge base whose citations dangle is worse than one with none, because the dangling
id implies a verification that never happened. Reading cannot prove a negative across a hundred
ids; a script can. The registry check here confirmed "all 90 principle IDs cited across the skills
and eval docs exist in the registry — zero dangling references," and even caught that a two-id
`QA-01/03` slash-notation read as one — the kind of miss a human scan waves through.

## When a machine gathers evidence a human will adjudicate

The software collects candidates; a person decides. Then machine filtering must not destroy the
human's ability to see what was found, or what was rejected and by whom.

**Keep candidate evidence and adjudicated knowledge in separate states** — a candidate is worth
looking at, knowledge is something someone ruled on. Collapsing them lets an unreviewed machine
output acquire the standing of a decision, which is rule 4's tier problem by another road.

- **Preserve rejected candidates and their disposition**, retention permitting, recording *who or
  what* rejected each and *why*. A successor who cannot see what was ruled out re-proposes it; an
  unattributed rejection is indistinguishable from a bug.
- **Ranking may advise; it may not silently drop the tail.** That is a decision taken on the
  human's behalf.
- **Never rank on a signal you have not checked against correctness.** Measured: a model's
  confidence was *higher* on its fabricated quotations than its real ones (figures removed
  until results are published), so the most available signal would have promoted the worst candidates.
- **Test the boundary that stops an advisory tool emitting a verdict.** A vocabulary that cannot
  spell the verdict cannot reach one by accident.

⚠️ **Do not ship the strong version: "never delete, rank, or reach a verdict."** The project that
coined it refuted it on itself — its accumulate-only store reached **6,552 candidates**, over a
hundred hours of expert attention that was never going to happen, so a filtered sheet of a few
hundred had to be built anyway. Refusing to rank buried everything rather than protecting anyone's
judgment. **The durable rule is inspectability, not abstinence:** rank and prune as the job needs,
but keep what was found, what was dropped, and who dropped it visible.

## Failure modes

**Reputation laundering.** A famous work is cited without being read, so its fame stands in for
verification. Prevented by rule 1, made visible by rule 4's explicit NOT-VERIFIED record.

**Span-verified overclaim.** The quote is exact, the attribution is right, and the claim still
says more than the passage supports — a subset read as a population, an aggregate read as a
per-case guarantee, a sentence read against the grain of its own section. Provenance verified,
entailment assumed. This is the failure that survives a byte-exact checker, so only rule 2
catches it.

**Citation laundering by proximity.** A source *quotes* a figure from somewhere else and the
quoting paper becomes the cited authority. The number is real, the trail is one hop short, and
a vendor projection acquires the standing of peer review.

**The `reference_only` leak.** A source correctly marked unacquired still gets quoted as authority
for a specific rule. The marking is only worth what your discipline in respecting it is worth.

**Tier inflation.** An example or a synthesis gets encoded as a MUST. The force outruns the
evidence, and taste ships as law.

**Silent seams.** Evidence, inference, and assumption are merged into one confident sentence. No
one downstream can pull them apart, so the weakest link inherits the strength of the strongest.

**Dangling id.** A cited id does not resolve — a typo, a renamed principle, a slash-list the
regex splits wrong. The citation implies a check that cannot be performed.

## Rationalizations that mean stop

| Thought | What is actually true |
|---|---|
| "Everyone cites this, it's fine" | Reputation is not verification. If it is canonical it will survive being read; until then it is unverified and stays unencoded. |
| "I'm confident that's what the paper says" | Confidence is not the text. Open the source and confirm the specific claim, or do not cite it. |
| "The quote is verbatim, so the claim is sourced" | Verbatim proves the words exist. It says nothing about scope. Read the passage alone and ask whether it entails the claim you are making; grade it direct, partial or adjacent. |
| "The source is about this topic, so it supports this point" | Topical overlap is not support. A paper can be squarely about your subject and still state the opposite of your claim two sentences later. |
| "A checker verified every span, so the citations are sound" | A span checker verifies provenance, never entailment. Both papers that shipped from this discipline carried over-claims while the checker read CLEAN. |
| "I'll add the real citation later" | The claim ships now and outlives the intention. An unsourced claim encoded today is a fabricated one until the day that never comes. |
| "The claim is true even if I can't source it" | Then encode it as an assumption at its true tier, not as a sourced finding. Truth you can't attribute is not evidence. |
| "It's only a soft heuristic, so sourcing matters less" | A SHOULD still carries a tier and a source; a reader trusts soft rules too. Lower force is not license to fabricate. |
| "The ids look right to me" | Eyeballing can't prove a hundred ids resolve. Grep them; the miss you can't see is the one that bites. |

## Worked example: an unverified canonical source, left unencoded

This repository contains a real instance of rules 1, 3 and 4 firing, and it is worth reading rather than
paraphrasing.

While building an analytical-question taxonomy, a well-known foundational work — Wilkinson's
*Grammar of Graphics* — was a natural background citation. But it could not be confirmed in-sandbox:
the exact-title reference page did not exist and searches "returned no usable confirmation of the
edition/venue." Rather than cite it on reputation, it was logged **NOT VERIFIED** and, explicitly,
"left unverified and is **not encoded** anywhere in the taxonomy or rubric," with a standing note to
"re-verify against a primary source ... before any load-bearing use." Compare the sources that *were*
seen in retrieved text (FT Visual Vocabulary, Mackinlay's APT, Draco): each carries a VERIFIED status
tied to a specific fetch. The ledger separates the two classes on purpose, and the paywalled sources
in `SOURCES.md` (S14; Cleveland & McGill 1984) sit in a third, `reference_only`, class.

The ledger itself lives in the sibling MandrakeVisualize repository and is not shipped here.
In that repository, read, in order:
- `sources/lineage-analytical-questions.md` — the verification ledger; the NOT-VERIFIED entry and its handling
- `sources/SOURCES.md` — the acquisition ledger; access tiers and the `reference_only` marking
- `synthesis/DECISIONS.md` — decision D8: paywalled/unacquired sources are `reference_only`, never encoded from memory
- `principles/principles.yaml` — the schema header (`evidence_tier` semantics) and the note that no source or DOI in the file is fabricated
- `DEPLOY_BRIEF.md` — the registry-integrity requirement that every cited id resolve, checked by grep before commit

## Boundaries with neighbouring skills

- **`knowledge-registry`** — designs the *structure* that holds sourced claims: the schema, the id
  scheme, how a principle records its tier and sources. This skill governs *whether a claim is
  entitled to go in* — it decides admissibility, not layout.
- **`falsifiable-claims`** — words a comparative result and sets the refutation bar. This skill is
  upstream of that: it asks whether the underlying source-claim was real and read before any result
  is worded on top of it.
- **`evidence-bound-papers`** — runs a whole authoring loop on top of this discipline: a closed
  citation corpus, byte-exact span checks, and human admission gates. It is the *machinery*; this
  skill is the judgment the machinery cannot supply, because a checker can verify that a span is
  verbatim but never that the source supports the claim's scope. Its
  `example-synthetic/04-log/evidence-audit.md` shows rule 2's audit format on an invented claim.
- **measurement-from-large-artifacts** (the sibling covering numbers extracted from files too large
  to read in full) — governs trust in a value pulled from a big artifact. This skill governs trust
  in a *source citation*. A number that was correctly extracted still needs its source verified
  before it is encoded as authority.

## Provenance of this skill

These practices come from one project's sourcing discipline — a single-domain corpus of ~28 fetched
sources, a verification ledger, a `reference_only` convention for paywalled works, and a registry
whose ids were grepped to zero dangling references. They are engineering practice that held up under
that project's own scrutiny, not an established empirical finding. The NOT-VERIFIED-and-unencoded
precedent in particular was a deliberate choice made once, on one canonical work; treat it as a
worked habit, not a proven law.

**Rule 2 comes from a second project** and is the best-evidenced item here, because it comes from a
failure rather than a success. Two ESAS 2028 white papers were written against a closed corpus with
every quoted span checked byte-for-byte by a deterministic checker; a domain expert then found
systematic scope overreach in both while that checker reported CLEAN, including one claim that
contradicted the source it quoted. The `direct` / `partial` / `adjacent` grading and the
evidence-table-before-prose discipline were adopted in response, mid-project, and are recorded as
that project's amendment AMD-003. Two instances found by one expert on one pass is enough to
establish that span verification has a ceiling; it is not enough to tell you how often the failure
occurs, so treat the *ceiling* as the finding and the grading scheme as the reasoned response to it.
