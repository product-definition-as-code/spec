# Validation

Structural validation is deterministic. Given the same repository content, validation MUST produce the same diagnostics in the same order on every platform. AI is never used to enforce structural invariants.

## Diagnostics

Every diagnostic carries:

| Field      | Presence        | Meaning                                            |
| ---------- | --------------- | -------------------------------------------------- |
| `severity` | always          | `error` or `warning`                               |
| `code`     | always          | stable code from the tables below                  |
| `message`  | always          | human-readable explanation                         |
| `file`     | always          | repository-relative source file (POSIX separators) |
| `artifact` | when available  | artifact ID                                        |
| `field`    | when available  | frontmatter field or relationship                  |
| `target`   | when applicable | referenced target ID                               |

Diagnostics MUST be available in machine-readable JSON (`--format json`) and MUST be ordered deterministically (by file, then code, then target).

Warnings are not errors. `validation.warnings-as-errors` in `.product/config.yaml` MAY escalate them for a repository; tools MUST NOT escalate unilaterally.

## Error codes

| Code         | Condition                                                                              |
| ------------ | -------------------------------------------------------------------------------------- |
| `PRODUCT001` | Invalid YAML frontmatter or unparseable artifact document                              |
| `PRODUCT002` | JSON Schema violation (missing required field, unknown property, invalid value)        |
| `PRODUCT003` | Unknown artifact `type`                                                                |
| `PRODUCT004` | ID prefix does not match the artifact type                                             |
| `PRODUCT005` | Duplicate ID                                                                           |
| `PRODUCT006` | Reference to an unknown ID                                                             |
| `PRODUCT007` | Relationship targets a disallowed artifact type                                        |
| `PRODUCT008` | Active artifact references a retired artifact                                          |
| `PRODUCT009` | Required body section missing or out of order                                          |
| `PRODUCT020` | Product Change addition whose ID already exists in the baseline                        |
| `PRODUCT021` | Product Change modification of an ID that does not exist in the baseline               |
| `PRODUCT022` | Product Change removal of an ID that does not exist in the baseline                    |
| `PRODUCT023` | Overlay produces duplicate IDs                                                         |
| `PRODUCT024` | Removal leaves a dangling reference from an active artifact in the overlay             |
| `PRODUCT025` | Concurrent active Product Changes with overlapping modify/remove operations            |
| `PRODUCT026` | Proposed artifact not listed in operations, or operation without its proposed artifact |
| `PRODUCT027` | Baseline revision incompatible at apply without explicit resolution                    |
| `PRODUCT028` | Apply attempted on a Product Change whose status is not `approved`                     |
| `PRODUCT042` | Invalid or unverifiable citation digest                                                 |
| `PRODUCT050` | Invalid configuration or unknown top-level configuration key                           |
| `PRODUCT051` | Managed integration file modified by hand                                              |
| `PRODUCT052` | Expected managed or generated file missing                                             |
| `PRODUCT060` | Unresolved citation: target `id` or `anchor` does not resolve                          |
| `PRODUCT062` | Tampered embedded projection: embedded block differs from canonical at recorded digest |
| `PRODUCT063` | Anchor not found: target resolves but the named anchor does not exist within it        |

`PRODUCT020`-`PRODUCT028` apply to Product Changes and their overlays; see [Product Changes](product-changes.md). They are reported when a change is validated or applied, never when validating the baseline alone, and never against archived changes.

`PRODUCT027` and `PRODUCT028` are apply preconditions: they are evaluated before anything is written and reported with the working tree untouched. The invocation itself is well-formed, so apply exits `1`, not `2` (see [Exit codes](#exit-codes)).

`PRODUCT050`-`PRODUCT052` are reported by `doctor` and integration commands; product-model validation does not inspect managed files.

`PRODUCT060`-`PRODUCT063` are citation diagnostics; see the [Citation Contract](citation-contract.md). `PRODUCT061` is a warning; a repository MAY escalate it via `warnings-as-errors`. Tools MUST NOT apply per-artifact-type severity defaults: risk policy belongs to the repository, not the kernel.

When more than one citation condition holds, [Citation Contract → Precedence](citation-contract.md#precedence) decides which one is reported, and only that condition's diagnostic is emitted: an embedded projection edited by hand whose cited text has also moved is `PRODUCT062`, never `PRODUCT062` and `PRODUCT061` together.

Diagnostic codes are stable and are never renumbered or reused. `PRODUCT030`-`PRODUCT032`, `PRODUCT040`-`PRODUCT041`, `PRODUCT043`-`PRODUCT044`, `PRODUCT109` and `PRODUCT110` are retired: they belonged to the delivery pipeline removed by [RFC 0004](../rfcs/0004-delivery-model-reset.md) and are never reissued with a new meaning.

## Warning codes

| Code         | Condition                                                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PRODUCT061` | Stale citation: target resolves but canonical content changed since the citation                                                                                   |
| `PRODUCT101` | Artifact file name not aligned with its ID                                                                                                                         |
| `PRODUCT102` | Active use case not present in any journey                                                                                                                         |
| `PRODUCT103` | Requirement not reachable from any actor (see [Relationships → Reachability](relationships.md#reachability)); product-wide constraints are reachable by definition |
| `PRODUCT104` | Deprecated artifact still referenced by an active artifact                                                                                                         |
| `PRODUCT105` | Business rule with no consumers                                                                                                                                    |
| `PRODUCT106` | Domain term with no usage                                                                                                                                          |
| `PRODUCT107` | Bounded context with no owned domain language                                                                                                                      |
| `PRODUCT108` | Product Change in status `approved` with an unresolved question (a list item) under `## Open Questions`                                                            |
| `PRODUCT111` | Draft artifact whose `provenance.confidence` is `low`                                                                                                              |

`PRODUCT101` is mechanically resolvable: an implementation MAY offer a fix operation renaming each file to `<id.toLowerCase()>.md`. It renames through a temporary name so it also works on case-insensitive filesystems, where a casing-only rename is otherwise a silent no-op. `--dry-run` reports the plan and exits non-zero when anything would change, which makes it usable as a CI gate: `PRODUCT101` is a warning, so it is not otherwise caught unless `warnings-as-errors` is set.

`PRODUCT111` marks recovered knowledge that needs human validation rather than a defect to repair; see [Frontmatter reference → Provenance](frontmatter-reference.md#provenance).

## Exit codes

| Code | Meaning                                                 |
| ---- | ------------------------------------------------------- |
| `0`  | Success; warnings allowed (unless `warnings-as-errors`) |
| `1`  | Validation or conformance errors                        |
| `2`  | Invalid invocation or configuration                     |
| `3`  | Unexpected internal failure                             |

## Digests

Content digests are SHA-256 over the artifact's UTF-8 bytes with CRLF and CR line endings normalized to LF, rendered as `sha256:<lowercase hex>`. This normalization is mandatory: digests MUST be identical across operating systems and Git line-ending configurations. Citation digests use the same normalization (see the [Citation Contract](citation-contract.md)).

## Determinism requirements

- Artifact discovery, graph compilation, traversal, product diff computation, impact analysis and diagnostic ordering MUST be deterministic and platform-independent.
- Generated outputs (`product-graph.json`, indexes, Mermaid, diagnostics JSON) MUST be byte-identical for identical input content, and `product-graph.json` MUST carry a versioned schema identifier.

Product diff determinism is semantic: the same baseline and applied result MUST yield the same set of impacted artifacts, impact kinds and resulting digests. Byte-identity of the diff report is not required while its serialization remains unfixed ([RFC 0004](../rfcs/0004-delivery-model-reset.md) open question 3).
