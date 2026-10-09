# End state

Apply when integrating a new requirement into an existing design, replacing an internal API while old callers exist, or running a planned rewrite or migration. Build what you would have built had the requirement existed on day one, and leave no compatibility layer behind.

Optimize for the intended, verifiable end state, not for keeping the old shape alive. Compatibility code written to smooth each intermediate step tends to become permanent debt. The end state is the target. How you reach it is [sequence-verifiable-units](sequence-verifiable-units.md): every committed unit stays green.

## Redesign as if it was always there

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start. The result should look like what we would have built if we had known on day one. This is how a design keeps its option value as requirements arrive.

- Read all affected files and understand the current design as a whole.
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections.
- Design the whole redesign first, then deliver it in units.

## Migrate callers, then delete the old API

When a new API is the right design, migrate its callers and remove the old API in the same wave instead of keeping a compatibility layer. Keeping both creates dual-path complexity, slows cleanup, and makes the codebase append-only.

- Do not keep a legacy path alive only because internal callers still exist.
- Inventory the callers, migrate them, and delete the old API in the same wave.
- Treat a temporary adapter as an exception with an end date, not as default architecture.
- Update tests to assert the new contract. Delete tests that only protect pre-refactor implementation details.

This applies when no external user depends on backward compatibility and the project can absorb a coordinated breaking change. A public API with external consumers needs a deprecation path instead.

## Keep every committed unit green

Breakage is allowed only inside one uncommitted unit. A renamed type whose callers have not moved yet is fine while you work on that unit. Migrate the callers, run the checks, and commit only once the unit is green. Never commit a red state with a plan to fix it later.

When the change is too wide for one green unit, use expand, migrate, contract. Add the new form beside the old so nothing breaks. Migrate callers in batches, each its own green commit. Then delete the old form. The old form's lifetime ends at the contract step.

- Declare the units and their checks before you start.
- Keep fast, high-signal checks on the touched areas while migrating.
- Run full static and runtime verification before declaring done.
