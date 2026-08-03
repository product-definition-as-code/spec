# Changelog

All notable changes to the Product Definition as Code specification are documented here. The
specification is versioned with semantic versioning, independently of any implementation.

## [Unreleased] - v0.1.0-rfc

- The specification defines the product model as accepted product intent on the repository's
  canonical branch. The baseline changes through exactly one operation: a human merging a validated
  proposed revision. Validation of a proposal is full structural validation of the proposed tree;
  tools MUST NOT merge a proposal that fails it (RFC #4).
- The citation contract binds consumer documents to canonical product text through
  machine-verifiable citations: a target artifact `id`, a content `digest`, and an optional
  scenario `anchor`. A conforming tool computes one status per citation (`current`, `stale`,
  `tampered`, `unresolved`) and emits diagnostics `PRODUCT060`-`PRODUCT063` (RFC #4).
- Functional and Quality Requirements accept an optional stable `id` on each `verification[]`
  entry, enabling scenario-id citation anchors. Backward compatible within `v1alpha1` (RFC #4).
- Initial extraction of the specification chapters from the reference implementation
  (ProductShape), with implementation-specific references neutralized.
- Manifesto restructured into a signable core (four value pairs, ten principles) plus the
  position in full.
- Governance, RFC process, signatories, implementations and adopters registries established.
