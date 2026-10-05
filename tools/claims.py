"""The marked claims of the book, as data (decision 0015). tools/export_llms.py writes them to
claims.json next to llms.txt.

A claim is marked when it leaves established physics: a callout of class `.extrapolation`,
`.speculation` or `.philosophy`, or a `[...]{.reported}` span. Unmarked running text is established
(decision 0005) and is not listed. Only the pages of the book are read, never `templates/`, and
fenced code, inline code and HTML comments are removed first, as tools/check.py does.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import book
import i18n

SCHEMA = 1
KINDS = ("reported", *i18n.CLAIM_CLASSES)
ESTABLISHED_RULE = (
    "Only what leaves established physics is marked, so the reading flow is preserved and the "
    "boundary stays visible."
)
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*(\{[^}\n]*\})?[ \t]*$")
FENCE_OPEN = re.compile(r"^:{3,}[ \t]*\S")
FENCE_CLOSE = re.compile(r"^:{3,}[ \t]*$")
REPORTED_END = re.compile(r"\]\{\.reported\}")
TITLE = re.compile(r'\btitle="([^"]*)"')


def citations(text: str) -> list[str]:
    """Citation keys in the order they first appear, without cross-references such as @sec-x."""
    keys = []
    for name in book.CITATION.findall(text):
        if "-" in name and name.split("-", 1)[0] in book.CROSSREF_PREFIXES:
            continue
        if name not in keys:
            keys.append(name)
    return keys


def headings(lines: list[str]) -> list[tuple[str, str | None] | None]:
    """For each line, the text and id of the last heading at or before it (None before the first)."""
    current = None
    found = []
    for line in lines:
        match = HEADING.match(line)
        if match:
            ident = re.search(r"#([\w-]+)", match.group(3) or "")
            current = (match.group(2).strip(), ident.group(1) if ident else None)
        found.append(current)
    return found


def callout_end(lines: list[str], start: int) -> int:
    """Index of the fence that closes the div opened at lines[start], counting nested divs."""
    depth = 1
    for index in range(start + 1, len(lines)):
        if FENCE_CLOSE.match(lines[index]):
            depth -= 1
            if depth == 0:
                return index
        elif FENCE_OPEN.match(lines[index]):
            depth += 1
    return len(lines)


def reported_spans(text: str) -> list[tuple[int, str]]:
    """(offset of the opening bracket, inner Markdown) for every `[...]{.reported}` span."""
    spans = []
    for match in REPORTED_END.finditer(text):
        depth, index = 1, match.start() - 1
        while index >= 0:
            if text[index] == "]":
                depth += 1
            elif text[index] == "[":
                depth -= 1
                if depth == 0:
                    break
            index -= 1
        if index >= 0:
            spans.append((index, text[index + 1 : match.start()]))
    return spans


def page_claims(page: book.Page, base: str) -> list[dict]:
    text = book.strip_code_and_comments(page.body)
    lines = text.split("\n")
    under = headings(lines)
    page_url = base + page.html
    status = page.meta.get("status")
    found: list[tuple[int, dict]] = []

    def claim(kind: str, line: int, title: str | None, body: str) -> dict:
        heading = under[line]
        item = {
            "kind": kind,
            "page": page.path,
            "url": f"{page_url}#{heading[1]}" if heading and heading[1] else page_url,
            "section": heading[0] if heading else None,
            "title": title,
            "text": body.strip(),
            "citations": citations(body),
            "page_status": status,
        }
        return {key: value for key, value in item.items() if value is not None}

    for index, line in enumerate(lines):
        match = book.CALLOUT.match(line)
        if not match:
            continue
        classes = re.findall(r"\.([\w-]+)", match.group(1))
        kind = next((name for name in classes if name in i18n.CLAIM_CLASSES), None)
        if kind is None:
            continue
        end = callout_end(lines, index)
        title = TITLE.search(match.group(1))
        body = "\n".join(lines[index + 1 : end])
        found.append((index, claim(kind, index, title.group(1) if title else None, body)))

    for offset, inner in reported_spans(text):
        line = text.count("\n", 0, offset)
        found.append((line, claim("reported", line, None, inner)))

    return [item for _, item in sorted(found, key=lambda pair: pair[0])]


def git_version() -> tuple[str | None, str | None]:
    """The short commit and its date, or (None, None) outside a git checkout."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%h %cs"],
            cwd=book.ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return None, None
    return (out[0], out[1]) if len(out) == 2 else (None, None)


def export(pages: list[book.Page], base: str, license_text: str) -> dict:
    claims = [item for page in pages for item in page_claims(page, base)]
    version, version_date = git_version()
    return {
        "schema": SCHEMA,
        "version": version,
        "version_date": version_date,
        "license": license_text,
        "site": base,
        "established_rule": ESTABLISHED_RULE,
        "counts": {kind: sum(1 for item in claims if item["kind"] == kind) for kind in KINDS},
        "claims": claims,
    }


def write(out: Path, pages: list[book.Page], base: str, license_text: str) -> dict:
    data = export(pages, base, license_text)
    (out / "claims.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data
