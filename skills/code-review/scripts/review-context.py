#!/usr/bin/env python3
"""Precompute the shared context every code-review axis reads.

    python3 review-context.py <fixed-point> [--head <sha>] [--out <dir>]

With --head, the code under review is `git diff <fixed-point>...<head>` and
the working tree is ignored. Without it, the code under review is the branch
plus uncommitted work: `git diff <fixed-point>...HEAD` on a clean tree, or
`git diff $(git merge-base <fixed-point> HEAD)` plus untracked files on a
dirty one.

Writes a directory under the OS temp dir (or --out) holding:

  meta.txt      fixed point, head, mode, diff base, and the diff command
  summary.txt   counts, the large-diff flag, and changed lines per directory
  commits.txt   git log --oneline <fixed-point>..<head>
  files.txt     git diff --name-status of tracked changes
  untracked.txt untracked files, read in full by the axes (working tree only)
  diff/<path>.diff  one diff per changed tracked file
  symbols.txt   names defined or edited in the hunks of code files (prose and
                data files are skipped), with the file they came from
  callers.txt   `git grep -n -w` hits for each symbol across the repo

The parent adds tests.txt with the output of the repo's test command.

Read-only: it runs git with GIT_OPTIONAL_LOCKS=0 so even `git status` leaves
the index untouched. Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from collections import defaultdict

LARGE_FILES = 40
LARGE_LINES = 2000
MAX_SYMBOLS = 200
MAX_CALLERS = 100
MIN_SYMBOL_LEN = 3
MAX_CLUSTERS_SHOWN = 15

# Prose and data files: a definition keyword there is a word, not a symbol.
NOT_CODE = {
    ".md",
    ".mdx",
    ".txt",
    ".rst",
    ".adoc",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".lock",
    ".csv",
    ".svg",
    ".xml",
    ".ini",
    ".cfg",
}

# Names too generic for a whole-repo grep to say anything about callers.
STOPLIST = {
    "__init__",
    "__call__",
    "__repr__",
    "__str__",
    "__eq__",
    "__hash__",
    "main",
    "init",
    "setup",
    "teardown",
    "run",
    "get",
    "set",
    "update",
    "render",
    "constructor",
    "handler",
    "default",
    "index",
    "self",
    "this",
    "props",
    "state",
    "result",
    "value",
    "data",
    "config",
    "options",
}

DEFINITION = re.compile(
    r"\bdef\s+(\w+)"
    r"|\bclass\s+(\w+)"
    r"|\bfunction\s*\*?\s*(\w+)"
    r"|\bfunc\s+(?:\([^)]*\)\s*)?(\w+)"
    r"|\bfn\s+(\w+)"
    r"|\b(?:struct|interface|trait|enum)\s+(\w+)"
    r"|\b(?:const|let|var)\s+(\w+)\s*(?::[^=]+)?=\s*(?:async\s+)?(?:\(|function\b|\w+\s*=>)"
    r"|\bexport\s+(?:default\s+)?(?:async\s+)?(?:const|let|var|type)\s+(\w+)"
)
HUNK_HEADER = re.compile(r"^@@ [^@]* @@ ?(.*)$")


def git(*args: str, check: bool = True) -> str:
    """Run git read-only and return stdout."""
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, env=env, errors="replace"
    )
    if check and proc.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def resolve(ref: str) -> str:
    """Resolve a ref to a commit SHA, or exit with a clear message."""
    out = git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)
    if not out.strip():
        sys.exit(f"cannot resolve {ref!r} to a commit")
    return out.strip()


def pin(fixed: str, head: str | None) -> dict[str, str]:
    """Decide the diff base, the target, and the mode."""
    fixed_sha = resolve(fixed)
    if head:
        head_sha = resolve(head)
        base = git("merge-base", fixed_sha, head_sha).strip()
        return {
            "mode": "pinned head",
            "fixed": fixed_sha,
            "head": head_sha,
            "base": base,
            "target": head_sha,
        }
    head_sha = resolve("HEAD")
    base = git("merge-base", fixed_sha, head_sha).strip()
    dirty = bool(git("status", "--porcelain", "--untracked-files=all").strip())
    if dirty:
        return {
            "mode": "working tree",
            "fixed": fixed_sha,
            "head": head_sha,
            "base": base,
            "target": "",
        }
    return {
        "mode": "clean HEAD",
        "fixed": fixed_sha,
        "head": head_sha,
        "base": base,
        "target": head_sha,
    }


def diff_args(ctx: dict[str, str]) -> list[str]:
    """The revision arguments for every git diff call."""
    return [ctx["base"], ctx["target"]] if ctx["target"] else [ctx["base"]]


def changed_lines(text: str) -> list[str]:
    """Added and removed lines plus hunk-header context from one file's diff."""
    lines = []
    for line in text.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith(("+", "-")):
            lines.append(line[1:])
            continue
        header = HUNK_HEADER.match(line)
        if header and header.group(1):
            lines.append(header.group(1))
    return lines


