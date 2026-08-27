# Artifacts

This chapter defines the artifact types of the current product model, their frontmatter contracts, required body sections and lifecycle states. Product Changes are specified in their own [chapter](product-changes.md).

![The product definition model, subtitled: the model is compiled from canonical Markdown. Across the top, Actors (ACT-CUSTOMER, ACT-PAYMENT-SERVICE) participate in Journeys (JRN-CHECKOUT, JRN-REFUND), which realise Use Cases (UC-CHECKOUT, UC-REFUND), which are governed by Business Rules (BR-REFUND-001, BR-AUTH-001). At the centre sits the Product Definition, labelled accepted intent, versioned and reviewable. Use cases use the Domain, which contains Terms (TERM-) and Bounded Contexts (BC-), and are constrained by Requirements, which contains Functional (FR-), Quality (QR-) and Constraints (CON-). A Product Change, CHG-REFUND-002, marked a semantic proposed delta, affects the definition. The definition projects to derived views: snapshot, impact, reference validation, graph diff, navigation and citation status. A dashed arrow labelled cited by reaches outside to delivery consumers: SDD specifications, AI agents, human teams, and backlog or code. Two notes read: the base model, not the only possible model; and illustrative relationships, not exhaustive. The closing line reads: Product Definition is canonical, the graph is compiled from authored Markdown.](../assets/diagrams/pdac-2-product-definition-model.png)

_Figure PDaC-2 - what does it mean to define the product? Non-normative; this chapter is authoritative for the types, [Relationships](relationships.md) for the arrows, [Product Changes](product-changes.md) for the change and the [Citation Contract](citation-contract.md) for the consumers._

## Common contract

Every product artifact is a Markdown file whose YAML frontmatter MUST include:

```yaml
---
id: FR-VALIDATE-001 # stable immutable ID, see identifiers.md
type: functional-requirement # one of the types below
title: Detect unresolved artifact references
status: active # artifact lifecycle state
---
```

