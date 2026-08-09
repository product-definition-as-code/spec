# Conformance

## Repository conformance

A repository conforms to Product Definition as Code v0.1 when:

1. Its canonical product definition lives in a git repository, the **model repository**, under a configured product root (default `docs/product`) with the model/changes layout defined in this specification. See [Topologies](#topologies).
2. Every product artifact satisfies the [artifact contracts](artifacts.md): valid frontmatter per schema, required body sections, valid lifecycle state.
3. Every ID satisfies the [identifier rules](identifiers.md) and every reference satisfies the [relationship vocabulary](relationships.md).
4. Structural validation of the baseline reports no errors. Warnings are permitted.
5. The Product Definition is the accepted product intent on the repository's canonical branch; semantic evolution happens only through [Product Changes](product-changes.md), applied by an explicit human-triggered apply and accepted by a reviewed merge. The first Product Definition enters through `CHG-INITIAL`, the same mechanism as every later change.
6. Every live Product Change satisfies the change contract: valid `change.md` frontmatter per schema, required body sections, operations consistent with `proposed/`, and an overlay that validates without errors.
7. Consumer documents outside `docs/product/model` MAY carry citations to canonical product text; a conforming tool verifies those citations per the [citation contract](citation-contract.md).
8. The canonical product artifacts are files in the model repository. A network service MUST NOT be the source of truth for the Product Definition. See [Services over the model](#services-over-the-model).

Clauses 1, 5 and 8 rest on facts a fixture cannot observe: a git repository, a canonical branch, a reviewed merge, and the absence of an external source of truth. They are verified by review of the repository, not by the conformance tests.

## Topologies

The model repository MAY be the same repository as the software it defines (**co-located topology**) or a repository of its own (**dedicated topology**). Both conform.

When one repository serves the product, co-location SHOULD be the default: the definition, its review history and the software stay on one review surface.

Both topologies use the same product root layout, the same artifact contracts, the same validation and the same Product Change lifecycle. A dedicated model repository is not a different kind of repository, only one whose software lives elsewhere.

A model repository holds one Product Definition. Splitting a single Product Definition across repositories is out of scope for v0.1.

| Layout                                                        | Topology   | v0.1                                                              |
| ------------------------------------------------------------- | ---------- | ----------------------------------------------------------------- |
| Monorepo: one repository holding the product and its software | co-located | conforms, and is the default                                      |
| One repository per product, beside the software it defines     | co-located | conforms, and is the default                                      |
| One product spanning several software repositories            | dedicated  | conforms; each consuming repository carries the pointer below      |
| One Product Definition split across several repositories      | neither    | out of scope; a model repository holds one Product Definition      |

### The model-repository pointer

In the dedicated topology, a consuming repository SHOULD carry a machine-readable pointer to the model repository, so that a tool or an agent can find the product context instead of being told out of band where it is.

The pointer is a record. It MUST carry:

| Field          | Presence | Meaning                                            |
| -------------- | -------- | -------------------------------------------------- |
| `repository`   | required | a resolvable git location of the model repository  |
| `revision`     | required | a git revision resolving to exactly one commit     |
| `product-root` | required | the product root path within the model repository  |

`revision` MUST NOT be a branch name. A branch moves, so a pointer to one resolves to different files on different days, which deterministic validation forbids. A repository that follows a branch advances its pointer, which is a reviewable diff.

`product-root` is required because the product root is configurable, so a consumer MUST NOT assume `docs/product`.

The pointer MUST be readable as data, without executing code.

The pointer locates the model repository and MUST NOT contain, summarize or restate product artifacts.

A consuming repository carries at most one model-repository pointer in v0.1.

This specification fixes the pointer's record shape and neither its serialization nor its location in the consuming repository, exactly as the [Citation Contract](citation-contract.md) fixes the citation record and not one of its three forms. Resolution is implementation-defined in v0.1: how an implementation fetches the model repository, caches it, authenticates, and what it reports when the repository is unreachable. `PRODUCT070`-`PRODUCT079` is reserved for model-repository resolution and no code in that band is issued in v0.1.

### Services over the model

A network service, whether a database, a wiki, an issue tracker or an API, MUST NOT be the source of truth for a Product Definition.

Services that serve the compiled graph or projections of it, including read APIs, agent-facing servers and dashboards, are permitted and encouraged. They are generated outputs, so they are reproducible from canonical files and never authoritative ([Specification index → Canonical authority](index.md#canonical-authority)).

## Implementation conformance

An implementation (tooling) conforms when:

1. It validates all of the above deterministically, emitting the diagnostic codes, fields, ordering and exit codes defined in [Validation](validation.md).
2. It compiles the product graph exclusively from canonical files and can always rebuild every derived output.
3. It derives reverse relationships and never requires reciprocal authoring.
4. It computes digests with the mandated LF normalization.
5. It validates a Product Change by compiling and validating its overlay, without modifying any baseline file.
6. It applies a Product Change only under the rules in [Product Changes → Apply](product-changes.md#apply): approved status (`PRODUCT028` otherwise), revalidated overlay, baseline-revision compatibility, computed and reported product diff, `--dry-run` support, never implicitly, never committing. It MUST NOT treat a successful apply as acceptance.
7. It MUST NOT merge a proposal that fails structural validation (the CI gate); validation of a proposed tree is full structural validation.
8. It MUST NOT merge, auto-approve or self-merge model changes: merging is a human decision.
9. It MUST compute citation statuses deterministically per the [citation contract](citation-contract.md).
10. It treats warnings as non-fatal unless the repository opts into `warnings-as-errors`.
11. It MUST NOT require a co-located software tree in order to validate a Product Definition ([Topologies](#topologies)).
12. It MUST NOT read canonical product artifacts from a network service. It MAY serve them ([Services over the model](#services-over-the-model)).

## Violation mapping

Each normative statement in this specification maps to a diagnostic in [Validation](validation.md), except where the statement is about the repository rather than its files: clauses 1, 5 and 8 of repository conformance are verified by review, as stated above. The conformance fixtures under `conformance/cases/` exercise representative violations and assert their codes. Diagnostic codes are stable and are never renumbered or reused. A change to normative behaviour MUST update the specification, the diagnostic table and the fixtures together.
