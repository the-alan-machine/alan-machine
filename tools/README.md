# Tools

Build tools for the book. They use only the Python standard library (Python 3.11 or later).

| Script | What it does | Who runs it |
|---|---|---|
| `generate.py` | Writes the Concepts, Notation, Constants and Moderators and Curators appendices, the Building Alan living review table and the language links of `_quarto.yml` from `data/`, `governance.toml`, `i18n/languages.toml` and the front matter. `--check` only reports. | Quarto, before every render (`pre-render` in `_quarto.yml`); you, after editing `data/` |
| `check.py` | Checks the sources: generated pages up to date, data valid, citation keys, cross-references, front matter, `_quarto.yml`, `governance.toml` and the GitHub handles in it and in `curators`, and the translations: their registry, words, glossary, data texts and pages against their English. | You, before a pull request; CI, on every pull request |
| `export_llms.py` | Writes `llms.txt`, `llms-full.txt`, the per-page Markdown and copies of `data/` and `references.bib` into `_book/`. | CI, after rendering |
| `moderation.py` | `pr` says who has to approve a pull request and whether they have ([GOVERNANCE.md](../GOVERNANCE.md)); `issue` finds the parts of the book and the language an issue names. Reads the pull request as text and never runs its code. | `.github/workflows/moderation.yml` and `triage.yml` |
| `book.py` | Shared helpers: page order from `_quarto.yml`, front matter, data and bibliography. | The other scripts |
| `i18n.py` | Shared helpers for translations ([decision 0014](../docs/decisions/0014-translations.md)): the languages, the English words of the editions, fingerprints, translated pages and data overlays. | The other scripts |
| `translate.py` | `status` of each language, `template` to start a page or data overlay, `show` English and translation side by side, `changes` in the English since a page was translated, `stamp` after updating it ([docs/translating.md](../docs/translating.md)). | Translators |
| `edition.py` | Writes each translated edition's sources to `_i18n/<lang>/`: translated pages under the English front matter, notices, generated appendices and `_quarto.yml` in the language. `--render` renders it into `_book/<lang>/`, after the English render. | CI, after rendering; you, to see an edition |

The tools read the page order from `_quarto.yml` and expect one file per line under `chapters:` and
`appendices:`, with parts written as `- part: "Title"`.
