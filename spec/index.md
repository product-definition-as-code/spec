# Product Definition as Code: Specification

> **Status: v0.1 draft (request for comments).** Extracted from the reference implementation and under public review; see the [repository README](../README.md) for milestones. All chapters are currently at stability level `draft` as defined in [GOVERNANCE.md](../GOVERNANCE.md).

This is the normative specification for Product Definition as Code. It defines the terminology, the artifact contracts and their exhaustive frontmatter, identity rules, relationship vocabulary, the accepted Product Definition, Product Change semantics, the citation contract, deterministic validation and conformance criteria.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** in these documents are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Human-facing explanations live in the [manifesto](../MANIFESTO.md), in particular the position in full. Where any explanatory text and this specification appear to disagree, this specification wins.

![The PDaC boundary. Inside, six numbered concerns: the accepted product definition, product artifacts, relationships, Product Changes, validation and impact analysis, and citations to the definition; below them, drawn dashed, the derived graph and its views. Outside: SDD specifications, backlogs, technical design, source code, deployment, runtime operation and release management. The definition is cited by SDD specifications, which guide implementation, which produces evidence; a dashed amber arrow labelled "may reveal" runs from evidence back to Product Changes. The closing line reads: PDaC defines the product, delivery builds it.](../assets/diagrams/pdac-1-product-definition-context.png)

_Figure PDaC-1 - what is inside Product Definition as Code and what is outside? Non-normative; the chapters below are authoritative._

## Contents

1. [Terminology](terminology.md) - definitions of the terms used normatively.
2. [Artifacts](artifacts.md) - artifact types, frontmatter contracts, required body sections, lifecycle states.
3. [Frontmatter reference](frontmatter-reference.md) - the exhaustive per-kind field tables (generated from the schemas): required and optional fields, allowed values, provenance.
4. [Identifiers](identifiers.md) - stable immutable IDs, prefixes, grammar, file naming.
5. [Relationships](relationships.md) - canonical relationship vocabulary and derivation rules.
6. [Product Changes](product-changes.md) - change structure, operations, overlay validation, lifecycle, apply, initialisation through `CHG-INITIAL`, change history.
7. [Citation Contract](citation-contract.md) - machine-verifiable references from consumer documents to canonical product text, citation statuses, the delivery boundary.
8. [Validation](validation.md) - deterministic diagnostics, stable codes, exit codes.
9. [Conformance](conformance.md) - what it means for a repository and an implementation to conform, the co-located and dedicated topologies a model repository may take, and the pointer to a dedicated one.

## Canonical authority

Within a repository that adopts Product Definition as Code:

| Path                                                                                                                | Authority                                                         |
| ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `docs/product/model/**/*.md`                                                                                        | Canonical current product semantics (the accepted Product Definition) |
| `docs/product/changes/active/**/change.md`                                                                          | Canonical definition of a live Product Change                     |
| `docs/product/changes/active/**/proposed/**/*.md`                                                                   | Canonical proposed future-state product semantics for that change |
| `docs/product/changes/completed/**`, `docs/product/changes/rejected/**`, `docs/product/changes/superseded/**`       | Change history; inert, never compiled into the graph              |
| Consumer documents outside `docs/product/model` (SDD specs, tasks, agent prompts, design docs)                      | Non-canonical; carry citations to canonical product text           |
| Graph files, generated indexes, Mermaid diagrams, traceability reports                                              | Generated and non-canonical                                       |

`docs/product/model/index.md` is a human navigation and orientation document only. It MUST NOT duplicate relationships and MUST NOT act as a generated product index.

Generated files MUST be reproducible from canonical sources at any time. Tools MUST NOT require a generated file to exist in order to rebuild it.
