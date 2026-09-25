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
  - DONE
  - DONE
  to: OPEN
  trigger: Reopen
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
