# Conformance

## Repository conformance

A repository conforms to Product Definition as Code v0.1 when:

1. Its canonical product definition lives under a configured product root (default `docs/product`) with the model/changes layout defined in this specification.
2. Every product artifact satisfies the [artifact contracts](artifacts.md): valid frontmatter per schema, required body sections, valid lifecycle state.
3. Every ID satisfies the [identifier rules](identifiers.md) and every reference satisfies the [relationship vocabulary](relationships.md).
4. Structural validation of the baseline reports no errors. Warnings are permitted.
5. The Product Definition is the accepted product intent on the repository's canonical branch; semantic evolution happens only through [Product Changes](product-changes.md), applied by an explicit human-triggered apply and accepted by a reviewed merge. The first Product Definition enters through `CHG-INITIAL`, the same mechanism as every later change.
6. Every live Product Change satisfies the change contract: valid `change.md` frontmatter per schema, required body sections, operations consistent with `proposed/`, and an overlay that validates without errors.
7. Consumer documents outside `docs/product/model` MAY carry citations to canonical product text; a conforming tool verifies those citations per the [citation contract](citation-contract.md).

## Implementation conformance

An implementation (tooling) conforms when:

1. It validates all of the above deterministically, emitting the diagnostic codes, fields, ordering and exit codes defined in [Validation](validation.md).
2. It compiles the product graph exclusively from canonical files and can always rebuild every derived output.
3. It derives reverse relationships and never requires reciprocal authoring.
4. It computes digests with the mandated LF normalization.
5. It validates a Product Change by compiling and validating its overlay, without modifying any baseline file.
6. It applies a Product Change only under the rules in [Product Changes → Apply](product-changes.md#apply): approved status (`PRODUCT028` otherwise), revalidated overlay, baseline-revision compatibility, computed and reported product diff, `--dry-run` support, never implicitly, never committing. It MUST NOT treat a successful apply as acceptance.
7. It MUST NOT merge a proposal that fails structural validation (the CI gate); validation of a proposed tree is full structural validation.
8. It MUST NOT merge, auto-approve or self-merge model changes: merging is a human decision.
9. It MUST compute citation statuses deterministically per the [citation contract](citation-contract.md).
10. It treats warnings as non-fatal unless the repository opts into `warnings-as-errors`.

## Violation mapping

Each normative statement in this specification maps to a diagnostic in [Validation](validation.md); the conformance fixtures under `conformance/cases/` exercise representative violations and assert their codes. Diagnostic codes are stable and are never renumbered or reused. A change to normative behaviour MUST update the specification, the diagnostic table and the fixtures together.
