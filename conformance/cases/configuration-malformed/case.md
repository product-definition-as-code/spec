# Case: configuration-malformed

**Verifies:** malformed `.product/config.yaml` produces exactly one `PRODUCT050`, exits `2`, and does not continue with defaults.

**Spec reference:** [Configuration → Invalid configuration](../../../spec/configuration.md#invalid-configuration).

## Fixture

The configuration contains an unterminated YAML sequence. No artifact discovery is attempted.

## Expected

One error against `.product/config.yaml`, no `field` because parsing failed, and exit `2`.
