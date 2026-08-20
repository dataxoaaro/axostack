---
plan: implement-skill-duplicates-the-feature-playbook
status: draft
created: 2026-08-20
tracker: none
branch: fix/model-invocable-skills
---

# Make the implement skill stop contradicting the playbooks it duplicates

## Done when

All four hold, each checkable by running something:

1. No skill body gives commit instructions that disagree with `skills/axo-mode/playbooks/committing.md`.
2. The test-cadence rule (typecheck regularly, single test files regularly, full suite once at the end) appears in exactly one place in the repo.
3. Every reference to `implement` resolves to something that exists.
4. `scripts/check-skill-refs.py` exits 0.

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

Retire `implement`. Rehome its one unique line, repoint its three references at the playbooks that already do the work, and delete the folder.

The routing entry becomes a pointer to the playbook rather than to a second description of it. `work-linear-issue:34` already names what actually happens ("drives `tdd` at the agreed seams and closes out with `code-review`"), so it loses only the indirection through `implement`.

This is **principle-laziness-protocol**'s "consolidate decisions": the build sequence is currently stated in two places that disagree, and the fix is one source of truth, not a better second copy.

## Alternatives rejected

- **Expand `implement` into a full skill** (60 to 80 lines, matching `triage` and `to-tickets`). Lost because it makes the duplication permanent and doubles the surface that can drift out of agreement with the playbooks. The defect is that the sequence is stated twice; a longer second statement is more of the defect.
- **Reduce `implement` to a three-line router** into axo-mode's playbook, the shape `grill-me` uses. Lost on a smaller margin. It keeps `/implement` working as a typed entry point and removes the contradiction. It also keeps a file whose entire content is "go read another file", which **principle-minimize-reader-load** treats as a one-caller wrapper to collapse. Kept as the fallback if Q1 comes back against deletion.

## What gets deleted

`skills/implement/` (14 lines), one routing entry in `skills/axo-mode/SKILL.md`, and one table row in `README.md`.

## Interface sketch

Skip: prose artifact, no types or signatures. The **architect** skill does not apply.

## Slices

| # | Slice | Blocked by | Delivers |
|---|-------|-----------|----------|
| 1 | Rehome the test-cadence rule into `tdd` | none | The cadence rule survives the deletion and lives in the skill that owns the build loop |
| 2 | Repoint the three references at the playbooks | 1 | `axo-mode:31`, `work-linear-issue:34`, and `README:10` describe the real sequence with no indirection |
| 3 | Delete `skills/implement/` | 2 | One statement of the build sequence in the repo |
| 4 | Ship `scripts/check-skill-refs.py` | 3 | A dangling or user-only skill reference fails a check instead of reaching an agent mid-task |

Slice 1 is reversible on its own and lands green. Slices 2 and 3 are the deletion wave, per **principle-migrate-callers-then-delete-legacy-apis**: callers move first, the old thing goes in the same wave, no deprecated stub left behind.

## Assumptions

| # | Assumption | Grade | Evidence |
|---|-----------|-------|----------|
| A1 | No file outside `skills/implement/` quotes its body, so rewriting or removing it breaks only the three name references | 4 | `probe_implement.py` over 110 Markdown files: 5 body sentences, 0 verbatim quotes, 3 name references |
| A2 | The test-cadence rule at line 10 is stated nowhere else | 4 | `grep -rniE "full test suite\|typecheck\|single test file\|whole suite" skills/` returns one unrelated hit in `refactoring.md:8` |
| A3 | `implement` contradicts `committing.md` rather than refining it | 3 | `implement:14` against `committing.md:5-6`; the bad case is an agent committing ungated on main, and nothing in `implement` prevents it |
| A4 | No user outside this repo has `/implement` in a saved workflow or muscle memory | 1 | **unproven**. This is a public plugin. Q1 exists because of this. |

A4 is the one that decides the plan and it is the one that cannot be proven from inside the repo.

## Verification

**Acceptance checks:**

- `grep -rn "Commit your work" skills/` returns nothing.
- `grep -rniE "full test suite|typecheck|single test file" skills/` returns exactly one intentional statement of the cadence rule.
- `python3 scripts/check-skill-refs.py` exits 0 with `implement` gone.
- Invoking the axo-mode feature playbook end to end reaches `tdd`, `code-review`, `no-comments`, and Committing with no step naming a skill that does not exist.

**Feature map:** this repo has no `verify-<app>` skill. The artifact under test is Markdown read by an agent, not an app with a user-facing surface, so `/create-verification-skill` does not apply here. The check script in slice 4 is the closest equivalent and is why it is in scope.

## Out of scope

- The broader question of whether `to-tickets`, `triage`, and `work-linear-issue` should also collapse into playbooks. Same shape of question, four times the blast radius.
- Renaming the Linear-specific skills (`to-linear-issue`, `work-linear-issue`) whose bodies are tracker-agnostic.
- Extracting blast-radius's evidence ladder into a shared reference now that `plan` is a second consumer.

## Open decisions

❓ **Q1** - **Delete `implement`, or reduce it to a three-line router?**: The repo is a published plugin, so `/implement` may be in someone's habits or a saved workflow. Deleting removes a typed entry point. The router keeps `/implement` working at the cost of a file that only forwards. A4 is unproven and cannot be proven from here.

➡️ Delete it. The routing entry and `work-linear-issue:34` already name the real sequence, so nothing that matters is lost, and a forwarding file is the one-caller wrapper **principle-minimize-reader-load** says to collapse. If you want the entry point kept, take the router and I will drop slices 2 and 3 to a repoint-only change.

❓ **Q2** - **Where does the test-cadence rule go?**: Options are the `tdd` skill, the Committing playbook, or the feature playbook. `tdd` owns the build loop and already sets the rules of red-green-refactor. Committing owns the gates that run once at the end. The cadence spans both: typecheck and single files run during the loop, the full suite runs at the end.

➡️ Split it. The during-the-loop half goes to `tdd`, the full-suite-before-commit half is already Committing step 2, so it needs one clause added rather than a new rule. Splitting keeps each half where the agent is already reading.

❓ **Q3** - **Ship the reference check (slice 4) here, or as its own change?**: The check also retro-covers the `disable-model-invocation` sweep in `42159b8`, which is a different piece of work.

➡️ Ship it here. Deleting a skill is the moment a dangling-reference check pays for itself, and it is roughly 30 lines. If you would rather keep this plan to the deletion, it moves out and I file it separately.

## Decision log

Empty. No questions resolved yet.
