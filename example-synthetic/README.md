# Synthetic example: a deep-ocean heat-content claim graph

**Everything here is invented**: the paper, its six sources, their authors and journals, the
office named as the decision-maker, and every number. It was written to be small enough to
read in five minutes and to exercise every check in `template/tools/enforce.py`.

```
python3 ../template/tools/enforce.py --root .     # verdict=CLEAN  passed=21/21
```

What to look at:

- `03-state/claims.md` is the paper. Twelve nodes: one DEFINITION with two rival views, one
  GAP with a reproducible scope and three nearest misses, a REMEDY with two rejected
  alternatives, the ASK it supports, a TENSION the paper concedes, and SUPPORT nodes tagged
  empirical, causal and comparative. A rejected (`dnq`) GAP and a still-`proposed` SUPPORT
  show that only accepted nodes are held to the admission checks.
- `03-state/draft.md` is a rendering of it. Every paragraph ends in a `<!-- claims: ... -->`
  binding, and every numeral and citation in a paragraph must come from a bound claim.
- `03-state/corpus.md` is the closed corpus. Four sources have cached full text, so their
  quoted spans are checked character for character against `corpus-text/`. Two have none, so
  claims citing them are capped at `Suggestive` and E-02 reports a WARN.
- `04-log/decisions.md` is the human's record: E-18 refuses any accepted claim without one.

Each check's failing case is in `../tests/test_enforce.py`: the same instance with one defect,
a fabricated quote, a citation to a key outside the corpus, a gap with two nearest misses
instead of three, and so on.

Running the checker writes `04-log/enforcer-report.md` and `04-log/.enforcer-state.json`
and appends a line to `04-log/iterations.md`, as it does in a real instance.
