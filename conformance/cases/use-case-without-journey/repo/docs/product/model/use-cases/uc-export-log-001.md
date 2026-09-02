---
id: UC-EXPORT-LOG-001
type: use-case
title: Export the activity log for a period
status: active
primary-actor: ACT-AUDITOR
---

## Goal

Obtain the recorded activity for a chosen period as a file the auditor can keep.

## Trigger

The auditor requests an export for a period.

## Preconditions

The auditor is authorised to read recorded activity.

## Main Flow

1. The auditor chooses the period to export.
2. The product collects the activity recorded in that period.
3. The product returns the collected activity as a downloadable file.

## Alternative Flows

None.

## Failure Conditions

The requested period is outside the retention window.

## Postconditions

The auditor holds an export covering exactly the requested period, or a stated reason why none was produced.
