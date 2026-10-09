### Refactoring

**Behavior-preserving. The tests prove it.**

1. `blast-radius` over the target: every caller, consumer, and serialized surface the shape touches.
2. Apply [laziness-protocol](../principles/laziness-protocol.md): remove dead weight first, then reshape the simpler base.
3. Confirm test coverage over the affected behavior before touching it. Missing coverage → write characterization tests first via `tdd`.
4. The reader-load test in [laziness-protocol](../principles/laziness-protocol.md) is the acceptance bar every unit is judged against: fewer layers, less hidden state, collapsed one-caller wrappers.
5. New API replacing an old one → [end-state](../principles/end-state.md). Migrate and delete in one wave, no deprecated stubs left behind.
6. Build via the **implement** skill, behavior-preserving, so each unit ends with the full test suite green before the next one starts. The suite is the proof that nothing moved.

**Reply:** what moved and why, what got deleted, proof behavior held.
