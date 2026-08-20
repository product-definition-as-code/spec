---
id: UC-VALIDATE-002
type: use-case
title: Validate scenario anchors
status: active
primary-actor: ACT-VALIDATOR
---

## Goal

Detect citations whose anchor names a verification scenario the target does not declare.

## Trigger

A validation run is requested on the consumer documents.

## Preconditions

The product model compiles and the consumer documents carry citation records.

## Main Flow

1. The validator resolves each citation's target artifact.
2. The validator looks the anchor up among the target's verification scenario ids.
3. Anchors that name no scenario are reported as errors.

## Alternative Flows

None.

## Failure Conditions

An anchor names a scenario id the target does not declare.

## Postconditions

All anchors resolve, or errors are reported.
