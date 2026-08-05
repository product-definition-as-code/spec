# Changelog

All notable changes to the Product Definition as Code specification are documented here. The specification is versioned with semantic versioning, independently of any implementation.

## [Unreleased] - v0.1.0-rfc

- The specification defines the Product Definition as the accepted, versioned and validated product graph on the repository's canonical branch. It evolves through exactly one mechanism: a `Product Change`, a semantic delta of `add`, `modify` and `remove` operations, validated as an overlay, applied by an explicit human-triggered operation, and accepted through a reviewed merge. A pull request reviews and accepts a Product Change; it is not the Product Change (RFC #4).
- `CHG-INITIAL` establishes the first Product Definition for both greenfield and brownfield products. Brownfield discovery is an input activity to it, not a separate lifecycle: there is no recovery change type and no `recover` operation (RFC #4).
- The delivery pipeline is not part of the normative model. Product Handoff, mandatory Delivery Slices, Promotion, Reconciliation, Implementation Claims and Deployment Evidence are removed; a delivery process may use its own equivalents outside PDaC. The `SLI-` and `HOF-` prefixes and diagnostics `PRODUCT030`-`PRODUCT032`, `PRODUCT040`-`PRODUCT041`, `PRODUCT043`-`PRODUCT044`, `PRODUCT109`-`PRODUCT110` are retired and never reused (RFC #4).
- Apply materializes and validates a proposal; it does not accept it. The accepted Product Definition changes only when a human merges the pull request carrying the applied result, and an implementation MUST NOT treat a successful apply as acceptance (RFC #4).
- Intent, effective change and impact are distinct: a Product Change is authoritative for what was intended, the product diff between baseline and applied result is authoritative for what effectively changed, and impact is computed from that diff and the citation index. Neither may be presented as the other (RFC #4).
- A `draft` or `proposed` change may be edited or rebased freely; an applied and accepted change is immutable, and later corrections are expressed through a new Product Change (RFC #4).
- Each terminal status has exactly one archive directory: `superseded/` joins `completed/` and `rejected/`, because a change that was approved and then overtaken is not a change that was refused, and the change history is the evidence of which happened (RFC #4).
- Applying a change whose status is not `approved` fails with `PRODUCT028`, exit `1`, leaving the working tree untouched (RFC #4).
- Baseline drift covers `operations.modify` and `operations.remove` only, and changed means the content digest differs at `base-revision`; an addition has no baseline artifact to compare against and is already covered by `PRODUCT020` (RFC #4).
- Apply reports the product diff in a human-readable and a machine-readable form and never writes it into the archived change; each entry carries the impacted artifact, the kind of impact and, for additions and modifications, the resulting digest. Diff determinism is semantic; an on-disk serialization stays deferred (RFC #4).
- `PRODUCT108` is state-based and syntactic: an unresolved question is a Markdown list item under `## Open Questions`, reported whenever an `approved` change is validated; prose such as `None.` is not a question (RFC #4).
- The citation contract binds consumer documents to canonical product text through machine-verifiable citations: a target artifact `id`, a content `digest`, and an optional scenario `anchor`. A conforming tool computes one status per citation (`current`, `stale`, `tampered`, `unresolved`) and emits diagnostics `PRODUCT060`-`PRODUCT063` (RFC #4).
- Functional and Quality Requirements accept an optional stable `id` on each `verification[]` entry, enabling scenario-id citation anchors. Backward compatible within `v1alpha1` (RFC #4).
- Initial extraction of the specification chapters from the reference implementation (ProductShape), with implementation-specific references neutralized.
- Manifesto restructured into a signable core (four value pairs, ten principles) plus the position in full.
- Governance, RFC process, signatories, implementations and adopters registries established.
