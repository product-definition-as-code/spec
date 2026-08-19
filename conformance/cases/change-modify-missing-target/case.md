# Case: change-modify-missing-target

**Verifies:** a Product Change declares a modification of an ID that does not exist in the baseline; validating the change reports `PRODUCT021`.

**Spec references:**

- [Product Changes → Operations](../../../spec/product-changes.md#operations) - every ID in `operations.modify` MUST exist in the baseline.
- [Validation](../../../spec/validation.md) - error `PRODUCT021`, reported when a change is validated, never when validating the baseline alone.

## Fixture

`repo/` contains the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL` - plus one active Product Change (`CHG-AMEND-REPORTING`) in status `proposed` that declares `modify: [FR-VALIDATE-002]`. The baseline's only requirement is `FR-VALIDATE-001`; `FR-VALIDATE-002` has never existed in it.

The change carries a complete proposed artifact for `FR-VALIDATE-002` under `proposed/`, derived from `UC-VALIDATE-001`, so the declared operation and its artifact agree (`PRODUCT026` does not hold) and the overlay - which gains the proposed requirement - compiles into a valid, fully reachable graph. The missing baseline target is the one clause that fails.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT021` as an error against the change file, with `artifact` `CHG-AMEND-REPORTING` and `target` `FR-VALIDATE-002`. The archived `CHG-INITIAL` takes no part: archived changes are inert history, and their operations are never re-checked.
