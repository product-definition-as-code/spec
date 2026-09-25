# Case: structured-behaviour-illustrates-retired

**Verifies:** an active Structured Behaviour illustrating a retired Business Rule emits `PRODUCT008` alone.

**Spec references:**

- [Relationships](../../../spec/relationships.md#status-interactions) - an active artifact must not reference a retired artifact.
- [Validation](../../../spec/validation.md) - retired Business Rules are excluded from the `PRODUCT105` population.

## Expected

The retired target produces `PRODUCT008` only, not `PRODUCT105`.
