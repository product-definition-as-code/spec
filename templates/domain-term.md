---
id: TERM-EXAMPLE-001
type: domain-term
title: Booking
status: draft
defined-in: BC-EXAMPLE-001
synonyms:
  - reservation
---

<!--
Domain Term: shared meaning, defined where it holds. The definition must say
more than the title does. defined-in names the bounded context that owns the
term. Reference layout: docs/product/model/domain/terms/term-example-001.md (the file is named by its lowercase ID).
Contract: spec/artifacts.md (Domain Term). Fields: spec/frontmatter-reference.md.
-->

## Definition

A booking is a member's confirmed hold on one room for one continuous time span.

## Distinguish From

A request that has not been confirmed is not a booking; neither is a room's opening schedule.

## Usage

Use booking for the confirmed hold itself. A cancelled booking stays a booking in history; it does not become a request again.
