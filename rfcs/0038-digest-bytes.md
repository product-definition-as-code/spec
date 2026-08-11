# RFC 0038: A content digest hashes bytes, never decoded text

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-11
- **Related:** #28 (digest granularity under an anchor), a different question about the same field
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/32>

## Problem

[Validation → Digests](../spec/validation.md#digests) defines a content digest as SHA-256 "over the artifact's UTF-8 bytes with CRLF and CR line endings normalized to LF". Two readings of "UTF-8 bytes" are defensible from that text: hashing the file's bytes as they are, and hashing the UTF-8 re-encoding of the file's decoded text. The two implementations initially took different ones (pdac-lint hashed bytes; ProductShape hashed decoded text until [juangcarmona/productshape#74](https://github.com/juangcarmona/productshape/pull/74)).

For well-formed UTF-8 the readings agree, because decoding and re-encoding is a round trip. They diverge on any input that is not well-formed UTF-8: a decoder replaces each invalid sequence with U+FFFD, which re-encodes as `EF BF BD`, so the decoded-text reading hashes bytes that were never in the file. A stripped byte order mark diverges the same way. Two implementations then compute different digests for the same artifact, and a citation that is `current` under one is `stale` under the other. The digest is the primitive the citation contract rests on; a disagreement here makes conformance claims incomparable, which is the thing the conformance tests exist to prevent. Nothing distinguishes the readings today: every fixture is well-formed UTF-8, so both readings pass every case.

## Proposal

Amend [Validation → Digests](../spec/validation.md#digests) to fix the byte reading in so many words:

> Content digests are SHA-256 over the artifact's raw bytes, with CRLF and CR byte sequences normalized to LF, rendered as `sha256:<lowercase hex>`. The input to the hash is bytes, never decoded text: an implementation MUST NOT decode content before hashing, MUST NOT strip a byte order mark, and MUST hash a byte sequence that is not well-formed UTF-8 exactly as it appears in the file. This normalization is mandatory: digests MUST be identical across operating systems and Git line-ending configurations. Citation digests use the same normalization (see the [Citation Contract](citation-contract.md)).

Bytes is the right reading because it needs no decoder, cannot be perturbed by one, and keeps the digest a pure function of repository content.

## Impact

- **On existing conformant repositories:** none. For well-formed UTF-8, which is every artifact in every known repository, the two readings produce identical digests.
- **On existing implementations:** none changes behaviour. pdac-lint has hashed bytes from the start (`digestBytes`); ProductShape moved to bytes in [juangcarmona/productshape#74](https://github.com/juangcarmona/productshape/pull/74); the shared test vectors from [pdac-lint#8](https://github.com/product-definition-as-code/pdac-lint/pull/8) already pin the byte reading across both.
- **On the conformance tests:** a distinguishing fixture should be added, an artifact containing a byte sequence that is not well-formed UTF-8 with its digest pinned, so an implementation that decodes before hashing fails a case instead of agreeing by coincidence. It arrives as a follow-up to the spec change that lands this determination.

## Alternatives considered

**Hash the decoded text under a fixed decoding policy** (replacement characters, BOM handling, error mode). Rejected: it requires every implementation to reproduce one decoder's error handling bit for bit, it hashes bytes that are not in the file, and it adds a dependency (the decoder) to the one primitive whose whole value is implementation independence.

**Leave the text as it is.** Rejected: both readings pass the current tests, so the divergence stays invisible exactly until an adopter hits it, and then it presents as one tool calling a citation `current` while another calls it `stale` with no visible cause.

This RFC is a determination in the sense of [CONTRIBUTING.md](../CONTRIBUTING.md): it fills a gap the specification left open, and no conforming repository or implementation changes behaviour. The comment window is 72 hours.
