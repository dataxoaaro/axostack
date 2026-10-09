# Type system discipline

Apply when designing types, reviewing a function signature, writing code in any statically-typed language, or wiring validation, error handling, or framework adapters. Make illegal states unrepresentable, parse external data at the boundary, and trust internal types.

The type checker is a proof assistant. Use it to eliminate impossible states, mismatched primitives, and unhandled variants at compile time. A case the types let you ignore becomes a runtime failure the compiler could have stopped. Prefer defining errors and special cases out of existence over proliferating handlers. Unrepresentable states, total functions, and interface redesign (the patterns below) are the tools.

Applies to any typed language. Use the idioms of the language in front of you. The patterns below name them for the common ones.

## The patterns

- **Make illegal states unrepresentable.** Model variants as sum types: discriminated unions in TypeScript, enums with payloads in Rust/Swift/Kotlin, sealed classes in Scala, ADTs in Haskell/OCaml. Don't model state as a bag of optional fields where contradictory combinations compile. A subtle anti-pattern worth naming: `{ completed: boolean; completedAt?: Date }` admits `completed: true; completedAt: undefined`, which is meaningless. Derive the boolean from a single source like `completedAt !== null`, or model the variants explicitly as `{ kind: 'open' } | { kind: 'done'; at: Date }`. If a bug forces the question "wait, can this combination actually happen?", the type is too loose.
- **Types are constructions, not restrictions.** Build the type up from the values you want instead of carving them out of a looser type with checks. The invariant that seems to need a refinement type is usually a construction away. A non-empty list is a head plus a rest, not a list with a length check. A valid time range is a start plus a duration, not two timestamps you must keep ordered. No representation is privileged. A list of pairs is an even-length list if you interpret it that way, so choose the shape that cannot build the illegal value and expose the interface callers need on top.
- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath but should not be interchangeable. Newtypes in Rust, opaque types in Swift, value classes in Kotlin, phantom types in Haskell, branded intersections in TypeScript. Validate once at creation, trust the type downstream.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC messages, CLI args, config files, environment variables, database rows. Have a parse function at every boundary that turns unstructured input into the typed model. See [Boundaries](#boundaries) below for where validation goes.
- **Don't lie to the type system.** Casts, unsafe coercions, and assertion functions that bypass the compiler are runtime crashes waiting to happen. If the compiler can't prove a fact, prove it (validate, narrow, refine the model) or accept that the cast is a hazard. The cast you bury today is the postmortem you write next week.
- **Exhaustive matching is the compiler's job.** When you match on a sum type, the compiler must fail compilation if a new variant is added without handling. Use the idiom your language provides: `never`-typed binding in TypeScript, unannotated `match` in Rust, `-Wincomplete-patterns` in Haskell, sealed-class match exhaustiveness in Kotlin.
- **Derive types from authoritative schemas.** When a protocol buffer, OpenAPI spec, GraphQL schema, database migration, or design-system token file defines a shape, derive from it instead of hand-rolling a parallel type. Manual duplication drifts, per [encode-lessons-in-structure](encode-lessons-in-structure.md).
- **Strengthen a type only where partiality appears.** A runtime assertion, null check, or "this should never happen" throw marks the place a type is too weak. Push that check up into the type. Then stop. The type system's job is to track the cases each use site must handle, not to describe the data as precisely as possible. Prefer total functions. `sum` of an empty list is 0, so it takes the plain list. `head` of an empty list has no answer, so it demands the non-empty one. Extra precision costs reuse and ceremony and buys no safety.

## Boundaries

Place validation, type narrowing, and error handling at system boundaries. Trust internal code. Business logic lives in pure functions, and the shell is thin and mechanical. Scattered validation is noisy, redundant, and gives a false sense of safety. Validate data once at the boundary. Keep logic out of framework wiring so it can be tested without the framework.

- **At boundaries** (CLI args, config files, external APIs, network protocols): validate, return errors, handle defensively. Validate config at parse time, not inside business logic.
- **Inside the system:** typed data, error propagation, no re-validation. No redundant nil checks deep in call chains when the boundary already validated.
- **Across the boundary:** expose domain concepts, not the boundary's private representation. Do not re-export transport, storage, framework, or wire types through the public surface. Keep general-purpose mechanism inside and special-purpose policy at the edge.
- **Code organization:** business logic in pure functions with no framework dependencies. Parsing is a pure transform from raw bytes to typed state. Prompt construction takes structured state in and returns a string. Scoring is a pure transform from state to results.

## The tests

- "Can I write a comment explaining when this combination of fields is valid?" If yes, the type is too loose. Split it into a sum type.
- "Do two of my function arguments share a primitive type but mean different things?" Brand them.
- "Where did this `any`, this `as`, this `assertNotNull` come from?" Trace it to the boundary and validate there instead.
- "If a new variant is added next month, will the compiler tell the next agent where to add a case?" If no, the match isn't exhaustive.
- "Is this type duplicating a shape another file owns?" Derive instead.
- "Am I strengthening this type to keep an operation total, or just to be more precise?" If nothing would otherwise panic, keep the plain type.
- "Is this data crossing a system boundary right now?" If not, validation is redundant.
- "Can this be a pure function that the shell just calls?" If yes, extract it.
