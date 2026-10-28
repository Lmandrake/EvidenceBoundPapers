# Enforcer spec  (FROZEN — v1.0)

> **Template note.** Every check here is venue-neutral **except E-16**, which is currently
> filled for the ESAS 2028 RFI. Derive your own E-16 with `../SOLICITATION-DECODING.md`
> before the rubric lock at G2 — see `../PORTING.md`.

The enforcer is the only dependable feedback channel in this system. Revision
guided by model judgement alone is unreliable and can degrade quality; revision
guided by a grounded check is what actually works. Everything that can be checked
mechanically must be, and must be checked by code — not by an agent reading
carefully.

## Implementation rule

**The enforcer is a script, not an agent.**

On first run, generate `enforce.py` from this spec. Thereafter:

- No agent may edit `enforce.py`'s check logic. Ever.
- No agent may call an LLM from inside a check.
- No agent may interpret, soften, or contextualize a HALT.
- If a check is wrong, that is a *spec amendment request*
  (`04-log/rubric-amendments.md`), applied by a human between sessions.

All state is markdown so the checks stay simple: parse the fixed block format in
`claims.md`, the binding comments in `draft.md`, the key table in `corpus.md`.
Nothing here needs a database.

The enforcer writes `04-log/enforcer-report.md`, overwriting it each run, and
appends a one-line summary to `04-log/iterations.md`.

---

## Severity

- **HALT** — the loop stops. Escalate to human. No agent may proceed.
- **BLOCK** — the affected node cannot be rendered; the loop continues elsewhere.
- **WARN** — logged, surfaced to the adjudicator, does not stop anything.

---

## Checks

### Evidence integrity

**E-01 · Citation resolves** — HALT
Every `cite:` key exists in `03-state/corpus.md`. No exceptions, no near-matches.

**E-02 · Span is verbatim** — HALT
Every `span:` appears character-exact in the source text indexed for that key
(normalize whitespace only). If the source text is not available locally, the
span cannot be verified: mark the claim `Suggestive` and WARN. Never mark
`Strong` on an unverifiable span.

**E-03 · Comparative completeness** — BLOCK
A claim with `tag: comparative` requires a named baseline and a named metric in
`text:`. (Ratified at G2, AMD-003: the check applies to comparative-TAGGED claims
only. A bare trigger word such as a descriptive "state-of-the-art" quoted inside an
empirical claim's span is not a comparative claim by this paper and does not fire.)

**E-04 · Causal discipline** — BLOCK
`tag: causal` requires a mechanism or identification note. WARN additionally if
the cited span contains observational-design markers
(`observed|associated|correlat|linked to`) with no accompanying mechanism.

### Binding

**E-05 · Named incidence** — BLOCK
`GAP.incidence` must match `<name-or-office> | <decision> | <metric>` with three
non-empty segments. Reject a name segment matching a category wordlist
(`decision-makers, stakeholders, the community, end users, managers, planners,
practitioners, operators, users`).

**E-06 · Paragraph binding** — BLOCK
Every paragraph in `draft.md` carries a `<!-- claims: ... -->` comment.
For bound paragraphs: every numeral, comparative/superlative, and citation marker
in the paragraph appears in at least one bound claim's `text` or `span`.
For `FRAMING` paragraphs: no numerals, no comparatives, no program/mission/
institution proper nouns, no citation markers.

### Gap discipline

**E-07 · Gap completeness** — HALT
Every `status: accepted` GAP has non-empty `scope`, `magnitude`, `incidence`,
`tractability`, and ≥3 `nearest-miss` entries each with a non-empty exclusion
rationale (4th pipe field). `scope` must contain a date and a query string.

**E-10 · Definitional dependency** — HALT
Any GAP whose `parent` is a DEF requires that DEF to have ≥2 `competing` entries
and a non-empty `excludes`. *This is the single highest-severity check in the
system.* A definitional gap with no rival definitions on the record is an
unfalsifiable gap.

### Remedy discipline

**E-08 · Remedy completeness** — BLOCK
Every accepted REMEDY has non-empty `mechanism`, `enabling-now`, `precedent`,
`yield`, `cost-class`, and ≥2 `alternatives` each with an exclusion rationale.

**E-09 · Yield specificity and reachability** — BLOCK
`yield` names at least one specific `GAP-nn/<component>`, not a bare `GAP-nn`.
Graph reachability: every accepted ASK → REMEDY → GAP. Every accepted SUPPORT
reaches a GAP or DEF. Orphans are BLOCK.

**E-12 · Enabling-now recency** — BLOCK
`enabling-now` carries ≥1 `cite:` whose corpus entry has a year within the
recency window. Default window: 5 years. Set in `corpus.md` header.

### Path strength

**E-11 · Advocacy tokens** — WARN
Institution/program proper nouns appearing in `ASK.action` or in any FRAMING
paragraph. Maintain the wordlist in `corpus.md` header.

**E-17 · Asserted load-bearing path** — BLOCK
No accepted ASK may reach its GAP through a node with `strength: Asserted`,
except where that node is a DEF that passes E-10.

### Loop health

**E-13 · Churn** — WARN
Diff ratio between `draft-v(N-1)` and `draft-vN` exceeds 0.35 with zero
`issues.md` status transitions. Report ratio and transition count.

**E-14 · Regression** — HALT
Any check that passed at iteration N-1 and fails at N. Report both states.
**Never auto-fix a regression.** It is the primary evidence that the loop is
making the paper worse while reporting that it is better.

**E-15 · Protected text** — HALT
Every entry in `03-state/protected.md` appears verbatim in `draft.md`, or has an
explicit human-approved release recorded in `04-log/decisions.md`.

**E-16 · Call conformance** — BLOCK
Page/word budget, required section presence, reference-count limits, and format
constraints from the actual call. **Populate these before the first run** — they
are the only checks in this file that depend on the specific solicitation.

*Populated for ESAS 2028 (RFI) at G2 — 2026-07-16. Source of truth: the call's
own RFI guidelines, FAQs and reviewer-metrics gate section (venue documents,
not shipped with this template). These are the
mechanical gates; the merit judgment lives in the rubric (R-08) and the reviewer
metrics file.*

- **E-16.1 length** — BLOCK. Body text ≤ 7 pages, single-spaced, ≥11-pt,
  excluding figures/tables/references. The draft is markdown so page count is
  estimated, not authoritative: enforce a proxy word budget of **≤ 4,900 words of
  body text** (≈700 words/page × 7), counting only rendered prose paragraphs
  (exclude the references section, binding comments, headings, and figure
  captions). Emit the word count every run. Treat 4,900–5,300 as WARN (proxy
  slack; a human confirms true page count in the typeset version) and > 5,300 as
  BLOCK. Font/spacing are not checkable in markdown — they are a G4 human check,
  noted here so they are not forgotten.
- **E-16.2 response type declared** — BLOCK. The draft must contain, in its first
  section, an explicit statement of response type — one of
  `science-target` / `implementation` / `contextual-topic` / `combination`.
  Check: a line matching `response type:` (case-insensitive) with one of those
  values. *This paper's declared type is `contextual-topic` (measurement
  infrastructure / data stewardship / AI-readiness); see decisions.md G1.*
