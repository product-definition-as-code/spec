---
id: CHG-RETIRE-REPORTING
type: product-change
title: Retire the duplicate-reporting requirement
status: proposed
base-revision: '0000000'
operations:
  add: []
  modify: []
  remove:
    - FR-VALIDATE-002
---

## Problem

The model is believed to carry a requirement about reporting granularity that the product no longer needs.

## Intended Product Outcome

The model no longer contains `FR-VALIDATE-002`; reporting granularity is left to the implementation.

## Rationale

A requirement nobody consumes is noise in the definition; removing it keeps the model honest about what the product promises.

## Affected Product Areas

Validation (`FR-VALIDATE-002`).

## Open Questions

None.

## Product Acceptance

The applied model validates without errors and no artifact references the removed ID.

## Out of Scope

The detection requirement `FR-VALIDATE-001`.
