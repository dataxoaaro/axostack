### Refactoring

**Behavior-preserving. The tests prove it.**

1. `blast-radius` over the target: every caller, consumer, and serialized surface the shape touches.
2. Apply **principle-subtract-before-you-add**: remove dead weight first, then reshape the simpler base.
3. Confirm test coverage over the affected behavior before touching it. Missing coverage → write characterization tests first via `tdd`.
4. Refactor in small units per **principle-sequence-verifiable-units**: each unit ends with the full test suite green, committed before the next.
5. Apply **principle-minimize-reader-load** as the acceptance bar: fewer layers, less hidden state, collapsed one-caller wrappers.
6. New API replacing an old one → **principle-migrate-callers-then-delete-legacy-apis**. Migrate and delete in one wave, no deprecated stubs left behind.
7. `code-review`, then run **Committing** (`playbooks/committing.md`).

**Reply:** what moved and why, what got deleted, proof behavior held.
