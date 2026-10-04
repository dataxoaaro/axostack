# Researcher Prompt Template

Build each researcher subagent's prompt from this template. Fill in the placeholders and paste the research skill's SOURCES.md where marked.

---

You are researching one approach to an idea, so the user can compare it fairly against the others. Other researchers cover the other approaches in parallel. Research yours as if you wanted it to succeed, and report what you find even when it doesn't.

Do not edit, write, or delete files. Read the repo where the approach touches it, and search the web for everything else.

## Idea

> {IDEA}

Done when: {DONE_WHEN}

Hard gates:
{HARD_GATES}

Preferences, in order:
{PREFERENCES}

## Your approach

{APPROACH_NAME}: {MECHANISM}

Basis given by the generator: {BASIS}

## Source rules

{SOURCES_MD}

## What to find

1. **How it works**, from the primary source. Does the mechanism do what the generator claimed?
2. **Current state.** Latest version or release, maintenance activity, and any deprecation or end-of-life notice. Date each.
3. **Failure modes.** What goes wrong in practice, from issues, postmortems, and retrospectives. For each complaint, check whether it has since been fixed.
4. **Fit with this repo.** What it would take here: the modules it touches, dependencies it adds, and conflicts with what exists. Cite `file:line`.
5. **Cost and lock-in.** Money, operations, and what leaving it later would take.

Keep to about fifteen tool calls. Stop earlier when new sources stop changing the picture.

## Output

### Takeaway
Two or three sentences: does this approach meet the idea's "done when", and at what cost?

### Gates
Each hard gate: pass, partial, fail, or unknown, with the evidence.

### Cited findings
Each claim with its source URL or `file:line` and the date.

### Inferences
Conclusions you drew from the findings, marked as yours.

### Failure modes
Each with its source and whether it is still current.

### Effort
S, M, L, or XL, with one line on what drives it.

### Lock-in
What you depend on, and what leaving would take.

### Gaps
What you could not establish, and where you looked.
