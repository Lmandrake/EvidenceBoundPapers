# Citable corpus

**Closed corpus.** A citation is legal only if its key appears below. No agent
may cite from memory, from the web, or from a paper it believes exists.

This converts hallucinated citations from a detection problem into an
impossibility. Additions go to `04-log/escalation-queue.md` as a request and are
added here by a human.

Full-text cache for E-02 span verification lives in `03-state/corpus-text/<key>.txt`,
extracted once from the source PDFs (`pdftotext -raw`); whitespace is normalized by
the enforcer before matching. A source with no cached full text is still citable but
`span-verifiable: no`, which **caps every claim citing it at `Suggestive`** — the
provenance cost is made explicit rather than hidden.

Watch for extraction artifacts when picking spans: ligatures (`ﬁ`, `ﬂ`),
hyphenated line-breaks, and mis-extractions such as `>5` becoming `N5`.

## Config

```
recency-window-years: 5          # E-12: a REMEDY's enabling-now must cite within this window.
advocacy-wordlist:               # E-11: institution/program proper nouns flagged in ASK.action and FRAMING.
                                 # List your own institutions, sponsors and programs here.
                                 # Do NOT list subject-matter proper nouns (instruments, datasets,
                                 # methods) — those are what the paper is about, not advocacy.
identifier-tokens:               # E-06: comma-separated instrument/mission names whose digits are
                                 # identifiers, not statistics ("Probe-2"). One line. Also barred
                                 # from FRAMING paragraphs as proper nouns.
```

## Keys

| key | authors | year | venue | local path (text cache) | span-verifiable |
|---|---|---|---|---|---|
| | | | | | |

*Empty. Populate before the first evidence-binding pass. `key` is what appears in
`cite:` fields and in `[key]` markers in the draft; keep it stable, because every
bound claim references it. The enforcer reads these six columns in this order;
`local path` is relative to `03-state/` (e.g. `corpus-text/smith2024.txt`, or `—`
when there is no cached text), and `span-verifiable` is `yes` or `no`.*
