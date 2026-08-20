### Bug fix

**Be scientific. Every shipped line traces to runtime evidence.** Belt-and-suspenders that "might help" is a hypothesis, not a fix. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself. A bug you can't reproduce, you can't prove fixed. Won't reproduce directly, force it: synthesize the trigger, tighten conditions, or instrument until it fires.
2. Run the `diagnosing-bugs` loop: build a feedback loop that goes red on this bug, minimise, hypothesise, instrument, eliminate. Seed hypotheses with `how` over the affected subsystem and `why` for regression history, fanned out as parallel subagents. Don't guess. Confirm the surviving mechanism with runtime evidence before designing the fix.
3. Plan the fix per **principle-fix-root-causes**. If it crosses a function boundary, `architect` first.
4. Write the failing regression test first via `tdd`, then the fix on top. The failing test lands before the fix in git history.
5. Verify on the same surface, driving the repo's `verify-<app>` skill when one exists: the original repro now passes. "Inconclusive" is not a pass.
6. `code-review`, then run **Committing** (`playbooks/committing.md`).

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
