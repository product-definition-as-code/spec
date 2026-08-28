# RFC 0085: JSON Pointer diagnostic fields

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-28
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/85>
- **Proposed target:** PDaC specification 0.2.0; no serialization-version change

## Problem

The validation chapter requires `PRODUCT002` to identify each invalid instance path in `field`, but does not define how an instance path is represented. One implementation can emit `given.0`, another can emit `/given/0`, and both describe the same location without producing the same diagnostic. The conformance runner compares `field` when a fixture asserts it, so the current suite cannot assert the full `PRODUCT002` contract portably.

The same gap applies to parsed configuration failures. `PRODUCT050` identifies the first invalid configuration instance path, but does not name its representation.

## Proposal

An instance path in a diagnostic `field` is an RFC 6901 JSON Pointer.

- A pointer identifies a location in the parsed document, not a source span or schema location.
- Array indexes are ordinary pointer segments. The first `given` item is `/given/0`.
- A missing required property or an additional property is identified as though the named property were present. A missing top-level `status` is `/status`.
- Pointer tokens use RFC 6901 escaping: `~` becomes `~0` and `/` becomes `~1`. An additional `recovered/by~` property under `provenance` is therefore `/provenance/recovered~1by~0`.
- The empty string identifies the document root when no named property identifies the failure.

The rule applies to `PRODUCT002` and to a parsed-configuration `PRODUCT050`. It does not change field notation for relationship, body-section, citation or Product Change diagnostics, which use the notation their existing rules prescribe.

The two Structured Behaviour keyword fixtures will assert `field: /given/0`. A new nested additional-property fixture will assert the escaped pointer `/provenance/recovered~1by~0`.

## Impact

- **On existing conformant repositories:** none. The rule controls diagnostic output, not document validity.
- **On implementations:** a v0.2 implementation must emit RFC 6901 pointers for the named diagnostics. No implementation currently claims v0.2 conformance.
- **On schemas and serialization:** none. The schemas and `v1alpha1` document representation are unchanged.
- **On conformance:** one fixture is added and two existing fixtures gain exact `field` assertions. No runner capability or diagnostic code is added.

## Alternatives considered

### Preserve dotted paths

Rejected. Dotted paths match one implementation's current output, but the notation has no existing escaping rule. Property names containing a dot, slash or tilde would make independently written dotted paths ambiguous. JSON Pointer is a standard, unambiguous locator already used by common schema validators.

### Leave the representation implementation-defined until v0.3

Rejected. The scope is a small determination over an existing required field, and delaying it preserves a cross-implementation ambiguity in the first v0.2 conformance suite. The change does not require a new schema, diagnostic or runner format.

### Define a new PDaC path syntax

Rejected. A new syntax would duplicate RFC 6901 while adding parser and escaping rules that every implementation would need to recreate.

## Decision record

Pending human acceptance under [CONTRIBUTING.md](../CONTRIBUTING.md). This is a determination: it selects a representation for an already-required diagnostic attribute and does not alter repository validity, schema semantics or the diagnostic set.
