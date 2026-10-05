# 0013. Reported claims, and dossiers become living reviews

- Date: 2026-10-05
- Status: accepted; amends 0005 and supersedes the term "dossier" in 0008, 0010 and 0011

## Context

Decision 0005 sorts every claim into kinds, and decision 0007 added philosophy. Established covers
accepted physics backed by a peer-reviewed paper or a standard textbook. The Building Alan pages
(decision 0008) report numbers that are often newer than that: a preprint, a manufacturer's figure,
a result shown in a talk. The style guide asked for these to be "reported as the vendor's", but no
kind of claim held them, so a reader or a model could not tell them from established physics, and
an author had to choose between overstating them and leaving them out.

The Escape Velocity atlas, which shares its evidence policy with the book, already has a
`reported` class for the same sources (its decision 0006).

Decision 0008 called each Building Alan page a dossier. The genre already has a name in science: a
review that is updated as new results appear is a living review, as in *Living Reviews in
Relativity* and living systematic reviews in medicine.

## Decision

1. **A fifth kind of claim: Reported.** A claim that rests on a source that does not establish it
   yet, such as a preprint, a figure from a company or the press, or a talk. It stays in running
   text, names its source in words ("a 2025 preprint reports"), carries the citation and sits in a
   `[...]{.reported}` span. It becomes established once the work is peer-reviewed or independently
   measured.
2. **Established names its sources:** a peer-reviewed paper or a standard textbook.
3. **A dossier is a living review.** The page kind, the template, the issue form, the generated
   table and the guides use the new term. The skill decision 0010 planned as `write-dossier` will
   be `write-living-review`.

## Consequences

- The style guide, the agent guide, the skills, the issue and PR forms and the knowledge base export
  list five kinds of claim.
- No chapter or living review is written yet, so no claim had to be reclassified.
- Issues opened from the old form carry a "Dossier" field; the moderation check still reads it.
- Decisions 0005, 0008, 0010 and 0011 are not edited; read "dossier" in them as "living review".
