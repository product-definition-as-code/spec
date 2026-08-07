---
id: CHG-INITIAL
type: product-change
title: Establish the first Product Definition
status: applied
base-revision: '0000000'
operations:
  add:
    - ACT-IMPLEMENTER
    - JRN-CLAIM-CONFORMANCE
    - UC-EVALUATE-001
    - BR-EXPECTATIONS-ARE-FIXED
    - BC-CONFORMANCE
    - TERM-FIXTURE
    - FR-EVALUATE-001
    - QR-DETERMINISM-001
    - CON-PLAIN-FILES-001
  modify: []
  remove: []
---

## Problem

The product has no definition: what conformance means, and the language it is claimed in, exist only as shared assumption.

## Intended Product Outcome

An accepted Product Definition describing who claims conformance, the journey and use case through which they do it, the rule that keeps expectations honest, the language the claim is made in, and the obligations a verdict carries.

## Rationale

Initialisation uses the same mechanism as every later change, so a product has one way to evolve rather than two.

## Affected Product Areas

The whole model; it did not exist before this change.

## Open Questions

None.

## Product Acceptance

The applied model validates without errors, and every declared artifact kind resolves the references it carries.

## Out of Scope

Delivery decomposition, technical design and implementation of anything described here.
