# Claim ledger (synthetic example)

**FICTIONAL.** This paper, its sources and every number in it are invented. It exists to show
the claim graph and to exercise every check in `template/tools/enforce.py`. A real paper has
40-80 nodes; this one has twelve so it can be read in five minutes.

| role | proposed | accepted | rejected | dnq |
|---|---|---|---|---|
| DEFINITION | 0 | 1 | 0 | 0 |
| GAP | 0 | 1 | 0 | 1 |
| REMEDY | 0 | 1 | 0 | 0 |
| ASK | 0 | 1 | 0 | 0 |
| TENSION | 0 | 1 | 0 | 0 |
| SUPPORT | 1 | 5 | 0 | 0 |

## Nodes

### DEF-01
- role: DEFINITION
- status: accepted
- strength: Asserted
- parent: -
- text: A deep heat-content estimate is traceable when every float profile in it carries its own calibration adjustment with a stated uncertainty, not only a fleet-average adjustment.
- claim-type: proposed-recommendation
- competing:
  - Fleet-average view: a record is adequate if the fleet-mean bias is removed | [cite: halvorsen2017] | ignores float-to-float spread.
  - Recovery view: a record is adequate if recovered floats validate it | [cite: ibarra2022] | too few floats are recovered to say.
- excludes: records whose only calibration is a fleet-average adjustment, and adjustments published without an uncertainty.
- why-decision-relevant: a climate-quality release is decided on the error of the series, and the per-float spread is part of that error.
- history: 2026-10-01 proposed by extractor; 2026-10-02 accepted at G3

### GAP-01
- role: GAP
- status: accepted
- strength: Suggestive
- parent: DEF-01
- text: Deep-float heat-content records below 2000 m are published without per-float calibration uncertainties.
- claim-type: supported-by-multiple-cases
- scope: the six-source fictional corpus in corpus.md, window 2017-2026, queries "deep float calibration uncertainty" and "abyssal heat content drift", searched 2026-10-01.
- magnitude: a residual warming trend error of 0.12 W m-2 in the 2000-4000 m layer when only the fleet-average adjustment is applied.
- incidence: Data Manager, Northreach Float Array Office | whether to release the deep heat-content series as a climate-quality record | residual trend error in W m-2 against the shipboard reference
- tractability: shared reference casts already exist and a 40-float pilot has used them.
- nearest-miss:
  - NM-01-1 | varga2024 | publishes per-float corrections | gives no uncertainty for them
  - NM-01-2 | lindqvist2023 | measures the error of shared-cast calibration | a pilot, not a published product
  - NM-01-3 | halvorsen2017 | defines the fleet-average adjustment | removes the mean bias only
- history: 2026-10-01 proposed by gap-scout; 2026-10-02 accepted at G3

### GAP-02
- role: GAP
- status: dnq
- strength: Asserted
- parent: DEF-01
- text: Nobody has ever studied deep float drift.
- notes: dnq. A universal negative the corpus contradicts (okafor2025). Kept so the loop stops re-proposing it.
- history: 2026-10-01 proposed by extractor; 2026-10-02 dnq at G3

### SUP-0001
- role: SUPPORT
- status: accepted
- strength: Strong
- tag: empirical
- parent: GAP-01/magnitude
- text: With only a fleet-average adjustment, the 2000-4000 m layer carries a residual warming trend error of 0.12 W m-2.
- cite: varga2024
- span: "Applying only a fleet-average bias adjustment leaves a residual warming trend error of 0.12 W m-2 in the 2000-4000 m layer"
- history: 2026-10-01 proposed by evidence-binder

### SUP-0002
- role: SUPPORT
- status: accepted
- strength: Strong
- tag: empirical
- parent: GAP-01/tractability
- text: Fewer than one in ten deep floats is ever recovered for recalibration.
- cite: ibarra2022
- span: "fewer than one in ten was ever recovered for post-deployment calibration"
- history: 2026-10-01 proposed by evidence-binder

