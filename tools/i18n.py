"""Translations of the book (decision 0014).

English is the source. A translation never changes the English; it sits under i18n/<lang>/, at the
path of what it translates:

    i18n/languages.toml               the languages, with their maintainers
    i18n/<lang>/strings.toml          the words of the edition around the pages: part titles,
                                      notices, the titles of claim callouts, the generated appendices
    i18n/<lang>/glossary.toml         the terms translators agree on
    i18n/<lang>/<page>.qmd            a page, such as i18n/pt/chapters/landauer/index.qmd
    i18n/<lang>/data/<file>.toml      an overlay of data/concepts.toml, notation.toml or constants.toml

A translated page records in its front matter the fingerprint of the English it was translated
from (`source`). When the English changes, the page is stale: the edition still shows it, with a
notice that links to the English, and tools/check.py warns. A text of a data overlay that is stale
falls back to the English. The papers are written for specialists and stay in English.

tools/edition.py builds the edition of each published language into _book/<lang>/.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import textwrap
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import book

BASE = book.ROOT / "i18n"
LANGUAGES_FILE = BASE / "languages.toml"
STATUSES = ("machine", "reviewed")
PAGE_STATUSES = ("todo", *STATUSES)  # a page started with tools/translate.py template is "todo"
FINGERPRINT = re.compile(r"^[0-9a-f]{10}$")
LANGUAGE_ID = re.compile(r"^[a-z]{2,3}(-[a-z0-9]+)?$")
LANGUAGE_TAG = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
GENERATED_BLOCK = re.compile(r"(<!-- BEGIN generated: (.+?) -->).*?(<!-- END generated: \2 -->)", re.S)
CLAIM_CLASSES = ("extrapolation", "speculation", "philosophy")
DATA_SOURCES = ("data/concepts.toml", "data/notation.toml", "data/constants.toml")
WIDTH = 100

# The words of the English edition. A language replaces them in i18n/<lang>/strings.toml, table by
# table; generate.py writes the generated appendices with them.
ENGLISH: dict = {
    "decimal": ".",
    "edition": {
        "author": "João Alisson and contributors",
        "link": "Read in English",
    },
    "claims": {
        "extrapolation": "Extrapolation",
        "speculation": "Speculation",
        "philosophy": "Philosophy",
    },
    "notice": {
        "untranslated": "This page is not translated yet and is shown in English. [How to help translate]({translating}).",
        "english_only": "The papers are written for specialists and stay in English.",
        "machine": "This page was translated by machine and has not been reviewed yet. When in doubt, the [English original]({english}) prevails.",
        "stale": "The English original has changed since this translation. See the [English original]({english}).",
        "data_machine": "Part of this page was translated by machine and has not been reviewed yet.",
        "data_partial": "Part of this page is still in English. [How to help translate]({translating}).",
    },
    "parts": {},
    "tools": {},
    "status": {},
    "pages": {
        "concepts_title": "Concepts",
        "concepts_intro": "Every technical term the book uses, in plain language. Each entry lists the pages that use it.",
        "related": "Related",
        "references": "References",
        "used_in": "Used in",
        "notation_title": "Notation",
        "notation_intro": "Every symbol keeps the same meaning across the whole book.",
        "notation_header": "| Symbol | Meaning | Unit |",
        "constants_title": "Constants",
        "constants_intro": "Values from the 2019 revision of the SI, where the constant is exact by definition, and from\nCODATA otherwise.",
        "constants_header": "| Constant | Symbol | Value | Unit | Standard uncertainty | Source |",
        "exact": "exact",
        "people_title": "Moderators and Curators",
        "people_intro": (
            "The people who look after the book. Maintainers look after the whole repository. Moderators\n"
            "look after a part: they review the changes to its pages and triage its issues. Curators look\n"
            "after single pages and review their living reviews. Translators look after the book in another\n"
            "language. People are named by their GitHub handle. How the roles work, and how to take one, is in\n"
            "[GOVERNANCE.md]({governance})."
        ),
        "maintainers": "Maintainers",
        "moderators": "Moderators",
        "moderators_header": "| Part | Moderators |",
        "curators": "Curators",
        "curators_header": "| Page | Part | Curators |",
        "no_curator": "No page has a curator yet.",
        "translators": "Translators",
        "translators_intro": (
            "The maintainers of a language approve the translations into it; the reviewers have reviewed\n"
            "some of them. How to translate is in [docs/translating.md]({translating})."
        ),
        "translators_header": "| Language | Maintainers | Reviewers |",
        "no_language": "The book is not translated yet.",
        "none_yet": "none yet",
        "living_review_header": "| Living review | Status | Last reviewed | Review due | Curators |",
        "never": "never",
        "not_reviewed": "not reviewed yet",
    },
}


@dataclass
class Language:
    id: str
    tag: str
    name: str
    english_name: str
    maintainers: list[str]
    published: bool

    @property
    def folder(self) -> Path:
        return BASE / self.id


def languages() -> dict[str, Language]:
    """The registered languages, from i18n/languages.toml; English is the source and is not one."""
    if not LANGUAGES_FILE.is_file():
        return {}
    with open(LANGUAGES_FILE, "rb") as handle:
        items = tomllib.load(handle).get("language", [])
    found = {}
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        found[str(item.get("id", ""))] = Language(
            id=str(item.get("id", "")),
            tag=str(item.get("tag", "")),
            name=str(item.get("name", "")),
            english_name=str(item.get("english_name", "")),
            maintainers=list(item.get("maintainers", [])) if isinstance(item.get("maintainers"), list) else [],
            published=bool(item.get("published", False)),
        )
    return found


def published() -> list[Language]:
    return [language for language in languages().values() if language.published]


def fingerprint(text: str) -> str:
    """The first ten hex digits of the SHA-256 of the text with its whitespace collapsed, so that
    rewrapping a paragraph does not make its translations stale."""
    return hashlib.sha256(" ".join(str(text).split()).encode("utf-8")).hexdigest()[:10]


def edition_url(lang: str | None, page_path: str = "") -> str:
    """The address of a page in an edition: the English one at the site's root, the others under
    /<lang>/."""
    base = book.site_url() + (f"{lang}/" if lang else "")
    return base + (page_path[: -len(".qmd")] + ".html" if page_path else "")


def strings(lang: str | None) -> dict:
    """The words of an edition: ENGLISH, with each table replaced key by key by the language's own
    from i18n/<lang>/strings.toml. A malformed file leaves the English."""
    found = copy.deepcopy(ENGLISH)
    file = BASE / lang / "strings.toml" if lang else None
    if not file or not file.is_file():
        return found
    try:
        with open(file, "rb") as handle:
            own = tomllib.load(handle)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError):
        return found
    for key, value in own.items():
        if isinstance(value, dict) and isinstance(found.get(key), dict):
            found[key].update({k: v for k, v in value.items() if isinstance(v, str)})
        elif isinstance(value, str) and isinstance(found.get(key), str):
            found[key] = value
    return found


def decimal(text: str, mark: str) -> str:
    """A number written by Python with the decimal mark of a language. In LaTeX a comma needs
    braces, or it is set as punctuation with a space after it."""
    if mark == ".":
        return text
    return re.sub(r"(?<=\d)\.(?=\d)", "{,}" if mark == "," else mark, text)


# Pages -----------------------------------------------------------------------------------------


def translatable(page: book.Page) -> bool:
    """Pages a language translates by hand: not the papers, which stay in English, and not the
    generated appendices, which tools/generate.py writes from the data overlays."""
    return page.path not in book.GENERATED_PAGES and not page.path.startswith("papers/")


def page_fingerprint(body: str) -> str:
    """The fingerprint of an English page, without the tables tools/generate.py writes into it, so
    that a new review date does not make its translations stale."""
    return fingerprint(GENERATED_BLOCK.sub(r"\1\3", body))


def page_file(lang: str, page_path: str) -> Path:
    return BASE / lang / page_path


@dataclass
class PageTranslation:
    path: str  # the English page, such as "chapters/landauer/index.qmd"
    file: Path
    meta: dict = field(default_factory=dict)
    body: str = ""
    state: str = "missing"  # "missing", "stale", "machine" or "reviewed"

    @property
    def reviewers(self) -> list[str]:
        value = self.meta.get("reviewers")
        return value if isinstance(value, list) else []


def page_translation(lang: str, page: book.Page) -> PageTranslation:
    file = page_file(lang, page.path)
    found = PageTranslation(path=page.path, file=file)
    if not file.is_file():
        return found
    found.meta, found.body = book.parse_front_matter(file.read_text(encoding="utf-8"))
    if not found.body.strip() or found.meta.get("translation") == "todo":
        return found
    if found.meta.get("source") != page_fingerprint(page.body):
        found.state = "stale"
    else:
        found.state = found.meta.get("translation") if found.meta.get("translation") in STATUSES else "machine"
    return found


def page_translations(lang: str, pages: list[book.Page] | None = None) -> list[PageTranslation]:
    return [page_translation(lang, page) for page in (pages if pages is not None else book.pages()) if translatable(page)]


def page_title(lang: str | None, page: book.Page) -> str:
    """The title of a page in an edition: its translation's first heading when there is one."""
    if lang:
        translation = page_translation(lang, page)
        if translation.state != "missing":
            heading = re.search(r"^#\s+(.+?)\s*(\{[^}]*\})?\s*$", translation.body, re.M)
            if heading:
                return heading.group(1).strip()
    return page.title


