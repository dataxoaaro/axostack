### Feature

**You own the design. Plan, review, verify.**

1. Requirements unclear or plan not yet agreed → the **grilling** skill, plus the **domain-modeling** skill when domain docs exist. Skipping stays as `skip: <reason>`.
2. More than one slice, or a shape worth a written record → the **plan** skill. It runs steps 3 to 5 inside it and lands a plan document to grill and slice; continue from step 6 against that plan. A single-slice change notes `skip: single slice` and runs steps 3 to 5 inline.
3. `how` over the affected subsystem.
4. `architect` for parallel design exploration when the change crosses a function boundary. Do not fold the design decision silently into implementation.
5. Name the data shape and its organizing structure per **principle-model-the-domain** before writing logic: a state machine over scattered booleans, a table or registry over branching, a typed model over repeated shape assumptions.
6. Build via `tdd`, one vertical slice at a time. Red, green, refactor.
7. Verify on the matching surface per **principle-prove-it-works**, driving the repo's `verify-<app>` skill when one exists. "It compiles" or "tests pass" alone is not a pass for behavior the user sees.
8. `code-review` on the diff, then `no-comments`.
9. Run **Committing** (`playbooks/committing.md`), sequencing commits per **principle-sequence-verifiable-units**.

**Reply:** what you built, what you chose and why, open decisions. Tables for design alternatives.
