---
name: verify-model-quotes
description: Check that a model's quotation and its cited page/section/line are both real before anyone reads them as the source's words. Use for extraction pipelines, RAG citations, evidence tables, "quote the passage that says X", when building such a verifier, or when a verifier just called a quote fabricated. Not source trust or claim support.
---

# Verify model quotes

A model asked for the passage that says X will sometimes return one that is not
in the document. It is fluent, formatted like a quotation, carries a page
number, and **looks no different from a real one.** Inspection is reading, and
fabrications read fine.

**Model confidence is not evidence and must never gate or rank a quote.** It can
be higher on fabricated quotes than on real ones; do not filter or sort on it.

## Verify a (text, location) pair, not existence

`if quote in document` is not the check. Boilerplate and appendix restatements
recur (the same clause on pages 27 and 65; one sentence on pages 4, 30, 87), so
a quote can exist in the document while the cited location is wrong. A
document-wide test reports verified and the reader follows the citation to
unrelated material. The haystack is the **claimed span only**.

## The haystack is the source document and nothing else

The most common fabrication is the model quoting the **question** back with a
page number. A verifier whose haystack is the prompt, a conversation log, or any
concatenated context blob will verify it. Question, instructions, schema,
few-shot examples, prior turns and sibling documents are all outside the
haystack. Write a test that feeds in a quote copied from the question and
asserts rejection; if it does not exist, assume the pipeline accepts echo.

## Prefer span selection over generated quotation

```
PREFER:  source -> assign span IDs -> model selects a span ID
                -> your code reconstructs the quotation from the source
OVER:    source -> model rewrites the quotation -> a fuzzy verifier recovers it
```

The model can then express only an identifier that resolves or does not, plus a
rationale labelled as its own words. Quote text comes out of the source by
construction and prompt-echo is unrepresentable. This removes the model-written
quote channel; it does not remove provenance errors (wrong source version, wrong
mapping), which the next section covers.

Give the model a locator it can **read off** the material rather than compute:
1-indexed line numbers as a left-margin ruler with `start_line`/`end_line`.
Character offsets are counted badly by models.

**Residual risk moved, it did not vanish: silent wrong-content extraction.** A
valid locator can point at the wrong or irrelevant text, and no verifier can see
it, because the text genuinely came from the source. Measure that separately by
review; "fabrication is impossible" must not be heard as "extraction is correct."

### Locators are bound to a source version

Line numbers and block indices are positions, not identities: inserting one
block before the cited one (a parser improvement, a changed header strip)
shifts every later locator onto a different passage, silently. A bare content
hash is ambiguous for repeated identical passages (boilerplate, restated
clauses) and resolves to whichever copy is found first.

- Store every locator with a **source version**: a hash of the exact extracted
  text the locator was assigned against (`{"v": <sha256 of extracted text>, ...}`).
- Resolve a locator only against text whose version matches. On version
  mismatch, **refuse** (re-extract and re-select; do not remap or guess).
- A content-hash locator that matches more than one passage in the span is
  **ambiguous: refuse**, or add disambiguating context (document id, page,
  block index) so it matches exactly one. Never take the first match.
- Document id + page + block index is a position within one version, not a
  stable identity across versions.

Executable fixtures: `tests/test_review_2026_10_15.py`.

Free-text quotation is sometimes unavoidable (the model must point inside a
span, or the interface returns text). Then use the checklist and accept the
weaker architecture.

## Checklist when generated quotes are unavoidable

1. **Verify against the claimed source, not the prompt.** Haystack = the
   document or window the model said it quoted.
2. **Verify the claimed location.** A hit outside the cited span is a failure,
   not a pass with a note.
3. **Three outcomes, never two:** `EXACT`, `MATCHED_UNDER_NORMALIZATION` (name
   the normalizations applied), `FAILED`. Whitespace/ligature matches can be
   published; an alphanumeric-only match is a lead for hand review.
4. **Keep offsets from normalized text back to the original**, so the locator
   can be corrected and a human can audit the hit.
5. **Forbid matching across scaffolding you inserted:** page markers,
   header/footer strips, window separators, chunk boundaries. A match spanning
   one is a plumbing artifact. Distinguish synthetic adjacency (unrelated
   chunks you concatenated: reject) from real document continuation (one
   passage legitimately spanning a page break: accept, matching on the source
   text with the markers removed).
6. **Test the prompt-echo case:** question text in, rejection out.
7. **Prove the verifier bites both ways:** corrupt a real quote and watch it
   fail; corrupt a valid quote's locator and watch it fail; restore both and
   watch them pass. A verifier never seen rejecting anything is untested.
8. **Use an independent implementation for any appeal path.** Re-checking a
   verdict with the code that produced it only confirms itself.

## The verifier lies too

- **The haystack is the source as the model saw it, with injected scaffolding
  removed.** Not the raw file (the model never saw that), not the marked-up
  window. If the marked-up text is searched, a genuine sentence spanning a page
  break is not contiguous and a byte-perfect quote is recorded as invented.
  Always write the page-spanning quote as a test; small fixtures omit it.
- Removing markers from the haystack without refusing matches that would have
  crossed them lets two unrelated pages weld into one false match (item 5).
- **Aggressive normalization manufactures false positives**: folding to
  alphanumerics only can bridge two unrelated entries into one phrase and
  declare a fabricated quote real.
- Fixing a verifier bug rarely explains away the fabrication problem; report the
  rate before and after the fix rather than letting "the verifier had a bug"
  stand in for it.

| what it looks like | what is true |
|---|---|
| A verbatim-looking quote with a page number | may not be in the source at all |
| `quote in document` is True | the cited page may still be wrong |
| Verifier reports 0 fabrications | confirm it has ever rejected anything |
| Verifier says FABRICATED | may be your scaffolding; check page-spanning quotes first |
| Looser matching recovered more quotes | it also recovers quotes that do not exist |
| A second pass confirmed the verdict | same implementation, so only itself |

## Scope

Only whether the quoted text and its cited location are real. Not: whether the
source is trustworthy (draft, superseded, third-party extraction), whether the
claim is supported by the passage, whether it is the best quote or something was
missed (recall), or whether the model's surrounding reasoning is sound. EXACT at
the cited span can still be worthless evidence; that is a later human question.

## Neighbours

- `confident-wrong-numbers` - wrong answer is a count/zero/empty list from a mis-shaped query.
- `grader-validation` - general case of a scorer or witness you built to grade your own work.
- `incomplete-ground-truth` - recall against positive-only reference data.
- `claim-provenance` - whether a source exists, was read, and says what you think.
- `evidence-bound-papers` - full apparatus where every claim traces to a real source; span verification is one gate.
