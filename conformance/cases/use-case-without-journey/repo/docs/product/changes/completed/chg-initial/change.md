---
id: CHG-INITIAL
type: product-change
title: Establish the first Product Definition
status: applied
base-revision: '0000000'
operations:
  add:
    - ACT-AUDITOR
    - UC-EXPORT-LOG-001
    - FR-EXPORT-LOG-001
  modify: []
  remove: []
---

## Problem

The product has no definition. The first decision to record is the export an auditor asks for, which is a standalone utility rather than a step inside a wider outcome.

## Intended Product Outcome

An accepted Product Definition holding the auditor, the export use case and the requirement that an export covers exactly the requested period.

## Rationale

The export is reached directly, so there is no end-to-end outcome to describe around it. Inventing a Journey to hold one step would state an ordering the product does not have.

## Affected Product Areas

The whole model; it did not exist before this change.

## Open Questions

None.

## Product Acceptance

The applied model validates without errors.

## Out of Scope

Retention policy, authorisation rules and the export file format.
