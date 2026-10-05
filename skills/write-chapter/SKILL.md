---
name: write-chapter
description: Draft or revise a chapter, interlude or Building Alan living review of The Alan Machine. Use when asked to write, expand, rewrite or update a page under chapters/, interludes/ or building-alan/, or to turn an accepted content proposal into text.
---

# Write a chapter, interlude or living review

## 1. Read before writing

- The page itself: its front matter and the `<!-- Scope: ... -->` comment, which is the agreed scope.
- The content proposal issue, if there is one (`gh issue list --label proposal`).
- The previous and next pages in `_quarto.yml`, so the text connects without repeating them.
- [STYLE.md](../../STYLE.md): the register that applies (popular, philosophy or living), classifying
  claims, self-contained sections.
- The template for the kind of page, in `templates/`.

## 2. Gather sources first

List the claims the page needs and find a source for each one before writing prose around it.
Follow the `verify-references` skill: BibTeX only from the DOI, never from memory. A claim with no
source you can check is not written as established; it becomes an extrapolation or speculation, or
it is left out. A claim whose only source is a preprint or a vendor's figure is reported.

## 3. Write

- **Chapter**: conversational English for a reader with no physics background. Equations go in a
  collapsed "Going deeper" callout; any equation left in the text gets a sentence that says the same
  thing in words. End with "What the machine would need" (an order-of-magnitude budget), "Open
  questions" and "Further reading".
- **Interlude**: 1,500 to 3,000 words, at least two positions with their best arguments and their
  philosophers cited. No new physics that later chapters depend on.
- **Living review**: every number with unit, date and source, in the text and in
  `data/technologies/<id>.toml` (metrics from `data/metrics.toml`). Compare against the Landauer,
  Margolus-Levitin and Bekenstein bounds and the wall-plug energy. Vendor figures stay attributed
  to the vendor. Set `technology` and `last_reviewed` in the front matter.

On every page:

- Link the first use of each term to its concept:
  `[entropy](../../appendices/concepts.qmd#sec-concept-entropy)`. Add missing terms to
  `data/concepts.toml` and missing symbols to `data/notation.toml`.
- Refer to other pages by label (`@sec-landauer`), never by number or by "as we saw".
- Mark every claim that is not established with its span or callout and class (`.reported`,
  `.extrapolation`, `.speculation`, `.philosophy`). Run the `classify-claims` skill on the draft.
- Remove the "has not been written yet" callout. Set `status: drafting` and add the contributor's
  GitHub handle to `contributors`.

## 4. Check

```bash
python3 tools/generate.py
python3 tools/check.py
```

Both must pass. Then report, for the pull request template: the claims added by kind, the references
added by key, and the concepts and symbols added. Do not change claims in other pages; if one is
wrong, say so and suggest a scientific challenge issue.
