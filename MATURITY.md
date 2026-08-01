# Maturity and compatibility

This page is the single source of truth for what each public surface of Product Definition as
Code is today, and for which version dimensions govern which contract. If any other page
disagrees with this one, this one wins and the other page has a bug.

## What each surface is, today

| Surface | Status |
| --- | --- |
| PDaC methodology | Experimental, open RFC |
| PDaC specification | v0.9 draft, extracted from one implementation, not yet independently implemented |
| ProductShape | Reference implementation and design origin |
| Conformance | Self-conformance only; independent corpus and runner planned |
| Adoption | One listed adopter (ProductShape itself) |
| Governance | Founder-led, pro tempore, with published decision records |

## Version dimensions

These are different dimensions, not one number. Every validation result and handoff should be
interpretable against this matrix.

| Dimension | Current | Governs |
| --- | --- | --- |
| Method / spec version | 0.9.0-rfc | Semantic rules |
| Serialization version | v1alpha1 | File representation and schemas |
| Conformance suite | none published | Executable rule fixtures |
| Reference implementation | `@prodshape/cli` (see [npm](https://www.npmjs.com/package/@prodshape/cli) for current) | Tool behaviour |
| Integration profile | openspec adapter | Handoff landing contract |

## Gates before v1 may be called a standard

These are release gates, not aspirations to be waived:

1. A normative, versioned conformance corpus.
2. At least one independent implementation or clean-room validator.
3. Two external adopters with materially different repository shapes.
4. Published disagreements discovered by those implementations.
5. Governance with more than one organization represented.

Until every gate is met, the accurate description of this work is: an open RFC methodology with
a working reference implementation.
