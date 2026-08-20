# Case: change-remove-missing-target

**Verifies:** a Product Change declares a removal of an ID that does not exist in the baseline; validating the change reports `PRODUCT022`.

**Spec references:**

- [Product Changes → Operations](../../../spec/product-changes.md#operations) - every ID in `operations.remove` MUST exist in the baseline; removed artifacts need no tombstone files.
- [Validation](../../../spec/validation.md) - error `PRODUCT022`, reported when a change is validated, never when validating the baseline alone.

## Fixture

`repo/` contains the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL` - plus one active Product Change (`CHG-RETIRE-REPORTING`) in status `proposed` that declares `remove: [FR-VALIDATE-002]`. No artifact in the baseline carries that ID.

A removal needs no proposed artifact, so the change carries no `proposed/` tree and no `PRODUCT026` condition can hold. The overlay is the baseline unchanged - removing a nonexistent ID deletes nothing - and it compiles cleanly, so the phantom removal target is the one clause that fails.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT022` as an error against the change file, with `artifact` `CHG-RETIRE-REPORTING` and `target` `FR-VALIDATE-002`.
