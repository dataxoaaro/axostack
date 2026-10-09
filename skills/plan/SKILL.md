---
name: plan
description: "Work a feature or fix into one written plan: grounded, shaped, risk-graded, and sliced into tickets. Use for /plan, 'plan this', or before building anything whose shape isn't settled. Skip for one obvious edit."
---

# Plan

Turn a feature or a fix into one plan document: what we're building, what we found, what we chose, what could break, how we'll know it works, and what's still open. The document is the deliverable. It gets grilled, then broken into tickets, then built.

The plan has to be attackable. Every decision that could have gone another way is either recorded with the alternative it beat, or left open as a numbered question with your recommended answer. Nothing is silently assumed.

## Route first

Answer one question before starting: can you state the change now?

| Situation | Skill |
|---|---|
| You can state the change; the shape, risks, and slicing need working out | this one |
| You have an idea with several possible approaches and none chosen yet | `/research-idea` |
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

Given a `/research-idea` decision record, start from it. Its requirements frame the plan, its chosen approach is the shape to work out, its rejected approaches are the recorded alternatives, and its open questions carry over. Reopen the choice only when grounding contradicts the record's evidence, and say so.

If a fork blocks the framing itself, run a short pass of the **grilling** skill on that fork alone. Only the questions that decide whether there is a plan to write. The full interview comes later, against the finished document.

## Phase B: Ground

Scale this to the question, the way the **how** skill scales its own exploration. A change touching one module is a single pass. A change spanning subsystems fans out as parallel subagents, keeping only their findings in the main thread, per axo-mode's [Subagents](../axo-mode/SKILL.md#subagents) section. Say which one you did.

- **how** over each subsystem the change touches. Structure, runtime flow, ownership.
- **why** over anything that looks arbitrary and is about to be changed. A constraint you can't see is the one you'll break.
- **research** for any external fact the approach rests on, against primary sources.

Read `GLOSSARY.md` and the ADRs under `docs/adr/` per the repo's domain doc rules. Write the plan in the glossary's vocabulary. Where the plan contradicts an ADR, say so in the document and say why it's worth reopening. Never override one quietly.

Then read the repo's `verify-<app>` feature map, when it has one. The features listed there that this change touches are the ones the plan has to keep working.

## Phase C: Shape

- Crosses a function boundary → the **architect** skill. Its synthesized type sketch and rationale become the plan's Interface sketch section, not a separate artifact.
- Name the data shape and its organizing structure before any logic, per [model-the-domain](../axo-mode/principles/model-the-domain.md).
- A fork whose answer is observable (behavior, timing, layout, output, perf) is not the user's to answer. Build the probe with the **prototype** skill and let the result decide. Reserve questions for genuine product calls no experiment can settle.
- Record at least one alternative shape you rejected, with the line on why it lost. Where the constraints forced the answer, say that instead of inventing a strawman. This is the **architect** skill's design-it-twice rule at plan scale.
- Say what gets deleted, per [laziness-protocol](../axo-mode/principles/laziness-protocol.md). "Nothing" is a valid answer once you have looked for dead weight and not found any.

## Phase D: Risk and verification

- Run the **blast-radius** skill against the proposed change, not the diff, since there is no diff yet. What breaks somewhere else, and the one fact this is safe because of.
- Grade every assumption the plan rests on with blast-radius's ladder: 1 you said so, 2 you pointed at the line, 3 you showed the bad case can't happen, 4 you ran it, 5 you reproduced it in the running app. Get the ones that matter to 4. Anything still at 1 is written into the plan as **unproven**. Do not round up, and do not quietly drop an assumption you failed to prove.
- Name the decision each graded assumption supports. A grade is a grade of one question. "Nothing quotes this file's body" is grade 4 evidence that deleting it is safe and says nothing about whether the file should exist, so carrying the number across to the second question is a guess wearing a 4.
- A script only earns grade 4 once you have seen it give the opposite answer. Until then you have run something, not proved something. When your own scan reports an absence, suspect the scan first: check what it excludes, whether the thing is written under a second name, and whether it matches case. A scan that finds nothing and a repo that contains nothing look identical from here.
- Write the acceptance checks as things somebody runs, one per behavior the user can see. They live as each slice's acceptance criteria (below), not as a second list. A check that lands in CI runs on whatever bare interpreter the image ships, so it takes no dependency the repo does not already install, resolves its targets from its own file rather than the working directory, and is proved by running it from an unrelated directory before you believe the green.
- When performance is an acceptance criterion, specify the metric, workload, environment, and threshold. Measure and record the baseline revision before implementation so the final comparison uses the same conditions. If the baseline cannot be measured, record that gap rather than claim an improvement.
- Name the `verify-<app>` feature files this change touches and the ones it needs to add. User-facing change and no verification skill in the repo → say so and recommend `/verification-skill create` as the first slice. No user-facing surface at all, as in a library or a config repo → say that in one line and move on rather than manufacturing a verification story.
- Slice the work into vertical tracer bullets, each demoable on its own and each sized for one fresh context window, with the blocking edges between them. Write them in the shape `/to-tickets` consumes so publishing is mechanical rather than a second breakdown from memory. A wide mechanical refactor is the exception. Sequence it expand, migrate, contract, as to-tickets describes. Every slice starts at `todo`; the **implement** skill moves it as work lands.
- Give each slice its own acceptance criteria: observable, checkable statements, such as a command and its expected output, a row count, or a page state. `/to-tickets` copies them verbatim into the slice's ticket, and the **code-review** skill's Spec axis checks them one by one, pass or fail with evidence. So write each one so a reviewer holding only the diff and the repo can settle it. "Handles errors well" can't be settled; "an empty CSV exits 1 with `no rows`" can.
- Give each slice an Evidence column, initially `pending`. On completion it links to a verification record with the checks, results, and exact revision or worktree snapshot tested. A landing commit alone records delivery, not verification.

## Phase E: Write and hand off

Write the file in the shape of [`references/plan-template.md`](references/plan-template.md), through the **technical-writing** and **unslop** skills. Numbered, dated, status `draft`.

The Open decisions section carries every question the plan could not settle, in the **grilling** skill's own format, each with your recommended answer. That section is the frontier the next grilling session starts from, so it is the part that has to be right. An empty Open decisions section alongside no recorded alternatives means the thinking did not happen, not that it was thorough.

Then stop and hand off. Do not start building.

```
/plan <feature>            →  docs/plans/<NNNN>-slug.md    status: draft
/grilling <path>           →  answers folded back in       status: grilled
(user approves)                                            status: approved
/to-tickets <path>         →  tickets in dependency order
/idea-to-pr <key>          →  built
```

You set `draft`, `grilled`, and the slice statuses. You never set `approved`. That one moves on an explicit statement from the user and on nothing else, because it is the gate that catches a plan whose reasoning is wrong, and a plan cannot pass its own gate. Building against an ungrilled plan is allowed when the user asks for it. Marking it approved to get there is not.

## Re-entry

`/plan <path>` on a plan that already exists updates it rather than writing a second one. Fold resolved answers into the body, move each question to the Decision log, bump the plan's status and any slice statuses that moved, and re-run only the phases the answers invalidated. A resolved decision lives in the plan, not in a chat transcript nobody can find. When a plan is abandoned, mark it `superseded` and name what replaced it; don't delete it.

**Reply:** the plan's path, the approach in three lines, the assumptions still unproven, and the open decisions by number. Not a re-run of the document.
