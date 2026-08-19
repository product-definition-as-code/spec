---
id: CHG-INITIAL
type: product-change
title: Establish the first Product Definition
status: applied
base-revision: '0000000'
operations:
  add:
    - ACT-VALIDATOR
    - JRN-VALIDATE
    - UC-VALIDATE-001
    - FR-VALIDATE-001
  modify: []
  remove: []
---

## Problem

The product has no definition, so a consumer document has nothing canonical to cite.

## Intended Product Outcome

An accepted Product Definition describing the validator, the journey and use case through which validation happens, and the requirement that unresolved references are detected.

## Rationale

Initialisation uses the same mechanism as every later change.

## Affected Product Areas

The whole model; it did not exist before this change.

## Open Questions

None.

## Product Acceptance

The applied model validates without errors.

## Out of Scope

Delivery decomposition, technical design and implementation.
