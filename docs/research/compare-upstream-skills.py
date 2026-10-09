#!/usr/bin/env python3
"""Print a file-level audit from local full-history upstream clones; never modify skills."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def tree(repo, revision, directory):
    result = {}
    for record in git(repo, "ls-tree", "-rz", revision, "--", directory).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        relative = str(Path(path.decode()).relative_to(directory))
        result[relative] = meta.decode().split()[2]
    return result


def worktree(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name != ".DS_Store":
            content = path.read_bytes()
            blob = b"blob " + str(len(content)).encode() + b"\0" + content
            result[str(path.relative_to(directory))] = hashlib.sha1(blob).hexdigest()
    return result


def changes(before, after):
    return {
        name: "added"
        if name not in before
        else "deleted"
        if name not in after
        else "modified"
        for name in sorted(before.keys() | after.keys())
        if before.get(name) != after.get(name)
    }


def skill_paths(repo, revision):
    paths = git(repo, "ls-tree", "-r", "--name-only", revision).decode().splitlines()
    return {
        Path(p).parent.name: str(Path(p).parent)
        for p in paths
        if p.startswith("skills/") and p.endswith("/SKILL.md")
    }


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("matt", type=Path)
parser.add_argument("cursor", type=Path)
parser.add_argument("--matt-ref", default="HEAD")
parser.add_argument("--cursor-ref", default="HEAD")
parser.add_argument(
    "--matt-base",
    default="b0618bc436ad893b3c5e84e55fba86586d34a404",
    help="last audited Matt revision",
)
parser.add_argument(
    "--cursor-base",
    default="ccb5507cec1546dc88135c1139c811e6c59115ba",
    help="last audited pstack revision",
)
parser.add_argument(
    "--cloudflare", type=Path, help="clone of cloudflare/security-audit-skill"
)
parser.add_argument("--cloudflare-ref", default="HEAD")
parser.add_argument(
    "--cloudflare-base",
    default="c1c8a8c1471069fb0e188eeaff69b8e8db6564a8",
    help="last audited security-audit-skill revision",
)
parser.add_argument("--pony", type=Path, help="clone of DietrichGebert/ponytail")
parser.add_argument("--pony-ref", default="HEAD")
parser.add_argument(
    "--pony-base",
    default="c982cd411abb53323c4baa1baa3c2f020b8d0b08",
    help="last audited ponytail revision",
)
args = parser.parse_args()
local = Path(__file__).resolve().parents[2]
sources = {
    "matt": (args.matt, args.matt_base, args.matt_ref),
    "pstack": (args.cursor, args.cursor_base, args.cursor_ref),
}
if args.cloudflare:
    sources["cloudflare"] = (args.cloudflare, args.cloudflare_base, args.cloudflare_ref)
if args.pony:
    sources["pony"] = (args.pony, args.pony_base, args.pony_ref)
cloudflare_names = {"security-audit"}
metadata = {
    key: {
        "base": git(repo, "rev-parse", base).decode().strip(),
        "head": git(repo, "rev-parse", head).decode().strip(),
    }
    for key, (repo, base, head) in sources.items()
}
matt_base = skill_paths(args.matt, metadata["matt"]["base"])
matt_head = skill_paths(args.matt, metadata["matt"]["head"])
pstack_names = {
    "architect",
    "arena",
    "benchmark-checklist",
    "blast-radius",
    "recall",
    "figure-it-out",
    "how",
    "no-comments",
    "show-me-your-work",
    "technical-writing",
    "unslop",
    "why",
}
# Upstream skills folded into a local skill. The local file no longer matches them
# file for file, so only their upstream changes are reported, for porting by hand.
merged = {
    "arena": [("pstack", "pstack/skills/swarm")],
    "architect": [("pstack", "pstack/skills/principle-exhaust-the-design-space")],
    "axo-mode": [
        ("pstack", "pstack/skills/principle-guard-the-context-window"),
        ("pstack", "pstack/skills/principle-never-block-on-the-human"),
    ],
    "benchmark-checklist": [("pstack", "pstack/skills/principle-explain-the-number")],
    "code-review": [("pony", "skills/ponytail-review")],
    "grilling": [("matt", "grill-with-docs")],
    "retro": [("pstack", "pstack/skills/reflect"), ("pstack", "pstack/skills/correct")],
    "verification-skill": [
        ("pstack", "pstack/skills/create-verification-skill"),
        ("pstack", "pstack/skills/maintain-verification-skill"),
    ],
}
# Principle files under axo-mode/principles/ and the pstack principle skills each one merges.
principle_sources = {
    "laziness-protocol": [
        "laziness-protocol",
        "subtract-before-you-add",
        "minimize-reader-load",
    ],
    "model-the-domain": ["model-the-domain", "foundational-thinking"],
    "type-system-discipline": ["type-system-discipline", "boundary-discipline"],
    "end-state": [
        "outcome-oriented-execution",
        "redesign-from-first-principles",
        "migrate-callers-then-delete-legacy-apis",
    ],
}


def upstream_changes(source: str, path: str) -> dict[str, object]:
    """File changes between the audited base and head of one merged upstream path.

    Returns a note instead when the source's clone was not passed on the command line.
    Matt paths are skill names, mapped to their folder at the base revision.
    """
    if source not in sources:
        return {"source": source, "path": path, "note": f"Pass --{source} to compare."}
    if source == "matt":
        path = matt_base.get(path, path)
    repo = sources[source][0]
    return {
        "source": source,
        "path": path,
        "upstream_changes": changes(
            tree(repo, metadata[source]["base"], path),
            tree(repo, metadata[source]["head"], path),
        ),
    }


rows = []
for directory in sorted((local / "skills").iterdir()):
    name = directory.name
    if not (directory / "SKILL.md").exists():
        continue
    if name in cloudflare_names:
        if not args.cloudflare:
            rows.append(
                {
                    "skill": name,
                    "source": "cloudflare",
                    "note": "Pass --cloudflare to compare.",
                }
            )
            continue
        source = "cloudflare"
        base_path = head_path = f"skills/{name}"
    elif name in pstack_names:
        source = "pstack"
        base_path = head_path = f"pstack/skills/{name}"
    else:
        upstream_name = "setup-matt-pocock-skills" if name == "setup-axostack" else name
        if upstream_name not in matt_base:
            rows.append(
                {
                    "skill": name,
                    "source": "local",
                    "note": "Review related upstream workflows manually.",
                }
            )
            continue
        source = "matt"
        base_path = matt_base[upstream_name]
        head_path = matt_head.get(upstream_name, base_path)
    repo = sources[source][0]
    base = tree(repo, metadata[source]["base"], base_path)
    head = tree(repo, metadata[source]["head"], head_path)
    installed = worktree(directory)
    rows.append(
        {
            "skill": name,
            "source": source,
            "base_path": base_path,
            "head_path": head_path,
            "upstream_changes": changes(base, head),
            "local_changes_since_base": changes(base, installed),
            "local_differs_from_head": changes(head, installed),
        }
    )
for row in rows:
    if row["skill"] in merged:
        row["merged_upstreams"] = [
            upstream_changes(source, path) for source, path in merged[row["skill"]]
        ]
for path in sorted((local / "skills" / "axo-mode" / "principles").glob("*.md")):
    upstream = principle_sources.get(path.stem, [path.stem])
    rows.append(
        {
            "skill": f"axo-mode/principles/{path.name}",
            "source": "pstack",
            "note": "Restructured locally; port upstream changes by hand.",
            "merged_upstreams": [
                upstream_changes("pstack", f"pstack/skills/principle-{name}")
                for name in upstream
            ],
        }
    )
print(
    json.dumps(
        {
            "local_head": git(local, "rev-parse", "HEAD").decode().strip(),
            "sources": metadata,
            "skills": rows,
        },
        indent=2,
    )
)
