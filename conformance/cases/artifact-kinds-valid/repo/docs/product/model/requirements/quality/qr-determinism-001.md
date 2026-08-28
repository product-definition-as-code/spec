---
id: QR-DETERMINISM-001
type: quality-requirement
title: Produce the same verdict for the same fixture
status: active
quality-attribute: determinism
applies-to:
  - UC-EVALUATE-001
verification:
  - id: S1
    scenario: The same fixture evaluated twice in one environment produces the same verdict and the same diagnostics in the same order.
  - id: S2
    scenario: The same fixture evaluated on a Windows checkout and on a Linux checkout produces the same verdict.
uses-terms:
  - TERM-QUALITY
---

## Requirement

A conformance verdict MUST depend only on the fixture and the expectations it carries. The same fixture MUST produce the same verdict on every run, on every operating system, and regardless of the order in which cases were evaluated.

## Measurement

Conformance is measured by evaluating every case twice on at least two operating systems and comparing the verdicts and the emitted diagnostics, including their order, byte for byte. Any difference is a failure of this requirement, whatever the cause.
