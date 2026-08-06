# RFC 0021: Deployment topologies: the model repository, co-located or dedicated

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-06
- **Related:** #4 (delivery-model reset), which narrowed this RFC's scope to where cited models live and how cross-repository citations resolve
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/2>

## Problem

The specification never says which repository the Product Definition lives in, and the manifesto does. [Conformance](../spec/conformance.md) clause 1 requires the canonical product definition to live under a configured product root, default `docs/product`, and says nothing about the repository holding it. [Manifesto](../MANIFESTO.md) principle 1 says product knowledge "lives in the repository, close to the software it defines". Read strictly, that principle couples the methodology to a co-located layout the normative text does not require, and it is the first text an adopter reads.

The coupling is accidental, not essential, and it breaks in two ordinary situations. One product frequently spans several repositories, so there is no single "the repository" for the model to live in. And the people who author product knowledge frequently should be able to write it without commit access to application code, which a co-located model cannot grant separately.

The invariant PDaC actually depends on is different and stronger: product knowledge lives in a git repository, as plain files, diffable, reviewable by pull request and deterministically validatable. That is what "as Code" means, and it holds in either layout.

Two chapters currently defer to this issue for an answer it has not given. [Citation Contract](../spec/citation-contract.md) records cross-repository citation resolution as out of scope and tracked here, and [Product Changes](../spec/product-changes.md) states that citations resolve within one repository in v0.1 and that cross-repository resolution is owned here. A reader following either pointer arrives at an open issue.

### Why now

This issue predates [RFC 0004](0004-delivery-model-reset.md) and was deliberately left open when 0004 was accepted, which recorded it as remaining open and narrowed its scope to where cited models live and how cross-repository citations resolve.

Leaving it open was right at the time. The delivery model was being reset, and the vocabulary this text has to be written in was still moving: `Product Definition`, `Product Change`, apply, acceptance and the citation contract all changed shape across that reset. Topology rules written against a vocabulary about to change would have needed a second rewrite, and would have been read as settled in the meantime.

What changed is not new information about topologies. The vocabulary settled across PRs #9, #14 and #19, and the conformance corpus acquired its first independent runner. Both reasons for waiting are gone, so the two questions this RFC owes an answer to can be decided against a stable vocabulary and checked against a runner rather than asserted. That is why the issue closes now instead of staying open a third time.

## Proposal

### 1. The model repository

A conforming Product Definition MUST live in a git repository, as files under the product root defined by [Conformance](../spec/conformance.md). The repository that holds it is the **model repository**.

This adds a terminology entry and names the subject of clause 1 of repository conformance. It states no new obligation on the files themselves.

### 2. Topologies

The model repository MAY be the same repository as the software it defines (**co-located topology**) or a repository of its own (**dedicated topology**). Both are conforming.

When one repository serves the product, co-location SHOULD be the default: it keeps the definition, its review history and the software it defines on a single review surface.

Both topologies use the same product-root layout, the same artifact contracts, the same validation and the same Product Change lifecycle. A dedicated model repository is not a different kind of repository; it is one whose software lives elsewhere.

An implementation MUST NOT require a co-located software tree in order to validate a Product Definition.

A model repository holds one Product Definition. Splitting a single Product Definition across repositories remains out of scope, and this RFC deliberately adds nothing that would make it easier by accident.

The four layouts adopters ask about resolve as follows:

| Layout                                                        | Topology    | v0.1                                                                       |
| ------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------- |
| Monorepo: one repository holding the product and its software | co-located  | conforming, and the default                                                |
| One repository per product, beside the software it defines     | co-located  | conforming, and the default                                                |
| One product spanning several software repositories            | dedicated   | conforming; each consuming repository carries the clause 3 pointer         |
| One Product Definition split across several repositories      | neither     | out of scope; a model repository holds one Product Definition              |

The table restates clauses 1 to 3 and adds nothing to them. In all four rows the invariant is the same: git, plain files, one product root, and no network service owning any of it (clause 4).

### 3. The pointer from a consuming repository

In the dedicated topology, a consuming repository SHOULD carry a machine-readable pointer to the model repository, so that a tool or an agent can resolve product context instead of being told out of band where it is.

The pointer is a record. It MUST carry:

| Field          | Presence | Meaning                                                          |
| -------------- | -------- | ---------------------------------------------------------------- |
| `repository`   | required | a resolvable git location of the model repository                |
| `revision`     | required | a git revision that resolves to exactly one commit               |
| `product-root` | required | the product root path within the model repository                |

`revision` MUST NOT be a branch name. A branch moves, and a pointer that moves resolves to different files on two machines on two days, which is what deterministic validation forbids ([manifesto](../MANIFESTO.md) principle 10). A repository that means to track a branch advances its pointer, which is a reviewable diff.

`product-root` is required because the product root is configurable, so a consumer MUST NOT assume `docs/product`.

The pointer MUST be readable as data, without executing code to compute it.

