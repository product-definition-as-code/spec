---
id: SB-KEYWORD-CASE
type: structured-behaviour
title: Open a clause with a mixed-case notation keyword
status: active
illustrates:
  - CON-KEYWORD-CASE
given:
  - Given a context exists
when: An example is validated
then:
  - Givens are recorded in the order they were authored
---

## Intent

Exercise the letter-case boundary of the clause-format schema rule.

## Boundaries

The `given` entry is intentionally invalid. The `then` entry is intentionally valid and asserts nothing about the `given` entry.
