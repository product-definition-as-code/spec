---
id: BR-EXAMPLE-001
type: business-rule
title: Booking lead time
status: draft
applies-to:
  - UC-EXAMPLE-001
uses-terms:
  - TERM-EXAMPLE-001
---

<!--
Business Rule: durable product knowledge that governs behaviour. A rule used by
several use cases or requirements is defined once, here, and referenced by ID,
never restated inside stories, acceptance criteria, code or tests.
The Rule section holds exactly one clear normative statement.
Reference layout: docs/product/model/business-rules/br-example-001.md (the file is named by its lowercase ID).
Contract: spec/artifacts.md (Business Rule). Fields: spec/frontmatter-reference.md.
-->

## Rule

A booking may start no more than 60 days after the day it is made.

## Rationale

Rooms booked far ahead sit idle while plans change; a bounded window keeps availability honest.

## Examples

A booking made on March 1 may start on any day up to April 30.

## Exceptions

None.
