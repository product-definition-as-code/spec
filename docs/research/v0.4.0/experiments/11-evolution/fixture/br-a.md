---
id: BR-A
type: business-rule
title: Draft capacity and lead-time rule
status: draft
uses-terms:
- TERM-A
---

## Rule

A requested booking can be confirmed only if remaining room slots accommodate the footprint defined by TERM-A and its start is at most 60 days after creation.

## Rationale

Research-only booking-capacity example, not accepted product policy.

## Examples

Confirmation succeeds when sufficient slots remain and the start is within the declared lead-time window; otherwise it is refused.

## Exceptions

None in this draft model.
