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

Each axis runs as a **parallel sub-agent** so they don't pollute each other's context. This skill then verifies the findings and aggregates them.

The issue tracker should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the user to run `/setup-axostack`.

## Process

### 1. Pin the fixed point and the code under review

Whatever the user or calling skill said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If none was given, use the merge-base with the default branch and say which ref you used.

Confirm the fixed point resolves (`git rev-parse <fixed-point>`) before going further. A bad ref should fail here, not inside four parallel sub-agents.

Pin the code under review:

- **A caller pinned a head SHA** (as `idea-to-pr` does): review exactly `git diff <fixed-point>...<head>`. Don't include the working tree.
- **Otherwise:** review the branch plus uncommitted work. Run `git status --porcelain`. With a clean tree, the diff is `git diff <fixed-point>...HEAD`. With uncommitted changes, it is `git diff $(git merge-base <fixed-point> HEAD)`, which covers committed and uncommitted tracked changes, plus every untracked file from `git ls-files --others --exclude-standard`, read in full.

Note the commits via `git log <fixed-point>..HEAD --oneline`. An empty diff ends the review here.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

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

### 3b. Decide whether the Security axis runs

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

### 4. Spawn the sub-agents in parallel

Spawn all of them in one message with the Agent tool, `subagent_type: "general-purpose"`. Every prompt includes the diff command from step 1, the untracked-file list when there is one, and the commit list. Every prompt also says: "Read-only. Do not edit, stage, or commit anything. One entry per finding with `file:line`, no preamble. Report every finding you can support; keep each one short instead of capping how many you report. The other axes have their own reviewers, so don't report or hand off findings outside your brief."

**Standards sub-agent prompt** adds:

- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Duplicated Code means duplication inside the change. Speculative generality, dead code, unused parameters, and copies of code that already exists elsewhere in the repo belong to the Complexity reviewer; skip them."

**Spec sub-agent prompt** adds:

- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

**Correctness sub-agent prompt** adds:

- The brief: "Find bugs, unhandled edge cases and failure paths, regressions in callers outside the diff, and changed behavior with no test. For each finding give `file:line`, the triggering scenario (concrete inputs or state), the impact, and the evidence: the code path, or a command you ran and its output. Search for callers of every changed function before judging it. You may run the tests and other read-only commands. No triggering scenario means no finding. Style, conventions, and size belong to other reviewers; skip them."

**Complexity sub-agent prompt** adds:

- The brief: "Hunt only for what the change could do without. For each new piece of code, the expected solution is the first of these that holds: it doesn't need to exist; it already exists in this repo; the standard library does it; a native platform feature does it (`<input type="date">` over a picker library, a database constraint over app code); an installed dependency does it; one line does it. Only then is new code justified. Flag code that skipped a step that holds. One line per finding: `<file>:L<line>: <tag> <what to cut>. <replacement>.` Tags: `delete:` dead code, unused flexibility, or a speculative feature, replaced by nothing. `stdlib:` hand-rolled code the standard library ships; name the function. `native:` code or a dependency doing what the platform does; name the feature. `reuse:` an equivalent helper, type, or pattern already in this repo; name the path. `yagni:` an abstraction with one implementation, config nobody sets, a parameter or hook the spec doesn't need, or a layer that only delegates. `shrink:` the same logic in fewer lines; show the shorter form. A replacement must keep the behavior, including edge cases such as which duplicate wins; when it doesn't, say what changes. Before a `delete:` or `reuse:`, search the whole repo for the symbol, including tests and string or dynamic references, and cite what you found. Never flag validation at trust boundaries, error handling that prevents data loss, security measures, accessibility, a single smoke test or self-check, or anything the spec explicitly asks for. Correctness and performance are out of scope. End with `net: -<N> lines, -<M> dependencies possible`, or `Lean already.` when nothing qualifies."

**Security sub-agent prompt**, when step 3b selected it, adds:

- The absolute path of the security-audit skill directory and the companion files step 3b selected.
- The brief: "Review the diff for security vulnerabilities only, in the security-audit skill's guidance mode: write no audit files and start no full audit. First read the skill's `SKILL.md` sections Universal execution safety, Core principles, and Anti-patterns, then each listed companion file. A finding names the lower-trust principal, the input or action they control, the intended control, the crossed boundary, the affected principal or resource, and the observed or owner-observable result, with a `file:line` source trace. Give confirmed findings a severity from the skill's anchors. When a decisive fact lives outside the repository, such as deployment, provider, proxy, or identity configuration, report `needs_validation` with the exact missing fact and no severity. Run target code only when every control in Universal execution safety is enforced; otherwise trace the source. Missing best practices and defense-in-depth advice are not findings."

### 5. Verify the findings

A sub-agent's finding is a claim. Before reporting it, check it against the code:

- Open the cited lines and confirm they say what the finding claims.
- **Correctness:** confirm the triggering scenario is reachable from a real caller or input. Run it when that is cheap.
- **Complexity:** confirm the `delete:` and `reuse:` searches, and that the named stdlib function, platform feature, or existing helper covers what the code does, including its edge cases.
- **Spec:** confirm the quoted spec line exists and says what the finding claims.
- **Security:** confirm the source trace from the lower-trust input to the affected resource, and that no control on that path stops it. A `needs_validation` finding keeps its status; confirm only that its missing fact really is outside the repository.

Drop a finding that fails the check, and count the drops per axis. Mark a finding `unverified` when you could not check it; don't drop it and don't assert it. With many findings, the checks can run in parallel sub-agents, one per axis.

### 6. Aggregate

Present the reports under `## Spec`, `## Correctness`, `## Security`, `## Standards`, and `## Complexity` headings, with verified findings verbatim or lightly cleaned. Do **not** merge or rerank findings across axes, because the axes are deliberately separate (see _Why separate axes_). Where two axes flag the same lines, keep both and cross-reference them. When the Security axis was skipped, its section says so and lists the signals checked.

End with a one-line summary: verified findings per axis, findings dropped in verification per axis, the worst issue _within each axis_ (if any), the highest confirmed Security severity, and the Complexity axis's `net:` line. Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why separate axes

A change can pass any axis and fail another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
- Code that is on spec and conventional but breaks on an empty input or a caller outside the diff → **Spec and Standards pass, Correctness fail.**
- Code that works for every honest caller but lets one tenant read another's records through a changed query → **Correctness pass, Security fail.**
- Code that is correct, on spec, and conventional, but builds a 300-line date picker where `<input type="date">` holds → **Complexity fail.**

Reporting them separately stops one axis from masking another. Security runs only when the change touches a trust boundary, because its evidence bar is expensive to meet and most diffs give it nothing to check. Complexity runs on its own because the other reviewers read the code as given. Asking whether the code should exist at all needs a reviewer whose only job is that question.
