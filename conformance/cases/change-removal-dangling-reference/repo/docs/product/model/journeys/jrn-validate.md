---
id: JRN-VALIDATE
type: journey
title: Validate a Product Change
status: active
primary-actor: ACT-VALIDATOR
steps:
  - use-case: UC-VALIDATE-001
  - use-case: UC-VALIDATE-002
---

## Intended Outcome

A Product Change is structurally validated before it is applied to the Product Definition.

## Entry Conditions

A Product Change exists under `docs/product/changes/active/`.

## Journey Narrative

The validator compiles the change's overlay against the baseline and reports any defects.

## Variants and Branches

None.

## Completion Conditions

Validation passes with no errors, or errors are reported for human review.
