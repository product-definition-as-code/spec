# RFC 0021: Deployment topologies: the model repository, co-located or dedicated

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-06
- **Related:** #4 (delivery-model reset), which narrowed this RFC's scope to where cited models live
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/2>

## Problem

The specification does not say which repository the Product Definition lives in. The manifesto does. [Conformance](../spec/conformance.md) clause 1 requires it under a configured product root, default `docs/product`, and says nothing about the repository. [Manifesto](../MANIFESTO.md) principle 1 says product knowledge "lives in the repository, close to the software it defines".

Read strictly, principle 1 requires a co-located layout that no MUST in the spec requires. It is also the first text an adopter reads, and it fails two ordinary cases: one product spanning several repositories, where there is no single "the repository"; and product authors who need to write artifacts without commit access to application code.

What PDaC actually depends on is narrower: product knowledge lives in a git repository, as plain files, diffable, reviewable by pull request and deterministically validatable. That holds in either layout.

Two chapters already defer to this issue. [Citation Contract](../spec/citation-contract.md) tracks cross-repository citation resolution here, and [Product Changes](../spec/product-changes.md) says citations resolve within one repository in v0.1 and that this issue owns the rest. A reader following either arrives at an open issue.

### Why now

[RFC 0004](0004-delivery-model-reset.md) left this issue open on purpose and narrowed its scope to where cited models live.

That was right at the time: the vocabulary this text needs was still moving. `Product Definition`, `Product Change`, apply and the citation contract all changed shape in that reset, so topology rules written then would have needed a second rewrite.

Nothing new is known about topologies. What changed is that the vocabulary settled across PRs #9, #14 and #19, and the corpus got its first independent runner. Both reasons for waiting are gone, so the clauses below can be written against stable terms and tested rather than asserted.

## Proposal

### 1. The model repository

A conforming Product Definition MUST live in a git repository, as files under the product root defined by [Conformance](../spec/conformance.md). The repository holding it is the **model repository**.

This names a subject. It adds no obligation on the files themselves.

### 2. Topologies

The model repository MAY be the same repository as the software it defines (**co-located topology**) or a repository of its own (**dedicated topology**). Both conform.

When one repository serves the product, co-location SHOULD be the default: the definition, its review history and the software stay on one review surface.

Both topologies use the same product-root layout, artifact contracts, validation and Product Change lifecycle. A dedicated model repository is not a different kind of repository, only one whose software lives elsewhere.

An implementation MUST NOT require a co-located software tree in order to validate a Product Definition.

A model repository holds one Product Definition. Splitting one Product Definition across repositories stays out of scope.

The four layouts adopters ask about:

| Layout                                                        | Topology   | v0.1                                                               |
| ------------------------------------------------------------- | ---------- | ------------------------------------------------------------------ |
| Monorepo: one repository holding the product and its software | co-located | conforming, and the default                                        |
| One repository per product, beside the software it defines     | co-located | conforming, and the default                                        |
| One product spanning several software repositories            | dedicated  | conforming; each consuming repository carries the clause 3 pointer  |
| One Product Definition split across several repositories      | neither    | out of scope; a model repository holds one Product Definition       |

The table restates clauses 1 to 3 and adds nothing. Every row keeps the same invariant: git, plain files, one product root, and no network service owning it (clause 4).

### 3. The pointer from a consuming repository

In the dedicated topology, a consuming repository SHOULD carry a machine-readable pointer to the model repository, so a tool or an agent can find the product context instead of being told out of band.

The pointer is a record. It MUST carry:

| Field          | Presence | Meaning                                            |
| -------------- | -------- | -------------------------------------------------- |
| `repository`   | required | a resolvable git location of the model repository  |
| `revision`     | required | a git revision resolving to exactly one commit     |
| `product-root` | required | the product root path within the model repository  |

`revision` MUST NOT be a branch name. A branch moves, so a pointer to one resolves to different files on different days, which deterministic validation forbids ([manifesto](../MANIFESTO.md) principle 10). A repository that wants to follow a branch advances its pointer, which is a reviewable diff.

`product-root` is required because the root is configurable, so a consumer MUST NOT assume `docs/product`.

