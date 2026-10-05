# 0010. Agents, skills and an MCP server

- Date: 2026-10-04
- Status: accepted

## Context

Two kinds of AI use matter to the project. Contributors use coding agents to draft, check and review
text, and those agents need the project's rules. Readers and researchers ask models about the book,
and those models need structured access that keeps the kind of each claim.

## Decision

1. **`AGENTS.md`** is the instruction file for any coding agent. `CLAUDE.md` imports it, so there is
   one source.
2. **Contributor skills** live in `skills/<name>/SKILL.md`, in the Agent Skills format, and are
   exposed to Claude Code through symbolic links in `.claude/skills/`. The first four:
   `write-chapter`, `classify-claims`, `verify-references` and `review-pr`. Planned:
   `write-paper`, `write-dossier` and `estimate-requirements`.
3. **Reader skills** (planned): `explain-alan`, `study-path`, `research-brief` and `debate`,
   distributed with the MCP server as a Claude Code plugin.
4. **MCP server** (planned), read-only, in a separate repository named `alan-tools`. It serves the
   published export, not the repository, so it never shows unreviewed text and a reader needs no
   clone. Planned tools: `search`, `read_section`, `claims` (filtered by kind), `technology`,
   `limits` (the Landauer, Margolus-Levitin and Bekenstein bounds for given parameters, computed by
   the `alan` library), `open_questions`, `concept`, `notation`, `constant` and `reference`. Every
   response carries the page URL, the status, the kind of claim and the license.
5. **Why a separate repository** for the server and the library: different license (MIT), release
   cycle and dependencies. The book repository stays buildable with Quarto and Python's standard
   library alone.

## Consequences

- The skills follow STYLE.md and CONTRIBUTING.md. A pull request that changes a rule updates the
  skills that apply it; the `review-pr` skill checks for that.
- On Windows, the links in `.claude/skills/` need `git config core.symlinks true`; without it, the
  skills can still be read in `skills/`.
- The MCP server depends on the export staying stable, which is why the JSON export will carry a
  schema version (decision 0009).
