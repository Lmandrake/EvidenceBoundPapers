# verify-model-quotes

A Claude Code skill for one failure class: **a language model returns a
quotation and a page citation, and neither is real.** Not a garbled quote — a
fluent, verbatim-looking, confidently-cited passage that is indistinguishable
from a true finding by reading it.

Measured over a corpus of governance PDFs: a nonzero share of returned quotes
were not in the source at all, the model's self-reported confidence was *higher*
on the fabricated ones, and many of the fabrications were the model quoting the
question back as though it were a passage from the document. (Figures removed
until results are published.)

`SKILL.md` covers the reframe that makes the skill worth loading — this is
**source-span verification, not quote existence**, because a boilerplate
sentence on three pages verifies against a document-wide check while the
citation is still wrong — the architecture that avoids generated quotations
entirely (model selects a stable span ID, your code reconstructs the text), the
eight-item checklist for when generated quotes are unavoidable, and the
verifier's own catalogued defects: scaffolding in the haystack that discarded
seven real findings, an over-loose normalization that manufactured a false
reinstatement, and why an appeal must re-verify with a *different*
implementation.

It deliberately does **not** cover whether the source is trustworthy or whether
the claim is supported. Only whether the text and the cited place exist.

## Install

The skill is a directory; Claude Code finds it through `~/.claude/skills/`.
Clone or check out this repo somewhere permanent and symlink it in:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/verify-model-quotes ~/.claude/skills/verify-model-quotes
```

Editing the checkout edits the installed skill; there is no build step. It
pairs with `grader-validation` (the general case of an instrument that grades
your work and lies), `incomplete-ground-truth` (recall, which this skill does
not measure) and `evidence-bound-papers` (where span verification is one gate
among several); it does not depend on any of them.

## Provenance

Extracted 2026-09-29 from a requirements-traceability project that ran a
language-model scan across a corpus of agency governance documents asking for
verbatim, page-cited provisions, then verified every returned quote
character-by-character against the window it was drawn from. The measurement's figures are withheld until results are published. The failure shapes are not specific to that
corpus or that model.
