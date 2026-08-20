---
id: CHG-AMEND-REPORTING
type: product-change
title: State that each unresolved reference is reported exactly once
status: proposed
base-revision: '0000000'
operations:
  add: []
  modify:
    - FR-VALIDATE-002
  remove: []
---

## Problem

Unresolved references are detected, but no requirement states that each of them is reported exactly once, so an implementation may legally flood the report with duplicates.

## Intended Product Outcome

`FR-VALIDATE-002` states that every unresolved reference is reported exactly once.

## Rationale

A requirement that fixes the reporting granularity is verifiable; one that does not leaves the report's shape to the implementation.

## Affected Product Areas

Validation (`FR-VALIDATE-002`).

## Open Questions

None.

## Product Acceptance

The modified requirement's scenario `S1` passes against the applied model.

## Out of Scope

Changing how unresolved references are detected.
