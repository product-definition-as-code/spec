# Conformance corpus

**Status: planned.** This directory will hold the portable conformance corpus: a set of fixture
repositories plus expected-diagnostics files that any implementation, in any language, can run to
verify conformance with the specification.

## Design

Each case is a directory:

```text
conformance/cases/<case-name>/
  repo/                      # a minimal product-model repository (the fixture)
  expected.json              # diagnostics an implementation MUST produce, with stable codes
  case.md                    # what this case verifies, citing the spec chapter and clause
```

Rules of the corpus: fixtures are plain files with no tooling assumptions; expected diagnostics
reference the stable PRODUCT0xx/1xx codes defined in [validation](../spec/validation.md); a case
covers exactly one normative clause wherever possible; and the corpus is versioned with the spec,
so "conformant with v1.0" is a precise, checkable claim.

The initial corpus will be derived from the validation suite of the reference implementation.
