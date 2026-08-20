---
id: FR-VALIDATE-002
type: functional-requirement
title: Report each unresolved reference exactly once
status: active
derived-from:
  - UC-VALIDATE-001
verification:
  - id: S1
    scenario: A validation run over a model with one unresolved reference reports exactly one diagnostic for it.
---

## Requirement

The product MUST report each unresolved reference exactly once per validation run.

## Rationale

Duplicate diagnostics for one defect bury the report's signal; a fixed granularity keeps reports comparable across runs.
