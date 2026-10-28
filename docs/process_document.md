# Authoring a Decadal Survey White Paper with a Claim-Grounded, Verifier-Gated LLM Loop

*A methodology note for anyone deciding whether to adopt this process for their own ESAS-class white paper.*

## Abstract

This document describes the method used to produce a submitted Decadal Survey white paper on
the uncertainty of satellite retrievals. The approach is a
**human-gated, verifier-constrained iterative-refinement loop**. Its distinguishing feature is that
the large language model (LLM) is never trusted to be its own judge: correctness is enforced by a
**deterministic, human-owned checker** and by **blind adversarial review**, while the argument itself
lives in a **claim graph** rather than in prose. The prose is a *rendering* of the claim graph, not the
source of truth. The design is a direct response to the well-documented failure modes of naive LLM
self-refinement — reward hacking, self-preference, and quality drift — and it trades speed for
auditability, citation integrity, and resistance to those failure modes.

---

## 1. Who this is for

Use this if you are writing a **high-stakes, evidence-bound, reviewer-scored document** (a Decadal
Survey white paper, a proposal, a position paper) where:

- every factual claim must be traceable to a real source;
- a fabricated citation or an over-generalized claim is a serious cost;
- a domain expert is available to make binding decisions at a few checkpoints; and
- you can afford deliberate iteration in exchange for a defensible result.

Do **not** use this for first drafts, brainstorming, or low-stakes writing. The overhead is only
justified when *being wrong is expensive* and *provenance matters*.

---

## 2. The problem this method solves

Iterative self-refinement with an LLM — generate, self-critique, revise, repeat — is attractive and
sometimes effective (Self-Refine, Madaan et al. 2023; Reflexion, Shinn et al. 2023). But when the same
model both writes and grades, the loop is vulnerable to a cluster of now-documented pathologies:

