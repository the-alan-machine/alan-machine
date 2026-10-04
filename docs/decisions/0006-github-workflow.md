# 0006. GitHub workflow

- Date: 2026-10-04
- Status: accepted

## Decision

- **Hosting:** the GitHub organization [`the-alan-machine`](https://github.com/the-alan-machine)
  holds the repository `alan-machine`, so the project can have several maintainers without a
  transfer. The organization matches the book title, following `the-turing-way`, and avoids
  confusion with `alanmachine`, an unrelated account that already existed.
- **Publishing:** GitHub Pages publishes the HTML edition on every merge to `main`. Releases
  (`v0.1`, `v0.2`, ...) attach the PDF edition.
- **Branches:** `main` is protected and changes only through pull requests. Branches are named
  `type/short-description`.
- **Merging:** squash merge. The pull request title becomes the commit and follows
  `type(scope): summary` (see CONTRIBUTING.md).
- **Issues:** four forms (erratum, scientific challenge, content proposal, reference suggestion).
  Blank issues are disabled, so every issue arrives with a location and references.
- **Discussions:** open ideas that are not proposals yet.
- **Labels:** `erratum`, `scientific-review`, `proposal`, `references`, `figures`, `build`,
  `good first issue`, plus `ch:<slug>` and `paper:<slug>`.
- **Planning:** a GitHub Projects board with the status of each chapter and paper (proposed,
  drafting, scientific review, done), and one milestone per part of the book.
- **No wiki.** A GitHub wiki is a separate repository, edited without pull requests or review, and
  drifts away from the book. Everything that would go there lives in the repository: the style
  guide in `STYLE.md`, the glossary and notation as appendices of the book, and decisions here.

## Consequences

- The repository lives at `https://github.com/the-alan-machine/alan-machine` and the book at
  `https://the-alan-machine.github.io/alan-machine/`.
- Other repositories, such as simulations, can live next to it in the same organization.
