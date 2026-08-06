---
id: FR-VALIDATE-001
type: functional-requirement
title: Detect unresolved artifact references
status: active
derived-from:
  - UC-VALIDATE-001
verification:
  - id: S1
    scenario: A validation run reports an unresolved reference with code PRODUCT006.
---

## Requirement

The product MUST detect references to unknown artifact IDs and report them as validation errors.

## Rationale

Unresolved references break the product graph; catching them deterministically prevents silent drift between artifacts.

## Acceptance Scenarios

- **S1.** A validation run reports an unresolved reference with code `PRODUCT006`.