- **Reward hacking / specification gaming / Goodhart's law** — the generator optimizes the *measure*
  (the judge's score) rather than the *target* (a good paper). "When a measure becomes a target, it
  ceases to be a good measure." (Amodei et al. 2016; Skalse et al. 2022.)
- **Self-preference bias** — LLM judges systematically favor text produced by similar models, and can
  recognize their own outputs (Zheng et al. 2023; Panickssery et al. 2024).
- **Limited intrinsic self-correction** — without an *external* signal, models often cannot reliably
  correct their own reasoning, and may "improve" confidence without improving quality (Huang et al.
  2024).
- **Drift under recursion** — quality can degrade across iterations while an automated judge reports
  improvement; a human-written starting point is often the highest-quality text in the trajectory
  (related to recursive-degradation findings, e.g. Shumailov et al. 2024).

The core hazard: a fluent revision loop will smooth a sharp, correct sentence into fluent nothing, and
a complicit judge will call it progress. Every design choice below exists to make that impossible or
detectable.

---

## 3. Design principles and the concepts they instantiate

| Principle in this loop | Established concept it draws on |
|---|---|
| The **claim graph is the paper**; prose only renders it | Argumentation modeling (Toulmin 1958); argument mining — separate *what is asserted* from *how it reads* |
| A **frozen, human-owned reward function** (a deterministic checker the agent may not edit) | Generator–verifier separation (Cobbe et al. 2021); process supervision (Lightman et al. 2023); explicit governing principles as in Constitutional AI (Bai et al. 2022), but human-controlled |
| **Closed corpus + character-exact span verification** of every quote | Retrieval-augmented generation (Lewis et al. 2020); verifiable attribution (Rashkin et al. 2023); hallucination mitigation (Ji et al. 2023) |
| **Protected text**: pinned human formulations survive verbatim or the loop halts | Anti-drift anchoring against the self-refinement degradation mode |
| **Human decision gates** (thesis, rubric, claim admission, final) | Scalable oversight / human-in-the-loop checkpoints |
| **Blind adversarial review** + **cross-family audit** (a different model family) | LLM-as-judge (Zheng et al. 2023) with blinding and evaluator diversity to counter self-preference (Panickssery et al. 2024); multi-agent debate/critique (Irving et al. 2018; Du et al. 2023) |
| **No-regression rule + append-only log + versioned snapshots** | Reproducibility and auditability of the trajectory |

Three principles do the heaviest lifting:

**(a) The draft is not the paper.** The argument is a graph of typed claims — definitions, gaps,
supporting evidence, remedies, asks, tensions, nearest-misses — each with a strength grade and, for
evidence, a citation and a verbatim source span. `draft.md` is a *rendering* bound to the graph
paragraph-by-paragraph. A drafter may improve clarity and voice; it may not introduce a fact, number,
or citation that is not already an admitted claim. This severs fluency from assertion.

**(b) The agent cannot touch its own grader.** The specification and the checker (`tools/enforce.py`)
are frozen. The checker is *deterministic and contains no LLM* — it verifies structural and provenance
properties (spans match sources character-for-character; every citation and numeral traces to a bound
claim; protected text is intact; the word/length proxy holds; no previously-passing check now fails).
The agent may only *propose* amendments; a human applies them. This is the anti-Goodhart core: you
cannot game a grader you cannot edit.

**(c) Citation hallucination is made impossible, not merely detected.** A citation is legal only if
its key exists in a closed corpus, and any quoted span is checked byte-for-byte against a cached copy
of the actual source. Unverifiable sources are allowed but *cap the claim's strength*, making the
provenance cost explicit rather than hidden.

---

## 4. The artifacts (repository layout)

```
00-seed/     immutable, hash-locked human seed essay (read-only input)
01-spec/     the frozen reward function: rubric, enforcer spec, claim schema,
             style anchor, stopping rules
02-agents/   role prompts: extractor, gap-scout, evidence-binder, drafter,
             blind reviewers (program / skeptic / conformance), adjudicator,
             cross-family auditor
03-state/    claims.md (the paper), draft.md (a rendering), corpus.md +
             corpus-text/ (cached full text for span checks), protected.md,
             versions/ (every snapshot)
04-log/      decisions.md (human gate rulings), iterations.md, issues.md,
             escalation-queue.md, rubric-amendments.md, enforcer-report.md
tools/       enforce.py (deterministic checker), export_packet.py (blinded
             review packets)
```

The separation is deliberate: **inputs** (seed, corpus) are immutable; the **reward function** (spec,
checker) is human-owned; the **work product** (claims, draft) is what the agent may change; and the
**ledger** (logs) records every decision before it is executed.

---

## 5. The loop

**Figure 1.** The authoring loop. Diamond nodes `< G >` are human decision gates; the reward function
is frozen and human-owned; the draft is only a rendering of the admitted claim graph.

```
        +-------------------------------------------------+
        |  FROZEN REWARD FUNCTION  (human-owned)          |
        |  rubric . enforcer spec . claim schema          |
        |  deterministic checker (contains no LLM)        |
        +------------------------^------------------------+
             agent may PROPOSE amendments (AMD-nnn);
                  only a human ever applies them
                                 |
  +------------+         +--------+--------+
  |   SEED     |         |    EXTRACT      |
  | immutable, | ------> |   claim graph   |
  | hash-locked|         | (read the holes)|
  +------------+         +--------+--------+
                                  |
                         < G1 >  thesis & structure     (human gate)
                                  |
                         < G2 >  rubric lock            (human gate)
                                  |
  +------------+         +-----------------+
  |  CLOSED    |  span-  | GAP-SCOUT +     | <----------------+
  |  CORPUS    | verified| EVIDENCE-BINDER |                  |
  | + cached   | ------> |                 |                  |
  | full text  |         +--------+--------+                  |
  +------------+                  |                           |
                         < G3 >  claim admission (human)      |
                                  |                           |
                          +-------+-------+                   |
                          |    RENDER     |  draft is only    | iterate
                          |    draft      |  a rendering      | (steps
                          +-------+-------+                   |  5-10)
                                  |                           |
                          +-------+-------+  HALT --> escalate |
                          |   ENFORCE     |  (deterministic)  |
                          +-------+-------+                   |
                                  | CLEAN                     |
                    +-------------+--------------+            |
                    |  BLIND REVIEW              |            |
                    |  advocate . skeptic .      | -----------+
                    |  conformance               |
                    |  + CROSS-FAMILY AUDIT      |
                    |  (different model family)  |
                    +-------------+--------------+
                                  |
                         < G4 >  final                 (human gate)
                                  |
                                  v
                             SUBMISSION
```

1. **Seed** — a human writes the initial essay. It is hash-locked and never edited.
2. **Extract** — an agent proposes a claim graph from the seed. *Read the holes, not the claims.*
3. **Gate G1 (thesis & structure)** — a human fixes the single proposition and the section skeleton.
4. **Gate G2 (rubric lock)** — the human affirms the scoring rubric, length/format rules, and style
   anchors *before* drafting, so the target cannot move to fit the output.
5. **Gap-scout + evidence-binder** — agents find missing evidence and bind real, span-verified sources
   from the closed corpus (adding new sources is a human-gated corpus request).
6. **Gate G3 (claim admission)** — only a human sets a claim's status to *accepted*; only accepted
   claims may be rendered.
7. **Render** — the drafter turns accepted claims into prose, keeping the binding comments intact.
8. **Enforce** — the deterministic checker runs. Any HALT-class failure stops the loop and is
   escalated; nothing is auto-fixed by editing the checker.
9. **Blind review** — isolated reviewer agents (an advocate, a skeptic, a conformance checker) see the
   draft and rubric *only* — no history, no scores, no claim table. A separate **cross-family audit**
   uses a different model family under the same blind conditions to dilute self-preference.
10. **Adjudicate** — a mediator turns findings into claim-graph changes; the reviewer and the reviser
    never share a context.
11. **Gate G4 (final)** — the human accepts the result.

Iterate steps 5–10 behind the gates. Everything is logged before it is done.

---

## 6. Tradeoffs and honest limitations

- **It is slow.** The discipline (closed corpus, span checks, gates, blind panels) costs real time and
  human attention. This is the price of provenance and drift-resistance.
- **The human is the bottleneck — by design.** Gates require a domain expert who can rule on thesis,
  evidence admission, and protected-text releases. Without that expert, the method degrades to
  ordinary LLM writing.
- **The deterministic checker cannot judge quality.** It verifies structure and provenance, not
  whether the argument is *good*. Semantic quality is delegated to blind review and to the human — a
  deliberate division of labor, not an oversight.
- **Closed-corpus friction is real.** You cannot cite what you have not ingested. This prevents
  hallucinated references but means evidence gaps surface as explicit work items, not silent
  paraphrases.
- **Claim-first authoring can feel rigid.** Rewriting a paragraph may require editing the graph first.
  The payoff is that every sentence remains traceable; the cost is lost spontaneity.
- **It does not remove bias or error — it makes them auditable.** The method surfaces disagreements
  (skeptic dissents, tensions, nearest-misses) rather than hiding them. A determined human can still
  admit a weak claim; the log will show that they did.

---

## 7. Should you use it?

**Prerequisites:** a committed domain expert for the gates; a set of real source documents you can
ingest; a machine-checkable specification of your call's rules (length, required sections, response
type); and tolerance for iteration.

