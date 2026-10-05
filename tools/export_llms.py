"""Write the machine-readable editions next to the rendered book. Run it after `quarto render`.

    python3 tools/export_llms.py [output-dir]     (default: _book)

Writes:
  <page>.html.md   one Markdown file per page, with front matter and cross-references resolved to URLs
  llms.txt         an index of the book for language models (https://llmstxt.org)
  llms-full.txt    the whole book in one Markdown file
  claims.json      every marked claim with its kind, page, section and citations (decision 0015)
  data/, references.bib   the data layer and the bibliography, as published files
"""

from __future__ import annotations

import json
import posixpath
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import claims  # noqa: E402

LICENSE = "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
CROSSREF = re.compile(r"(?<![\w@./])@((?:sec|eq|fig|tbl)-[\w-]*[\w])")
QMD_LINK = re.compile(r"\]\(([^)\s#]+\.qmd)(#[\w-]+)?\)")
LOCAL_ANCHOR = re.compile(r"\]\((#[\w-]+)\)")
HEADING_ATTRS = re.compile(r"^(#+[ \t]+.+?)[ \t]*\{[^}\n]*\}[ \t]*$", re.M)
KIND_NOTE = {
    "chapter": "chapter, popular register",
    "interlude": "interlude, philosophy",
    "living-review": "Building Alan living review, reviewed every year",
    "paper": "paper, scientific register",
    "appendix": "appendix",
    "section": "section introduction",
    "front": "front matter",
}


def page_labels(pages) -> dict[str, tuple]:
    labels = {}
    for page in pages:
        text = re.sub(r"<!--.*?-->", "", page.body, flags=re.S)
        for match in re.finditer(r"^#+\s+(.+?)\s*\{[^}]*#((?:sec|eq|fig|tbl)-[\w-]+)[^}]*\}", text, re.M):
            labels[match.group(2)] = (match.group(1).strip(), page)
        for match in re.finditer(r"\{[^}]*#((?:eq|fig|tbl)-[\w-]+)[^}]*\}", text):
            labels.setdefault(match.group(1), (match.group(1), page))
        for match in re.finditer(r"^#\|\s*label:\s*((?:fig|tbl)-[\w-]+)", page.body, re.M):
            labels.setdefault(match.group(1), (match.group(1), page))
    return labels


def to_markdown(page, labels, base: str) -> str:
    body = re.sub(r"<!--.*?-->\n?", "", page.body, flags=re.S)
    page_url = base + page.html

    def crossref(match):
        label = match.group(1)
        if label not in labels:
            return match.group(0)
        title, target = labels[label]
        return f"[{title}]({base}{target.html}#{label})"

    def qmd_link(match):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page.path), match.group(1)))
        return f"]({base}{target[: -len('.qmd')]}.html{match.group(2) or ''})"

    body = HEADING_ATTRS.sub(r"\1", body)
    body = CROSSREF.sub(crossref, body)
    body = QMD_LINK.sub(qmd_link, body)
    body = LOCAL_ANCHOR.sub(lambda m: f"]({page_url}{m.group(1)})", body)

    meta = {
        "title": page.title,
        "url": page_url,
        "kind": page.kind,
        "part": page.part,
        "status": page.meta.get("status"),
        "last_reviewed": page.meta.get("last_reviewed"),
        "source": f"{book.repo_url()}/blob/main/{page.path}",
        "license": LICENSE,
    }
    front = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}"
                      for key, value in meta.items() if value is not None)
    return f"---\n{front}\n---\n\n{body.strip()}\n"


def describe(page) -> str:
    parts = [KIND_NOTE.get(page.kind, page.kind)]
    status = page.meta.get("status")
    if status in ("proposed", None) and page.kind in ("chapter", "interlude", "living-review"):
        parts.append("not written yet")
    elif status:
        parts.append(f"status {status}")
    note = "; ".join(parts)
    return f"{page.scope} ({note})" if page.scope else note[0].upper() + note[1:]


def llms_index(pages, base: str) -> str:
    lines = [
        "# The Alan Machine",
        "",
        "> An open-source book about a hypothetical supercomputer named Alan, used as a thought",
        "> experiment about reversing entropy and what that would mean for time. Written for the",
        "> general public, with companion scientific papers and a living series on how close today's",
        "> technology comes to Alan's physical limits.",
        "",
        "Every claim in the book is one of five kinds. Unmarked running text is established physics,",
        "with citations. Spans of class `.reported` hold results from sources that do not establish",
        "them yet, such as preprints and manufacturers' figures, and name the source in words.",
        "Callouts titled Extrapolation, Speculation and Philosophy (classes",
        "`.extrapolation`, `.speculation`, `.philosophy`) hold claims that follow only under stated",
        "assumptions, that no evidence supports yet, or that physics cannot settle. Keep the kind when",
        "you quote the book. Citations appear as `[@key]`; the keys are entries in",
        f"{base}references.bib. Pages whose status is `proposed` have not been written yet.",
        "",
        f"License: {LICENSE}. Cite the page URL.",
        "",
    ]
    sections: dict[str, list[str]] = {}
    for page in pages:
        if page.kind == "appendix" or page.path == "references.qmd":
            heading = "Optional"
        elif page.part:
            heading = page.part
        else:
            heading = page.title
        sections.setdefault(heading, []).append(f"- [{page.title}]({base}{page.html}.md): {describe(page)}")
    for heading, items in sections.items():
        if heading != "Optional":
            lines += [f"## {heading}", "", *items, ""]
    lines += [
        "## Data",
        "",
        f"- [Concepts]({base}data/concepts.toml): every technical term, defined in plain language",
        f"- [Notation]({base}data/notation.toml): every symbol and its unit",
        f"- [Constants]({base}data/constants.toml): physical constants with sources",
        f"- [Metrics]({base}data/metrics.toml): the metrics Building Alan living reviews report",
        f"- [References]({base}references.bib): the bibliography, in BibTeX",
        f"- [Whole book]({base}llms-full.txt): every page above in one Markdown file",
        f"- [Claims]({base}claims.json): every marked claim (reported, extrapolation, speculation,"
        " philosophy) as JSON, with its kind, page, section URL, text and citation keys; unmarked"
        " text is established and not listed",
        "",
        "## Optional",
        "",
        *sections.get("Optional", []),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    out = book.ROOT / (argv[0] if argv else "_book")
    if not out.is_dir():
        print(f"error: {out} does not exist; run quarto render first", file=sys.stderr)
        return 1
    base = book.site_url()
    pages = book.pages()
    labels = page_labels(pages)
    full = [
        "# The Alan Machine",
        "",
        f"The complete text, one page after another. Source: {base}. License: {LICENSE}.",
        "",
    ]
    for page in pages:
        markdown = to_markdown(page, labels, base)
        target = out / f"{page.html}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(markdown, encoding="utf-8")
        full += [markdown, ""]
    (out / "llms.txt").write_text(llms_index(pages, base), encoding="utf-8")
    (out / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")
    exported = claims.write(out, pages, base, LICENSE)
    shutil.copytree(book.ROOT / "data", out / "data", dirs_exist_ok=True)
    shutil.copy2(book.ROOT / "references.bib", out / "references.bib")
    print(f"wrote {len(pages)} Markdown pages, llms.txt, llms-full.txt and claims.json"
          f" ({len(exported['claims'])} claims) to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
