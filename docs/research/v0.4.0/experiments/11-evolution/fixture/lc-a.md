---
id: LC-A
type: domain-lifecycle
title: Draft booking lifecycle
status: draft
subject: TERM-A
states:
- id: REQUESTED
  title: Requested
  initial: true
- id: CONFIRMED
  title: Confirmed
- id: CANCELLED
  title: Cancelled
  terminal: true
- id: EXPIRED
  title: Expired
  terminal: true
transitions:
- id: CONFIRM
  title: Confirm
  from:
  - REQUESTED
  to: CONFIRMED
  trigger: The actor requests confirm
  initiated-by:
  - ACT-A
  governed-by:
  - BR-A
  realized-by:
  - UC-A
- id: CANCEL
  title: Cancel
  from:
  - CONFIRMED
  to: CANCELLED
  trigger: The actor requests cancel
  initiated-by:
  - ACT-A
  governed-by:
  - BR-A
  realized-by:
  - UC-A
- id: EXPIRE
  title: Expire
  from:
  - CONFIRMED
  to: EXPIRED
  trigger: The actor requests expire
  initiated-by:
  - ACT-A
  governed-by:
  - BR-A
  realized-by:
  - UC-A
---

## Purpose

Research-only confirmation, cancellation and expiry.

## Invariants

Capacity is positive. Used slots lie between zero and capacity. A confirmed booking implies at least its room-slot footprint is used.

## State Semantics

REQUESTED holds no slot; CONFIRMED holds one; CANCELLED and EXPIRED release it and are terminal.

## Transition Semantics

CONFIRM checks the rule and consumes the footprint defined by TERM-A. CANCEL and EXPIRE each require CONFIRMED and release that footprint. Actor identity and capacity are unchanged. The two release operations cannot both apply to the same booking.

## Boundaries

Atomic single-booking transitions; no concurrent transactions, clock, real identity provider or deployed implementation.
