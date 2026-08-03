# Case: citation-current

**Verifies:** a consumer document cites a baseline Functional Requirement; the citation status is
`current` and no `PRODUCT06x` diagnostic is produced.

**Spec references:**

- [Citation Contract](../../../spec/citation-contract.md) - citation record, `current` status.
- [Validation](../../../spec/validation.md) - `PRODUCT060`-`PRODUCT063` (none expected here).

## Fixture

`repo/` contains a minimal product model with one Functional Requirement (`FR-VALIDATE-001`) that
has one verification scenario with a stable `id` (`S1`). A consumer document
(`repo/specs/feature-x.md`) carries a citation sidecar (`repo/specs/feature-x.citations.yml`)
recording the FR's current content digest and the `S1` anchor.

## Expected

`expected.json` asserts zero diagnostics: the target resolves, the digest matches, and the anchor
exists. This is the happy path for the citation contract.
