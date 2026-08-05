# Conformance corpus

**Status: in progress (scaffolded).** This directory holds the portable conformance corpus: a set of fixture repositories plus expected-diagnostics files that any implementation, in any language, can run to verify conformance with the specification.

## Design

Each case is a directory:

```text
conformance/cases/<case-name>/
  repo/                      # a minimal product-model repository (the fixture)
  expected.json              # diagnostics an implementation MUST produce, with stable codes
  case.md                    # what this case verifies, citing the spec chapter and clause
```

Rules of the corpus: fixtures are plain files with no tooling assumptions; expected diagnostics reference the stable PRODUCT0xx/1xx codes defined in [validation](../spec/validation.md); a case covers exactly one normative clause wherever possible; and the corpus is versioned with the spec, so "conformant with v1.0" is a precise, checkable claim.

## Seed corpus

The seed corpus targets Product Change semantics, the citation contract, and the end-to-end scenarios that join them:

| Case | Verifies | Status |
| --- | --- | --- |
| `citation-current` | a consumer doc cites a baseline FR; status `current`; no `PRODUCT06x` | scaffolded |
| `citation-stale` | canonical FR amended after citation; `PRODUCT061` warning | planned |
| `citation-tampered` | embedded projection differs from canonical at recorded digest; `PRODUCT062` | planned |
| `citation-unresolved` | target id or anchor does not resolve; `PRODUCT060` | planned |
| `scenario-id-addressing` | a citation anchors to `verification[].id`; partial scope without loss | planned |
| `greenfield-first-increment` | initialisation: empty model → `CHG-INITIAL` → apply → accept → cite | scaffolded |
| `brownfield-initial` | `CHG-INITIAL` from recovered artifacts carrying provenance; `PRODUCT111` | planned |
| `change-operations` | add of an existing ID, modify or remove of an absent one; `PRODUCT020`-`PRODUCT022` | planned |
| `change-proposed-mismatch` | proposed artifact not listed in operations, and the reverse; `PRODUCT026` | planned |
| `overlay-validation` | overlay duplicate IDs and removal leaving a dangling reference; `PRODUCT023`-`PRODUCT024` | planned |
| `concurrent-changes` | two active changes with overlapping modify/remove sets; `PRODUCT025` | planned |
| `apply-baseline-drift` | baseline artifact changed since `base-revision`; `PRODUCT027` at apply | planned |
| `change-open-questions` | change approved with unresolved open questions; `PRODUCT108` warning | planned |
| `intent-changes-mid-flight` | a change amends a cited rule; the citing spec reports `stale` | planned |
| `partial-scope-without-loss` | cite `S1`,`S2` of a five-scenario FR | planned |
| `work-over-existing-baseline` | cite baseline requirements directly, with no product change at all | planned |
| `bug-or-refactor` | no product change; the fix's spec cites the governing rule; `current` | planned |
