# Conformance

## Repository conformance

A repository conforms to Product Definition as Code v0.1 when:

1. Its canonical product definition lives under a configured product root (default
   `docs/product`) with the model/changes layout defined in this specification.
2. Every product artifact satisfies the [artifact contracts](artifacts.md): valid frontmatter per
   schema, required body sections, valid lifecycle state.
3. Every ID satisfies the [identifier rules](identifiers.md) and every reference satisfies the
   [relationship vocabulary](relationships.md).
4. Structural validation of the baseline reports no errors. Warnings are permitted.
5. The baseline is the accepted product intent on the repository's canonical branch; semantic
   evolution happens only through reviewed merges, and the initial baseline enters through the same
   mechanism as every later change (a reviewed merge into an empty model).
6. Consumer documents outside `docs/product/model` MAY carry citations to canonical product text;
   a conforming tool verifies those citations per the [citation contract](citation-contract.md).

## Implementation conformance

An implementation (tooling) conforms when:

1. It validates all of the above deterministically, emitting the diagnostic codes, fields,
   ordering and exit codes defined in [Validation](validation.md).
2. It compiles the product graph exclusively from canonical files and can always rebuild every
   derived output.
3. It derives reverse relationships and never requires reciprocal authoring.
4. It computes digests with the mandated LF normalization.
5. It MUST NOT merge a proposal that fails structural validation (the CI gate); validation is full
   structural validation of the proposed tree.
6. It MUST NOT merge, auto-approve or self-merge model changes: merging is a human decision.
7. It MUST compute citation statuses deterministically per the
   [citation contract](citation-contract.md).
8. It treats warnings as non-fatal unless the repository opts into `warnings-as-errors`.

## Violation mapping

Each normative statement in this specification maps to a diagnostic in
[Validation](validation.md); the conformance fixtures under `conformance/cases/` exercise
representative violations and assert their codes. Diagnostic codes are stable and are never
renumbered or reused. A change to normative behaviour MUST update the specification, the
diagnostic table and the fixtures together.
