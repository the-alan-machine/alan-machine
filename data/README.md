# Data

The structured layer of The Alan Machine: one source for the book, for readers and for AI models.
People edit these files; `tools/generate.py` turns them into pages, and the published exports are
built from them. See [decision 0009](../docs/decisions/0009-knowledge-base-for-people-and-models.md).

| File | Becomes | Rule |
|---|---|---|
| `concepts.toml` | The Concepts appendix, one entry per term, with "Used in" links | A term enters here the first time a page uses it |
| `notation.toml` | The Notation appendix | A symbol enters here before it is used, and keeps one meaning |
| `constants.toml` | The Constants appendix | Values from the 2019 SI or CODATA, with the source |
| `metrics.toml` | The list of metrics a technology may report | A new metric enters here in the pull request that first uses it |
| `technologies/<id>.toml` | The numbers behind a Building Alan dossier | Every metric has a unit, an `as_of` date and a source |

The format is TOML because Python's standard library reads it (`tomllib`, Python 3.11 or later),
so building the book needs no installed packages.

Do not edit the generated appendices (`appendices/concepts.qmd`, `appendices/notation.qmd`,
`appendices/constants.qmd`) or the marked table in `building-alan/index.qmd`. Edit the data and run:

```bash
python3 tools/generate.py
```

`quarto render` and `quarto preview` run it for you before rendering.
