# Case: change-open-questions

**Verifies:** a Product Change in status `approved` still carries unresolved questions - Markdown list items under `## Open Questions` - and validating the change reports the `PRODUCT108` warning.

**Spec references:**

- [Product Changes](../../../spec/product-changes.md) - lifecycle, the `PRODUCT108` trigger (an unresolved question is a list item; the warning is state-based).
- [Validation](../../../spec/validation.md) - warning `PRODUCT108`.

## Fixture

`repo/` contains the same minimal model as `citation-current`, established by an archived `CHG-INITIAL`, plus one active Product Change (`CHG-TIGHTEN-VALIDATION`) in status `approved` that modifies `FR-VALIDATE-001` with a complete proposed artifact. Its `## Open Questions` section carries two list items. The overlay validates without errors, so the only finding is the warning under test. The negative case needs no fixture of its own: the archived `CHG-INITIAL` records in these tests carry `## Open Questions` containing the prose `None.`, which counts as resolved because prose is not a question.

## Expected

Exactly one warning regardless of the two list items: `PRODUCT108` against the change file, with `change` `CHG-TIGHTEN-VALIDATION` and `field` `Open Questions`. No `artifact` or `target` is asserted: a Product Change is not a Product Artifact, and the warning is state-based rather than attributed to an individual question.
