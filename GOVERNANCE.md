# Governance

Who looks after each part of the book, who approves a pull request, and how to take a role. The
reasons are in [decision 0011](docs/decisions/0011-moderators-and-the-moderation-check.md).

## Roles

| Role | Looks after | Listed in |
|---|---|---|
| Maintainer | The whole repository: build, tools, data, decisions, workflows, the page order and the lists of people. Maintainers merge pull requests and handle conduct reports. | `maintainers` in [`governance.toml`](governance.toml) |
| Moderator | A part of the book, as listed in `_quarto.yml`: its pages, the references they cite and its issues. | `[[part]]` entries in [`governance.toml`](governance.toml) |
| Curator | Single pages: a chapter, an interlude, a living review or a paper. | `curators` in the page's front matter |

People are listed by GitHub handle, without @. The lists change only through pull requests. The
names appear in the book, in the [Moderators and Curators](https://the-alan-machine.github.io/the-alan-machine/appendices/people.html)
appendix, and the living review table shows each living review's curators.

Moderators and curators do not need write access. A maintainer gives them the triage role, so
GitHub can request their reviews and they can label and close issues. Their approval counts through
the `moderation` check, not through repository permissions.

Moderating a part is about the review of its pages: scientific accuracy, classification of claims
and references. It does not change authorship, which follows `contributors` and the paper's author
list ([CONTRIBUTING.md](CONTRIBUTING.md#credit)).

## Who approves what

The required check `moderation` ([`.github/workflows/moderation.yml`](.github/workflows/moderation.yml),
[`tools/moderation.py`](tools/moderation.py)) reads the files a pull request changes. It passes when
each change has an approving review from someone who covers it:

| Change | Approved by |
|---|---|
| A page, or any file in its folder, such as a figure | A curator of the page or a moderator of its part |
| A change to a page's `curators` | A maintainer, as well as the above |
| An entry in `references.bib` | A curator or moderator of any page that cites it, before or after the change |
| `data/technologies/<id>.toml` | A curator or moderator of the living review with `technology: <id>` |
| A new page, a page outside the parts, `_quarto.yml`, `data/` (other than technologies), tools, documentation, `governance.toml` | A maintainer |

- The curators and moderators counted are those on `main`, so nobody approves a change by adding
  themselves in the same pull request.
- The author's own approval does not count. If the author is the only person who covers a change, a
  maintainer approves it. If the author is the only maintainer and nobody else covers the change,
  the check passes; that happens only while the project has a single maintainer.
- An approval counts until the same person requests changes or the review is dismissed. It still
  counts after new commits, except for the yearly review of a living review (below). The maintainer
  who merges reads the final diff.
- Generated pages are not counted: the appendices that `tools/generate.py` writes and the living
  review table in `building-alan/index.qmd`. `tools/check.py` fails when they do not match their
  sources.

On each pull request the check requests reviews from the people who can approve and, while it is
not passing, keeps a comment with a table of each change and who can approve it. A review re-runs
the check.

Typo and formatting fixes go through the same check. A moderator or curator can approve them
quickly; the check counts who approved, not how long they looked.

## Reviewing a living review

A living review is reviewed every 12 months ([decision
0008](docs/decisions/0008-building-alan-living-series.md)): the reviewer looks for newer results,
updates the numbers and their sources, and checks that every claim is still classified correctly. To
record it, set `last_reviewed` to the date and `reviewed_by` to your handle. When `last_reviewed`
changes, the check requires that:

1. `reviewed_by` curates the living review or moderates Building Alan, or is a maintainer when
   nobody does;
2. `reviewed_by` approved the last commit of the pull request, or wrote the pull request.

`tools/check.py` warns when a review is past due and names the living review's curators.

Agents never hold a role, never set `reviewed_by` and never add anyone to a list
([AGENTS.md](AGENTS.md)).

## Curators

A curator keeps their pages accurate:

- reviews the pull requests on the page and on the references it cites;
- for a living review, does the yearly review above;
- answers the issues that name the page.

## Moderators

A moderator looks after a part of the book:

- reviews pull requests on its pages and on the references they cite;
- triages its issues. An issue opened from a form gets the label `part: <part>` for each part it
  names, and a comment mentioning their moderators and the curators of the pages
  ([`.github/workflows/triage.yml`](.github/workflows/triage.yml));
- finds curators for the pages that need one, starting with the living reviews.

## Becoming one

Open an issue, or a pull request that adds your handle to the list, with:

- the part or the pages;
- your background in them, with a link others can check;
- any conflict of interest (below).

A maintainer approves the change, which the check requires for any change to a list, and then
gives you the triage role.

## Conflicts of interest

Declare your affiliations when you take a role, and update them when they change. Do not approve a
change or review a living review about your own work, your employer's products or a company you hold
a stake in. Leave it to another curator or moderator, or to a maintainer, and say so in the review.
A paper's own authors do not approve the review of their paper; another curator, moderator or
maintainer does.

## Stepping down and inactivity

Anyone can step down by removing their handle in a pull request. A maintainer removes a moderator or
curator who has not reviewed anything in the repository for twelve months, in a pull request that
mentions them. They can come back the same way they joined.

## Conduct

The [code of conduct](CODE_OF_CONDUCT.md) applies to everyone. Reports go to the maintainers, not to
moderators. A maintainer can remove a role from someone who breaks the code of conduct or these
rules.
