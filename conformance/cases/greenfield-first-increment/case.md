# Case: greenfield-first-increment

**Verifies:** initialisation - an empty model receives `CHG-INITIAL`, which adds Product actors, a journey, a use case, two rules and one FR with scenario ids; the change is applied and accepted through review; an SDD spec cites `FR-X#S1` and `BR-Y`; all citations are `current`; implementation proceeds.

**Spec references:**

- [Product Changes](../../../spec/product-changes.md) - `CHG-INITIAL`, apply, archived change history.
- [Citation Contract](../../../spec/citation-contract.md) - citation `current` status.
- [Identifiers](../../../spec/identifiers.md) - artifact IDs and prefixes.
- [Validation](../../../spec/validation.md) - structural validation of the applied model.

## Fixture

`repo/` represents the state *after* apply and the reviewed merge: the canonical branch contains the added actors, use case, journey, rules and FR, and the archived change under `docs/product/changes/completed/chg-initial/`. A consumer spec (`repo/specs/feature-greenfield.md`) cites the FR's scenario `S1` and one of the business rules. Both citations are `current`.

## Expected

`expected.json` asserts zero diagnostics: the model is structurally valid, both citations resolve with matching digests, and the archived change is inert history whose `operations.add` IDs produce no duplicate-ID diagnostic against the model they were applied into.
