# Style anchor  (FROZEN — v1.0)

> **Template note.** `## Voice` and `## Prohibited moves` travel unchanged. The exemplar
> passages `EX-1`–`EX-4` and anti-exemplars `AX-1`–`AX-2` do **not** — EX-1–EX-3 are short
> attributed passages from ESAS 2017 exemplar papers and EX-4 is one paper's own seed voice.
> Replace them with samples from your venue. See `../PORTING.md`.

Register drift is the failure that judges reliably miss. Successive revisions pull
prose toward generic model voice — hedged, balanced, smooth, and saying less —
and generic prose scores well on every rubric item except the one nobody wrote
down. This file is the one nobody wrote down.

## Voice

**Community position, not institutional pitch.** The paper speaks as the field
assessing itself. Recommendations are addressed to the Decadal and the agencies
collectively. Prior investment appears as shared community context, not as "our
program." Institutional exemplars stay unattributed; the concrete case carries
the argument.

Test: delete the author's institution from the world. Does the paper still work?

**Verdict first.** Lead with the conclusion, support with reasoning. Never open a
section with background. The first sentence of each section, read alone and in
sequence, should give a panelist the whole argument.

**Lucid-first (author directive, 2026-07-17; amended at G1' 2026-07-18 — the opening
*declaration* was removed at that gate, but the lucid-first PRACTICE stays: keep the plain
verdict sentence before the dense support in each section; simply do not include the meta "note on
method" paragraph that announces it).** This paper makes a deliberate stylistic choice: most
decadal white papers
pursue dense, rigorously logical prose for professionalism, but that density often
obscures the point and forces reviewers through a complex argument before any
punchline is made clear. This paper keeps all of that logical analysis and linkage
— the rigor is not reduced — but it *additionally* uses short, lucid passages of
plain prose to make each thesis unmistakably clear **before** rigorously supporting
it. So the shape within a section is: (1) a clear plain-language statement of the
point, in a sentence a non-specialist could repeat; then (2) the dense, fully
bound, evidence-backed argument beneath it. This is not "verdict first" as a
one-liner followed by density — it is a genuine lucid layer that coexists with the
rigorous layer. Do not let revision smooth the lucid sentences back into hedged
technical prose; their plainness is the point. The paper says it is doing this, so
the reader is not surprised to find both registers.

**Honest about tension.** Name the tradeoff, the risk, and the thing that would
falsify the claim. A paper with no acknowledged tension reads as a sales
document, and panels have read a lot of sales documents.

**Precision over hedging.** "Few fielded systems" is a claim and needs a scope
statement. "Some might argue" is not a position. If a sentence would survive
being wrong, it is not saying anything.

## Prohibited moves

- Hedging that removes falsifiability ("may potentially help in some contexts")
- Balance for its own sake — presenting a rival view you do not actually credit
- Enthusiasm as argument ("exciting", "transformative", "revolutionary",
  "unprecedented")
- Summary paragraphs that restate the section they end
- Transitions that carry no information ("Furthermore," "It is important to note")
- Abstraction ladders — three sentences of generality before the point
- The word "robust" without a named property that is robust to a named
  perturbation

## Exemplar passages

> **Populate this section before the first run.** Paste 3–5 passages: from real
> accepted Decadal white papers, and from your own writing that lands the way you
> want. These are what the reviewer compares against for F7.5.
>
> The reviewer cannot detect drift against a description of good voice. It can
> detect drift against a sample. This section is not optional decoration; it is
> the detector.

### EX-1 — Lee et al., "Sea Surface Salinity Continuity" (ESAS 2017 RFI-2 exemplar) — quantified requirement with rationale
```
The accuracy requirement for SSS is 0.15 psu for SSS anomalies on monthly and 1° scales and
0.1 on 10° scale, averaged over the global ocean. Defining the accuracies for anomalies as
opposed to absolute SSS (akin to altimetry-derived sea level anomalies instead of absolute sea
level) is more fundamental to studying spatiotemporal changes of the ocean. These accuracy
requirements, already achieved by Aquarius V4.0 SSS, serve as the baseline requirements for a
future satellite salinity mission.
```
Why it works: every number carries a unit, a scale, and a reason the number is *that* number, tied back to an achieved heritage baseline — this is the traceability chain M2/M3 rewards, verdict-first.

### EX-2 — Nerem et al., "Advancing Sea Level Science" (ESAS 2017 RFI-2 exemplar) — stakes named and quantified, not asserted
```
According to the 2014 U.S. National Climate Assessment, global average sea level will rise between
6 and 33 cm in the next 20 years. The socioeconomic importance of coastal infrastructure and
population centers threatened by SLC cannot be overstated; over a hundred million people live in
densely-populated regions within 1 m of present day mean sea level and even a rise of 20 cm will
have profound impacts on these communities as flood risks and return frequencies of extreme
events increase.
```
Why it works: importance is grounded in a cited external report with quantities, not in the adjective "critical"; the stake is a measured consequence, not a mood.

### EX-3 — Hardesty et al., "Global Wind Profiles" (ESAS 2017 RFI-2 exemplar) — engages the rival capability on its own terms
```
While there has been a long history of deriving AMVs with passive techniques, and the approach
discussed in Maschhoff et al. 2015 is very promising, a space-based DWL stands alone in being able
to provide direct wind measurements. This is especially important in the tropics where passive
techniques cannot infer the divergent component of the wind.
```
Why it works: names the strongest rival approach, credits it fairly, then states precisely the one thing it cannot do — a steelmanned nearest-miss exclusion, not a strawman.

### EX-4 — your own seed — the register to hold (protected formulations)
```
Deep ocean heat content is only as trustworthy as the thermometers that measure it. Below
2000 m we rely on floats that are almost never recovered, and we correct them with one
adjustment for the whole fleet.
```
*(Placeholder from the invented `example-synthetic/` seed. Replace it with the sharpest
lines of your own seed essay.)*
Why it works: short declarative verdicts, a named falsifiable failure mode, and a distinction stated exactly — this is the voice the loop must not smooth away (see `03-state/protected.md`).

## Anti-exemplars

### AX-1 — institutional advocacy in community clothing (constructed)
```
Our team's pipeline is uniquely positioned to deliver the calibrated Level 2 uncertainty products
the community needs. Building on our institution's decade of investment in retrieval science, we
propose that the Survey prioritize continued support for this effort, which has already
demonstrated leadership in the field.
```
Why it fails: delete the author's institution and the ask collapses — the recommendation is shaped around who receives the money, not around a field-wide measurement need (F1.1). "Uniquely positioned," "leadership," "the community needs" are the tells.

### AX-2 — fluent generic model prose (the drift attractor) (constructed)
```
It is important to note that uncertainty quantification is a critical and multifaceted challenge that
may potentially help improve a wide range of downstream applications. A robust, holistic approach
that carefully balances the many important considerations could offer significant benefits and
represents an exciting opportunity for the community going forward.
```
Why it fails: hedged past falsifiability ("may potentially," "could offer"), enthusiasm as argument ("exciting"), "robust" and "critical" with no named property, zero quantities or named stakes — smooth, balanced, and saying nothing. This is the F7.5 attractor; score it against the samples above, not against your sense of good writing.
