# Changelog

All notable changes to the Product Definition as Code specification are documented here. The specification is versioned with semantic versioning, independently of any implementation.

## [Unreleased] - v0.1.0-rfc

- The specification defines the Product Definition as the accepted, versioned and validated product graph on the repository's canonical branch. It evolves through exactly one mechanism: a `Product Change`, a semantic delta of `add`, `modify` and `remove` operations, validated as an overlay, applied by an explicit human-triggered operation, and accepted through a reviewed merge. A pull request reviews and accepts a Product Change; it is not the Product Change (RFC #4).
- `CHG-INITIAL` establishes the first Product Definition for both greenfield and brownfield products. Brownfield discovery is an input activity to it, not a separate lifecycle: there is no recovery change type and no `recover` operation (RFC #4).
- The delivery pipeline is not part of the normative model. Product Handoff, mandatory Delivery Slices, Promotion, Reconciliation, Implementation Claims and Deployment Evidence are removed; a delivery process may use its own equivalents outside PDaC. The `SLI-` and `HOF-` prefixes and diagnostics `PRODUCT030`-`PRODUCT032`, `PRODUCT040`-`PRODUCT041`, `PRODUCT043`-`PRODUCT044`, `PRODUCT109`-`PRODUCT110` are retired and never reused (RFC #4).
- Applying a change records the impacted artifacts and their resulting digests, so the citations a change puts at risk are derivable from the change itself (RFC #4).
- The citation contract binds consumer documents to canonical product text through machine-verifiable citations: a target artifact `id`, a content `digest`, and an optional scenario `anchor`. A conforming tool computes one status per citation (`current`, `stale`, `tampered`, `unresolved`) and emits diagnostics `PRODUCT060`-`PRODUCT063` (RFC #4).
- Functional and Quality Requirements accept an optional stable `id` on each `verification[]` entry, enabling scenario-id citation anchors. Backward compatible within `v1alpha1` (RFC #4).
- Initial extraction of the specification chapters from the reference implementation (ProductShape), with implementation-specific references neutralized.
- Manifesto restructured into a signable core (four value pairs, ten principles) plus the position in full.
- Governance, RFC process, signatories, implementations and adopters registries established.
