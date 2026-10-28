# Porting this template to a new venue

Everything in `template/` came out of two completed ESAS 2028 Decadal Survey white papers.
Most of it is venue-neutral. This file lists the parts that are not, so you can tell at a
glance what must be re-populated before a new run and what should be left alone.

The split is not a guess. The two instances that produced the shipped papers were diffed:
`CLAUDE.md`, `01-spec/failure-taxonomy.md` and `01-spec/stopping-rules.md` were
**byte-identical** across both, while `rubric.md`, `claim-schema.md` and `enforce.py`
differed. That is the seam.

## Leave alone — portable as-is

| File | Why it travels |
|---|---|
| `CLAUDE.md` | The operating contract. Identical across both instances. Only the twelve hard rules matter, and none of them mention a venue. |
| `01-spec/failure-taxonomy.md` | Failure classes F1–F7 with detection procedures. Identical across both instances. The taxonomy outlives any one paper, and the rubric derives from it. |
| `01-spec/stopping-rules.md` | Stop conditions, suspicious-success triggers, cross-family audit doctrine, gate list. Identical across both instances. |
| `02-agents/*` | Nine role briefs, context topology, hard separations. Resist adding a tenth role. |
| `tools/export_packet.py` | Builds blinded review packets. Paper-agnostic by design; both instances shared it unmodified. |

## Re-populate before the first run

### `01-spec/rubric.md` — item **R-08** only

R-01 through R-07 derive from the failure taxonomy and travel unchanged. **R-08 is the
call's own requirements** and is currently filled for the ESAS 2028 RFI (contextual-topic
lens, fiscal realism against the 2018 Program of Record, "what over how", right-agency).
Replace the `### R-08 populated for …` block and its anchor table with your venue's merit
criteria. Keep the four-level behavioural anchors; do not switch to numeric descriptions.

### `01-spec/enforcer-spec.md` — check **E-16** only

E-01 through E-15 and E-17 through E-21 are venue-neutral. **E-16 is the only check that
depends on the specific solicitation** — the spec says so itself. The current E-16.1–.7 are
ESAS 2028: a ≤7-page body word proxy, a declared response type, a named NASA sphere,
required sections, corpus closure, agency target, content-safe tokens. Rewrite these from
your own call. Derive them with `SOLICITATION-DECODING.md` before you touch anything else,
because the rubric lock (G2) freezes them.

### `01-spec/style-anchor.md` — the exemplar and anti-exemplar passages

`## Voice` and `## Prohibited moves` travel. **`EX-1`–`EX-4` and `AX-1`–`AX-2` do not.**
EX-1–EX-3 are short attributed passages from ESAS 2017 exemplar white papers; EX-4 is the
Retrievals seed's own voice. Replace them with 3–5 passages from accepted papers in *your*
venue plus your own writing. This section is the drift detector, not decoration: a reviewer
cannot detect register drift against a description of good voice, only against a sample.

### `01-spec/claim-schema.md` — the G1′ additive extension

The roles, required components, strength grades, FRAMING restrictions and binding rule all
travel. The `## Evidence-table fields — G1′ additive extension` block was added mid-run for
one paper under expert direction. It is genuinely useful (`claim-type`,
`generalization-boundary`, `known-counterargument`). Checks E-20/E-21 enforce two of its
fields on rendered claims; the rest are optional. To drop them, remove E-20/E-21 at G2
as a recorded amendment.

### `tools/enforce.py` — three ESAS-specific spots

The checker is generated from `enforcer-spec.md` and is otherwise generic, but grep for:

- the **E-16 implementations** — word budget, response-type regex, sphere tokens, required
  sections. All venue-specific.
- **`identifier-tokens:`** in `03-state/corpus.md` (read into `MISSION_TOKENS`) and the
  `Level N` strip: false-positive suppressors for numeral tracing in E-06. A mission name
  such as `Probe-2` would otherwise contribute a bare "2" that no claim contains. List your
  domain's names there; the code holds none.
- the **citation-key regex** — the Retrievals instance widened it to `[A-Za-z0-9_]+` because
  its keys contain underscores.

### `tools/build-final.sh`

The pipeline is right (filter em-dashes → render DOCX at the smallest allowed font → render
a real PDF headlessly → *then* measure pages on the rendered PDF). The venue-specific inputs
are outside the script: the masthead in `00-seed/masthead.md`, the font and margins in a
pandoc reference document (`EBP_REFERENCE_DOCX`), the page limit (`EBP_PAGE_LIMIT`) and an
optional review folder (`EBP_REVIEW_DIR`). The author-year reference conversion is generic
but simple; check it against your venue's style. Keep the order.

## One correction to carry forward

Nothing in `01-spec/` catches a claim whose quoted span is verbatim but whose *scope*
outruns the source. Both shipped papers had instances of this, found by a human expert while
the checker read CLEAN. An **evidence audit** is the mechanism that was invented in
response (`example-synthetic/04-log/evidence-audit.md` shows the format), and it is worth adopting from the start rather than after an
expert catches you. See the `Verification has a ceiling` section of the skill.
