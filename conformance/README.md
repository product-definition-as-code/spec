# Conformance tests

**Status: published and runnable, not yet a complete normative set.** This directory holds the portable conformance tests: a set of fixture repositories plus expected-diagnostics files that any implementation, in any language, can run to verify conformance with the specification. All 43 published fixture directories execute today via [`pdac-conformance@1.0.0`](https://www.npmjs.com/package/pdac-conformance).

## Design

Each case is a directory:

```text
conformance/cases/<case-name>/
  repo/                      # a minimal product-model repository (the fixture)
  expected.json              # exitCode when asserted, plus diagnostics an implementation MUST produce
  case.md                    # what this case verifies, citing the spec chapter and clause
```

Rules for these tests: fixtures use only the normative repository, configuration and citation-carrier contracts; expected diagnostics reference the stable PRODUCT0xx/1xx codes defined in [validation](../spec/validation.md); a case covers exactly one normative clause wherever possible; and the tests are versioned with the spec. A conformance claim names both the method/spec version and the serialization version, so `0.2.0` with `v1alpha1` selects one precise document set and semantic contract.

## Comparing diagnostics

A runner compares `severity`, `code`, `file`, `artifact`, `change`, `field`, `target`, `line` and `entry`; `message` is implementation-defined ([Validation](../spec/validation.md)) and MUST NOT be compared. A field absent from an expected diagnostic is not asserted. `file` uses POSIX separators relative to `repo/`, and expected diagnostics follow the full deterministic order defined by the specification.

## Pinned digests

Several cases pin a content digest: a citation ledger (`*.citations.yml`) or a Markdown marker block records the digest of the artifact it cites. Editing a fixture artifact changes that digest, so a pin left behind describes a citation the case no longer contains. Every pin is recomputed on each pull request by the `Conformance` workflow, and locally with:

```bash
npx --yes pdac-conformance@1.0.0 digests --spec . \
  --spec-version 0.2.0 --serialization-version v1alpha1
```

A pin is expected to match the artifact it cites, except in a case that exists because it does not: a case expecting `PRODUCT061` or `PRODUCT062` for an artifact pins a digest that MUST differ, and the check asserts the difference, so an edit that accidentally makes a tampered fixture faithful is reported rather than quietly voiding the case. A case expecting `PRODUCT060` for a target pins an ID that MUST NOT resolve, asserted the same way. After changing a fixture artifact, recompute its digest and update every pin against it.

## Seed test cases

The seed test cases target Product Change semantics, the citation contract, and the end-to-end scenarios that join them:

| Case | Verifies | Status |
| --- | --- | --- |
| `citation-current` | a consumer doc cites a baseline FR; status `current`; no `PRODUCT06x` | runnable |
| `citation-stale` | canonical FR amended after citation; `PRODUCT061` warning | runnable |
| `citation-tampered` | embedded projection differs from canonical at recorded digest; `PRODUCT062` | planned |
| `citation-tampered-and-stale` | embedded block edited by hand and the cited target also moved; `PRODUCT062` alone, never `PRODUCT061` | runnable |
| `citation-unresolved` | target `id` does not resolve; `PRODUCT060` | runnable |
| `citation-anchor-not-found` | target resolves at the current digest but the named anchor does not exist within it; `PRODUCT063`, not `PRODUCT060` | runnable |
| `digest-bytes-not-text` | the cited artifact contains bytes that are not well-formed UTF-8; the digest covers the raw bytes; `current`, no diagnostics | runnable |
| `configuration-custom-root` | versioned config selects a non-default product root; artifact is discovered; exit `0` | runnable |
| `configuration-malformed` | malformed config; one `PRODUCT050`; exit `2`; no artifact discovery | runnable |
| `configuration-unknown-key` | unknown top-level config key; one attributed `PRODUCT050`; exit `2` | runnable |
| `scenario-id-addressing` | a citation anchors to `verification[].id`; the anchor scopes reliance while the digest covers the whole artifact | runnable via `citation-current` |
| `greenfield-first-increment` | initialisation: empty model → `CHG-INITIAL` → apply → accept → cite | runnable |
| `artifact-kinds-valid` | one artifact of each of the ten kinds plus a second Domain Term, including a Structured Behaviour referenced alongside an inline scenario; zero diagnostics | runnable |
| `brownfield-initial` | `CHG-INITIAL` from recovered artifacts carrying provenance; `PRODUCT111` | planned |
| `change-add-existing` | add of an ID that already exists in the baseline; `PRODUCT020` | planned |
| `change-modify-missing-target` | modify of an ID absent from the baseline; `PRODUCT021` | runnable |
| `change-remove-missing-target` | remove of an ID absent from the baseline; `PRODUCT022` | runnable |
| `change-proposed-undeclared` | proposed artifact not listed in operations; `PRODUCT026` | runnable |
| `change-operation-unproposed` | declared operation without its proposed artifact; `PRODUCT026` | runnable |
| `overlay-duplicate-id` | overlay produces duplicate IDs; one `PRODUCT023` per occurrence after the first | planned |
| `change-removal-dangling-reference` | removal leaving a dangling reference in the overlay; `PRODUCT024` | runnable |
| `concurrent-changes` | two active changes with overlapping modify sets; `PRODUCT025` against each | runnable |
| `apply-not-approved` | apply invoked on a change in status `proposed`; `PRODUCT028`, exit `1`, working tree untouched | planned |
| `apply-baseline-drift` | a `modify` target changed in the baseline since `base-revision`; `PRODUCT027` at apply; `add` not drift-checked | planned |
| `apply-initial-sentinel` | `CHG-INITIAL` with exact `0000000` skips revision resolution and drift checks; any other change or all-zero value follows ordinary Git rules | planned - needs the apply case format |
| `apply-base-revision-unresolved` | an ordinary unresolved `base-revision` emits one `PRODUCT027`, exits `1`, and leaves the working tree untouched | planned - needs the apply case format |
| `change-open-questions` | change in status `approved` with list items under `## Open Questions`; `PRODUCT108` warning | runnable |
| `change-superseded-archive` | a `superseded` change archived under `superseded/`; inert history, no diagnostics | planned |
| `intent-changes-mid-flight` | a change amends a cited rule; the product diff covers it and the citing spec reports `stale`; untouched citations stay `current` | planned |
| `anchored-whole-artifact-review` | an edit outside cited anchor `S1` still makes its whole-artifact digest stale | runnable via `citation-stale` |
| `citation-carrier-malformed` | malformed or conflicting carrier emits attributed `PRODUCT067` | planned |
| `consumer-population-unclassified` | an enumerated current document without a scope declaration emits `PRODUCT064` | planned - needs an adapter fixture format |
| `consumer-population-bound-empty` | an enumerated `bound` document without citations emits `PRODUCT065` | planned - needs an adapter fixture format |
| `consumer-population-invalid-exemption` | empty exemption reason or citations on an exempt document emit `PRODUCT066` | planned - needs an adapter fixture format |
| `work-over-existing-baseline` | cite baseline requirements directly, with no product change at all | planned |
| `bug-or-refactor` | no product change; the fix's spec cites the governing rule; `current` | planned |
| `dedicated-topology` | a model repository holding the definition and no software; no diagnostics | runnable |

### RFC 0084 fixture matrix

`artifact-kinds-valid` covers acceptance of the tenth artifact kind, a Functional Requirement reference and mixed verification entry, all three allowed `illustrates` target prefixes, Use Case and Structured Behaviour term usage on one term each, and Product Change addition through `CHG-INITIAL`.

The following cases complete the executable RFC 0084 matrix:

| Case | Verifies | Status |
| --- | --- | --- |
| `structured-behaviour-quality-reference` | Quality Requirement reference to a Structured Behaviour | runnable |
| `structured-behaviour-change-add` | valid active Product Change addition of a Structured Behaviour | runnable |
| `structured-behaviour-change-modify` | valid Product Change modification of a Structured Behaviour | runnable |
| `structured-behaviour-citation-current` | current direct Structured Behaviour citation | runnable |
| `structured-behaviour-citation-stale` | changed direct Structured Behaviour target; `PRODUCT061` | runnable |
| `structured-behaviour-citation-unaffected` | current direct citation alongside an unrelated archived change and uncited second Structured Behaviour | runnable |
| `structured-behaviour-scenario-ref-unknown` | unknown `verification[].scenario-ref`; `PRODUCT006` | runnable |
| `structured-behaviour-scenario-ref-retired` | retired `verification[].scenario-ref` target; `PRODUCT008` | runnable |
| `structured-behaviour-scenario-ref-removed` | removed `verification[].scenario-ref` target in an overlay; `PRODUCT024` | runnable |
| `structured-behaviour-illustrates-unknown` | unknown `illustrates` target; `PRODUCT006` | runnable |
| `structured-behaviour-illustrates-retired` | retired `illustrates` target; `PRODUCT008` alone | runnable |
| `structured-behaviour-illustrates-removed` | removed `illustrates` target in an overlay; `PRODUCT024` | runnable |
| `structured-behaviour-uses-terms-unknown` | unknown `uses-terms` target; `PRODUCT006` | runnable |
| `structured-behaviour-uses-terms-retired` | retired `uses-terms` target; `PRODUCT008` alone | runnable |
| `structured-behaviour-uses-terms-removed` | removed `uses-terms` target in an overlay; `PRODUCT024` | runnable |
| `structured-behaviour-semantic-keyword` | forbidden upper-case semantic-keyword prefix; `PRODUCT002` | runnable |
| `structured-behaviour-semantic-keyword-case` | mixed-case semantic keyword rejected, longer word accepted; one `PRODUCT002` | runnable |
| `structured-behaviour-body-section-missing` | missing `## Boundaries`; `PRODUCT009` | runnable |
| `structured-behaviour-body-section-order` | out-of-order `## Boundaries`; `PRODUCT009` | runnable |
| `structured-behaviour-citation-anchor` | anchor on a Structured Behaviour; `PRODUCT063` | runnable |
| `structured-behaviour-illustrates-no-consumer` | `illustrates` does not suppress `PRODUCT105` | runnable |
| `structured-behaviour-retired-governed-by-no-consumer` | retired `governed-by` source does not suppress `PRODUCT105` | runnable |
| `structured-behaviour-retired-uses-terms-no-usage` | retired Structured Behaviour term use does not suppress `PRODUCT106` | runnable |

The retired Business Rule and Domain Term target cases assert `PRODUCT008` alone because retired targets are outside the `PRODUCT105` and `PRODUCT106` warning populations. Each relationship-negative case asserts the source artifact, exact field and target, including the exact `verification[].scenario-ref` spelling.

### RFC 0085 diagnostic-field notation

| Case | Verifies | Status |
| --- | --- | --- |
| `schema-instance-path-escaping` | nested additional property has an escaped JSON Pointer `field`; `PRODUCT002` | runnable |

The two Structured Behaviour semantic-keyword cases also assert `field: /given/0`, so a runner must report the array-member JSON Pointer rather than only the diagnostic code.

No new-field fixture isolates `PRODUCT007`. The new schemas admit only allowed target prefixes, so a resolving artifact with an admitted prefix but a disallowed type also violates that artifact's ID/type alignment. A conforming implementation emits both `PRODUCT004` against the target artifact and `PRODUCT007` against the source relationship entry, but the two subjects prevent one fixture from isolating one normative clause under the case convention.

Duplicate-ID granularity is fixed in [Validation → Emission granularity and attribution](../spec/validation.md#emission-granularity-and-attribution): deterministic file/document order establishes the first occurrence, and each later occurrence receives one diagnostic. `change-add-existing` and `overlay-duplicate-id` are therefore implementable rather than blocked; their fixtures remain planned.

What the tests cannot check they do not pretend to. Repository conformance clauses 1, 5 and 8 ([Conformance](../spec/conformance.md)) are about the repository rather than its files, a git repository, a canonical branch, a reviewed merge and the absence of an external source of truth, and a runner executes each fixture in a plain working copy. Those clauses are verified by review. The model-repository pointer has no fixture either: a pointer case needs two repository roots, the consumer and the model repository it points at, where a case is one `repo/`, and the specification deliberately fixes the pointer's record shape without fixing a serialization to check. Pointer cases arrive with that serialization.

The planned apply cases (`apply-not-approved`, `apply-baseline-drift`, `apply-initial-sentinel` and `apply-base-revision-unresolved`) are not expressible as a flat `repo/` plus `expected.json`: they need the case format to express an apply invocation and working-tree outcome, and, for drift and revision resolution, a Git history. The runner can assert an `exitCode` for its configured validation commands, but it does not yet describe an apply invocation or repository history. The shape of the product diff report is likewise not asserted by the tests - fixing an expected report in a fixture would fix the serialization [RFC 0004](../rfcs/0004-delivery-model-reset.md) defers - so the reporting obligation joins `--dry-run` and `--format json` as implementation-conformance criteria verified by review rather than by fixture.

The three configuration fixtures specify `exitCode` because invalid configuration MUST exit `2` before validation. `pdac-conformance@1.0.0` asserts that exit code independently for every configured implementation command. A skipped case is not conformance evidence.

## Diagnostic coverage

Which fixture exercises which diagnostic code, code by code. "Exercises" means the case expects the diagnostic and fails an implementation that does not emit it; the zero-diagnostic cases (`artifact-kinds-valid`, `citation-current`, `configuration-custom-root`, `digest-bytes-not-text`, `greenfield-first-increment`, `dedicated-topology`, `structured-behaviour-quality-reference`, `structured-behaviour-change-add`, `structured-behaviour-change-modify`, `structured-behaviour-citation-current` and `structured-behaviour-citation-unaffected`) additionally fail an implementation that emits any of these codes where none is warranted, and `citation-tampered-and-stale` asserts the *absence* of `PRODUCT061` next to the `PRODUCT062` it expects. Codes marked not yet covered are honest gaps: a badge computed from these tests says nothing about them. The retired codes (`PRODUCT030`-`PRODUCT032`, `PRODUCT040`-`PRODUCT041`, `PRODUCT043`-`PRODUCT044`, `PRODUCT109`, `PRODUCT110`) and the reserved `PRODUCT070`-`PRODUCT079` band are never issued, so they have nothing to cover.

| Code | Condition | Exercised by |
| --- | --- | --- |
| `PRODUCT001` | invalid frontmatter or unparseable document | not yet covered |
| `PRODUCT002` | JSON Schema violation | `structured-behaviour-semantic-keyword`, `structured-behaviour-semantic-keyword-case`, `schema-instance-path-escaping` |
| `PRODUCT003` | unknown artifact `type` | not yet covered |
| `PRODUCT004` | ID prefix does not match the artifact type | not yet covered |
| `PRODUCT005` | duplicate ID | not yet covered - duplicate-ID granularity (see above) |
| `PRODUCT006` | reference to an unknown ID | `structured-behaviour-scenario-ref-unknown`, `structured-behaviour-illustrates-unknown`, `structured-behaviour-uses-terms-unknown` |
| `PRODUCT007` | relationship targets a disallowed artifact type | not yet covered |
| `PRODUCT008` | active artifact references a retired artifact | `structured-behaviour-scenario-ref-retired`, `structured-behaviour-illustrates-retired`, `structured-behaviour-uses-terms-retired` |
| `PRODUCT009` | required body section missing or out of order | `structured-behaviour-body-section-missing`, `structured-behaviour-body-section-order` |
| `PRODUCT020` | addition whose ID already exists in the baseline | not yet covered |
| `PRODUCT021` | modification of an ID absent from the baseline | `change-modify-missing-target` |
| `PRODUCT022` | removal of an ID absent from the baseline | `change-remove-missing-target` |
| `PRODUCT023` | overlay produces duplicate IDs | not yet covered |
| `PRODUCT024` | removal leaves a dangling reference in the overlay | `change-removal-dangling-reference`, `structured-behaviour-scenario-ref-removed`, `structured-behaviour-illustrates-removed`, `structured-behaviour-uses-terms-removed` |
| `PRODUCT025` | concurrent changes with overlapping modify/remove sets | `concurrent-changes` |
| `PRODUCT026` | proposed artifact and operations disagree | `change-proposed-undeclared`, `change-operation-unproposed` |
| `PRODUCT027` | unresolved ordinary `base-revision` or baseline drift at apply | not yet covered - needs the apply case format |
| `PRODUCT028` | apply on a change not `approved` | not yet covered - needs the apply case format |
| `PRODUCT042` | invalid or unverifiable citation digest | not yet covered |
| `PRODUCT050` | invalid configuration | `configuration-malformed`, `configuration-unknown-key` |
| `PRODUCT051` | managed file modified by hand | not yet covered - `doctor` surface |
| `PRODUCT052` | expected managed file missing | not yet covered - `doctor` surface |
| `PRODUCT060` | citation target `id` does not resolve | `citation-unresolved` |
| `PRODUCT061` | stale citation | `citation-stale`, `structured-behaviour-citation-stale`; absence asserted by `citation-tampered-and-stale` |
| `PRODUCT062` | tampered embedded projection | `citation-tampered-and-stale` |
| `PRODUCT063` | citation anchor not found in the target | `citation-anchor-not-found`, `structured-behaviour-citation-anchor` |
| `PRODUCT064` | enumerated current consumer has no scope declaration | not yet covered - needs an adapter fixture format |
| `PRODUCT065` | bound consumer contains no citations | not yet covered - needs an adapter fixture format |
| `PRODUCT066` | invalid exemption | not yet covered - needs an adapter fixture format |
| `PRODUCT067` | malformed, orphaned or conflicting citation carrier | not yet covered |
| `PRODUCT101` | file name not aligned with ID | not yet covered |
| `PRODUCT102` | active use case in no journey | not yet covered |
| `PRODUCT103` | requirement unreachable from any actor | not yet covered |
| `PRODUCT104` | deprecated artifact still referenced | not yet covered |
| `PRODUCT105` | business rule with no consumers | `structured-behaviour-illustrates-no-consumer`, `structured-behaviour-retired-governed-by-no-consumer` |
| `PRODUCT106` | domain term with no usage | `artifact-kinds-valid` demonstrates both Use Case and Structured Behaviour usage, one term each; `structured-behaviour-retired-uses-terms-no-usage` |
| `PRODUCT107` | bounded context with no owned language | not yet covered |
| `PRODUCT108` | `approved` change with unresolved open questions | `change-open-questions` |
| `PRODUCT111` | draft artifact with low-confidence provenance | not yet covered |
