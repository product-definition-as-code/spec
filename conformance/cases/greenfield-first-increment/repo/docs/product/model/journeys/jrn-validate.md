---
id: JRN-VALIDATE
type: journey
title: Validate a proposed revision
status: active
primary-actor: ACT-VALIDATOR
steps:
  - use-case: UC-VALIDATE-001
---

## Intended Outcome

A proposed revision is structurally validated before merge.

## Entry Conditions

A proposed revision exists on a branch.

## Journey Narrative

The validator runs structural validation on the proposed tree and reports any defects.

## Variants and Branches

None.

## Completion Conditions

Validation passes with no errors, or errors are reported for human review.
