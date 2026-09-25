# Verification Evidence

Verification Evidence records traceable claims from external verification providers. It is optional to integrate and is not a Product Artifact, graph node, test definition, execution engine or test-management subsystem. PDaC does not schedule tests, manage suites or retries, prove that a run occurred, or require evidence coverage for acceptance or apply.

## Envelope

An explicitly selected evidence document MUST be one JSON object satisfying [`verification-evidence.schema.json`](../schemas/v1alpha2/verification-evidence.schema.json). Duplicate object keys are forbidden. The envelope and every result are closed objects.

| Field | Required value |
| --- | --- |
| `format` | exactly `pdac-verification-evidence/v1alpha1` |
| `provider` | nonblank external provider identifier |
| `run-id` | nonblank external run identifier |
| `revision` | full lowercase 40- or 64-hex Git commit SHA identifying the external run's revision |
| `results` | non-empty ordered array of result records |
| `results[].test-id` | nonblank external test identifier, unique within this document |
| `results[].level` | `domain`, `component`, `integration`, `end-to-end`, `manual` or `exploratory` |
| `results[].outcome` | `passed`, `failed` or `inconclusive` |
| `results[].citations` | non-empty ordered array of standard citation records (`id`, `digest`, optional `anchor`) |

The same test identifier MAY appear in different run documents. Evidence revision has no all-zero sentinel semantics. An adapter MUST report the exact run revision and the selected model revision separately; one MUST NOT be substituted for the other. The revision is a provider claim, not proof of authenticity or execution.

## Citation evaluation

Evidence citations MUST resolve to Structured Behaviour, Functional Requirement or Quality Requirement artifacts. The shared citation schema permits all Product Artifact ID prefixes syntactically; resolved target-kind restriction is semantic. Structured Behaviours are cited as whole artifacts without anchors. FR/QR citations MAY select an existing inline scenario anchor. Citation meaning, whole-artifact hashing and precedence are defined once in the [Citation Contract](citation-contract.md).

An adapter MUST preserve the provider's outcome independently of citation status. A passed result whose citation is stale remains an external passed claim about earlier intent; it MUST NOT be presented as evidence of current verification. Optional coverage views MUST retain this distinction and keep verification level separate from outcome.

Evaluation proceeds as follows:

1. A malformed or schema-invalid document produces exactly one `PRODUCT080`, then stops semantic evaluation of that document. For parseable input, `field` is the first invalid JSON Pointer in Unicode code-point order. Unparseable input, including duplicate JSON keys, omits `field`.
2. Each duplicate `test-id` occurrence after the first produces one `PRODUCT081` with `field: results[n].test-id`, using one-based result positions. That duplicate result's citations MUST NOT be evaluated. This form omits `target` and `entry`.
3. For each citation in a remaining result, an unresolved target produces `PRODUCT060`. A resolved target of a disallowed kind produces `PRODUCT081` alone for that citation, with `field: results[n].citations[m].id`, its `target`, and its flattened `entry`. Positions `n` and `m` are one-based.
4. After shape and target-kind checks, the existing citation precedence applies (`PRODUCT042`, `PRODUCT060`, `PRODUCT061`, `PRODUCT063`). Malformed citation shape is already `PRODUCT080`. Evidence carries no embedded projection, so `PRODUCT062` cannot arise from the evidence record itself.

Evidence diagnostics name the evidence file and MUST NOT carry `artifact` or `change`. Citation `entry` is the one-based ordinal across all citations in all results, including suppressed duplicate results. Suppression MUST NOT renumber subsequent entries. A disallowed resolved kind uses `PRODUCT081` rather than an additional citation diagnostic.

## Discovery and live population

An implementation claiming evidence integration MUST document explicit adapter selection/discovery and support the envelope and diagnostics above. It MUST NOT scan arbitrary JSON as evidence or require a duplicate `citations.yml` carrier for the same evidence. An evidence citation MUST NOT be indexed twice through multiple adapters.

Immutable historical run documents are excluded from the live consumer population. An adapter MAY include explicitly current evidence documents in its documented live population. When it does, verification and the [affected-citation forecast](product-changes.md#affected-citations) MUST use the same population, citation attribution and status rules. The applying change's container remains excluded. External outcome never changes an apply precondition. Evidence neither creates Product Graph edges nor silently refreshes citation pins.
