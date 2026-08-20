### Committing

**Invoked at the end of every other playbook.**

1. `git status` first. Never commit on main: create or switch to a feature branch, prefixed with the tracker key when the work has one (for Linear, the issue key prefixes the branch name).
2. Run the repo's format, lint, and test gates. In Python repos: `ruff format .`, `ruff check . --fix`, `uv run pytest`. A failing gate blocks the commit; fix it, don't skip it.
3. Check the diff for tracker keys in code comments or identifiers: `git diff <base>...HEAD | grep -n "^+.*[A-Z]\{2,\}-[0-9]"`. Keys belong in the branch name and commit message, never in code.
4. Conventional commit message: `<type>: <description>` with types feat, fix, refactor, docs, test, chore, perf, ci. The tracker key goes in the message body. No AI attribution lines.
5. Sequence commits per **principle-sequence-verifiable-units**: each commit builds and passes tests on its own. For a bug fix, the failing test commits before the fix.
6. Never push to remote without explicit approval. Commit locally, report, and ask before pushing.

**Reply:** branch name, commit list, gate results.
