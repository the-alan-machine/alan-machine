# 0004. Two registers: chapters and papers

- Date: 2026-10-04
- Status: accepted

## Context

The book is written for the general public, but some subjects deserve full scientific rigor. A
contributor should be able to write in either register: for example, a chapter in popular language
that links to a scientific paper within the same project.

## Decision

The book has three levels of depth:

1. **Running text of the chapters** (`chapters/`): plain, conversational English with few
   equations.
2. **"Going deeper" boxes** inside the chapters: collapsed by default, with the math for curious
   readers. The chapter makes sense without them.
3. **Papers** (`papers/<slug>/index.qmd`): full scientific treatment. Each paper has its own
   authors, abstract and references, and can be cited independently of the book.

- Papers live outside the chapter folders, because the relation is many-to-many: a chapter can
  lean on several papers, and a paper can support several chapters.
- The link is explicit in both directions: `papers:` in the chapter's front matter plus a "The
  science behind this chapter" box, and `chapters:` in the paper's front matter.
- A chapter can be published before its paper exists, as long as its established claims cite the
  literature.
- Paper authorship follows academic practice, which gives contributors who write the science a
  citable result of their own.

## Prior art

- Kip Thorne's popular book *The Science of Interstellar* (2014) came with a peer-reviewed
  companion paper on the film's black hole imagery (James, von Tunzelmann, Franklin and
  Thorne, *Classical and Quantum Gravity*, 2015, doi:10.1088/0264-9381/32/6/065001). It is the closest
  model: one piece of work, told to the public and argued to specialists.
- eLife publishes a plain-language digest with its research articles: the same pairing, written in
  the opposite direction.
- For the running text: Stephen Hawking's editor warned him that each equation would halve the
  readership of *A Brief History of Time*.

## Consequences

- Each paper should also get a standalone PDF and, at releases, a DOI. The CI for that comes with
  the first paper.
