# The verification suite

Five skills, one question: **is the thing you are about to report actually true?** The paper
harness in this repo checks that a claim traces to a source. These skills cover the other
places a confident falsehood gets in: the number you counted, the quotation a model produced,
the source you cited from memory, and the checker that told you everything passed.

| Skill | The failure it catches |
|---|---|
| `confident-wrong-numbers` | A query whose shape returns a plausible wrong number: a count, a zero, an empty list, an all-None field |
| `measuring-large-artifacts` | A number taken from a file too large to read whole (dumps, logs, exports), where grep and wc mislead |
| `verify-model-quotes` | A model quotation, or the page, section or line it cites, that does not exist in the source |
| `claim-provenance` | A claim encoded as knowledge before anyone confirmed the source is real, was read, and says what you think |
| `grader-validation` | A scorer, oracle or guard that reports a clean verdict because it cannot see the fault |

They are ordered from the cheapest check to the deepest. The first three check a value
against its source. `claim-provenance` checks the source itself. `grader-validation` checks the
instrument doing the checking, and it is the one to reach for whenever a tool you built reports
"0 lost", "0 spurious" or "all tests pass".

Each `<name>/SKILL.md` is the entry point. To install one for Claude Code, symlink its
directory into `~/.claude/skills/` (for example
`ln -s "$PWD/skills/verify-model-quotes" ~/.claude/skills/`). `confident-wrong-numbers`,
`verify-model-quotes` and `measuring-large-artifacts` carry their own tests and scripts; run
them from their own directory.

## Where they came from

`claim-provenance` and `grader-validation` were written in MandrakeVisualize, where their worked
examples live. The other three came from MandrakeWorkflows, and before that from their own
repos, now archived. They were gathered here on 2026-10-26 so the suite ships as one family
beside the paper harness that depends on the same discipline.
