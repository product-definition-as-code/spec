# Governance

This document describes how the Product Definition as Code specification is governed. It is deliberately lightweight and will evolve as the community grows; changes to this document follow the same RFC process as changes to the specification.

## Goals

The specification is a vendor-neutral, implementation-independent standard. No single company owns it, and no implementation (including the reference implementation) gets to change it unilaterally. The specification defines contracts; implementations compete on everything else.

## Roles

**Maintainers** review RFCs and pull requests, and decide what merges. Current maintainers:

| Name | Affiliation | Role |
| --- | --- | --- |
| Juan G. Carmona ([@juangcarmona](https://github.com/juangcarmona)) | Plain Concepts | Founding maintainer, BDFL pro tempore |

**Contributors** are anyone who opens an issue, an RFC, or a pull request.

The target composition, stated openly: at least three maintainers from at least two organizations before v1.0 freezes. Until then, the founding maintainer acts as benevolent dictator pro tempore, and this is understood as a bootstrap state, not the destination. If you maintain an implementation or run PDaC in production and want to help govern the spec, open an issue.

## Decision process

- **Editorial changes** (typos, clarity, formatting, non-normative text): a maintainer merges directly.
- **Normative changes** (anything that alters what MUST, MUST NOT, SHOULD or MAY mean for a conforming repository or implementation): require an RFC (see [CONTRIBUTING.md](CONTRIBUTING.md)), a public comment window of the length stated there, and consensus among maintainers. Consensus means no maintainer objects; with three or more maintainers, a single objection triggers a discussion and, if unresolved after 14 days, a simple majority decides.
- **Breaking changes** to the spec after v1.0 require a new major version and an explicit migration note.

## How v0.1.0 was released

RFC 0021 and RFC 0022 were accepted without the public comment window this document requires. RFC 0022 was opened, accepted and implemented on the same day. That was a deliberate decision by the founding maintainer in order to close v0.1, not an oversight, and it is recorded here because a governance rule quietly skipped is worse than one openly suspended.

The window applies as written from v0.1.0 onward. Its length was revised in the same release, from a flat 14 days to a period matched to what an RFC does, on the reasoning that a window exists to buy external review and there was no external constituency to spend it: a rule nobody can use is a rule that teaches its author to break rules, which is what happened here.

## Versioning and stability

The specification is versioned with semantic versioning, independently of any implementation. Stability levels per chapter are declared in the spec index: `stable` (normative, breaking changes need a major version), `draft` (normative intent, may change in minor versions) and `experimental` (may change or disappear at any time). Until v1.0, all chapters are at most `draft`.

## Scope of this organization

The `product-definition-as-code` organization hosts the specification, the manifesto, the conformance corpus and neutral tooling (`pdac-lint`). Implementations live in their own homes. The organization will not ship a competing implementation; if the reference implementation is ever donated here, it will be governed separately from the spec.

## Trademark and name

"Product Definition as Code" and "PDaC" name the methodology and this specification. Anyone may claim conformance if their implementation passes the published conformance corpus for the spec version they target. Do not use the names to imply endorsement of a specific product.
