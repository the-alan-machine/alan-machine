# Style Guide

## Registers

### Chapters: popular

- Write for a curious reader with no physics background.
- Use conversational English. "We" and "you" are welcome. Prefer short sentences.
- Define every technical term the first time it appears, and link that first use to its entry in
  the Concepts appendix: `[entropy](../../appendices/concepts.qmd#sec-concept-entropy)`. If the
  term has no entry yet, add it to [`data/concepts.toml`](data/concepts.toml).
- Keep equations out of the running text. Stephen Hawking's editor warned him that every equation
  would halve the book's readership; treat that as a budget. An equation that must appear gets a
  sentence that says the same thing in words. Anything more goes in a "Going deeper" box or in a
  paper.
- An analogy is not an argument. Say when you are using one, and say where it breaks.
- Simplify, never distort. A chapter may leave details out, but it may not say anything its
  references or its paper contradict.

### Papers: scientific

- Standard scientific prose: precise, complete, with every assumption stated.
- Full derivations, or a citation to where they can be found.
- A one-paragraph abstract.
- The paper must make sense without the book.

### Interludes: philosophy

- An interlude takes up one question that physics informs but cannot settle. It is short: 1,500 to
  3,000 words.
- Present at least two positions, each with its best argument, before saying which one the evidence
  favors, if any.
- Cite the philosophers: primary works, or reviewed reference works such as the Stanford
  Encyclopedia of Philosophy.
- An interlude does not introduce physics that later chapters depend on.

### Living reviews: dated

- A Building Alan living review describes the state of a technology, so it is written to be updated.
- Every number has a unit, the date it refers to and a source. Put it in
  `data/technologies/<id>.toml`, and write it in the text as "about 1 fJ per operation in 2025
  [@source]".
- Measure the technology against the same yardsticks every time: the Landauer bound at the
  operating temperature, the Margolus-Levitin bound, the Bekenstein bound, and the energy at the
  wall plug, with cooling and power delivery included.
- A vendor's figure or a preprint's is Reported ("the manufacturer reports ...") until it is
  peer-reviewed or independently measured. See [Classifying claims](#classifying-claims).
- When you review a living review, update `last_reviewed` in its front matter, even if nothing
  changed.

## Classifying claims

The same rule applies to every register.

| Kind | How it appears |
|---|---|
| Established | Running text, with a citation to a peer-reviewed paper or a standard textbook |
| Reported | Running text that names the source ("a 2025 preprint reports"), in a span of class `reported`, with a citation |
| Extrapolation | A warning callout titled "Extrapolation", stating its assumptions |
| Speculation | An important callout titled "Speculation" |
| Philosophy | A caution callout titled "Philosophy", with at least two positions |

Every classified callout carries its class as well as its title, so that tools and AI models can
tell the kinds apart. A translation keeps the class and takes the title its language gives the kind
in `i18n/<lang>/strings.toml` ([docs/translating.md](docs/translating.md)):

```markdown
::: {.callout-warning .extrapolation title="Extrapolation"}
If the machine can be kept at 1 K, then ...
:::

::: {.callout-important .speculation title="Speculation"}
Nothing we know rules out ...
:::

::: {.callout-caution .philosophy title="Philosophy"}
Some philosophers hold that time really passes ...; others answer that ...
:::
```

A reported claim rests on a source that does not establish it yet: a preprint, a figure from a
company or the press, or a talk. It stays in running text, because the numbers of a living review
are often this new, and it says so in words. The span lets tools and AI models tell it apart:

```markdown
[A 2025 preprint reports about 1 fJ per operation at 4 K [@source].]{.reported}
```

It becomes established once the work is peer-reviewed or independently measured.

Narrative, analogies and questions are not claims and need no label. Optional math goes in a
collapsed box:

```markdown
::: {.callout-note title="Going deeper" collapse="true"}
...
:::
```

## Self-contained sections

The book is read by people who jump to one section, and by AI models that read sections out of
context. Write every section so that it makes sense alone.

- Name the subject instead of pointing back: "Landauer's bound" rather than "the bound above".
- Avoid "as we saw" and "as mentioned earlier". Link instead: "Landauer's principle
  (@sec-landauer) says ...".
- Link the first use of each concept in every chapter, not only in the first chapter that uses it.
- One idea per section. A heading says what the section establishes, not just its topic.

## Alan

- In running text the machine is "Alan". Use "the Alan Machine" when introducing it or in formal
  contexts.
- Alan is a machine: refer to it as "it".
- Alan obeys physics. When a question needs Alan to do something physics forbids, say so. That is a
  result, not a plot hole.

## Language and numbers

- American English spelling.
- SI units throughout.
- Scientific notation for very large or very small quantities: $6.626 \times 10^{-34}$ J s.

## Math and notation

- LaTeX math: `$...$` inline and `$$...$$` for display.
- Label the display equations you refer to: `$$ E = k_B T \ln 2 $$ {#eq-landauer-bound}`.
- Every symbol is listed in [`data/notation.toml`](data/notation.toml) with its meaning and unit,
  which generates the Notation appendix. Add it there before you use it. A symbol keeps the same
  meaning across the whole book.
- Constants come from the 2019 SI or CODATA and are listed in
  [`data/constants.toml`](data/constants.toml), which generates the Constants appendix.

## Cross-references

- Use labels, never numbers: `@sec-landauer`, `@eq-landauer-bound`, `@fig-spin-echo`,
  `@tbl-speed-limits`. Chapters move; labels stay.
- A label is a prefix (`sec`, `eq`, `fig`, `tbl`) plus the chapter slug or a short name. The title
  of every chapter, interlude and living review carries the label `sec-<slug>`.
- Concepts are labeled `sec-concept-<id>`.

## Citations

- `[@landauer1961irreversibility]` in parentheses, or `@landauer1961irreversibility` as part of the
  sentence ("@landauer1961irreversibility showed that ...").
- Keys follow `authorYEARfirstword`, with the year that appears in the entry.
- Entries come from the DOI metadata (see [CONTRIBUTING](CONTRIBUTING.md#writing-with-ai-assistance)),
  never from memory.
- Prefer peer-reviewed papers and standard textbooks. Preprints are allowed; a claim that rests on
  one is Reported. Popular articles belong only in "Further reading".

## Figures

- A figure lives in the chapter's `figures/` folder, or is generated by a code cell in the chapter.
- Every figure has a caption, a label and alt text.
- Colors must work for colorblind readers and in grayscale.
- The code that produces a figure is licensed under MIT; the figure itself is CC BY 4.0.
- The first chapter that needs code adds a `requirements.txt` with pinned versions. Code shared by
  several chapters goes in `src/`.

## File names

- Slugs are lowercase words joined by hyphens, with no numbers. The order of the chapters lives only
  in `_quarto.yml`.
- Slugs are unique across chapters, interludes, living reviews and papers.

## Generated files

Do not edit `appendices/concepts.qmd`, `appendices/notation.qmd`, `appendices/constants.qmd` or the
marked table in `building-alan/index.qmd`. They are generated from `data/` by
`python3 tools/generate.py`, which Quarto also runs before every render.
