# Claim schema  (FROZEN — v1.0)

The claim graph is the paper. This file defines its grammar.

> **Template note.** Roles, required components, strength grades, FRAMING restrictions and
> the binding rule all travel. The `## Evidence-table fields — G1′ additive extension` block
> near the end was added mid-run for one paper; treat it as an option, not a default. See
> `../PORTING.md`.

## Two axes

**Structural role** — what the node does in the argument.
**Evidence tag** — how a SUPPORT node is grounded. Only SUPPORT nodes carry one.

### Roles

| Role | ID prefix | Purpose |
|---|---|---|
| `DEFINITION` | `DEF-nn` | A stipulation the argument depends on. Contestable, not citable. |
| `GAP` | `GAP-nn` | A root. Something the field cannot currently do. |
| `REMEDY` | `REM-nn-m` | An approach that would close GAP-nn. |
| `ASK` | `ASK-nn-m` | The addressed-to-agency recommendation flowing from REM-nn-m. |
| `SUPPORT` | `SUP-nnnn` | An evidenced proposition attached to a DEF / GAP / REMEDY / TENSION component. |
| `TENSION` | `TEN-nn` | A named tradeoff, risk, or limitation the paper concedes. Added at G1 (AMD-002). |
| `FRAMING` | — | Connective prose. Not tracked as a claim. Heavily restricted (see below). |

### Evidence tags (SUPPORT only)

| Tag | Extra obligation |
|---|---|
| `empirical` | ≥1 corpus citation with a quoted supporting span |
| `causal` | citation + explicit mechanism or identification note. Auto-flagged if the cited support is correlational only. |
| `comparative` | named baseline **and** named metric. "Outperforms" without both is illegal. |

### Strength

`Strong` / `Suggestive` / `Asserted`. Assigned by the evidence-binder, confirmed
by the human at admission.

- `Strong` — direct corpus evidence, quoted span, no interpretive leap
- `Suggestive` — indirect, analogical, single-source, or contested
- `Asserted` — no corpus evidence. Legal for DEFINITION. Everywhere else it is a debt.

The strength grades exist for exactly one check: **no ASK may reach a GAP through
an Asserted node.** That is the whole point of grading here. Do not elaborate it
into an evidence assessment; this paper is not one.

### Status

`proposed` → `accepted` | `rejected` | `dnq` | `superseded`

Only a human writes `accepted`. `dnq` = does-not-qualify, kept on the record so
the loop stops re-proposing it.

---

## Required components by role

A node is **complete** when every required component is present and non-empty.
Incomplete nodes cannot be rendered. Incomplete GAP nodes halt the loop.

### DEFINITION — `DEF-nn`

| Component | Requirement |
|---|---|
| `competing` | ≥2 rival definitions in current use, each named and sourced |
| `excludes` | what this definition explicitly rules *out*, stated positively |
| `why-decision-relevant` | why this cut is the one that matters for the decisions at issue |

> A definitional root makes the gap *entailed* rather than discovered. This is
> the most attackable node type in the graph. Argued well, it is the paper's
> strongest section. Left implicit, it is the first thing a panelist attacks.

### GAP — `GAP-nn`

| Component | Requirement |
|---|---|
| `scope` | corpus examined, time window, queries used, date of search. Must be reproducible by a reader. |
| `nearest-miss` | ≥3 closest existing works, each with an exclusion rationale: what it does, and precisely why it does not close the gap |
| `magnitude` | what is lost / mispredicted / uncharacterized. Quantified where possible. |
| `incidence` | ≥1 **named** decision-maker, the specific decision, and the decisional metric. Categories ("water managers", "the community") are not names. |
| `tractability` | why this is solvable within the decade |

> A gap claim cannot be proved by citation — you cannot cite a paper for the
> nonexistence of papers. Its evidence is the `scope` statement plus the
> `nearest-miss` set. That pair is what makes a gap reproducible rather than
> asserted, and it is what separates a prioritized gap from the ninety-nine
> other asserted gaps in the pile.

### REMEDY — `REM-nn-m`

| Component | Requirement |
|---|---|
| `mechanism` | the technical approach, specifically |
| `enabling-now` | what changed that makes this the decade. ≥1 citation inside the recency window (default: 5 years). |
| `precedent` | partial or adjacent demonstrations that it can work |
| `yield` | which **named components** of GAP-nn close, and how far. "Addresses GAP-nn" is not a yield. |
| `alternatives` | ≥2 other approaches considered, each with exclusion rationale |
| `cost-class` | research program / instrument / mission line / observation continuity |

> `alternatives` is where community voice is enforced structurally rather than
> stylistically. A remedy with one candidate approach reads as advocacy no matter
> how the prose is toned.
>
> `enabling-now` is the mechanical defense against the panel's fastest reason to
> deprioritize: "they have been asking for this for fifteen years."

### ASK — `ASK-nn-m`

| Component | Requirement |
|---|---|
| `addressee` | the agency or body being asked |
| `action` | what specifically to do |
| `parent` | `REM-nn-m`, which must be complete and attached to a complete GAP |

### TENSION — `TEN-nn`  (added G1, AMD-002)

| Component | Requirement |
|---|---|
| `text` | the tradeoff/risk/limitation, stated in one sentence as a concession the paper owns |
| `bears-on` | which node(s) it qualifies, e.g. `REM-04-1` or `GAP-06` — the thing whose adoption carries this cost |
| `disposition` | how the paper answers it: mitigation, scope limit, or explicit residual risk accepted |

