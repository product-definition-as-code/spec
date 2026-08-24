# Frontmatter reference

The exhaustive field contract of every document kind: which properties are allowed, which are required, and what values they accept.

[Artifacts](artifacts.md) defines what each artifact type _means_ and why it exists; this chapter defines the _fields_. Where the two appear to disagree, the JSON Schemas under `schemas/` win: the tables below are maintained by hand against the schemas.

Every kind is a **closed** object: an unknown property is a `PRODUCT002` error, not a warning and not silently ignored. There is no extension point. If you need to record something the schema does not allow, put it in the Markdown body.

Conforming implementations SHOULD expose this contract programmatically (for example as a schema query command), so it can be inspected without a repository.

## How to read the tables

| Column         | Meaning                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| Field          | The YAML key. `a.b` is a nested key; `a[]` is an array element, and `a[].b` a key of an element object. |
| Required       | Whether the key must be present. For a nested key, whether it is required _when its parent is present_. |
| Type           | `string`, `const` (one permitted value), `enum`, `array`, `object`.                                     |
| Allowed values | The permitted values, or the regular expression a string must match.                                    |
| Notes          | Constraints and guidance carried by the schema itself.                                                  |

Four fields are common to every Markdown-authored kind: `id` (stable and immutable, see [Identifiers](identifiers.md)), `type`, `title` and `status`. Artifact `status` is `draft | active | deprecated | retired`; the Product Change lifecycle is separate and is listed with its own kind below.

## Provenance

`provenance` is an optional object accepted by all nine artifact kinds. It records the **evidence** behind recovered knowledge: where a claim came from and how strongly the evidence supports it.

Set it on recovered (brownfield) artifacts. Leave it unset on greenfield artifacts authored from intent: there is no evidence to cite, and an empty claim of provenance is worse than none.

Provenance is deliberately _not_ authorship metadata. [Artifacts](artifacts.md) forbids author, owner, date, version and review fields because Git history already records who changed what and when. Provenance answers a different question: how far to trust this artifact's content.

A `draft` artifact whose `provenance.confidence` is `low` produces a `PRODUCT111` warning, so the queue of candidates needing human validation is derivable from validation output rather than tracked by hand.

| Field            | Required | Allowed values                                           | Meaning                                                                                                                                                                  |
| ---------------- | -------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `source`         | yes      | free text                                                | A file path, a URL, a ticket reference, or `interview: <person>`.                                                                                                        |
| `confidence`     | yes      | `high`, `medium`, `low`                                  | `high`: read directly from a specification scenario or a test. `medium`: inferred from structured prose. `low`: inferred from indirect evidence such as a variable name. |
| `recovered-from` | no       | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered. Optional, because real evidence is often more than one of these.                                                                        |

```yaml
provenance:
  source: src/orders/validation.ts (limit check), tests/orders/limits.spec.ts
  confidence: high
  recovered-from: observation
```

`provenance` itself is closed: an unrecognised sub-field such as `recovered-by` is a `PRODUCT002` error, and omitting `confidence` while providing `source` is too.

---

## Artifact frontmatter

The nine artifact types of the current product model.

### Actor

