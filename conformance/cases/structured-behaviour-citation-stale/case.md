# Case: structured-behaviour-citation-stale

**Verifies:** a direct Structured Behaviour citation becomes stale when its target changes.

**Spec references:**

- [Citation Contract](../../../spec/citation-contract.md) - a changed target makes a faithful prior citation stale.

## Expected

The sidecar emits exactly one `PRODUCT061` warning for the cited Structured Behaviour.
