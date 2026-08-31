---
id: QR-EXAMPLE-001
type: quality-requirement
title: Availability answers feel immediate
status: draft
quality-attribute: responsiveness
applies-to:
  - UC-EXAMPLE-001
verification:
  - scenario: Under the agreed reference load, availability for a chosen time is shown within one second for at least 95 percent of requests.
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Quality Requirement: a measurable quality obligation. quality-attribute names
the quality (responsiveness, portability, determinism, ...). applies-to names
the journeys, use cases or bounded contexts it binds. The Measurement section
must state how conformance is measured; "should be fast" does not qualify.
verification uses the same inline-or-reference union as a Functional Requirement.
Contract: spec/artifacts.md (Quality Requirement). Fields: spec/frontmatter-reference.md.
-->

## Requirement

Checking a time's availability MUST feel immediate to the member while they compare rooms.

## Measurement

Measured over one week of production traffic: the time from the availability request to the rendered answer, reported as the 95th percentile against the one second bound.
