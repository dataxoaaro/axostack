# Plan template

The shape of a plan document. Replace the italic notes with real content. Delete a section only when it genuinely doesn't apply, and say so in one line rather than leaving an empty heading.

Sentence-case headings, no boilerplate, no preamble. The reader is a colleague picking this up cold, or you in three weeks.

---

```markdown
---
plan: <slug>
status: draft
created: <YYYY-MM-DD>
tracker: <issue key or URL, or none>
branch: <branch name, or none yet>
---

# <Imperative title, in the project's glossary vocabulary>

## Done when

*The falsifiable predicate from Phase A. One or two lines. Somebody must be able to run it and get a yes or a no.*

## Problem

*What is wrong or missing, and what makes the shape non-obvious. Every claim cites a `file:line`, command output, measurement, or primary source. Never fabricate a citation.*

## Current state

*What Phase B found: how the affected subsystems work now, and any constraint the design has to honor. Where this contradicts an ADR, name the ADR and say why it's worth reopening.*

## Approach

*The shape we're building. Data structures first, then how data moves through them. Name the decisions that could have gone another way.*

## Alternatives rejected

*At least one. One line each on what it was and why it lost. If constraints forced the answer, say "this was the only viable shape because ..." rather than inventing a strawman.*

## What gets deleted

*What comes out before anything goes in. "Nothing" is an acceptable answer once you have actually looked.*

## Interface sketch

*From the architect skill, when it ran: the caller's usage first, then types and signatures. Omit for changes that don't cross a function boundary, and say so in one line.*

## Slices

*Vertical tracer bullets in dependency order, the shape to-tickets consumes. `Status` is one of `todo`, `in flight`, `landed <sha>`, or `dropped: <reason>`. The table indexes the work; git records it. A landed status points at the commit rather than restating what it did, so `implement` can check the table against `git log` when it resumes and see drift instead of guessing.*

| # | Slice | Blocked by | Status | Delivers | Evidence |
|---|-------|-----------|--------|----------|----------|
| 1 | <short title> | none | todo | <the end-to-end behaviour this makes work, from the user's side> | pending |
| 2 | <short title> | 1 | todo | <...> | pending |

*Replace `pending` with a link to the slice's verification record in this document or a durable artifact. Record commands or actions, observed results, and the verified commit. For uncommitted work, record the base commit and a saved patch or equivalent reproducible snapshot, including relevant untracked files. `HEAD` or "dirty worktree" alone does not identify what passed. Keep delivery status separate from verification evidence.*

*Each slice names its seams below the table: the public interfaces its tests go through. tdd treats them as agreed, and `/to-tickets` copies them into the ticket.*

*Each slice gets its own acceptance criteria below the table: observable statements a reviewer can check against the diff and the repo, such as a command and its expected output, a row count, or a page state. `/to-tickets` copies them verbatim into the slice's ticket, and code-review's Spec axis marks each one pass or fail with evidence.*

### Slice 1: <short title>

Seams: <the public interfaces this slice's tests go through, e.g. "`importer` CLI, `OrdersRepo.count()`">

- [ ] <observable, checkable statement, e.g. "`importer orders.csv` on a 40MB file exits 0 and `SELECT count(*) FROM orders` equals the file's row count">
- [ ] <...>

### Slice 2: <short title>

Seams: <...>

- [ ] <...>

## Assumptions

*Everything the plan rests on, graded on the blast-radius ladder: 1 you said so, 2 you pointed at the line, 3 you showed the bad case can't happen, 4 you ran it, 5 you reproduced it in the running app. Anything left at 1 says **unproven** in the evidence column. Do not round up.*

| # | Assumption | Grade | Evidence |
|---|-----------|-------|----------|
| A1 | <the fact this is safe because of> | 4 | `scripts/probe.py`, output pasted below |
| A2 | <...> | 1 | **unproven** |

## Verification

*How we'll know it works.*

- **Acceptance checks:** the slices' acceptance criteria above are the checks, one per user-visible behavior. Here, add only how to run the ones that need setup, and the end-to-end check for the Done when predicate.
- **Feature map:** the `verify-<app>/features/*.md` entries this change touches, and the ones it adds. One line saying it doesn't apply is the right answer for a repo with no user-facing surface.
- **Performance baseline, when required by acceptance criteria:** metric, workload, environment, threshold, baseline revision, and measured result. Link the final comparison run under the same conditions, or state why the comparison remains unverified.
- **Results, filled during implementation:** link each completed slice to its checks and verified revision or snapshot. Record failed or substituted checks and remaining gaps. Preserve historical results when later changes require another run; a pass applies to the recorded state, not automatically to the current branch.

## Out of scope

*What this plan deliberately does not cover, so the boundary is a decision rather than an oversight.*

## Open decisions

*Every question the plan could not settle, in the grilling skill's format, each with a recommended answer. This is the frontier the next grilling session starts from. An empty section means the plan was not thought about, not that it was thorough.*

❓ **Q1** - **<question title>**: <the question, including the options if it's a choice>

➡️ <your recommended answer, and the one line of reasoning behind it>

## Decision log

*Appended as the questions above get answered, so the resolution lives in the plan instead of a chat transcript. Move each question here from Open decisions rather than copying it.*

- **Q1** <the answer that was chosen>. Resolved <YYYY-MM-DD>, <grilling session / prototype / measurement>.
```
