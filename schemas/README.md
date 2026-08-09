# Schemas

**These JSON Schemas are normative.** They define the serialization contract (version: `v1alpha1`) for every artifact kind: the closed frontmatter, allowed values and required fields that the specification text describes in prose. Where prose and schema disagree, the schema wins and the prose has a bug.

They were extracted from the reference implementation ([ProductShape](https://github.com/juangcarmona/productshape), commit `e00f67e`), which developed and validated them against a self-hosted product model. From this point forward this repository is their home: implementations, including the reference one, consume released schema versions from here. Migrating ProductShape to consume these released schemas instead of its internal copies is tracked work, not an assumption.

`product-change.schema.json` is the one schema this repository now defines rather than mirrors: its `status` enum follows the corrected lifecycle in [RFC 0004](../rfcs/0004-delivery-model-reset.md) and no longer matches the extracted copy.

A second implementer needs nothing from ProductShape source to parse and validate artifacts: these schemas plus the specification chapters are the whole contract. What is still missing for full independent conformance is the executable conformance tests (see [conformance/](../conformance/)), which are planned.

Versioning: directories are serialization versions (`v1alpha1`, then `v1beta1`, then `v1`). A schema change within a version must be backward compatible; anything else starts a new version directory. See [MATURITY.md](../MATURITY.md) for how serialization versions relate to spec and tool versions.