def symbols_in(lines: list[str]) -> list[str]:
    """Definition names found in the lines, in first-seen order."""
    found: dict[str, None] = {}
    for line in lines:
        for match in DEFINITION.finditer(line):
            name = next(g for g in match.groups() if g)
            keep = (
                len(name) >= MIN_SYMBOL_LEN
                and name not in STOPLIST
                and not name.lower().startswith("test")
            )
            if keep:
                found.setdefault(name, None)
    return list(found)


def callers(name: str, ctx: dict[str, str]) -> list[str]:
    """`git grep -n -w` hits for one name, at the target or in the worktree."""
    if ctx["target"]:
        out = git(
            "grep", "-n", "-w", "-I", "-F", "-e", name, ctx["target"], "--", check=False
        )
        prefix = ctx["target"] + ":"
        return [line.removeprefix(prefix) for line in out.splitlines()]
    out = git(
        "grep", "-n", "-w", "-I", "-F", "--untracked", "-e", name, "--", check=False
    )
    return out.splitlines()


def cluster_of(path: str) -> str:
    """The directory a file is grouped under for a split Correctness review."""
    parts = pathlib.PurePosixPath(path).parts
    return (
        "/".join(parts[:2]) if len(parts) > 2 else (parts[0] if len(parts) > 1 else ".")
    )


def write_diffs(
    out: pathlib.Path, ctx: dict[str, str], files: list[str]
) -> dict[str, list[str]]:
    """One diff file per changed path. Returns each path's changed lines."""
    per_file = {}
    for path in files:
        text = git("diff", "--no-renames", *diff_args(ctx), "--", path)
        target = out / "diff" / f"{path}.diff"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        per_file[path] = changed_lines(text)
    return per_file


def numstat(ctx: dict[str, str]) -> dict[str, int]:
    """Changed lines (added plus removed) per tracked path. Binary counts as 0."""
    counts = {}
    for line in git("diff", "--no-renames", "--numstat", *diff_args(ctx)).splitlines():
        added, removed, path = line.split("\t", 2)
        counts[path] = (int(added) if added.isdigit() else 0) + (
            int(removed) if removed.isdigit() else 0
        )
    return counts


