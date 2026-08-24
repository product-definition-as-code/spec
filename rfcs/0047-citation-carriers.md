# RFC 0047: One citation payload, any comment

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-19
- **Accepted:** 2026-08-24
- **Class:** change
- **Target:** PDaC v0.2.0
- **PR:** <https://github.com/product-definition-as-code/spec/pull/49>
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/47>
- **Depends on:** [RFC 0077](0077-whole-artifact-digests-for-anchored-citations.md)
- **Supersedes:** [RFC 0004](0004-delivery-model-reset.md) open question 1, in part

## Problem

The [Citation Contract](../spec/citation-contract.md) names an inline reference, a Markdown marker block and a YAML sidecar while mandating none of their serializations. The conformance fixtures nevertheless require a marker and a sidecar. A second implementation cannot discover those citations, write an interoperable citation, or attribute its location from normative text alone.

The reference implementation exposes the missing decisions rather than resolving them: an inline brace syntax exists only in its source, its parser accepts two sidecar shapes, and its writer must choose shapes the specification does not name. The initial RFC draft proposed a token and a mapping sidecar but still left writer-critical behavior open: attribute order and escaping, duplicate and unknown attributes, malformed payload handling, YAML document count, entry ordinals, missing consumer files and what happens when payloads and a sidecar coexist.

[RFC 0077](0077-whole-artifact-digests-for-anchored-citations.md) separately fixes digest scope: every citation digest covers the whole target artifact, including when `anchor` is present. This RFC fixes only how the citation record is carried and written.

## Proposal

### Two carriers, one record

A conforming consumer document uses exactly one citation carrier:

1. one or more carrier-independent comment payloads in the consumer document; or
2. one adjacent YAML sidecar ledger.

The carriers serialize the same citation record (`id`, `digest`, optional `anchor`) and use the same whole-artifact digest semantics. A consumer MUST NOT combine payload citations with a sidecar ledger. Keeping the carrier choice exclusive prevents the same dependency from being counted twice by one implementation and once by another.

### Payload grammar

A citation payload occupies one physical line and has this grammar, where `SP` is one or more ASCII space or tab characters:

```text
pdac:cite SP id="<artifact-id>" SP digest="<digest>" [SP anchor="<anchor>"]
```

The attributes MUST appear in that order. Values use no escape syntax and MUST NOT contain a quote, backslash, carriage return or line feed. `id`, `digest` and `anchor` retain their normative patterns and semantics. Attributes are neither optional beyond `anchor` nor extensible in this version: an unknown, repeated or out-of-order attribute is malformed rather than silently ignored.

The payload is carried inside the host format's native comment. The comment opener, closer and any whitespace outside the payload are not part of the citation. Examples:

```text
<!-- pdac:cite id="FR-VALIDATE-001" digest="sha256:..." anchor="S1" -->
# pdac:cite id="FR-VALIDATE-001" digest="sha256:..." anchor="S1"
// pdac:cite id="FR-VALIDATE-001" digest="sha256:..." anchor="S1"
```

Discovery scans text lines for the exact `pdac:cite` token and parses the grammar from that token through the closing quote of the final attribute. A token that is followed by payload-like text but does not parse is a malformed citation; it MUST NOT be silently treated as ordinary prose. A bare mention of the token with no `id=` payload, such as documentation describing `` `pdac:cite` ``, is not a citation candidate.

This rule is carrier-independent: implementations do not need a registry of programming-language comment syntaxes. Authors remain responsible for placing the payload in a comment so it does not change the consumer format's behavior.

### Embedded projections

An embedded projection begins with a valid payload line and ends with a line containing the exact token `/pdac:cite` inside the same host comment style. The bytes between the line ending after the opening marker and the line beginning the closing marker are the embedded projection.

[RFC 0077](0077-whole-artifact-digests-for-anchored-citations.md) applies: the digest covers the whole target artifact. Therefore an anchored embedded projection MUST contain the whole artifact, even though the anchor identifies the scenario relied on. A projection containing only that scenario cannot be verified against the citation digest and is `PRODUCT062`.

### YAML sidecar ledger

For a consumer named `<stem>.<extension>`, the sidecar is the adjacent file `<stem>.citations.yml`; only the final extension is replaced. For example, `api.v2.md` uses `api.v2.citations.yml`. For a consumer with no extension, `.citations.yml` is appended.

The sidecar MUST be a single YAML 1.2 document with exactly one top-level key, `citations`. Its value MUST be a non-empty sequence. Each entry MUST be a mapping with exactly `id`, `digest` and optional `anchor`, and MUST satisfy the citation-record patterns. Duplicate YAML keys, aliases, anchors, tags and merge keys are not permitted.

