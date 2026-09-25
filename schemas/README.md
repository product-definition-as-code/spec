# Schemas

**These JSON Schemas are normative.** They define the serialization contract (version: `v1alpha1`) for every artifact kind, repository configuration and citation sidecar: closed shapes, allowed values and required fields that the specification text describes in prose. Where prose and schema disagree, the schema wins and the prose has a bug.

They were extracted from the reference implementation ([ProductShape](https://github.com/juangcarmona/productshape), commit `e00f67e`), which developed and validated them against a self-hosted product model. From this point forward this repository is their home: implementations, including the reference one, consume released schema versions from here. Migrating ProductShape to consume these released schemas instead of its internal copies is tracked work, not an assumption.

Two schemas are defined directly in this repository rather than mirrored from the extracted ProductShape copy. `product-change.schema.json` follows the corrected lifecycle in [RFC 0004](../rfcs/0004-delivery-model-reset.md), while `structured-behaviour.schema.json` implements [RFC 0084](../rfcs/0084-explicit-behaviour-semantics.md) and has no ProductShape original to mirror.

A second implementer needs nothing from ProductShape source to parse artifacts, kernel configuration or citation sidecars: these schemas plus the specification chapters are the whole contract. What is still missing for full independent conformance is a complete conformance suite (see [conformance/](../conformance/)): the published tests are runnable today but not yet a complete, normative set.

Versioning: directories are serialization versions (`v1alpha1`, then `v1beta1`, then `v1`). For a schema change within one serialization version to be backward compatible, every document valid under an earlier released schema set in that version MUST remain valid with the same interpretation under the later set. A backward-compatible change MAY accept new documents, fields or enum members. Any change that does not meet that rule starts a new version directory. See [MATURITY.md](../MATURITY.md) for how serialization versions relate to spec and tool versions.

The RFC 0084 expansion of `v1alpha1` is backward compatible under that rule. Repositories valid under the earlier schema set require no configuration edit or migration merely to remain valid under specification v0.2. Structured Behaviour is optional to author and the existing inline Requirement verification form retains its meaning.

The case-insensitive form of the `structuredBehaviourClause` keyword prohibition is not an exception to that rule. No released `v1alpha1` schema set contained `structuredBehaviourClause` at all, so narrowing it before release invalidates no document any released set accepted. It is narrowed now precisely because doing so after release would not be backward compatible.
