# Agent artifacts

Where the engineering skills write their own Markdown in this repo. Three buckets, split by how long the output is meant to last.

## Plans

- **Location:** `docs/plans/<NNNN>-<slug>.md`, numbered from `0001` like ADRs
- **Committed:** yes

Written by the `plan` skill. Read by `/grill-with-docs` when the plan gets stress-tested, by `to-tickets` when it gets sliced, and by whoever reviews the PR that implements it. Committed because all three of those happen after the session that wrote it.

Every plan carries `status:` in its frontmatter: `draft`, `grilled`, `approved`, `superseded`. Update it in place rather than writing a second file. An abandoned plan is marked `superseded` with a pointer to what replaced it, never deleted.

## Research notes

- **Location:** `docs/research/<slug>.md`
- **Committed:** yes

Cited findings from the `research` skill against primary sources. Committed because the point of citing a primary source is that the next person doesn't have to read it again. Each claim carries its source.

## Throwaway analysis

- **Location:** `claudedocs/`
- **Committed:** no, gitignored

Writeups from `how`, `why`, and `blast-radius`, and anything else produced to answer one question inside one session. Not a durable record and not a place to look things up later.

When something written here turns out to matter, promote it rather than leaving it: a decision becomes an ADR, a shape becomes a plan, a term becomes a line in `GLOSSARY.md`.

## Rules for anything written here

- One artifact per question. Re-entering a topic updates the existing file; it does not fork a second one.
- Committed artifacts go through the `technical-writing` and `unslop` skills before they land.
- Every claim cites a `file:line`, command output, or a primary source. Never fabricate a citation.
- Tickets are not artifacts. They live wherever `docs/agents/issue-tracker.md` says, including the local-markdown tracker's `.scratch/`.