def template_page(page: book.Page) -> str:
    """A new translation of a page: the English body to translate in place, under the front matter
    that records what it was translated from."""
    return (
        "---\n"
        "translation: todo             # todo until translated, then machine or reviewed (decision 0014)\n"
        f"source: {page_fingerprint(page.body)}             # the English it follows; tools/translate.py stamp\n"
        "reviewers: []                 # GitHub handles of whoever reviewed this translation\n"
        "---\n\n" + page.body
    )


def set_meta(text: str, key: str, value: str) -> str:
    """Replace one field of a translation's front matter, keeping its comment."""
    pattern = re.compile(rf"^({re.escape(key)}:\s*)(\S+)", re.M)
    end = text.find("\n---", 4)
    head, rest = text[: end + 1], text[end + 1 :]
    if pattern.search(head):
        return pattern.sub(lambda m: m.group(1) + value, head, count=1) + rest
    return head.replace("---\n", f"---\n{key}: {value}\n", 1) + rest


# Data overlays ---------------------------------------------------------------------------------


@dataclass
class Slot:
    path: str  # such as "concept[entropy].definition"
    english: str
    table: dict  # the table that holds the text
    key: str  # the field in that table


def _text(table: dict, key: str) -> bool:
    return isinstance(table.get(key), str) and bool(table[key].strip())


