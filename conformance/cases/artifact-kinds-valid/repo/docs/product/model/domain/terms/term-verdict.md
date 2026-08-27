---
id: TERM-VERDICT
type: domain-term
title: Verdict
status: active
defined-in: BC-CONFORMANCE
---

## Definition

The single conclusion an evaluation reaches about one case: the case passed, the case failed, or the case could not be run. A verdict is inseparable from the case it is about and the revision it was measured at.

## Distinguish From

A verdict is not a diagnostic. A diagnostic is what an implementation emits about a model; a verdict is what the evaluation concludes about the implementation after comparing the diagnostics emitted with the ones the case expects. One verdict may rest on many diagnostics, or on none.

## Usage

Used when reporting the outcome of one case. A reader who says "the verdict changed" means the conclusion moved, which is a different statement from "the implementation changed".
