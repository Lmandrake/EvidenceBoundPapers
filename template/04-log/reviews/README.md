# Reviews

One file per reviewer per round: `rNNN-program.md`, `rNNN-skeptic.md`,
`rNNN-conformance.md`.

**Reviewers never read this directory.** It exists for you and the adjudicator.
A reviewer that can see prior rounds is an online judge, and online judges drift
from ground truth under optimization pressure much faster than blind ones.

If a reviewer's report opens with a contamination error, something in the harness
is leaking history into its context. Fix the harness; do not rerun and hope.
