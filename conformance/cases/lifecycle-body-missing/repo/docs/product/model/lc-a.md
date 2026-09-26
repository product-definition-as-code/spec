---
id: LC-A
type: domain-lifecycle
title: LC-A
status: draft
subject: TERM-A
states:
- id: OPEN
  title: Open
  initial: true
- id: DONE
  title: Done
  terminal: true
transitions:
- id: FINISH
  title: Finish
  from:
  - OPEN
  to: DONE
  trigger: The actor finishes
  initiated-by:
  - ACT-A
  governed-by:
  - BR-A
  realized-by:
  - UC-A
---

## Purpose

Product meaning for this fixture.

## Invariants

Product meaning for this fixture.

## State Semantics

Product meaning for this fixture.

## Transition Semantics

Product meaning for this fixture.
