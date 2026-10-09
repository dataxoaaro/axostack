---
status: proposed  # proposed | active | superseded
date: 2026-10-09
superseded-by:
---

# axo-factory: what we want to build after the developer skills

This document records the target for the factory pack and the research behind it. It is not a plan yet. When the factory work starts, run `/plan docs/research/axo-factory-direction.md` to shape it and slice it into tickets. The decision to keep factory behavior out of the developer skills is [ADR 0001](../adr/0001-factory-behavior-lives-in-a-separate-pack.md).

## Goal

axo-factory turns a tracker issue into a reviewed draft PR with evidence, with no human present between the trigger and the merge. It then handles review comments and red CI on that PR. A human approves intent before work starts and merges at the end. Nothing crosses a one-way door (merge, deploy, force-push, an external message, spend) without a human.

Done when one labeled issue becomes a draft PR that carries its evidence and a verdict for each acceptance criterion. Every run must end with a machine-readable outcome, and none may report success when it did nothing.

## What axostack already provides

The developer skills cover every station except release and monitoring. See the station table in [the developer-skills record](lean-developer-skills-for-a-future-factory.md). axo-factory reuses their content and the headings of the documents they write. It adds only what running without a human needs.

| Station | axostack skill | What the factory version adds |
|---|---|---|
| Intake | `to-issue`, `triage` | Verifies the claim before labeling. Writes questions for the reporter into the needs-info template instead of asking. Never closes an issue as wontfix. |
| Planning | `plan`, `to-tickets` | Can reach `draft` but never `approved`. A human approves through a label or comment. Publishes tickets only from an approved plan. |
| Build | `implement`, `implement-spec`, `idea-to-pr` | Takes seams from the plan, skips slices gated on a decision, pushes only `factory/*` branches, opens draft PRs only. |
| Review | `code-review` | Reads only the pushed branch and returns a verdict for each acceptance criterion. Runs read-only. |
| Review feedback | `address-pr-feedback` | Runs on red CI or a review comment on a `factory/*` PR. At most two fix attempts, with the attempt count kept on the PR thread. |
| Process improvement | `retro` | Unattended runs only propose additions to the repo's notes. A human applies them. |

## Mechanisms

These are researched and mostly verified. Verify them again against current Claude Code docs when the work starts, because AI tooling changes quickly.

1. **One headless session per station.** A small runner starts each station with `claude -p "/<station> <ref>"`. Slash-only skills run this way: verified on Claude Code 2.1.295 on 2026-10-09. They do not run from `/loop` or Claude's scheduled tasks, so use cron or CI instead.
2. **Permission profile per station.** `--permission-mode dontAsk` denies anything not on the allowlist. `--permission-prompts none` removes `AskUserQuestion`. No profile lists merge, force-push, `gh api` writes, deploy, or messaging tools. Bash deny rules match command text and are not a security boundary. GitHub branch protection, which makes merge human-only, is the real gate.
3. **Structured outcome.** `--json-schema` makes every run end with `success`, `flawed`, `blocked`, or `manual`, plus links to its evidence. The runner checks this value and never the exit code. A headless run of `grill-me` asked its question as plain text and still reported `success`.
4. **Unattended rule.** The skill researches facts. It takes the recommended answer on a reversible decision and records it as assumed in the artifact. It posts any other question where a human will see it, such as a ticket comment or a draft PR, and stops with `blocked`.
5. **Eval gate.** `claude plugin eval` runs each station on fixture repos, with and without the pack. A station runs unattended only after its suite passes. The suite also holds safety cases: no push to main, the run stops on a decision, and a prompt-injection case. The exit code checks only the score with the pack loaded. The with-versus-without difference needs its own script.
6. **Triggers.** Start with a local runner or cron. The Linear MCP accepts an API key as a bearer token, so Linear works without an interactive login. Move to `anthropics/claude-code-action` once its open issues #1458 and #1646 are fixed. Both are silent failures with plugin skills.

## Before the first unattended run

pstack's overnight guide sets four conditions:
- A human has done the task by hand.
- The agent has the same tools and signals the human used.
- Every station proves its work and can stop the line.
- Someone has read the transcripts and turned repeated mistakes into checks.

Add to those:
- The five developer-skill PRs have landed.
- Branch protection is on for every target repo.

## Rough sequence

1. Write evals for code-review: seeded bugs, plus the safety cases.
2. Run code-review on every PR, headless and read-only, posting a comment. This tests the runner, the outcome schema, and the evals before anything writes.
3. Chain triage, plan draft, and implement into a draft PR on a `factory/*` branch.
4. Run `address-pr-feedback` on factory PRs.
5. Add a metrics script that counts merged PRs, closed issues, backlog size, and outcomes by type, reviewed monthly through `retro`.
6. Release and monitoring stations, once something real runs unattended.

## Open questions

❓ **Q1** - **Where axo-factory lives**: A second plugin in this repo, or its own repo?

➡️ A second plugin in this repo. The factory skills reuse axostack's content and the headings of its documents, and one repo keeps them in sync.

---

❓ **Q2** - **How factory skills reuse developer skills**: A thin factory skill that loads the developer skill plus the unattended rule, or a separate copy of each station?

➡️ Thin wrappers. A copy doubles the upstream-sync work. Confirm with a prototype on code-review first.

---

❓ **Q3** - **Trigger surface**: Linear issues, or GitHub issues?

➡️ Linear, through the local runner, because it is axostack's main tracker.

---

❓ **Q4** - **Eval budget**: How often should the full suite run? A full run of 15 cases with 3 runs each and two variants costs an estimated $50 to $150. That estimate is not verified. A minimal headless run cost $0.81.

➡️ Weekly, and before each upstream port. Run only the cases tagged fast on each PR.

## Sources

Retrieved 2026-10-09 unless noted.

- Claude Code docs:
  - headless: https://code.claude.com/docs/en/headless
  - permissions: https://code.claude.com/docs/en/permissions
  - plugin evals: https://code.claude.com/docs/en/plugin-evals
  - GitHub Actions: https://code.claude.com/docs/en/github-actions
  - scheduled tasks: https://code.claude.com/docs/en/scheduled-tasks
  - sub-agents: https://code.claude.com/docs/en/sub-agents
- vercel-labs/eve-software-factory-template: https://github.com/vercel-labs/eve-software-factory-template, last push 2026-10-07.
- Vercel, "Building a software factory for AI SDK", 2026-08-12: https://vercel.com/blog/building-a-software-factory-for-ai-sdk
- Linear MCP: https://linear.app/docs/mcp
- claude-code-action issues: https://github.com/anthropics/claude-code-action/issues/1458 and https://github.com/anthropics/claude-code-action/issues/1646
- pstack guide `07-overnight.md` in https://github.com/cursor/plugins, commit `2cbf585`.
- The earlier station model: [software-factory-2026-10-07.md](software-factory-2026-10-07.md).
