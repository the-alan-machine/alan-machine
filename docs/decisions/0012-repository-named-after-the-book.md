# 0012. The repository takes the book's name

- Date: 2026-10-05
- Status: accepted; supersedes the repository name in 0001 and the addresses in 0006

## Context

Decision 0001 named the repository after the machine, `alan-machine`, so that a change of title
would not change the URL. The organization, created later (decision 0006), took the title instead:
`the-alan-machine`. The repository read as half of the title, and so did the book's address.

## Decision

1. **The repository is `the-alan-machine/the-alan-machine`**, the same name as the organization and
   the title, as many projects do (`rust-lang/rust`, `vuejs/vue`).
2. **New addresses.** The repository is at https://github.com/the-alan-machine/the-alan-machine and
   the book at https://the-alan-machine.github.io/the-alan-machine/.

## Consequences

- GitHub redirects the old repository URLs, for the web and for Git. GitHub Pages does not: links to
  https://the-alan-machine.github.io/alan-machine/ stopped working on the day of the rename, a few
  days after the first publication.
- `_quarto.yml`, `CITATION.cff`, the README, the issue forms and the governance links use the new
  addresses, and so does the Escape Velocity atlas.
- If the title ever changes, the repository name follows it or keeps the old title; decision 0001's
  reason for naming it after the machine no longer holds.
