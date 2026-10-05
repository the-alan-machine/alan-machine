# 0015. Claims export

- Date: 2026-10-05
- Status: accepted; implements the claims part of the JSON export planned in 0009 §6

## Context

[Decision 0009](0009-knowledge-base-for-people-and-models.md) made the book a knowledge base for
people and models, and left for later "a JSON export with a versioned schema (every claim with its
kind, location and citations)", a Zenodo DOI for each release and the `alan` Python library.
[Decision 0010](0010-agents-skills-and-mcp.md) plans a read-only MCP server in `alan-tools` that
depends on that export staying stable.

The Markdown exports already carry the claim markers, but a tool that wants the claims has to parse
Quarto's callouts and spans itself, and every tool would parse them a little differently. The kind
of a claim is the one thing the book asks every reader, human or model, to keep when quoting it.

## Decision

1. **`claims.json`** is written by `tools/export_llms.py` next to `llms.txt`, in the same CI step,
   and `llms.txt` points to it. It is built with Python's standard library, from the sources, so it
   does not need the rendered book.
2. **Only marked claims are listed.** By [decision 0005](0005-claim-classification.md), "Only what
   leaves established physics is marked"; unmarked running text is established, and listing it would
   mean guessing where one claim ends and the next begins. The file states this rule in
   `established_rule`. The marks are the callouts of class `.extrapolation`, `.speculation` and
   `.philosophy`, and the `[...]{.reported}` spans of [decision 0013](0013-reported-claims-and-living-reviews.md).
3. **Only the pages of the book are read**, in the order of `_quarto.yml`; never `templates/` or the
   translations. Fenced code, inline code and HTML comments are removed first, as `tools/check.py`
   does, so examples of the syntax are not claims.
4. **Schema 1.** The top level has `schema` (1), `version` and `version_date` (the short commit and
   its date), `license`, `site`, `established_rule`, `counts` by kind and `claims`. Each claim has:

   | Field | Meaning |
   |---|---|
   | `kind` | `reported`, `extrapolation`, `speculation` or `philosophy` |
   | `page` | the `.qmd` path of the page |
   | `url` | the page URL, with the `#id` of the section when its heading has one |
   | `section` | the text of the heading the claim is under |
   | `title` | the callout title, when there is one |
   | `text` | the Markdown of the callout body or of the span |
   | `citations` | the citation keys in the text, entries of `references.bib`; cross-references are left out |
   | `page_status` | the `status` of the page's front matter, when it has one |

   A field without a value is left out. Adding a field keeps schema 1; removing or renaming a field,
   or changing what one means, raises the number.
5. **English only** in version 1, like `llms.txt` ([decision 0014](0014-translations.md) §9).
6. **The MCP server serves this file.** The `alan-tools` server of decision 0010 §4 reads
   `claims.json` instead of parsing the book.
7. **Still later**: the Zenodo DOI for each release, the `alan` library, and the rest of the JSON
   export of 0009 §6.

## Consequences

- A tool or a model can list, filter and cite the claims of the book by kind without parsing
  Quarto, and can check a quotation against the kind the book gives it.
- The extractor and `tools/check.py` read callouts and citations with the same regular expressions,
  kept in `tools/book.py`, so what the check counts and what the export lists cannot drift apart.
- Established claims are not in the file. A reader who needs them reads the page, through its URL.
- While the pages are proposals, the file lists no claims; it fills as the chapters are written.
