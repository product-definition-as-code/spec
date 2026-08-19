---
id: CHG-REWORD-VALIDATION
type: product-change
title: Reword the detection requirement around the product graph
status: proposed
base-revision: '0000000'
operations:
  add: []
  modify:
    - FR-VALIDATE-001
  remove: []
---

## Problem

The detection requirement speaks of "artifact IDs" without naming the product graph they hold together, so the requirement reads narrower than the behaviour it governs.

## Intended Product Outcome

`FR-VALIDATE-001` states that unresolved references are detected wherever the product graph carries them.

## Rationale

A requirement phrased against the graph covers every relationship kind at once, instead of enumerating them.

## Affected Product Areas

Validation (`FR-VALIDATE-001`).

## Open Questions

None.

## Product Acceptance

The modified requirement's scenario `S1` still passes against the applied model.

## Out of Scope

The set of relationship kinds the graph defines.
