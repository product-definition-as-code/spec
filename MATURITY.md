# Maturity and compatibility

This page is the single source of truth for what each public surface of Product Definition as Code is today, and for which version dimensions govern which contract. If any other page disagrees with this one, this one wins and the other page has a bug.

## What each surface is, today

| Surface | Status |
| --- | --- |
| PDaC methodology | Experimental, open RFC |
| PDaC specification | v0.3.0 released, serialization v1alpha2, extracted from one implementation, not yet independently implemented. Every chapter is at most `draft` until v1.0 |
| ProductShape | Reference implementation and design origin |
| Conformance | 147/147 executable v0.3.0/v1alpha2 cases pass against published ProductShape 0.26.1 with runner 1.1.0 and its trusted operation adapter. No skips. The suite does not cover every normative rule. Exact revisions, legacy regression and limitations: [release evidence](docs/releases/v0.3.0.md). |
| Adoption | One listed adopter (ProductShape itself) |
| Governance | Founder-led, pro tempore, with published decision records |

## Version dimensions

These are different dimensions, not one number. Every conformance claim MUST identify both the method/spec version and the serialization version. That pair selects the accepted document set and semantic contract. A Git revision MAY identify the specification repository content that was observed, but MUST NOT substitute for either claimed version.

| Dimension | Current | Governs |
| --- | --- | --- |
| Method / spec version | 0.3.0 | Semantic rules |
| Serialization version | v1alpha2 | File representation and authoritative schemas; paired with the method/spec version to select the accepted document set |
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

v0.3.0 selects serialization `v1alpha2`, including the explicit Rule/Use Case governance migration. Releasing this pair does not satisfy the independent-implementation or other v1.0 maturity gates. See the [release evidence](docs/releases/v0.3.0.md) and [migration guide](docs/migrations/v0.3.0.md).
