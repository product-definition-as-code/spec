# Product Definition as Code: Specification

> **Status: v0.1 draft (request for comments).** Extracted from the reference implementation and under public review; see the [repository README](../README.md) for milestones. All chapters are currently at stability level `draft` as defined in [GOVERNANCE.md](../GOVERNANCE.md).

This is the normative specification for Product Definition as Code. It defines the terminology, the artifact contracts and their exhaustive frontmatter, identity rules, relationship vocabulary, accepted product intent, change-as-PR, the citation contract, deterministic validation and conformance criteria.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** in these documents are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Human-facing explanations live in the [methodology overview](https://github.com/juangcarmona/productshape/blob/main/docs/methodology/overview.md) of the reference implementation. Where any explanatory text and this specification appear to disagree, this specification wins.

## Contents

1. [Terminology](terminology.md) - definitions of the terms used normatively.
2. [Artifacts](artifacts.md) - artifact types, frontmatter contracts, required body sections, lifecycle states.
3. [Frontmatter reference](frontmatter-reference.md) - the exhaustive per-kind field tables (generated from the schemas): required and optional fields, allowed values, provenance.
4. [Identifiers](identifiers.md) - stable immutable IDs, prefixes, grammar, file naming.
5. [Relationships](relationships.md) - canonical relationship vocabulary and derivation rules.
6. [Citation Contract](citation-contract.md) - machine-verifiable references from consumer documents to canonical product text, citation statuses, the delivery boundary.
7. [Validation](validation.md) - deterministic diagnostics, stable codes, exit codes.
8. [Conformance](conformance.md) - what it means for a repository and an implementation to conform.

## Canonical authority

Within a repository that adopts Product Definition as Code:

| Path                                                                                                                | Authority                                                         |
| ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `docs/product/model/**/*.md`                                                                                        | Canonical current product semantics (the accepted baseline)        |
| Consumer documents outside `docs/product/model` (SDD specs, tasks, agent prompts, design docs)                      | Non-canonical; carry citations to canonical product text           |
| Graph files, generated indexes, Mermaid diagrams, traceability reports                                              | Generated and non-canonical                                       |

`docs/product/model/index.md` is a human navigation and orientation document only. It MUST NOT duplicate relationships and MUST NOT act as a generated product index.

Generated files MUST be reproducible from canonical sources at any time. Tools MUST NOT require a generated file to exist in order to rebuild it.
