---
title: "Concepts"
url: "https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html"
kind: "appendix"
source: "https://github.com/the-alan-machine/the-alan-machine/blob/main/appendices/concepts.qmd"
license: "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
---

# Concepts


Every technical term the book uses, in plain language. Each entry lists the pages that use it.

## Arrow of time

The difference between past and future that we observe in everyday life: eggs break but do not unbreak, and we remember yesterday but not tomorrow. It stands out because the fundamental laws of physics barely distinguish between the two directions of time.

**Related:** [Entropy](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-entropy), [Second law of thermodynamics](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-second-law)

## Bit

The unit of information. Learning which of two equally likely answers is the true one gives one bit; an answer that could be predicted gives less, and a certain one gives none. A memory that can hold one of two states, such as 0 or 1, can store one bit, and ten such memories ten bits. Claude Shannon set out the measure in 1948: the logarithm to base 2 of the number of equally likely possibilities.

**Related:** [Landauer's principle](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-landauer-principle), [Entropy](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-entropy)

**References:** [@shannon1948mathematical]

## Entropy

A measure of how many microscopic arrangements of a system (its microstates) are compatible with what we observe at large scale (its macrostate). The more ways the parts can be arranged without changing how the whole looks, the higher the entropy. It grows with the logarithm of that number: the entropy is $k_B$ times its natural logarithm, so doubling the number of arrangements adds $k_B \ln 2$, however large the system. Thermodynamics measures the same quantity through heat: heat taken in reversibly at temperature $T$, divided by $T$, is the change in entropy.

**Related:** [Second law of thermodynamics](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-second-law), [Arrow of time](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-arrow-of-time), [Bit](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-bit)

## Landauer's principle

Erasing one bit of information in surroundings at temperature $T$ releases at least $k_B T \ln 2$ of heat. Forgetting has a minimum physical cost. The bound was proposed by Rolf Landauer in 1961 and confirmed experimentally in 2012.

**Related:** [Bit](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-bit), [Reversible computing](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-reversible-computing), [Maxwell's demon](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-maxwells-demon)

**References:** [@landauer1961irreversibility; @berut2012experimental]

## Maxwell's demon

A thought experiment devised by James Clerk Maxwell in 1867: a tiny being opens and closes a door between two boxes of gas, letting fast molecules go one way and slow ones the other. It seems to lower entropy for free. The accepted resolution is that the demon must record what it sees, and erasing that record eventually pays the entropy back.

**Related:** [Second law of thermodynamics](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-second-law), [Landauer's principle](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-landauer-principle)

## Quantum speed limit

The shortest time in which a quantum system can evolve into a state fully distinguishable from the one it started in. Leonid Mandelstam and Igor Tamm bounded it by the spread of the system's energy; Norman Margolus and Lev Levitin, in 1998, by its average energy above the lowest possible: the time is at least $\pi\hbar / 2E$, with $E$ measured from the ground state. Each step of a computation has to reach a distinguishable state, so the limit caps how many steps per second a computer with a given energy can take.

**Related:** [Bit](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-bit), [Reversible computing](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-reversible-computing)

**References:** [@mandelstam1991uncertainty; @margolus1998maximum; @lloyd2000ultimate]

## Reversible computing

Computing without erasing information, so that every step can be run backward. Two meanings are kept apart. A computation is logically reversible when each state has only one possible predecessor, so the input can be recovered from the output; Charles Bennett showed in 1973 that a general-purpose computer can be made logically reversible at every step. It is thermodynamically reversible when it produces no entropy, a limit a real device approaches only by running ever more slowly. Logical reversibility removes the minimum cost that Landauer's principle sets on erasure; it does not by itself remove the rest of the dissipation.

**Related:** [Landauer's principle](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-landauer-principle), [Bit](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-bit)

**References:** [@bennett1973logical]

## Second law of thermodynamics

In an isolated system, entropy does not decrease over time. It is a statistical law: a decrease is not forbidden, only overwhelmingly unlikely for systems with many parts.

**Related:** [Entropy](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-entropy), [Arrow of time](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-arrow-of-time), [Maxwell's demon](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-maxwells-demon)

## Turing machine

An abstract model of computation introduced by Alan Turing in 1936: a machine that reads and writes symbols on an unlimited tape, following a finite table of rules. Anything a modern computer can compute, a Turing machine can compute too, given enough time and tape.

**Related:** [Bit](https://the-alan-machine.github.io/the-alan-machine/appendices/concepts.html#sec-concept-bit)

**References:** [@turing1937computable]