def slots(source: str, data: dict) -> list[Slot]:
    """The translatable texts of a data file. Symbols, units, values and identifiers are never
    translated."""
    fields = {
        "data/concepts.toml": ("concept", ("term", "short", "definition")),
        "data/notation.toml": ("symbol", ("meaning",)),
        "data/constants.toml": ("constant", ("name", "source")),
    }
    if source not in fields:
        return []
    table_name, keys = fields[source]
    found = []
    for item in data.get(table_name, []):
        for key in keys:
            if isinstance(item, dict) and _text(item, key):
                found.append(Slot(f"{table_name}[{item.get('id')}].{key}", item[key], item, key))
    return found


def sources() -> dict[str, dict]:
    """The data files a translation can overlay, by their path relative to the repository."""
    return {source: book.load_data(source.split("/", 1)[1]) for source in DATA_SOURCES}


def overlay_path(lang: str, source: str) -> Path:
    return BASE / lang / source


@dataclass
class Entry:
    path: str
    source: str
    text: str
    status: str | None = None  # overrides the file's status for this text


@dataclass
class Overlay:
    file: Path
    status: str = "machine"
    reviewed_by: list[str] = field(default_factory=list)
    entries: list[Entry] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def by_path(self) -> dict[str, Entry]:
        return {entry.path: entry for entry in self.entries}


def load_overlay(file: Path) -> Overlay:
    """Read an overlay. Raises tomllib.TOMLDecodeError; tools/check.py reports malformed fields."""
    with open(file, "rb") as handle:
        raw = tomllib.load(handle)
    entries = [
        Entry(
            path=str(item.get("path", "")),
            source=str(item.get("source", "")),
            text=item.get("text", "") if isinstance(item.get("text", ""), str) else "",
            status=item.get("status"),
        )
        for item in raw.get("text", [])
        if isinstance(item, dict)
    ]
    reviewed_by = raw.get("reviewed_by", [])
    return Overlay(
        file=file,
        status=raw.get("status", "machine"),
        reviewed_by=list(reviewed_by) if isinstance(reviewed_by, list) else [],
        entries=entries,
        raw=raw,
    )


