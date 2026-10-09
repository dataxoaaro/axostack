---
name: code-review
description: "Review the diff since a fixed point on four axes (Standards, Spec, Correctness, Complexity), plus Security at trust boundaries, and verify each finding against the code. Use for a branch, PR, WIP, or 'review since X'."
---

Four-axis review of the diff between a fixed point and the code under review, plus a fifth when the change touches a trust boundary:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?
- **Correctness**: does the code work, including edge cases, failure paths, and callers outside the diff?
- **Complexity**: what could the change do without? Code that skipped a simpler solution that holds.
- **Security**, conditional: can a lower-trust principal cross a trust boundary the change creates or modifies? Uses the **security-audit** skill's evidence bar in guidance mode.

Each axis runs as a **parallel sub-agent** so they don't pollute each other's context. A script precomputes the diff, commits, and callers once, and every axis reads that instead of re-running git. Each axis verifies its own findings; this skill re-checks the expensive claims and aggregates.

The issue tracker should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the user to run `/setup-axostack`.

Two modes:

- **Full review**, the default: every step below.
- **Re-review since `<sha>`**: a caller (such as `idea-to-pr`'s repair rounds) passes `re-review since <sha>`, the head, and the prior findings. Only the fix commits are reviewed. See [Re-review since a commit](#re-review-since-a-commit).

## Process

### 1. Pin the fixed point and the code under review

Whatever the user or calling skill said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If none was given, use the merge-base with the default branch and say which ref you used.

Confirm the fixed point resolves (`git rev-parse <fixed-point>`) before going further. A bad ref should fail here, not inside four parallel sub-agents.

Pin the code under review:

- **A caller pinned a head SHA** (as `idea-to-pr` does): review exactly `git diff <fixed-point>...<head>`. Don't include the working tree.
- **Otherwise:** review the branch plus uncommitted work. With a clean tree, the diff is `git diff <fixed-point>...HEAD`. With uncommitted changes, it is `git diff $(git merge-base <fixed-point> HEAD)` plus every untracked file, read in full. The step 2 script applies this rule.

### 2. Build the review context

Run [`scripts/review-context.py`](scripts/review-context.py) from this skill's directory, once, inside the repo:

```
python3 <skill-dir>/scripts/review-context.py <fixed-point> [--head <sha>]
```

Pass `--head` when a caller pinned one; leave it off to include the working tree. The script is read-only. It writes a directory under the OS temp dir and prints its path with a summary: the diff command it used, commit and file counts, changed lines, whether the diff is large, and changed lines per directory. The directory holds `commits.txt`, `files.txt`, `untracked.txt`, one diff per changed file under `diff/`, `symbols.txt` (names defined or edited in the hunks of code files), and `callers.txt` (`git grep -n -w` hits for each of those names across the repo). Zero changed files ends the review here.

Then run the repo's test command once, but only when the code under review is the user's own work or the user asks for it. The command and the tests come from the tree under review, so on someone else's PR they run that author's code with the user's credentials. For someone else's PR, write `skipped: untrusted code, ask the user` to `tests.txt` and run nothing. Find the command in `CLAUDE.md`, `AGENTS.md`, `package.json` scripts, `pyproject.toml`, or the `Makefile`. Save its output and exit code to `tests.txt` in the context directory. When no command is documented, or the checked-out tree is not the code under review, write that to `tests.txt` with the places you checked, and run nothing.

### 3. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user or calling skill passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.

When nothing is found, skip the **Spec** sub-agent and report "no spec available" with the places you searched. Don't ask.

Note whether the spec carries acceptance criteria: a plan slice's criteria, or a ticket's `## Acceptance criteria` section. The Spec axis checks them one by one.

### 4. Identify the standards sources

Search the repo for every file that documents how code should be written. `CODING_STANDARDS.md` and `CONTRIBUTING.md` are always checked, and each one that exists goes on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

Speculative Generality and Middle Man belong to the Complexity axis, so each finding is reported once.

### 4b. Decide whether the Security axis runs

The Security axis runs when the change touches a trust boundary. Check the changed file list and the diff for these signals; when unsure, run it. Each signal selects the **security-audit** skill's companion files the Security sub-agent reads:

| The diff touches | Companion files |
|---|---|
| Any signal below | `ATTACK-CLASSES.md`, always |
| Request handlers, authentication, sessions, tokens, cookies, CORS, redirects | `WEB-PROTOCOL-AND-AUTH.md` |
| LLM prompts, model output handling, RAG retrieval, agent memory, tool calls, MCP servers or clients | `AI-AND-LLM.md` |
| Terraform or other infrastructure as code, IAM policy, containers, Kubernetes, serverless or deploy configuration | `CLOUD-AND-DEPLOYMENT.md` |
| Dependency manifests or lockfiles, CI workflows, release, packaging, or plugin loading | `SUPPLY-CHAIN-AND-RELEASE.md` |
| Tenant or user data scoping, caches, search, export, backup, deletion | `DATA-ISOLATION-AND-LIFECYCLE.md` |
| Queues, webhooks, RPC, serialization formats, streaming | `PROTOCOLS-RPC-AND-MESSAGING.md` |
| Browser code, DOM rendering, `postMessage`, service workers | `CLIENT-SIDE.md` |
| Quotas, rate limits, worker pools, paid API spend | `RESOURCE-EXHAUSTION-AND-AVAILABILITY.md` |
| Native code, unsafe blocks, FFI | `MEMORY-SAFETY-AND-BINARY.md` |
| Desktop or mobile apps, deep links, local IPC | `DESKTOP-MOBILE-AND-LOCAL-IPC.md` |
| Input parsing, SQL, shell commands, file paths, outbound fetches, secrets, cryptography, deserialization | `ATTACK-CLASSES.md` alone covers these |

The companion files live in the security-audit skill's directory, `../security-audit/` relative to this skill's directory. Resolve that absolute path before spawning, and confirm it exists. When no signal matches, skip the axis and record which signals you checked.

### 5. Spawn the sub-agents

Issue every axis call in one message with the Agent tool, Correctness first, all in the foreground (`run_in_background: false`), and aggregate the reports they return. Use `subagent_type: "general-purpose"`. Standards, Spec, Complexity, and Security run on `model: "sonnet"`. Correctness runs on the session model, so leave its `model` unset. When the caller names reviewer models, use those instead.

Every prompt includes the context directory from step 2 and says: "Read `summary.txt`, `commits.txt`, `files.txt`, `untracked.txt`, the per-file diffs under `diff/`, `callers.txt`, and `tests.txt` in that directory instead of running `git diff`, `git log`, or the full test suite. Open source files in the repo for surrounding code; when the head is pinned and is not the checked-out tree, use `git show <head>:<path>`. Read-only. Do not edit, stage, or commit anything. One entry per finding with `file:line`, no preamble. Report every finding you can support; keep each one short instead of capping how many you report. The other axes have their own reviewers, so don't report or hand off findings outside your brief. Before you report a finding, verify it: open the cited lines, confirm they say what you claim, and run the cheap command that settles it. Drop any finding that fails, and say how many you dropped."

Each brief below ends with the check that axis applies to its own findings.

**Correctness sub-agent prompt** adds:

- The brief: "Find bugs, unhandled edge cases and failure paths, regressions in callers outside the diff, and changed behavior with no test. For each finding give `file:line`, the triggering scenario (concrete inputs or state), the impact, and the evidence: the code path, or a command you ran and its output. Check the callers of every changed function before judging it: start from `callers.txt`, and search for callers of any changed function it misses, such as a method whose body changed without its definition line or a hunk header naming it. Check scale too, which is fine for one user and wrong for many: check-then-write races, per-process state that breaks with more than one process, memory or lists that only grow, and a query or request per item in a loop. No triggering scenario means no finding. Style, conventions, and size belong to other reviewers; skip them. Bounds: spawn no sub-agents. The full test run is in `tests.txt`; run only targeted tests and read-only commands. When `tests.txt` says the tests were skipped as untrusted code, run no tests unless the user approves. Aim for about 25 tool calls; past that, report what you have and list what you did not reach. Verify: each triggering scenario is reachable from a real caller or input; run it when that is cheap."
- **Large diff.** When the summary says the diff is large (over 40 files or 2,000 changed lines), split Correctness into 2 or 3 agents by top directories, building the clusters from `files.txt` (and `untracked.txt`) and balancing changed lines. The summary lists at most 15 directories, so don't split from it. Each gets its own file list plus the full `callers.txt`, so callers in another cluster stay visible. Report their findings under one `## Correctness` heading.

**Spec sub-agent prompt** adds:

- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Verify: each quoted spec line exists and says what the finding claims."
- When the spec carries acceptance criteria, add: "Before the findings, return one table row per acceptance criterion: `criterion | pass, fail, or unclear | evidence`. Copy each criterion verbatim. Evidence is a `file:line` or a command and its output. `unclear` says what would settle it."

**Standards sub-agent prompt** adds:

- The list of standards-source files you found in step 4, **plus the smell baseline from step 4** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Duplicated Code means duplication inside the change. Speculative generality, dead code, unused parameters, and copies of code that already exists elsewhere in the repo belong to the Complexity reviewer; skip them. Verify: each cited standard exists in the file you name and says what you claim."

**Complexity sub-agent prompt** adds:

- The brief: "Hunt only for what the change could do without. For each new piece of code, the expected solution is the first of these that holds: it doesn't need to exist; it already exists in this repo; the standard library does it; a native platform feature does it (`<input type="date">` over a picker library, a database constraint over app code); an installed dependency does it; one line does it. Only then is new code justified. Flag code that skipped a step that holds. One line per finding: `<file>:L<line>: <tag> <what to cut>. <replacement>.` Tags: `delete:` dead code, unused flexibility, or a speculative feature, replaced by nothing. `stdlib:` hand-rolled code the standard library ships; name the function. `native:` code or a dependency doing what the platform does; name the feature. A component the repo already uses (a house component) beats a native widget, so never suggest `native:` to replace one. `reuse:` an equivalent helper, type, or pattern already in this repo; name the path. `yagni:` an abstraction with one implementation, config nobody sets, a parameter or hook the spec doesn't need, or a layer that only delegates. `shrink:` the same logic in fewer lines; show the shorter form. A replacement must keep the behavior, including edge cases such as which duplicate wins; when it doesn't, say what changes. Before a `delete:` or `reuse:`, search the whole repo for the symbol, including tests and string or dynamic references, and cite what you found. Never flag validation at trust boundaries, error handling that prevents data loss, security measures, accessibility, a single smoke test or self-check, or anything the spec explicitly asks for. Correctness and performance are out of scope. End with `net: -<N> lines, -<M> dependencies possible`, or `Lean already.` when nothing qualifies. Verify: rerun each `delete:` and `reuse:` search, and confirm the named stdlib function, platform feature, or existing helper covers what the code does, including its edge cases."

**Security sub-agent prompt**, when step 4b selected it, adds:

- The absolute path of the security-audit skill directory and the companion files step 4b selected.
- The brief: "Review the diff for security vulnerabilities only, in the security-audit skill's guidance mode: write no audit files and start no full audit. First read the skill's `SKILL.md` sections Universal execution safety, Core principles, and Anti-patterns, then each listed companion file. A finding names the lower-trust principal, the input or action they control, the intended control, the crossed boundary, the affected principal or resource, and the observed or owner-observable result, with a `file:line` source trace. Give confirmed findings a severity from the skill's anchors. When a decisive fact lives outside the repository, such as deployment, provider, proxy, or identity configuration, report `needs_validation` with the exact missing fact and no severity. Run target code only when every control in Universal execution safety is enforced; otherwise trace the source. Missing best practices and defense-in-depth advice are not findings. Verify: re-read the source trace from the lower-trust input to the affected resource, and confirm no control on that path stops it."

### 6. Re-check the findings

The axes verified their own findings. Re-open the cited lines of every Correctness and Security finding. Spot-check one or two findings per other axis; a failed spot check means re-checking the rest of that axis. A `needs_validation` Security finding keeps its status; confirm only that its missing fact really is outside the repository.

Drop a finding that fails the check, and add the drops to the axis's own count. Mark a finding `unverified` when you could not check it; don't drop it and don't assert it.

### 7. Aggregate

Present the reports under `## Spec`, `## Correctness`, `## Security`, `## Standards`, and `## Complexity` headings, with verified findings verbatim or lightly cleaned. The Spec section opens with the acceptance-criteria table when there is one. Do **not** merge or rerank findings across axes, because the axes are deliberately separate (see _Why separate axes_). Where two axes flag the same lines, keep both and cross-reference them. When the Security axis was skipped, its section says so and lists the signals checked. When the Spec axis was skipped, its section lists where you searched.

End with a one-line summary: verified findings per axis, findings dropped in verification per axis, acceptance criteria passed out of the total, the worst issue _within each axis_ (if any), the highest confirmed Security severity, and the Complexity axis's `net:` line. Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Re-review since a commit

`re-review since <sha>` reviews only the commits a repair round added. The caller passes the sha the prior review covered, the new head, and the prior findings with their axes.

1. Confirm `<sha>` is an ancestor of the head (`git merge-base --is-ancestor <sha> <head>`). When it is not, because the branch was rebased or force-pushed, say so and run a full review instead.
2. Run step 2 with `review-context.py <sha> --head <head>`. The diff is `git diff <sha>..<head>`.
3. Spawn the axes that ran in the prior review, as in step 5. Security also runs when the new hunks hit a step 4b signal. Each axis gets its own prior findings and the brief: "For each prior finding, report `fixed`, `not fixed`, or `regressed`, with `file:line` evidence. Then report new findings in the new hunks only." Correctness checks the new hunks and their callers, not the whole branch. Spec re-checks only the acceptance criteria that were `fail` or `unclear`.
4. Re-check as in step 6, then aggregate as in step 7. Each axis section opens with its prior-finding table: finding | status | evidence.

## Why separate axes

A change can pass any axis and fail another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
- Code that is on spec and conventional but breaks on an empty input or a caller outside the diff → **Spec and Standards pass, Correctness fail.**
- Code that works for every honest caller but lets one tenant read another's records through a changed query → **Correctness pass, Security fail.**
- Code that is correct, on spec, and conventional, but builds a 300-line date picker where `<input type="date">` holds → **Complexity fail.**

Reporting them separately stops one axis from masking another. Security runs only when the change touches a trust boundary, because its evidence bar is expensive to meet and most diffs give it nothing to check. Complexity runs on its own because the other reviewers read the code as given. Asking whether the code should exist at all needs a reviewer whose only job is that question.
