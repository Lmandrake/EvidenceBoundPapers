# EvidenceBoundPapers

**Papers in which every claim is traced to evidence and checked by a machine.**

A language model can write a fluent scientific paper in minutes. Nothing in that fluency
tells you which sentences are true. A citation can be invented, a quotation can be
paraphrased into something the source never said, and a revision loop that grades its own
work will report steady improvement while it smooths a sharp, correct claim into nothing.

This repository is a harness for writing AI-assisted science that can be audited. The
argument lives in a typed **claim graph**: definitions, gaps, remedies, asks, conceded
tensions, and the evidence supporting each one. The prose is only a rendering of that graph.
A **deterministic checker** that calls no model, and that the model may not edit, enforces
the rules:

- every citation resolves to a closed corpus, so a citation cannot be made up;
- every quoted span is found character for character in the cited source's cached text;
- every numeral and citation in a paragraph comes from a claim bound to that paragraph;
- connective prose carries no numbers, comparatives, names or citations;
- a gap names who decides, what they decide and the metric that moves;
- a remedy shows its rejected alternatives and a recent enabling result;
- no recommendation rests on an unevidenced link;
- no claim is accepted without a human's logged decision;
- protected human-written text is never silently dropped;
- a check that passed last run and fails now halts the loop.

Blind reviewers score the draft against a frozen rubric, and a human rules at four gates.
The method produced two submitted white papers. In both, a domain expert then found claims
whose quotes were verbatim but whose scope outran the source, while the checker read clean.
That limit is stated up front (see `SKILL.md`, "the ceiling of verification"), and the
evidence audit that answers it ships as a template file, with a filled-in example in
`example-synthetic/04-log/evidence-audit.md`.

## Quickstart (60 seconds, Python 3.9+ standard library only)

```bash
git clone https://github.com/Lmandrake/EvidenceBoundPapers && cd EvidenceBoundPapers
python3 template/tools/enforce.py --root example-synthetic
#   verdict=CLEAN  passed=21/21 applicable (0 n/a)
python3 -m unittest discover -s tests          # 44 checker tests
```

`example-synthetic/` is an **invented** two-page paper on deep-ocean heat content, with
invented sources, so the whole graph can be read in five minutes. Now break it. Change one
word inside a quoted span in `example-synthetic/03-state/claims.md`, for example "one in ten"
to "one in twenty", and run the checker again:

```
verdict=HALT  passed=19/21 applicable (0 n/a)
REGRESSION newly failing: E-02
```

The report in `example-synthetic/04-log/enforcer-report.md` names the claim and the source
the quote was not found in. Each check's failing case is a test in `tests/test_enforce.py`.
(Running the checker updates the example's report and log files; `git checkout
example-synthetic` restores them.)

## The verification suite

The checker covers one place a confident falsehood gets into a document. Five companion
skills in `skills/` cover the others. They are written for an AI coding agent such as Claude
Code (each `SKILL.md` is the entry point), and read just as well as checklists for a person.

| Skill | The failure it catches |
|---|---|
| `confident-wrong-numbers` | A query whose shape returns a plausible wrong number: a count, a zero, an empty list, an all-None field |
| `measuring-large-artifacts` | A number taken from a file too large to read whole, where grep and wc mislead |
| `verify-model-quotes` | A model quotation, or the page, section or line it cites, that does not exist in the source |
| `claim-provenance` | A claim encoded as knowledge before anyone confirmed its source is real, was read, and says what you think |
| `grader-validation` | A scorer, oracle or guard that reports a clean verdict because it cannot see the fault |

They run from cheapest to deepest: the first three check a value against its source,
`claim-provenance` checks the source, and `grader-validation` checks the instrument doing the
checking. See `skills/README.md`. Their own tests need `pytest` (and `jq` for one), and run
from each skill's directory. Skills they mention but that are not in this repo
(`knowledge-registry`, `incomplete-ground-truth`, `evaluation-independence`,
`falsifiable-claims`) are neighbours, not dependencies.

## Layout

```
SKILL.md                 the method: loop, gates, checks, limits
docs/
  process_document.md    the methodology note written during the first paper, with citations
  voice-guide.md         the prose style guide the drafts were held to
template/                copy this to start a paper
  PORTING.md             what travels to a new venue and what you must re-populate; read first
  SOLICITATION-DECODING.md  turn a call for papers into mechanical gates and a merit rubric
  CLAUDE.md              the agent operating contract: twelve hard rules, all halt conditions
  01-spec/               the frozen reward function: taxonomy, rubric, claim schema, checks
  02-agents/             nine role briefs (extractor, gap scout, drafter, blind reviewers, ...)
  03-state/ 04-log/      empty scaffolds with the required formats
  tools/                 enforce.py (the checker), export_packet.py, build-final.sh
example-synthetic/       an invented instance that passes every check
tests/                   the checker's tests
skills/                  the verification suite
```

## Starting a paper

Copy `template/`, read `template/PORTING.md`, and decode your call with
`template/SOLICITATION-DECODING.md` before writing anything. Write the seed essay yourself and
pin its best sentences in `03-state/protected.md`. Fill `03-state/corpus.md` and cache each
source's full text in `03-state/corpus-text/` so its quotes can be verified. Then run the
extractor and read the holes, not the claims. `SKILL.md` walks the whole loop.

The honest costs: it is slow, a domain expert has to rule at the gates, and the checker
verifies structure and provenance, never whether the argument is good.

## Credit

Please credit me if you find this work useful.
