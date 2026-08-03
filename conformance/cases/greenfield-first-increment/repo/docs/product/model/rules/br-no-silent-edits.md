---
id: BR-NO-SILENT-EDITS
type: business-rule
title: No silent edits to the baseline
status: active
applies-to:
  - UC-VALIDATE-001
---

## Rule

The baseline MUST NOT be modified except by a human merging a validated proposed revision.

## Rationale

Silent edits break trust in the canonical model.

## Examples

A tool auto-merging a model change violates this rule.

## Exceptions

None.
