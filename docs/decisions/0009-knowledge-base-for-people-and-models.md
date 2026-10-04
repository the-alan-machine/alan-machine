# 0009. A knowledge base for people and models

- Date: 2026-10-04
- Status: accepted

## Context

More and more readers will reach the book through AI models: assistants, search and agents that
research for someone. Researchers will want to query the book, not only read it. A model that reads
the book badly will misquote it, and the book's main value, the separation between what physics says
and what the book imagines, is exactly what a careless extraction loses.

## Decision

**Authors write prose; tooling derives the machine-readable layer.** No contributor writes JSON by
hand, and no machine-readable file is maintained in parallel with the text.

1. **Data layer.** `data/` holds the structured facts in TOML: concepts, notation, constants,
   metrics and technologies. TOML is read by Python's standard library, so building the book needs
   no installed packages. The Concepts, Notation and Constants appendices are generated from it by
   `tools/generate.py`, which Quarto runs before every render. CI fails when a committed generated
   page is out of date.
2. **Concepts instead of a wiki or a glossary.** The Concepts appendix has one entry per term, a
   plain-language definition, related concepts, references, and "Used in" links to every page that
   links to it. It is one page with an anchor per term, not one page per term: Quarto's navigation
   and cross-references work at the page level, and hundreds of pages would bury the chapters.
3. **Self-contained sections.** A section makes sense when it is read alone: it names its subject
   instead of saying "as we saw", and it links to what it builds on by label.
4. **Machine-readable claim markers.** A classified callout carries a class as well as a title
   (`.extrapolation`, `.speculation`, `.philosophy`), so any extractor can tell the kinds apart in
   any output format.
5. **Published exports**, built in CI after each render:
   - one Markdown file per page at `<page>.html.md`, following the [llms.txt](https://llmstxt.org)
     convention, with front matter (title, URL, kind, part, status, source, license) and every
     cross-reference resolved to an absolute URL;
   - `llms.txt`, an index of the book with the reading rules (the four kinds, citation keys, status);
   - `llms-full.txt`, the whole book in one file;
   - the `data/` folder and `references.bib`, as published files.
6. **Later**: a JSON export with a versioned schema (every claim with its kind, location and
   citations), a Zenodo DOI for each release, and the `alan` Python library, which computes the
   physical limits from the same data.
7. **AI use.** The README states that models and tools may use the text under CC BY 4.0, citing the
   page URL and keeping the kind of each claim.

## Alternatives considered

- **A wiki.** Rejected: unreviewed, with no citation or claim checks, and it splits the content.
- **YAML for the data.** Rejected: Python needs a third-party parser for it; TOML is in the standard
  library since Python 3.11.
- **Hand-written JSON.** Rejected: hostile to contributors and certain to drift from the text.

## Consequences

- Rendering the book locally needs Python 3.11 or later, besides Quarto.
- The generated pages must not be edited by hand; their first line says so.
- The tools read the page order from `_quarto.yml` and expect one file per line under `chapters:`
  and `appendices:`.
