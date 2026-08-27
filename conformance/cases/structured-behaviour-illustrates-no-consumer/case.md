# Case: structured-behaviour-illustrates-no-consumer

**Verifies:** an incoming Structured Behaviour `illustrates` edge does not suppress `PRODUCT105` for an active Business Rule with no consumer.

**Spec references:**

- [Relationships](../../../spec/relationships.md#knowledge-warning-relationship-sets) - `illustrates` is not a Business Rule consumer.

## Expected

The Business Rule emits exactly one `PRODUCT105` warning.
