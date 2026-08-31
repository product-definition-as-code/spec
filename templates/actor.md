---
id: ACT-EXAMPLE-001
type: actor
title: Member
status: draft
actor-kind: human
---

<!--
Actor: who or what interacts with the product to achieve a meaningful outcome.
Actors are not personas: no demographics, no fictional detail.
actor-kind: human | external-system | scheduled-process | product.
Contract: spec/artifacts.md (Actor). Fields: spec/frontmatter-reference.md.
Copy this file, replace the id (immutable once accepted), fill the sections,
and keep them in this order. More sections may follow the required ones.
-->

## Purpose

A member books shared meeting rooms for their team.

## Goals

- Find a free room that fits the meeting.
- Hold the room with confidence that nobody else gets it.

## Responsibilities

- Provides the meeting time, expected attendance and any equipment needs.
- Cancels bookings that are no longer needed.

## Boundaries

A member manages only their own bookings. Approving exceptional requests is outside this actor's reach.
