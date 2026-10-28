# Agent roster

Nine roles. Resist adding more — role proliferation buys the appearance of rigor
and costs context.

| Agent | Owns | Never does |
|---|---|---|
| `architect` | thesis, structure, section briefs, whole-document view | write prose, admit claims |
| `extractor` | one-shot: seed → proposed claims | invent claims not in the seed |
| `gap-scout` | proposes DEF / GAP / REMEDY / ASK nodes | cite outside corpus, admit claims |
| `evidence-binder` | proposes SUPPORT, owns all citations and spans | write prose, touch structure |
| `drafter` | renders accepted claims into prose, section-scoped | assert anything not in a claim |
| `reviewer-program` | blind review, program/decadal-fitness lens | see history, suggest fixes |
| `reviewer-skeptic` | blind review, methodological lens | see history, suggest fixes |
| `reviewer-conformance` | blind review, voice/structure/call lens | see history, suggest fixes |
| `adjudicator` | synthesizes reviews → issues, assigns won't-fix, escalates | write prose, score |
| `enforcer` | deterministic checks (a script, not an agent) | reason, contextualize, be overruled |

## Context topology

- **Section-scoped agents run with clean contexts and write to files.** Do not pass
  large outputs back through a coordinator; that is a game of telephone and it
  costs fidelity at every hop.
- **Only the architect sees the whole draft at once.** Argument arc,
  non-redundancy, and voice are whole-document properties that no section agent
  can perceive. The architect files issues; it does not edit prose.
- **Reviewers are isolated from everything.** See `CLAUDE.md` rule 6.

## Delegation brief rule

Every subagent brief includes the *rationale*, not just the task: why this
subtask matters and how it fits the whole. A subagent that knows why it is
writing section 3 writes a better section 3 and wastes less effort rediscovering
context. Every section brief carries the thesis and the named decision-makers,
not just the heading.

## Hard separations

- reviewer ≠ reviser (never the same context)
- proposer ≠ admitter (only a human admits)
- checker ≠ interpreter (the enforcer's verdict is not negotiable)

## Not an agent: the cross-family audit

`cross-family-audit.md` documents a **tool the adjudicator invokes**
(`tools/export_packet.py`), not a tenth agent. It runs a non-Claude model over a
blinded packet as a rare, on-demand calibration of the panel — see
`01-spec/stopping-rules.md`. It proposes nothing and admits nothing; its output
feeds `04-log/rubric-amendments.md`. Resist the urge to make it a routine
reviewer: that would turn a scarce calibration instrument into just another
same-configuration vote.
