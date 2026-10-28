# Writing Guide: Matching This Voice

Calibrated against the OWLS/OSIA paper (Wronkiewicz et al. 2024, *PSJ*). The through-line: **specificity does the persuading.** Concrete numbers, named things, and explicit reasoning carry the weight, not adjectives or emphasis.

## Do

- **Cite the actual number, not its shadow.** The paper says "34 kbit s⁻¹," "τ = 0.529 (p = 1.09×10⁻⁶)," "data reduction of 1887.8×." Reach for the figure before "significant," "substantial," or "orders of magnitude." When you must round, round to a real quantity (~10,000×), not to a vibe.
- **Ground the abstract in something familiar.** Bandwidth is made real by comparing it to dial-up (56 kbit/s) and "roughly an hour to transmit a single 12-megapixel photo"; coordinated motion is explained as "a school of fish." One grounded referent beats three abstract descriptors.
- **Show the load path with *because / therefore / thus*.** The paper doesn't assert conclusions, it walks them: inverse-square law, then limited downlink, then "therefore, novel mission strategies are required." Make the causal chain visible rather than stating the endpoint.
- **Commit, then bound.** State the claim plainly ("In practice, this has little direct negative impact on overall sensitivity"), then give the honest caveat. Report failures the same way you report wins, e.g. "HELM's tracking performance suffered due to frequent particle crossings."
- **Own decisions in first person.** "We defined," "we chose not to rely on deep learning," "we selected the RF model for further analysis." Agency, not passive drift.

## Don't

- **Don't use em-dashes.** They are one of the strongest current model tells. Recast with a comma, a colon, parentheses, or a full stop. If a phrase reads as a dramatic aside, make it its own sentence.
- **Don't default to the rule of three.** "Clear, concise, and compelling" is a model tic. The paper lists three things only when the count is real (three microscopes, six instruments). Otherwise it uses one precise word.
- **Don't throat-clear.** Cut "It's worth noting that," "It's important to," "At its core," "Ultimately." (A bare "Note that…" pointing at a specific caveat is fine; that's the paper's move, and it earns its place.)
- **Don't decorate with atmosphere-words:** *leverage, robust, nuanced, seamless, multifaceted, landscape, realm, navigate, foster, underscore.* Keep the word only if it names something exact. The paper writes "robust to short particle occlusions" (precise) but never "a robust solution" (filler). Precise vs. decorative is the dividing line, not the word itself.
- **Don't close with a recap.** Avoid "In conclusion, we have shown…" The paper's ending generalizes outward ("whether at home or at interplanetary distances…") instead of restating. End by pointing somewhere new, or just stop.
- **Don't flatten the rhythm.** Set a short declarative ("On Earth, all life requires access to water.") against the longer technical builds. Uniform sentence length is the loudest machine tell.

## Ready-to-paste prompt preamble

> Write in this voice: lead with specific numbers and named entities; ground each abstract point in one familiar comparison; make reasoning explicit with because/therefore; commit to claims, then state the honest caveat; use first-person "we" with clear agency. Avoid: em-dashes (recast with commas, colons, or full stops), the rule of three, hedge preambles ("it's worth noting," "importantly"), decorative filler (leverage, robust, nuanced, seamless, landscape, realm), participial pile-ups, and recap conclusions. Vary sentence length deliberately.
>
> [Attach 1–2 paragraphs of the OWLS paper as a style sample. Few-shot with real prose matters more than any description of the voice.]

---
*Calibrated to formal technical writing. For shorter deliverables (memos, review slides), the same rules hold but dial the sentence-length variation up and drop citation formality.*
