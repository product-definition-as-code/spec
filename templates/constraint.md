---
id: CON-EXAMPLE-001
type: constraint
title: Booking records stay in the customer's region
status: draft
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Constraint: an externally imposed or deliberately fixed boundary. When
applies-to is absent, the constraint applies to the entire product.
Contract: spec/artifacts.md (Constraint). Fields: spec/frontmatter-reference.md.
-->

## Constraint

Booking records MUST be stored and processed in the customer's contracted region.

## Rationale

Customer contracts and regional data protection law impose residency; the product does not get to choose.

## Consequences

Availability across regions cannot be answered from one shared store, and moving a customer between regions is a migration, not a setting.
