# Laziness protocol

Apply when refactoring, sizing a diff, sequencing an addition or rewrite, shaping code that is hard to trace, or when tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem.

Writing code is cheap for you, which makes over-engineering easy. Counter it by borrowing a human maintainer's fatigue. Aim for the most result with the least code and complexity.

- **Prefer deletion.** When asked to refactor or improve, look for removals before additions. Before deleting a component for being thin, run the same argument against its structural siblings. If it would also delete one nobody would touch, what you found is an unwritten file, not a redundant slot.
- **Maintain a flat call hierarchy.** Avoid deep call chains. A rich interface that hides substantial work is not a deep call chain. If answering a question requires tracing through more than 3 files or layers, flatten it.
- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Read the history before sweeping a pattern.** A pattern repeated across many files is a convention until `git log -S '<the pattern>'` says otherwise. Applied deliberately over several commits, it was someone's decision, and changing it is a decision too, not a cleanup. Count what is actually broken first. The minimal fix is the baseline the wide fix has to beat, out loud, in front of whoever owns the convention.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
- **Question the threading.** If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- **Sweat the small leaks.** Remove tiny pass-throughs, representation leaks, and duplicated choices before they spread. Small leaks compound into permanent coordination costs.

## Subtract before you add

When evolving a system, remove complexity first, then build. Deletion gives you a simpler base, which makes the next addition smaller and less brittle. Adding to a complex system compounds complexity. Removing first cuts the surface area, reveals the essential structure, and usually makes the next design obvious.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence removal before construction.
- Cut before you polish. Get to the minimum before investing in quality.
- Design for observed usage, not speculative edge cases.
- No speculative validators, parsers, or guards beyond what the spec demands. Out-of-spec features drag validators behind them. Persistence, retry-on-startup, and schema migration each need guards to defend their inputs.
- Simplify prompts. Remove redundant instructions and excessive templates.
- When a reference has no novel content, delete it rather than leaving a stub.

## Minimize reader load

Maintainability is the work a reader must do to understand code. Track two axes:

1. **Layers to trace.** How many indirections sit between the question and the answer.
2. **State to hold.** How much hidden or mutable context the reader must keep in their head.

Code is read far more than it is written. LOC, cyclomatic complexity, and "clean architecture" are proxies. The two axes are independent. A flat file with 50 globals can be as hard to reason about as a 6-layer adapter stack. Guard both. Working memory is finite for readers, the same way the context window is finite for agents (axo-mode's [Subagents](../SKILL.md#subagents) section).

- **Collapse layers** that do not earn their keep: wrappers with one caller, adapters with no second implementation, indirection introduced for a future that never came. Inline them.
- **Make adjacent layers change the abstraction.** A layer that repeats the same methods and arguments adds reader load without compression.
- **Demand interface compression.** A broad interface that hides little complexity makes readers learn both the surface and the implementation. Prefer boundaries that hide meaningful decisions.
- **Shrink state scope.** Prefer pure functions (returns over mutations), locals over fields, fields over module state, and module state over globals. Derive instead of sync.
- **Name the invariant at the boundary,** not in every consumer, so the reader learns it once.
- Before adding a layer or a piece of state, ask whether it reduces reader load somewhere else by at least as much.

**The test:** can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.

**Prime directive:** if a human developer would find the code exhausting to maintain, it is a bad solution. Be lazy. Stay simple.
