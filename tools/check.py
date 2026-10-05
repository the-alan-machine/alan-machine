"""Check the sources before rendering. Run it before every pull request; CI runs it too.

    python3 tools/check.py

Errors (exit 1): generated pages out of date or invalid data, citation keys missing from
references.bib or breaking the authorYEARfirstword convention, cross-references to labels that do
not exist, invalid front matter, pages missing from _quarto.yml, a governance.toml that does not
match the parts of the book, people named by something other than a GitHub handle, and in the
translations (decision 0014): an invalid i18n/languages.toml, strings.toml or glossary, a
translation of a page or text the book does not have, and a translated page whose citations,
labels, math or claim callouts differ from its English, or a data text whose numbers do.
Warnings (exit 0): Building Alan living reviews past their review date, and translations whose
English has changed since (stale), which never block an English contributor.
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
import i18n  # noqa: E402

LABEL_DEFINITION = re.compile(r"\{[^}]*#((?:%s)-[\w-]+)[^}]*\}" % "|".join(book.CROSSREF_PREFIXES))
CELL_LABEL = re.compile(r"^#\|\s*label:\s*((?:fig|tbl)-[\w-]+)", re.M)
LANGUAGE_KEYS = {"id", "tag", "name", "english_name", "maintainers", "published"}
OVERLAY_KEYS = {"status", "reviewed_by", "text"}
TEXT_KEYS = {"path", "source", "text", "status"}
GLOSSARY_KEYS = {"en", "text", "note"}
PAGE_KEYS = {"translation", "source", "reviewers"}
DIGITS = re.compile(r"\d+")
PLACEHOLDER = re.compile(r"\{[a-z_]+\}")
MATH = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$", re.S)
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


def load_toml(path: Path, errors: list[str]) -> dict | None:
    try:
        with open(path, "rb") as handle:
            return tomllib.load(handle)
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as error:
        errors.append(f"{path.relative_to(book.ROOT)}: not valid TOML: {error}")
        return None


def check_languages(errors: list[str], warnings: list[str]):
    where = "i18n/languages.toml"
    if not i18n.LANGUAGES_FILE.exists():
        return
    data = load_toml(i18n.LANGUAGES_FILE, errors)
    if data is None:
        return
    for key in set(data) - {"language"}:
        errors.append(f"{where}: unknown field {key!r}")
    seen = set()
    for item in data.get("language", []):
        lang = item.get("id") if isinstance(item, dict) else None
        if not isinstance(lang, str) or not i18n.LANGUAGE_ID.match(lang):
            errors.append(f"{where}: every [[language]] needs an id, a lowercase ISO 639 code such as pt")
            continue
        here = f"{where} [{lang}]"
        if lang == "en":
            errors.append(f"{here}: English is the source of the book, not a translation")
        if lang in seen:
            errors.append(f"{here}: listed twice")
        seen.add(lang)
        for key in set(item) - LANGUAGE_KEYS:
            errors.append(f"{here}: unknown field {key!r}")
        if not i18n.LANGUAGE_TAG.match(str(item.get("tag", ""))):
            errors.append(f"{here}: tag {item.get('tag')!r} is not a BCP 47 tag such as pt-BR")
        for key in ("name", "english_name"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{here}: needs a {key}")
        check_people(here, "maintainers", item.get("maintainers", []), errors)
        if not item.get("maintainers"):
            warnings.append(f"{here}: has no maintainers, so the maintainers of the book approve its translations")
        if item.get("published") and not (i18n.BASE / lang / "strings.toml").is_file():
            errors.append(f"{here}: is published, but i18n/{lang}/strings.toml is missing")
    for folder in sorted(i18n.BASE.iterdir()) if i18n.BASE.is_dir() else []:
        if folder.is_dir() and folder.name not in seen:
            errors.append(f"i18n/{folder.name}/: no language with this id in {where}")


def check_strings(lang: str, parts: list[str], errors: list[str], warnings: list[str]):
    file = i18n.BASE / lang / "strings.toml"
    where = f"i18n/{lang}/strings.toml"
    data = load_toml(file, errors) if file.is_file() else None
    if data is None:
        return
    quarto = book.QUARTO_YML.read_text(encoding="utf-8")
    statuses = set().union(*book.STATUS_BY_KIND.values())
    for key, value in data.items():
        english = i18n.ENGLISH.get(key)
        if english is None:
            errors.append(f"{where}: unknown field {key!r}")
        elif isinstance(english, str):
            if not isinstance(value, str) or not value:
                errors.append(f"{where}: {key} must be a string")
        elif not isinstance(value, dict):
            errors.append(f"{where}: {key} must be a table")
        else:
            for name, text in value.items():
                if not isinstance(text, str) or not text.strip():
                    errors.append(f"{where} [{key}]: {name!r} must be a string")
                elif key == "parts" and name not in parts:
                    warnings.append(f"{where} [parts]: {name!r} is not a part of _quarto.yml")
                elif key == "tools" and f'"{name}"' not in quarto:
                    warnings.append(f"{where} [tools]: {name!r} is not the text of a sidebar link in _quarto.yml")
                elif key == "status" and name not in statuses:
                    warnings.append(f"{where} [status]: {name!r} is not a status of a page")
                elif english and name not in english:
                    errors.append(f"{where} [{key}]: unknown field {name!r}")
                elif english:
                    if sorted(PLACEHOLDER.findall(text)) != sorted(PLACEHOLDER.findall(english[name])):
                        errors.append(f"{where} [{key}]: {name} needs the placeholders of the English: {english[name]!r}")
                    if name.endswith("_header") and text.count("|") != english[name].count("|"):
                        errors.append(f"{where} [{key}]: {name} needs as many columns as the English")
            for name in english or {}:
                if name not in value:
                    warnings.append(f"{where} [{key}]: {name} is missing; the edition shows the English")
    for title in parts:
        if title not in data.get("parts", {}):
            warnings.append(f"{where} [parts]: the part {title!r} has no translation; the edition shows it in English")


def check_glossary(lang: str, errors: list[str]):
    file = i18n.BASE / lang / "glossary.toml"
    where = f"i18n/{lang}/glossary.toml"
    data = load_toml(file, errors) if file.is_file() else None
    if data is None:
        return
    for key in set(data) - {"term"}:
        errors.append(f"{where}: unknown field {key!r}")
    seen = set()
    for index, term in enumerate(data.get("term", []), 1):
        if not isinstance(term, dict):
            continue
        for key in set(term) - GLOSSARY_KEYS:
            errors.append(f"{where}: term {index} has an unknown field {key!r}")
        for key in ("en", "text"):
            if not isinstance(term.get(key), str) or not term[key].strip():
                errors.append(f"{where}: term {index} needs {key}")
        english = str(term.get("en", "")).lower()
        if english in seen:
            errors.append(f"{where}: the term {term.get('en')!r} is listed twice")
        seen.add(english)


def check_overlays(lang: str, errors: list[str], warnings: list[str]):
    folder = i18n.BASE / lang / "data"
    sources = i18n.sources()
    for file in sorted(folder.rglob("*")) if folder.is_dir() else []:
        if file.is_dir():
            continue
        source = file.relative_to(i18n.BASE / lang).as_posix()
        where = f"i18n/{lang}/{source}"
        if source not in sources:
            errors.append(f"{where}: translates no data file; the book translates {', '.join(i18n.DATA_SOURCES)}")
            continue
        raw = load_toml(file, errors)
        if raw is None:
            continue
        for key in set(raw) - OVERLAY_KEYS:
            errors.append(f"{where}: unknown field {key!r}")
        status = raw.get("status", "machine")
        if status not in i18n.STATUSES:
            errors.append(f"{where}: status {status!r} is not one of {', '.join(i18n.STATUSES)}")
        check_people(where, "reviewed_by", raw.get("reviewed_by", []), errors)
        if status == "reviewed" and not raw.get("reviewed_by"):
            errors.append(f"{where}: is reviewed, so reviewed_by names who reviewed it")
        slots = {slot.path: slot for slot in i18n.slots(source, sources[source])}
        seen = set()
        for item in raw.get("text", []):
            if not isinstance(item, dict):
                continue
            path = str(item.get("path", ""))
            for key in set(item) - TEXT_KEYS:
                errors.append(f"{where} [{path}]: unknown field {key!r}")
            if path in seen:
                errors.append(f"{where}: {path} is translated twice")
            seen.add(path)
            if path not in slots:
                errors.append(f"{where}: {path} is not a text of {source}")
                continue
            if not i18n.FINGERPRINT.match(str(item.get("source", ""))):
                errors.append(f"{where} [{path}]: source must be the fingerprint of the English; run tools/translate.py stamp")
            if item.get("status") is not None and item["status"] not in i18n.STATUSES:
                errors.append(f"{where} [{path}]: status {item['status']!r} is not one of {', '.join(i18n.STATUSES)}")
            text = item.get("text", "")
            if not isinstance(text, str) or not text.strip():
                continue
            english = slots[path].english
            if item.get("source") != i18n.fingerprint(english):
                warnings.append(f"{where} [{path}]: stale, the English has changed since; the edition shows the English")
            elif sorted(DIGITS.findall(text)) != sorted(DIGITS.findall(english)):
                errors.append(f"{where} [{path}]: the numbers differ from the English")


def structure(body: str, claims: dict | None = None) -> dict[str, list[str]]:
    """What a translation keeps from its English: citations and cross-references, labels, math,
    claim callouts, reported spans and generated tables."""
    text = book.strip_code_and_comments(body)
    callouts = [re.findall(r"\.([\w-]+)", attrs) for attrs in book.CALLOUT.findall(text)]
    return {
        "citations and cross-references": sorted(book.CITATION.findall(text)),
        "labels": sorted(LABEL_DEFINITION.findall(text)),
        "math": sorted(m.replace("{,}", ".") for m in MATH.findall(text)),
        "claim callouts": sorted(c for classes in callouts for c in classes if c in i18n.CLAIM_CLASSES),
        "reported spans": ["reported"] * len(re.findall(r"\{\.reported\}", text)),
        "generated tables": sorted(match.group(2) for match in i18n.GENERATED_BLOCK.finditer(body)),
    }


def check_pages(lang: str, pages: list, errors: list[str], warnings: list[str]):
    folder = i18n.BASE / lang
    by_path = {page.path: page for page in pages}
    titles = i18n.strings(lang)["claims"]
    for file in sorted(folder.rglob("*.qmd")) if folder.is_dir() else []:
        path = file.relative_to(folder).as_posix()
        where = f"i18n/{lang}/{path}"
        page = by_path.get(path)
        if page is None:
            errors.append(f"{where}: translates no page of the book (_quarto.yml lists the pages)")
            continue
        if not i18n.translatable(page):
            reason = "the papers stay in English" if path.startswith("papers/") else "it is generated from the data overlays"
            errors.append(f"{where}: is not translated by hand: {reason}")
            continue
        translation = i18n.page_translation(lang, page)
        meta = translation.meta
        for key in set(meta) - PAGE_KEYS:
            errors.append(f"{where}: unknown front matter field {key!r}; the edition uses the English page's")
        if meta.get("translation") not in i18n.PAGE_STATUSES:
            errors.append(f"{where}: translation {meta.get('translation')!r} is not one of {', '.join(i18n.PAGE_STATUSES)}")
        if not i18n.FINGERPRINT.match(str(meta.get("source", ""))):
            errors.append(f"{where}: source must be the fingerprint of the English; run tools/translate.py stamp")
        check_people(where, "reviewers", meta.get("reviewers"), errors)
        if meta.get("translation") == "reviewed" and not translation.reviewers:
            errors.append(f"{where}: is reviewed, so reviewers names who reviewed it")
        if translation.state == "stale":
            warnings.append(f"{where}: stale, the English has changed since; tools/translate.py changes {lang} {path}")
        for attrs in book.CALLOUT.findall(book.strip_code_and_comments(translation.body)):
            for claim in i18n.CLAIM_CLASSES:
                if f".{claim}" in attrs.split():
                    title = re.search(r'title="([^"]*)"', attrs)
                    if not title or title.group(1) != titles[claim]:
                        errors.append(f'{where}: a .{claim} callout is titled "{titles[claim]}" (i18n/{lang}/strings.toml)')
        # A stale translation follows an older English, so it is compared with nothing.
        if translation.state not in i18n.STATUSES:
            continue
        english, translated = structure(page.body), structure(translation.body)
        for name, items in english.items():
            if items != translated[name]:
                missing = [item for item in dict.fromkeys(items) if items.count(item) > translated[name].count(item)]
                extra = [item for item in dict.fromkeys(translated[name]) if translated[name].count(item) > items.count(item)]
                detail = "; ".join(part for part in (
                    f"missing {', '.join(missing[:3])}" if missing else "",
                    f"not in the English {', '.join(extra[:3])}" if extra else "",
                ) if part)
                errors.append(f"{where}: does not keep the {name} of the English ({detail})")


def check_translations(pages: list, errors: list[str], warnings: list[str]):
    check_languages(errors, warnings)
    parts = list(dict.fromkeys(page.part for page in pages if page.part))
    for lang in i18n.languages():
        if not i18n.LANGUAGE_ID.match(lang):
            continue
        check_strings(lang, parts, errors, warnings)
        check_glossary(lang, errors)
        check_overlays(lang, errors, warnings)
        check_pages(lang, pages, errors, warnings)


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
    check_translations(pages, errors, warnings)
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
        for name in book.CITATION.findall(text):
            prefix = name.split("-", 1)[0]
            if "-" in name and prefix in book.CROSSREF_PREFIXES:
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
