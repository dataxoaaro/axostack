### Bug fix

**Be scientific. Every shipped line traces to runtime evidence.** Belt-and-suspenders that "might help" is a hypothesis, not a fix. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself. A bug you can't reproduce, you can't prove fixed. Won't reproduce directly, force it: synthesize the trigger, tighten conditions, or instrument until it fires.
2. Run the `diagnosing-bugs` loop: build a feedback loop that goes red on this bug, minimise, hypothesise, instrument, eliminate. Seed hypotheses with `how` over the affected subsystem and `why` for regression history, fanned out as parallel subagents. Don't guess. Confirm the surviving mechanism with runtime evidence before designing the fix.
3. Plan the fix per [fix-root-causes](../principles/fix-root-causes.md). If it crosses a function boundary, `architect` first. A fix spanning more than one slice → the **plan** skill, with the confirmed mechanism as its Problem section.
4. Build via the **implement** skill, under two constraints this playbook adds: the failing regression test lands before the fix in git history, and the verification target is the original repro from step 1, not a proxy for it. "Inconclusive" is not a pass.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
