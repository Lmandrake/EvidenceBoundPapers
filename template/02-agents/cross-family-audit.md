# Cross-family audit (external-model check)

## What this is

A **rare, on-demand** check that runs a non-Claude model (e.g. ChatGPT) over a
blinded packet. It is the main compensation for running a same-family reviewer
panel day to day: an external pass scored against the *same frozen rubric* is a
calibration audit of the internal panel, and a patterned divergence on a rubric
item is a defect in the *item*, not a fact about the draft.

It is **scarce by design.** Do not spend it on "read my paper and tell me what you
think." The tool is `tools/export_packet.py`; it assembles the packet and prints
an ESC stub.

## When the loop may request it

The adjudicator (never a reviewer, never the drafter) requests a cross-family
audit, and only for one of these triggers — each already named in
`01-spec/stopping-rules.md`:

| Trigger | Mode to use |
|---|---|
| Reviewers converge high with low variance (F7.3) — suspected shared blind spot | `--mode draft` |
| Rubric scores rise while enforcer findings are flat (F7.1) — suspected reward hacking | `--mode draft` |
| A reviewer's `meta` block repeatedly reports the same inapplicable item | `--mode draft` (to test if an external model also cannot apply it) |
| A load-bearing claim rests on a span whose support is contested internally | `--mode source KEY` |
| Before a major human gate, as a periodic calibration pass | `--mode draft` |
| The human, or the loop, wants the *machinery itself* stress-tested | `--mode process` |

Any other use is out of budget. If you are tempted to run it and none of the
above fired, that itself is a signal — write the temptation to
`04-log/rubric-amendments.md` instead; it may be a missing trigger.

## The blinding contract (load-bearing)

For `--mode draft`, the external model must run in the **same blind, offline
configuration** as the internal panel, or the comparison measures the
configuration, not the model. The exporter enforces this mechanically:

- ships **only** draft prose + frozen rubric + style anchor
- strips **all** HTML comments, including `<!-- claims: ... -->` binding comments,
  so the claim graph is invisible
- omits revision history, prior scores, other reviewers' output, the issue log,
  and adjudicator notes

`--mode source` and `--mode process` are not blind reviews and do not carry this
contract — they are targeted assessments, not panel members.

## How to run

```
python3 tools/export_packet.py --mode draft
python3 tools/export_packet.py --mode source --source <corpus-key>
python3 tools/export_packet.py --mode process
```

Each writes a single self-contained Markdown file to `04-log/exports/` (paste the
whole file into the external model) and prints an ESC stub for
`04-log/escalation-queue.md`.

## Reading the result

Paste the external model's output to `04-log/reviews/rNNN-external.md`. Then, per
`01-spec/stopping-rules.md`, compare **item by item** against the internal panel
and record in `04-log/rubric-amendments.md`:

- **agreement** → the item is doing its job
- **one-off divergence** → note it, do nothing
- **patterned divergence across runs** → the rubric item is defective; draft an
  amendment. A human applies it.

**Do not "fix the draft" to close a divergence.** The divergence is information
about the measuring instrument, not about the paper. This is the single easiest
mistake to make with this check and it quietly destroys its value.

## Example packets on disk

Packets are written to `04-log/exports/`. None ship with the template; generate one
against `example-synthetic/` to see the shape (see below).
