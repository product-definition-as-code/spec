# Maturity and compatibility

This page is the single source of truth for what each public surface of Product Definition as Code is today, and for which version dimensions govern which contract. If any other page disagrees with this one, this one wins and the other page has a bug.

## What each surface is, today

| Surface | Status |
| --- | --- |
| PDaC methodology | Experimental, open RFC |
| PDaC specification | v0.2.0 released for comment 2026-08-28, extracted from one implementation, not yet independently implemented. Every chapter is at most `draft` until v1.0 |
| ProductShape | Reference implementation and design origin |
| Conformance | 44 published cases runnable, covering initialisation, the citation contract, configuration, topology, artifact kinds, most of the Product Change band, the full Structured Behaviour matrix, semantic `uses-terms` sources and JSON Pointer diagnostic fields, run by [`pdac-conformance@1.0.1`](https://www.npmjs.com/package/pdac-conformance). The reference implementation passes the whole set: 44 of 44 cases and 12 of 12 pinned digests on 2026-08-29, run against the published `@prodshape/cli` 0.16.0 from npm; the dated record lives in [IMPLEMENTATIONS.md](IMPLEMENTATIONS.md). |
| Adoption | One listed adopter (ProductShape itself) |
| Governance | Founder-led, pro tempore, with published decision records |

## Version dimensions

These are different dimensions, not one number. Every conformance claim MUST identify both the method/spec version and the serialization version. That pair selects the accepted document set and semantic contract. A Git revision MAY identify the specification repository content that was observed, but MUST NOT substitute for either claimed version.

| Dimension | Current | Governs |
| --- | --- | --- |
| Method / spec version | 0.2.0 | Semantic rules |
| Serialization version | v1alpha1 | File representation and authoritative schemas; paired with the method/spec version to select the accepted document set |
| Conformance suite | the conformance tests in this repository, run by [`pdac-conformance`](https://www.npmjs.com/package/pdac-conformance) | Executable rule fixtures |
| Reference implementation | `@prodshape/cli` (see [npm](https://www.npmjs.com/package/@prodshape/cli) for current) | Tool behaviour |
| Integration binding | openspec adapter | Citation contract |

## Gates before v1 may be called a standard

These are release gates, not aspirations to be waived:

1. A normative, versioned set of conformance tests.
2. At least one independent implementation or clean-room validator.
3. Two external adopters with materially different repository shapes.
4. Published disagreements discovered by those implementations.
5. Governance with more than one organization represented.

Until every gate is met, the accurate description of this work is: an open RFC methodology with a working reference implementation.
