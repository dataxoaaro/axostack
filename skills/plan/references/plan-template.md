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

*Vertical tracer bullets in dependency order, the shape to-tickets consumes.*

| # | Slice | Blocked by | Delivers |
|---|-------|-----------|----------|
| 1 | <short title> | none | <the end-to-end behaviour this makes work, from the user's side> |
| 2 | <short title> | 1 | <...> |

## Assumptions

*Everything the plan rests on, graded on the blast-radius ladder: 1 you said so, 2 you pointed at the line, 3 you showed the bad case can't happen, 4 you ran it, 5 you reproduced it in the running app. Anything left at 1 says **unproven** in the evidence column. Do not round up.*

| # | Assumption | Grade | Evidence |
|---|-----------|-------|----------|
| A1 | <the fact this is safe because of> | 4 | `scripts/probe.py`, output pasted below |
| A2 | <...> | 1 | **unproven** |

## Verification

*How we'll know it works.*

- **Acceptance checks:** one per user-visible behavior, each something somebody runs.
- **Feature map:** the `verify-<app>/features/*.md` entries this change touches, and the ones it adds. One line saying it doesn't apply is the right answer for a repo with no user-facing surface.

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