The pointer MUST be readable as data, without executing code.

The pointer locates the model repository and MUST NOT contain, summarize or restate product artifacts. A pointer carrying product text would be one more place for knowledge to drift.

A consuming repository carries at most one pointer in v0.1. More than one is a multi-repository graph, out of scope.

**Deferred on purpose.** v0.1 fixes the pointer's record shape and not its serialization or its location, the same way the [Citation Contract](../spec/citation-contract.md) fixes the citation record and not one of its three forms. Resolution stays implementation-defined: how a tool fetches the model repository, caches it, authenticates, or behaves when it is unreachable.

That deferral has a cost, stated plainly: until one serialization is normalized, two implementations can both conform and still not read each other's pointer. Fixing the record shape bounds the cost, because the fields will not be invented twice. It closes when a pilot carries pointers in at least two consuming repositories and two implementations resolve them, which is how [RFC 0004](0004-delivery-model-reset.md) treats citation forms in its first open question.

No diagnostic code is allocated. `PRODUCT070`-`PRODUCT079` is reserved for model-repository resolution and stays unissued until there is a serialization to check, since a code no portable input can trigger cannot be tested. Reserved codes follow the existing rule: never renumbered, never reused.

### 4. No network service as the source of truth

A network service, whether a database, a wiki, an issue tracker or an API, MUST NOT be the source of truth for a Product Definition.

Services that serve the compiled graph or projections of it, including read APIs, agent-facing servers and dashboards, are permitted and encouraged. They are generated outputs, so they inherit the existing rule: reproducible from canonical files, never authoritative ([manifesto](../MANIFESTO.md) principle 2).

An implementation MUST NOT read canonical product artifacts from a network service. It MAY serve them.

This is what keeps clause 2 safe. Relaxing which repository the model lives in must not relax that it lives in a repository.

### 5. Manifesto principle 1

Principle 1 is reworded to:

> Product knowledge lives in a git repository, as files. Co-located with the code when one repository serves; dedicated when many do.

The manifesto is non-normative. This rewording lands with the spec text in the follow-up pull request, not in this one.

## Testability

[CONTRIBUTING](../CONTRIBUTING.md) requires every normative statement to be testable, and requires an RFC to say why a clause the corpus cannot check is normative anyway. The issue proposed one fixture for the dedicated topology and deferred pointer fixtures. That was checked with `pdac-lint` at `178c13b`, built from source and driving the reference implementation over candidate fixtures, rather than reasoned about.

**The dedicated-topology fixture works today.** A case whose `repo/` holds only the product root, with `expected.json` asserting zero diagnostics, runs and passes. It needs none of the case-format extension the two apply cases [wait on](../conformance/README.md).

**It discriminates.** Against a stand-in implementation that demands a co-located software tree, the same fixture fails. So it does check clause 2's obligation on implementations.

**It cannot show the topology positively.** A control fixture identical except for source files beside the product root passes the same `expected.json`. A case's `repo/` is just a directory tree, so a model repository standing alone looks exactly like a co-located one whose software was left out of the fixture. The case proves that co-located software is not required, which is what clause 2 asks for, and nothing more.

**Clause 1's git requirement is not checked at all.** The runner copies each fixture into a scratch directory with no git metadata, and both candidates passed there. An implementation that ignores git passes every case in this corpus. Clause 1 is normative anyway and lands as a repository-conformance criterion verified by review, next to [Conformance](../spec/conformance.md) clause 5, which already rests on a canonical branch and a reviewed merge. Checking it by fixture would need fixtures that are git repositories with history, a corpus-wide change this RFC does not propose.

**Clause 3 needs a case format that does not exist.** A pointer case needs two repository roots, the consumer and the model repository it points at, plus a resolution step; a case today is one `repo/`. Nesting one inside the other would fake it and would privilege a path-based pointer that clause 3 declines to mandate. A case declaring anything beyond `diagnostics` is skipped rather than failed, and a skip is not evidence, so declaring one now would record nothing. Pointer fixtures arrive with the serialization.

