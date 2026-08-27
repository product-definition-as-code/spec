---
id: UC-EVALUATE-001
type: use-case
title: Evaluate an implementation against the fixtures
status: active
primary-actor: ACT-IMPLEMENTER
bounded-context: BC-CONFORMANCE
governed-by:
  - BR-EXPECTATIONS-ARE-FIXED
---

## Goal

Obtain a verdict for an implementation against every case, with the evidence for each verdict.

## Trigger

The implementer asks for a verdict, at a named revision of the fixtures.

## Preconditions

The fixtures are readable, and the implementation under test can be invoked.

## Main Flow

The fixtures are read in a stable order. Each case is evaluated against the implementation. The diagnostics the implementation emits are compared with the ones the case expects. Each case receives exactly one verdict, and the verdicts are reported together with the revision they were measured at.

## Alternative Flows

A case whose format this evaluation cannot execute is reported as unrun, with the reason, and counts as evidence of nothing.

## Failure Conditions

The fixtures cannot be read, or the implementation cannot be invoked at all. Neither produces a verdict, because a verdict nobody can attribute is worse than none.

## Postconditions

Every case is either verdicted or reported unrun, and the fixtures are unchanged by having been evaluated.
