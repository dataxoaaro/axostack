---
name: idea-to-pr
description: "Take a requested idea or fix through investigation, an implementation plan, a Linear issue, an isolated worktree, a PR, and independent reviews with repairs. Use for /idea-to-pr or when the user asks for this complete workflow. Skip discussion-only requests and requests that stop at planning, ticket creation, or review."
---

# Idea to PR

Deliver a verified PR with review findings addressed. Own the sequence below; use the build and review skills where named. The separate ticket-creation and ticket-execution entry points retain their standalone workflows.

## Establish the task and destination

1. Read the repository instructions, git status, remotes, and `docs/agents/issue-tracker.md` when present. Identify the repository and intended base branch. Preserve unrelated edits.
2. Discover the available Linear and PR tools and their authenticated connections. Tool names vary. A Linear connection may expose only one workspace; do not treat teams as workspaces or promise access to unconnected workspaces.
3. For an existing issue, first fetch its description, comments, and blockers. Reuse its workspace, project, and key. Preserve its assignee unless a change is requested. Skip the new-issue selections below. Ask only when its connection cannot be resolved or a requested reassignment is ambiguous. Do not move it between workspaces or create a replacement issue automatically.
4. For a new issue, ask which Linear workspace to use unless the user already selected one for this task. Show the accessible workspace names when available, with the configured workspace as a suggestion. Verify that the selected connection belongs to that workspace before writing. If it is unavailable, request the connection and continue repository investigation meanwhile.
5. Within that workspace, use the configured team and project when they match the task. Otherwise inspect candidate projects and ask about ambiguity. Missing repository configuration does not block discovery through the connected tools.
6. Ask who to assign unless the user already specified an assignee. Suggest the authenticated user for "me", then resolve the actual user ID in the selected workspace. Bundle workspace, project, and assignee questions when practical. Do not treat silence as a selection.

A request to execute this complete workflow authorizes creating and updating its issue, committing and pushing its task branch, creating and updating its PR, and publishing the review summary there. Carry that authorization through delegated skills without asking again. Skill discovery or a request to discuss the workflow is not authorization to execute it. Merging, deployment, force-pushing, and unrelated changes require separate authorization.

## Investigate and plan

Trace the affected code, tests, and relevant history before proposing a fix. For bugs, reproduce the failure and identify its cause, using the **diagnosing-bugs** skill when needed. For changes, identify the current behavior and the requested result. Resolve only questions that change scope, design, or acceptance criteria; continue independent investigation while answers are pending.

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
| PR body | Problem, resulting behavior, verification, and the Linear issue URL | Link the actual issue returned by Linear |

Keep the issue prefix first, even when the repository uses conventional PR titles: `[AXO-123] fix: Preserve the checkout session`. Update the description when scope changes while retaining the key. Commit messages follow repository conventions, with the issue key in the body rather than in code.

Before reusing a branch or worktree, verify that it belongs to this task. Never reset, delete, or overwrite another task's work to claim its name. Perform implementation, installs, tests, and commits in the task worktree. Isolate ports and generated outputs when the repository requires them.

Build through the **implement** skill against the issue's plan, applying **tdd** for behavior changes. Supply the issue as the spec and the base commit for its reviews. Carry the task's push authorization into its committing steps. Update the issue if implementation changes the plan materially.

## Open and review the PR

After local verification, push the task branch and create a draft PR against the agreed base. Reuse an existing PR for that repository and branch. Apply the title format above and link the issue in the PR body. Add the PR URL to Linear.

Capture the merge-base SHA and PR head SHA. All reviewers inspect that same committed revision and can read the surrounding source and tests. Do not edit the reviewed worktree until their reports return.

Run independent, read-only reviewers in parallel:

- Invoke the **code-review** skill with the pinned base, head, issue spec, and repository standards. It owns the separate Standards and Spec reports.
- Run a separate correctness reviewer for bugs, edge cases, regressions, and missing tests. Require file and line references, the triggering scenario, impact, and supporting evidence for each finding. Avoid speculative style advice.

Give reviewers the source evidence without the implementer's conclusions or each other's reports. If concurrency is limited, queue reviews while retaining separate contexts. If subagents are unavailable, disclose the limitation and perform the review passes sequentially; do not claim independent reviews ran.

Use the user's configured reviewer models when available. Otherwise inherit the runtime's model. Different models may review different responsibilities when the runtime supports explicit model selection. Report which models actually ran. External providers require a configured, authorized CLI or API connection; never silently substitute a provider or claim model diversity that did not occur.

Keep Standards, Spec, and Correctness findings separate. Reconcile duplicates with cross-references. Validate each finding against the code or a reproduction; agreement between models is not proof. Record each finding as fixed, rejected with evidence, or unresolved.

Fix valid findings in the task worktree, run affected checks, commit, and push. Re-review the changed areas and prior findings at the new head. After two repair rounds, leave the PR in draft if blockers remain and report them. Do not cycle indefinitely or mark unresolved blockers as passed.

## Verify and hand off

Check that local verification, required CI checks, and reviews apply to the latest PR head. Changes after review invalidate the affected review results. Report unavailable or failing checks explicitly. Mark the PR ready only when verification and required checks pass and no blocking findings remain.

Publish a concise review summary on the PR with the reviewed SHA, reviewer responsibilities and models, findings, and dispositions. Update Linear with verification and the PR link. Move it to the team's In Review state when ready. Do not mark it Done before merge.

Return the Linear link, PR link, worktree path, verification results, and unresolved concerns. Retain the worktree for follow-up unless cleanup was requested.

## Resume without duplicates

Apply **principle-make-operations-idempotent**. Keep a task record under the repository's git common directory, outside tracked source files, in `idea-to-pr/<task-id>.json`. Choose a unique local task ID before the first external write.

Record the repository, selected Linear connection and workspace, team, project, assignee, issue ID and key, worktree, branch, base SHA, PR URL, phase, reviewed head, verification results, and review findings with their dispositions. Record intended creates before sending them and returned identifiers immediately afterward. Never store credentials.

On resume, reconcile the record with Linear, git worktrees, branch history, and the remote PR before acting. After an ambiguous create or push response, search or read the destination to determine whether it succeeded before retrying. Live state takes precedence over a stale phase marker. Recheck verification and reviews when the head differs from the recorded revision.
