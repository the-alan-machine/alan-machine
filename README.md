# The Alan Machine

An open-source book about a hypothetical supercomputer named Alan, and what theoretical physics
says about reversing entropy and what that would mean for time.

Read it online: https://the-alan-machine.github.io/alan-machine/

## Premise

Alan is a thought-experiment device. It pushes known physics to its limits so we can ask what
theoretical physics allows, forbids or leaves open about reversing entropy, and what such a
reversal would do to time.

Alan is not a prediction of real technology. Its job is to show where the reasoning holds and
where it breaks.

## Two registers

The book is written for the general public, in plain and conversational English. When a subject
deserves full rigor, it gets a companion scientific paper inside the same project, and the chapter
links to it.

| Folder | Register | For |
|---|---|---|
| `chapters/` | Popular | Anyone curious. Few equations, optional "Going deeper" boxes. |
| `papers/` | Scientific | Readers who want the full argument. Each paper has its own authors, abstract and references, and can be cited on its own. |

A contributor can write in either register, or in both.

Each part ends with a short **interlude** on a philosophical question the part raises, and a living
series, **Building Alan**, follows the main text.

## Contents

- **Part I. The Machine and the Question**: Meet Alan; What Entropy Is; The Arrow of Time.
  *Interlude: Does Time Flow?*
- **Part II. Information Is Physical**: Maxwell's Demon and the Szilard Engine; Landauer's
  Principle; Reversible Computing; Can a Mind Beat the Second Law? *Interlude: Three Demons*
- **Part III. The Limits of the Machine**: How Fast Can It Compute; How Much Can It Hold; Is Alan a
  Quantum Computer?; Laplace's Demon; Black Holes and Information. *Interlude: Are We Inside an
  Alan?*
- **Part IV. Reversing Entropy**: Local Reversal; Life: The Original Local Reversal; Fluctuations
  and Recurrence; Global Reversal. *Interlude: Would You Remember?*
- **Part V. The Impact on Time**: What Time Is; Would Time Run Backward; Closed Timelike Curves;
  The End of the Universe. *Interlude: Can Alan Think?*
- **Epilogue**: What Alan Cannot Do

## Building Alan

The chapters ask what physics allows; Building Alan asks how close today's technology comes. Each
dossier takes one technology or bottleneck (CMOS, moving data, removing heat, reversible and
superconducting logic, quantum hardware, thermodynamic, neuromorphic and optical computing, the
energy of a language model token) and measures it against the same physical limits, with every
number dated and sourced. The dossiers are reviewed every year, so they stay useful to people who
design processors, AI hardware and data centers.

Its sister project, [Escape Velocity](https://scape-velocity.github.io/escape-velocity/), applies
the same method beyond computing: an atlas of what each technology still needs to reach maturity,
from fusion to medicine, with the dependencies between them.

## Approach

Every statement in the book is one of four kinds, and the reader can always tell which:

- **Established**: accepted physics, backed by references.
- **Extrapolation**: follows from established physics under assumptions that are stated explicitly.
- **Speculation**: conceivable, but not supported by current evidence.
- **Philosophy**: a question physics informs but cannot settle, with at least two positions.

## For AI models and tools

The book is written to be read by people and by machines.

- https://the-alan-machine.github.io/alan-machine/llms.txt is an index of the book for language
  models, with the reading rules.
- https://the-alan-machine.github.io/alan-machine/llms-full.txt is the whole book in one Markdown
  file.
- Every page has a Markdown version at the same address plus `.md`, for example
  `chapters/landauer/index.html.md`.
- The structured facts (concepts, notation, constants and technology metrics) are in [`data/`](data/).

Models, assistants and tools may use the text under [CC BY 4.0](LICENSE): cite the page URL and keep
the kind of each claim. An extrapolation quoted as established physics is a misquotation. A
read-only MCP server is planned (see [decision 0010](docs/decisions/0010-agents-skills-and-mcp.md)).

Contributors who use coding agents will find the project's instructions in [AGENTS.md](AGENTS.md)
and skills in [`skills/`](skills/).

## The name

The machine is named after Alan Turing, whose 1936 paper defined the machine every computer
descends from, and after Alan Ricardo, the author's brother.

## Building the book

The book is a [Quarto](https://quarto.org) project. The build tools in `tools/` need Python 3.11 or
later and nothing else.

```bash
quarto preview
```

`quarto render` writes the HTML and PDF editions to `_book/`. Before a pull request, run
`python3 tools/check.py`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [STYLE.md](STYLE.md). The reasons behind each project
decision are in [docs/decisions/](docs/decisions/).

## License

The text and figures are licensed under [CC BY 4.0](LICENSE). The code is licensed under
[MIT](LICENSE-CODE).

## Citing

See [CITATION.cff](CITATION.cff).
