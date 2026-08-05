---
id: CHG-INITIAL
type: product-change
title: Establish the first Product Definition
status: applied
base-revision: 0000000
operations:
  add:
    - ACT-PRODUCT-ENGINEER
    - ACT-VALIDATOR
    - JRN-VALIDATE
    - UC-VALIDATE-001
    - BR-NO-SILENT-EDITS
    - BR-CITE-CANONICAL
    - FR-GREENFIELD-001
  modify: []
  remove: []
---

## Problem

The product has no definition: there is nothing for a consumer document to cite and nothing to validate.

## Intended Product Outcome

An accepted Product Definition describing who validates a product model, the journey and use case through which they do it, the rules that govern how the definition changes, and the requirement that the definition is established this way.

## Rationale

Initialisation uses the same mechanism as every later change, so a product has one way to evolve rather than two.

## Affected Product Areas

The whole model; it did not exist before this change.

## Open Questions

None.

## Product Acceptance

The applied model validates without errors and every consumer citation into it resolves.

## Out of Scope

Delivery decomposition, technical design and implementation of anything described here.
