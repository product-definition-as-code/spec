# Case: change-removal-dangling-reference

**Verifies:** a Product Change removes an artifact that an active artifact still references; compiling and validating the overlay reports `PRODUCT024` against the referencing artifact.

**Spec references:**

- [Product Changes → Overlay validation](../../../spec/product-changes.md#overlay-validation) - validating a change compiles the overlay (removals deleted) and applies full structural validation to it, without modifying any baseline file.
- [Validation](../../../spec/validation.md) - error `PRODUCT024`: removal leaves a dangling reference from an active artifact in the overlay.

## Fixture

`repo/` extends the citation-current model with a second Use Case (`UC-VALIDATE-002`, validating scenario anchors) that the Journey (`JRN-VALIDATE`) lists as a step alongside `UC-VALIDATE-001`. The baseline is fully valid. One active Product Change (`CHG-RETIRE-ANCHOR-UC`) in status `proposed` declares `remove: [UC-VALIDATE-002]` - a legal operation, since the ID exists in the baseline - but does not modify the journey that references it.

The construction keeps the defect singular: in the overlay, the journey's step is the only reference to the removed use case, and nothing becomes unreachable - `UC-VALIDATE-002` is gone entirely, and every surviving artifact still connects to the actor through `UC-VALIDATE-001` - so the dangling step is the one finding. In the baseline the reference is sound, which is why this is an overlay diagnostic: the baseline file is never modified, and `PRODUCT024` is reported when the change is validated, never when validating the baseline alone.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT024` as an error against `docs/product/model/journeys/jrn-validate.md` - the referencing artifact, at its baseline path, since the overlay modifies no file - with `artifact` `JRN-VALIDATE` and `target` `UC-VALIDATE-002`. A plain `PRODUCT006` is the wrong answer: the reference dangles because a removal in the change under validation deleted its target, and the overlay code exists to say so.
