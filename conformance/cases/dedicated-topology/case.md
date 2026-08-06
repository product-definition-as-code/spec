# Case: dedicated-topology

**Verifies:** a model repository in the dedicated topology, holding the Product Definition and no software, validates with no diagnostics. An implementation MUST NOT require a co-located software tree.

**Spec references:**

- [Conformance](../../../spec/conformance.md) - Topologies; implementation conformance clause 11.
- [Terminology](../../../spec/terminology.md) - model repository.

## Fixture

`repo/` contains only the product root: an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL`. There is no source tree and no consumer document, because in this topology the software lives in another repository.

## Expected

`expected.json` asserts zero diagnostics. An implementation that requires software beside the product root, or that refuses a product root it cannot relate to a code tree, fails this case.

## What this case does not verify

A case is one directory tree, so a model repository standing alone is indistinguishable from a co-located repository whose software was left out of the fixture: the co-located cases in this corpus pass the same expectation. This case therefore proves that co-located software is not required, which is the obligation the specification places on implementations, and not that the fixture is a dedicated model repository.

Repository conformance clause 1 requires a git repository, and a runner executes fixtures in a plain working copy, so that part is verified by review rather than here. The model-repository pointer of the dedicated topology has no fixture: it needs two repository roots per case and a serialization the specification deliberately leaves open.