**Use it when** provenance, reviewer scrutiny, and resistance to over-claiming dominate — exactly the
Decadal Survey setting. In this instance the loop carried a paper through ~30 logged iterations and
several independent expert reviews (aggregate scores rising into the mid-80s/100), with every quoted
citation span-verified against its source and every accepted claim tied to a human ruling.

**Skip it when** you need speed, are exploring ideas, or the cost of being wrong is low. The machinery
is overhead that only pays off under scrutiny.

---

## References

- Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., Mané, D. (2016). *Concrete
  Problems in AI Safety.* arXiv:1606.06565.
- Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.* arXiv:2212.08073.
- Cobbe, K., et al. (2021). *Training Verifiers to Solve Math Word Problems.* arXiv:2110.14168.
- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., Mordatch, I. (2023). *Improving Factuality and
  Reasoning in Language Models through Multiagent Debate.* arXiv:2305.14325.
- Huang, J., et al. (2024). *Large Language Models Cannot Self-Correct Reasoning Yet.* ICLR 2024.
- Irving, G., Christiano, P., Amodei, D. (2018). *AI Safety via Debate.* arXiv:1805.00899.
- Ji, Z., et al. (2023). *Survey of Hallucination in Natural Language Generation.* ACM Computing
  Surveys 55(12).
- Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.*
  NeurIPS 2020.
- Lightman, H., et al. (2023). *Let's Verify Step by Step.* arXiv:2305.20050.
- Madaan, A., et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback.* NeurIPS 2023.
- Panickssery, A., Bowman, S. R., Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own
  Generations.* arXiv:2404.13076.
- Rashkin, H., et al. (2023). *Measuring Attribution in Natural Language Generation Models.*
  Computational Linguistics 49(4).
- Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S. (2023). *Reflexion: Language Agents
  with Verbal Reinforcement Learning.* NeurIPS 2023.
- Shumailov, I., et al. (2024). *AI Models Collapse When Trained on Recursively Generated Data.*
  Nature 631.
- Skalse, J., Howe, N. H. R., Krasheninnikov, D., Krueger, D. (2022). *Defining and Characterizing
  Reward Hacking.* NeurIPS 2022.
- Toulmin, S. (1958). *The Uses of Argument.* Cambridge University Press.
- Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023.