def build(fixed: str, head: str | None, out: pathlib.Path) -> str:
    """Write the context directory and return the summary text."""
    ctx = pin(fixed, head)
    log_target = ctx["target"] or ctx["head"]
    commits = git("log", "--oneline", f"{ctx['fixed']}..{log_target}")
    name_status = git("diff", "--no-renames", "--name-status", *diff_args(ctx))
    counts = numstat(ctx)
    files = list(counts)
    untracked = (
        []
        if ctx["target"]
        else git("ls-files", "--others", "--exclude-standard").splitlines()
    )

    per_file = write_diffs(out, ctx, files)
    for path in untracked:
        source = pathlib.Path(path)
        text = source.read_text(errors="replace") if source.is_file() else ""
        per_file[path] = text.splitlines()
        counts[path] = len(per_file[path])

    origin: dict[str, list[str]] = defaultdict(list)
    for path, lines in per_file.items():
        if pathlib.PurePosixPath(path).suffix.lower() in NOT_CODE:
            continue
        for name in symbols_in(lines):
            origin[name].append(path)
    names = list(origin)[:MAX_SYMBOLS]

    caller_blocks = []
    for name in names:
        hits = callers(name, ctx)
        shown = hits[:MAX_CALLERS]
        more = (
            f" (first {MAX_CALLERS} of {len(hits)})" if len(hits) > MAX_CALLERS else ""
        )
        caller_blocks.append(
            f"## {name}  defined or edited in: {', '.join(origin[name])}{more}\n"
            + "\n".join(shown)
            + "\n"
        )

    by_cluster: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for path, n in counts.items():
        by_cluster[cluster_of(path)][0] += 1
        by_cluster[cluster_of(path)][1] += n
    total_lines = sum(counts.values())
    large = len(counts) > LARGE_FILES or total_lines > LARGE_LINES

    diff_cmd = (
        f"git diff {ctx['fixed']}...{ctx['target']}"
        if ctx["target"]
        else f"git diff {ctx['base']}  (plus untracked files)"
    )
    meta = (
        f"mode: {ctx['mode']}\nfixed point: {fixed} = {ctx['fixed']}\n"
        f"head: {ctx['head']}\ndiff base: {ctx['base']}\ndiff command: {diff_cmd}\n"
    )
    ranked = sorted(by_cluster.items(), key=lambda item: -item[1][1])
    clusters = "\n".join(
        f"  {name}: {f} files, {n} lines"
        for name, (f, n) in ranked[:MAX_CLUSTERS_SHOWN]
    )
    if len(ranked) > MAX_CLUSTERS_SHOWN:
        clusters += f"\n  and {len(ranked) - MAX_CLUSTERS_SHOWN} more directories"
    summary = (
        f"context: {out}\n{meta}"
        f"commits: {len(commits.splitlines())}\n"
        f"changed files: {len(files)} tracked, {len(untracked)} untracked\n"
        f"changed lines: {total_lines}\n"
        f"symbols: {len(origin)} found, {len(names)} grepped for callers\n"
        f"large diff (over {LARGE_FILES} files or {LARGE_LINES} lines): {'yes' if large else 'no'}\n"
        f"changed lines per directory:\n{clusters}\n"
    )

    (out / "meta.txt").write_text(meta)
    (out / "commits.txt").write_text(commits)
    (out / "files.txt").write_text(name_status)
    (out / "untracked.txt").write_text(
        "\n".join(untracked) + ("\n" if untracked else "")
    )
    (out / "symbols.txt").write_text(
        "".join(f"{name}\t{', '.join(paths)}\n" for name, paths in origin.items())
    )
    (out / "callers.txt").write_text("\n".join(caller_blocks))
    (out / "summary.txt").write_text(summary)
    return summary


def main() -> None:
    """Parse arguments, build the context directory, print the summary."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("fixed_point")
    parser.add_argument(
        "--head",
        help="review exactly <fixed-point>...<head>, ignoring the working tree",
    )
    parser.add_argument(
        "--out", help="directory to write; default is a new one under the OS temp dir"
    )
    args = parser.parse_args()

    root = git("rev-parse", "--show-toplevel").strip()
    os.chdir(root)
    out = (
        pathlib.Path(args.out)
        if args.out
        else pathlib.Path(tempfile.mkdtemp(prefix="code-review-"))
    )
    out.mkdir(parents=True, exist_ok=True)
    print(build(args.fixed_point, args.head, out.resolve()), end="")


if __name__ == "__main__":
    main()
