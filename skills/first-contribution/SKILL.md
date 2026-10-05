---
name: first-contribution
description: Guide someone who has never contributed to The Alan Machine from picking a small task to an open pull request, following CONTRIBUTING.md. Use when a newcomer asks how to start contributing, asks for a good first task, or wants help with their first pull request.
---

# First contribution

The person you are helping has never contributed to the book. Keep the task small, follow
[CONTRIBUTING.md](../../CONTRIBUTING.md) step by step, and end with an open pull request.

## 1. Pick a small task

```bash
python3 skills/first-contribution/scripts/good_first.py              # pt, five of each
python3 skills/first-contribution/scripts/good_first.py --lang es --limit 10
python3 skills/first-contribution/scripts/good_first.py --json
```

The script prints two lists:

- **References without a source link:** entries of `references.bib` with no `doi`, `url`, `isbn`
  or `eprint`. Finding the DOI or ISBN of one and adding it is a good first task; follow
  [`verify-references`](../verify-references/SKILL.md).
- **Pages to translate:** pages with no translation, or a stale one, in the language of `--lang`.
  Only offer these to someone who reads that language; follow
  [`translate-page`](../translate-page/SKILL.md).

When both lists are empty, the script prints the link to the open issues labelled
`good first issue`; offer one of those, or an erratum the person found while reading.

Let the person choose one item. If they want to write or fix text instead, and the change makes or
moves a scientific claim, follow [`classify-claims`](../classify-claims/SKILL.md) as well.

## 2. Follow CONTRIBUTING.md to the pull request

1. Fork the repository and clone the fork, as in CONTRIBUTING.md.
2. Create one branch for the subject, named `type/short-description`, with a type from the list in
   CONTRIBUTING.md (for example `fix/landauer-doi`).
3. Make the change, and nothing else in the same branch.
4. Run the checks and fix everything they report:

   ```bash
   python3 tools/check.py
   ```

5. Commit with the sign-off every commit needs:

   ```bash
   git commit -s -m "fix(references): add DOI to landauer1961"
   ```

6. Push the branch and open the pull request from GitHub, with a title in the convention of
   CONTRIBUTING.md. If a reviewer asks for changes, commit again with `git commit -s` and push.

## 3. Which skill for which task

| Task | Skill |
|---|---|
| A reference, a DOI, a new citation | [`verify-references`](../verify-references/SKILL.md) |
| Text that states or changes a scientific claim | [`classify-claims`](../classify-claims/SKILL.md) |
| A translation | [`translate-page`](../translate-page/SKILL.md) |
