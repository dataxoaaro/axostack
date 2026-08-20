#!/usr/bin/env python3
"""Check that every skill reference in this library resolves and is reachable.

    python3 scripts/check-skill-refs.py

Four failure classes, one line each on stdout, non-zero exit if any fire:

  dangling    a bold reference to a skill that does not exist
  bare-stem   a principle cited without its `principle-` prefix, so it names
              nothing; the skill is `principle-prove-it-works`, not
              `prove-it-works`
  user-only   a skill body telling the agent to invoke a skill whose
              frontmatter sets `disable-model-invocation: true`. The Skill
              tool refuses those, and refuses replicating them by other
              means, so the instruction is unexecutable. Recommend it to the
              user as `/name` instead.
  frontmatter missing, unparseable, or a `name:` that does not match the
              folder, which stops the skill registering at all

Stdlib only, so it runs in a checkout with nothing installed.
"""

import pathlib
import re
import sys

SKILLS = pathlib.Path(__file__).resolve().parent.parent / "skills"

BOLD = re.compile(r"\*\*([a-z][a-z0-9-]+)\*\*")
SLASH = re.compile(r"`/([a-z][a-z0-9-]+)`")
LINK = re.compile(r"\]\((?!https?:)([^)#]+)")
FENCE = re.compile(r"^\s*```")


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


def unfenced(text):
    """Yield (lineno, line) outside fenced code blocks."""
    inside = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield n, line


def main():
    skills, problems = load()
    stems = {n[len("principle-"):]: n for n in skills if n.startswith("principle-")}

    for path in sorted(SKILLS.rglob("*.md")):
        owner = path.relative_to(SKILLS).parts[0]
        text = path.read_text()

        for n, line in unfenced(text):
            for ref in BOLD.findall(line):
                if ref in skills:
                    if skills[ref] and ref != owner:
                        problems.append((path, n, "user-only", f"**{ref}** is user-run; recommend `/{ref}` instead"))
                elif ref in stems:
                    problems.append((path, n, "bare-stem", f"**{ref}** names nothing; use **{stems[ref]}**"))
                elif f"**{ref}** skill" in line:
                    problems.append((path, n, "dangling", f"**{ref}** is not a skill in this library"))

            for ref in SLASH.findall(line):
                if ref not in skills and ref in stems:
                    problems.append((path, n, "bare-stem", f"`/{ref}` names nothing; use **{stems[ref]}**"))

            for target in LINK.findall(line):
                target = target.strip()
                if "/" not in target and "." not in target:
                    continue  # a bare word like (link) or (url) is a template placeholder
                if not (path.parent / target).exists():
                    problems.append((path, n, "dangling", f"link target {target!r} does not exist"))

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
