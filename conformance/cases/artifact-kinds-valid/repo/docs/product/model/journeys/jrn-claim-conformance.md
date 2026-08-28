---
id: JRN-CLAIM-CONFORMANCE
type: journey
title: Claim conformance for an implementation
status: active
primary-actor: ACT-IMPLEMENTER
steps:
  - use-case: UC-EVALUATE-001
uses-terms:
  - TERM-JOURNEY
---

## Intended Outcome

The implementer holds a verdict about their tool that someone else can reproduce from the same fixtures.

## Entry Conditions

A tool exists and can be invoked, and the fixtures are available at a named revision.

## Journey Narrative

The implementer obtains the fixtures, evaluates the tool against them, and reads the verdict. A verdict of conformance is attributable to the revision it was measured at. A verdict of failure names the cases that failed and what each expected, which the implementer takes back into the tool.

## Variants and Branches

A case the tool cannot run at all is reported as unrun rather than passed, and the implementer decides whether to treat it as a gap in the tool or a gap in the case format. An implementer who believes a case is wrong contests it rather than editing it locally.

## Completion Conditions

Every case has a verdict, and no case has been silently skipped.