> A TENSION is not a GAP (it is not something the field should fund closing) and
> not a REMEDY (it proposes nothing). It is the "honest about tension" requirement
> made structural: a decadal paper with no conceded tradeoff reads as a sales
> document. SUPPORT may attach to a TENSION (e.g. evidence that generative
> posteriors can themselves be miscalibrated). A TENSION carries no ASK and is not
> on any ASK→REMEDY→GAP path, so it never triggers the Asserted-path check.

### SUPPORT — `SUP-nnnn`

| Component | Requirement |
|---|---|
| `parent` | the node **and component** it supports, e.g. `GAP-03/magnitude` |
| `tag` | `empirical` \| `causal` \| `comparative` |
| `cite` | ≥1 corpus key |
| `span` | verbatim quoted text from the cited source that supports the claim |

---

## FRAMING restrictions

A paragraph with no claim IDs is FRAMING. FRAMING prose may not contain:

- numerals or quantities
- comparatives or superlatives ("better", "most", "leading", "few", "largely")
- proper nouns naming programs, systems, missions, or institutions
- citation markers

Anything that needs one of those is not framing; it is an unbound claim.

## Binding rule (paragraph-level)

Every paragraph in `draft.md` ends with a binding comment:

```
<!-- claims: GAP-03, SUP-0117, SUP-0118 -->
```

or

```
<!-- claims: FRAMING -->
```

Every numeral, comparative, and citation marker in a bound paragraph must appear
in one of that paragraph's bound claims. This is mechanically checkable and is
the main defense against the FRAMING escape hatch.

---

## Ledger block format

`03-state/claims.md` is a flat list of these blocks. Keys are literal and
lower-case. Order is fixed. The enforcer parses this strictly; do not improvise
format, do not add keys, do not reflow.

```
### GAP-03
- role: GAP
- status: proposed
- strength: Suggestive
- parent: DEF-01
- text: <one sentence, the claim itself>
- scope: <corpus / window / queries / date>
- magnitude: <...>
- incidence: <named person or office | decision | metric>
- tractability: <...>
- nearest-miss:
  - NM-03-1 | <corpus-key> | <what it does> | <why it does not close the gap>
  - NM-03-2 | <corpus-key> | ... | ...
  - NM-03-3 | <corpus-key> | ... | ...
- notes: <optional>
- history: 2026-07-16 proposed by gap-scout
```

```
### SUP-0117
- role: SUPPORT
- status: proposed
- strength: Strong
- tag: empirical
- parent: GAP-03/magnitude
- text: <one sentence>
- cite: <corpus-key>
- span: "<verbatim text from the source>"
- history: 2026-07-16 proposed by evidence-binder
```

```
### REM-03-1
- role: REMEDY
- status: proposed
- strength: Suggestive
- parent: GAP-03
- text: <one sentence>
- mechanism: <...>
- enabling-now: <...> [cite: <corpus-key>]
- precedent: <...> [cite: <corpus-key>]
- yield: GAP-03/magnitude — <how far>; GAP-03/incidence — <how far>
- alternatives:
  - ALT-03-1-a | <approach> | <why not>
  - ALT-03-1-b | <approach> | <why not>
- cost-class: <...>
- history: 2026-07-16 proposed by gap-scout
```

## Evidence-table fields — G1' additive extension (2026-07-18, human-authorized)

Added mid-run on the first paper, under expert direction (AMD-011). Most are optional keys on any
node, and the parser tolerates unknown keys. Two are enforced: **E-20** requires a `claim-type` on
every non-SUPPORT claim rendered in the draft, and **E-21** requires a `generalization-boundary` on
any rendered claim of type `inferred-from-shared-architecture`.

| Field | Meaning |
|---|---|
| `claim-type` | one of: `directly-demonstrated` \| `supported-by-multiple-cases` \| `inferred-from-shared-architecture` \| `proposed-recommendation` \| `unresolved-hypothesis` |
| `domain` | scientific domain (e.g. atmosphere/composition, land/hydrology, precipitation/cryosphere) |
| `product` | the retrieval or product the claim concerns (e.g. OCO-2 XCO2, SMAP soil moisture) |
| `generalization-boundary` | the explicit limit of the claim — what it does NOT cover |
| `known-counterargument` | the strongest objection a skeptic would raise |
| `wording-limitation` | required wording constraint (e.g. "regime-level not per-observation coverage") |
| `downstream-consequence` | the science/operational consequence if the gap is unaddressed |
| `recommendation-supported` | which ASK/remedy this claim feeds |
| `citation-completeness` | status of citation support (e.g. complete / span-verified / pending-source) |

Discipline (enforced by review until AMD-011 is applied): reject or rewrite any claim that
generalizes beyond its `generalization-boundary`, lacks a mechanism where one is asserted, conflates
retrieval vs representation error, rests only on aggregate validation for a per-regime reliability
claim, or cites a source that does not directly support the stated proposition. An inference must not
be written as a direct measurement — set `claim-type` honestly.

## Granularity

One claim = one thing a reviewer could disagree with independently.

Target 40–80 nodes for a 7-page paper; expect the upper end once REMEDY branches
are populated. At 150 you are transcribing, not claiming. At 15 the binding check
is vacuous.
