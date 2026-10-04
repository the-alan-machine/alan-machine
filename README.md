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

## Contents

- **Part I. The Machine and the Question**: Meet Alan; What Entropy Is; The Arrow of Time
- **Part II. Information Is Physical**: Maxwell's Demon and the Szilard Engine; Landauer's
  Principle; Reversible Computing
- **Part III. The Limits of the Machine**: How Fast Can It Compute; How Much Can It Hold; Black
  Holes and Information
- **Part IV. Reversing Entropy**: Local Reversal; Fluctuations and Recurrence; Global Reversal
- **Part V. The Impact on Time**: Would Time Run Backward; Closed Timelike Curves; The End of the
  Universe
- **Epilogue**: What Alan Cannot Do

## Approach

Every statement in the book is one of three kinds, and the reader can always tell which:

- **Established**: accepted physics, backed by references.
- **Extrapolation**: follows from established physics under assumptions that are stated explicitly.
- **Speculation**: conceivable, but not supported by current evidence.

## The name

The machine is named after Alan Turing, whose 1936 paper defined the machine every computer
descends from, and after Alan Ricardo, the author's brother.

## Building the book

The book is a [Quarto](https://quarto.org) project.

```bash
quarto preview
```

`quarto render` writes the HTML and PDF editions to `_book/`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [STYLE.md](STYLE.md). The reasons behind each project
decision are in [docs/decisions/](docs/decisions/).

## License

The text and figures are licensed under [CC BY 4.0](LICENSE). The code is licensed under
[MIT](LICENSE-CODE).

## Citing

See [CITATION.cff](CITATION.cff).
