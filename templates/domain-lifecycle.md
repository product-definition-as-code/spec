---
id: LC-EXAMPLE-001
type: domain-lifecycle
title: Room booking lifecycle
status: draft
subject: TERM-EXAMPLE-001
states:
  - id: REQUESTED
    title: Requested
    initial: true
  - id: CONFIRMED
    title: Confirmed
    terminal: true
transitions:
  - id: CONFIRM
    title: Confirm the booking
    from: [REQUESTED]
    to: CONFIRMED
    trigger: The member confirms an available room
    initiated-by: [ACT-EXAMPLE-001]
    governed-by: [BR-EXAMPLE-001]
    realized-by: [UC-EXAMPLE-001]
---

## Purpose

Explain when a room request becomes a binding booking.

## Invariants

A confirmed booking holds the room for the member.

## State Semantics

A request does not reserve capacity; confirmation does.

## Transition Semantics

Confirmation is permitted only while the room remains available and the booking lead time permits it.

## Boundaries

Cancellation is outside this example's scope.
