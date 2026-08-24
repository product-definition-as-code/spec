# Case: artifact-kinds-valid

**Verifies:** every artifact kind of the product model is accepted when it satisfies its contract, and a model containing all nine, wired into a complete graph, validates with no diagnostics at all.

**Spec references:**

- [Artifacts](../../../spec/artifacts.md) - the frontmatter contract, required body sections and lifecycle of each kind.
- [Frontmatter reference](../../../spec/frontmatter-reference.md) - the exhaustive per-kind field tables.
- [Relationships](../../../spec/relationships.md) - the edges this fixture authors, and reachability.
- [Specification index → Canonical authority](../../../spec/index.md#canonical-authority) - model subdirectories are non-normative and kinds come from frontmatter.

## Why this case exists

Every other case selects the kinds it needs to make its point, and between them they only ever used Actor, Journey, Use Case, Business Rule and Functional Requirement. Quality Requirement, Constraint, Domain Term and Bounded Context appeared nowhere. An implementation could reject all four and still pass all the conformance tests while claiming conformance.

## Fixture

`repo/` carries one artifact of each of the nine kinds, established by an archived `CHG-INITIAL`:

| Kind | Artifact |
| --- | --- |
| Actor | `ACT-IMPLEMENTER` |
| Journey | `JRN-CLAIM-CONFORMANCE` |
| Use Case | `UC-EVALUATE-001` |
| Business Rule | `BR-EXPECTATIONS-ARE-FIXED` |
| Bounded Context | `BC-CONFORMANCE` |
| Domain Term | `TERM-FIXTURE` |
| Functional Requirement | `FR-EVALUATE-001` |
| Quality Requirement | `QR-DETERMINISM-001` |
| Constraint | `CON-PLAIN-FILES-001` |

The graph is complete on purpose, not decorative. The journey carries the use case in `steps`, so the use case is not orphaned (`PRODUCT102`). The use case declares `bounded-context`, `governed-by` and `uses-terms`, so the bounded context owns language (`PRODUCT107`), the rule has a consumer (`PRODUCT105`) and the term has usage (`PRODUCT106`). Every requirement, including the Quality Requirement and the Constraint, reaches the actor through the use case, so none is unreachable (`PRODUCT103`). Those four warnings are what a fixture holding the four missing kinds and nothing else produces, and a case that expected them would be asserting its own incompleteness.

No citations and no consumer documents: there is nothing here to pin, so this case never needs a digest repinned when its artifacts are edited.

The fixture deliberately uses descriptive nested directories such as `model/domain/terms/` and `model/requirements/quality/`. Those paths carry no artifact-kind semantics: the validator discovers each kind from frontmatter `type`.

## Expected

`expected.json` asserts zero diagnostics. Every kind validates, every reference resolves, and no graph warning applies.

## Note on the reference implementation

This case currently fails ProductShape, with `PRODUCT009` against the Functional Requirement and the Quality Requirement, because ProductShape still requires the `## Acceptance Scenarios` and `## Verification` body sections that [RFC 0022](../../../rfcs/0022-criteria-in-verification-list.md) removed from the required sets. The fixture is correct against the specification as it stands; the implementation has not caught up. Every other conformance test reports the same finding for the same reason.