`ACT-`. Who or what interacts with the product to achieve a meaningful outcome. See [Artifacts → Actor](artifacts.md#actor-actor-act-).

| Field                       | Required | Type   | Allowed values                                             | Notes                                                                                                                                                              |
| --------------------------- | -------- | ------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string | `^ACT-[A-Z0-9]+(-[A-Z0-9]+)*$`                             |                                                                                                                                                                    |
| `type`                      | yes      | const  | `actor`                                                    |                                                                                                                                                                    |
| `title`                     | yes      | string |                                                            | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum   | `draft`, `active`, `deprecated`, `retired`                 | Lifecycle of a product artifact.                                                                                                                                   |
| `actor-kind`                | yes      | enum   | `human`, `external-system`, `scheduled-process`, `product` |                                                                                                                                                                    |
| `provenance`                | no       | object |                                                            | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string |                                                            | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum   | `high`, `medium`, `low`                                    | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum   | `observation`, `inference`, `interview`, `documentation`   | How the knowledge was recovered from the evidence.                                                                                                                 |

### Journey

`JRN-`. An end-to-end outcome pursued by an actor. `steps` defines the main ordered path only; branches and exceptional paths belong in the body. See [Artifacts → Journey](artifacts.md#journey-journey-jrn-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^JRN-[A-Z0-9]+(-[A-Z0-9]+)*$`                           |                                                                                                                                                                    |
| `type`                      | yes      | const           | `journey`                                                |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `primary-actor`             | yes      | string          | `^ACT-[A-Z0-9]+(-[A-Z0-9]+)*$`                           |                                                                                                                                                                    |
| `steps`                     | yes      | array of object |                                                          | The main ordered journey. Branches and exceptional paths belong in the body. At least one entry.                                                                   |
| `steps[].use-case`          | yes      | string          | `^UC-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Use Case

`UC-`. A concrete interaction through which an actor obtains a product outcome. See [Artifacts → Use Case](artifacts.md#use-case-use-case-uc-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^UC-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `type`                      | yes      | const           | `use-case`                                               |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `primary-actor`             | yes      | string          | `^ACT-[A-Z0-9]+(-[A-Z0-9]+)*$`                           |                                                                                                                                                                    |
| `supporting-actors`         | no       | array of string |                                                          |                                                                                                                                                                    |
| `supporting-actors[]`       | yes      | string          | `^ACT-[A-Z0-9]+(-[A-Z0-9]+)*$`                           |                                                                                                                                                                    |
| `bounded-context`           | no       | string          | `^BC-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `governed-by`               | no       | array of string |                                                          |                                                                                                                                                                    |
| `governed-by[]`             | yes      | string          | `^BR-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `uses-terms`                | no       | array of string |                                                          |                                                                                                                                                                    |
| `uses-terms[]`              | yes      | string          | `^TERM-[A-Z0-9]+(-[A-Z0-9]+)*$`                          |                                                                                                                                                                    |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Business Rule

`BR-`. Durable product knowledge that governs behaviour. See [Artifacts → Business Rule](artifacts.md#business-rule-business-rule-br-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^BR-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `type`                      | yes      | const           | `business-rule`                                          |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `applies-to`                | no       | array of string |                                                          |                                                                                                                                                                    |
| `applies-to[]`              | yes      | string          | `^(JRN\|UC\|BC)-[A-Z0-9]+(-[A-Z0-9]+)*$`                 | A journey, use case or bounded context.                                                                                                                            |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Domain Term

`TERM-`. Shared meaning within a bounded context. Ownership is authored here, on the term, and never on the context. See [Artifacts → Domain Term](artifacts.md#domain-term-domain-term-term-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^TERM-[A-Z0-9]+(-[A-Z0-9]+)*$`                          |                                                                                                                                                                    |
| `type`                      | yes      | const           | `domain-term`                                            |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `defined-in`                | yes      | string          | `^BC-[A-Z0-9]+(-[A-Z0-9]+)*$`                            | Canonical direction of term ownership. Bounded contexts never author owns-terms.                                                                                   |
| `synonyms`                  | no       | array of string |                                                          |                                                                                                                                                                    |
| `synonyms[]`                | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Bounded Context

`BC-`. A product-language boundary. Note the absence of `owns-terms`: term ownership is derived from `Domain Term.defined-in` and MUST NOT be authored here (see [Relationships](relationships.md)). See [Artifacts → Bounded Context](artifacts.md#bounded-context-bounded-context-bc-).

| Field                       | Required | Type   | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | ------ | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string | `^BC-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `type`                      | yes      | const  | `bounded-context`                                        |                                                                                                                                                                    |
| `title`                     | yes      | string |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum   | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `provenance`                | no       | object |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum   | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum   | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Functional Requirement

`FR-`. A derived product obligation stating what the product must do. `derived-from` is what keeps it traceable to the knowledge it came from. See [Artifacts → Functional Requirement](artifacts.md#functional-requirement-functional-requirement-fr-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^FR-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `type`                      | yes      | const           | `functional-requirement`                                 |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `derived-from`              | yes      | array of string |                                                          | Traceability to the use cases, business rules or constraints this requirement originates from. At least one entry.                                                 |
| `derived-from[]`            | yes      | string          | `^(UC\|BR\|CON)-[A-Z0-9]+(-[A-Z0-9]+)*$`                 |                                                                                                                                                                    |
| `verification`              | yes      | array of object |                                                          | At least one entry.                                                                                                                                                |
| `verification[].scenario`   | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `verification[].id`         | no       | string          | `^[A-Z0-9]+(-[A-Z0-9]+)*$`                               | Optional stable id, unique within the artifact. When present, the scenario is citable via anchor (see [Citation Contract](citation-contract.md)).                   |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Quality Requirement

`QR-`. A measurable quality obligation. See [Artifacts → Quality Requirement](artifacts.md#quality-requirement-quality-requirement-qr-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^QR-[A-Z0-9]+(-[A-Z0-9]+)*$`                            |                                                                                                                                                                    |
| `type`                      | yes      | const           | `quality-requirement`                                    |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `quality-attribute`         | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `applies-to`                | yes      | array of string |                                                          | At least one entry.                                                                                                                                                |
| `applies-to[]`              | yes      | string          | `^(JRN\|UC\|BC)-[A-Z0-9]+(-[A-Z0-9]+)*$`                 | A journey, use case or bounded context.                                                                                                                            |
| `verification`              | yes      | array of object |                                                          | At least one entry.                                                                                                                                                |
| `verification[].scenario`   | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `verification[].id`         | no       | string          | `^[A-Z0-9]+(-[A-Z0-9]+)*$`                               | Optional stable id, unique within the artifact. When present, the scenario is citable via anchor (see [Citation Contract](citation-contract.md)).                   |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

### Constraint

`CON-`. An externally imposed or deliberately fixed boundary. When `applies-to` is absent the constraint applies to the entire product. See [Artifacts → Constraint](artifacts.md#constraint-constraint-con-).

| Field                       | Required | Type            | Allowed values                                           | Notes                                                                                                                                                              |
| --------------------------- | -------- | --------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                        | yes      | string          | `^CON-[A-Z0-9]+(-[A-Z0-9]+)*$`                           |                                                                                                                                                                    |
| `type`                      | yes      | const           | `constraint`                                             |                                                                                                                                                                    |
| `title`                     | yes      | string          |                                                          | Must not be empty.                                                                                                                                                 |
| `status`                    | yes      | enum            | `draft`, `active`, `deprecated`, `retired`               | Lifecycle of a product artifact.                                                                                                                                   |
| `applies-to`                | no       | array of string |                                                          |                                                                                                                                                                    |
| `applies-to[]`              | yes      | string          | `^(JRN\|UC\|BC)-[A-Z0-9]+(-[A-Z0-9]+)*$`                 | A journey, use case or bounded context.                                                                                                                            |
| `provenance`                | no       | object          |                                                          | Evidence behind recovered knowledge. Set on recovered (brownfield) artifacts only.                                                                                 |
| `provenance.source`         | yes      | string          |                                                          | Where the knowledge came from: a file path, a URL, a ticket reference, or 'interview: <person>'. Must not be empty.                                                |
| `provenance.confidence`     | yes      | enum            | `high`, `medium`, `low`                                  | high: read directly from a specification scenario or a test. medium: inferred from structured prose. low: inferred from indirect evidence such as a variable name. |
| `provenance.recovered-from` | no       | enum            | `observation`, `inference`, `interview`, `documentation` | How the knowledge was recovered from the evidence.                                                                                                                 |

---

## Product Change frontmatter

### Product Change

`CHG-`. The Markdown-authored definition of a proposed change to the baseline. Authored by hand and validated through the same schema path as the artifacts. Semantics, lifecycle and overlay rules are in [Product Changes](product-changes.md).

Note that `provenance` is **not** accepted here. Recovered knowledge carries provenance on the proposed artifacts, which are ordinary artifact documents, not on the change itself; this holds for `CHG-INITIAL` on a brownfield product like any other change.

| Field                 | Required | Type            | Allowed values                                                       | Notes                                                      |
| --------------------- | -------- | --------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------- |
| `id`                  | yes      | string          | `^CHG-[A-Z0-9]+(-[A-Z0-9]+)*$`                                       |                                                            |
| `type`                | yes      | const           | `product-change`                                                     |                                                            |
| `title`               | yes      | string          |                                                                      | Must not be empty.                                         |
| `status`              | yes      | enum            | `draft`, `proposed`, `approved`, `applied`, `rejected`, `superseded` | Lifecycle of a product change.                             |
| `base-revision`       | yes      | string          | `^[0-9a-f]{7,40}$`                                                   | Baseline Git revision, or exactly `0000000` only for `CHG-INITIAL`. |
| `operations`          | yes      | object          |                                                                      |                                                            |
| `operations.add`      | yes      | array of string |                                                                      |                                                            |
| `operations.add[]`    | yes      | string          | `^(ACT\|JRN\|UC\|BR\|TERM\|BC\|FR\|QR\|CON)-[A-Z0-9]+(-[A-Z0-9]+)*$` | Any artifact of the current product model.                 |
| `operations.modify`   | yes      | array of string |                                                                      |                                                            |
| `operations.modify[]` | yes      | string          | `^(ACT\|JRN\|UC\|BR\|TERM\|BC\|FR\|QR\|CON)-[A-Z0-9]+(-[A-Z0-9]+)*$` | Any artifact of the current product model.                 |
| `operations.remove`   | yes      | array of string |                                                                      |                                                            |
| `operations.remove[]` | yes      | string          | `^(ACT\|JRN\|UC\|BR\|TERM\|BC\|FR\|QR\|CON)-[A-Z0-9]+(-[A-Z0-9]+)*$` | Any artifact of the current product model.                 |

`base-revision` normally names the Git commit containing the baseline against which the change was created. The exact seven-character string `0000000` is the reserved **no-baseline sentinel** only when `id` is `CHG-INITIAL`; it records that no commit names the empty Product Definition baseline. An implementation MUST NOT resolve that pair against Git. Other all-zero strings and `0000000` on any other Product Change are ordinary revisions. `CHG-INITIAL` MAY instead name a real commit at which the Product Definition is empty ([RFC 0066](../rfcs/0066-initial-base-revision-sentinel.md)).

