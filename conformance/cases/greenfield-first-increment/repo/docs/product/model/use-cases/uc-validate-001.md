---
id: UC-VALIDATE-001
type: use-case
title: Validate artifact references
status: active
primary-actor: ACT-VALIDATOR
governed-by:
  - BR-NO-SILENT-EDITS
  - BR-CITE-CANONICAL
---

## Goal

Detect unresolved artifact references before a Product Change is applied.

## Trigger

A validation run is requested on a Product Change.

## Preconditions

The change's overlay can be compiled from the baseline and its proposed artifacts.

## Main Flow

1. The validator compiles the product graph from the overlay.
2. The validator checks every reference for a resolvable target.
3. Unresolved references are reported as errors.

## Alternative Flows

None.

## Failure Conditions

A reference targets an unknown ID.

## Postconditions

All references resolve, or errors are reported.
