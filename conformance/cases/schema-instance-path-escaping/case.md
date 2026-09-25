# Case: schema-instance-path-escaping

**Verifies:** an additional nested property emits `PRODUCT002` whose `field` is the RFC 6901 JSON Pointer to that property, including slash and tilde escaping.

**Spec references:**

- [Validation](../../../spec/validation.md#schema-instance-path-notation) - schema-instance paths are JSON Pointers, and additional properties name their escaped pointer.

## Why this case exists

The JSON Schema validator reports an additional property at its containing object. A conforming implementation must append the property name, escape its tokens and report the property itself. This fixture uses `recovered/by~` beneath `provenance`, so both required escapes are observable in one expected value.

## Expected

Exactly one `PRODUCT002`, attributed to `ACT-INSTANCE-PATH`, with `field: /provenance/recovered~1by~0`.
