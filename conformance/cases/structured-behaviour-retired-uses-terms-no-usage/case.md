# Case: structured-behaviour-retired-uses-terms-no-usage

**Verifies:** a retired Structured Behaviour's `uses-terms` relationship does not suppress `PRODUCT106` for an active Domain Term.

**Spec references:**

- [Relationships](../../../spec/relationships.md#knowledge-warning-relationship-sets) - only non-retired relationship authors count as term usage.

## Expected

The active Domain Term emits exactly one `PRODUCT106` warning.
