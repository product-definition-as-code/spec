---
id: CON-PLAIN-FILES-001
type: constraint
title: A fixture is plain files and nothing else
status: active
applies-to:
  - UC-EVALUATE-001
---

## Constraint

A fixture MUST consist of plain files carrying no dependency on a runtime, a package manager, a build step or a network service. Anything an implementation needs in order to read a fixture beyond a filesystem is outside what a fixture may assume.

## Rationale

A fixture that runs only where its author's tooling is installed measures that tooling as much as it measures the implementation. Keeping fixtures to plain files is what lets an implementation in any language make the same claim about the same material.

## Consequences

Cases that need more than files, such as a specific invocation and an expected exit code, cannot be expressed until the case format is extended to carry that. Such a case is declared and left unwritten rather than approximated with files that assert less than the case intends.
