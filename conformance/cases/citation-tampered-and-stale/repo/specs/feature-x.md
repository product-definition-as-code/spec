# Feature X

This feature implements validation of artifact references. The governing requirement is projected below from the canonical model; the block is read-only and regenerable.

<!-- pdac:cite id="FR-VALIDATE-001" digest="sha256:cd567f9e119089438556095f639b896e63f638a7cf5efd50d951f2ae24ead8c4" -->
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

The product MAY detect references to unknown artifact IDs and report them as validation errors.

## Rationale

Unresolved references break the product graph; catching them deterministically prevents silent drift between artifacts.
<!-- /pdac:cite -->

The implementation follows the projected requirement.
