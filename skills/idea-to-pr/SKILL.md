---
name: idea-to-pr
description: "Take an idea, a fix, or an existing Linear issue through investigation, a plan, the issue, an isolated worktree, a PR, and independent reviews with repairs. Run bare to take the next ready issue. A local mode stops at commits on the branch. Use for /idea-to-pr, 'work on issue <key>', or 'pick up the next ready issue'."
disable-model-invocation: true
---

# Idea to PR

Deliver a verified PR with review findings addressed. Own the sequence below; use the build and review skills where named. `/to-issue` and `/to-tickets` remain separate entry points that stop at the tracker.

## Pick the input and the mode

- **A request** (`/idea-to-pr <idea or fix>`, or a `/research-idea` decision record) → a new issue, created below.
- **An issue key** (`/idea-to-pr <issue-key>`) → that existing issue, per step 3 below.
- **Nothing** (`/idea-to-pr` run bare) → read `docs/agents/issue-tracker.md`. If it doesn't exist, tell the user to run `/setup-axostack` and stop. Otherwise query the frontier: open issues labeled `ready-for-agent` with no open blockers and no assignee. Take the first in the tracker's priority order, assign it to the authenticated user, and name it in your first progress update. An empty frontier ends the run with that report.

An issue with open blockers does not start. Report the blockers and stop.

**Local mode** runs when the user asks for it (`/idea-to-pr --local <issue-key>`, "don't push", "local only"). It follows the same flow through implementation and the **implement** skill's local review, then commits on the task branch and stops. It never pushes, opens a PR, or publishes a PR review summary. Its authorization covers the issue updates and local commits only. Close out by commenting on the issue with what changed, how it was verified, the branch name, and any leftovers, then move the issue to In Review. Return the issue link, branch, commit list, gate results, and worktree path. Pushing later is a separate request.

## Establish the task and destination

1. Read the repository instructions, git status, remotes, and `docs/agents/issue-tracker.md` when present. Identify the repository and intended base branch. Preserve unrelated edits.
2. Discover the available Linear and PR tools and their authenticated connections. Tool names vary. A Linear connection may expose only one workspace; do not treat teams as workspaces or promise access to unconnected workspaces.
3. For an existing issue, first fetch its description, comments, and blockers. Reuse its workspace, project, and key. Preserve its assignee unless a change is requested. Skip the new-issue selections below. Ask only when its connection cannot be resolved or a requested reassignment is ambiguous. Do not move it between workspaces or create a replacement issue automatically.
4. For a new issue, take the workspace, team, and project from the user's request, then `docs/agents/issue-tracker.md`, then the connected tracker. Check the configured project against the task, and when it does not fit, inspect the candidate projects for one that does. Missing repository configuration does not block discovery through the connected tools. Verify that the selected connection belongs to the workspace before writing. If it is unavailable, request the connection and continue repository investigation meanwhile.
5. Assign the authenticated user unless the user named another assignee, and resolve the actual user ID in the selected workspace.
6. Ask only when a selection has zero or several equally good matches. Batch those selections into one question, each with your recommendation, per axo-mode's [question rule](../axo-mode/SKILL.md#autonomy). Do not treat silence as a selection.

A request to execute this complete workflow authorizes creating and updating its issue, committing and pushing its task branch, creating and updating its PR, and publishing the review summary there. Carry that authorization through delegated skills without asking again. Skill discovery or a request to discuss the workflow is not authorization to execute it. Merging, deployment, force-pushing, and unrelated changes require separate authorization, as one-way doors or new scope under the question rule.

## Investigate and plan

When the request is a `/research-idea` decision record, its chosen approach and requirements are settled input. Do not reopen the choice unless the code contradicts the record's evidence.

Trace the affected code, tests, and relevant history before proposing a fix. For bugs, reproduce the failure and identify its cause, using the **diagnosing-bugs** skill when needed. For changes, identify the current behavior and the requested result. Resolve only questions that change scope, design, or acceptance criteria, asked per the question rule; continue independent investigation while answers are pending. For an existing issue, append the decisions resolved this way to it as a comment, so the tracker stays the source of truth.

Write a plan proportional to the task. Use the **plan** skill when the change needs substantial design or multiple slices. Keep the plan local until the destination and scope are settled. Do not publish tickets from a nested planning workflow; this workflow owns issue creation. Its planning handoff returns here: the user's request for this complete workflow authorizes continuing into implementation once blocking decisions are resolved. Do not label a plan user-approved without an explicit approval.

The issue description must contain:

- The problem and desired behavior, with evidence from code, reproduction, or primary sources.
- The implementation approach and ordered steps, including affected components and significant design decisions.
- Scope boundaries, dependencies, and unresolved decisions that block implementation.
- Observable acceptance criteria and the commands or user flows that will verify them.

Show the plan in a progress update and proceed under the existing authorization when no blocking decisions remain. If the request expands into independently deliverable work, resolve the scope or ticket breakdown with the user before publishing a larger effort.

