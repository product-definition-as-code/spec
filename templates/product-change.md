---
id: CHG-EXAMPLE-001
type: product-change
title: Introduce the booking lead time
status: draft
base-revision: a1b2c3d
operations:
  add:
    - BR-EXAMPLE-001
  modify: []
  remove: []
---

<!--
Product Change: an explicit, validated delta against the accepted definition.
It records semantic intent; a pull request is only its review boundary, and
apply never accepts anything by itself.
base-revision: the commit of the baseline the change was written against
(CHG-INITIAL with no baseline commit uses the 0000000 sentinel).
operations: every added or modified ID needs a complete proposed future-state
artifact under this change's proposed/ directory.
Open Questions is syntactic: a list item counts as unresolved whatever it says;
resolve a question by removing its item. "None." in prose is resolved.
Reference layout: docs/product/changes/active/chg-example-001/change.md.
Contract: spec/product-changes.md. Fields: spec/frontmatter-reference.md.
-->

## Problem

Members book rooms months ahead and abandon them, so free rooms show as taken and trust in availability erodes.

## Intended Product Outcome

A booking may start no more than 60 days after the day it is made, and members are told the earliest permitted start when a request exceeds it.

## Rationale

A bounded window keeps availability honest with the least ceremony; exceptions can come later as their own change if evidence demands them.

## Affected Product Areas

Scheduling (BC-EXAMPLE-001): booking creation (UC-EXAMPLE-001) gains a governing rule.

## Open Questions

None.

## Product Acceptance

The rule reads as intended to the product owner, and the booking use case names it as a failure condition.

## Out of Scope

Enforcement in delivery, migration of existing far-future bookings, and any exception mechanism.
