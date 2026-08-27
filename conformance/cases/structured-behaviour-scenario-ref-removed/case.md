# Case: structured-behaviour-scenario-ref-removed

**Verifies:** removing a Structured Behaviour that an active Functional Requirement references emits one `PRODUCT024` in the overlay.

**Spec references:**

- [Product Changes](../../../spec/product-changes.md#overlay-validation) - a removal-caused dangling relationship is `PRODUCT024`.

## Expected

`PRODUCT024` is attributed to the baseline Functional Requirement and its exact scenario-reference field.
