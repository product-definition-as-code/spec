# Case: citation-tampered-and-stale

**Verifies:** the `tampered` and the `stale` condition hold for the same citation; the status is `tampered` and the only diagnostic is `PRODUCT062`. `PRODUCT061` is not emitted.

**Spec references:**

- [Citation Contract → Precedence](../../../spec/citation-contract.md#precedence) - the evaluation order, and one diagnostic per citation.
- [Citation Contract → Embedding](../../../spec/citation-contract.md#embedding) - faithfulness is decided against the recorded digest, not against current canonical content.
- [Validation](../../../spec/validation.md) - `PRODUCT061` (not expected here), `PRODUCT062`.

## Fixture

`repo/` carries the same minimal model as `citation-current`: an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`) with one verification scenario carrying the stable `id` `S1`, established by an archived `CHG-INITIAL`.

The consumer document `repo/specs/feature-x.md` carries a marker-block citation of `FR-VALIDATE-001` recording the digest `sha256:cd567f9e119089438556095f639b896e63f638a7cf5efd50d951f2ae24ead8c4`, which is the digest of this earlier revision of the artifact, ending with a final newline:

```markdown
---
id: FR-VALIDATE-001
type: functional-requirement
title: Detect unresolved artifact references
status: active
derived-from:
  - UC-VALIDATE-001
verification:
  - id: S1
    scenario: A validation run reports an unresolved reference with code PRODUCT006.
---

## Requirement

The product SHOULD detect references to unknown artifact IDs and report them as validation errors.

## Rationale

Unresolved references break the product graph; catching them deterministically prevents silent drift between artifacts.
```

Both conditions therefore hold at once:

- **tampered**: the embedded projection reads `The product MAY detect`, so it is not the canonical text at the recorded digest. It cannot reach that digest under either reading of the block's trailing newline, so the case is decidable without settling that question.
- **stale**: the artifact in the baseline reads `The product MUST detect` and hashes to `sha256:cb93b565e529ada665c37f3c962ed50221bb6cade065fa332a4aa9ee148a4970`, so the target's recomputed digest differs from the recorded one.

The recorded digest is deliberately the digest of text that is not in the fixture: the canonical artifact reads `MUST` and the projection reads `MAY`, so no file under `repo/` hashes to it. It is the canonical artifact with `MUST` replaced by `SHOULD`, so a runner verifying pinned digests ([issue #10](https://github.com/product-definition-as-code/spec/issues/10)) can reproduce it from the fixture rather than trusting it.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT062` as an error at line 5 of `specs/feature-x.md`, with `target` `FR-VALIDATE-001`. The absence of `PRODUCT061` is the other half of the assertion: an implementation that gates its tamper check on the target still matching the recorded digest reports this citation as `stale` and fails this case, which is the failure mode reported in [issue #17](https://github.com/product-definition-as-code/spec/issues/17).
