---
id: CHG-RETIRE-ANCHOR-UC
type: product-change
title: Retire anchor validation as a separate use case
status: proposed
base-revision: '0000000'
operations:
  add: []
  modify: []
  remove:
    - UC-VALIDATE-002
---

## Problem

Anchor validation is a step of reference validation, not a use case of its own, and keeping it separate splits one behaviour across two artifacts.

## Intended Product Outcome

The model no longer contains `UC-VALIDATE-002`; anchor checking is understood as part of `UC-VALIDATE-001`.

## Rationale

One use case per operator-visible behaviour keeps the journey readable; a use case that only restates a step of another is noise.

## Affected Product Areas

Validation (`UC-VALIDATE-002`, `JRN-VALIDATE`).

## Open Questions

None.

## Product Acceptance

The applied model validates without errors and the journey's steps all resolve.

## Out of Scope

The behaviour of anchor checking itself.
