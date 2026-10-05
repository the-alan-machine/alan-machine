"""Who has to approve a pull request, and whether they have; and the part of the book an issue is
about.

    python3 tools/moderation.py pr --dir .moderation
    python3 tools/moderation.py issue --body-file body.md

`pr` reads what .github/workflows/moderation.yml fetched into the directory: pr.json (the pull
request), files.jsonl and reviews.jsonl (the GitHub API's changed files and reviews, one JSON
object per line) and head/, the pull request's version of each page and of references.bib it
changes. It writes result.json (state, description, reviewers to request) and comment.md. The
maintainers, moderators, curators and language maintainers come from this checkout, the main
branch, so a pull request that adds its author to a list does not make the author an approver. The
pull request's files are read as text, never run.

`issue` reads the body of an issue opened from a form and prints, as JSON, the labels of the parts
and the language it names and the people to mention.

The rules are in GOVERNANCE.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book  # noqa: E402
import i18n  # noqa: E402
from generate import LIVING_REVIEW_BEGIN, LIVING_REVIEW_END  # noqa: E402

# The folder of a chapter, interlude, living review or paper: everything in it belongs to its page.
PAGE_DIR = re.compile(r"^((?:chapters|interludes|building-alan|papers)/[A-Za-z0-9._-]+)/")
TECH_DATA = re.compile(r"^data/technologies/([A-Za-z0-9._-]+)\.toml$")
# A translation (decision 0014): a translated page, a data overlay, or the words and terms of a language.
TRANSLATION_FILE = re.compile(r"^i18n/([a-z0-9-]+)/.+$")
BIB = "references.bib"
BIB_ENTRY = re.compile(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", re.M)
LIVING_REVIEW_TABLE = re.compile(re.escape(LIVING_REVIEW_BEGIN) + r".*?" + re.escape(LIVING_REVIEW_END), re.S)
MARKER = "<!-- moderation -->"
MAX_DESCRIPTION = 140  # GitHub's limit for a commit status description
MAX_LISTED = 6
MAX_REQUESTED = 15
DECISIVE = ("APPROVED", "CHANGES_REQUESTED", "DISMISSED")
# Issue form fields that name a place in the book.
# "Dossier" is the label of issues opened before the Building Alan dossiers became living reviews.
LOCATION_FIELDS = ("Location", "Living review", "Dossier", "Where it belongs", "Related chapters or papers")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def handles(values) -> list[str]:
    """The valid GitHub handles in a list, in order, without repeats (case-insensitive)."""
    seen, found = set(), []
    for value in values if isinstance(values, list) else []:
        if isinstance(value, str) and book.GITHUB_HANDLE.match(value) and value.lower() not in seen:
            seen.add(value.lower())
            found.append(value)
    return found


def mention(people) -> str:
    return ", ".join(f"@{person}" for person in sorted(people, key=str.lower))


def either(people) -> str:
    names = [f"@{person}" for person in sorted(people, key=str.lower)]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " or " + names[-1]


def listed(items: list[str]) -> str:
    shown = ", ".join(f"`{item}`" for item in items[:MAX_LISTED])
    return shown + (f" and {len(items) - MAX_LISTED} more" if len(items) > MAX_LISTED else "")


def bib_texts(text: str) -> dict[str, str]:
    """Citation key -> the text of its entry, to tell which entries a pull request changes."""
    starts = [m for m in BIB_ENTRY.finditer(text) if m.group(1).lower() not in {"comment", "string", "preamble"}]
    found = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        found[match.group(2)] = text[match.start() : end].strip()
    return found


def cites(text: str, key: str) -> bool:
    return re.search(r"(?<![\w@./])@" + re.escape(key) + r"(?![\w:.#$%&+?<>~/-]*[\w])", text) is not None


@dataclass
class Group:
    """Changes that the same people can approve."""

    role: str  # "curators and moderators", "<language> maintainers" or "maintainers"
    people: list[str]  # who can approve, without the author
    covers: list[str] = field(default_factory=list)
    approved_by: list[str] = field(default_factory=list)
    waived: bool = False

    @property
    def done(self) -> bool:
        return self.waived or bool(self.approved_by)


class PullRequest:
    def __init__(self, directory: Path):
        self.dir = directory
        pr = json.loads((directory / "pr.json").read_text(encoding="utf-8"))
        self.number = pr["number"]
        self.author = pr["user"]["login"]
        self.head_sha = pr["head"]["sha"]
        self.maintainers = handles(book.maintainers())
        self.moderators = book.part_moderators()
        self.languages = i18n.languages()
        self.pages = {page.path: page for page in book.pages()}

        self.changes: list[tuple[str, str]] = []
        for item in read_jsonl(directory / "files.jsonl"):
            if item.get("status") == "renamed" and item.get("previous_filename"):
                self.changes.append((item["previous_filename"], "removed"))
                self.changes.append((item["filename"], "added"))
            else:
                self.changes.append((item["filename"], item.get("status", "modified")))

        latest: dict[str, dict] = {}
        self.reviewed: set[str] = set()
        for review in sorted(read_jsonl(directory / "reviews.jsonl"), key=lambda r: r.get("submitted_at") or ""):
            login = (review.get("user") or {}).get("login")
            if not login:
                continue
            self.reviewed.add(login.lower())
            if review.get("state") in DECISIVE:
                latest[login.lower()] = review
        self.approved = {login for login, review in latest.items() if review["state"] == "APPROVED"}
        self.approved_on_head = {
            login for login, review in latest.items() if review["state"] == "APPROVED" and review.get("commit_id") == self.head_sha
        }

        self.groups: dict[tuple[str, frozenset[str]], Group] = {}
        self.failures: list[str] = []
        self.waiting: list[tuple[str, str]] = []  # (what, who)

    def head_text(self, relative: str) -> str | None:
        path = self.dir / "head" / relative
        if not path.is_file():
            return None
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None

    def base_text(self, relative: str) -> str:
        path = book.ROOT / relative
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def page_of(self, name: str) -> str | None:
        """The page (as listed on main) a changed file belongs to, or None."""
        if name in self.pages:
            return name
        match = PAGE_DIR.match(name)
        if match and f"{match.group(1)}/index.qmd" in self.pages:
            return f"{match.group(1)}/index.qmd"
        return None

    def reviewers_of(self, path: str) -> list[str]:
        """Curators of a page (as on main) and moderators of its part."""
        page = self.pages[path]
        curators = page.meta.get("curators")
        return handles((curators if isinstance(curators, list) else []) + self.moderators.get(page.part or "", []))

    def add(self, people: list[str], what: str, role: str = "curators and moderators"):
        others = [person for person in people if person.lower() != self.author.lower()]
        if others:
            approvers = others
        else:
            role, approvers = "maintainers", [m for m in self.maintainers if m.lower() != self.author.lower()]
        key = (role, frozenset(person.lower() for person in approvers))
        group = self.groups.setdefault(key, Group(role=role, people=approvers))
        if what not in group.covers:
            group.covers.append(what)

    def check_review(self, path: str, head: dict, people: list[str]):
        """A living review whose last_reviewed changes names who reviewed it, and they approve."""
        base = self.pages[path].meta
        if not head.get("last_reviewed") or head.get("last_reviewed") == base.get("last_reviewed"):
            return
        who = head.get("reviewed_by")
        allowed = people or self.maintainers
        if not isinstance(who, str) or not book.GITHUB_HANDLE.match(who):
            self.failures.append(f"{path}: last_reviewed changed, so reviewed_by names the GitHub handle of the reviewer")
        elif who.lower() not in {person.lower() for person in allowed}:
            self.failures.append(f"{path}: @{who} does not curate this living review or moderate Building Alan")
        elif who.lower() != self.author.lower() and who.lower() not in self.approved_on_head:
            self.waiting.append((f"`{path}` is reviewed by @{who}, who approves the last commit", who))

    def bib_change(self, status: str):
        """Each changed entry goes to whoever covers a page that cites it, before or after."""
        before = bib_texts(self.base_text(BIB))
        after = bib_texts(self.head_text(BIB) or "") if status != "removed" else {}
        changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
        for key in changed:
            people: list[str] = []
            for path, page in self.pages.items():
                if cites(page.body, key) or cites(self.head_text(path) or "", key):
                    people += self.reviewers_of(path)
            self.add(handles(people), f"{BIB} ({key})")
        if not changed:
            self.add([], BIB)  # comments or layout only

    def evaluate(self) -> dict:
        for name, status in self.changes:
            if name in book.GENERATED_PAGES:
                continue
            if name == BIB:
                self.bib_change(status)
                continue
            if (match := TRANSLATION_FILE.match(name)) and match.group(1) in self.languages:
                # Translators approve translations; the English they follow was approved already.
                lang = self.languages[match.group(1)]
                self.add(handles(lang.maintainers), name, role=f"{lang.english_name} maintainers")
                continue
            if match := TECH_DATA.match(name):
                people: list[str] = []
                for path, page in self.pages.items():
                    if page.kind == "living-review" and page.meta.get("technology") == match.group(1):
                        people += self.reviewers_of(path)
                self.add(handles(people), name)
                continue
            path = self.page_of(name)
            if path is None:
                # Anything else, including a new page: its place in _quarto.yml needs a maintainer.
                self.add([], name)
                continue
            if path == "building-alan/index.qmd" and status != "removed":
                head = self.head_text(path)
                if head is not None and LIVING_REVIEW_TABLE.sub("", head) == LIVING_REVIEW_TABLE.sub("", self.base_text(path)):
                    continue  # only the living review table, which tools/generate.py writes
            people = self.reviewers_of(path)
            self.add(people, name)
            if name == path and status != "removed" and (text := self.head_text(path)) is not None:
                head, _ = book.parse_front_matter(text)
                before = handles(self.pages[path].meta.get("curators"))
                after = handles(head.get("curators"))
                if sorted(p.lower() for p in before) != sorted(p.lower() for p in after):
                    self.add([], f"{name} (curators)")
                if self.pages[path].kind == "living-review":
                    self.check_review(path, head, people)

        for group in self.groups.values():
            group.approved_by = [person for person in group.people if person.lower() in self.approved]
            group.waived = group.role == "maintainers" and not group.people

        if not self.maintainers:
            self.failures.insert(0, "governance.toml lists no maintainers")
        pending = [group for group in self.groups.values() if not group.done]
        if self.failures:
            state, description = "failure", self.failures[0]
        elif pending or self.waiting:
            parts = [either(group.people) for group in pending] + [f"@{who}" for _, who in self.waiting]
            state, description = "pending", "Waiting for " + "; ".join(dict.fromkeys(parts))
        elif not self.groups:
            state, description = "success", "Only generated pages changed; tools/check.py compares them with their sources"
        elif all(group.waived for group in self.groups.values()):
            state, description = "success", "No reviewer but the author, who is the only maintainer"
        else:
            state, description = "success", "Approved by someone who covers each change"
        if len(description) > MAX_DESCRIPTION:
            description = description[: MAX_DESCRIPTION - 3].rstrip() + "..."

        # Ask everyone who can unblock a pending group and has not reviewed yet, and ask again the
        # person who reviewed a living review, whose approval has to be on the last commit.
        request = []
        candidates = [(p, False) for group in pending for p in group.people] + [(who, True) for _, who in self.waiting]
        for person, again in candidates:
            low = person.lower()
            if low != self.author.lower() and (again or low not in self.reviewed) and low not in {r.lower() for r in request}:
                request.append(person)
        return {
            "state": state,
            "description": description,
            "head_sha": self.head_sha,
            "request": request[:MAX_REQUESTED],
        }

    def comment(self, result: dict) -> str:
        lines = [MARKER, "### Moderation", ""]
        if result["state"] == "success":
            lines += ["Every change is covered.", ""]
        if self.groups:
            lines += ["| Changes | Who can approve | Status |", "|---|---|---|"]
        else:
            lines += ["Only generated pages changed."]
        for group in self.groups.values():
            if group.waived:
                who, status = "the author, the only maintainer", "no other reviewer"
            else:
                who = f"{mention(group.people)} ({group.role})"
                status = f"approved by {mention(group.approved_by)}" if group.approved_by else "waiting"
            lines.append(f"| {listed(group.covers)} | {who} | {status} |")
        if self.failures or self.waiting:
            lines += ["", "Yearly reviews of living reviews:", ""]
            lines += [f"- {failure}" for failure in self.failures]
            lines += [f"- {what}." for what, _ in self.waiting]
        lines += [
            "",
            f"The rules are in [GOVERNANCE.md]({book.governance_url()}). The moderation check updates this comment.",
        ]
        return "\n".join(lines) + "\n"


FORM_HEADING = re.compile(r"^###[ \t]+(.+?)[ \t]*$", re.M)


def form_fields(body: str) -> dict[str, str]:
    """The answers of an issue form: GitHub writes each one under a '### Label' heading."""
    parts = FORM_HEADING.split(body or "")
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def issue_places(body: str) -> dict:
    """The pages an issue names, by folder (chapters/landauer) or title, their parts and people,
    and the language a translation issue names, with its maintainers."""
    fields = form_fields(body)
    text = "\n".join(fields.get(name, "") for name in LOCATION_FIELDS).lower()
    moderators = book.part_moderators()
    labels: dict[str, str] = {}
    people: list[str] = []
    for page in book.pages():
        if page.kind not in ("chapter", "interlude", "living-review", "paper"):
            continue
        folder = page.path.rsplit("/", 1)[0].lower()
        title = page.title.lower()
        if folder in text or re.search(r"(?<!\w)" + re.escape(title) + r"(?!\w)", text):
            curators = page.meta.get("curators")
            people += curators if isinstance(curators, list) else []
            if page.part:
                labels[f"part: {book.part_slug(page.part)}"] = page.part
                people += moderators.get(page.part, [])
    named = fields.get("Language", "").strip().strip("`").lower()
    for lang in i18n.languages().values() if named else []:
        if named in (lang.id, lang.tag.lower(), lang.name.lower(), lang.english_name.lower()):
            labels[f"lang: {lang.id}"] = lang.english_name
            people += lang.maintainers
    return {
        "labels": [{"name": name, "description": title} for name, title in labels.items()],
        "mention": handles(people),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    pr = sub.add_parser("pr", help="evaluate a pull request fetched by the moderation workflow")
    pr.add_argument("--dir", type=Path, required=True)
    issue = sub.add_parser("issue", help="find the parts of the book an issue opened from a form names")
    issue.add_argument("--body-file", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "issue":
        print(json.dumps(issue_places(args.body_file.read_text(encoding="utf-8"))))
        return 0

    request = PullRequest(args.dir)
    result = request.evaluate()
    comment = request.comment(result)
    (args.dir / "result.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    (args.dir / "comment.md").write_text(comment, encoding="utf-8")
    print(f"{result['state']}: {result['description']}")
    print(comment)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