**Clause 4 cannot be falsified by a fixture,** because it forbids something that leaves no trace in a file tree. It is normative anyway: it decides whether a setup is PDaC at all, and the follow-up puts it in implementation conformance, checked by review.

Net: one fixture that runs today, two clauses verified by review with the reason recorded, one clause's fixtures deferred with its serialization, and no case-format extension requested.

## Impact

- **On existing conformant repositories:** none. All are co-located; co-location stays conforming and stays the default when one repository serves the product. No path, artifact, frontmatter field, diagnostic or lifecycle rule changes. Adopting the dedicated topology means moving the product root elsewhere, which is a choice, not a migration this RFC imposes.
- **On the specification:** a Topologies section, suggested home [Conformance](../spec/conformance.md); a **model repository** entry in [Terminology](../spec/terminology.md); clause 1 of repository conformance naming it; implementation-conformance criteria for clauses 2 and 4; the reserved `PRODUCT070`-`PRODUCT079` band in [Validation](../spec/validation.md); and updates to the deferral notes in [Citation Contract](../spec/citation-contract.md) and [Product Changes](../spec/product-changes.md). Those notes are updated, not removed: this RFC settles where a cited model may live, and cross-repository citation resolution stays deferred.
- **On existing implementations:** minimal. Nothing done today becomes non-conforming. Two prohibitions are added, on requiring co-located software and on reading canonical artifacts from a network service, and any implementation reading files under a configured product root already satisfies both. Pointer resolution is implementation-defined in v0.1 and required of nobody.
- **On the conformance corpus:** one case added, `dedicated-topology`, verified to run and pass. No existing case changes. Pointer cases deferred per Testability.
- **On the manifesto:** principle 1 reworded per clause 5.
- **On positioning:** answers the two objections adopters raise first, that a product is fourteen repositories and that product people have no code access, without weakening the git-and-files invariant.

## Alternatives considered

- **Keep the strict reading, co-location required.** Simplest, and it fails both the multi-repository product and the write-access case. It also invites private forks of the methodology for "enterprise" layouts.
- **Allow a network service as the source of truth.** Rejected. Not diffable, not reviewable as pull requests, and it puts authentication and availability inside the definition of truth. It brings back the wiki failure mode.
- **Specify a full multi-repository graph now.** Deferred. A dedicated model repository covers the dominant need; splitting one Product Definition across repositories waits for real adopter requirements.
- **Specify the pointer's serialization now, a fixed path and format.** Tempting: it would be corpus-testable immediately as a single-repository fixture and would close the interoperability gap. Rejected for v0.1 because no adopter has carried a pointer yet, and a file every consuming repository must agree on should be normalized after a pilot, not invented before one.
- **Defer the pointer entirely.** Rejected. Clause 2 makes the dedicated topology conforming, and a dedicated setup with no way to find its model repository leaves the location in out-of-band knowledge. A record shape with a deferred serialization is the smaller gap.
- **Leave the issue open and let the manifesto wording stand.** Rejected. Two chapters already point here for an answer, and deferring a third time would keep the coupling rather than being neutral about it.

## Consequences

The model repository becomes a named thing, so later work can say where something lives without saying which repository holds the code. Cross-repository citation resolution stays deferred but now has a subject: a citation resolves against a model repository, and the open question is how a consumer reaches one it does not contain.

Relaxing the repository relaxes nothing else. Layout, validation, Product Changes, apply, acceptance by reviewed merge and the citation contract are identical in both topologies. The only observable difference is whether the software sits in the same working tree, and clause 2 forbids an implementation from caring.

The coupling removed here was never in the normative text. It was in the sentence adopters read first.

## Open questions

1. The pointer's serialization and its location in a consuming repository. Deferred per clause 3; closed by a pilot with pointers in two consuming repositories and two implementations resolving them.
2. Cross-repository citation resolution: how a citation verifies a digest against a model repository the consumer does not contain, and whether an unreachable model repository is `unresolved` (`PRODUCT060`) or a status of its own. v0.1 keeps citations resolving within one repository.
3. Whether the corpus should ever check clause 1 directly, which needs fixtures that are git repositories with history. A corpus-format question, out of scope here.
