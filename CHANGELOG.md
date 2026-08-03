# Changelog

All notable changes to the Product Definition as Code specification are documented here. The
specification is versioned with semantic versioning, independently of any implementation.

## [Unreleased] - v0.1.0-rfc

- **Delivery-model reset (RFC #4).** Retired the Product Change → Delivery Slice → Product Handoff
  → Promotion pipeline from the normative core. The baseline is now accepted product intent; change
  is the repository's native branch-review-merge mechanism (change-as-PR); full-tree structural
  validation is the CI gate; merging is a human decision. The bootstrap exception is deleted: the
  initial baseline enters through the same reviewed-merge mechanism as every later change.
- **Citation contract (RFC #4).** Added machine-verifiable references from consumer documents to
  canonical product text: citation record (`id` + `digest` + optional `anchor`), embedding as a
  read-only projection, four statuses (`current`/`stale`/`tampered`/`unresolved`), and diagnostics
  `PRODUCT060`–`PRODUCT063`. `PRODUCT042` generalized to citation digests. `handoff-contract.md`
  rewritten as the Citation Contract.
- **Addressable verification scenarios (RFC #4).** Added optional stable `id` to `verification[]`
  entries on Functional and Quality Requirements (`common.schema.json`), enabling scenario-id
  citation anchors. Backward compatible within `v1alpha1`.
- **Retired artifacts and diagnostics (RFC #4).** Removed `product-changes.md`, `delivery-slices.md`,
  and four schemas (`product-change`, `delivery-slice`, `product-handoff`, `product-coverage`).
  Retired diagnostic codes `PRODUCT020`–`PRODUCT027`, `PRODUCT030`–`PRODUCT032`,
  `PRODUCT040`–`PRODUCT041`, `PRODUCT043`–`PRODUCT044`, `PRODUCT108`–`PRODUCT110` (never reused).
  Retired prefixes `CHG-`, `SLI-`, `HOF-` (never reused). Manifesto principles 5, 8 and 9 reworded.
- Initial extraction of the ten specification chapters from the reference implementation
  (ProductShape), with implementation-specific references neutralized.
- Manifesto restructured into a signable core (four value pairs, ten principles) plus the
  position in full.
- Governance, RFC process, signatories, implementations and adopters registries established.

### Editorial (pre-RFC, v0.1 draft window)

- Reframed the methodology boundary end to end: definition hands off to *delivery*, of which
  Spec-Driven Development is one consumer among three (SDD frameworks, AI coding agents,
  human teams). The handoff contract was already framework-independent; the narrative now
  matches it.