## Create the issue and isolate implementation

Search the selected project for a matching issue before creating one. Reuse a confirmed match. Do not adopt a vaguely similar issue without checking its scope.

If no confirmed matching issue exists, create it in the selected workspace, team, and project, with the resolved assignee and plan. Otherwise reuse the confirmed issue and update its plan as needed. Preserve its destination and assignee unless the user requested a change, including when the match was found after new-issue selections. In either case, record the issue ID, key, and URL, then read it back to verify its destination and assignment. Set the team's In Progress state when implementation starts. Open blockers prevent dependent implementation.

Create a dedicated git worktree from the agreed base. Transfer only this task's plan and investigation artifacts into it before implementation, preserving unrelated work in the original checkout. Obtain the real issue key before naming the branch. Use these conventions:

| Artifact | Format | Example |
| --- | --- | --- |
| Branch | Lowercase issue key, then a short kebab-case description | `axo-123-fix-session-expiry` |
| PR title | Uppercase issue key in brackets, then a concise imperative description | `[AXO-123] Fix session expiry during checkout` |
| PR body | The **pr** skill's template, ending with the Linear issue URL | Link the actual issue returned by Linear |

Keep the issue prefix first, even when the repository uses conventional PR titles: `[AXO-123] fix: Preserve the checkout session`. Update the description when scope changes while retaining the key. Commit messages follow repository conventions, with the issue key in the body rather than in code.

Before reusing a branch or worktree, verify that it belongs to this task. Never reset, delete, or overwrite another task's work to claim its name. Perform implementation, installs, tests, and commits in the task worktree. Isolate ports and generated outputs when the repository requires them.

Build through the **implement** skill against the issue's plan, applying **tdd** for behavior changes. Supply the issue as the spec and the base commit for its reviews. Carry the task's push authorization into its committing steps. Update the issue if implementation changes the plan materially.

## Open and review the PR

After local verification, push the task branch and create a draft PR against the agreed base. Reuse an existing PR for that repository and branch. Apply the title format above and link the issue in the PR body. Add the PR URL to Linear.

Capture the merge-base SHA and PR head SHA. All reviewers inspect that same committed revision and can read the surrounding source and tests. Do not edit the reviewed worktree until their reports return.

Invoke the **code-review** skill with the pinned base, head, issue spec, and repository standards. It runs independent, read-only reviewers in parallel and owns the separate Spec, Correctness, Standards, and Complexity reports.

Give reviewers the source evidence without the implementer's conclusions or each other's reports. If concurrency is limited, queue reviews while retaining separate contexts. If subagents are unavailable, disclose the limitation and perform the review passes sequentially; do not claim independent reviews ran.

Use the user's configured reviewer models when available. Otherwise inherit the runtime's model. Different models may review different responsibilities when the runtime supports explicit model selection. Report which models actually ran. External providers require a configured, authorized CLI or API connection; never silently substitute a provider or claim model diversity that did not occur.

Keep the four axes' findings separate. Reconcile duplicates with cross-references. Validate each finding against the code or a reproduction; agreement between models is not proof. Record each finding as fixed, rejected with evidence, or unresolved.

Fix valid findings in the task worktree, run affected checks, commit, and push. Then invoke the **code-review** skill in its re-review mode, passed as `re-review since <sha>` with the head the previous review saw as `<sha>`, plus the prior findings and their dispositions. It reviews only the fix commits and checks each prior finding at the new head. After two repair rounds, leave the PR in draft if blockers remain and report them. Do not cycle indefinitely or mark unresolved blockers as passed.

## Verify and hand off

Check that local verification, required CI checks, and reviews apply to the latest PR head. Changes after review invalidate the affected review results. Report unavailable or failing checks explicitly. Mark the PR ready only when verification and required checks pass and no blocking findings remain.

Publish a concise review summary on the PR with the reviewed SHA, reviewer responsibilities and models, findings, and dispositions. Update Linear with verification and the PR link. File each leftover as its own new issue rather than a vague note. Move it to the team's In Review state when ready. Do not mark it Done before merge.

Return the Linear link, PR link, worktree path, verification results, and unresolved concerns. Retain the worktree for follow-up unless cleanup was requested.

## Resume without duplicates

Apply [make-operations-idempotent](../axo-mode/principles/make-operations-idempotent.md). Keep a task record under the repository's git common directory, outside tracked source files, in `idea-to-pr/<task-id>.json`. Choose a unique local task ID before the first external write.

Record the repository, selected Linear connection and workspace, team, project, assignee, issue ID and key, worktree, branch, base SHA, PR URL, phase, reviewed head, verification results, and review findings with their dispositions. Record intended creates before sending them and returned identifiers immediately afterward. Never store credentials.

On resume, reconcile the record with Linear, git worktrees, branch history, and the remote PR before acting. After an ambiguous create or push response, search or read the destination to determine whether it succeeded before retrying. Live state takes precedence over a stale phase marker. Recheck verification and reviews when the head differs from the recorded revision.
