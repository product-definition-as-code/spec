---
id: SB-REPORT-SPEC-REVISION
type: structured-behaviour
title: Report the specification revision measured by a verdict
status: active
illustrates:
  - UC-EVALUATE-001
  - BR-EXPECTATIONS-ARE-FIXED
  - CON-PLAIN-FILES-001
given:
  - The conformance cases were read from a named specification revision
when: The implementer requests a conformance verdict
then:
  - The report identifies that exact specification revision
uses-terms:
  - TERM-FIXTURE
---

## Intent

Make every conformance verdict attributable to the exact accepted case definitions it measured.

## Boundaries

This example does not prescribe how the revision is rendered in a human-readable or machine-readable report.
