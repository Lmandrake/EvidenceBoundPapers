# Evidence audit (synthetic example)

*FICTIONAL claims and sources. This file shows the format of the audit the checker cannot do.*

The checker proves a quoted span exists in the cited source. It cannot prove the source
supports the claim's **scope**. This audit is done by a person (or a reviewer under the same
blind rules) before prose is regenerated, one row per load-bearing claim. A claim may not enter
the paper unless its source directly supports its scope; a rescoped claim is re-admitted by a
human at a G3-revision gate.

Fields: exact claim · type · scope · source and exact passage · support level
(`direct` / `partial` / `adjacent`) · counter-evidence · revised language · confidence.

## SUP-0004: the pilot result

- exact claim (first draft): "Shared-cast calibration cuts deep heat-content error by nearly
  two thirds for deep floats."
- type: comparative, used as REM-01-1 precedent
- scope as written: all deep floats
- source and exact passage (lindqvist2023): "calibrating each profile against a shared
  reference cast reduced the heat-content RMSE to 0.4 W m-2 relative to the shipboard
  reference, compared with 1.1 W m-2". The Discussion adds: "The pilot used Abyss-6K units
  only; whether other housings drift the same way was not tested."
- support level: **partial.** The numbers are direct; "for deep floats" outruns a one-design
  pilot of 40 units. The span check passed on the first draft, because every quoted word is
  in the source.
- counter-evidence: the source's own Discussion limits it to one housing.
- revised language: "In a 40-float pilot, shared-cast calibration gave a heat-content RMSE of
  0.4 W m-2 compared with 1.1 W m-2 for the fleet-average adjustment." The scope limit became
  TEN-01, with a `generalization-boundary` that E-21 now requires.
- confidence: high that the first wording overreached.

## SUP-0003: the drift mechanism

- exact claim: "Creep of the pressure housing causes the thermistor drift."
- type: causal
- source and exact passage (okafor2025): "slow creep of the pressure housing shifts the
  thermistor's reference resistance, producing a temperature drift that grows with time at
  depth", from pressure-chamber tests.
- support level: **direct** for the tested housing.
- counter-evidence: none in the corpus.
- revised language: unchanged.
- confidence: medium. A laboratory mechanism, not a measurement on deployed floats.
