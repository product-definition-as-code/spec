---
id: FR-EXAMPLE-001
type: functional-requirement
title: Reject bookings beyond the lead time
status: draft
derived-from:
  - BR-EXAMPLE-001
verification:
  - scenario: A booking whose start lies beyond the lead time is rejected and the member is told the earliest permitted start.
    id: BEYOND-LEAD-TIME
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Functional Requirement: a derived product obligation stating what the product
must do, in explicit normative language, never a disguised implementation task.
derived-from: the use cases, business rules or constraints it follows from.
verification: each entry is either an inline scenario (optional stable id makes
it citable by anchor) or exactly one scenario-ref naming a Structured Behaviour:
  - scenario-ref: SB-EXAMPLE-001
The body should not restate the verification entries.
Contract: spec/artifacts.md (Functional Requirement). Fields: spec/frontmatter-reference.md.
-->

## Requirement

The product MUST reject any booking whose start lies more than the permitted lead time after the day the booking is made.

## Rationale

Derived from BR-EXAMPLE-001: the lead time only protects availability if the product enforces it at the moment of booking.
