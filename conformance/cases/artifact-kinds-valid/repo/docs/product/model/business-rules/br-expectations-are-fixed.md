---
id: BR-EXPECTATIONS-ARE-FIXED
type: business-rule
title: Expectations belong to the case, never to the implementation
status: active
applies-to:
  - UC-EVALUATE-001
uses-terms:
  - TERM-RULE
---

## Rule

What a case expects MUST be fixed by the case itself, and MUST NOT be derived from, negotiated with, or adjusted to the implementation being evaluated.

## Rationale

An expectation an implementation can influence measures nothing: the tool would be marking its own work, and every verdict would be a tautology.

## Examples

A case expects one diagnostic and the implementation emits two: the case fails, and the surplus is reported. A case expects a diagnostic the implementation cannot yet produce: the case fails, and it stays failing until the implementation catches up.

## Exceptions

None. A case believed to be wrong is contested and changed for every implementation at once, never for one.