### SUP-0003
- role: SUPPORT
- status: accepted
- strength: Strong
- tag: causal
- parent: GAP-01/magnitude
- text: Creep of the pressure housing causes the thermistor drift.
- mechanism: housing creep shifts the thermistor's reference resistance, so the reading drifts with time at depth (pressure-chamber tests).
- cite: okafor2025
- span: "slow creep of the pressure housing shifts the thermistor's reference resistance, producing a temperature drift that grows with time at depth"
- history: 2026-10-01 proposed by evidence-binder

### SUP-0004
- role: SUPPORT
- status: accepted
- strength: Strong
- tag: comparative
- parent: REM-01-1/precedent
- text: In a 40-float pilot, shared-cast calibration gave a heat-content RMSE of 0.4 W m-2 compared with 1.1 W m-2 for the fleet-average adjustment.
- cite: lindqvist2023
- span: "calibrating each profile against a shared reference cast reduced the heat-content RMSE to 0.4 W m-2 relative to the shipboard reference, compared with 1.1 W m-2 for profiles carrying only the fleet-average adjustment"
- history: 2026-10-01 proposed by evidence-binder

### SUP-0005
- role: SUPPORT
- status: accepted
- strength: Suggestive
- tag: empirical
- parent: TEN-01
- text: Reference casts are scheduled opportunistically.
- cite: quill2021
- span: "reference casts are scheduled opportunistically"
- notes: quill2021 has no cached full text, so this span cannot be verified and the claim is capped at Suggestive (E-02 reports it as a WARN).
- history: 2026-10-01 proposed by evidence-binder

### SUP-0006
- role: SUPPORT
- status: proposed
- strength: Strong
- tag: empirical
- parent: TEN-01
- text: The pilot used one housing design.
- cite: lindqvist2023
- span: "The pilot used Abyss-6K units only"
- history: 2026-10-03 proposed by evidence-binder; awaiting G3

### REM-01-1
- role: REMEDY
- status: accepted
- strength: Suggestive
- parent: GAP-01
- text: Calibrate every deep profile against a shared reference cast and publish the per-float adjustment with its uncertainty.
- claim-type: proposed-recommendation
- mechanism: each float's profiles are compared with the nearest shared shipboard reference cast; the fitted offset and its standard error ship with every profile.
- enabling-now: shared reference casts were piloted on 40 floats [cite: lindqvist2023]
- precedent: the pilot's RMSE result [cite: lindqvist2023]; the fleet-average method it extends [cite: halvorsen2017]
- yield: GAP-01/magnitude — removes most of the 0.12 W m-2 residual; GAP-01/incidence — gives the Data Manager a stated uncertainty to release against
- alternatives:
  - ALT-01-1-a | recover more floats for laboratory recalibration | too few are recoverable (ibarra2022)
  - ALT-01-1-b | model the drift from housing physics alone | the creep rate varies float to float
- cost-class: observation continuity
- history: 2026-10-01 proposed by gap-scout; 2026-10-02 accepted at G3

### ASK-01-1
- role: ASK
- status: accepted
- strength: Suggestive
- parent: REM-01-1
- claim-type: proposed-recommendation
- addressee: the deep-float data assembly centres
- action: publish a per-float calibration adjustment and its uncertainty with every deep profile, derived from shared reference casts.
- text: Publish a per-float calibration adjustment and its uncertainty with every deep profile.
- history: 2026-10-02 accepted at G3

### TEN-01
- role: TENSION
- status: accepted
- strength: Suggestive
- parent: -
- claim-type: inferred-from-shared-architecture
- generalization-boundary: holds for the DeepProfiler-2 and Abyss-6K floats, which share the tested housing; says nothing about other designs.
- text: Shared reference casts cost ship time, and the pilot tested one housing design.
- bears-on: REM-01-1
- disposition: scope limit. The ask covers floats with the tested housing; other designs need their own pilot.
- history: 2026-10-02 accepted at G3
