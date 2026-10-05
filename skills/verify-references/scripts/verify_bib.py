"""Compare the BibTeX entries that have a DOI with their Crossref metadata.

    python3 skills/verify-references/scripts/verify_bib.py [key ...]

Checks title, year and first author's family name, and asks Crossref for notices that update the
work (Crossref carries the Retraction Watch database). A retraction, withdrawal or removal is a
failure; any other notice (correction, erratum, expression of concern) is printed as a warning.
Exits with 1 on any mismatch, retraction or lookup error. Uses only the Python standard library.
"""

from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
USER_AGENT = "the-alan-machine-verify-bib/1.0 (https://github.com/the-alan-machine/the-alan-machine)"

RETRACTING = {"retraction", "withdrawal", "removal"}

LATEX_ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327"}


def entries(text: str) -> dict[str, dict[str, str]]:
    found = {}
    for match in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", text, re.M):
        if match.group(1).lower() in {"comment", "string", "preamble"}:
            continue
        start, depth, i = match.end(), 1, match.end()
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body = text[start : i - 1]
        fields = {}
        for field in re.finditer(r"(\w+)\s*=\s*", body):
            j, value = field.end(), ""
            if j < len(body) and body[j] == "{":
                depth, k = 1, j + 1
                while k < len(body) and depth:
                    depth += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                value = body[j + 1 : k - 1]
            elif j < len(body) and body[j] == '"':
                k = body.index('"', j + 1)
                value = body[j + 1 : k]
            else:
                value = re.match(r"[^,\s]*", body[j:]).group(0)
            fields.setdefault(field.group(1).lower(), value)
        found[match.group(2)] = fields
    return found


def normalize(text: str) -> str:
    text = re.sub(r"\\([`'^\"~c])\{?(\w)\}?", lambda m: m.group(2) + LATEX_ACCENTS[m.group(1)], text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"<[^>]+>|\\[a-zA-Z]+|[{}$]", " ", text)
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())


def get_message(url: str, retries: int = 3) -> dict:
    """GET a Crossref API URL. Waits and retries on 429 (Crossref rate-limits bursts) and 503."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)["message"]
        except urllib.error.HTTPError as error:
            if error.code not in (429, 503) or attempt == retries:
                raise
            wait = error.headers.get("Retry-After")
            time.sleep(float(wait) if wait and wait.isdigit() else delay)
            delay *= 2
    raise AssertionError("unreachable")


def crossref(doi: str) -> dict:
    return get_message("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))


def crossref_updates(doi: str) -> list[dict]:
    """Notices registered as updating the DOI: one dict per notice with type, notice, date, source."""
    url = "https://api.crossref.org/works?rows=100&filter=updates:" + urllib.parse.quote(doi, safe="/")
    items = get_message(url)["items"]
    notices = []
    for item in items:
        for update in item.get("update-to", []):
            if str(update.get("DOI", "")).lower() != doi.lower():
                continue
            parts = (update.get("updated") or {}).get("date-parts") or [[]]
            date = "-".join(f"{int(p):02d}" for p in parts[0] if p) or "no date"
            notices.append({
                "type": str(update.get("type", "unknown")).lower(),
                "notice": item.get("DOI", "?"),
                "date": date,
                "source": update.get("source", "publisher"),
            })
    return notices


def crossref_years(message: dict) -> list[str]:
    """Years Crossref records for the work. The DOI's BibTeX uses `issued`; print dates may differ."""
    years = []
    for field in ("issued", "published-print", "published-online"):
        parts = message.get(field, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0] and str(parts[0][0]) not in years:
            years.append(str(parts[0][0]))
    return years


def main(keys: list[str]) -> int:
    bib = entries((ROOT / "references.bib").read_text(encoding="utf-8"))
    selected = keys or list(bib)
    failures = 0
    for key in selected:
        entry = bib.get(key)
        if entry is None:
            print(f"MISSING   {key}: not in references.bib")
            failures += 1
            continue
        doi = entry.get("doi")
        if not doi:
            print(f"NO-DOI    {key}: check it by hand against the publisher or ISBN record")
            continue
        try:
            message = crossref(doi)
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
            print(f"ERROR     {key}: {doi}: {error}")
            failures += 1
            continue
        problems = []
        title = normalize(" ".join(message.get("title", [""])))
        if normalize(entry.get("title", "")) != title:
            problems.append(f"title is {' '.join(message.get('title', ['?']))!r}")
        years = crossref_years(message)
        if years and entry.get("year") not in years:
            problems.append(f"year is {' or '.join(years)}")
        authors = message.get("author", [])
        if authors:
            family = normalize(authors[0].get("family", authors[0].get("name", "")))
            first = normalize(re.split(r"\s+and\s+", entry.get("author", ""))[0].split(",")[0])
            if family and family not in first:
                problems.append(f"first author is {authors[0].get('family')!r}")
        if problems:
            print(f"MISMATCH  {key}: {'; '.join(problems)}")
            failures += 1
        else:
            print(f"OK        {key}")
        try:
            notices = crossref_updates(doi)
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
            print(f"ERROR     {key}: {doi}: updates: {error}")
            failures += 1
            continue
        for notice in notices:
            text = f"{notice['type']} notice {notice['notice']} of {notice['date']} ({notice['source']})"
            if notice["type"] in RETRACTING:
                print(f"RETRACTED {key}: {text}; do not cite it as valid")
                failures += 1
            else:
                print(f"UPDATED   {key}: {text}; read it and check the cited claim still holds")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
