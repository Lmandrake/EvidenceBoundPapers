# Protected text

Text listed here survives verbatim in `draft.md`, or the loop halts (E-15).
Release requires an explicit human entry in `04-log/decisions.md`.

## Why this file exists

Your prose is the only text in this project that is definitely not
model-generated. It is also the text a fluent revision loop is most likely to
smooth away, one defensible edit at a time. Recursive refinement degrades a
human-written starting point while an automated judge reports improvement, so the
seed is frequently the highest-quality text anywhere in the trajectory.

Put anything here that you would be annoyed to lose: a formulation you worked
out, a sentence that lands, a distinction stated exactly right.

Two practical notes learned the hard way:

- E-15 compares against the **prior** draft version. A protected phrase that was
  present and is now missing is a silent drop and HALTs. A phrase whose section has
  not been written yet is a WARN, not a halt, and must be resolved before the final
  gate.
- Changing a protected line's punctuation is a protected-text change. If a later
  style pass needs to alter one (removing em-dashes, for instance), that is a human
  decision logged in `decisions.md`, and the entry here is **re-pinned** to the new
  wording so E-15 keeps guarding it. Do not blanket-release it.

## Entries

*Empty. Pin the seed's sharpest formulations here before the first render.*

| id | text (verbatim) |
|---|---|
| P-01 | |
