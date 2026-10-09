---
name: retro
description: "Retrospective on a session that went harder than it should have. Fixes target this skills library (approved edits from three transcript reviewers) or the worked-on repo (checks, pointers, standards, steering files), each traced to the session. Use for /retro."
disable-model-invocation: true
metadata:
  credits:
    retro:
      author: Matt Pocock
      url: "https://github.com/mattpocock/skills"
    reflect-and-correct:
      author: Lauren Tan
      organisation: pstack
      url: "https://github.com/cursor/plugins/tree/main/pstack"
---

The user has asked for a **retrospective**. You are suggesting improvements that make the next agent's run go better, each traced to a moment in a session.

## 1. Pick the target

- **This skills library.** A skill misfired, didn't trigger when it should have, or a working recipe emerged that no skill captures. The fixes are edits to existing skills in the axostack checkout. Run [Library target](#library-target).
- **The worked-on repo.** The session struggled because of the repo: slow to find things, a mistake a check could catch, missing information. The fixes land in that repo and in the user's global steering files. Run [Repo target](#repo-target).

Take the target from the invocation (`/retro library`, `/retro repo`) or from what went wrong in the session. When neither settles it, ask once, with your recommendation. A session can feed both targets, one after the other. Structural improvements to the code go to `/improve-codebase-architecture` in either case.

Apply the **technical-writing** and **unslop** skills to every skill edit, steering file, standard, or doc you propose.

## 2. Find the session

Read the primary sources for the session the user specifies. If the user doesn't specify one, default to the current session. Claude Code transcripts live under `~/.claude/projects/<slug>/`, where `<slug>` is the working directory path with each "/" turned into "-" (so `/Users/you/proj` becomes `-Users-you-proj`). Read only the active project's directory. Do not glob across `~/.claude/projects/*/`; that crosses project boundaries and reads private chats from unrelated projects.

```bash
ls -t ~/.claude/projects/<slug>/*.jsonl 2>/dev/null | head -10
```

Each transcript is one JSONL file named by session id. For each candidate, read the first JSONL line and check that `message.content[0].text` contains the conversation's opening user prompt. Take the matching path. If no path resolves, write a tight digest of the session and pass that instead.

## Library target

Mine the session for durable learnings, then route them into skill edits. Skip it when the conversation is trivial, off-topic, or already covered by an existing skill the agent followed correctly. One-offs are not learnings.

### Spawn three reviewers in parallel

One message, three Agent tool calls with `subagent_type: "general-purpose"` so they run in parallel. Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript); readonly strips MCPs. The prompt forbids file writes; the parent applies edits.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your strongest judgment model (default: the session model) | `references/judgment-reviewer.md` |
| Tooling | your strongest instruction-following model (default: the session model) | `references/tooling-reviewer.md` |
| Divergent | your strongest judgment model (default: the session model) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their final report.

### Synthesize

One Agent tool call with `subagent_type: "general-purpose"` on your strongest judgment model. The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

Then sanity-check the Accepted list. Move any item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog, per [encode-lessons-in-structure](../axo-mode/principles/encode-lessons-in-structure.md).

### Apply

Before applying any Accepted edit, present the full Accepted / Rejected / Backlog output and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent; do not auto-apply.

Backlog items are checks or tooling, not skill edits. List them for the user. Build one under the repo target, or file it with `/to-issue`, only when the user asks.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): apply it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than about 10 lines): draft the edit in the target skill's own voice and check the section still reads cold to an agent that has never seen this session.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): rewrite the description as a routing rule with explicit use and skip conditions; the description is all the agent sees when deciding to load the skill.
- `new skill: <kebab-name>`: create the folder and SKILL.md following the conventions of the skills already in this repo. Do not invent a new shape ad hoc.

Run the library's checker (`python3 scripts/check-skill-refs.py`) on the result before declaring done.

An edit in a checkout is not in effect. Skills run from an installed copy, so every applied edit stays invisible to the next agent until that copy is updated. Run the repo's sync script if it has one, and verify the install matches before you call the retro done.

Reply with a short list, no preamble: edits applied (`<skill path>`, one line each), new skills created (rare), backlog items (one line each), and dropped findings with the synthesizer's reason.

## Repo target

The environment is the repo the session worked in and the user's global steering files.

1. Look for candidates for improvement in these categories.

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Linting, typing, tests, filesystem linters? Read the repo's own check command first (its `package.json`/build-tool `lint`/`check` scripts, its CI workflow), so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint/typecheck/test command) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards**: should the **reviewer agent** be given a new rule to enforce? Should an existing rule be removed or clarified? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop: a custom rule in the repo's own linter, a new pre-commit hook, or a new CI job, whichever the repo's language and existing guardrail make cheapest. Default to building the check over writing the rule. Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could ever substitute for). _Use when_ the reviewer agent failed to catch a mistake.
- **Global CLAUDE.md / AGENTS.md**: are there any steering instructions that should be moved to coding standards (or automated checks) instead? _Use when_ the CLAUDE.md or AGENTS.md file is particularly large, in the repo or the user's global scope (`~/.claude/CLAUDE.md` and `~/.claude/rules/`).
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLI's, MCP's) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **No-ops**: look for instructions in steering files that don't modify the agent's behavior. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent.

Every candidate cites the moment in the session that produced it: the message, the tool call, or the failing command. Discard a candidate you cannot trace, because a category with no evidence invites generic advice. Where a check already exists but is unwired or broken, the finding is to wire or fix it, not to build a new one. Mechanical rules go into checks per [encode-lessons-in-structure](../axo-mode/principles/encode-lessons-in-structure.md).

2. For a mistake the agent made, check whether it recurs. Read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds for the same mistake. A mistake class counts once it has happened twice. Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Fix each recurring class at the highest level that works:

   1. **Architecture.** One owner per piece of state, one supported way per task, internals hidden so the wrong import fails, one source of truth instead of hand-synced lists. Delete the old ways and dead code an agent would copy.
   2. **Types**, so the bad state cannot be written.
   3. **A lint or CI check** whose error message names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
   4. **Tests** of the behavior. Fix or delete any test that would still pass if every function it calls returned nothing.
   5. **Docs or agent rules**, last, and only for judgment calls. Nothing fails when an agent skips them.

3. Present the candidates to the user, in order of severity. For each: the category, the session evidence, the proposed fix, the file or check it lands in, and for a recurring class the level you picked and why a higher level didn't work.

4. Change nothing until the user picks candidates. Build each picked one under the **axo-mode** skill's playbooks. Each new check must fail on the real past mistake, from the session or the history, and pass once that mistake is gone. Run the same command locally and in CI. An exception goes on the offending line with a reason, an expiry date, and a human's approval. Close out through the Committing playbook.

5. Keep a table that pairs each rule with what enforces it, in `CODING_STANDARDS.md` or wherever the repo already keeps its agent rules. When the user corrects the same mistake again and the table shows nothing enforcing its rule, that is a repeat: fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure - it receives a diff, so no exploration needed. It often does not need to write code or debug.

This means that the review agent should be responsible for imposing coding standards, not the implementation agent.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. They should be used incredibly sparingly, usually only for **navigation pointers** to other files.
- `CODING_STANDARDS.md`: this file is read during review, not implementation. The **code-review** skill's Standards axis reads it, along with `CONTRIBUTING.md` and any other doc on how code should be written. No skill creates it. Propose it the first time a judgement-call rule appears. Add **navigation pointers** to docs folders if the standards file gets more than 1,000 lines long.
- Docs: use docs as references files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs (since their description goes into the agent's context window), or for user-invoked commands. Write them per the **technical-writing** skill.
