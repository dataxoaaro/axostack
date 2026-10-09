### Committing

**Invoked at the end of every other playbook.**

1. `git status` first. Never commit on main: create or switch to a feature branch, prefixed with the tracker key when the work has one (for Linear, the issue key prefixes the branch name).
2. Run the repo's format, lint, and test gates. In Python repos: `ruff format .`, `ruff check . --fix`, `uv run pytest`. A failing gate blocks the commit; fix it, don't skip it.
3. Check the diff for tracker keys in code comments or identifiers: `git diff <base>...HEAD | grep -n "^+.*[A-Z]\{2,\}-[0-9]"`. Keys belong in the branch name and commit message, never in code.
4. Conventional commit message: `<type>: <description>` with types feat, fix, refactor, docs, test, chore, perf, ci. The tracker key goes in the message body. No AI attribution lines.
5. Sequence commits per [sequence-verifiable-units](../principles/sequence-verifiable-units.md): each commit builds and passes tests on its own. For a bug fix, the failing test commits before the fix.
6. Pushing is a one-way door under the [question rule](../SKILL.md#autonomy). Commit locally, report, and ask before pushing, unless the invocation already approved the push.
7. Every PR body is written with the **pr** skill, including a rewrite after a large change under review.
8. Once a push is approved and done, read the remote instead of predicting it: `gh pr checks` and `gh run list --branch <branch>` for CI, `gh pr view --json state,mergedAt,url` for merge state. After pulling a merge, run `git log <base>..<merge>` to catch commits made outside this session, and check whether any landed in files you rewrote.

**Reply:** branch name, commit list, gate results, and remote state when a push happened.
