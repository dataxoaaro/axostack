---
name: plan
description: "Work a feature or fix into one written plan: grounded in the codebase, shaped, risk-graded, and sliced into tickets. Use for /plan, 'plan this', 'write up a plan', or before building anything whose shape isn't settled yet. Skip when the change is one obvious edit, when the path itself is fogged (`/wayfinder`), or when the shape is already settled and only the run is long (`/figure-it-out`)."
---

# Plan

Turn a feature or a fix into one plan document: what we're building, what we found, what we chose, what could break, how we'll know it works, and what's still open. The document is the deliverable. It gets grilled, then broken into tickets, then built.

The plan has to be attackable. Every decision that could have gone another way is either recorded with the alternative it beat, or left open as a numbered question with your recommended answer. Nothing is silently assumed.

## Route first

Answer one question before starting: can you state the change now?

| Situation | Skill |
|---|---|
| You can state the change; the shape, risks, and slicing need working out | this one |
| You can state the questions but not the change | `/wayfinder` |
| The change is clear, the run is long, mechanical, or unattended | `/figure-it-out` |
| One obvious edit in one file | none, just do it |

Inside a plan, the **architect** skill designs the types and signatures. It does not replace this skill, and this skill does not replace it.

## Start

Open a todolist with one entry per phase, plus a first entry to read the Principles section of the **axo-mode** skill. Phases don't silently disappear from a list the user can see. No todo tool in this environment → state the phase list in your first reply and mark each one as you go, so a skipped phase is still visible.

## Phase A: Frame

Nothing else starts until these three hold.

- **Done when.** State the definition of done as a falsifiable predicate. "Done well" is not checkable; "the importer accepts a 40MB CSV and the row count in `orders` matches the file" is.
- **Root cause in hand, for a fix.** A fix plan built on a guessed cause plans the wrong fix. No confirmed cause with runtime evidence → stop and run the **diagnosing-bugs** loop first. Come back with the mechanism.
- **A home for the file.** Read `docs/agents/artifacts.md` for where plans live. Missing → default to `docs/plans/`, write the plan there, and tell the user they can settle the convention with `/setup-axostack`.

If a fork blocks the framing itself, run a short pass of the **grilling** skill on that fork alone. Only the questions that decide whether there is a plan to write. The full interview comes later, against the finished document.

## Phase B: Ground

Scale this to the question, the way the **how** skill scales its own exploration. A change touching one module is a single pass. A change spanning subsystems fans out as parallel subagents, keeping only their findings in the main thread, per **principle-guard-the-context-window**. Say which one you did.

- **how** over each subsystem the change touches. Structure, runtime flow, ownership.
- **why** over anything that looks arbitrary and is about to be changed. A constraint you can't see is the one you'll break.
- **research** for any external fact the approach rests on, against primary sources.

Read `CONTEXT.md` and the ADRs under `docs/adr/` per the repo's domain doc rules. Write the plan in the glossary's vocabulary. Where the plan contradicts an ADR, say so in the document and say why it's worth reopening. Never override one quietly.

Then read the repo's `verify-<app>` feature map, when it has one. The features listed there that this change touches are the ones the plan has to keep working.

## Phase C: Shape

- Crosses a function boundary → the **architect** skill. Its synthesized type sketch and rationale become the plan's Interface sketch section, not a separate artifact.
- Name the data shape and its organizing structure before any logic, per **principle-model-the-domain**.
- A fork whose answer is observable (behavior, timing, layout, output, perf) is not the user's to answer. Build the probe with the **prototype** skill and let the result decide. Reserve questions for genuine product calls no experiment can settle.
- Record at least one alternative shape you rejected, with the line on why it lost. Where the constraints forced the answer, say that instead of inventing a strawman. This is **principle-exhaust-the-design-space** at plan scale.
- Say what gets deleted, per **principle-subtract-before-you-add**. "Nothing" is a valid answer once you have looked for dead weight and not found any.

## Phase D: Risk and verification

- Run the **blast-radius** skill against the proposed change, not the diff, since there is no diff yet. What breaks somewhere else, and the one fact this is safe because of.
- Grade every assumption the plan rests on with blast-radius's ladder: 1 you said so, 2 you pointed at the line, 3 you showed the bad case can't happen, 4 you ran it, 5 you reproduced it in the running app. Get the ones that matter to 4. Anything still at 1 is written into the plan as **unproven**. Do not round up, and do not quietly drop an assumption you failed to prove.
- Write the acceptance checks as things somebody runs, one per behavior the user can see.
- Name the `verify-<app>` feature files this change touches and the ones it needs to add. User-facing change and no verification skill in the repo → say so and recommend `/create-verification-skill` as the first slice. No user-facing surface at all, as in a library or a config repo → say that in one line and move on rather than manufacturing a verification story.
- Slice the work into vertical tracer bullets, each demoable on its own and each sized for one fresh context window, with the blocking edges between them. Write them in the shape the **to-tickets** skill consumes so publishing is mechanical rather than a second breakdown from memory. A wide mechanical refactor is the exception. Sequence it expand, migrate, contract, as to-tickets describes. Every slice starts at `todo`; the **implement** skill moves it as work lands.

## Phase E: Write and hand off

Write the file in the shape of [`references/plan-template.md`](references/plan-template.md), through the **technical-writing** and **unslop** skills. Numbered, dated, status `draft`.

The Open decisions section carries every question the plan could not settle, in the **grilling** skill's own format, each with your recommended answer. That section is the frontier the next grilling session starts from, so it is the part that has to be right. An empty Open decisions section alongside no recorded alternatives means the thinking did not happen, not that it was thorough.

Then stop and hand off. Do not start building.

```
/plan <feature>            →  docs/plans/0007-slug.md      status: draft
/grill-with-docs <path>    →  answers folded back in       status: grilled
(user approves)                                            status: approved
/to-tickets <path>         →  tickets in dependency order
/work-linear-issue <key>   →  built
```

## Re-entry

`/plan <path>` on a plan that already exists updates it rather than writing a second one. Fold resolved answers into the body, move each question to the Decision log, bump the plan's status and any slice statuses that moved, and re-run only the phases the answers invalidated. A resolved decision lives in the plan, not in a chat transcript nobody can find. When a plan is abandoned, mark it `superseded` and name what replaced it; don't delete it.

**Reply:** the plan's path, the approach in three lines, the assumptions still unproven, and the open decisions by number. Not a re-run of the document.
