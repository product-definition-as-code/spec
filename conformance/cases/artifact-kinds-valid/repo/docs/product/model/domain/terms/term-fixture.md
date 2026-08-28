---
id: TERM-FIXTURE
type: domain-term
title: Fixture
status: active
defined-in: BC-CONFORMANCE
synonyms:
  - case repository
uses-terms:
  - TERM-BASE
---

## Definition

The files a conformance case is measured against: a self-contained repository whose content is the input of exactly one claim, paired with the diagnostics that claim expects.

## Distinguish From

A fixture is not a test. A test decides an outcome; a fixture is the material an outcome is decided about, and the same fixture serves every implementation that makes the claim.

## Usage

Used when naming the input of a case. A reader who says "the fixture changed" means the material moved, which is a different statement from "the expectation changed".
