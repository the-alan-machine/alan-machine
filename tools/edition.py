"""Build the book in another language (decision 0014).

    python3 tools/edition.py [LANG...]            write each edition's sources to _i18n/<lang>/
    python3 tools/edition.py --render [LANG...]   and render them with Quarto into _book/<lang>/

Without LANG, every published language of i18n/languages.toml. Render the English book first:
`quarto render` empties _book/. Set QUARTO to the Quarto binary when it is not on the PATH.

An edition is a copy of the repository in which each page is replaced by its translation, under the
English page's front matter, and the generated appendices are written from the data overlays. A
page without a translation keeps its English, and a notice says so; so does a page translated by
machine or whose English has changed since. The English sources are never changed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import generate  # noqa: E402
import i18n  # noqa: E402

OUT = book.ROOT / "_i18n"
IGNORE = shutil.ignore_patterns(".git", "_book", "_i18n", ".quarto", "__pycache__", "*.pyc", ".venv", "node_modules")
TRANSLATING = book.repo_url() + "/blob/main/docs/translating.md"


def split(text: str) -> tuple[str, str]:
    """A page's front matter, as written, and its body."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[: end + 4] + "\n\n", text[end + 4 :].lstrip("\n")
    return "", text


def with_notice(body: str, text: str) -> str:
    """A notice under the page's title: before it, Quarto would no longer read the title."""
    notice = f'::: {{.callout-note .translation appearance="minimal"}}\n{text}\n:::\n'
    heading = re.search(r"^#\s.*$", body, re.M)
    if not heading:
        return notice + "\n" + body
    return body[: heading.end()] + "\n\n" + notice + body[heading.end() :]


def page_notice(state: str, notices: dict, page_path: str) -> str | None:
    english = i18n.edition_url(None, page_path)
    if state == "missing":
        return notices["untranslated"].format(translating=TRANSLATING, english=english)
    if state in ("machine", "stale"):
        return notices[state].format(translating=TRANSLATING, english=english)
    return None


def data_notice(states: list[i18n.State], notices: dict) -> str | None:
    """A generated appendix is translated text by text; say what part of it is not reviewed."""
    if any(item.state in ("missing", "stale") for item in states):
        return notices["data_partial"].format(translating=TRANSLATING)
    if any(item.state == "machine" for item in states):
        return notices["data_machine"].format(translating=TRANSLATING)
    return None


def config(text: str, language: i18n.Language, strings: dict) -> str:
    """The edition's _quarto.yml: its language, address, part titles and links to the others."""
    text = re.sub(r"^lang:\s*\S+", f"lang: {language.tag}", text, flags=re.M)
    text = re.sub(r"^(\s*site-url:\s*)\S+", lambda m: m.group(1) + i18n.edition_url(language.id), text, flags=re.M)
    # The pages are generated already, in the language; tools/generate.py would write them in English.
    text = re.sub(r"^\s*pre-render:.*\n", "", text, flags=re.M)
    # "Edit this page" would open the English source.
    text = re.sub(r"^(\s*repo-actions:\s*)\[.*\]", r"\1[issue]", text, flags=re.M)
    text = re.sub(r'^(\s*author:\s*).*$', lambda m: m.group(1) + json.dumps(strings["edition"]["author"], ensure_ascii=False), text, count=1, flags=re.M)
    for english, translated in strings["parts"].items():
        text = text.replace(f'- part: "{english}"', f"- part: {json.dumps(translated, ensure_ascii=False)}")
    for english, translated in strings["tools"].items():
        text = re.sub(
            r"^(\s*(?:text|aria-label):\s*)" + re.escape(json.dumps(english)) + r"\s*$",
            lambda m: m.group(1) + json.dumps(translated, ensure_ascii=False),
            text,
            flags=re.M,
        )
    return generate.quarto_yml(text, language.id)


def stage(language: i18n.Language) -> Path:
    """Write the sources of an edition to _i18n/<lang>/ and return the folder."""
    dest = OUT / language.id
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(book.ROOT, dest, ignore=IGNORE)
    strings = i18n.strings(language.id)
    notices = strings["notice"]
    pages = book.pages()

    generated, states = generate.translated_outputs(language.id)
    data_of = {
        "appendices/concepts.qmd": states["data/concepts.toml"],
        "appendices/notation.qmd": states["data/notation.toml"],
        "appendices/constants.qmd": states["data/constants.toml"],
    }
    counts = {"reviewed": 0, "machine": 0, "stale": 0, "missing": 0, "english only": 0}
    for page in pages:
        if page.path in generated:
            body = generated[page.path]
            notice = data_notice(data_of[page.path], notices) if page.path in data_of else None
            (dest / page.path).write_text(with_notice(body, notice) if notice else body, encoding="utf-8")
            continue
        front, english = split((book.ROOT / page.path).read_text(encoding="utf-8"))
        if not i18n.translatable(page):
            body, state = with_notice(english, notices["english_only"].format(translating=TRANSLATING)), "english only"
        else:
            translation = i18n.page_translation(language.id, page)
            state = translation.state
            body = english if state == "missing" else translation.body
            notice = page_notice(state, notices, page.path)
            body = with_notice(body, notice) if notice else body
            if page.path == "building-alan/index.qmd":
                body = generate.building_alan_index(pages, body, language.id)
        counts[state] += 1
        (dest / page.path).write_text(front + body, encoding="utf-8")

    yml = dest / "_quarto.yml"
    yml.write_text(config(yml.read_text(encoding="utf-8"), language, strings), encoding="utf-8")
    summary = ", ".join(f"{count} {state}" for state, count in counts.items() if count)
    print(f"{language.id}: wrote {dest.relative_to(book.ROOT)}/ ({len(pages)} pages: {summary})")
    return dest


def render(language: i18n.Language, dest: Path):
    quarto = os.environ.get("QUARTO", "quarto")
    subprocess.run([quarto, "render", "--to", "html"], cwd=dest, check=True)
    target = book.ROOT / "_book" / language.id
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(dest / "_book", target)
    print(f"{language.id}: rendered into {target.relative_to(book.ROOT)}/")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("languages", nargs="*", help="language ids; every published language by default")
    parser.add_argument("--render", action="store_true", help="render each edition into _book/<lang>/")
    args = parser.parse_args(argv)
    registered = i18n.languages()
    unknown = [lang for lang in args.languages if lang not in registered]
    if unknown:
        print(f"error: not in i18n/languages.toml: {', '.join(unknown)}", file=sys.stderr)
        return 1
    chosen = [registered[lang] for lang in args.languages] or i18n.published()
    if not chosen:
        print("no published language")
    for language in chosen:
        dest = stage(language)
        if args.render:
            render(language, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
