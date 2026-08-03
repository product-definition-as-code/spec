# Case: greenfield-first-increment

**Verifies:** acceptance scenario 1 from RFC #4 - an empty model receives a PR adding Product actors, two rules, and one FR with scenario ids; the PR is merged; an SDD spec cites `FR-X#S1` and `BR-Y`; all citations are `current`; implementation proceeds. No change container was ever created.

**Spec references:**

- [Citation Contract](../../../spec/citation-contract.md) - change-as-PR, citation `current` status.
- [Identifiers](../../../spec/identifiers.md) - artifact IDs and prefixes.
- [Validation](../../../spec/validation.md) - full-tree structural validation of the proposed tree.

## Fixture

`repo/` represents the state *after* the reviewed merge: the canonical branch now contains the added actors, use case, journey, rules, and FR. A consumer spec (`repo/specs/feature-greenfield.md`) cites the FR's scenario `S1` and one of the business rules. Both citations are `current`.

## Expected

`expected.json` asserts zero diagnostics: the model is structurally valid, both citations resolve with matching digests.
