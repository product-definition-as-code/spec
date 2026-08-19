# RFC 0047: One citation payload, any comment: normalize the citation carriers

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-19
- **Class:** change
- **Target:** PDaC v0.2.0
- **PR:** <https://github.com/product-definition-as-code/spec/pull/49>
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/47>
- **Public comment:** seven days; earliest acceptance 2026-08-26
- **Supersedes:** [RFC 0004](0004-delivery-model-reset.md) open question 1, in part

## Problem

The [Citation Contract](../spec/citation-contract.md) names three citation forms - an inline structured reference, a Markdown marker block, and a YAML sidecar ledger - and mandates none: "The spec defines the citation record shape, not a mandatory serialization."

That sentence is contradicted by the conformance tests and hollow for a second implementer, in four specific ways:

1. The conformance fixtures hard-code two serializations. `citation-current` requires reading a `feature-x.citations.yml` sidecar; `citation-tampered-and-stale` requires reading a `<!-- pdac:cite ... -->` marker block. An implementation that chooses only the third permitted form cannot pass the tests that define conformance, so the permission the text grants is one the tests revoke.
2. The inline structured reference has no syntax anywhere in the specification. It is named once. Its only concrete definition is the reference implementation's source code, which is exactly the dependency an implementation-independent specification exists to remove.
3. The sidecar has two accepted shapes. The reference implementation reads both a bare array and a mapping under a `citations:` key, with a source comment stating it is waiting for the specification to normalize one. The specification never does.
4. `conformance/README.md` states that "fixtures are plain files with no tooling assumptions", which is false for the citation cases: they assume the two serializations above.

[RFC 0004](0004-delivery-model-reset.md) deferred this deliberately ("the pilot exercises all three; a follow-up normalizes"). The deferral has done its work: the reference implementation has exercised all three forms, the fixtures pin two of them, and what remains is transcription, not invention. Deferring further protects no adopter and taxes every future implementer.

## Proposal

### One payload grammar, carrier-independent

A **citation payload** is the token `pdac:cite` followed by whitespace-separated `key="value"` attributes on a single line:

```
pdac:cite id="FR-VALIDATE-001" digest="sha256:..." anchor="S1"
```

- `id` and `digest` are required; `anchor` is optional. Their semantics are unchanged from the [Citation record](../spec/citation-contract.md#citation-record).
- Attribute values are double-quoted. Unknown attributes MUST be preserved and ignored, reserving room for evolution without breaking older readers.
- A payload MUST be discoverable by scanning for the `pdac:cite` token; the characters surrounding it belong to the host format and carry no citation semantics.

The payload rides inside the host format's native comment. Canonical carriers, non-exhaustively:

| Host format | Carrier |
| --- | --- |
| Markdown, HTML, MDX | `<!-- pdac:cite ... -->` |
| YAML, TOML, Python, shell | `# pdac:cite ...` |
| TypeScript, Go, Rust, C-family | `// pdac:cite ...` or `/* pdac:cite ... */` |

This is the pattern proven by `SPDX-License-Identifier`: one grammar, hosted by whatever comment syntax the file already has, so every commentable text format works without per-format specification text. The table above is illustrative; conformance is defined by the token scan, not by the table.

### The inline form is retired

A citation that embeds nothing is a self-contained payload line. The separately named "inline structured reference" was always this concept under a second syntax, so the two collapse into one: the specification defines the payload, and a bodyless payload line is the inline case. The brace-delimited `{pdac:cite ...}` syntax of the reference implementation remains discoverable under the token scan and is deprecated as a distinct form.

### Embedding is unchanged in semantics, normalized in syntax

A consumer MAY embed the cited canonical text. When it does: an opening payload line precedes the embedded bytes, and a closing line carrying the `/pdac:cite` token follows them (in Markdown: `<!-- /pdac:cite -->`). Every existing obligation of [Embedding](../spec/citation-contract.md#embedding) - byte-identical at the recorded digest, read-only, regenerable, `PRODUCT062` on divergence - applies as written.

### One sidecar shape

The sidecar ledger is normalized to exactly one form: a file named `<basename>.citations.yml` adjacent to the consumer document, containing a mapping with a top-level `citations:` array of citation records:

```yaml
citations:
  - id: FR-VALIDATE-001
    digest: sha256:...
    anchor: S1
```

The bare-array shape is retired. The mapping shape is chosen because it leaves room for sibling keys without a breaking change. The sidecar is intended for host formats that cannot carry comments; it remains a first-class form everywhere and the conformance tests continue to exercise it.

### Point of use is part of the contract

A payload-carried citation has a location: the consumer file and line where the token appears. Verification and impact reporting MUST include that location when the carrier provides one; a sidecar citation reports its ledger file and entry instead. Location is what turns "a citation went stale" into "review `specs/checkout.md:42`", and downstream obligations (see RFC 0048) depend on it.

## Impact

- **On the Citation Contract:** the "three forms" list and the "not a mandatory serialization" sentence are replaced by the payload grammar, the carrier rule, the embedding syntax and the sidecar shape above. The citation record's fields and the four statuses do not change.
- **On existing conformant repositories:** none. Every citation in the existing fixtures is already valid under this RFC.
- **On the reference implementation:** `cite --form inline` is retired (emitting a payload line instead); the sidecar writer emits the mapping shape only; the reader MAY keep accepting the bare array with a deprecation notice for one minor version; discovery moves to the token scan.
- **On conformance tests:** the two existing citation cases stay as they are. Two cases are added: a payload carried in a non-Markdown comment (for example `# pdac:cite` inside a YAML consumer), and a normalized-shape sidecar. The `conformance/README.md` sentence "fixtures are plain files with no tooling assumptions" is corrected to name the citation carriers.
- **On RFC 0004:** open question 1 is closed for the serializations; the "per host format" concern dissolves because the grammar is carrier-independent.
- **On versioning:** this adds normative serializations, so it targets v0.2.0.

## Alternatives considered

### Mandate the sidecar as the only form

Rejected. The sidecar records no point of use inside the consumer document, so review degrades from "look at line 42" to "somewhere in this document", and a reader of the document - human or agent - loses the in-context signal that a passage is grounded in canonical text. Location is load-bearing for the review workflow and for change-time impact (RFC 0048).

### Keep three forms

Rejected. The inline form is a bodyless marker under a second syntax; naming it separately doubles the surface a second implementer must build and a fixture author must cover, and adds no capability.

### A per-format syntax registry

Rejected. Enumerating carriers per host format grows the specification with every language and still misses the next one. The token-scan rule makes carriers open-ended with zero specification churn.

### Defer until an external pilot, per the RFC 0021 policy

Rejected here, on the policy's own terms. That policy exists so a format everyone must agree on is normalized after use rather than invented before it. These syntaxes have been in use by the reference implementation and pinned by fixtures for weeks; the invention already happened. What this RFC does is move the definition from one implementation's source into the specification, which is the smaller risk, not the larger one.

## Out of scope

- Digest granularity under an anchor ([issue #28](https://github.com/product-definition-as-code/spec/issues/28)).
- Scope-declaration serialization, which [RFC 0042](0042-consumer-binding-for-sdd-alignment.md) leaves open by design.
- Cross-repository citation resolution ([RFC 0021](0021-deployment-topologies.md)).

## RFC classification and review window

This RFC is a **change** under [CONTRIBUTING.md](../CONTRIBUTING.md): it adds normative serializations and retires a named form. Before v1.0 it requires a public comment window of at least seven days.
