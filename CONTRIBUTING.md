# Contributing to The Alan Machine

Thank you for helping. This book is written in the open, and anyone can improve any chapter,
interlude, living review, figure or paper. You do not need to know git: half of the ways to help
below are a form on GitHub.

Before you start, read the [Code of Conduct](CODE_OF_CONDUCT.md) and the [Style Guide](STYLE.md).
The book also has a short [Contributing](https://the-alan-machine.github.io/the-alan-machine/contributing.html)
page for readers; this file holds the complete rules.

## Pick your path

| You are | Start here |
|---|---|
| A reader who found an error, has a reference, or wants to propose or challenge something, and does not use git | [Without git: the issue forms](#without-git-the-issue-forms) |
| Someone who wants to fix a few words and has a GitHub account, but not git on their computer | [In the browser: edit a page on GitHub](#in-the-browser-edit-a-page-on-github) |
| Someone who will write, edit data or change several files | [With git: step by step](#with-git-step-by-step) |
| A translator | [docs/translating.md](docs/translating.md), then the steps with git |

All of them need a free [GitHub account](https://github.com/signup).

## Ground rules

- Everything is written in English: text, notes, issues, pull requests and commit messages.
  Translations of the book are the exception and live only under `i18n/<lang>/`
  ([docs/translating.md](docs/translating.md)); their pull requests are still titled and described
  in English.
- Every claim is established, reported, an extrapolation, speculation or philosophy, and the
  reader can always tell which. See [Classifying claims](STYLE.md#classifying-claims).
- Every established claim cites a peer-reviewed paper or a standard textbook.
- Every reference comes from its source. Never cite from memory.

## Ways to contribute

| You want to | Do this |
|---|---|
| Fix a typo, a broken link or formatting | Open a pull request directly, or an **Erratum** issue if you do not use git. |
| Fix an error in an equation or a number | Open a pull request with the reference that shows the correct value, or an **Erratum** issue with that reference. |
| Challenge a scientific claim, or how it is classified | Open a **Scientific challenge** issue with references. Send the pull request once the issue is agreed. |
| Write a new chapter, section, interlude, living review or paper | Open a **Content proposal** issue first: topic, why it belongs, outline and key references. Start writing once it is accepted. |
| Update the numbers in a Building Alan living review | Open a **Living review update** issue, or a pull request to `data/technologies/` with the value, unit, date and source. |
| Define a term, or improve a definition | Open a pull request to `data/concepts.toml`. |
| Suggest a reference | Open a **Reference suggestion** issue, or a pull request to `references.bib`. |
| Report a wrong translation, or offer to translate | Open a **Translation** issue ([docs/translating.md](docs/translating.md)). |
| Explore an open idea ("what if Alan could...") | Start a thread in [Discussions](https://github.com/the-alan-machine/the-alan-machine/discussions). Ideas that mature become proposals. |

## Without git: the issue forms

Each form asks for what a reviewer needs, so fill in every field it marks as required. Write in
English.

| Form | Use it for |
|---|---|
| [Erratum](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=erratum.yml) | A typo, a broken link, or an error in an equation or a number |
| [Scientific challenge](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=scientific-challenge.yml) | A claim that is wrong, unsupported, or classified as the wrong kind |
| [Content proposal](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=content-proposal.yml) | A new chapter, section, interlude, living review or paper, before writing it |
| [Living review update](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=living-review-update.yml) | New or corrected numbers for a Building Alan living review |
| [Reference suggestion](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=reference-suggestion.yml) | A paper or book that should be cited or listed as further reading |
| [Translation](https://github.com/the-alan-machine/the-alan-machine/issues/new?template=translation.yml) | A wrong or missing translation, a term of a glossary, or an offer to translate |

Blank issues are turned off. A question or an idea that is not a proposal yet goes to
[Discussions](https://github.com/the-alan-machine/the-alan-machine/discussions).

An issue opened from a form is labeled with the parts of the book it names, and their moderators
and the curators of the pages are mentioned in a comment, so the right people see it
([GOVERNANCE.md](GOVERNANCE.md#moderators)).

## In the browser: edit a page on GitHub

For a small change to the text of one page:

1. At the foot of the page of the book, open "Edit this page". It opens the source file of the
   page in GitHub's editor.
2. GitHub offers to fork the repository into your account, since you cannot edit the original;
   accept.
3. Make the change. Keep the [Style Guide](STYLE.md), and keep every label (`{#sec-...}`), citation
   (`[@key]`) and callout as they are.
4. Commit it. The commit message is a title that follows
   [the convention](#commit-and-pull-request-titles), and its description ends with the sign-off
   line of the [Developer Certificate of Origin](#developer-certificate-of-origin), written by
   hand: `Signed-off-by: Your Name <you@example.com>`.
5. Open the pull request GitHub proposes, and fill in the template. Then follow
   [After you open the pull request](#after-you-open-the-pull-request).

The checks of the pull request build the book for you. Anything larger than a few words is easier
with git.

## With git: step by step

The steps start from a computer with nothing installed. Commands are typed in a terminal.

### 1. Install the tools

- **Git**: [git-scm.com/downloads](https://git-scm.com/downloads). Tell it your name and the
  email of your GitHub account, which go into the sign-off of your commits:

  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"
  ```

- **Python 3.11 or later**, from [python.org](https://www.python.org/downloads/) or a package
  manager. `tools/check.py` needs nothing else, but it needs that version: the `python3` that comes
  with macOS is older (3.9) and stops with `ModuleNotFoundError: No module named 'tomllib'`. Check
  the version you have:

  ```bash
  python3 --version
  ```

- **Quarto**, only if you want to see the book as it will be published:
  [quarto.org/docs/get-started](https://quarto.org/docs/get-started/). The checks of every pull
  request render it anyway. Check it with `quarto --version`.

### 2. Fork and clone

Select **Fork** at the top of the
[repository](https://github.com/the-alan-machine/the-alan-machine) to make your copy, then bring
your copy to your computer and keep a link to the original:

```bash
git clone https://github.com/<your-user>/the-alan-machine.git
cd the-alan-machine
git remote add upstream https://github.com/the-alan-machine/the-alan-machine.git
```

### 3. Create a branch

One branch per subject, named `type/short-description`, with a type from
[the list below](#commit-and-pull-request-titles), for example `content/szilard-engine`,
`paper/landauer-bound` or `fix/landauer-factor`:

```bash
git checkout -b content/szilard-engine
```

### 4. Make your change

Edit the files with any text editor. [Writing in two registers](#writing-in-two-registers) says
where each kind of page lives and which template to start from, and the [Style Guide](STYLE.md)
says how to write it. A new page also needs a line in `_quarto.yml`. Do not edit the generated
appendices (`appendices/concepts.qmd`, `notation.qmd`, `constants.qmd`, `people.qmd`): edit
`data/` and run `python3 tools/generate.py`.

### 5. Check it

```bash
python3 tools/check.py
```

It must end with `ok:`. It catches citation keys missing from `references.bib`, cross-references
to labels that do not exist, generated pages out of date and pages missing from `_quarto.yml`. Lines
that start with `warning:` do not block, but read them: they name what needs a person, such as a
translation that has gone stale.

### 6. Build the book (optional)

```bash
quarto render --to html
```

The book is written to `_book/`; open `_book/index.html` in a browser. Never commit `_book/` or
`.quarto/`. To build a translation as well, see [docs/translating.md](docs/translating.md).

### 7. Commit with sign-off

```bash
git add <the files you changed>
git commit -s -m "content(maxwells-demon): add section on the Szilard engine"
```

`-s` adds the sign-off line ([Developer Certificate of Origin](#developer-certificate-of-origin)).
Every commit needs it.

### 8. Push and open the pull request

```bash
git push -u origin content/szilard-engine
```

GitHub then shows a button to open a pull request from your branch. Give it a title that follows
[the convention](#commit-and-pull-request-titles) and fill in the template: what changes, which
pages, which claims are affected and how they are classified, and which references were added.

### After you open the pull request

- **Checks.** `tools/check.py` runs, the book and its translations are built, and the `moderation`
  check requests a review from the people who can approve your change and lists them in a comment.
- **Review.** A curator of the pages or a moderator of their part reviews it, or a maintainer when
  nobody else covers it ([Pull requests](#pull-requests)). To answer a review, commit to the same
  branch with `git commit -s` and push again; the pull request updates itself.
- **Merge.** A maintainer merges it with squash merge, and the pull request title becomes the
  commit on `main`. How contributors are credited is under [Credit](#credit).

Before your next contribution, bring your copy up to date and start from a new branch:

```bash
git checkout main
git pull upstream main
git checkout -b type/next-subject
```

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

In short, the steps above:

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
| `translation` | Translations under `i18n/<lang>/`, with the language as scope ([docs/translating.md](docs/translating.md)) |
| `build` | Quarto configuration, CI, dependencies |
| `docs` | Project documentation: README, CONTRIBUTING, STYLE, decisions |
| `chore` | Maintenance that changes no content |

- `scope` is the slug of the chapter, interlude, living review or paper (`landauer`,
  `does-time-flow`, `cmos-baseline`), the data file for `data` (`concepts`), or the language for
  `translation` (`pt`). Leave it out when the change is not about a single page.
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
translation(pt): translate the landauer chapter
build: render the PDF edition in CI
docs: explain the two registers in CONTRIBUTING
```

## Developer Certificate of Origin

Every commit must be signed off with `git commit -s`. The `Signed-off-by` line certifies that you
wrote the contribution, or otherwise have the right to submit it, under the project's licenses. See
[developercertificate.org](https://developercertificate.org). There is no separate contributor
agreement.

The sign-off is a person's certification. When you write with an AI tool, you sign off, and an
agent never signs off on anyone's behalf ([AGENTS.md](AGENTS.md#commits-and-pull-requests)).

## Pull requests

- One subject per pull request.
- Fill in the template: what changes, which pages, which claims are affected and how they are
  classified, and which references were added.
- Every pull request needs an approval from a curator of the pages it changes or a moderator of
  their part; the `moderation` check says who, requests their review and passes once one of them
  approves. Without one, a maintainer reviews. Typo and formatting fixes need a light review.
- A translation is approved by a maintainer of its language instead
  ([docs/translating.md](docs/translating.md#pull-requests)).
- Roles, the yearly review of living reviews, conflicts of interest and how to become a moderator or
  curator are in [GOVERNANCE.md](GOVERNANCE.md).

## Credit

- Chapter contributors are listed in the chapter's front matter (`contributors:`) and in the
  book's acknowledgments.
- Paper authorship follows academic practice: an author made a substantial contribution to the
  content and approved the final version. Everyone else who helped is acknowledged in the paper.
- Translators are credited in the [Moderators and Curators](https://the-alan-machine.github.io/the-alan-machine/appendices/people.html)
  appendix: the language's maintainers and whoever reviewed a translation.

## Writing with AI assistance

You may use AI tools to help you write. You are responsible for everything you submit, and above
all for every reference: check each one against its source. Invented references are the most
common failure of machine-generated text, and the most damaging one for a scientific book.

The fastest way to get a correct BibTeX entry is from the DOI:

```bash
curl -sL -H "Accept: application/x-bibtex" https://doi.org/<DOI>
```

The repository includes instructions for coding agents in [AGENTS.md](AGENTS.md) and skills in
[`skills/`](skills/): `write-chapter`, `classify-claims`, `verify-references`, `review-pr` and
`translate-page`.
Claude Code picks them up automatically; other agents can read them as plain Markdown. To check
every DOI entry in `references.bib` against Crossref:

```bash
python3 skills/verify-references/scripts/verify_bib.py
```

## Licenses

By contributing, you agree that your text and figures are licensed under
[CC BY 4.0](LICENSE) and your code under [MIT](LICENSE-CODE).
