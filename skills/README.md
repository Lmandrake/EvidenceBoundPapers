# The verification suite

Three skills, one question: **is the thing you are about to report actually true?** The paper
harness in this repo checks that a claim traces to a source. These skills cover the other
places a confident falsehood gets in: the quotation a model produced, the source you cited from
memory, and the checker that told you everything passed.

| Skill | The failure it catches |
|---|---|
| `verify-model-quotes` | A model quotation, or the page, section or line it cites, that does not exist in the source |
| `claim-provenance` | A claim encoded as knowledge before anyone confirmed the source is real, was read, and says what you think |
| `grader-validation` | A scorer, oracle or guard that reports a clean verdict because it cannot see the fault |

They are ordered from the cheapest check to the deepest. `verify-model-quotes` checks a value
against its source. `claim-provenance` checks the source itself. `grader-validation` checks the
instrument doing the checking, and it is the one to reach for whenever a tool you built reports
"0 lost", "0 spurious" or "all tests pass".

Each `<name>/SKILL.md` is the entry point. To install one for Claude Code, symlink its
directory into `~/.claude/skills/` (for example
`ln -s "$PWD/skills/verify-model-quotes" ~/.claude/skills/`). `verify-model-quotes` carries its
own tests; run them from its directory.

## Where they came from

`claim-provenance` and `grader-validation` were written in MandrakeVisualize, where their worked
examples live. `verify-model-quotes` came from MandrakeWorkflows, and before that from its own
repo, now archived. They were gathered here on 2026-10-26 so the suite ships as one family
beside the paper harness that depends on the same discipline.

Two companions gathered here at the same time, `confident-wrong-numbers` (a query whose shape
returns a plausible wrong number) and `measuring-large-artifacts` (a number taken from a file too
large to read whole), moved back to [MandrakeWorkflows](https://github.com/Lmandrake/MandrakeWorkflows) on 2026-11-04, where they sit with the other
evaluation-and-judgment skills. They pair with this suite but do not depend on it.
