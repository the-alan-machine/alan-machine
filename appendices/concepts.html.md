---
title: "Concepts"
url: "https://the-alan-machine.github.io/alan-machine/appendices/concepts.html"
kind: "appendix"
source: "https://github.com/the-alan-machine/alan-machine/blob/main/appendices/concepts.qmd"
license: "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
---

# Concepts


Every technical term the book uses, in plain language. Each entry lists the pages that use it.

## Arrow of time

The difference between past and future that we observe in everyday life: eggs break but do not unbreak, and we remember yesterday but not tomorrow. It stands out because the fundamental laws of physics barely distinguish between the two directions of time.

**Related:** [Entropy](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-entropy), [Second law of thermodynamics](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-second-law)

## Bit

The basic unit of information: the answer to one yes-or-no question. A memory that can hold one of two states, such as 0 or 1, stores one bit.

**Related:** [Landauer's principle](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-landauer-principle), [Entropy](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-entropy)

## Entropy

A measure of how many microscopic arrangements of a system are compatible with what we observe at large scale. The more ways the parts can be arranged without changing how the whole looks, the higher the entropy.

**Related:** [Second law of thermodynamics](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-second-law), [Arrow of time](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-arrow-of-time), [Bit](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-bit)

## Landauer's principle

Erasing one bit of information in surroundings at temperature $T$ releases at least $k_B T \ln 2$ of heat. Forgetting has a minimum physical cost. The bound was proposed by Rolf Landauer in 1961 and confirmed experimentally in 2012.

**Related:** [Bit](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-bit), [Reversible computing](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-reversible-computing), [Maxwell's demon](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-maxwells-demon)

**References:** [@landauer1961irreversibility; @berut2012experimental]

## Maxwell's demon

A thought experiment devised by James Clerk Maxwell in 1867: a tiny being opens and closes a door between two boxes of gas, letting fast molecules go one way and slow ones the other. It seems to lower entropy for free. The accepted resolution is that the demon must record what it sees, and erasing that record eventually pays the entropy back.

**Related:** [Second law of thermodynamics](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-second-law), [Landauer's principle](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-landauer-principle)

## Reversible computing

Computing without erasing information, so that every step can be run backward. Because nothing is erased, Landauer's principle sets no minimum energy cost per operation: in principle, a reversible computer running slowly enough can dissipate as little energy as we like.

**Related:** [Landauer's principle](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-landauer-principle), [Bit](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-bit)

**References:** [@bennett1973logical]

## Second law of thermodynamics

In an isolated system, entropy does not decrease over time. It is a statistical law: a decrease is not forbidden, only overwhelmingly unlikely for systems with many parts.

**Related:** [Entropy](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-entropy), [Arrow of time](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-arrow-of-time), [Maxwell's demon](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-maxwells-demon)

## Turing machine

An abstract model of computation introduced by Alan Turing in 1936: a machine that reads and writes symbols on an unlimited tape, following a finite table of rules. Anything a modern computer can compute, a Turing machine can compute too, given enough time and tape.

**Related:** [Bit](https://the-alan-machine.github.io/alan-machine/appendices/concepts.html#sec-concept-bit)

**References:** [@turing1937computable]
