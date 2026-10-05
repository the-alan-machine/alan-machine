# 0014. Translations

- Date: 2026-10-05
- Status: accepted; narrows rule 8 of AGENTS.md ("English only") to the work, not its readers

## Context

The book is written for the general public, and much of that public reads another language better
than English. Translating it raises four problems:

- **The work has to stay in one language.** Review, moderation and the classification of claims
  happen in English; splitting them across languages would split the community that checks the
  physics.
- **Translations go stale.** A chapter is revised and its translation keeps the old wording. English
  contributors cannot be asked to update languages they do not read.
- **Translators are not physicists, and physicists are not translators.** The moderator of a part
  can judge the English of a chapter, not its Portuguese.
- **Machine translation is cheap and unreviewed.** Waiting for people to translate everything would
  publish almost nothing; publishing machine output as if reviewed would mislead.

The Escape Velocity atlas, which shares its methods with the book, faced the same problems and
answered them in its own decision 0014. This decision follows it where the two projects are alike.

## Decision

1. **English is the source of every text.** Code, data, commits, issues, decisions and the titles
   and descriptions of pull requests stay in English. A translation is derived from the English, and
   nothing in the English depends on it.
2. **Languages are registered** in `i18n/languages.toml`, each with its own maintainers. They
   approve the translations into their language through the `moderation` check, instead of the
   curators and moderators: the English was approved already, and what is left to judge is the
   language. Translators are credited in the People appendix of the book.
3. **A page is translated whole.** Its translation is `i18n/<lang>/<page path>`, with three fields
   of front matter: `translation` (`todo`, `machine` or `reviewed`), `source`, the fingerprint of
   the English body it was translated from, and `reviewers`. Every other field comes from the
   English page, so curators, statuses and dates are kept in one place.
4. **The data appendices are translated text by text.** Concepts, notation and constants have
   overlays in `i18n/<lang>/data/`, each text with the fingerprint of its English, and the
   translated appendices are generated from them. Symbols, values, units, identifiers and
   references are never translated.
5. **Staleness warns and never blocks.** When the English changes, its fingerprint no longer
   matches. `tools/check.py` warns, so an English contributor is never blocked. A stale page is
   still shown, with a notice and a link to the English; a stale data text falls back to English.
   Pages are long, and losing a whole chapter to a corrected comma would cost readers more than a
   notice.
6. **Machine translation may be published, marked as such.** A translation is `machine` until a
   person reviews it and sets `reviewed`, with their handle. Pages translated by machine say so,
   and pages not translated yet show the English with a notice.
7. **The checks that can be automated are errors**: a translated page must keep its English's
   citations, cross-references, labels, math, claim callouts, reported spans and generated tables;
   claim callouts carry the titles the language's `strings.toml` gives the kinds of claim; a data
   text keeps the numbers of its English; and a translation of a page or text the book does not have
   fails.
8. **Each language is an edition of the book** at `/<id>/` of the site, rendered from the English
   repository by `tools/edition.py` with the language's own `lang`, so Quarto's interface speaks
   it too. Each page links to the same page in the other editions.
9. **What stays in English only**: the papers, which are written for specialists in the language
   of their field; `llms.txt`, `llms-full.txt` and the MCP server; the PDF and EPUB editions; the
   decisions and the documentation.
10. **A translation pull request** has the type `translation` and the language as its scope. Its
    title and description are in English; discussion of the wording may be in the language.
11. **No translation platform for now.** Pull requests, `tools/translate.py` and the
    `translate-page` skill are enough while each language has a few translators. A platform such as
    Weblate is reconsidered when that stops being true.

## Consequences

- Adding a language is a registry entry, a `strings.toml`, a glossary and translated pages; no
  page of the book names a language.
- Portuguese (Brazil) is the first language, maintained by @JoaoAlisson, translated by machine
  from the start and reviewed as the chapters are written.
- Every change to English prose can make a translation stale. That is the translators' work, and
  `python3 tools/translate.py status` shows how much of it is waiting.
- Rendering the book takes one more Quarto render per published language.
