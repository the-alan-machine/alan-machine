# Contributing to The Alan Machine

Thank you for helping. This book is written in the open, and anyone can improve any chapter,
interlude, living review, figure or paper.

Before you start, read the [Code of Conduct](CODE_OF_CONDUCT.md) and the [Style Guide](STYLE.md).

## Ground rules

- Everything is written in English: text, notes, issues, pull requests and commit messages.
- Every claim is established, reported, an extrapolation, speculation or philosophy, and the
  reader can always tell which. See [Classifying claims](STYLE.md#classifying-claims).
- Every established claim cites a peer-reviewed paper or a standard textbook.
- Every reference comes from its source. Never cite from memory.

## Ways to contribute

| You want to | Do this |
|---|---|
| Fix a typo, a broken link or formatting | Open a pull request directly. |
| Fix an error in an equation or a number | Open a pull request with the reference that shows the correct value. |
| Challenge a scientific claim, or how it is classified | Open a **Scientific challenge** issue with references. Send the pull request once the issue is agreed. |
| Write a new chapter, section, interlude, living review or paper | Open a **Content proposal** issue first: topic, why it belongs, outline and key references. Start writing once it is accepted. |
| Update the numbers in a Building Alan living review | Open a **Living review update** issue, or a pull request to `data/technologies/` with the value, unit, date and source. |
| Define a term, or improve a definition | Open a pull request to `data/concepts.toml`. |
| Suggest a reference | Open a **Reference suggestion** issue, or a pull request to `references.bib`. |
| Explore an open idea ("what if Alan could...") | Start a thread in Discussions. Ideas that mature become proposals. |

## Writing in two registers

The book has two registers. You can write in either one, or in both.

- **Chapters** (`chapters/<slug>/index.qmd`) are for the general public: plain, conversational
  English, few equations, and optional "Going deeper" boxes for the math. Start from
  [`templates/chapter.qmd`](templates/chapter.qmd).
- **Papers** (`papers/<slug>/index.qmd`) are for specialists: full derivations, stated assumptions
  and complete references. Each paper has its own authors and abstract and can be cited on its own.
  Start from [`templates/paper.qmd`](templates/paper.qmd).

Two more kinds of page sit beside the chapters:

- **Interludes** (`interludes/<slug>/index.qmd`) close each part with one philosophical question.
  Start from [`templates/interlude.qmd`](templates/interlude.qmd).
- **Building Alan living reviews** (`building-alan/<slug>/index.qmd`) describe how close one
  technology comes to Alan's limits. Each one carries a review date. Start from
  [`templates/living-review.qmd`](templates/living-review.qmd).

A chapter links to the papers behind it with a "The science behind this chapter" box and lists
their slugs in its front matter (`papers:`). A paper lists the chapters it supports (`chapters:`).
A chapter can be published before its paper exists, as long as its established claims cite the
literature.

When you add a page, also add its file to `_quarto.yml`. Terms go in `data/concepts.toml`, symbols
in `data/notation.toml` and constants in `data/constants.toml`; the appendices are generated from
them. See [`data/README.md`](data/README.md).

## Workflow

1. Fork the repository and create a branch named `type/short-description`, for example
   `content/szilard-engine` or `paper/landauer-bound`.
2. Make your changes, then check them and build the book:

   ```bash
   python3 tools/check.py
   quarto render --to html
   ```

   `tools/check.py` needs only Python 3.11 or later. It catches citation keys missing from
   `references.bib`, cross-references to labels that do not exist, generated pages out of date and
   pages missing from `_quarto.yml`.
3. Commit with sign-off (see [Developer Certificate of Origin](#developer-certificate-of-origin)).
4. Open a pull request and fill in the template.

Pull requests are merged with **squash merge**: the pull request title becomes the single commit on
`main`. The title must follow the convention below. The commits inside your branch do not need to.

## Commit and pull request titles

Format: `type(scope): summary`

| Type | Use for |
|---|---|
| `content` | New or rewritten text in a chapter |
| `paper` | New or rewritten text in a paper |
| `fix` | Correction of an error |
| `ref` | References and `references.bib` |
| `fig` | Figures and the code that produces them |
| `data` | Concepts, notation, constants and technology data in `data/` |
| `build` | Quarto configuration, CI, dependencies |
| `docs` | Project documentation: README, CONTRIBUTING, STYLE, decisions |
| `chore` | Maintenance that changes no content |

- `scope` is the slug of the chapter, interlude, living review or paper (`landauer`,
  `does-time-flow`, `cmos-baseline`), or the data file for `data` (`concepts`). Leave it out when
  the change is not about a single page.
- `summary` is in the imperative mood, lowercase, with no final period and at most 72 characters.
- The body, when there is one, explains why the change was made.

```
content(maxwells-demon): add section on the Szilard engine
paper(landauer): derive the bound for a single-bit memory
fix(landauer): correct the factor in the erasure bound
ref(speed-limits): add Margolus and Levitin 1998
fig(local-reversal): plot the spin echo signal
content(cmos-baseline): update energy per operation to 2026
data(concepts): define the Bekenstein bound
build: render the PDF edition in CI
docs: explain the two registers in CONTRIBUTING
```

## Developer Certificate of Origin

Every commit must be signed off with `git commit -s`. The `Signed-off-by` line certifies that you
wrote the contribution, or otherwise have the right to submit it, under the project's licenses. See
[developercertificate.org](https://developercertificate.org). There is no separate contributor
agreement.

## Pull requests

- One subject per pull request.
- Fill in the template: what changes, which pages, which claims are affected and how they are
  classified, and which references were added.
- Every pull request needs an approval from a curator of the pages it changes or a moderator of
  their part; the `moderation` check says who, requests their review and passes once one of them
  approves. Without one, a maintainer reviews. Typo and formatting fixes need a light review.
- Roles, the yearly review of living reviews, conflicts of interest and how to become a moderator or
  curator are in [GOVERNANCE.md](GOVERNANCE.md).

## Credit

- Chapter contributors are listed in the chapter's front matter (`contributors:`) and in the
  book's acknowledgments.
- Paper authorship follows academic practice: an author made a substantial contribution to the
  content and approved the final version. Everyone else who helped is acknowledged in the paper.

## Writing with AI assistance

You may use AI tools to help you write. You are responsible for everything you submit, and above
all for every reference: check each one against its source. Invented references are the most
common failure of machine-generated text, and the most damaging one for a scientific book.

The fastest way to get a correct BibTeX entry is from the DOI:

```bash
curl -sL -H "Accept: application/x-bibtex" https://doi.org/<DOI>
```

The repository includes instructions for coding agents in [AGENTS.md](AGENTS.md) and skills in
[`skills/`](skills/): `write-chapter`, `classify-claims`, `verify-references` and `review-pr`.
Claude Code picks them up automatically; other agents can read them as plain Markdown. To check
every DOI entry in `references.bib` against Crossref:

```bash
python3 skills/verify-references/scripts/verify_bib.py
```

## Licenses

By contributing, you agree that your text and figures are licensed under
[CC BY 4.0](LICENSE) and your code under [MIT](LICENSE-CODE).
