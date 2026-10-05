---
name: verify-references
description: Check the citations and BibTeX entries of The Alan Machine against their sources, and add new references correctly from the DOI. Use when adding or reviewing references, when a page cites something new, when references.bib changes, or before a pull request with scientific claims.
---

# Verify references

Invented or garbled references are the most common failure of machine-assisted writing and the most
damaging one for a scientific book. Nothing in this skill may be done from memory.

## Add a reference

1. Find the DOI on the publisher's page or in Crossref (https://search.crossref.org).
2. Fetch the entry:
   ```bash
   curl -sL -H "Accept: application/x-bibtex" https://doi.org/<DOI>
   ```
   Crossref may return the entry with a leading space; remove it.
3. Rename the key to `authorYEARfirstword`, using the first author's family name, the year in the
   entry and the first word of the title that is not an article, all lowercase.
4. Append it to `references.bib`. Books without a DOI: take the data from the publisher's page or
   the ISBN record, and include the ISBN.

## Check existing entries

```bash
python3 skills/verify-references/scripts/verify_bib.py            # every entry with a DOI
python3 skills/verify-references/scripts/verify_bib.py key1 key2  # only these keys
```

The script compares title, year and first author with Crossref and exits with 1 on any mismatch.
It also asks Crossref for notices that update each DOI
(`https://api.crossref.org/works?filter=updates:<DOI>`). Crossref has carried the Retraction Watch
database since September 2023, so the notices include retractions the publisher did not register.
Each notice prints its type, its own DOI, its date and its source:

- `RETRACTED`: a retraction, withdrawal or removal. A failure.
- `UPDATED`: any other notice, such as a correction, an erratum or an expression of concern. A
  warning.

A network error on that request prints `ERROR`, as for the metadata.

## When a reference is retracted

A retracted work cannot support a claim as established. Read the notice (`https://doi.org/<notice
DOI>`) and then:

1. If the page cites it for the claim it made, remove the citation and find a source that is not
   retracted. If there is none, reclassify the claim with `classify-claims`.
2. If the page cites it as a retracted work (to discuss the retraction itself), keep it, say in the
   sentence that it was retracted and cite the notice too.

For an `UPDATED` notice, read it and check that the cited sentence still holds. A correction to
another part of the paper changes nothing; a correction to the number or result cited changes the
sentence; an expression of concern makes the claim at most Reported.
`python3 tools/check.py` separately checks that every key cited in the book exists.

## Check that the source says what the sentence says

For each citation in new or changed text:

1. Read the abstract (Crossref, the publisher or arXiv).
2. If the abstract does not support the sentence, ask the contributor for the section or page that
   does, and note it in the pull request.
3. If no part of the source supports it, the citation is wrong. Remove it and reclassify the claim
   with `classify-claims`.

## Report

For each reference: key, DOI, verified metadata (yes or no), supports the sentence (yes, no or
unknown, and why). Never mark "yes" for a source you have not read.
