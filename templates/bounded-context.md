---
id: BC-EXAMPLE-001
type: bounded-context
title: Scheduling
status: draft
---

<!--
Bounded Context: a product-language boundary, delimiting where a set of domain
terms carries a specific meaning. It implies nothing about modules or code
structure. Term ownership is derived from each Domain Term's defined-in; do not
author owns-terms here.
Contract: spec/artifacts.md (Bounded Context). Fields: spec/frontmatter-reference.md.
-->

## Responsibility

Scheduling answers who holds which room at which time, and keeps overlapping holds impossible.

## Language

Booking, room, time span, lead time. Within Scheduling, availability always means bookable time, not physical readiness.

## Boundaries

Scheduling ends where payment, room maintenance and building access begin.

## External Relationships

Scheduling learns which rooms exist from facility management, and reports usage to it.
