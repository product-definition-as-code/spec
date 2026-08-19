# Case: change-proposed-undeclared

**Verifies:** a Product Change carries a proposed future-state artifact that its `operations` never declare; validating the change reports `PRODUCT026` against the undeclared artifact.

**Spec references:**

- [Product Changes → Operations](../../../spec/product-changes.md#operations) - every artifact under `proposed/` MUST be listed in `operations.add` or `operations.modify`.
- [Validation](../../../spec/validation.md) - error `PRODUCT026`: proposed artifact not listed in operations. The reverse direction of the same code - an operation without its proposed artifact - is `change-operation-unproposed`.

## Fixture

`repo/` contains the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL` - plus one active Product Change (`CHG-DRAFT-REPORTING`) in status `draft` whose `operations` lists are all empty, while its `proposed/` tree carries a complete requirement `FR-VALIDATE-002`: the elaboration drafted the artifact but never declared the operation that would carry it into the model.

The proposed requirement is complete and well-connected - derived from `UC-VALIDATE-001`, with a scenario id - so the overlay it joins compiles into a valid, fully reachable graph, and the undeclared operation is the one clause that fails. The point is that `operations` is the authoritative statement of what the change means to do: an artifact that would ride along without being declared is exactly the silent scope the check exists to catch, however sound the artifact itself is.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT026` as an error against the proposed artifact's file, with `artifact` `FR-VALIDATE-002`. The finding is about the undeclared file, so it carries the proposed artifact's path, not the change file's.
