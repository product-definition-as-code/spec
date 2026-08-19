---
id: CHG-DRAFT-REPORTING
type: product-change
title: Fix the reporting granularity of unresolved references
status: draft
base-revision: '0000000'
operations:
  add: []
  modify: []
  remove: []
---

## Problem

Unresolved references are detected, but no requirement states that each of them is reported exactly once, so an implementation may legally flood the report with duplicates.

## Intended Product Outcome

The model states the reporting granularity for unresolved references.

## Rationale

A requirement that fixes the reporting granularity is verifiable; one that does not leaves the report's shape to the implementation.

## Affected Product Areas

Validation.

## Open Questions

None.

## Product Acceptance

The new requirement's scenario `S1` passes against the applied model.

## Out of Scope

Changing how unresolved references are detected.
