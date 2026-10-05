"""Check the sources before rendering. Run it before every pull request; CI runs it too.

    python3 tools/check.py

Errors (exit 1): generated pages out of date or invalid data, citation keys missing from
references.bib or breaking the authorYEARfirstword convention, cross-references to labels that do
not exist, invalid front matter, pages missing from _quarto.yml, a governance.toml that does not
match the parts of the book, people named by something other than a GitHub handle.
Warnings (exit 0): Building Alan living reviews past their review date.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import generate  # noqa: E402

CROSSREF_PREFIXES = ("sec", "eq", "fig", "tbl", "lst", "thm", "lem", "cor", "prp", "def", "exm", "exr")
CITATION = re.compile(r"(?<![\w@./])@([A-Za-z][\w:.#$%&+?<>~/-]*[\w])")
LABEL_DEFINITION = re.compile(r"\{[^}]*#((?:%s)-[\w-]+)[^}]*\}" % "|".join(CROSSREF_PREFIXES))
CELL_LABEL = re.compile(r"^#\|\s*label:\s*((?:fig|tbl)-[\w-]+)", re.M)
PAGE_GLOBS = ("chapters/*/index.qmd", "interludes/*/index.qmd", "building-alan/*/index.qmd", "papers/*/index.qmd")


def check_people(where: str, field_name: str, value, errors: list[str]):
    """A list of GitHub handles, without @, each once."""
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{where}: {field_name} must be a list of GitHub handles, like [name, other]")
        return
    seen = set()
    for person in value:
        if not isinstance(person, str) or not book.GITHUB_HANDLE.match(person):
            errors.append(f"{where}: {field_name}: {person!r} is not a GitHub handle (write it without @)")
        elif person.lower() in seen:
            errors.append(f"{where}: {field_name}: {person!r} is listed twice")
        else:
            seen.add(person.lower())


def check_governance(parts: list[str], errors: list[str]):
    where = "governance.toml"
    if not book.GOVERNANCE_TOML.exists():
        errors.append(f"{where} is missing; it lists the maintainers and moderators (GOVERNANCE.md)")
        return
    try:
        data = book.governance()
    except tomllib.TOMLDecodeError as error:
        errors.append(f"{where}: not valid TOML: {error}")
        return
    for key in set(data) - {"maintainers", "part"}:
        errors.append(f"{where}: unknown field {key!r}")
    check_people(where, "maintainers", data.get("maintainers", []), errors)
    if not data.get("maintainers"):
        errors.append(f"{where}: needs at least one maintainer")
    titles = []
    for entry in data.get("part", []):
        title = entry.get("title") if isinstance(entry, dict) else None
        if not isinstance(title, str):
            errors.append(f"{where}: every [[part]] needs a title")
            continue
        for key in set(entry) - {"title", "moderators"}:
            errors.append(f"{where} [{title}]: unknown field {key!r}")
        if title in titles:
            errors.append(f"{where}: part {title!r} is listed twice")
        elif title not in parts:
            errors.append(f"{where}: part {title!r} is not a part in _quarto.yml")
        titles.append(title)
        check_people(f"{where} [{title}]", "moderators", entry.get("moderators", []), errors)
    for title in parts:
        if title not in titles:
            errors.append(f"{where}: the part {title!r} of _quarto.yml has no [[part]] entry")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    files, data_errors = generate.outputs()
    errors += data_errors
    for relative_path, content in files.items():
        path = book.ROOT / relative_path
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            errors.append(f"{relative_path} is out of date; run python3 tools/generate.py")

    pages = book.pages()
    check_governance(list(dict.fromkeys(page.part for page in pages if page.part)), errors)
    listed = {page.path for page in pages}
    for pattern in PAGE_GLOBS:
        for path in sorted(book.ROOT.glob(pattern)):
            relative_path = path.relative_to(book.ROOT).as_posix()
            if relative_path not in listed:
                errors.append(f"{relative_path} is not listed in _quarto.yml")
    for page in pages:
        if not (book.ROOT / page.path).exists():
            errors.append(f"_quarto.yml lists {page.path}, which does not exist")

    keys = book.bib_keys()
    for key, year in book.bib_entries().items():
        match = re.fullmatch(r"[a-z]+(\d{4})[a-z]+", key)
        if not match:
            errors.append(f"references.bib: key {key!r} does not follow authorYEARfirstword")
        elif year and match.group(1) != year:
            errors.append(f"references.bib: key {key!r} has year {match.group(1)}, the entry says {year}")
    labels: dict[str, str] = {}
    for page in pages:
        text = book.strip_code_and_comments(page.body)
        for label in LABEL_DEFINITION.findall(text) + CELL_LABEL.findall(page.body):
            if label in labels:
                errors.append(f"{page.path}: label {label} is already defined in {labels[label]}")
            labels[label] = page.path

    today = dt.date.today()
    for page in pages:
        text = book.strip_code_and_comments(page.body)
        for name in CITATION.findall(text):
            prefix = name.split("-", 1)[0]
            if "-" in name and prefix in CROSSREF_PREFIXES:
                if name not in labels:
                    errors.append(f"{page.path}: cross-reference @{name} points to no label")
            elif name not in keys:
                errors.append(f"{page.path}: citation @{name} is not in references.bib")

        check_people(page.path, "curators", page.meta.get("curators"), errors)
        if page.meta.get("reviewed_by") is not None:
            if page.kind != "living-review":
                errors.append(f"{page.path}: only living reviews have reviewed_by")
            elif not book.GITHUB_HANDLE.match(str(page.meta["reviewed_by"])):
                errors.append(f"{page.path}: reviewed_by {page.meta['reviewed_by']!r} is not a GitHub handle (write it without @)")

        allowed = book.STATUS_BY_KIND.get(page.kind)
        if allowed is not None:
            status = page.meta.get("status")
            if status not in allowed:
                errors.append(f"{page.path}: status {status!r} is not one of {', '.join(sorted(allowed))}")
            if page.label != f"sec-{page.slug}" and page.kind != "paper":
                errors.append(f"{page.path}: the title needs the label {{#sec-{page.slug}}}")

        if page.kind == "living-review":
            technology = page.meta.get("technology")
            if technology and not (book.ROOT / "data" / "technologies" / f"{technology}.toml").exists():
                errors.append(f"{page.path}: technology {technology!r} has no data/technologies/{technology}.toml")
            last = page.meta.get("last_reviewed")
            if last:
                try:
                    due = dt.date.fromisoformat(generate.review_due(last))
                except ValueError:
                    errors.append(f"{page.path}: last_reviewed {last!r} is not YYYY-MM-DD")
                else:
                    if due < today:
                        curators = page.meta.get("curators") if isinstance(page.meta.get("curators"), list) else []
                        who = "; curators: " + ", ".join(f"@{c}" for c in curators) if curators else ""
                        warnings.append(f"{page.path}: review was due on {due.isoformat()}{who}")
            elif page.meta.get("status") not in (None, "proposed"):
                warnings.append(f"{page.path}: has content but no last_reviewed date")

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if not errors:
        print(f"ok: {len(pages)} pages, {len(keys)} references, {len(labels)} labels")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