The pointer locates the model repository and carries no product content. It MUST NOT contain, summarize or restate product artifacts. A pointer carrying product text would be a re-statement surface, which is the thing PDaC exists to remove.

A consuming repository carries at most one model-repository pointer in v0.1. More than one is a multi-repository graph, which is out of scope.

**What this clause does not specify, deliberately.** v0.1 mandates the pointer's record shape and neither its serialization nor its location in the consuming repository, exactly as the [Citation Contract](../spec/citation-contract.md) mandates the citation record and not one of its three forms. Resolution semantics are likewise out of scope for v0.1 and remain implementation-defined: how an implementation fetches the model repository, what it does when the model repository is unreachable, how it caches and how it authenticates.

This is a decision and not an omission, and it has a cost worth stating plainly: until a serialization is normalized, two implementations can both conform and still fail to read each other's pointer. The mandated record shape bounds that cost, because when serializations do normalize they will normalize around one field set rather than three. What closes the deferral is a pilot carrying pointers in at least two consuming repositories with at least two implementations resolving them; a follow-up then normalizes one form, the same treatment [RFC 0004](0004-delivery-model-reset.md) gives concrete citation forms in its first open question.

No diagnostic code is allocated here. `PRODUCT070`-`PRODUCT079` are reserved for model-repository resolution and stay unissued until a serialization exists to check, because a code no portable input can trigger is a code that cannot be tested. Reserved codes follow the existing rule: never renumbered, never reused.

### 4. No network service as the source of truth

A network service, whether a database, a wiki, an issue tracker or an API, MUST NOT be the source of truth for a Product Definition.

Services that serve the compiled graph or projections of it, including read APIs, agent-facing servers and dashboards, are permitted and encouraged. They are generated outputs and inherit the existing rule: reproducible from canonical files, and never authoritative ([manifesto](../MANIFESTO.md) principle 2).

An implementation MUST NOT read canonical product artifacts from a network service. It MAY serve them.

This clause is what makes clause 2 safe. Relaxing which repository the model lives in must not relax that it lives in a repository at all.

### 5. Manifesto principle 1

Principle 1 is reworded to:

> Product knowledge lives in a git repository, as files. Co-located with the code when one repository serves; dedicated when many do.

The manifesto is non-normative. The rewording lands with the spec text in the follow-up pull request, not in this one.

## Testability

[CONTRIBUTING](../CONTRIBUTING.md) requires every normative statement to be testable, and requires an RFC whose clause the corpus cannot check to say why the clause is normative anyway. The issue proposed one fixture for the dedicated topology and deferred pointer-resolution fixtures. That proposal was checked with a runner rather than reasoned about: `pdac-lint` at `178c13b`, built from source, driving the reference implementation over candidate fixtures.

**The dedicated-topology fixture is expressible today.** A case whose `repo/` holds only the product root, with `expected.json` asserting zero diagnostics, runs and passes. It needs no case-format extension, unlike the two apply cases the [corpus](../conformance/README.md) defers until such a format exists.

**It discriminates.** Run against a stand-in implementation that requires a co-located software tree, the same fixture fails on an unexpected diagnostic. The case therefore has real power: it rejects an implementation that treats co-location as mandatory, which is exactly the obligation clause 2 places on implementations.

**It cannot express the topology positively.** A control fixture identical but for source files sitting alongside the product root passes the same `expected.json`. A case's `repo/` is a directory tree, so a model repository standing alone is indistinguishable from a co-located repository whose software was simply left out of the fixture. What the case verifies is that co-located software is not required, not that the fixture is a dedicated model repository. That is the honest reading, and it is sufficient here, because clause 2's normative content is a permission plus one prohibition on implementations, and the fixture checks the prohibition.

**Clause 1's git requirement is not exercised at all.** The runner copies each fixture into a scratch directory carrying no git metadata and runs the implementation there, which both candidate fixtures passed. An implementation indifferent to git passes every case in this corpus. Clause 1 is normative anyway, and lands as a repository-conformance criterion verified by review, alongside [Conformance](../spec/conformance.md) clause 5, which already rests on facts no fixture can observe: a canonical branch and a reviewed merge. Making clause 1 fixture-checkable would require fixtures that are themselves git repositories carrying history, which is a corpus-wide change this RFC does not propose.

**Clause 3 needs a case format the corpus does not have.** A pointer-resolution case needs at least two repository roots, a consuming repository and the model repository it points at, plus a resolution step, where a case today is one `repo/`. Nesting the model repository inside the consumer's tree would fake the topology and would quietly privilege a path-based pointer, which clause 3 declines to mandate. A case declaring structure beyond `diagnostics` is skipped rather than failed by the runner, and a skip is not evidence, so declaring such a case before the format exists would record nothing. Pointer fixtures are deferred with the serialization they depend on, and arrive with it.

