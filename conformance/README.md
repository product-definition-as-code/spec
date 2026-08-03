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

The seed corpus targets the citation contract and the six acceptance scenarios from RFC #4:

| Case | Verifies | Status |
| --- | --- | --- |
| `citation-current` | a consumer doc cites a baseline FR; status `current`; no `PRODUCT06x` | scaffolded |
| `citation-stale` | canonical FR amended after citation; `PRODUCT061` warning | planned |
| `citation-tampered` | embedded projection differs from canonical at recorded digest; `PRODUCT062` | planned |
| `citation-unresolved` | target id or anchor does not resolve; `PRODUCT060` | planned |
| `scenario-id-addressing` | a citation anchors to `verification[].id`; partial scope without loss | planned |
| `greenfield-first-increment` | acceptance scenario 1: empty model → PR → merge → cite | scaffolded |
| `intent-changes-mid-flight` | acceptance scenario 2: cited rule amended → `stale` in CI | planned |
| `partial-scope-without-loss` | acceptance scenario 3: cite `S1`,`S2` of a five-scenario FR | planned |
| `work-over-existing-baseline` | acceptance scenario 4: cite baseline requirements directly | planned |
| `bug-or-refactor` | acceptance scenario 5: no model PR; cite governing rule; `current` | planned |
| `brownfield-recovery` | acceptance scenario 6: recovered artifacts enter via PRs; `PRODUCT111` | planned |
