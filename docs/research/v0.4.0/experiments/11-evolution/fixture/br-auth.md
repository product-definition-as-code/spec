---
id: BR-AUTH
type: business-rule
title: Draft trusted issuer authorization
status: draft
uses-terms: [TERM-IDENTITY]
---

## Rule

Accept an authentic editor credential exactly when its issuer is trusted as defined by TERM-IDENTITY.

## Rationale

Research-only external identity boundary.

## Examples

An authentic editor credential from issuer A is accepted initially.

## Exceptions

Credential authenticity is assumed, not cryptographically verified here.
