# Operation case protocol, version 2

This is a portable test-runner protocol, not a required PDaC CLI, output format or persisted model format. Flat cases retain their existing `diagnostics`/`exitCode` shape. Version 2 is implemented by the coordinated `pdac-conformance` operation-runner change; the published 1.0.0 runner reports these cases as unsupported, never as passing.

`expected.json` uses `format: pdac-conformance-case/v2`, an operation (`validate`, `apply`, `apply-dry-run`, `verify-evidence`), diagnostics, required exitCode, reports and a tree assertion. Apply selects a `change` ID. Evidence operations explicitly select repository-relative `evidence` paths; `currentEvidence` selects only documents included in the live citation population. Fixture data never supplies executable commands.

`history` is an ordered list of fixture-relative full snapshot directories. The runner creates an isolated Git repository, commits each snapshot, overlays `repo/`, then replaces controlled `{{revision:0}}` tokens with the corresponding full commit SHA. Revisions are deterministic fixture setup, not an unresolved-revision exception in the specification. The fixture source remains read-only. Relative paths must not escape the fixture or address `.git`; fixture symlinks are unsupported.

The operator supplies a trusted `--adapter-command`. The runner appends `--request <temporary-json-file>` and invokes it with the working directory set to the isolated repository. The request contains operation, selected change, selected evidence/currentEvidence arrays and materialized revision SHAs. The adapter maps these to the implementation's CLI and normalizes observed output to JSON. It MUST preserve the implementation's exit code, diagnostics, forecast occurrence order and provider outcomes. It MUST NOT invent missing reports, re-sort a faulty forecast, repair the model or renew pins.

Normalized output contains `diagnostics` plus the report properties asserted by that case:

| Property | Normalized observation |
| --- | --- |
| `affectedCitations` | `{count, records}`; each record has `file`, optional `line` or `entry`, `target`, optional `anchor`, and `status`; preserve actual order and duplicate occurrences |
| `productDiff` | entries with `id`, `kind` and resulting `digest` except removals; adapter sorts by ID because product-diff serialization/order is not normative |
| `runRevision` | exact revision claimed by an evidence document |
| `evidenceResults` | result order, `testId`, `level`, unchanged `outcome`, and `citationStatuses` in citation order |

A `null` expected report property asserts absence, so a blocked gate cannot masquerade as an evaluated zero. Other expected report values are compared structurally, with array order significant. A selected implementation that offers no evidence integration may omit that optional group from its claim, but its named skipped cases remain visible.

`tree: {unchanged: true}` compares every ordinary file byte-for-byte, including untracked files, before and after invocation. `{after: "after", optionalAbsent: [...]}` compares the result with a complete expected snapshot. Only listed archived proposed files may be omitted, as the spec permits. Changed materialized content uses the standard line-ending equivalence; unchanged files remain exact. Archived change frontmatter is compared as YAML data and its body is retained, avoiding a requirement on YAML formatting. Git refs and staged content must remain unchanged.

The spec permits a generated product diff outside the archive. If an implementation persists one, its adapter may return `persistedProductDiffs: [{file, productDiff}]`, identifying the actual new file and decoding its contents into the same normalized diff. The runner compares that decoded value before permitting that extra file. Existing/canonical paths cannot be exempted. No other extra file, including a persisted citation forecast, is allowed. This adapter observation must be audited with the implementation; it is not permission to relabel a forecast as a diff.

These tests observe terminal output and files. The temporal obligation to emit the forecast before the first write, rollback on an injected mid-apply I/O failure, human acceptance and provider authenticity require additional implementation/integration review evidence; a successful final snapshot alone does not prove them.

Run both groups with the coordinated runner build:

```text
node <runner>/dist/bin.js run --spec <spec> --command "<implementation validation command>" --adapter-command "<trusted adapter>" --spec-version 0.3.0 --serialization-version v1alpha2
```

The legacy digest audit covers flat citation cases. `python scripts/check-v030.py` additionally audits v0.3 schemas, selected evidence, impact pins and report-source integrity. Neither fixture audit is an implementation conformance result.
