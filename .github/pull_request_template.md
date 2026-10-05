## What changes

<!-- One subject per pull request. -->

## Where

Slugs of the chapters, interludes, living reviews or papers, or the data files:

## Claims affected

<!-- List the claims this pull request adds or changes, and classify each one as established,
reported, extrapolation, speculation or philosophy. Write "none" for typo and formatting fixes. -->

## References added

<!-- New entries in references.bib, by key. -->

Closes #

## Checklist

- [ ] The title follows `type(scope): summary` (see CONTRIBUTING.md).
- [ ] `python3 tools/check.py` passes and the book builds: `quarto render --to html`.
- [ ] Every new reference was checked against its source.
- [ ] Every new claim is classified, and every established claim has a citation.
- [ ] New terms are in `data/concepts.toml` and new symbols are in `data/notation.toml`.
- [ ] Every new number in a living review has a unit, a date and a source in `data/technologies/`.
- [ ] Every commit is signed off (`git commit -s`).
- [ ] A living review whose `last_reviewed` changes names its reviewer in `reviewed_by`, and nobody is added to `curators` or `governance.toml` without a maintainer (GOVERNANCE.md).
