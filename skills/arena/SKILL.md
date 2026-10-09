---
name: arena
description: "Fan out N parallel subagents. Race mode: candidates attempt one task, then pick a base and graft the best of the rest. Partition mode: one worker per slice, one report. Use for /arena, 'arena this', 'swarm this'."
---

# Arena

Fan out N parallel subagents with the Agent tool. They run locally, in this session. Two modes:

- **Race** (the default). N attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result. Use it when one attempt at a non-trivial artifact would lock in the wrong shape.
- **Partition.** Split the work into slices, one worker each, drain them, and return one report. Use it for coverage matrices, sweeps, gauntlets, and exploration. See [Partition mode](#partition-mode) below.

## Start

Open a todolist with one entry per phase before launching anything. The arena runs autonomously and the list keeps phases from silently disappearing. Race mode runs these phases:

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract. Get it right before spawning anything.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. Concrete: `Adds a --dry-run flag that skips writes`. Vague: `code is correct`. The rubric is the picker's tool in Phase D; candidates only see the task.
3. Pick the runners. Default to one runner per available model tier so the candidates diverge. Spawn more when the arena covers multiple design directions. Same model N times when the work is generation-bound rather than judgment-sensitive.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`). N candidates writing to the same path is shared mutable state and fails the [separate-before-serializing-shared-state](../axo-mode/principles/separate-before-serializing-shared-state.md) test.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, and instructions to produce both the artifact and a short rationale.

The rationale is mandatory. Without it, the parent cannot tell whether a candidate's structure is principled or accidental, which makes Phase E grafting unreliable. Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, pick the strongest available model as cross-judge, preferring a different model from the runners'. Spawn one readonly judge subagent on that model. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with the parent's reading in Phase D, not with the candidates themselves. Spawning while candidates are still writing means the judge sees partial or empty outputs and reports them as dropouts.

## Phase D: Pick a base

Read every candidate end to end before picking. Skimming N candidates surfaces only the candidate whose surface looks most familiar.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller surface area when two feel tied, per [laziness-protocol](../axo-mode/principles/laziness-protocol.md).

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per [end-state](../axo-mode/principles/end-state.md). Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why. The rejection notes are the highest-signal part of the record. Future readers learn from what you considered and dropped, not just what you kept.

When N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per [prove-it-works](../axo-mode/principles/prove-it-works.md). The arena does not earn you a pass.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.

## Partition mode

Fan out N workers over separate slices of the work. The parent waits, aggregates, and returns one report. Open a todolist with four entries: Frame, Fan out, Aggregate, Report.

### Frame

1. State the done predicate and the report the workers must feed.
2. Partition the work into slices that do not overlap. Set N from the user or derive it from the slices. N is the total number of workers, not a concurrency limit.
3. Pick the worker model. Default to the session model, and drop to a fast model for mechanical sweeps.
4. Give each worker its own writable output when it writes: a worktree, a branch, or `/tmp/arena-<slug>/worker-<n>/`, per [separate-before-serializing-shared-state](../axo-mode/principles/separate-before-serializing-shared-state.md). When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

### Fan out

Spawn all N workers in one message with the Agent tool (`subagent_type: "general-purpose"`) so they run concurrently, passing each worker the model from step 3. When a worker must start from a non-default branch, pass `isolation: "worktree"` and name the branch to check out in its brief.

Every brief stands alone. Include the goal, the scope, the exact slice, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

### Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. Every required slice needs a result. Do not paste raw worker dumps.

### Report

Return one consolidated in-chat report: a compact result table, one-line evidenced issues, and explicit gaps or dropouts.
