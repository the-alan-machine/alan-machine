---
name: classify-claims
description: Find every claim in a page of The Alan Machine and classify it as established, reported, extrapolation, speculation or philosophy, flagging missing citations and unmarked claims. Use when drafting or reviewing text, when a scientific challenge questions a classification, or before marking a page ready for scientific review.
---

# Classify the claims on a page

The book's promise is that the reader always knows what kind of statement they are reading. This
skill checks that promise, sentence by sentence.

## Decision procedure

For each sentence that asserts something about the world, ask in order:

1. **Is it about meaning, value, mind or metaphysics, which no experiment could settle?**
   Philosophy. It belongs in a `{.callout-caution .philosophy title="Philosophy"}` with at least two
   positions.
2. **Is it accepted physics, with a peer-reviewed paper or standard textbook that states it?**
   Established. It stays in running text and needs a citation.
3. **Does it rest on a source that does not establish it yet** (a preprint, a figure from a company
   or the press, a talk)? Reported. It stays in running text that names the source ("a 2025
   preprint reports"), inside a `[...]{.reported}` span, with the citation.
4. **Does it follow from established physics, but only if some assumption holds** (a temperature,
   a scale, an idealization, a trend continuing)? Extrapolation. It belongs in a
   `{.callout-warning .extrapolation title="Extrapolation"}` that states the assumptions.
5. **Is it conceivable, with no evidence for it?** Speculation. It belongs in a
   `{.callout-important .speculation title="Speculation"}`.

Not claims, and not labeled: narrative, questions, definitions, and analogies that are presented
as analogies.

## Warning signs

- Hedges in running text ("might", "could", "perhaps", "in principle"): usually an unmarked
  extrapolation or speculation.
- "Scientists believe", "it is thought": find the source or reclassify.
- A preprint or a vendor's figure cited in plain running text: an unmarked reported claim.
- A number without a citation, or in a living review without a date.
- An analogy used as an argument.
- An extrapolation without its assumptions.
- Philosophy presented as physics ("time does not really flow"), or physics dismissed as philosophy.
- A citation that exists but does not say what the sentence says. Check with `verify-references`.

## Output

A table, in page order:

| Location | Claim (short quote) | Marked now as | Should be | Why | Missing |
|---|---|---|---|---|---|

Then the changes to make, as concrete edits. Do not reclassify a claim in someone else's merged page
silently; propose the change in a pull request or a scientific challenge issue.