```yaml
citations:
  - id: FR-VALIDATE-001
    digest: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    anchor: S1
```

The sidecar's corresponding consumer file MUST exist. A **ledger entry** is its one-based position in the `citations` sequence across the single document. Verification and impact output identify a sidecar citation by the ledger path and entry number.

The former bare-sequence sidecar is retired. A reader MAY accept it as an explicitly non-conforming compatibility extension, but conformance results and the canonical writer MUST use the mapping form above.

### Canonical writer

A conforming citation writer MUST emit only the two forms above.

For a payload it MUST emit the exact attribute order `id`, `digest`, `anchor`, omitting `anchor` when absent, with one ASCII space between grammar elements. The caller supplies the host comment wrapper and point of use; the writer MUST NOT guess a comment syntax from a file extension.

For a sidecar it MUST emit one YAML document, the `citations` key, and entries in requested order with field order `id`, `digest`, `anchor`. It MUST write the mapping shape even when maintaining a legacy bare-sequence ledger. Updating an existing sidecar is therefore a deterministic migration to the canonical form.

The writer MUST record the whole-artifact digest defined by RFC 0077. It MUST NOT emit the legacy brace-delimited inline form, a bare-sequence sidecar, duplicate carriers or a scenario-only digest. Readers MAY support legacy inputs as implementation extensions, but MUST NOT describe those inputs as conforming v0.2 citations.

### Invalid serialization and location

Add the stable error diagnostic:

| Code | Condition |
| --- | --- |
| `PRODUCT067` | Malformed citation payload or sidecar, missing sidecar consumer, or payload/sidecar carrier conflict. |

A payload citation's source location is its consumer file and one-based line number. A sidecar citation's source location is its ledger file and one-based entry number. Verification and impact output MUST report those locations. The diagnostic field-attribution contract is defined with the other diagnostics rather than invented by this RFC.

## Impact

- **On the Citation Contract:** replaces three unnamed forms with two fully specified carriers and a canonical writer contract. Citation fields, statuses, precedence and whole-artifact digest semantics do not change.
- **On existing repositories:** current mapping-form sidecars and `<!-- pdac:cite ... -->` fixtures already conform. Bare-sequence ledgers and brace-delimited inline references require canonical rewrite; readers may keep a compatibility path.
- **On implementations:** parsers gain closed validation and `PRODUCT067`; writers emit deterministic payloads or mapping-form sidecars only. Point-of-use reporting becomes portable.
- **On conformance tests:** add canonical payload, normalized sidecar, malformed payload, malformed sidecar, missing consumer and mixed-carrier cases. At least one negative case must require discovery so zero-citation discovery cannot pass vacuously.
- **On RFC 0004:** closes its citation-serialization deferral. Scope declarations and cross-repository resolution remain separate.

## Alternatives considered

**Mandate sidecars only.** Rejected. Sidecars are universal but lose a point of use inside a document, which is required for actionable review.

**Allow payload and sidecar citations together.** Rejected. Without citation identity beyond the record, implementations cannot distinguish a duplicated carrier from two intended dependencies and will disagree on counts.

**Preserve unknown attributes.** Rejected for v0.2. Ignoring an attribute whose future semantics may be security- or scope-relevant makes old readers report false success. A later serialization version can add fields explicitly.

**Accept arbitrary attribute order and escapes.** Rejected. The record has three fields; a closed order and no escapes make independent writers byte-for-byte predictable without reducing useful expressiveness.

**Keep the legacy inline form as normative.** Rejected. It adds a second payload grammar whose only definition is ProductShape source. Compatibility reading does not require canonical writing.

## Out of scope

- Scope-declaration serialization from [RFC 0042](0042-consumer-binding-for-sdd-alignment.md).
- Cross-repository citation resolution from [RFC 0021](0021-deployment-topologies.md).
- Sub-artifact digest canonicalization, rejected by [RFC 0077](0077-whole-artifact-digests-for-anchored-citations.md).

## Decision record

Accepted 2026-08-24 by the founding maintainer under the founder-led stabilization exception. The initial draft had been public since 2026-08-19; no substantive objection remained unresolved. Acceptance follows RFC 0077 so the writer has one digest rule for anchored and unanchored citations.

The decisive revision is that the RFC now specifies a writer, not only examples a parser might accept. Closed grammar, one sidecar document shape, exclusive carrier choice, stable entry numbering and `PRODUCT067` let a second implementation produce and diagnose the same repository without consulting ProductShape source.

Normative chapters, schema material and conformance cases land in a follow-up change.
