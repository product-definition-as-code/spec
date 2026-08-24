# Case: configuration-custom-root

**Verifies:** a versioned kernel configuration discovered at `.product/config.yaml` selects a non-default Product Definition root and validates with no diagnostics.

**Spec references:**

- [Configuration](../../../spec/configuration.md) - location, discovery, version and `product-root`.
- [Configuration schema](../../../schemas/v1alpha1/config.schema.json) - closed `v1alpha1` shape.

## Fixture

`repo/.product/config.yaml` selects `product-root: product`. The only artifact lives under `repo/product/model/actors/`, not under the default `docs/product`, and is a valid Actor. A validator that ignores configuration discovers no artifact and fails this case's positive discovery assertion; a validator that reads ProductShape-specific keys instead of the normative contract reports `PRODUCT050`.

## Expected

Zero diagnostics and exit `0`. The actor is discovered from the configured root.
