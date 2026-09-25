---
id: LC-A
type: domain-lifecycle
title: LC-A
status: active
subject: TERM-A
states:
- id: OPEN
  title: Open
  initial: true
- id: DONE
  title: Done
  terminal: true
- id: REVIEW
  title: Review
transitions:
- id: FINISH
  title: Finish
  from:
  - OPEN
  - REVIEW
  to: DONE
  trigger: The actor finishes
  initiated-by:
  - ACT-A
  governed-by:
  - BR-A
  realized-by:
  - UC-A
- id: REVIEW
  title: Enter review
  from:
  - OPEN
  to: REVIEW
  trigger: Review
---

## Purpose

Product meaning for this fixture.

## Invariants

Product meaning for this fixture.

## State Semantics

Product meaning for this fixture.

## Transition Semantics

Product meaning for this fixture.

## Boundaries

Product meaning for this fixture.
