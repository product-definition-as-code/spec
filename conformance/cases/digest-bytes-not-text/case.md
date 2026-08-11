# Case: digest-bytes-not-text

**Verifies:** a content digest is computed over the artifact's raw bytes, never over decoded text. The cited Functional Requirement contains a byte sequence that is not well-formed UTF-8 (`C3 28`); the ledger pins the digest of those exact bytes; the citation status is `current` and no diagnostic is produced.

**Spec references:**

- [Validation → Digests](../../../spec/validation.md#digests) - bytes, never decoded text ([RFC 0038](../../../rfcs/0038-digest-bytes.md)).
- [Citation Contract](../../../spec/citation-contract.md) - citation record, `current` status.

## Fixture

`repo/` is the citation-current model (Actor, Journey, Use Case, Functional Requirement, archived `CHG-INITIAL`), with one difference: the Functional Requirement's body carries a byte sequence that no UTF-8 decoder accepts. The consumer sidecar (`repo/specs/feature-x.citations.yml`) pins the digest of the file's raw bytes, CRLF and CR normalized to LF at byte level.

## Expected

`expected.json` asserts zero diagnostics. An implementation that hashes the raw bytes recomputes the pinned digest and reports `current`. An implementation that decodes before hashing replaces the invalid sequence with U+FFFD, computes a different digest, reports the citation `stale`, and fails this case with an unexpected `PRODUCT061`. The two readings of the digest rule agree on every well-formed file, so this fixture is the only thing that tells them apart.
