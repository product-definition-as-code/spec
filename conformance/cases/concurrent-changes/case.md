# Case: concurrent-changes

**Verifies:** two active Product Changes declare overlapping `modify` sets; validating the changes reports `PRODUCT025` for each of them.

**Spec references:**

- [Product Changes → Overlay validation](../../../spec/product-changes.md#overlay-validation) - concurrent active Product Changes MUST be checked for overlapping `modify`/`remove` sets; an overlap is an error until one change is rebased or withdrawn.
- [Validation](../../../spec/validation.md) - error `PRODUCT025`.

## Fixture

`repo/` contains the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL` - plus two active Product Changes, both in status `proposed` and both declaring `modify: [FR-VALIDATE-001]`: `CHG-TIGHTEN-VALIDATION` names the diagnostic the failure surfaces with, `CHG-REWORD-VALIDATION` rephrases the requirement around the product graph. Each carries a complete proposed artifact, and each overlay compiles and validates cleanly in isolation - the overlap is the only defect either change has.

## Expected

`expected.json` asserts two diagnostics: one `PRODUCT025` error per change and overlapping target, against that change's file, with the Product Change ID in `change`, `field` `operations.modify` and `target` `FR-VALIDATE-001`. Validation is per change - each change's overlay is compiled against the same baseline, and each is validated with the other as concurrent context - so the overlap fails both changes symmetrically: whichever change is rebased or withdrawn, the report told its author. An implementation that reports the overlap against only one of the two changes leaves the other's validation claiming a clean bill it does not have, and fails this case with a missing diagnostic.
