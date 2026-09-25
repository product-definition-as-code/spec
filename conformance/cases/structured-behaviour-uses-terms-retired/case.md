# Case: structured-behaviour-uses-terms-retired

**Verifies:** an active Structured Behaviour using a retired Domain Term emits `PRODUCT008` alone.

**Spec references:**

- [Relationships](../../../spec/relationships.md#status-interactions) - an active artifact must not reference a retired artifact.
- [Validation](../../../spec/validation.md) - retired Domain Terms are excluded from the `PRODUCT106` population.

## Expected

The retired target produces `PRODUCT008` only, not `PRODUCT106`.
