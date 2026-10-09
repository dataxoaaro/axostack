#!/usr/bin/env python3
"""Check that every skill reference in this library resolves and is reachable.

    python3 scripts/check-skill-refs.py

Failure classes, one line each on stdout, non-zero exit if any fire:

  dangling    a bold reference to a skill that does not exist; a relative
              link in skills/, README.md, or agents/ whose target does not
              exist; or a backticked path in a skill file that ends in .md,
              starts with playbooks/, principles/, references/, or ../, and
              resolves neither from the file nor from its skill's folder
  anchor      a link's #anchor into a Markdown file that matches no heading
              there. Headings slug GitHub style: lowercase, punctuation other
              than hyphens and spaces dropped, spaces turned into hyphens
  principle   principles are reference files in skills/axo-mode/principles/,
              not skills. Fires on a principle file that axo-mode's
              Principles index does not link, and on a `principle-<name>`
              skill name, which no longer exists
  user-only   a skill body telling the agent to invoke a skill whose
              frontmatter sets `disable-model-invocation: true`. The Skill
              tool refuses those, and refuses replicating them by other
              means, so the instruction is unexecutable. Recommend it to the
              user as `/name` instead.
  frontmatter missing, unparseable, or a `name:` that does not match the
              folder, which stops the skill registering at all
  convention  the `disable-model-invocation` frontmatter flags and the
              user-only list in README.md disagree. The flag is a maintained
              convention, so its membership is written down; without that,
              the next reader has to guess whether a flag was a decision or
              an accident

Stdlib only, so it runs in a checkout with nothing installed.
"""

from __future__ import annotations

import functools
import pathlib
import re
import sys
from collections.abc import Iterator

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
AGENTS = ROOT / "agents"
PRINCIPLES = SKILLS / "axo-mode" / "principles"
INDEX = SKILLS / "axo-mode" / "SKILL.md"

USER_ONLY = re.compile(
    r"<!-- user-only:start -->(.*?)<!-- user-only:end -->", re.DOTALL
)
BOLD = re.compile(r"\*\*([a-z][a-z0-9-]+)\*\*")
LINK = re.compile(r"\]\((?!https?:|mailto:)([^)#]*)(?:#([^)\s]*))?\)")
BACKTICK_PATH = re.compile(
    r"`((?:playbooks/|principles/|references/|\.\./)[^`\s<>*{}]*\.md)`"
)
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
INLINE_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
FENCE = re.compile(r"^\s*```")
OLD_PRINCIPLE = re.compile(r"\bprinciple-[a-z][a-z0-9-]+")
INDEX_LINK = re.compile(r"\]\(principles/([a-z0-9-]+\.md)\)")

Problem = tuple[pathlib.Path, int, str, str]


def load() -> tuple[dict[str, bool], list[Problem]]:
    """Every skill's user-only flag by folder, plus the frontmatter problems."""
    skills: dict[str, bool] = {}
    problems: list[Problem] = []
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        folder = path.parent.name
        head = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
        if not head:
            problems.append((path, 1, "frontmatter", "no frontmatter block"))
            continue
        fields = dict(re.findall(r"^([a-z-]+):\s*(.*)$", head.group(1), re.MULTILINE))
        name = fields.get("name", "").strip().strip("\"'")
        if name != folder:
            problems.append(
                (
                    path,
                    2,
                    "frontmatter",
                    f"name {name!r} does not match folder {folder!r}",
                )
            )
        if not fields.get("description", "").strip():
            problems.append(
                (
                    path,
                    3,
                    "frontmatter",
                    "no description, so the agent cannot route to it",
                )
            )
        skills[folder] = fields.get("disable-model-invocation", "").strip() == "true"
    return skills, problems


def convention(skills: dict[str, bool]) -> list[Problem]:
    """The frontmatter flags and README's user-only list must name the same skills."""
    flagged = {n for n, is_flagged in skills.items() if is_flagged}
    if not README.exists():
        return [
            (
                README,
                1,
                "convention",
                "no README.md to check the user-only list against",
            )
        ]
    block = USER_ONLY.search(README.read_text())
    if not block:
        return [
            (
                README,
                1,
                "convention",
                "no <!-- user-only:start --> block, so the flag's membership is undocumented",
            )
        ]
    listed = set(re.findall(r"`([a-z][a-z0-9-]+)`", block.group(1)))
    line = README.read_text()[: block.start()].count("\n") + 2
    missing = [
        (
            README,
            line,
            "convention",
            f"{name} sets disable-model-invocation but is not in the user-only list",
        )
        for name in sorted(flagged - listed)
    ]
    extra = [
        (
            README,
            line,
            "convention",
            f"{name} is listed as user-only but does not set disable-model-invocation",
        )
        for name in sorted(listed - flagged)
    ]
    return missing + extra


