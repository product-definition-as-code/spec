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
- **Normative changes** (anything that alters what MUST, MUST NOT, SHOULD or MAY mean for a conforming repository or implementation): require an RFC (see [CONTRIBUTING.md](CONTRIBUTING.md)), a public comment window of the length stated there, and consensus among maintainers. Consensus means no maintainer objects; with three or more maintainers, a single objection triggers a discussion and, if unresolved after 14 days, a simple majority decides. The deciding maintainer MUST record the decision and its rationale, SHOULD leave an RFC open while it is producing useful review, and MUST resolve substantive feedback before accepting it.
- **Breaking changes** to the spec after v1.0 require a new major version and an explicit migration note.

## How v0.1.0 was released

RFC 0021 and RFC 0022 were accepted without the public comment window this document requires. RFC 0022 was opened, accepted and implemented on the same day. That was a deliberate decision by the founding maintainer in order to close v0.1, not an oversight, and it is recorded here because a governance rule quietly skipped is worse than one openly suspended.

The window applied from v0.1.0 until the founder-led stabilization exception, whose end is recorded below. Its length was revised in the same release, from a flat 14 days to a period matched to what an RFC does, on the reasoning that a window exists to buy external review and there was no external constituency to spend it: a rule nobody can use is a rule that teaches its author to break rules, which is what happened here.

The window then stopped applying for the duration of the v0.2 extraction. The founding maintainer exercised the BDFL pro tempore bootstrap authority described under [Roles](#roles) to suspend only the minimum elapsed-time requirement, on the same reasoning, while the specification was still being pulled out of one implementation.

## How v0.2.0 was released

The suspension was recorded on 2026-08-24. Five RFCs were accepted under it: RFC 0072, RFC 0077, RFC 0084, RFC 0085 and RFC 0093. Three of those were opened, accepted and implemented on the same day. That was the point of the exception, and it is recorded here rather than left to be reconstructed from merge dates. The RFCs accepted earlier in the v0.2 cycle, RFC 0038, RFC 0042, RFC 0047 and RFC 0066, predate the suspension and were subject to the windows as revised at v0.1.0.

The exception ends with v0.2.0. Its own text sunset it at the first stable specification version, and v0.2.0 is not stable, so this ends it earlier than promised. Ending an exception ahead of its sunset needs no new authority: it only gives back a latitude the founding maintainer had granted himself. The reason to give it back now is that the condition it rested on is gone. The extraction is finished, the specification is published as a request for comments, and the conformance tests are executable by anyone, so an elapsed-time window now has someone to buy review from.

The obligations that ran through the suspension are folded into the decision process above so they survive it.

Ending the exception left the minimum elapsed times keyed to a release number, which is the wrong trigger. At v0.2.0 there is no independent implementation and one adopter, so a 7-day wait on an RFC written and reviewed by one person buys no review at all. That is the condition this document already diagnosed for v0.1.0: a rule nobody can use is a rule that teaches its author to break rules. Restoring an unusable rule would have set up the same failure a second time and called it governance.

So the windows in [CONTRIBUTING.md](CONTRIBUTING.md) are keyed to the constituency instead: the minimum elapsed times begin once gate 2 or gate 3 in [MATURITY.md](MATURITY.md) is met, an independent implementation or a listed adopter other than the reference implementation. This is not the suspension under another name. The suspension was a latitude the founding maintainer granted himself, sunset at a version, and it took a governance act to end. This is a published condition inside the rule: it is checkable by anyone, it begins on its own, and no maintainer can extend it. The BDFL bootstrap authority is not exercised here and is not needed.

## Versioning and stability

The specification is versioned with semantic versioning, independently of any implementation. Stability levels per chapter are declared in the spec index: `stable` (normative, breaking changes need a major version), `draft` (normative intent, may change in minor versions) and `experimental` (may change or disappear at any time). Until v1.0, all chapters are at most `draft`.

## Scope of this organization

The `product-definition-as-code` organization hosts the specification, the manifesto, the conformance tests and neutral tooling (`pdac-conformance`). Implementations live in their own homes. The organization will not ship a competing implementation; if the reference implementation is ever donated here, it will be governed separately from the spec.

## Trademark and name

"Product Definition as Code" and "PDaC" name the methodology and this specification. Anyone may claim conformance if their implementation passes the published conformance tests for the spec version they target. Do not use the names to imply endorsement of a specific product.
