# Case: structured-behaviour-retired-governed-by-no-consumer

**Verifies:** a retired Use Case's `governed-by` relationship does not suppress `PRODUCT105` for an active Business Rule.

**Spec references:**

- [Relationships](../../../spec/relationships.md#knowledge-warning-relationship-sets) - only non-retired relationship authors count as consumers.

## Expected

The active Business Rule emits exactly one `PRODUCT105` warning.
