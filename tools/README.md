# Tools

Build tools for the book. They use only the Python standard library (Python 3.11 or later).

| Script | What it does | Who runs it |
|---|---|---|
| `generate.py` | Writes the Concepts, Notation and Constants appendices and the Building Alan dossier table from `data/`. `--check` only reports. | Quarto, before every render (`pre-render` in `_quarto.yml`); you, after editing `data/` |
| `check.py` | Checks the sources: generated pages up to date, data valid, citation keys, cross-references, front matter, `_quarto.yml`. | You, before a pull request; CI, on every pull request |
| `export_llms.py` | Writes `llms.txt`, `llms-full.txt`, the per-page Markdown and copies of `data/` and `references.bib` into `_book/`. | CI, after rendering |
| `book.py` | Shared helpers: page order from `_quarto.yml`, front matter, data and bibliography. | The other scripts |

The tools read the page order from `_quarto.yml` and expect one file per line under `chapters:` and
`appendices:`, with parts written as `- part: "Title"`.
