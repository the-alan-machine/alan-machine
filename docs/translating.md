# Translating the book

The book is written in English and translated into other languages by people who read both
([decision 0014](decisions/0014-translations.md)). A translation never changes the English: it is
an edition built from it, and where a page is not translated yet readers see the English, with a
notice.

| Language | Folder | Maintainers | Edition |
|---|---|---|---|
| Portuguese (Brazil) | [`i18n/pt/`](../i18n/pt/) | @JoaoAlisson | [/pt/](https://the-alan-machine.github.io/the-alan-machine/pt/) |

The list is [`i18n/languages.toml`](../i18n/languages.toml).

## What there is to translate

| What | Where |
|---|---|
| A page: the preface, a chapter, an interlude, a living review, an appendix written by hand | `i18n/<lang>/<page path>`, such as `i18n/pt/chapters/landauer/index.qmd` |
| The concepts, the notation and the constants | `i18n/<lang>/data/concepts.toml`, `notation.toml`, `constants.toml` |
| The words around the pages: part titles, the titles of the kinds of claim, notices, the headings of the generated appendices, the decimal mark | `i18n/<lang>/strings.toml`, by the keys of `ENGLISH` in [`tools/i18n.py`](../tools/i18n.py) |
| The terms of the book | `i18n/<lang>/glossary.toml` |

Not translated: the papers, which stay in English for specialists; the generated appendices, which
the edition writes from the data overlays and `strings.toml`; math, code, citation keys, labels,
file names and addresses; the titles of sources, and quotations, which stay as the source wrote
them.

## A translated page

A translated page has its own front matter, with three fields, and the translated body:

```yaml
---
translation: machine   # todo until translated, then machine or reviewed
source: 9d07a9bba5     # fingerprint of the English body it was translated from
reviewers: []          # GitHub handles of whoever reviewed this translation
---
```

Everything else, such as the curators, the status and the dates, comes from the English page. In
the body:

- keep every label (`{#sec-landauer}`), citation (`[@landauer1961irreversibility]`),
  cross-reference (`@sec-landauer`), equation and link to another page as they are;
- keep the class of every claim callout and use the title `strings.toml` gives it under
  `[claims]`: `::: {.callout-warning .extrapolation title="Extrapolação"}`. Keep reported spans,
  `[...]{.reported}`, around the same claims;
- translate the title of "Going deeper" boxes with the glossary;
- leave HTML comments in English: they are notes for contributors;
- leave the generated table of `building-alan/index.qmd` as it is: the edition writes it in the
  language.

`tools/check.py` fails if a translated page loses or adds a citation, a label, an equation, a claim
callout or a reported span.

## A data text

Each file under `i18n/<lang>/data/` lists the texts that replace the English of a data file:

```toml
status = "machine"         # or "reviewed"
reviewed_by = []           # GitHub handles of whoever reviewed the whole file

[[text]]
path = "concept[entropy].term"   # where the text is in the data file
source = "bb846881f6"            # fingerprint of the English it was translated from
text = "Entropia"
```

`path` names the field: `concept[<id>].term`, `.short` or `.definition`, `symbol[<id>].meaning`,
`constant[<id>].name` or `.source`. You do not have to write paths or fingerprints: the tool does.
`tools/check.py` fails if a number in a text differs from the English.

## Step by step

```bash
python3 tools/translate.py status --lang pt                        # what is missing or stale
python3 tools/translate.py template pt chapters/landauer/index.qmd # start a page from the English
python3 tools/translate.py show pt data/concepts.toml              # English and translation side by side
python3 tools/check.py
```

`template` copies the English page to `i18n/<lang>/`, with `translation: todo`; translate it in
place and set `translation: machine` or, if you are a person who read it against the English,
`reviewed` with your handle in `reviewers`. For a data file, `template` adds every text the overlay
lacks with an empty `text`; fill in the ones you translate and leave the rest empty.

To see the edition, render the English book first and then the translation:

```bash
quarto render --to html
python3 tools/edition.py --render pt    # into _book/pt/
```

Use the terms in `i18n/<lang>/glossary.toml`; if a term is missing or wrong, change it in the same
pull request and say why.

## When the English changes

The fingerprint of the English no longer matches and the translation is **stale**: `tools/check.py`
warns, the edition shows a stale page with a notice and a link to the English, and a stale data text
in English. To update a page, see what changed since it was translated, fix the translation and
record the English it now follows:

```bash
python3 tools/translate.py status --lang pt --list stale
python3 tools/translate.py changes pt chapters/landauer/index.qmd
python3 tools/translate.py stamp pt chapters/landauer/index.qmd
python3 tools/translate.py stamp pt data/concepts.toml --path "concept[entropy].definition"
```

Stamp only what you have read. Stamping without updating the text hides a stale translation.

## Machine and reviewed

A translation made by a model is `machine`, and its page says that the text has not been reviewed.
Whoever reviews it against the English sets `reviewed` and adds their handle. A data text added later
by a model can carry its own `status = "machine"` in a reviewed file.

An agent translating follows the [`translate-page`](../skills/translate-page/SKILL.md) skill and
leaves its work as `machine`; a person reviews it.

## Pull requests

- Title: `translation(<lang>): <what>`, in English, such as
  `translation(pt): translate the landauer chapter`.
- The description is in English; comments on the wording can be in the language.
- One of the language's maintainers approves it. Curators and moderators do not need to: the
  English was approved already.
- The [translation form](../.github/ISSUE_TEMPLATE/translation.yml) reports a wrong translation or
  offers help with a language.
- Translators are credited in the [Moderators and Curators](https://the-alan-machine.github.io/the-alan-machine/appendices/people.html)
  appendix: the language's maintainers and whoever reviewed a translation.

## A new language

Open an issue with the translation form. A maintainer adds the language to `i18n/languages.toml`
with `published = false` and you as its maintainer; you write `strings.toml`, a glossary and the
translations of the preface and the data; then the language is published, and the build renders its
edition and links it from every page.
