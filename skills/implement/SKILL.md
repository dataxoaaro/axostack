---
name: implement
description: "Build the work a plan, spec, or ticket set describes: read the slices, drive tdd at the agreed seams, verify each slice before starting the next, and close out through review and the Committing playbook. Use for /implement, 'build this', or the build phase of any playbook. Skip when there is no agreed shape yet, where `/plan` or `/grill-me` comes first, and for a single obvious edit."
---

# Implement

The build phase. The shape was decided before you got here, so your job is to land it one verifiable slice at a time and to notice when the plan turns out to be wrong.

Everything this skill names is owned somewhere else. The **tdd** skill owns the red-green loop, the **code-review** skill owns the review, and axo-mode's Committing playbook owns branches, gates, and commit messages. Route into them, don't restate them.

## Input

A plan under `docs/plans/`, a ticket, or a spec in the conversation. Read all three of a plan's tables, not just the first:

- **Slices** is the work list, already in dependency order.
- **Assumptions** is what to watch. An assumption a slice depends on that is graded 1 gets proven before that slice starts, not after it breaks.
- **Open decisions** is what is not settled. A question that gates a slice stops that slice. Say whether it gates, then either continue or report and stop. Picking an answer silently is the failure this section exists to prevent.

No plan, no slices → name the seams before writing anything: where behavior changes and **tdd** applies, and where it doesn't because the change is config, wiring, or generated code.

## Start

Copy the slices into the todo list, one entry each, in dependency order. A slice you don't build stays in the list with `skip: <reason>`.

## The loop, one slice at a time

Per **principle-sequence-verifiable-units**. Finish a slice before opening the next one.

1. Confirm the slice's blockers landed. A blocked slice does not start.
2. Behavior change → the **tdd** skill, red first. Not a behavior change → say which kind it is and skip tdd with that reason.
3. Cut the narrow complete path through every layer the slice touches. A slice that lands in one layer is not a slice.
4. Cadence: typecheck after each meaningful edit, and run the single test file you are working in on each red-green cycle. Leave the full suite for close-out; running it every cycle is slow enough that you learn to ignore it.
5. Verify on the real surface per **principle-prove-it-works**, driving the repo's `verify-<app>` skill when it has one. "It compiles" and "tests pass" are not a pass for behavior a user can see.
6. Commit the slice before starting the next, through the Committing playbook.

## When the build proves the plan wrong

A slice that fights back is evidence about the plan, not friction to absorb. One instance is a note in the reply. A pattern is a re-entry.

Tells:

- An assumption in the plan's table turns out to be false. This one is never a judgment call. The plan graded its assumptions so that this moment is detectable, so it goes straight to re-entry.
- The slice needs a capability the plan never mentions, and it isn't a detail.
- Two slices are really one, or one is really three.
- The acceptance check cannot be written as the plan states it.

Then stop building and re-enter the plan through the **plan** skill, carrying what the build found as evidence. Revise the affected sections, resume from the revised slices. Bolting the discovery onto the current slice hides it from everyone who reads the plan next, per **principle-fix-root-causes**.

## Resuming

Picking up half-built work in a fresh context:

1. `git status` and `git log --oneline main..HEAD`. What actually landed.
2. The plan's Slices table against those commits. Which slice is in flight.
3. The **recall** skill when git alone doesn't show what was being attempted.
4. Re-run the in-flight slice's verification before continuing. Uncommitted work is not in the state you assume it is.

## Close out

1. Full test suite once, green.
2. The **code-review** skill over the diff since the branch point.
3. The **no-comments** skill.
4. Run axo-mode's Committing playbook. It owns branch naming, the gates, the tracker-key scan, the message format, and the rule that pushing waits for explicit approval.
5. If what shipped differs from what the plan described, re-enter the plan so it matches. A plan that disagrees with the branch is worse than no plan.

**Reply:** the slices that landed, gate results, anything the build changed about the plan, and what is left.
