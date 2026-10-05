# Instructions for AI agents

This file is for coding agents that work in this repository (Claude Code, Codex, Cursor and
others). Humans should start with [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md);
everything here is consistent with them.

## What this repository is

The Alan Machine: an open-source book, written in English, about a hypothetical supercomputer named
Alan, used as a thought experiment about reversing entropy and what that would mean for time. It is a
[Quarto](https://quarto.org) book with build tools in Python's standard library.

| Path | What it holds |
|---|---|
| `chapters/<slug>/index.qmd` | Chapters, popular register |
| `interludes/<slug>/index.qmd` | Philosophical interludes, one at the end of each part |
| `building-alan/<slug>/index.qmd` | Building Alan dossiers: living documents on real technology |
| `papers/<slug>/index.qmd` | Standalone scientific papers |
| `appendices/` | Appendices; `concepts`, `notation`, `constants` and `people` are generated |
| `data/` | Concepts, notation, constants, metrics and technology data, in TOML |
| `references.bib` | The single bibliography |
| `governance.toml` | Maintainers and the moderators of each part ([GOVERNANCE.md](GOVERNANCE.md)) |
| `tools/` | `generate.py`, `check.py`, `export_llms.py` and `moderation.py` |
| `templates/` | Starting points for each kind of page |
| `skills/` | Agent skills for contributors |
| `docs/decisions/` | Why the project is the way it is |
| `_quarto.yml` | Page order and book configuration |

## Rules that are easy to break

1. **Never cite from memory.** Every reference comes from its source. Get BibTeX from the DOI:
   `curl -sL -H "Accept: application/x-bibtex" https://doi.org/<DOI>`, then rename the key to
   `authorYEARfirstword` with the year in the entry. If you cannot find a source for a claim, say so;
   do not write the claim as established. Use the `verify-references` skill.
2. **Classify every claim.** Established (running text with a citation), Extrapolation, Speculation
   or Philosophy (callouts with a title and a class). See [STYLE.md](STYLE.md#classifying-claims)
   and the `classify-claims` skill. Hedged running text ("might", "could") is usually an unmarked
   extrapolation or speculation.
3. **Do not edit generated files**: `appendices/concepts.qmd`, `appendices/notation.qmd`,
   `appendices/constants.qmd`, `appendices/people.qmd` and the marked table in
   `building-alan/index.qmd`. Edit `data/`, `governance.toml` or the front matter and run
   `python3 tools/generate.py`.
4. **Every number has a source**, and in a dossier also a date (`as_of`) and an entry in
   `data/technologies/<id>.toml`.
5. **Keep the registers apart.** Chapters keep equations out of the running text; the math goes in a
   collapsed "Going deeper" callout or in a paper.
6. **Write self-contained sections**: name the subject, link by label (`@sec-landauer`), no "as we
   saw".
7. **New page, new line in `_quarto.yml`**, with the title labeled `{#sec-<slug>}`.
8. **English only**: text, comments, commit messages, issues and pull requests.
9. **Roles are people's acts.** Never add anyone to `curators` or `governance.toml`, and never set
   `reviewed_by` or move `last_reviewed` of a dossier; a person does that ([GOVERNANCE.md](GOVERNANCE.md)).

## Before you finish

```bash
python3 tools/check.py
quarto render --to html     # when Quarto is installed
```

`tools/check.py` must pass. It needs only Python 3.11 or later.

## Commits and pull requests

- Title: `type(scope): summary`, imperative, lowercase, no final period, at most 72 characters.
  Types: `content`, `paper`, `fix`, `ref`, `fig`, `data`, `build`, `docs`, `chore`. The scope is the
  page slug. See [CONTRIBUTING.md](CONTRIBUTING.md#commit-and-pull-request-titles).
- Every commit is signed off (`git commit -s`) by the human contributor responsible for it. The
  sign-off is a human's certification; an agent does not certify on anyone's behalf.
- Fill in the pull request template, including the claims affected and how they are classified.
- Never commit `_book/` or `.quarto/`.

## Skills

| Skill | Use it to |
|---|---|
| [`write-chapter`](skills/write-chapter/SKILL.md) | Draft or revise a chapter, interlude or dossier |
| [`classify-claims`](skills/classify-claims/SKILL.md) | Find and classify every claim on a page |
| [`verify-references`](skills/verify-references/SKILL.md) | Check citations and BibTeX entries against their sources |
| [`review-pr`](skills/review-pr/SKILL.md) | Review a pull request against the project's rules |

## Reading the book as a knowledge base

To answer questions about the book rather than edit it, use the published exports: `llms.txt`,
`llms-full.txt` and the per-page Markdown at
https://the-alan-machine.github.io/the-alan-machine/. Keep the kind of each claim when you quote it.
