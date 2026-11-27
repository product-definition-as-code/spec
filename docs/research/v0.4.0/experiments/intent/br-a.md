---
id: BR-A
type: business-rule
title: Draft capacity and lead-time rule
status: draft
uses-terms:
- TERM-A
---

## Rule

A requested booking can be confirmed only if used room slots are below capacity and its start is at most 60 days after creation.

## Rationale

Research-only booking-capacity example, not accepted product policy.

## Examples

With capacity 1, used slots 0 and lead time 30 days, confirmation consumes one slot. With used slots 1, confirmation is refused.

## Exceptions

None in this draft model.
