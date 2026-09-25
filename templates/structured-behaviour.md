---
id: SB-EXAMPLE-001
type: structured-behaviour
title: Confirm a booking within the lead time
status: draft
illustrates:
  - UC-EXAMPLE-001
  - BR-EXAMPLE-001
given:
  - The room is free for the requested time
  - The requested start lies within the booking lead time
when: The member confirms the booking
then:
  - The booking is recorded for that room and time
  - The member receives the confirmation
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Structured Behaviour: one concrete, implementation-independent example of
accepted observable behaviour, with its own identity and digest so tests and
specs can cite exactly what they verify. Clause values must not begin with a
GIVEN, WHEN, THEN or AND keyword in any letter case; renderers add those words.
All given entries are conjunctive, all then entries are conjunctive: express an
alternative as a separate Structured Behaviour. Never name test classes, mocks
or other implementation machinery.
Reference layout: docs/product/model/behaviours/sb-example-001.md (the file is named by its lowercase ID). The directory is behaviours, not structured-behaviours.
Contract: spec/artifacts.md (Structured Behaviour). Fields: spec/frontmatter-reference.md.
-->

## Intent

Establish the accepted result of the ordinary booking confirmation, the case every variant is compared against.

## Boundaries

This example does not assert how the confirmation reaches the member, and it does not cover starts beyond the lead time.
