---
id: JRN-EXAMPLE-001
type: journey
title: Reserve a room for a recurring meeting
status: draft
primary-actor: ACT-EXAMPLE-001
steps:
  - use-case: UC-EXAMPLE-001
---

<!--
Journey: an end-to-end outcome pursued by an actor. It may cross use cases,
channels, bounded contexts, waiting periods, branches and failure paths.
steps: the main ordered path only, one `- use-case:` entry per step; branches
and exceptional paths belong in the body. No screen-by-screen UI behaviour.
Reference layout: docs/product/model/journeys/jrn-example-001.md (the file is named by its lowercase ID).
Contract: spec/artifacts.md (Journey). Fields: spec/frontmatter-reference.md.
-->

## Intended Outcome

The member's team meets in a suitable room every week without rebooking by hand.

## Entry Conditions

The member belongs to an organisation with bookable rooms.

## Journey Narrative

The member finds a room that fits the team, books it for the first occurrence, and repeats the booking for the series. When a conflict appears later in the series, the member resolves it by moving that occurrence.

## Variants and Branches

- No room fits the whole series: the member books the largest available room and splits the remainder.
- A booked room is withdrawn from service: the affected occurrences need rebooking.

## Completion Conditions

Every occurrence of the series holds a confirmed booking.
