# Case: change-operation-unproposed

**Verifies:** a Product Change declares a modification without carrying the complete proposed future-state artifact it requires; validating the change reports `PRODUCT026` against the change.

**Spec references:**

- [Product Changes → Operations](../../../spec/product-changes.md#operations) - every ID in `operations.modify` MUST have a complete proposed future-state artifact under `proposed/` using the same ID.
- [Validation](../../../spec/validation.md) - error `PRODUCT026`: operation without its proposed artifact. The other direction of the same code - a proposed artifact not listed in operations - is `change-proposed-undeclared`.

## Fixture

`repo/` contains the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL` - plus one active Product Change (`CHG-TIGHTEN-VALIDATION`) in status `proposed` that declares `modify: [FR-VALIDATE-001]` and carries no `proposed/` tree at all. The declared target exists in the baseline, so `PRODUCT021` does not hold: what is missing is the future state itself.

A modify operation without its artifact is a change that names what it will touch while withholding what it will say - unreviewable by construction, since approval would be given to a delta whose result is not in the change. The overlay is well-defined regardless (the modification replaces the baseline artifact with nothing proposed, leaving the graph the baseline's remainder), and here it stays structurally clean: nothing references the requirement, so the missing artifact is the one clause that fails.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT026` as an error against the change file, with `artifact` `CHG-TIGHTEN-VALIDATION` and `target` `FR-VALIDATE-001` - the finding is about the declared operation, so it carries the change's file, the mirror of `change-proposed-undeclared`, where it carries the undeclared artifact's.
