# Product Definition as Code: Specification

> **Status: v0.1 draft (request for comments).** Extracted from the reference implementation and under public review; see the [repository README](../README.md) for milestones. All chapters are currently at stability level `draft` as defined in [GOVERNANCE.md](../GOVERNANCE.md).

This is the normative specification for Product Definition as Code; the chapters below define its terms, contracts and conformance criteria.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** in these documents are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Human-facing explanations live in the [manifesto](../MANIFESTO.md), in particular the position in full. Where any explanatory text and this specification appear to disagree, this specification wins.

![The PDaC boundary. Inside, six numbered concerns: the accepted product definition, product artifacts, relationships, Product Changes, validation and impact analysis, and citations to the definition; below them, drawn dashed, the derived graph and its views. Outside: SDD specifications, backlogs, technical design, source code, deployment, runtime operation and release management. The definition is cited by SDD specifications, which guide implementation, which produces evidence; a dashed amber arrow labelled "may reveal" runs from evidence back to Product Changes. The closing line reads: PDaC defines the product, delivery builds it.](../assets/diagrams/pdac-1-product-definition-context.png)

_Figure PDaC-1 - what is inside Product Definition as Code and what is outside? Non-normative; the chapters below are authoritative._

## Contents

The grouping below mirrors the manifesto's ["a kernel, a profile, a workflow"](../MANIFESTO.md) distinction, as a reading aid. It defines no conformance subset: what conformance means is defined solely by [Conformance](conformance.md), which today covers all three groups.

1. [Terminology](terminology.md) - definitions of the terms used normatively.

**The kernel** - stable identity, typed relationships, verifiable citations, deterministic validation.

2. [Identifiers](identifiers.md) - stable immutable IDs, prefixes, grammar, file naming.
3. [Relationships](relationships.md) - canonical relationship vocabulary and derivation rules.
4. [Citation Contract](citation-contract.md) - machine-verifiable references from consumer documents to canonical product text, citation statuses, the delivery boundary.
5. [Validation](validation.md) - deterministic diagnostics, stable codes, exit codes.

**The reference profile** - the artifact vocabulary: opinionated, a good default, distinguished from the kernel on purpose.

6. [Artifacts](artifacts.md) - artifact types, frontmatter contracts, required body sections, lifecycle states.
7. [Frontmatter reference](frontmatter-reference.md) - the exhaustive per-kind field tables: required and optional fields, allowed values, provenance.

**The reference workflow** - how the accepted definition evolves.

8. [Product Changes](product-changes.md) - change structure, operations, overlay validation, lifecycle, apply, initialisation through `CHG-INITIAL`, change history.

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

The `model/` root is normative; its subdirectory names and nesting are not. An implementation MUST inspect Markdown files recursively below `model/`, determine each product artifact's kind from its parsed frontmatter `type`, and MUST NOT infer or restrict an artifact kind from its path. Repositories MAY group artifacts by kind, domain or another local convention. The lifecycle directories directly below `changes/` remain normative because they determine whether a Product Change is live or inert history.

`docs/product/model/index.md` is a human navigation and orientation document only. It MUST NOT duplicate relationships and MUST NOT act as a generated product index.

Generated files MUST be reproducible from canonical sources at any time. Tools MUST NOT require a generated file to exist in order to rebuild it.
