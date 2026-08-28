# Case: artifact-kinds-valid

**Verifies:** every artifact kind of the product model is accepted when it satisfies its contract, and a model containing all ten, wired into a complete graph, validates with no diagnostics at all.

**Spec references:**

- [Artifacts](../../../spec/artifacts.md) - the frontmatter contract, required body sections and lifecycle of each kind.
- [Frontmatter reference](../../../spec/frontmatter-reference.md) - the exhaustive per-kind field tables.
- [Relationships](../../../spec/relationships.md) - the edges this fixture authors, and reachability.
- [Specification index → Canonical authority](../../../spec/index.md#canonical-authority) - model subdirectories are non-normative and kinds come from frontmatter.

## Why this case exists

Every other published case selects the kinds it needs to make its point. This case keeps one minimal positive example of every kind together so an implementation cannot reject a less common kind while still passing the published suite.

## Fixture

`repo/` carries one artifact of each of the ten kinds, plus additional Domain Terms used to exercise term dependencies, established by an archived `CHG-INITIAL`:

| Kind | Artifact |
| --- | --- |
| Actor | `ACT-IMPLEMENTER` |
| Journey | `JRN-CLAIM-CONFORMANCE` |
| Use Case | `UC-EVALUATE-001` |
| Business Rule | `BR-EXPECTATIONS-ARE-FIXED` |
| Bounded Context | `BC-CONFORMANCE` |
| Domain Term | `TERM-FIXTURE`, `TERM-VERDICT`, `TERM-RULE`, `TERM-BASE`, `TERM-REQUIREMENT`, `TERM-QUALITY`, `TERM-CONSTRAINT` |
| Functional Requirement | `FR-EVALUATE-001` |
| Quality Requirement | `QR-DETERMINISM-001` |
| Constraint | `CON-PLAIN-FILES-001` |
| Structured Behaviour | `SB-REPORT-SPEC-REVISION` |

The graph is complete on purpose, not decorative. The journey carries the use case in `steps`, so the use case is not orphaned (`PRODUCT102`). The use case declares `bounded-context` and `governed-by`, so the bounded context owns language (`PRODUCT107`) and the rule has a consumer (`PRODUCT105`). The Structured Behaviour illustrates the Use Case, Business Rule and Constraint, and is referenced alongside an inline scenario by the Functional Requirement. Every requirement, including the Quality Requirement and the Constraint, reaches the actor through the use case, so none is unreachable (`PRODUCT103`).

The fixture includes the seven permitted semantic `uses-terms` source kinds. The Use Case, Business Rule, Domain Term, Functional Requirement, Quality Requirement, Constraint and Structured Behaviour each author a resolving edge to a term that no other source uses; every referenced term therefore has a valid incoming use and no `PRODUCT106` warning applies.

No citations and no consumer documents: there is nothing here to pin, so this case never needs a digest repinned when its artifacts are edited.

The fixture deliberately uses descriptive nested directories such as `model/domain/terms/` and `model/requirements/quality/`. Those paths carry no artifact-kind semantics: the validator discovers each kind from frontmatter `type`.

## Expected

`expected.json` asserts zero diagnostics. Every kind validates, every reference resolves, and no graph warning applies.

## Note on the reference implementation

This fixture follows the current specification. A reference implementation that has not yet implemented [RFC 0022](../../../rfcs/0022-criteria-in-verification-list.md) and [RFC 0084](../../../rfcs/0084-explicit-behaviour-semantics.md) may fail it for obsolete Requirement body-section rules, the new artifact kind or the expanded verification union. Those are implementation gaps, not fixture exemptions.
