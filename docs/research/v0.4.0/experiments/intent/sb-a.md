---
id: SB-A
type: structured-behaviour
title: Draft ordinary confirmation
status: draft
illustrates:
- UC-A
- BR-A
when: The member confirms
then:
- The state is CONFIRMED and used slots are 1
covers-transition:
  lifecycle: LC-A
  transition: CONFIRM
given:
- Capacity is 1, used slots are 0 and the state is REQUESTED
- Lead time is 30 whole days
---

## Intent

Concrete positive confirmation example; not exhaustive behaviour.

## Boundaries

Does not cover full capacity, cancellation, expiry or boundary day 60.
