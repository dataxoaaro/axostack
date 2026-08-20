---
plan: implement-skill-duplicates-the-feature-playbook
status: approved
created: 2026-08-20
tracker: none
branch: fix/model-invocable-skills
---

# Write the implement skill as the build-phase verb

## Done when

All five hold, each checkable by running something:

1. No skill body gives commit instructions that disagree with `skills/axo-mode/playbooks/committing.md`.
2. The test-cadence rule (typecheck and single test files during the loop, full suite before close-out) appears in exactly one place in the repo.
3. Each of `feature`, `bug-fix`, and `refactoring` states the build tail once, by naming `implement`, and keeps only its per-type difference.
4. Every reference to `implement` resolves to something that exists.
5. `scripts/check-skill-refs.py` exits 0.

## Problem

`skills/implement/SKILL.md` is 14 lines including frontmatter, and has not been touched since the initial scaffold (`a34f3a3`). Three things reference it: `skills/axo-mode/SKILL.md:31`, `skills/work-linear-issue/SKILL.md:34`, and `README.md:10`. It is the step every tracked piece of work passes through, and it is the thinnest file in the library. Its siblings run 42 to 112 lines.

Two concrete defects.

**It contradicts the Committing playbook.** `skills/implement/SKILL.md:14` says "Commit your work to the current branch." `skills/axo-mode/playbooks/committing.md:5` says "Never commit on main: create or switch to a feature branch." The playbook also requires format, lint, and test gates, a conventional message, a tracker-key scan over the diff, and per-unit commit sequencing. An agent that follows `implement` to the letter commits on whatever branch it is standing on, ungated. `work-linear-issue` routes into `implement` at step 4 and into Committing at step 5, so it hits both.

**Everything else in it is a worse copy of the feature playbook.** "Use tdd at the seams" is step 6, "code-review" is step 8, "commit" is step 9. The playbook states each with the principle behind it; `implement` states each in one clause with none.

One line is not duplicated anywhere: the test cadence at `skills/implement/SKILL.md:10`. A grep across `skills/` finds no other statement of it.

## Current state

`implement` has no awareness of the layer it sits in. It never mentions axo-mode, the playbooks, the principles, verification, branches, or gates. It reads as a note written before the playbooks existed, which the history supports.

This repo has no `CONTEXT.md`, no `docs/adr/`, and no `verify-<app>` skill, so there is no glossary to honor and no ADR to contradict.

## Approach

Keep `implement` and write it. It occupies the build phase the way `code-review` occupies the review phase. `code-review` is 87 lines of real content reached from feature step 8; `implement` is 14 lines reached from feature step 6. The slot is right and the file was never written.

A playbook is the sequence for a task type and spans every phase. A verb is the depth on one phase and is reused across task types. They sit on different axes, so a verb that routes into the library is not a second copy of the playbook.

That distinction also fixes the duplication properly. `feature` steps 6 to 9, `bug-fix` steps 4 to 6, and `refactoring` steps 3 to 7 are one tail written three times: build via `tdd`, verify on the real surface, review, commit. The tail moves into `implement`, and each playbook keeps only its per-type difference (the bug fix's failing regression test landing before the fix in git history, the refactor's characterization tests). Deleting `implement` would have left all three copies standing.

`implement` then owns, as the only statement of each:

- Which seams get `tdd` and which don't, read off the plan rather than re-decided mid-build.
- The build cadence: typecheck and single test files during the loop, full suite once before close-out. This is the one line already unique to the file.
- Slice sequencing, one at a time, each verified before the next, per **principle-sequence-verifiable-units**.
- What to do when the build proves the plan wrong. The **architect** skill's Phase E covers this for type sketches; nothing covers it for plans, and it is the most common way a build goes sideways.
- Resuming a half-built slice in a fresh context.
- Close-out: `code-review`, then `no-comments`, then the Committing playbook. That delegation is what removes the contradiction at line 14.

## Alternatives rejected

- **Delete `implement` and fold it into the playbooks.** This plan's original recommendation, and wrong. It judged the file as written instead of the slot it fills, and it was falsified by `code-review`, which holds the identical position and is nobody's idea of duplication. Deleting also leaves the three playbook tails duplicated, which was the stated defect.
- **Reduce it to a three-line router** into axo-mode's playbook, the shape `grill-me` uses. Lost because the six responsibilities above have no other home, so a forwarding file would leave them unwritten. `grill-me` forwards to a skill that already holds the content; there is no such skill here.
- **Expand it into a self-contained build skill** that restates tdd, verification, and review rather than delegating to them. Lost on **principle-laziness-protocol**: the library already holds each piece, and a second statement is the drift risk this plan exists to remove.

## What gets deleted

The tail duplicated across three playbooks: `feature` steps 6 to 9 collapse to one step, and `bug-fix` steps 5 to 6 and `refactoring` step 7 likewise. `implement`'s line 14 goes, replaced by delegation to Committing. Roughly 12 lines of playbook text come out. Nothing is deleted from `skills/`.

## Interface sketch

Skip: prose artifact, no types or signatures. The **architect** skill does not apply.

## Slices

