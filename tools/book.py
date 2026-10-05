"""Shared helpers for the build tools: the book's page order, page metadata, the data layer and
who looks after each part (governance.toml).

Only the Python standard library is used, so the book builds with Quarto and Python 3.11+.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUARTO_YML = ROOT / "_quarto.yml"
GOVERNANCE_TOML = ROOT / "governance.toml"
# Shared by tools/check.py and tools/claims.py. Cross-reference prefixes Quarto knows; a citation or
# cross-reference, `@key` or `@sec-label`; and the opening fence of a div, `::: {attributes}`.
CROSSREF_PREFIXES = ("sec", "eq", "fig", "tbl", "lst", "thm", "lem", "cor", "prp", "def", "exm", "exr")
CITATION = re.compile(r"(?<![\w@./])@([A-Za-z][\w:.#$%&+?<>~/-]*[\w])")
CALLOUT = re.compile(r"^:::+\s*\{([^}\n]*)\}", re.M)
# A GitHub handle: letters, digits and single hyphens, at most 39 characters, no hyphen at the ends.
GITHUB_HANDLE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")

STATUS_BY_KIND = {
    "chapter": {"proposed", "drafting", "scientific-review", "done"},
    "interlude": {"proposed", "drafting", "scientific-review", "done"},
    "living-review": {"proposed", "drafting", "scientific-review", "done"},
    "paper": {"draft", "in-review", "stable"},
}

# Pages written by tools/generate.py. They are scanned for links, never for concept usage.
GENERATED_PAGES = {
    "appendices/concepts.qmd",
    "appendices/notation.qmd",
    "appendices/constants.qmd",
    "appendices/people.qmd",
}


@dataclass
class Page:
    path: str  # relative to ROOT, for example "chapters/landauer/index.qmd"
    part: str | None  # the part it belongs to in _quarto.yml, or None
    appendix: bool
    meta: dict = field(default_factory=dict)
    title: str = ""
    label: str | None = None
    body: str = ""

    @property
    def kind(self) -> str:
        top = self.path.split("/", 1)[0]
        if self.appendix:
            return "appendix"
        if top == "chapters":
            return "chapter"
        if top == "interludes":
            return "interlude"
        if top == "building-alan":
            return "living-review" if self.path != "building-alan/index.qmd" else "section"
        if top == "papers":
            return "paper" if self.path != "papers/index.qmd" else "section"
        return "front"

    @property
    def slug(self) -> str:
        parts = Path(self.path).parts
        return parts[-2] if parts[-1] == "index.qmd" and len(parts) > 1 else Path(self.path).stem

    @property
    def html(self) -> str:
        return self.path[: -len(".qmd")] + ".html"

    @property
    def scope(self) -> str | None:
        match = re.search(r"<!--\s*Scope:\s*(.+?)\s*-->", self.body, re.S)
        return " ".join(match.group(1).split()) if match else None


def site_url() -> str:
    match = re.search(r"^\s*site-url:\s*(\S+)", QUARTO_YML.read_text(encoding="utf-8"), re.M)
    url = match.group(1) if match else ""
    return url if url.endswith("/") else url + "/"


def repo_url() -> str:
    match = re.search(r"^\s*repo-url:\s*(\S+)", QUARTO_YML.read_text(encoding="utf-8"), re.M)
    return match.group(1).rstrip("/") if match else ""


def book_order() -> list[tuple[str, str | None, bool]]:
    """Pages listed under book: chapters and book: appendices, in order, as (path, part, appendix).

    The scanner relies on the layout of _quarto.yml: one file per line, parts as `- part: "Title"`.
    Glob patterns (the `render:` list) are skipped.
    """
    order: list[tuple[str, str | None, bool]] = []
    part: str | None = None
    section = None
    for line in QUARTO_YML.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if re.match(r"^chapters:\s*$", stripped) and line.startswith("  chapters"):
            section, part = "chapters", None
            continue
        if re.match(r"^appendices:\s*$", stripped) and line.startswith("  appendices"):
            section, part = "appendices", None
            continue
        if section is None:
            continue
        if line and not line.startswith(" "):
            break  # left the book: block
        part_match = re.match(r'^-\s+part:\s+"?(.+?)"?\s*$', stripped)
        if part_match:
            part = part_match.group(1)
            continue
        file_match = re.match(r"^-\s+([\w./-]+\.qmd)\s*$", stripped)
        if file_match and "*" not in file_match.group(1):
            indent = len(line) - len(line.lstrip())
            in_part = part if indent > 4 else None
            if indent <= 4:
                part = None
            order.append((file_match.group(1), in_part, section == "appendices"))
    return order


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Front matter in the subset the templates use: `key: value`, `key: []`, `key: [a, b]`, null."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict = {}
    for raw in text[4:end].splitlines():
        line = re.sub(r"\s+#.*$", "", raw).rstrip()
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in ("", "null", "~"):
            meta[key] = None
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [v.strip().strip("\"'") for v in inner.split(",")] if inner else []
        else:
            meta[key] = value.strip("\"'")
    body = text[end + 4 :].lstrip("\n")
    return meta, body


def read_page(path: str, part: str | None = None, appendix: bool = False) -> Page:
    file = ROOT / path
    text = file.read_text(encoding="utf-8") if file.exists() else ""
    meta, body = parse_front_matter(text)
    page = Page(path=path, part=part, appendix=appendix, meta=meta, body=body)
    heading = re.search(r"^#\s+(.+?)\s*(\{[^}]*\})?\s*$", body, re.M)
    if heading:
        page.title = heading.group(1).strip()
        attrs = heading.group(2) or ""
        label = re.search(r"#((?:sec)-[\w-]+)", attrs)
        page.label = label.group(1) if label else None
    if not page.title:
        page.title = meta.get("title") or page.slug
    return page


def pages() -> list[Page]:
    return [read_page(path, part, appendix) for path, part, appendix in book_order()]


def governance() -> dict:
    """governance.toml: `maintainers` and one `part` entry per part, with its `moderators`."""
    with open(GOVERNANCE_TOML, "rb") as handle:
        return tomllib.load(handle)


def maintainers() -> list[str]:
    return list(governance().get("maintainers", []))


def part_moderators() -> dict[str, list[str]]:
    """Part title -> the GitHub handles of its moderators."""
    found = {}
    for entry in governance().get("part", []):
        if isinstance(entry, dict) and isinstance(entry.get("title"), str):
            moderators = entry.get("moderators", [])
            found[entry["title"]] = list(moderators) if isinstance(moderators, list) else []
    return found


def part_slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def governance_url() -> str:
    return repo_url() + "/blob/main/GOVERNANCE.md"


def load_data(name: str) -> dict:
    with open(ROOT / "data" / name, "rb") as handle:
        return tomllib.load(handle)


def technologies() -> dict[str, tuple[Path, dict]]:
    found = {}
    for path in sorted((ROOT / "data" / "technologies").glob("*.toml")):
        if path.name.startswith("_"):
            continue
        with open(path, "rb") as handle:
            found[path.stem] = (path, tomllib.load(handle))
    return found


def bib_entries() -> dict[str, str | None]:
    """Citation key -> the year field of the entry (None when it has no year)."""
    text = (ROOT / "references.bib").read_text(encoding="utf-8")
    starts = [
        match
        for match in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", text, re.M)
        if match.group(1).lower() not in {"comment", "string", "preamble"}
    ]
    found = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        year = re.search(r"\byear\s*=\s*[{\"]?(\d{4})", text[match.end() : end], re.I)
        found[match.group(2)] = year.group(1) if year else None
    return found


def bib_keys() -> set[str]:
    return set(bib_entries())


def strip_code_and_comments(text: str) -> str:
    """Remove fenced code, inline code and HTML comments, which may mention keys as examples."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^(```|~~~).*?^\1\s*$", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)
