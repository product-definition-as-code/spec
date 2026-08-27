---
id: CON-KEYWORD-CASE
type: constraint
title: Reject notation keywords in any letter case
status: active
---

## Constraint

Canonical behaviour clauses MUST NOT open with a notation keyword, whatever letter case it is written in.

## Rationale

Authors transcribing an existing scenario write `Given`, not `GIVEN`, so a rule that catches only the upper-case spelling misses the mistake it exists to prevent.

## Consequences

A clause opening with `Given` is rejected. A clause opening with a longer word that merely begins with those letters is not.
