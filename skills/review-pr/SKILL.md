---
name: review-pr
description: Review a pull request to The Alan Machine against the project's rules (title convention, sign-off, claim classification, references, registers, data and generated files). Use when asked to review a pull request, or to check a branch before opening one.
---

# Review a pull request

## Gather

```bash
gh pr view <number> --json title,body,author,files,commits,labels
gh pr diff <number>
gh pr checks <number>
```

## Check

**Form**

- Title follows `type(scope): summary` (CONTRIBUTING.md): known type, scope is a page slug, a data
  file or, for `translation`, a language id, imperative, lowercase, no final period, at most 72
  characters.
- Every commit has a `Signed-off-by` line.
- One subject. The template is filled in, including the claims affected and how they are classified.

**Content**

- Run `classify-claims` on the changed prose. Every claim is classified, established claims cite a
  source, reported claims name their source and sit in a `{.reported}` span, extrapolations state
  their assumptions, philosophy gives at least two positions.
- Run `verify-references` on new or changed keys. No reference from memory.
- Register: chapters keep equations out of the running text; interludes add no physics later
  chapters depend on; living review numbers have unit, date and source in `data/technologies/`.
- Sections are self-contained; cross-references use labels.

**Structure**

- New pages are in `_quarto.yml` and their titles carry `{#sec-<slug>}`.
- New terms are in `data/concepts.toml`, new symbols in `data/notation.toml`.
- Generated files were regenerated, not edited by hand.
- A change to STYLE.md or CONTRIBUTING.md updates the skills and AGENTS.md where they repeat the
  rule.
- `python3 tools/check.py` passes and the `render` check is green.

## Report

Two lists: **blocking** (wrong or unsupported claims, invented references, broken build, missing
sign-off) and **suggestions** (style, clarity). Quote the line and propose the fix for each item.

Draft the review; post it with `gh pr review` only when the maintainer asks. Never approve, request
changes on or merge a pull request unless the maintainer says so.
