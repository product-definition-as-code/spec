---
id: FR-GREENFIELD-001
type: functional-requirement
title: Greenfield baseline is accepted via reviewed merge
status: active
derived-from:
  - BR-NO-SILENT-EDITS
verification:
  - id: S1
    scenario: An empty model receives a PR adding artifacts; after merge the baseline is valid.
  - id: S2
    scenario: A consumer spec cites the merged FR and a governing rule; all citations are current.
---

## Requirement

The initial product baseline MUST enter through the same reviewed-merge mechanism as every later change: a branch, full-tree structural validation, and a human merge into an empty model.

## Rationale

There is no special-cased first increment; the initial baseline uses the same mechanism as every later change.

## Acceptance Scenarios

- **S1.** An empty model receives a PR adding artifacts; after merge the baseline is valid.
- **S2.** A consumer spec cites the merged FR and a governing rule; all citations are `current`.
