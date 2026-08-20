---
name: work-linear-issue
description: "Pick up a Linear issue by key and drive it to a reviewed, locally committed change on a correctly named branch, with the issue updated. Use for 'work on ABC-123', 'pick up the next ready issue', or starting any tracked piece of work."
disable-model-invocation: true
---

# Work Linear Issue

Drive one tracked issue from key to reviewed local commits. The issue is the spec; axo-mode is the discipline; this skill is the glue between them and the tracker.

## Process

### 1. Load the tracker config and pick the issue

Read `docs/agents/issue-tracker.md`. If it doesn't exist, tell the user to run `/setup-axostack` and stop.

- **Key given** (`/work-linear-issue ABC-123`) → fetch that issue with its comments and blocking relations.
- **No key** → query the frontier: open issues labeled `ready-for-agent` with no open blockers and no assignee. Propose the first; let the user confirm or pick another.

An issue with open blockers does not start. Report the blockers and stop.

### 2. Claim it

Assign the issue and move it to the team's In Progress state. This is the session's first tracker write.

### 3. Align before building

The issue plus its comments is the spec. If requirements are still unclear or the design is contested, run the **grilling** skill, plus the **domain-modeling** skill when the repo has domain docs, and append the resolved decisions to the issue as a comment, so the tracker stays the source of truth.

### 4. Build under axo-mode

Enter the `axo-mode` skill and match the issue to its playbook: feature, bug-fix, or refactoring. Copy the playbook's steps verbatim into the todo list. Branch first, named with the issue key prefix (`abc-123-short-slug`), so Linear links the branch automatically.

Implementation runs through the `implement` skill, which drives `tdd` at the agreed seams and closes out with `code-review`.

### 5. Close out

- Run axo-mode's Committing playbook: gates green, conventional commits, the issue key in the message body and never in code.
- Comment on the issue: what changed, how it was verified, the branch name, and any decisions or leftovers, each leftover as its own new issue rather than a vague note.
- Move the issue to In Review. Never move it to Done for work that hasn't landed, and never push to remote without explicit approval.

**Reply:** issue key, branch, commit list, gate results, open decisions.