| # | Slice | Blocked by | Delivers |
|---|-------|-----------|----------|
| 1 | Write `implement` as the build-phase verb, closing out through the Committing playbook | none | The contradiction is gone and an agent following `implement` commits on a branch, gated |
| 2 | Give `implement` the behavior-preserving cadence clause, then collapse the tail out of the three playbooks into one `implement` step each, last in the list | 1 | The build sequence is stated once; each playbook keeps only its per-type difference, and `no-comments` reaches all three instead of only `feature` |
| 3 | Ship `scripts/check-skill-refs.py` | 2 | A dangling or user-only skill reference fails a check instead of reaching an agent mid-task |

Slice 1 lands green on its own and fixes the shipped defect without touching a single caller, so it is worth landing even if 2 and 3 stall.

**Landed:** all three slices. Slice 1 in `bf87f10`, slice 2 in `40065ab`, slice 3 in this commit. All five Done-when predicates pass.

Slice 3 widened during the build. Scoped to dangling references when the plan was written, it grew to cover bare-stem principle citations after the skills review found 28 of them, and that class turned out to be the only one actually present in the library. The check was written before the fix and proved by injecting one defect of each class and watching it fail, so a green run means something.

Slice 2 grew during the build. The `implement` step has to be **last** in each playbook, because `implement` closes out with review and commit, so a step sitting after it would fall outside the build it belongs to. That reorders `refactoring`'s acceptance bar and migrate-callers rule ahead of the build step, where they read as constraints on it rather than as steps after it.

## Assumptions

| # | Assumption | Grade | Evidence |
|---|-----------|-------|----------|
| A1 | No file outside `skills/implement/` quotes its body, so rewriting or removing it breaks only the three name references | 4 | `probe_implement.py` over 110 Markdown files: 5 body sentences, 0 verbatim quotes, 3 name references |
| A2 | The test-cadence rule at line 10 is stated nowhere else | 4 | `grep -rniE "full test suite\|typecheck\|single test file\|whole suite" skills/` returns one unrelated hit in `refactoring.md:8` |
| A3 | `implement` contradicts `committing.md` rather than refining it | 3 | `implement:14` against `committing.md:5-6`; the bad case is an agent committing ungated on main, and nothing in `implement` prevents it |
| A4 | No user outside this repo has `/implement` in a saved workflow or muscle memory | n/a | Moot. Q1 resolved toward keeping the skill, so nothing rests on this. |
| A5 | The tails of `feature`, `bug-fix`, and `refactoring` are the same sequence with per-type flavor, so they collapse into one verb | 3 | Partly false, found while building slice 2. The **close-out** (review, no-comments, commit) is identical in all three and collapses cleanly. The **build loop** does not: `refactoring.md:8` requires the full suite green per unit, which contradicts `implement.md:33`. See A6. |
| A6 | A behavior-preserving unit needs the full suite per unit, because the suite is the proof; a feature slice does not | 4 | `refactoring.md:3` states the playbook is behavior-preserving and "the tests prove it". Landed as `implement`'s cadence exception in `40065ab`; `probe_tails.py` goes red without it. |

A5 was the assumption carrying the plan and slice 2 partly falsified it, which is what grading it was for. The close-out collapses in all three playbooks. The build loop needed one clause added to `implement` (A6) before `refactoring` could collapse without contradicting it, and it needed two of `refactoring`'s steps reordered so nothing sits after the build phase. Both are inside slice 2 rather than new work.

## Verification

**Acceptance checks:**

- `grep -rn "Commit your work" skills/` returns nothing.
- `grep -rniE "full test suite|typecheck|single test file" skills/` returns exactly one intentional statement of the cadence rule.
- `python3 scripts/check-skill-refs.py` exits 0.
- Invoking the axo-mode feature playbook end to end reaches `tdd`, `code-review`, `no-comments`, and Committing through `implement`, with no step naming a skill that does not exist and no step restating one `implement` already owns.

**Feature map:** this repo has no `verify-<app>` skill. The artifact under test is Markdown read by an agent, not an app with a user-facing surface, so `/create-verification-skill` does not apply here. The check script in slice 3 is the closest equivalent and is why it is in scope.

## Out of scope

- The broader question of whether `to-tickets`, `triage`, and `work-linear-issue` should also collapse into playbooks. Same shape of question, four times the blast radius.
- Renaming the Linear-specific skills (`to-linear-issue`, `work-linear-issue`) whose bodies are tracker-agnostic.
- Extracting blast-radius's evidence ladder into a shared reference now that `plan` is a second consumer.

## Open decisions

None. All three resolved and moved to the decision log below.

## Decision log

- **Q3** Ship the check here rather than filing it separately. Resolved 2026-08-20 on evidence rather than preference: running its logic ad hoc during a review of all 57 skills turned up 28 live defects that had been in the repo since the initial scaffold. A check that finds 28 real problems before it exists has made its own case.
- **Q2** The test-cadence rule stays in `implement`, which now owns the build loop. The full-suite half needs no new home: Committing step 2 already runs the repo's gates before a commit. Resolved 2026-08-20, as a consequence of Q1 rather than on its own evidence.
- **Q1** Keep `implement` and write it as the build-phase verb, rather than deleting it or reducing it to a router. Plan, implement, and review are one verb per phase, each routing into the library, while the playbooks stay on the task-type axis. Resolved 2026-08-20 by the user, against this plan's original recommendation. The deletion case was falsified by `code-review` holding the identical slot with 87 lines of content, and by the fact that deleting leaves the three playbook tails duplicated.
