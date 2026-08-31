---
id: UC-EXAMPLE-001
type: use-case
title: Book a room
status: draft
primary-actor: ACT-EXAMPLE-001
bounded-context: BC-EXAMPLE-001
governed-by:
  - BR-EXAMPLE-001
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Use Case: one concrete interaction through which an actor obtains a product
outcome. The body describes observable behaviour, not implementation design.
Optional frontmatter: supporting-actors, bounded-context, governed-by, uses-terms.
Contract: spec/artifacts.md (Use Case). Fields: spec/frontmatter-reference.md.
-->

## Goal

The member holds a confirmed booking for a specific room and time.

## Trigger

The member requests a room for a chosen time.

## Preconditions

The member is entitled to book rooms in their organisation.

## Main Flow

1. The member picks a time and sees which rooms are free.
2. The member picks a room and confirms.
3. The booking is recorded and the member receives the confirmation.

## Alternative Flows

- The preferred room is taken: the member picks another free room at the same time.

## Failure Conditions

- The requested start lies beyond the booking lead time (BR-EXAMPLE-001): the booking is rejected with the reason.

## Postconditions

The room is held for the member; the time no longer appears as free to others.
