---
id: CHG-TIGHTEN-VALIDATION
type: product-change
title: State how unresolved references surface to the operator
status: proposed
base-revision: '0000000'
operations:
  add: []
  modify:
    - FR-VALIDATE-001
  remove: []
---

## Problem

Validation detects unresolved references, but the requirement does not state how the failure surfaces to the operator.

## Intended Product Outcome

`FR-VALIDATE-001` states that every unresolved reference is reported as a validation error with a deterministic code.

## Rationale

A requirement that names the observable failure is verifiable; one that does not leaves the behaviour to the implementation.

## Affected Product Areas

Validation (`FR-VALIDATE-001`).

## Open Questions

None.

## Product Acceptance

The modified requirement's scenario `S1` still passes against the applied model.

## Out of Scope

Changing the diagnostic codes themselves.
