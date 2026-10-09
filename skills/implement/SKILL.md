---
name: implement
description: "Build what a plan, spec, or tickets describe, one verified slice at a time, through tdd and review. Use for /implement, 'build this', or a playbook's build phase. Skip with no agreed shape (`/plan` or grilling first)."
---

# Implement

The build phase. The shape was decided before you got here, so your job is to land it one verifiable slice at a time and to notice when the plan turns out to be wrong. Skip it when there is no agreed shape yet, where `/plan` or the **grilling** skill comes first, and for a single obvious edit.

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

Per [sequence-verifiable-units](../axo-mode/principles/sequence-verifiable-units.md). Finish a slice before opening the next one.

1. Confirm the slice's blockers landed. A blocked slice does not start.
   If performance is an acceptance criterion, capture the plan's baseline on the pre-change revision before implementation, with the specified workload and environment. Record an unavailable baseline as a verification gap.
2. Behavior change → the **tdd** skill, red first. Not a behavior change → say which kind it is and skip tdd with that reason.
3. Cut the narrow complete path through every layer the slice touches. A slice that lands in one layer is not a slice.
4. Cadence: typecheck after each meaningful edit, and run the single test file you are working in on each red-green cycle. Leave the full suite for close-out; running it every cycle is slow enough that you learn to ignore it. Behavior-preserving work is the exception: when the change is supposed to alter nothing a test can see, the full suite is the proof, so it runs on every unit.
5. Verify on the real surface per [prove-it-works](../axo-mode/principles/prove-it-works.md), driving the repo's `verify-<app>` skill when it has one. "It compiles" and "tests pass" are not a pass for behavior a user can see.
   When the slice delivers a check, verifying it means making it fail. Write a throwaway subject carrying one deliberate defect per class the check claims to catch, plus the near misses that must stay silent, and confirm each class reports and the exit code flips back once the subject is gone. A check that has only ever returned green is a check you hope works.
   Save the checks, observed results, and tested state in a verification record and link it from the slice's Evidence column. For a clean checkout, record the commit; for uncommitted work, record the base commit and a saved patch or equivalent reproducible snapshot, including relevant untracked files. Compare performance with the recorded baseline under the same conditions when required.
6. Commit the slice before starting the next, through the Committing playbook. Then set that slice's Status in the plan to `landed <sha>`, so the next session reads where the work stopped instead of inferring it.
   Associate the verification record with the landing commit only after confirming its relevant contents match the tested snapshot. If hooks or intervening edits changed them, re-run the affected checks. If the user asked to leave work uncommitted, retain `in flight` and its snapshot evidence. A later commit that only records plan status does not require re-running checks; later changes to the implementation, tests, dependencies, or relevant configuration do. Preserve earlier results and add evidence for the new state.

## When the build proves the plan wrong

A slice that fights back is evidence about the plan, not friction to absorb. One instance is a note in the reply. A pattern is a re-entry.

Tells:

- An assumption in the plan's table turns out to be false. This one is never a judgment call. The plan graded its assumptions so that this moment is detectable, so it goes straight to re-entry.
- The slice needs a capability the plan never mentions, and it isn't a detail.
- Two slices are really one, or one is really three.
- The acceptance check cannot be written as the plan states it.

Then stop building and re-enter the plan through the **plan** skill, carrying what the build found as evidence. Revise the affected sections, resume from the revised slices. Bolting the discovery onto the current slice hides it from everyone who reads the plan next, per [fix-root-causes](../axo-mode/principles/fix-root-causes.md).

## Resuming

Picking up half-built work in a fresh context:

1. `git status` and `git log --oneline main..HEAD`. What actually landed.
2. The plan's Slices table and linked evidence. Check landed commits in repository history, including merged work outside `main..HEAD`. Confirm their changes remain present; a reverted commit can still be an ancestor. The first unfinished slice whose blockers hold is where to resume.
3. Reconcile any disagreement before building. Missing commits may have been squashed or rebased; inspect the replacement history and contents before changing the table. For historical plans without Evidence columns or saved results, preserve valid landed statuses and add verification gaps instead of inventing past checks. Re-run checks needed for the work being resumed, then link the new evidence. Do not treat a historical pass as proof of later changes.
4. The **recall** skill when git alone doesn't show what was being attempted.
5. Re-run the in-flight slice's verification before continuing. Uncommitted work is not in the state you assume it is.

## Close out

1. Full test suite once, green.
2. The **code-review** skill over the diff since the branch point.
3. The **no-comments** skill.
4. Run axo-mode's Committing playbook. It owns branch naming, the gates, the tracker-key scan, the message format, and the rule that pushing waits for explicit approval.
5. If what shipped differs from what the plan described, re-enter the plan so it matches. A plan that disagrees with the branch is worse than no plan.
6. A slice that delivers a procedure, script, or skill does not close until you have run it once, end to end, against a real task, and folded the first-run defects into the same slice. Say which of its branches never executed. A procedure exercised only where every optional input was absent has had its default path tested and its configured path shipped on faith.
7. Link the final gate results to the revision or snapshot they tested. Re-run affected checks after review fixes and other relevant changes. Report unresolved verification gaps, including missing performance comparisons, rather than mark them passed.

A gate you could not run as written is reported as a substitution, with what you ran instead and why. "Reviewed" means the **code-review** skill ran. A grep that stands in for it is a grep, and calling it a pass is how three slices ship unreviewed while every line of the report says green.

**Reply:** the slices that landed, gate results, anything the build changed about the plan, and what is left.
