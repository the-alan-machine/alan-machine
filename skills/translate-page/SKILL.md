---
name: translate-page
description: Translate a page (preface, chapter, interlude, living review, appendix) or the concepts, notation and constants of The Alan Machine from English into a language registered in i18n/languages.toml, under i18n/<lang>/. Use when asked to translate part of the book, to update stale translations, or to work on an issue opened with the translation form.
---

# Translate a page

English is the source; a translation is a copy of a page, or an overlay of data texts, under
`i18n/<lang>/`, from which the edition in that language is built
([decision 0014](../../docs/decisions/0014-translations.md),
[docs/translating.md](../../docs/translating.md)). You write the translation; a person who reads
the language reviews it.

## 1. Check the language and what is missing

```bash
python3 tools/translate.py status --lang <lang> --list missing
python3 tools/translate.py status --lang <lang> --list stale
```

The language must be in `i18n/languages.toml`. If it is not, stop: adding a language is a
maintainer's decision, asked for with the translation form. Papers are never translated, and the
generated appendices are written from the data overlays.

## 2. Read the glossary and the words of the edition

Open `i18n/<lang>/glossary.toml` and `i18n/<lang>/strings.toml`. Use the glossary's term for every
English term it lists, on every page, even where another word would read better in that sentence;
one term, one word. If a term the page needs is missing, add it to the glossary in the same pull
request. The titles of claim callouts are under `[claims]` in `strings.toml`.

## 3. Prepare the file

```bash
python3 tools/translate.py template <lang> <page or data file>
```

For a page, `template` copies the English to `i18n/<lang>/<page path>` with `translation: todo`
and the fingerprint of the English in `source`; translate the body in place and leave `source`
alone. For a data file, it adds each text the overlay lacks with an empty `text`; fill in `text`
and do not touch `path` or `source`. `show` prints each English data text next to its translation.

## 4. Translate

- **Meaning first.** Translate what the English claims, at the same strength. The kind of a claim
  is part of its meaning: an established claim stays plain, a reported one keeps naming its source
  ("a 2025 preprint reports"), and hedges ("about", "at least", "might") stay. A translation that
  sounds surer than the English is wrong.
- **Keep the structure.** Every label (`{#sec-...}`), citation (`[@key]`), cross-reference
  (`@sec-...`), equation, code block, link to another page, reported span (`[...]{.reported}`) and
  callout class stays where the English has it. Claim callouts take the title in `[claims]`.
- **Numbers stay as written**, with the language's decimal mark: `1.5` becomes `1,5` in Portuguese
  text and `1{,}5` in math. Units and symbols stay.
- **Never translate**: math, citation keys, labels, names of people, institutions and products,
  the titles of sources, and quotations, which stay as the source wrote them. Alan, The Alan
  Machine and Escape Velocity are names.
- **Leave as they are**: HTML comments, which are notes for contributors, and the generated table
  of `building-alan/index.qmd`, which the edition writes in the language.
- **Style**: the register of the English. Chapters are plain and conversational, living reviews
  are precise and dated. No added explanations; if the English is unclear, say so in the pull
  request instead of guessing.

## 5. Mark it as machine translation

Set `translation: machine` on a page and leave `reviewers: []`; leave `status = "machine"` and
`reviewed_by = []` in a data overlay. Only a person who read the translation against the English
sets `reviewed` and adds their handle.

## 6. Check

```bash
python3 tools/check.py
quarto render --to html && python3 tools/edition.py --render <lang>   # when Quarto is installed
```

`check.py` fails when a translated page loses or adds a citation, a label, an equation, a claim
callout or a reported span, when a claim callout has another title than `[claims]`, and when a data
text's numbers differ from the English; fix the translation, not the check. Then open the page in
`_book/<lang>/`.

## 7. Updating stale translations

For a stale page, see what changed in the English since it was translated, update the translation,
then record the English it now follows:

```bash
python3 tools/translate.py changes <lang> <page>
python3 tools/translate.py stamp <lang> <page>
python3 tools/translate.py stamp <lang> <data file> --path "<path>"
```

Never stamp a translation you did not update.

## 8. The pull request

Title `translation(<lang>): <what>`, in English, such as
`translation(pt): translate the landauer chapter`. Say which model translated it. One of the
language's maintainers approves it (GOVERNANCE.md).