**Clause 4 is unfalsifiable by fixture,** because it prohibits something that leaves no trace in a file tree. It is normative anyway: it decides whether a setup is PDaC at all, and it is checkable by review of an implementation, which is where the follow-up places it as an implementation-conformance criterion.

Net: one new fixture that runs today, one clause verified by review with the reason recorded, one clause whose fixtures are deferred with its serialization, and no case-format extension requested.

## Impact

- **On existing conformant repositories:** none. No existing conformant repository is affected. Every one of them is co-located, co-location stays conforming, and stays the recommended default when one repository serves the product. No path, artifact, frontmatter field, diagnostic or lifecycle rule changes. A repository that adopts the dedicated topology does so by moving its product root elsewhere, which is an adopter's choice and not a migration this RFC imposes.
- **On the specification:** a Topologies section, suggested home [Conformance](../spec/conformance.md) since that chapter states repository-level conformance; a **model repository** entry in [Terminology](../spec/terminology.md); clause 1 of repository conformance naming the model repository; an implementation-conformance criterion for clauses 2 and 4; the reserved `PRODUCT070`-`PRODUCT079` band in [Validation](../spec/validation.md); and an update to the two deferral notes in [Citation Contract](../spec/citation-contract.md) and [Product Changes](../spec/product-changes.md) that currently point at this issue. Those notes are updated rather than removed: this RFC settles where a cited model may live, and cross-repository citation resolution stays deferred.
- **On existing implementations:** minimal for conformance. Nothing an implementation does today becomes non-conforming. Two prohibitions are added, on requiring a co-located software tree and on reading canonical artifacts from a network service, and an implementation that reads files under a configured product root already satisfies both. Pointer resolution is implementation-defined in v0.1, can be added incrementally, and is required of no implementation.
- **On the conformance corpus:** one case added, `dedicated-topology`, verified to run and pass as `repo/` plus `expected.json`. No existing case changes. Pointer-resolution cases deferred per Testability.
- **On the manifesto:** principle 1 reworded per clause 5.
- **On positioning:** answers the two objections adopters raise first, that a product is fourteen repositories and that the people writing product knowledge have no code access, without weakening the git-and-files invariant.

## Alternatives considered

- **Keep the strict reading, co-location required.** Simplest, and it fails both the multi-repository product and the write-permission case. It also invites forks of the methodology for "enterprise" layouts, which is the worst outcome available: the kernel gets re-litigated privately, once per adopter.
- **Allow a network service as the source of truth.** Rejected. Not diffable, not reviewable as pull requests, and it moves authentication and availability inside the definition of truth. It reintroduces the wiki failure mode the methodology exists to remove.
- **Specify a full multi-repository graph now.** Deliberately deferred. A dedicated model repository covers the dominant need; splitting one Product Definition across repositories stays out of scope until real adopters bring requirements.
- **Specify the pointer's serialization now, a fixed path and file format.** Tempting, because it would be corpus-testable immediately as a single-repository fixture and would close the interoperability gap clause 3 leaves open. Rejected for v0.1: no adopter has carried a pointer yet, and a file that every consuming repository must agree on is exactly the surface that should be normalized after a pilot rather than invented before one. The record shape is the part that must not be invented twice, and clause 3 fixes it.
- **Defer the pointer entirely and mandate nothing.** Rejected. Clause 2 makes the dedicated topology conforming, and a conforming dedicated setup with no way to find its model repository pushes the location into out-of-band knowledge, which is where product knowledge goes to rot. A record shape with a deferred serialization is the smaller of the two gaps.
- **Leave the issue open and let the manifesto wording stand.** Rejected. Two spec chapters already point here for an answer, and silence has been the status quo across two accepted RFCs. Deferring a third time would be a decision to keep the coupling, not a neutral act.

## Consequences

The model repository becomes a named thing, which is what lets later work say where something lives without saying which repository holds the code. Cross-repository citation resolution stays deferred, but it now has a subject: a citation resolves against a model repository, and the open question is how a consumer reaches one it does not contain.

Relaxing the repository relaxes nothing else. Product root layout, validation, Product Changes, apply, acceptance by reviewed merge and the citation contract are identical in both topologies. The only difference a tool can observe is whether the software it serves happens to sit in the same working tree, and clause 2 forbids an implementation from caring.

The coupling this RFC removes was never in the normative text. It was in the sentence adopters read first, which constrained adoption more tightly than any MUST in the specification.

## Open questions

1. The pointer's serialization and its location in a consuming repository. Deferred per clause 3, and closed by a pilot carrying pointers in at least two consuming repositories with at least two implementations resolving them.
2. Cross-repository citation resolution: how a citation verifies a digest against a model repository the consuming repository does not contain, what it reports when that repository is unreachable, and whether unreachable is `unresolved` (`PRODUCT060`) or a status of its own. v0.1 keeps citations resolving within one repository.
3. Whether the corpus should ever check clause 1 directly, which would need fixtures that are git repositories carrying history. That is a corpus-format question rather than a topology question, and is out of scope here.
