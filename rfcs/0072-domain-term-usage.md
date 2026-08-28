# RFC 0072: Domain-term usage from semantic artifacts

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-24
- **Issue:** <https://github.com/product-definition-as-code/spec/pull/72>
- **Proposed target:** PDaC specification 0.2.0; additive `v1alpha1` schema evolution

## Problem

`uses-terms` is currently authored by a Use Case or Structured Behaviour only. Business Rules, Domain Terms, Functional Requirements, Quality Requirements and Constraints can require a Domain Term to be interpreted, but cannot record that typed dependency. `PRODUCT106` can therefore report a term as unused despite an artifact depending on it.

## Proposal

`uses-terms` declares that understanding the source artifact requires the target Domain Term. It remains canonical from the consuming artifact to a Domain Term; reverse views are derived and MUST NOT be authored.

The permitted sources are Use Case, Business Rule, Domain Term, Functional Requirement, Quality Requirement, Constraint and Structured Behaviour. The last two existing sources retain their meaning. Actors, Journeys and Bounded Contexts do not gain the field.

Business Rule, Domain Term, Functional Requirement, Quality Requirement and Constraint gain optional `uses-terms` arrays of Domain Term IDs. Existing documents remain valid. A Domain Term MAY depend on another Domain Term; this RFC does not prohibit cycles.

`PRODUCT106` applies only when a non-retired Domain Term has no valid incoming `uses-terms` edge from a non-retired permitted source. Prose mentions, ownership, generated reverse views and paths through other relationships do not count.

## Conformance

The existing all-kinds fixture adds one valid edge from each of the five newly permitted source kinds, alongside the existing Use Case and Structured Behaviour edges. A negative case covers an unresolved Constraint `uses-terms` target.

No new-field fixture isolates `PRODUCT007`. The `uses-terms` schemas admit only `TERM-` IDs, so an existing target with that prefix and a disallowed type also violates its own ID/type alignment and produces `PRODUCT004`; the two diagnostics have different subjects. This is the same limitation recorded for RFC 0084 relationship fields.

## Impact

- **Repositories:** no migration; every added field is optional.
- **Implementations:** add five schemas and graph edges, and evaluate `PRODUCT106` across all seven permitted source kinds.
- **Serialization:** `v1alpha1` is expanded backward-compatibly.
- **Diagnostics:** no code is added or renamed.

## Alternatives considered

### Infer usage through graph traversal

Rejected. Traversal does not record which artifact requires a term.

### Count prose mentions

Rejected. Prose is not a typed canonical relationship.

### Defer to v0.3

Rejected. This is an optional, backward-compatible expansion that resolves an existing false-positive warning before v0.2 freezes.

## Decision record

Pending human acceptance under [CONTRIBUTING.md](../CONTRIBUTING.md).
