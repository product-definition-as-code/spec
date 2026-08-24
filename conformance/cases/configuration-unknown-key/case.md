# Case: configuration-unknown-key

**Verifies:** a parsed configuration with an unknown top-level key produces exactly one `PRODUCT050` attributed to that key and exits `2`.

**Spec reference:** [Configuration → Invalid configuration](../../../spec/configuration.md#invalid-configuration).

## Fixture

The document is otherwise valid but places implementation-specific `tooling` at the top level instead of below `extensions`.

## Expected

One error against `.product/config.yaml`, `field: tooling`, and exit `2`.