- `type` MUST be one of: `actor`, `journey`, `use-case`, `business-rule`, `domain-term`, `bounded-context`, `functional-requirement`, `quality-requirement`, `constraint`, `structured-behaviour`.
- Frontmatter MUST validate against the JSON Schema for its `type` (`schemas/<type>.schema.json`). Unknown frontmatter properties are invalid. The exhaustive per-kind field tables (required and optional properties, allowed values, ID patterns) are in the [Frontmatter reference](frontmatter-reference.md), maintained by hand against those authoritative schemas.
- The Markdown body MUST contain the required sections for its type as `##` headings, in the order listed. Additional sections MAY follow the required ones.
- Every artifact type additionally accepts the optional `provenance` object ([Frontmatter reference → Provenance](frontmatter-reference.md#provenance)).
- Artifacts MUST NOT carry author, owner, date, version or review metadata; Git history is the record of who changed what and when. `provenance` is not an exception to this rule but a different concern: it records the **evidence** behind recovered knowledge (its source, the confidence that evidence supports, and how it was recovered), and it SHOULD be set only on artifacts recovered from an existing system.
- Artifact bodies describe product behaviour and obligations. They MUST NOT contain implementation design (class names, package names, algorithms, framework or storage choices) unless naming an externally imposed, externally visible constraint is unavoidable.

## Artifact lifecycle

The artifact lifecycle (`artifactStatus`) is:

| Status       | Meaning                                                                      |
| ------------ | ---------------------------------------------------------------------------- |
| `draft`      | Incomplete or not yet approved. Not part of the accepted product definition. |
| `active`     | Part of the current product definition.                                      |
| `deprecated` | Still present but scheduled for replacement or removal.                      |
| `retired`    | No longer active; retained only for historical traceability.                 |

Rules:

- An `active` artifact MUST NOT reference a `retired` artifact.
- A reference from an `active` artifact to a `deprecated` artifact SHOULD produce a warning.
- `draft` artifacts MAY reference other `draft` artifacts.
- This lifecycle applies to product artifacts only. The artifact lifecycle and the [Product Change lifecycle](product-changes.md#lifecycle) are separate state machines and MUST NOT be mixed.

## Actor (`actor`, `ACT-`)

An Actor identifies who or what interacts with the product to achieve a meaningful outcome.

Additional frontmatter: `actor-kind` (required), one of `human`, `external-system`, `scheduled-process`, `product`.

Required body sections: `## Purpose`, `## Goals`, `## Responsibilities`, `## Boundaries`.

Actors are not personas. Actor artifacts MUST NOT model demographics or fictional persona details.

## Journey (`journey`, `JRN-`)

A Journey describes an end-to-end outcome pursued by an actor. It may cross use cases, channels, bounded contexts, external systems, manual activities, waiting periods, branches and failure paths.

Additional frontmatter: `primary-actor` (required, Actor ID); `steps` (required, ordered list of `- use-case: <UC id>` entries defining the main journey).

Required body sections: `## Intended Outcome`, `## Entry Conditions`, `## Journey Narrative`, `## Variants and Branches`, `## Completion Conditions`.

Branches and exceptional paths belong in the body. There is no workflow DSL: `steps` defines the main ordered path only. Journeys MUST NOT describe screen-by-screen UI behaviour unless the UI sequence is materially part of the product behaviour.

## Use Case (`use-case`, `UC-`)

A Use Case describes a concrete interaction through which an actor obtains a product outcome.

Additional frontmatter: `primary-actor` (required, Actor ID); `supporting-actors` (optional, list of Actor IDs); `bounded-context` (optional, Bounded Context ID); `governed-by` (optional, list of Business Rule IDs); `uses-terms` (optional, list of Domain Term IDs).

Required body sections: `## Goal`, `## Trigger`, `## Preconditions`, `## Main Flow`, `## Alternative Flows`, `## Failure Conditions`, `## Postconditions`.

The body describes observable behaviour, not implementation design.

## Business Rule (`business-rule`, `BR-`)

A Business Rule expresses durable product knowledge that governs behaviour. A rule that applies to multiple use cases or requirements MUST be independently identifiable and reusable rather than hidden inside stories, acceptance criteria, UI validation, code, database constraints, tests or SDD tasks.

Additional frontmatter: `applies-to` (optional, list of Journey, Use Case or Bounded Context IDs).

Required body sections: `## Rule`, `## Rationale`, `## Examples`, `## Exceptions`.

The `## Rule` section MUST contain one clear normative statement.

The `## Examples` section MAY contain local illustrations that do not require independent identity, reuse, lifecycle or citation. When a concrete, testable example is authored as a Structured Behaviour, that artifact is the canonical carrier of its clauses and `illustrates` is the canonical association to the Business Rule. The Business Rule body MUST NOT present an authored restatement as a second canonical carrier. It MAY mention the Structured Behaviour ID or contain non-canonical explanatory prose. It MAY carry a restatement only as a non-canonical projection that cites the Structured Behaviour and follows the [embedding rules](citation-contract.md#embedding). Whether differently worded prose restates the same behaviour is a review question, not a deterministic validation rule.

## Domain Term (`domain-term`, `TERM-`)

A Domain Term establishes shared meaning.

Additional frontmatter: `defined-in` (required, Bounded Context ID); `synonyms` (optional, list of strings).

Required body sections: `## Definition`, `## Distinguish From`, `## Usage`.

A term's definition MUST NOT merely repeat its title.

## Bounded Context (`bounded-context`, `BC-`)

A Bounded Context is a product-language boundary: it delimits where a set of domain terms carries a specific meaning. Bounded contexts in v0.2 do not imply aggregates, implementation modules or source-code structure.

Additional frontmatter: none beyond the common contract. In particular, `owns-terms` MUST NOT be authored: term ownership is derived from `Domain Term.defined-in` (see [Relationships](relationships.md)).

Required body sections: `## Responsibility`, `## Language`, `## Boundaries`, `## External Relationships`.

## Functional Requirement (`functional-requirement`, `FR-`)

A Functional Requirement is a derived product obligation stating what the product must do.

Additional frontmatter: `derived-from` (required, non-empty list of Use Case, Business Rule or Constraint IDs); `verification` (required, non-empty list whose entries are either an inline `scenario` with an optional stable `id` for citation anchoring, or exactly one `scenario-ref` naming a Structured Behaviour; see [Frontmatter reference](frontmatter-reference.md)).

Required body sections: `## Requirement`, `## Rationale`.

The `## Requirement` section MUST use explicit normative language. A requirement MUST NOT be a disguised implementation task and MUST retain traceability to the product knowledge it derives from.

An inline `verification[].scenario` is the canonical carrier of that acceptance criterion. A `verification[].scenario-ref` is the canonical authored relationship to a Structured Behaviour. An item MUST use exactly one form and MUST NOT carry unknown properties. Inline and reference entries MAY be mixed in one Requirement, and inline verification remains conforming. The same Structured Behaviour MAY verify more than one Requirement. The same expected behaviour MUST NOT appear as both forms in the same Requirement. Whether differently worded entries express the same behaviour is a review question, not a deterministic validation rule.

The body SHOULD NOT restate verification criteria. A body section that reproduces them is a projection, not a second source. An artifact MAY carry such a projection; when it does, the projection MUST follow the [embedding rules](citation-contract.md#embedding), so that a copy edited by hand is detectable rather than silently divergent.

## Quality Requirement (`quality-requirement`, `QR-`)

A Quality Requirement states a measurable quality obligation.

Additional frontmatter: `quality-attribute` (required, string such as `portability`, `determinism`); `applies-to` (required, non-empty list of Journey, Use Case or Bounded Context IDs); `verification` (required, non-empty list using the same inline-or-reference union as a Functional Requirement; see [Frontmatter reference](frontmatter-reference.md)).

Required body sections: `## Requirement`, `## Measurement`.

The `## Measurement` section MUST state how conformance is measured: a vague quality statement ("the system should be fast") does not satisfy this contract. `verification` carries the acceptance criteria under the same rule as for a [Functional Requirement](#functional-requirement-functional-requirement-fr-): the body SHOULD NOT restate them.

## Constraint (`constraint`, `CON-`)

A Constraint expresses an externally imposed or deliberately fixed boundary.

Additional frontmatter: `applies-to` (optional, list of Journey, Use Case or Bounded Context IDs). When `applies-to` is absent, the constraint applies to the entire product.

Required body sections: `## Constraint`, `## Rationale`, `## Consequences`.

## Structured Behaviour (`structured-behaviour`, `SB-`)

A Structured Behaviour is one concrete, implementation-independent example of accepted observable product behaviour. It separates the context in which behaviour occurs, the single stimulus that occurs and the observable outcomes that follow. Authors MAY continue to use inline Requirement verification scenarios when independent identity, reuse, lifecycle or citation is not needed.

Additional frontmatter: `illustrates` (required, non-empty list of Use Case, Business Rule or Constraint IDs); `given` (optional, non-empty ordered list of context strings); `when` (required, one stimulus string); `then` (required, non-empty ordered list of outcome strings); `uses-terms` (optional, list of Domain Term IDs).

Required body sections: `## Intent`, `## Boundaries`.

`## Intent` explains why the example is product-significant. `## Boundaries` states what the example does not assert where a reader could otherwise mistake it for broader behaviour. `None.` is valid when no material boundary is known.

```yaml
---
id: SB-CANCEL-PAID-ORDER
type: structured-behaviour
title: Cancel a paid order while cancellation remains available
status: active
illustrates:
  - UC-CANCEL-ORDER
  - BR-CANCELLATION-WINDOW
given:
  - The order is in the PAID state
  - The cancellation window remains open
when: The customer requests cancellation
then:
  - The order enters the CANCELLED state
  - A refund is requested
uses-terms:
  - TERM-ORDER
---

## Intent

Establish the accepted result of cancelling an order whose payment has already been captured.

## Boundaries

This example does not specify how or when the refund is settled.
```

Each `given` entry states product context, `when` states one product-level stimulus and each `then` entry states an externally or business-observable outcome. Authors MUST NOT include literal `GIVEN`, `WHEN`, `THEN` or `AND` prefixes in those values. Renderers MAY supply those words for a target format.

All `given` entries are conjunctive, and all `then` entries are conjunctive. Alternative contexts or outcomes MUST be expressed as separate Structured Behaviour artifacts rather than an ambiguous `or` clause.

A Structured Behaviour MUST NOT name test classes, step definitions, selectors, mocks, database rows, internal messages or other implementation machinery. An externally visible API operation, event or document MAY be named when it is itself part of the product contract.

The required `illustrates` relationship gives every Structured Behaviour an authored position in the Product Graph. Absence of a Requirement reference does not make the behaviour disconnected or invalid. Implementations MAY report possible omissions as non-conformance advice for human review, but MUST NOT present that advice as a deterministic diagnostic.