- **E-16.3 sphere named** — BLOCK. The draft must name ≥1 NASA sphere
  (`Atmosphere`, `Biosphere`, `Cryosphere`, `Geosphere`, `Hydrosphere`) or an
  explicit cross-sphere justification. Check: at least one sphere token present,
  or a line matching `cross-sphere`.
- **E-16.4 required sections present** — BLOCK. For a contextual-topic paper the
  rendered draft must contain sections satisfying: (a) the issue/opportunity and
  its significance to the community; (b) actionable priorities/considerations for
  the Survey; plus the paper's own required scaffolding: a thesis/executive
  section and a references section. Check by heading presence against the
  architect's `03-state/structure.md` section list (every section marked
  `required: yes` there resolves to a heading in the draft).
- **E-16.5 reference-count / corpus closure** — BLOCK. Every citation marker in
  the draft resolves to a corpus key (this is E-01 applied at the prose layer; the
  RFI sets no hard reference cap, so there is no upper limit here — only the
  closed-corpus rule). WARN if the references section lists a key never cited in
  body prose (orphan reference) or cites a key absent from the references section.
*Implementation status in `tools/enforce.py`: E-16.1, .2, .3 and .5 are mechanical.
E-16.5 recognises a citation marker by shape (a lower-case key ending in a year), so a
marker such as `[ghost]` is left to review. E-16.4, .6 and .7 are not implemented and
are carried by the conformance reviewer and the human at G4.*

- **E-16.6 agency target** — WARN (judgmental; primary detection is R-08). Flag
  occurrences of `NOAA`, `USGS`, or `commercial` in an `ASK.action` where they are
  the *addressee* rather than context — ESAS 2028 recommendations target NASA's
  Earth Science Division; other agencies are context only. This is a soft signal
  to the adjudicator, not a hard block, because context-vs-subject is a judgment
  the reviewer (R-08) owns.
- **E-16.7 content-safe** — WARN. Surface any occurrence of `ITAR`,
  `proprietary`, `SBU`, or `export-controlled` as a string for human check.
  Submissions are posted publicly; this is a reminder flag, not an adjudication.

**E-18 · Admission integrity** — HALT
No claim's `status` moved to `accepted` without a matching entry in
`04-log/decisions.md`: its id on a `- accepted:` line (ranges such as
`SUP-0001..0012` expand). A mention anywhere else, such as `- pending:`, is not an
admission. Agents cannot admit claims. This check is what makes that rule real
rather than aspirational.

**E-19 · Tension completeness** — BLOCK (accepted only; added by AMD-002)
An accepted TENSION has non-empty `text`, `bears-on` and `disposition`, and
`bears-on` names at least one node that exists.

**E-20 · Rendered claim declares a type** — BLOCK (added by AMD-011)
Every non-SUPPORT claim bound to a paragraph of the draft declares a `claim-type`.

**E-21 · Inference states its boundary** — BLOCK (added by AMD-011)
A rendered claim of type `inferred-from-shared-architecture` has a non-empty
`generalization-boundary`, so an inference cannot read as a measurement.

---

## Report format

`04-log/enforcer-report.md`, overwritten each run:

```
# Enforcer report
- run: <ISO datetime>
- draft version: v007
- verdict: HALT | BLOCKED | CLEAN
- halts: 1 | blocks: 4 | warns: 2
- checks passed: 14/21

## HALT
- E-10 | GAP-00 | parent DEF-01 has 0 competing definitions (needs 2)

## BLOCK
- E-05 | GAP-02 | incidence segment 1 is a category: "urban planners"
- E-07 | GAP-04 | 1 nearest-miss entry, needs 3
...

## WARN
- E-13 | churn 0.41, issue transitions 0

## Delta vs previous run
- newly failing: none
- newly passing: E-03
```

The `Delta` block is the section to read first. Newly-failing is a regression and
should never be non-empty without a halt beside it.
