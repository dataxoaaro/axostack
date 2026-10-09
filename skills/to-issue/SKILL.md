---
name: to-issue
description: "Research a question, idea, or reported problem and publish it as one well-formed issue in the configured tracker (Linear first) with evidence, a proposed approach, and acceptance criteria. Use for 'make a ticket for X', 'research X and file it', or when a conversation surfaces work worth tracking before building it."
disable-model-invocation: true
---

# To issue

Turn an unshaped input into one researched, tracked issue. The research happens now, once, so the issue carries its evidence and whoever picks it up starts from decisions, not questions.

## Process

### 1. Load the tracker config

Read `docs/agents/issue-tracker.md`. If it doesn't exist, tell the user to run `/setup-axostack` and stop. The config names the team and binds the tracker operations; this skill is written for Linear but follows whatever the config says.

### 2. Classify the input and research it

- **Internal question** (how does our X work, why is Y slow, is Z safe to change) → fan out the **how** and **why** skills as parallel subagents over the affected subsystems, per axo-mode's [Subagents](../axo-mode/SKILL.md#subagents) section.
- **External question** (library capabilities, API behavior, ecosystem practice) → the `research` skill against primary sources.
- **Product or scope fork** no research can settle → a short pass of the `grilling` skill with the user. Only the forks that change the issue's scope; this is not a full grill session.

Every claim that survives into the issue cites its evidence: a file path, command output, measurement, or primary source. Never fabricate a citation.

### 3. Draft the issue

- **Title**: imperative, in the project's domain language (`GLOSSARY.md` vocabulary when it exists).
- **Problem**: what is wrong or missing, with the evidence from step 2.
- **Proposed approach**: the shape of the fix or build, and the alternatives research ruled out with one line each on why.
- **Out of scope**: what this issue deliberately does not cover.
- **Acceptance criteria**: observable checks, each one verifiable by running something.

Avoid specific file paths and code snippets; they go stale. Exception: a snippet that encodes a decision more precisely than prose can (a type shape, schema, state machine), trimmed to the decision-rich part.

### 4. Confirm and publish

Show the user the draft. Let them edit. Then create the issue per the tracker config, apply the `needs-triage` label (or `ready-for-agent` when the user says it's ready to build), and report the issue key and URL.

### 5. Too big for one issue

If research reveals a multi-slice effort, say so: propose `/to-tickets` for a dependency-ordered breakdown, or `/wayfinder` when the path itself is unclear. Publish the map or the tickets instead of one bloated issue.

**Reply:** the issue key and URL, the evidence that shaped it, and what research ruled out.
