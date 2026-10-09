# Model the domain

Apply before writing logic: choosing core types and data structures, writing stateful logic, sequencing scaffold-vs-feature work, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals.

Encode the real domain in a data structure instead of scattering it across conditionals.

**Why:** scattered booleans, repeated shape assumptions, and branching spread across files are accidental complexity. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Choosing it at write time is cheap. Recovering it later reads as a refactor and gets deferred. A data-structure change late is a rewrite. Early, it is often a one-line diff.

## Data structures first

Get the data shape right before writing logic. The right shape makes downstream code obvious. Define core types early, trace every access pattern, and choose structures that match the dominant paths. Structural decisions protect option value. Code-level decisions protect simplicity. Over-engineering is often a premature decision that closes doors. The right foundational data structure keeps them open.

Reach for structures like these:

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed object or model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command/event model instead of ad hoc state mutations.
- A module organized around one body of domain knowledge instead of a sequence such as load, validate, transform, and save. Execution order is not ownership.
- A small module boundary that gathers repeated behavior, ownership, or invariants.
- A queue, cache, index, graph/tree, or normalized collection where the data access pattern calls for it.
- Any other structure that fits. The list above covers the common cases only. When none fits, work out what the code must never allow and how the data gets read, then find the structure that encodes exactly that.

At code level, DRY the structure, not every line. Types and data models should converge. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Do not force an abstraction. Prefer boring code if the current shape is already clear, local, and unlikely to grow. Be skeptical of an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

Before sharing state between actors, ask "what happens if another actor modifies this concurrently?" If the answer is not "nothing", isolate it, per [separate-before-serializing-shared-state](separate-before-serializing-shared-state.md).

## Scaffold first

If something helps every later phase, do it first. Ask "does every subsequent phase benefit from this existing?" CI, linting, test infrastructure, and shared types are scaffold. Sequence for option value: setup before features, tests before fixes. Subtraction comes before scaffolding, per [laziness-protocol](laziness-protocol.md): remove dead weight first, then lay foundations.

Each increment should land a coherent abstraction or deepen one that exists. Do not spread a new capability across callers as special-case coordination.

## The tell

You skipped this when a new feature grows an existing if/else chain by one more branch, or adds a second boolean that must stay in sync with the first. Temporal decomposition is another tell. Phase-named modules repeat the same domain rules across steps.
