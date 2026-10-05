# 0011. Moderators by part and a moderation check

- Date: 2026-10-05
- Status: accepted

## Context

Changes to scientific claims needed a review from a maintainer. With one maintainer, that person
reviews thermodynamics, quantum hardware, general relativity and philosophy alike, and the Building
Alan dossiers add a yearly review each. The book needs people who know a part to review its
changes, without giving them write access to the whole repository.

GitHub's CODEOWNERS was the obvious tool and does not fit. A code owner needs write access to the
repository. Ownership is decided by path only, while `references.bib` is one file shared by every
page, so its owner would review every reference. And a code owner's approval cannot be tied to a
field in the front matter, such as who reviewed a dossier.

## Decision

1. **Three roles.** Maintainers look after the repository. Moderators look after a part of the
   book, as listed in `_quarto.yml`. Both are listed in `governance.toml`, which has one entry per
   part. Curators look after single pages and are listed in `curators` in the page's front matter.
   People are named by GitHub handle; the lists change by pull request, approved by a maintainer.
2. **A moderation check instead of CODEOWNERS.** `.github/workflows/moderation.yml` runs
   `tools/moderation.py` on every pull request and on every review, and reports the commit status
   `moderation`, required on `main`. It passes when each changed file has an approving review from
   someone who covers it: a page or its folder from its curators or its part's moderators; a
   reference from those of any page that cites it; technology data from those of its dossier;
   everything else, and any change to a list of people, from a maintainer. The lists counted are
   those on `main`.
3. **Dossier reviews are tied to the review on GitHub.** When a dossier's `last_reviewed` changes,
   `reviewed_by` names someone who covers it, and that person approved the pull request's last
   commit or wrote it.
4. **The check runs main's code on the pull request's data.** It uses `pull_request_target` and
   `workflow_run`, so it can write a status and a comment on pull requests from forks. It never
   runs code from the pull request: the pages and `references.bib` it needs are fetched through the
   API and read as text.
5. **Roles without write access.** Moderators and curators get the triage role, so GitHub can
   request their reviews and they can triage issues. Only maintainers merge.
6. **Names in the book.** A generated appendix, Moderators and Curators, lists the maintainers, the
   moderators of each part and the curated pages; the dossier table shows each dossier's curators.
7. **Terms.** Dossiers keep their yearly review (decision 0008). Moderators and curators inactive
   for twelve months are removed and can return. Nobody approves or reviews their own work, their
   employer's products or a company they hold a stake in. The details are in
   [GOVERNANCE.md](../../GOVERNANCE.md).
8. **Issues are routed.** Issues opened from a form that name a page get a `part: <part>` label and
   a comment mentioning the part's moderators and the page's curators.

## Consequences

- A part can grow without its changes waiting on one person, and the check says who can approve.
- While a part has no moderators, its changes fall back to the maintainers, which is the current
  state.
- A pull request that adds a page needs a maintainer, because the page also needs its place in
  `_quarto.yml`.
- An approval survives later commits, except for a dossier review. The maintainer who merges still
  reads the final diff.
- GitHub requests reviews only from collaborators, so a moderator without the triage role is
  mentioned in the comment instead.
- Changing the rules means changing `tools/moderation.py` on `main`; a pull request cannot loosen the
  check it is judged by.
