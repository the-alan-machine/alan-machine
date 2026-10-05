#!/usr/bin/env python3
"""Small first tasks for a new contributor: references without a source link, and pages with no
translation or a stale one in a language. Standard library only."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))

import book  # noqa: E402
import i18n  # noqa: E402

# Fields can sit on their own line or after a comma on the entry's single line.
LINK_FIELDS = re.compile(r"(?<![\w-])(doi|url|isbn|eprint)\s*=\s*[{\"\w]", re.I)

GOOD_FIRST_ISSUES = f"{book.repo_url()}/issues?q=is%3Aopen+label%3A%22good+first+issue%22"


def references_without_link() -> list[str]:
    """Keys of references.bib entries with no doi, url, isbn or eprint (walked as book.bib_entries)."""
    text = (book.ROOT / "references.bib").read_text(encoding="utf-8")
    starts = [
        match
        for match in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", text, re.M)
        if match.group(1).lower() not in {"comment", "string", "preamble"}
    ]
    found = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        if not LINK_FIELDS.search(text[match.end() : end]):
            found.append(match.group(2))
    return found


def pages_to_translate(lang: str) -> list[dict]:
    return [
        {"page": item.path, "state": item.state}
        for item in i18n.page_translations(lang)
        if item.state in ("missing", "stale")
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", default="pt", help="language of the translations (default pt)")
    parser.add_argument("--limit", type=int, default=5, help="items per list (default 5)")
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    references = references_without_link()
    pages = pages_to_translate(args.lang)
    if args.json:
        print(json.dumps({
            "lang": args.lang,
            "references_without_link": {"total": len(references), "items": references[: args.limit]},
            "pages_to_translate": {"total": len(pages), "items": pages[: args.limit]},
            "good_first_issues": GOOD_FIRST_ISSUES,
        }, indent=2, ensure_ascii=False))
        return 0

    print(f"References without doi, url, isbn or eprint ({len(references)}):")
    for key in references[: args.limit]:
        print(f"  {key}")
    print(f"\nPages missing or stale in '{args.lang}' ({len(pages)}):")
    for item in pages[: args.limit]:
        print(f"  {item['state']:8} {item['page']}")
    if not references and not pages:
        print(f"\nNothing to pick from the repository today. Open issues for newcomers:\n  {GOOD_FIRST_ISSUES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
