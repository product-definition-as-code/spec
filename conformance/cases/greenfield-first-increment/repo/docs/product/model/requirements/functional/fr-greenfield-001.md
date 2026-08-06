---
id: FR-GREENFIELD-001
type: functional-requirement
title: The first Product Definition is established by CHG-INITIAL
status: active
derived-from:
  - BR-NO-SILENT-EDITS
verification:
  - id: S1
    scenario: An empty model receives CHG-INITIAL; after apply and merge the Product Definition is valid.
  - id: S2
    scenario: A consumer spec cites the accepted FR and a governing rule; all citations are current.
---

## Requirement

The first Product Definition MUST be established by `CHG-INITIAL`, applied into an empty model and accepted through review, using the same mechanism as every later Product Change.

## Rationale

There is no special-cased first increment and no separate greenfield or brownfield path; only the knowledge available at initialisation differs.