def unfenced(text: str) -> Iterator[tuple[int, str]]:
    """Yield (lineno, line) outside fenced code blocks."""
    inside = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield lineno, line


def slug(heading: str) -> str:
    """GitHub's anchor for a heading: lowercase, punctuation dropped, spaces to hyphens."""
    text = INLINE_LINK.sub(r"\1", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


@functools.cache
def anchors(path: pathlib.Path) -> frozenset[str]:
    """Every heading anchor in a Markdown file, with GitHub's -1, -2 duplicate suffixes."""
    seen: dict[str, int] = {}
    found = set()
    for _, line in unfenced(path.read_text()):
        heading = HEADING.match(line)
        if not heading:
            continue
        base = slug(heading.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.add(f"{base}-{count}" if count else base)
    return frozenset(found)


def link_refs(path: pathlib.Path, lineno: int, line: str) -> list[Problem]:
    """Relative links must point at a file that exists, and a #anchor at a heading."""
    out: list[Problem] = []
    for raw, anchor in LINK.findall(line):
        target = raw.strip()
        if target and "/" not in target and "." not in target:
            continue  # a bare word like (link) or (url) is a template placeholder
        resolved = (path.parent / target).resolve() if target else path
        if not resolved.exists():
            out.append(
                (path, lineno, "dangling", f"link target {target!r} does not exist")
            )
            continue
        if anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
            out.append(
                (
                    path,
                    lineno,
                    "anchor",
                    f"#{anchor} matches no heading in {target or path.name}",
                )
            )
    return out


def backtick_refs(path: pathlib.Path, lineno: int, line: str) -> list[Problem]:
    """A backticked relative .md path must resolve from the file or its skill folder."""
    skill_dir = SKILLS / path.relative_to(SKILLS).parts[0]
    return [
        (path, lineno, "dangling", f"backticked path {ref!r} does not exist")
        for ref in BACKTICK_PATH.findall(line)
        if not (path.parent / ref).is_file() and not (skill_dir / ref).is_file()
    ]


def principle_refs(path: pathlib.Path, lineno: int, line: str) -> list[Problem]:
    """Old `principle-<name>` skill names must not appear; principles are files now."""
    return [
        (
            path,
            lineno,
            "principle",
            f"{name} is not a skill; link the file in skills/axo-mode/principles/ instead",
        )
        for name in OLD_PRINCIPLE.findall(line)
    ]


def principle_index() -> list[Problem]:
    """Every principle file must be linked from axo-mode's Principles index."""
    text = INDEX.read_text()
    section = re.search(
        r"^## Principles\n(.*?)(?=^## )", text, re.DOTALL | re.MULTILINE
    )
    if not section:
        return [
            (
                INDEX,
                1,
                "principle",
                "no ## Principles section to index the principle files",
            )
        ]
    listed = set(INDEX_LINK.findall(section.group(1)))
    return [
        (
            path,
            1,
            "principle",
            f"{path.name} is not linked from axo-mode's Principles index",
        )
        for path in sorted(PRINCIPLES.glob("*.md"))
        if path.name not in listed
    ]


def skill_refs(
    path: pathlib.Path, lineno: int, line: str, skills: dict[str, bool]
) -> list[Problem]:
    """Bold skill references must name a skill the agent is allowed to invoke."""
    owner = path.relative_to(SKILLS).parts[0]
    out: list[Problem] = []
    for ref in BOLD.findall(line):
        if ref in skills:
            if skills[ref] and ref != owner:
                out.append(
                    (
                        path,
                        lineno,
                        "user-only",
                        f"**{ref}** is user-run; recommend `/{ref}` instead",
                    )
                )
        elif f"**{ref}** skill" in line:
            out.append(
                (path, lineno, "dangling", f"**{ref}** is not a skill in this library")
            )
    return out


def main() -> int:
    """Run every check, print one line per problem, and return the exit code."""
    skills, problems = load()
    problems.extend(convention(skills))
    problems.extend(principle_index())

    for path in sorted(SKILLS.rglob("*.md")):
        for lineno, line in unfenced(path.read_text()):
            problems.extend(principle_refs(path, lineno, line))
            problems.extend(skill_refs(path, lineno, line, skills))
            problems.extend(link_refs(path, lineno, line))
            problems.extend(backtick_refs(path, lineno, line))

    for path in [README, *sorted(AGENTS.glob("*.md"))]:
        for lineno, line in unfenced(path.read_text()):
            problems.extend(principle_refs(path, lineno, line))
            problems.extend(link_refs(path, lineno, line))

    for path, lineno, kind, msg in problems:
        rel = path.relative_to(ROOT)
        print(f"{rel}:{lineno}: {kind}: {msg}")

    counts: dict[str, int] = {}
    for _, _, kind, _ in problems:
        counts[kind] = counts.get(kind, 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "none"
    print(f"\n{len(skills)} skills checked. Problems: {summary}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
