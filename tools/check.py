"""Check the sources before rendering. Run it before every pull request; CI runs it too.

    python3 tools/check.py

Errors (exit 1): generated pages out of date or invalid data, citation keys missing from
references.bib or breaking the authorYEARfirstword convention, cross-references to labels that do
not exist, invalid front matter, pages missing from _quarto.yml.
Warnings (exit 0): Building Alan dossiers past their review date.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import generate  # noqa: E402

CROSSREF_PREFIXES = ("sec", "eq", "fig", "tbl", "lst", "thm", "lem", "cor", "prp", "def", "exm", "exr")
CITATION = re.compile(r"(?<![\w@./])@([A-Za-z][\w:.#$%&+?<>~/-]*[\w])")
LABEL_DEFINITION = re.compile(r"\{[^}]*#((?:%s)-[\w-]+)[^}]*\}" % "|".join(CROSSREF_PREFIXES))
CELL_LABEL = re.compile(r"^#\|\s*label:\s*((?:fig|tbl)-[\w-]+)", re.M)
PAGE_GLOBS = ("chapters/*/index.qmd", "interludes/*/index.qmd", "building-alan/*/index.qmd", "papers/*/index.qmd")


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

        allowed = book.STATUS_BY_KIND.get(page.kind)
        if allowed is not None:
            status = page.meta.get("status")
            if status not in allowed:
                errors.append(f"{page.path}: status {status!r} is not one of {', '.join(sorted(allowed))}")
            if page.label != f"sec-{page.slug}" and page.kind != "paper":
                errors.append(f"{page.path}: the title needs the label {{#sec-{page.slug}}}")

        if page.kind == "dossier":
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
                        warnings.append(f"{page.path}: review was due on {due.isoformat()}")
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
