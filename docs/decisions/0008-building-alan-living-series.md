# 0008. Building Alan, a living series

- Date: 2026-10-04
- Status: accepted

## Context

The chapters ask what physics allows. Engineers and researchers who design processors, memory, AI
hardware and data centers want a second answer: how far today's technology is from those limits,
and what would close the gap. The physics changes slowly; the state of the art changes every year.
A book that mixes both will either go stale or never be finished.

## Decision

A part named **Building Alan** holds one **dossier** per technology or bottleneck, in
`building-alan/<slug>/index.qmd`. Dossiers are living documents:

- Each dossier has `last_reviewed` in its front matter. A review is due 12 months later; the table
  in `building-alan/index.qmd` shows the due date and `tools/check.py` warns when it has passed.
- Every number has a unit, the date it refers to (`as_of`) and a source. The numbers live in
  `data/technologies/<id>.toml`, with the metrics defined in `data/metrics.toml`, so the book, the
  exports and future tools read the same values.
- Every dossier measures its technology against the same yardsticks: the Landauer bound at the
  operating temperature, the Margolus-Levitin bound, the Bekenstein bound, and the energy drawn at
  the wall plug, with cooling and power delivery included.
- A vendor's figure is reported as the vendor's until it is peer-reviewed or independently measured.
- Dossiers follow the same claim classification as the rest of the book.
- Dossiers are unnumbered, so the book's chapter numbers stay stable as dossiers come and go.

Each dossier has the same sections: what it is, how it computes, where it stands today, distance to
Alan's limits, what blocks it, what would change the picture, what it means for processors and AI,
and further reading.

The first dossiers: CMOS (the baseline), the cost of moving data, getting the heat out, adiabatic
and reversible logic, superconducting logic, quantum hardware, thermodynamic and probabilistic
computing, neuromorphic computing, optical computing, and the energy of a language model token.

## Alternatives considered

- **A separate repository or a wiki.** Rejected: the dossiers need the same review, references and
  classification as the book, and readers move between a limit (in a chapter) and how close we are
  to it (in a dossier).
- **Numbers only in the text.** Rejected: they could not be checked, reused or flagged as stale.

## Consequences

- The dossiers are the part of the book most likely to go stale. The review date makes that
  visible instead of hidden.
- Maintainers need a review cadence. An overdue review is a good first issue for a new contributor.
- The same data will feed the `alan` Python library and the MCP server (decision 0010).
