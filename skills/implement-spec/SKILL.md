---
name: implement-spec
description: "Land a whole spec in one run: read its tickets as a task graph, build every unblocked ticket at once in background implementer subagents with their own worktrees, merge each into one integration branch, then review and fix once. Use for /implement-spec with a plan or parent issue whose tickets carry blocking edges. Skip for a single ticket or fewer than three unlinked tickets, where `implement` or `/work-linear-issue` fits."
disable-model-invocation: true
---

# Implement spec

You have been given a spec. It has tickets with blocking edges, written by the **to-tickets** skill, or a plan under `docs/plans/` whose Slices table has a Blocked by column.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way this skill's tracker rules below describe.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. There is always a **frontier**: the tickets whose blockers have all merged into the integration branch. Every frontier ticket runs at once.

You are the orchestrator. Do no implementation yourself, per **principle-guard-the-context-window**. Communicate with subagents through **context pointers**: the spec, the ticket, the shared notes file, and commits. Don't paste what a pointer already holds.

## Inputs

1. Read `docs/agents/issue-tracker.md`. If the spec is a tracker issue and the file is missing, tell the user to run `/setup-axostack` and stop. A plan file needs no tracker.
2. Read the spec and every ticket, including comments and blocking edges. Build the graph. A cycle, an edge to a ticket outside the spec, or a ticket with open questions stops the run; report it. For a plan, apply the **implement** skill's Input rules to its Assumptions and Open decisions tables.
3. Name the seams for each ticket. Implementers run in the background and cannot confirm seams with the user, so the seams named in the ticket or spec are the agreed seams for the **tdd** skill. A behavior-changing ticket with no named seams is an open question under step 2.
4. Check the frontier for collisions. Two tickets that will touch one shared file (a registry, a message catalogue, a shared type) either get a blocking edge between them, or the shared notes fix the exact names each adds. Worktrees postpone collisions to merge time. They do not prevent them.
5. A graph with one ticket, or no edges and fewer than three tickets, gains nothing from this skill. Say so and recommend the **implement** skill.

## Run record

Keep the run's state in `$(git rev-parse --git-common-dir)/implement-spec/<spec-slug>/`, outside the tracked tree and visible from every worktree:

- `run.json`: base SHA, integration branch and worktree, and per ticket its state (`waiting`, `running`, `merged <sha>`, `failed`), branch, worktree, and retry count.
- `notes.md`: exploration notes every implementer reads.

Write a state change before acting on it, per **principle-make-operations-idempotent**. On resume, reconcile `run.json` with `git worktree list`, branch history, and the tracker before spawning anything. Live state wins over the record.

Compute the frontier from `run.json`, not from the tracker. Blocked-by counts on a tracker drop only when a blocker closes, which is after the run ends.

## Steps

1. Optional: spawn one exploration subagent for what the tickets need from the codebase or external docs. It writes `notes.md` and nothing else.
2. Create the integration branch from the agreed base, prefixed with the parent issue key when there is one (`abc-123-short-slug`), and check it out in its own worktree. Leave the user's checkout alone.
3. For each frontier ticket, spawn an implementer with the Agent tool: the `axo-agent` agent (`axostack:axo-agent` when this library is installed as a plugin), `isolation: "worktree"`, `run_in_background: true`. The brief names the spec, the ticket, `notes.md`, the integration branch, and its own branch name. Each implementer:
   - confirms its worktree is based on the integration branch tip, and resets onto it if not;
   - builds the ticket with the **tdd** skill at the seams the brief names, or says which kind of change it is when tdd does not apply;
   - runs the repo's format, lint, and type gates and the test files it touched;
   - commits on its own branch, with the ticket key in the message body and never in code;
   - merges the integration branch tip into its branch, reruns its tests, and reports the branch, head SHA, gate results, and any verification it could not run.
   It does not push, open a PR, run code-review, or touch the tracker.
4. Assign each ticket to the user and move it to In Progress when its implementer starts, so `/work-linear-issue` does not pick it up in another session.
5. When an implementer reports, run `git merge --ff-only <ticket-branch>` in the integration worktree. Once one branch has merged, the other parallel branches are behind the tip, so expect this to fail often. On failure, spawn a merger subagent in the ticket's worktree. It merges the integration tip into the ticket branch, resolves conflicts in favour of both tickets' acceptance criteria, reruns the affected tests, and reports the new head SHA. Then retry `--ff-only`. Merge one branch at a time. The orchestrator is the only writer to the integration branch, per **principle-separate-before-serializing-shared-state**.
6. After each merge, record `merged <sha>` in `run.json`, comment the SHA on the ticket, and move it to In Review. Recompute the frontier and spawn implementers for every newly unblocked ticket.
7. A failed implementer gets one retry with its failure as a pointer. A second failure marks the ticket `failed`, and its dependants stay `waiting`. Keep running the rest of the graph.
8. Once every ticket is merged or failed, run the full test suite in the integration worktree. Then run the **code-review** skill once, with the base SHA as the fixed point, the integration tip as the pinned head, and the whole spec as its Spec input. Never review before every ticket has landed, because each unbuilt ticket reads as a finding.
9. Spawn one fix implementer in its own worktree, based on the integration tip. It fixes every valid finding, runs the **no-comments** skill over the base SHA to its head, and reports like a ticket implementer. Merge it as in step 5. Then check only the fixed findings and rerun the full suite. Do not start a second broad review. Findings that survive the fix are reported, not looped on.
10. For a plan input, set each merged slice's Status to `landed <sha>` from `run.json`, in one commit on the integration branch. Run axo-mode's Committing playbook on the integration branch. Push and open a PR only when the user asked for one when invoking this skill. Otherwise ask before pushing. The **pr** skill writes the body. Open it as a draft when a blocking finding survived step 9, and ready for review otherwise.
11. Remove the implementer worktrees and branches recorded in `run.json` once they have merged. Keep the integration worktree, and keep the worktrees of failed tickets for inspection.

Never move a ticket to Done. That happens when the work reaches the default branch.

A ticket whose verification reads gitignored fixtures, local databases, or credentials can skip silently inside a worktree. Flag it in the brief. After the merge, copy or link the named untracked files from the user's checkout into the integration worktree, run the verification there, and record that you did.

**Reply:** integration branch and worktree, merged tickets with SHAs, failed tickets with the reason, review findings and their dispositions, gate results, verification gaps, and the PR link if one was opened.
