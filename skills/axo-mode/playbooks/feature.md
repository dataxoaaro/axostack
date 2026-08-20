### Feature

**You own the design. Plan, review, verify.**

1. Requirements unclear or plan not yet agreed → `grill-me` (or `grill-with-docs` when domain docs exist). Skipping stays as `skip: <reason>`.
2. `how` over the affected subsystem.
3. `architect` for parallel design exploration when the change crosses a function boundary. Do not fold the design decision silently into implementation.
4. Name the data shape and its organizing structure per **principle-model-the-domain** before writing logic: a state machine over scattered booleans, a table or registry over branching, a typed model over repeated shape assumptions.
5. Build via `tdd`, one vertical slice at a time. Red, green, refactor.
6. Verify on the matching surface per **principle-prove-it-works**. "It compiles" or "tests pass" alone is not a pass for behavior the user sees.
7. `code-review` on the diff, then `no-comments`.
8. Run **Committing** (`playbooks/committing.md`), sequencing commits per **principle-sequence-verifiable-units**.

**Reply:** what you built, what you chose and why, open decisions. Tables for design alternatives.
