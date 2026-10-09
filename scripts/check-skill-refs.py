#!/usr/bin/env python3
"""Check that every skill reference in this library resolves and is reachable.

    python3 scripts/check-skill-refs.py

Failure classes, one line each on stdout, non-zero exit if any fire:

  dangling    a bold reference to a skill that does not exist, or a relative
              link whose target does not exist
  principle   principles are reference files in skills/axo-mode/principles/,
              not skills. Fires on a link into that folder that does not
              resolve, on a principle file that axo-mode's Principles index
              does not link, and on a `principle-<name>` skill name, which
              no longer exists
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

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
AGENTS = ROOT / "agents"
PRINCIPLES = SKILLS / "axo-mode" / "principles"
INDEX = SKILLS / "axo-mode" / "SKILL.md"

USER_ONLY = re.compile(r"<!-- user-only:start -->(.*?)<!-- user-only:end -->", re.S)
BOLD = re.compile(r"\*\*([a-z][a-z0-9-]+)\*\*")
SLASH = re.compile(r"`/([a-z][a-z0-9-]+)`")
LINK = re.compile(r"\]\((?!https?:)([^)#]+)")
FENCE = re.compile(r"^\s*```")
OLD_PRINCIPLE = re.compile(r"\bprinciple-[a-z][a-z0-9-]+")
INDEX_LINK = re.compile(r"\]\(principles/([a-z0-9-]+\.md)\)")


def load():
    """Every skill's frontmatter, plus the problems found reading it."""
    skills, problems = {}, []
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        folder = path.parent.name
        head = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
        if not head:
            problems.append((path, 1, "frontmatter", "no frontmatter block"))
            continue
        fields = dict(
            re.findall(r"^([a-z-]+):\s*(.*)$", head.group(1), re.M)
        )
        name = fields.get("name", "").strip().strip("\"'")
        if name != folder:
            problems.append(
                (path, 2, "frontmatter", f"name {name!r} does not match folder {folder!r}")
            )
        if not fields.get("description", "").strip():
            problems.append((path, 3, "frontmatter", "no description, so the agent cannot route to it"))
        skills[folder] = fields.get("disable-model-invocation", "").strip() == "true"
    return skills, problems


def convention(skills):
    """The frontmatter flags and README's user-only list must name the same skills."""
    flagged = {n for n, is_flagged in skills.items() if is_flagged}
    if not README.exists():
        return [(README, 1, "convention", "no README.md to check the user-only list against")]
    block = USER_ONLY.search(README.read_text())
    if not block:
        return [(README, 1, "convention",
                 "no <!-- user-only:start --> block, so the flag's membership is undocumented")]
    listed = set(re.findall(r"`([a-z][a-z0-9-]+)`", block.group(1)))
    line = README.read_text()[: block.start()].count("\n") + 2
    out = []
    for name in sorted(flagged - listed):
        out.append((README, line, "convention",
                    f"{name} sets disable-model-invocation but is not in the user-only list"))
    for name in sorted(listed - flagged):
        out.append((README, line, "convention",
                    f"{name} is listed as user-only but does not set disable-model-invocation"))
    return out


def unfenced(text):
    """Yield (lineno, line) outside fenced code blocks."""
    inside = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield n, line


def principle_refs(path, n, line):
    """Links into the principles folder must resolve, and old skill names must not appear."""
    out = []
    for name in OLD_PRINCIPLE.findall(line):
        out.append((path, n, "principle",
                    f"{name} is not a skill; link the file in skills/axo-mode/principles/ instead"))
    for target in LINK.findall(line):
        resolved = (path.parent / target.strip()).resolve()
        if PRINCIPLES.resolve() in resolved.parents and not resolved.is_file():
            out.append((path, n, "principle", f"link target {target.strip()!r} is not a principle file"))
    return out


def principle_index():
    """Every principle file must be linked from axo-mode's Principles index."""
    text = INDEX.read_text()
    section = re.search(r"^## Principles\n(.*?)(?=^## )", text, re.S | re.M)
    if not section:
        return [(INDEX, 1, "principle", "no ## Principles section to index the principle files")]
    listed = set(INDEX_LINK.findall(section.group(1)))
    return [(path, 1, "principle", f"{path.name} is not linked from axo-mode's Principles index")
            for path in sorted(PRINCIPLES.glob("*.md")) if path.name not in listed]


def main():
    skills, problems = load()
    problems.extend(convention(skills))
    problems.extend(principle_index())

    for path in sorted(SKILLS.rglob("*.md")):
        owner = path.relative_to(SKILLS).parts[0]
        text = path.read_text()

        for n, line in unfenced(text):
            problems.extend(principle_refs(path, n, line))

            for ref in BOLD.findall(line):
                if ref in skills:
                    if skills[ref] and ref != owner:
                        problems.append((path, n, "user-only", f"**{ref}** is user-run; recommend `/{ref}` instead"))
                elif f"**{ref}** skill" in line:
                    problems.append((path, n, "dangling", f"**{ref}** is not a skill in this library"))

            for target in LINK.findall(line):
                target = target.strip()
                if "/" not in target and "." not in target:
                    continue  # a bare word like (link) or (url) is a template placeholder
                if PRINCIPLES.resolve() in (path.parent / target).resolve().parents:
                    continue  # principle_refs reports these
                if not (path.parent / target).exists():
                    problems.append((path, n, "dangling", f"link target {target!r} does not exist"))

    for path in [README, *sorted(AGENTS.glob("*.md"))]:
        for n, line in unfenced(path.read_text()):
            problems.extend(principle_refs(path, n, line))

    for path, n, kind, msg in problems:
        rel = path.relative_to(SKILLS.parent)
        print(f"{rel}:{n}: {kind}: {msg}")

    counts = {}
    for _, _, kind, _ in problems:
        counts[kind] = counts.get(kind, 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "none"
    print(f"\n{len(skills)} skills checked. Problems: {summary}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
