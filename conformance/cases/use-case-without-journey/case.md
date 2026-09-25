# Case: use-case-without-journey

**Verifies:** an active Use Case that no Journey references is conformant. The model contains no Journey at all, and an implementation MUST NOT emit any diagnostic because of that absence. This is the executable form of the retirement of `PRODUCT102`.

**Spec references:**

- [Artifacts](../../../spec/artifacts.md) - Journey; Use Case. A Use Case MAY be referenced by zero, one or multiple Journeys, and an implementation MUST NOT emit a conformance diagnostic solely because an active Use Case is not referenced by a Journey.
- [Validation](../../../spec/validation.md) - Error codes; `PRODUCT102` is retired with no replacement.
- [RFC 0112](../../../rfcs/0112-optional-use-case-journey-context.md) - Use Case journey context is optional.

## Fixture

`repo/` holds an Actor (`ACT-AUDITOR`), a Use Case (`UC-EXPORT-LOG-001`) and a Functional Requirement (`FR-EXPORT-LOG-001`), established by an archived `CHG-INITIAL`. There is no `model/journeys/` directory.

The Use Case is not a fragment left half-authored. It declares its required `primary-actor`, carries every required body section, and a Functional Requirement derives from it. The export it describes is reached directly, so no end-to-end outcome surrounds it, which is the shape the retirement exists for: a Use Case with real product content and no Journey above it.

Nothing else in the fixture can produce a warning that would obscure the result. `FR-EXPORT-LOG-001` reaches `ACT-AUDITOR` through `derived-from` and `primary-actor`, so it is reachable and no `PRODUCT103` applies. There is no Business Rule, Domain Term, Bounded Context or deprecated artifact, so `PRODUCT104`-`PRODUCT107` have empty populations. Every file is named by its lowercase ID, so no `PRODUCT101` applies. The change is archived and `applied`, so `PRODUCT108` does not apply, and no artifact is `draft`, so `PRODUCT111` does not apply.

## Expected

`expected.json` asserts zero diagnostics. An implementation that still reports an active Use Case as absent from every Journey fails this case, whichever code or severity it reports it under.

## What this case does not verify

It does not verify that Journeys are discouraged. Journey modelling stays part of the reference profile wherever it explains a genuine end-to-end outcome; this case fixes only that its absence is not a defect.

It does not constrain what an implementation may offer outside the conformance diagnostic namespace. The specification permits surfacing the absence as non-conformance advice for human review, and a runner comparing emitted diagnostics cannot see such a surface, so the boundary between advice and diagnostic is verified by review.
