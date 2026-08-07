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

## Comparing diagnostics

A runner compares `severity`, `code`, `file`, `artifact`, `field` and `target`; `message` is implementation-defined ([Validation](../spec/validation.md)) and MUST NOT be compared. A field absent from an expected diagnostic is not asserted. `file` uses POSIX separators relative to `repo/`, and expected diagnostics are listed in the deterministic order the spec mandates: by file, then code, then target.

## Pinned digests

Several cases pin a content digest: a citation ledger (`*.citations.yml`) or a Markdown marker block records the digest of the artifact it cites. Editing a fixture artifact changes that digest, so a pin left behind describes a citation the case no longer contains. Every pin is recomputed on each pull request by the `Corpus` workflow, and locally with:

```bash
npx pdac-lint digests --spec .
```

A pin is expected to match the artifact it cites, except in a case that exists because it does not: a case expecting `PRODUCT061` or `PRODUCT062` for an artifact pins a digest that MUST differ, and the check asserts the difference, so an edit that accidentally makes a tampered fixture faithful is reported rather than quietly voiding the case. After changing a fixture artifact, recompute its digest and update every pin against it.

## Seed corpus

The seed corpus targets Product Change semantics, the citation contract, and the end-to-end scenarios that join them:

| Case | Verifies | Status |
| --- | --- | --- |
| `citation-current` | a consumer doc cites a baseline FR; status `current`; no `PRODUCT06x` | scaffolded |
| `citation-stale` | canonical FR amended after citation; `PRODUCT061` warning | planned |
| `citation-tampered` | embedded projection differs from canonical at recorded digest; `PRODUCT062` | planned |
| `citation-tampered-and-stale` | embedded block edited by hand and the cited target also moved; `PRODUCT062` alone, never `PRODUCT061` | scaffolded |
| `citation-unresolved` | target id or anchor does not resolve; `PRODUCT060` | planned |
| `scenario-id-addressing` | a citation anchors to `verification[].id`; partial scope without loss | planned |
| `greenfield-first-increment` | initialisation: empty model → `CHG-INITIAL` → apply → accept → cite | scaffolded |
| `brownfield-initial` | `CHG-INITIAL` from recovered artifacts carrying provenance; `PRODUCT111` | planned |
| `change-operations` | add of an existing ID, modify or remove of an absent one; `PRODUCT020`-`PRODUCT022` | planned |
| `change-proposed-mismatch` | proposed artifact not listed in operations, and the reverse; `PRODUCT026` | planned |
| `overlay-validation` | overlay duplicate IDs and removal leaving a dangling reference; `PRODUCT023`-`PRODUCT024` | planned |
| `concurrent-changes` | two active changes with overlapping modify/remove sets; `PRODUCT025` | planned |
| `apply-not-approved` | apply invoked on a change in status `proposed`; `PRODUCT028`, exit `1`, working tree untouched | planned |
| `apply-baseline-drift` | a `modify` target changed in the baseline since `base-revision`; `PRODUCT027` at apply; `add` not drift-checked | planned |
| `change-open-questions` | change in status `approved` with list items under `## Open Questions`; `PRODUCT108` warning | scaffolded |
| `change-superseded-archive` | a `superseded` change archived under `superseded/`; inert history, no diagnostics | planned |
| `intent-changes-mid-flight` | a change amends a cited rule; the product diff covers it and the citing spec reports `stale`; untouched citations stay `current` | planned |
| `partial-scope-without-loss` | cite `S1`,`S2` of a five-scenario FR | planned |
| `work-over-existing-baseline` | cite baseline requirements directly, with no product change at all | planned |
| `bug-or-refactor` | no product change; the fix's spec cites the governing rule; `current` | planned |
| `dedicated-topology` | a model repository holding the definition and no software; no diagnostics | scaffolded |

What the corpus cannot check it does not pretend to. Repository conformance clauses 1, 5 and 8 ([Conformance](../spec/conformance.md)) are about the repository rather than its files, a git repository, a canonical branch, a reviewed merge and the absence of an external source of truth, and a runner executes each fixture in a plain working copy. Those clauses are verified by review. The model-repository pointer has no fixture either: a pointer case needs two repository roots, the consumer and the model repository it points at, where a case is one `repo/`, and the specification deliberately fixes the pointer's record shape without fixing a serialization to check. Pointer cases arrive with that serialization.

Two planned apply cases (`apply-not-approved`, `apply-baseline-drift`) are not expressible as a flat `repo/` plus `expected.json`: they need the case format to express an apply invocation with an expected exit code and working-tree outcome, and, for drift, the baseline content at `base-revision`. That format extension is deferred until the corpus has its first runner. The shape of the product diff report is likewise not asserted by the corpus - fixing an expected report in a fixture would fix the serialization [RFC 0004](../rfcs/0004-delivery-model-reset.md) defers - so the reporting obligation joins `--dry-run` and `--format json` as implementation-conformance criteria verified by review rather than by fixture.
