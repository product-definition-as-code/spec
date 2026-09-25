---
id: FR-EXPORT-LOG-001
type: functional-requirement
title: Export covers exactly the requested period
status: active
derived-from:
  - UC-EXPORT-LOG-001
verification:
  - id: S1
    scenario: An export requested for a single day contains the activity recorded on that day and no activity recorded outside it.
---

## Requirement

An activity export MUST contain every activity record within the requested period and no record outside it.

## Rationale

An auditor relies on the export being complete and bounded; a partial or overreaching export makes the audit worthless without saying so.
