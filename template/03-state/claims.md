# Claim ledger

**This file is the paper.** `draft.md` is a rendering of it and has no
independent authority. If the two disagree, the prose is wrong.

Format is defined in `01-spec/claim-schema.md` and parsed strictly by the
enforcer. Do not improvise keys, reorder them, or reflow the blocks.

Only a human writes `status: accepted`, and every admission has a matching entry
in `04-log/decisions.md` (E-18).

Target 40–80 nodes for a seven-page paper. At 150 you are transcribing, not
claiming. At 15 the paragraph-binding check is vacuous.

---

## Counts

Update at each admission. The enforcer does not read this table; it is for you.

| role | proposed | accepted | rejected | dnq |
|---|---|---|---|---|
| DEFINITION | 0 | 0 | 0 | 0 |
| GAP | 0 | 0 | 0 | 0 |
| REMEDY | 0 | 0 | 0 | 0 |
| ASK | 0 | 0 | 0 | 0 |
| TENSION | 0 | 0 | 0 | 0 |
| SUPPORT | 0 | 0 | 0 | 0 |

---

## Nodes

*Empty. The extractor writes the first pass here from `00-seed/seed-paper.md`,
all with `status: proposed`. Read the holes, not the claims.*

*Block formats — copy exactly from `01-spec/claim-schema.md`; the four shapes are
DEFINITION, GAP, REMEDY / ASK, TENSION, and SUPPORT.*
