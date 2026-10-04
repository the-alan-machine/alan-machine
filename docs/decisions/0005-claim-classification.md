# 0005. Three kinds of claim

- Date: 2026-10-04
- Status: accepted

## Context

A book built on a hypothetical machine is only scientific if the reader can always separate what
physics says from what the book imagines.

## Decision

Every claim in the book, in both registers, is one of three kinds:

| Kind | Meaning | How it appears |
|---|---|---|
| Established | Accepted physics | Running text, with a citation |
| Extrapolation | Follows from established physics under stated assumptions | "Extrapolation" callout, with the assumptions |
| Speculation | Conceivable, not supported by current evidence | "Speculation" callout |

Narrative, analogies and questions are not claims and are not labeled.

## Consequences

- Only what leaves established physics is marked, so the reading flow is preserved and the
  boundary stays visible.
- A scientific challenge can dispute a claim or only its classification. Both are valid issues.
