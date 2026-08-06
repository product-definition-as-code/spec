# Feature X

This feature implements validation of artifact references. The governing requirement is projected below from the canonical model; the block is read-only and regenerable.

<!-- pdac:cite id="FR-VALIDATE-001" digest="sha256:0c1ac562387d45687f560ec88975080cb9b12041b560a19b64c329df75d2cbcd" -->
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

## Acceptance Scenarios

- **S1.** A validation run reports an unresolved reference with code `PRODUCT006`.
<!-- /pdac:cite -->

The implementation follows the projected requirement.