def _overlay(lang: str, source: str) -> Overlay:
    file = overlay_path(lang, source)
    try:
        return load_overlay(file) if file.is_file() else Overlay(file=file)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError):
        return Overlay(file=file)


@dataclass
class State:
    slot: Slot
    entry: Entry | None
    state: str  # "missing", "stale", "machine" or "reviewed"


def states(lang: str, source: str, data: dict, overlay: Overlay | None = None) -> list[State]:
    """Each translatable text of a data file and where its translation stands."""
    overlay = overlay if overlay is not None else _overlay(lang, source)
    entries = overlay.by_path()
    found = []
    for slot in slots(source, data):
        entry = entries.get(slot.path)
        if entry is None or not entry.text.strip():
            state = "missing"
        elif entry.source != fingerprint(slot.english):
            state = "stale"
        else:
            state = entry.status if entry.status in STATUSES else overlay.status
            state = state if state in STATUSES else "machine"
        found.append(State(slot, entry, state))
    return found


def translate(lang: str, source: str, data: dict) -> tuple[dict, list[State]]:
    """A copy of a data file with the current translations in place of the English, and the state
    of each text. A stale or missing translation leaves the English."""
    copied = copy.deepcopy(data)
    found = states(lang, source, copied)
    for item in found:
        if item.state in STATUSES:
            text = item.entry.text
            if "\n" not in item.slot.english.strip():
                text = " ".join(text.split())  # one line in English, one line translated
            item.slot.table[item.slot.key] = text
    return copied, found


def reviewers(lang: str) -> list[str]:
    """Everyone who reviewed part of a language: the reviewers of its pages and of its overlays."""
    found: list[str] = []
    for translation in page_translations(lang):
        found += translation.reviewers
    for source in DATA_SOURCES:
        found += _overlay(lang, source).reviewed_by
    unique: dict[str, str] = {}
    for person in found:
        if isinstance(person, str) and book.GITHUB_HANDLE.match(person):
            unique.setdefault(person.lower(), person)
    return sorted(unique.values(), key=str.lower)


# Writing overlays ------------------------------------------------------------------------------


def _string(key: str, text: str, multiline: bool) -> list[str]:
    single = f"{key} = {json.dumps(text.strip(), ensure_ascii=False)}"
    if not multiline and "\n" not in text.strip() and len(single) <= WIDTH:
        return [single]
    body = []
    for paragraph in re.split(r"\n\s*\n", text.strip()):
        flat = " ".join(paragraph.split()).replace("\\", "\\\\").replace('"""', '\\"""')
        body += textwrap.wrap(flat, WIDTH, break_long_words=False, break_on_hyphens=False) + [""]
    return [f'{key} = """', *body[:-1], '"""']


def write_overlay(lang: str, source: str, data: dict, overlay: Overlay):
    """Write an overlay in the order of its source file. Texts whose path the source no longer has
    are kept at the end, where tools/check.py reports them."""
    language = languages().get(lang)
    title = language.english_name if language else lang
    order = {slot.path: (index, slot) for index, slot in enumerate(slots(source, data))}
    entries = sorted(overlay.entries, key=lambda e: order.get(e.path, (len(order), None))[0])
    lines = [
        f"# {title} translation of {source} (decision 0014).",
        "# Each text replaces the English at `path` while `source` is the fingerprint of the English it",
        "# was translated from. Run python3 tools/translate.py show to see both side by side.",
        f'status = "{overlay.status}"',
        f"reviewed_by = {json.dumps(overlay.reviewed_by)}",
    ]
    for entry in entries:
        slot = order.get(entry.path, (None, None))[1]
        lines += ["", "[[text]]", f"path = {json.dumps(entry.path)}", f'source = "{entry.source}"']
        if entry.status:
            lines.append(f'status = "{entry.status}"')
        lines += _string("text", entry.text, multiline=bool(slot and "\n" in slot.english.strip()))
    overlay.file.parent.mkdir(parents=True, exist_ok=True)
    overlay.file.write_text("\n".join(lines) + "\n", encoding="utf-8")
