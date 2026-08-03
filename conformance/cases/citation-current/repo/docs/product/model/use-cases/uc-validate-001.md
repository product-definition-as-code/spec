---
id: UC-VALIDATE-001
type: use-case
title: Validate artifact references
status: active
primary-actor: ACT-VALIDATOR
---

## Goal

Detect unresolved artifact references before a proposal is merged.

## Trigger

A validation run is requested on a proposed revision.

## Preconditions

The proposed tree is available for validation.

## Main Flow

1. The validator compiles the product graph from the proposed tree.
2. The validator checks every reference for a resolvable target.
3. Unresolved references are reported as errors.

## Alternative Flows

None.

## Failure Conditions

A reference targets an unknown ID.

## Postconditions

All references resolve, or errors are reported.
