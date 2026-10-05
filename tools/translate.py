"""Work on a translation of the book (decision 0014, docs/translating.md).

    python3 tools/translate.py status [--lang pt] [--list stale|missing|machine]
                                      how much of each language is translated, and what is stale
    python3 tools/translate.py template pt FILE... | --all
                                      start the translation of a page, or add the texts a data
                                      overlay lacks with an empty translation
    python3 tools/translate.py show pt FILE
                                      each English text of a data file next to its translation
    python3 tools/translate.py changes pt PAGE
                                      what changed in the English of a page since it was translated
    python3 tools/translate.py stamp pt FILE... [--path PATH]
                                      after updating a stale translation, record the English it
                                      now follows

FILE is a page (chapters/landauer/index.qmd), a data file (data/concepts.toml) or its translation
under i18n/<lang>/. The papers and the generated appendices are not translated by hand.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import i18n  # noqa: E402


def known() -> tuple[dict[str, book.Page], dict[str, dict]]:
    return {page.path: page for page in book.pages() if i18n.translatable(page)}, i18n.sources()


def resolve(lang: str, names: list[str], every: bool) -> list[str]:
    pages, data = known()
    if every:
        return list(pages) + list(data)
    found = []
    for name in names:
        path = Path(name).resolve()
        relative = path.relative_to(book.ROOT).as_posix() if path.is_relative_to(book.ROOT) else name
        prefix = f"i18n/{lang}/"
        if relative.startswith(prefix):
            relative = relative[len(prefix) :]
        if relative not in pages and relative not in data:
            raise SystemExit(f"{name}: not a page or data file the book translates (papers and generated appendices are not)")
        found.append(relative)
    return found


def language(lang: str) -> i18n.Language:
    registered = i18n.languages()
    if lang not in registered:
        raise SystemExit(f"{lang}: not in i18n/languages.toml (registered: {', '.join(registered) or 'none'})")
    return registered[lang]


def status(args) -> int:
    langs = [language(args.lang)] if args.lang else list(i18n.languages().values())
    pages, data = known()
    for lang in langs:
        rows = {"pages": dict.fromkeys(("total", "reviewed", "machine", "stale", "missing"), 0)}
        rows["data texts"] = dict(rows["pages"])
        listed = []
        for translation in i18n.page_translations(lang.id, list(pages.values())):
            rows["pages"][translation.state] += 1
            rows["pages"]["total"] += 1
            if args.list == translation.state:
                listed.append(f"  {translation.path}")
        for source, english in data.items():
            for item in i18n.states(lang.id, source, english):
                rows["data texts"][item.state] += 1
                rows["data texts"]["total"] += 1
                if args.list == item.state:
                    listed.append(f"  {source}  {item.slot.path}")
        print(f"{lang.english_name} ({lang.id}), maintained by {', '.join('@' + m for m in lang.maintainers) or 'nobody'}")
        print(f"  {'':11} {'total':>6} {'reviewed':>9} {'machine':>8} {'stale':>6} {'missing':>8}")
        for name, row in rows.items():
            print(f"  {name:11} {row['total']:>6} {row['reviewed']:>9} {row['machine']:>8} {row['stale']:>6} {row['missing']:>8}")
        if args.list:
            print(f"\n{args.list}:" if listed else f"\nnothing {args.list}")
            print("\n".join(listed))
    return 0


def template(args) -> int:
    language(args.lang)
    pages, data = known()
    for source in resolve(args.lang, args.files, args.all):
        if source in pages:
            file = i18n.page_file(args.lang, source)
            if file.is_file():
                print(f"{file.relative_to(book.ROOT)}: exists, left as it is")
                continue
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(i18n.template_page(pages[source]), encoding="utf-8")
            print(f"{file.relative_to(book.ROOT)}: the English to translate in place")
            continue
        file = i18n.overlay_path(args.lang, source)
        overlay = i18n.load_overlay(file) if file.is_file() else i18n.Overlay(file=file)
        present = overlay.by_path()
        added = 0
        for slot in i18n.slots(source, data[source]):
            if slot.path not in present:
                overlay.entries.append(i18n.Entry(path=slot.path, source=i18n.fingerprint(slot.english), text=""))
                added += 1
        if added or file.is_file():
            i18n.write_overlay(args.lang, source, data[source], overlay)
            print(f"{file.relative_to(book.ROOT)}: {added} texts added")
    return 0


def show(args) -> int:
    language(args.lang)
    pages, data = known()
    for source in resolve(args.lang, args.files, False):
        if source in pages:
            translation = i18n.page_translation(args.lang, pages[source])
            print(f"[{translation.state}] {source}: open it next to {translation.file.relative_to(book.ROOT)}")
            continue
        for item in i18n.states(args.lang, source, data[source]):
            print(f"[{item.state}] {item.slot.path}")
            print(f"  en: {' '.join(item.slot.english.split())}")
            if item.entry and item.entry.text.strip():
                print(f"  {args.lang}: {' '.join(item.entry.text.split())}")
            print()
    return 0


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=book.ROOT, capture_output=True, text=True, check=True).stdout


def changes(args) -> int:
    """Find the version of the English page the translation follows and show the diff since."""
    language(args.lang)
    pages, _ = known()
    for source in resolve(args.lang, args.files, False):
        if source not in pages:
            print(f"{source}: changes works on pages; for data, show prints the English as it is now", file=sys.stderr)
            continue
        translation = i18n.page_translation(args.lang, pages[source])
        followed = translation.meta.get("source")
        if translation.state != "stale":
            print(f"{source}: {translation.state}, nothing to compare")
            continue
        for commit in git("log", "--format=%H", "--", source).split():
            _, body = book.parse_front_matter(git("show", f"{commit}:{source}"))
            if i18n.page_fingerprint(body) == followed:
                print(git("diff", commit, "--", source), end="")
                break
        else:
            print(f"{source}: no commit has the English with fingerprint {followed}; compare the files by hand")
    return 0


def stamp(args) -> int:
    language(args.lang)
    pages, data = known()
    for source in resolve(args.lang, args.files, False):
        if source in pages:
            file = i18n.page_file(args.lang, source)
            if not file.is_file():
                print(f"{source}: not translated", file=sys.stderr)
                continue
            text = file.read_text(encoding="utf-8")
            file.write_text(i18n.set_meta(text, "source", i18n.page_fingerprint(pages[source].body)), encoding="utf-8")
            print(f"{file.relative_to(book.ROOT)}: stamped")
            continue
        file = i18n.overlay_path(args.lang, source)
        if not file.is_file():
            print(f"{source}: no overlay", file=sys.stderr)
            continue
        overlay = i18n.load_overlay(file)
        english = {slot.path: slot.english for slot in i18n.slots(source, data[source])}
        changed = 0
        for entry in overlay.entries:
            if entry.path in english and (not args.path or entry.path in args.path):
                new = i18n.fingerprint(english[entry.path])
                if entry.source != new:
                    entry.source = new
                    changed += 1
        i18n.write_overlay(args.lang, source, data[source], overlay)
        print(f"{file.relative_to(book.ROOT)}: {changed} texts stamped")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("status", help="coverage of each language")
    p.add_argument("--lang")
    p.add_argument("--list", choices=["stale", "missing", "machine"])
    p = sub.add_parser("template", help="start a page, or add the texts a data overlay lacks")
    p.add_argument("lang")
    p.add_argument("files", nargs="*")
    p.add_argument("--all", action="store_true", help="every page and data file")
    p = sub.add_parser("show", help="English and translation side by side")
    p.add_argument("lang")
    p.add_argument("files", nargs="+")
    p = sub.add_parser("changes", help="the English diff since a page was translated")
    p.add_argument("lang")
    p.add_argument("files", nargs="+")
    p = sub.add_parser("stamp", help="record the English a translation now follows")
    p.add_argument("lang")
    p.add_argument("files", nargs="+")
    p.add_argument("--path", action="append", help="only this text of a data overlay; repeat for more")
    args = parser.parse_args(argv)
    if args.command == "template" and not (args.files or args.all):
        parser.error("template needs FILE... or --all")
    commands = {"status": status, "template": template, "show": show, "changes": changes, "stamp": stamp}
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
