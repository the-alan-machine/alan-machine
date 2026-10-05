# 0007. Philosophy, interludes and new chapters

- Date: 2026-10-04
- Status: accepted
- Amends: [0005](0005-claim-classification.md)

## Context

The premise raises questions that physics informs but cannot settle: whether time flows, whether a
machine can think, whether we could be inside a simulation, what the heat death means for us.
Leaving them out makes the book poorer. Leaving them unlabeled is worse: philosophy gets passed off
as physics, or physics gets dismissed as philosophy.

The first table of contents also left out three subjects that belong to the question: intelligence
as a physical process (today's AI included), quantum computing, and life as the everyday case of
local entropy reversal.

## Decision

**A fourth kind of claim.** A claim about meaning, value, mind or metaphysics, which physics
informs but cannot settle, is classified as **Philosophy**. It appears in a caution callout titled
"Philosophy", with the class `.philosophy`. A Philosophy callout presents at least two positions
with their best arguments and cites the philosophical literature: primary works, or reviewed
reference works such as the Stanford Encyclopedia of Philosophy.

| Kind | Meaning | How it appears |
|---|---|---|
| Established | Accepted physics | Running text, with a citation |
| Extrapolation | Follows from established physics under stated assumptions | "Extrapolation" callout, with the assumptions |
| Speculation | Conceivable, not supported by current evidence | "Speculation" callout |
| Philosophy | A question physics informs but cannot settle | "Philosophy" callout, with at least two positions |

**Interludes.** Each part ends with a short, unnumbered interlude that takes up one philosophical
question raised by the part. Interludes live in `interludes/<slug>/index.qmd`. They do not
introduce physics that later chapters depend on.

| After | Interlude |
|---|---|
| Part I | Does Time Flow? |
| Part II | Three Demons (Maxwell's, Laplace's and Loschmidt's) |
| Part III | Are We Inside an Alan? |
| Part IV | Would You Remember? |
| Part V | Can Alan Think? |

**New chapters.**

| Part | Chapter | Why |
|---|---|---|
| II | Can a Mind Beat the Second Law? | Intelligence is a physical process with a thermodynamic cost; an agent that predicts and acts is a Maxwell's demon with a model. Today's AI is a case we can measure. |
| III | Is Alan a Quantum Computer? | Quantum evolution is reversible and measurement is not; quantum computing sits at the center of the question. |
| III | Laplace's Demon | Reversing a system requires knowing it; this chapter asks how much Alan can know. |
| IV | Life: The Original Local Reversal | Living things are the proof that local entropy reversal happens every day. |
| V | What Time Is | The part about time's reversal needs, first, a clear account of what physics means by time. |

**Epilogue.** The epilogue closes with the human side of the question: Russell's despair at the
heat death against Dyson's eternal intelligence, Nietzsche's eternal return against Poincaré
recurrence, and Asimov's "The Last Question".

## Consequences

- The reader keeps the guarantee of decision 0005: they always know what kind of statement they are
  reading. There are now four kinds instead of three.
- Chapter numbers shift. Cross-references use labels, so nothing breaks.
- Interludes are unnumbered, so adding or removing one does not renumber the chapters.
