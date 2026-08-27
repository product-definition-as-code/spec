# Validation

Structural validation is deterministic. Given the same repository content, validation MUST produce the same diagnostics in the same order on every platform. An implementation never uses AI to enforce structural invariants.

## Diagnostics

Every diagnostic carries:

| Field      | Presence        | Meaning                                                                                     |
| ---------- | --------------- | ------------------------------------------------------------------------------------------- |
| `severity` | always          | `error` or `warning`                                                                        |
| `code`     | always          | stable code from the tables below                                                           |
| `message`  | always          | human-readable explanation                                                                  |
| `file`     | always          | repository-relative source or expected file (POSIX separators)                              |
| `artifact` | when applicable | ID of the Product Artifact the diagnostic is about; never a Product Change or unresolved ID |
| `change`   | when applicable | ID of the Product Change the diagnostic is about                                            |
| `field`    | when applicable | frontmatter field, relationship or body section                                             |
| `target`   | when applicable | referenced, operated-on or cited ID exactly as authored, whether or not it resolves          |
| `line`     | payload only    | one-based consumer-file line carrying a citation payload                                     |
| `entry`    | sidecar only    | one-based citation entry within the sidecar's `citations` sequence                           |

`artifact`, `change` and `target` are distinct subjects. In particular, a citation diagnostic uses `target` for the cited ID. An unresolved ID MUST NOT appear in `artifact`, because resolution is what would establish that it identifies an artifact. A Product Change ID MUST appear in `change`, never `artifact`.

Diagnostics MUST be available in machine-readable JSON (`--format json`) and MUST be ordered deterministically by `file`, then `line` (absent before present), then `entry` (absent before present), then `code`, `field`, `target`, `artifact` and `change`, comparing absent strings as empty strings. Numeric fields sort numerically; strings sort by Unicode code point.

Warnings are not errors. `validation.warnings-as-errors` in the versioned [Configuration](configuration.md) MAY make a command fail when warnings are present; tools MUST NOT escalate unilaterally, and the emitted diagnostic severity remains `warning`.

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
| `PRODUCT027` | Ordinary base revision does not resolve, or a modify/remove target changed since it    |
| `PRODUCT028` | Apply attempted on a Product Change whose status is not `approved`                     |
| `PRODUCT042` | Invalid or unverifiable citation digest                                                 |
| `PRODUCT050` | Invalid configuration or unknown top-level configuration key                           |
| `PRODUCT051` | Managed integration file modified by hand                                              |
| `PRODUCT052` | Expected managed or generated file missing                                             |
| `PRODUCT060` | Unresolved citation: target `id` does not resolve                                     |
| `PRODUCT062` | Tampered embedded projection: embedded block differs from canonical at recorded digest |
| `PRODUCT063` | Anchor not found: target resolves but the named anchor does not exist within it        |
| `PRODUCT064` | Current consumer document has no population-aware scope declaration                    |
| `PRODUCT065` | Consumer document declares `bound` but contains no citations                           |
| `PRODUCT066` | Invalid exemption: empty reason or citation present                                    |
| `PRODUCT067` | Malformed citation carrier, missing sidecar consumer or mixed carriers                  |

`PRODUCT020`-`PRODUCT028` apply to Product Changes and their overlays; see [Product Changes](product-changes.md). They are reported when a change is validated or applied, never when validating the baseline alone, and never against archived changes.

When a dangling reference in the overlay is caused by an ID named in the change's `remove` set, only `PRODUCT024` is reported for it; `PRODUCT006` MUST NOT additionally be reported for the same reference. `PRODUCT006` remains the diagnostic for a reference that dangles for any other reason (see [Product Changes → Overlay validation](product-changes.md#overlay-validation)).

`PRODUCT027` and `PRODUCT028` are apply preconditions: they are evaluated before anything is written and reported with the working tree untouched. The invocation itself is well-formed, so apply exits `1`, not `2` (see [Exit codes](#exit-codes)).

`PRODUCT050` is reported by any command that discovers an invalid configuration and stops that invocation before command-specific work. `PRODUCT051` and `PRODUCT052` concern implementation-managed files and are reported only by commands that inspect those files; product-model validation does not inspect managed files.

`PRODUCT060`-`PRODUCT067` are citation and consumer-population diagnostics; see the [Citation Contract](citation-contract.md). `PRODUCT061` is a warning; a repository MAY make warnings fail the command through `validation.warnings-as-errors`. Tools MUST NOT apply per-artifact-type severity defaults: risk policy belongs to the repository, not the kernel.

When more than one citation condition holds, [Citation Contract → Precedence](citation-contract.md#precedence) decides which one is reported, and only that condition's diagnostic is emitted: an embedded projection edited by hand whose cited text has also moved is `PRODUCT062`, never `PRODUCT062` and `PRODUCT061` together.

`PRODUCT070`-`PRODUCT079` is reserved for model-repository resolution ([Conformance → Topologies](conformance.md#topologies)). No code in that band is issued in v0.1: the model-repository pointer's record shape is fixed and its serialization is not, so there is no portable input to check.

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

`PRODUCT101` is mechanically resolvable: an implementation MAY offer a fix operation renaming each file to `<id.toLowerCase()>.md`. The fix operation renames through a temporary name so it also works on case-insensitive filesystems, where a casing-only rename is otherwise a silent no-op. `--dry-run` reports the plan and exits non-zero when anything would change, which makes the dry run usable as a CI gate: `PRODUCT101` is a warning, so it is not otherwise caught unless `validation.warnings-as-errors` is set.

`PRODUCT111` marks recovered knowledge that needs human validation rather than a defect to repair; see [Frontmatter reference → Provenance](frontmatter-reference.md#provenance).

## Emission granularity and attribution

The table below is normative. “Per” fixes diagnostic count: an implementation MUST emit exactly one diagnostic for each described unit and MUST NOT collapse several units into one or expand one unit into several diagnostics. `file` is always present; the remaining columns name fields that MUST be present when that code is emitted. Fields not named MAY be omitted and MUST obey their definitions above if present.

| Code | One diagnostic per | Required attribution beyond `file` |
| --- | --- | --- |
| `PRODUCT001` | unparseable file | none |
| `PRODUCT002` | distinct invalid instance path in a parsed file; multiple failed schema keywords at the same path count once | `field` = instance path |
| `PRODUCT003` | parsed artifact file with an unknown `type` | `field: type` |
| `PRODUCT004` | artifact whose ID prefix and type disagree | `artifact`, `field: id` |
| `PRODUCT005` | occurrence of a duplicated ID after its first occurrence in deterministic file/document order | `artifact` |
| `PRODUCT006`-`PRODUCT008` | authored relationship entry that violates the condition | source `artifact`, `field`, `target` |
| `PRODUCT009` | required body section that is missing or out of order | `artifact`, `field` = section heading |
| `PRODUCT020`-`PRODUCT022` | invalid Product Change operation entry | `change`, operation `field`, `target` |
| `PRODUCT023` | overlay occurrence of a duplicated ID after its first occurrence in deterministic file/document order | `artifact` |
| `PRODUCT024` | relationship entry made dangling by the removal | source `artifact`, `field`, `target` |
| `PRODUCT025` | overlapping target for each Product Change that names it | `change`, operation `field`, `target` |
| `PRODUCT026` | undeclared proposed artifact, or operation entry without its proposed artifact | proposed-file direction: `artifact`; operation direction: `change`, operation `field`, `target` |
| `PRODUCT027` | unresolved ordinary base revision, or changed `modify`/`remove` target | unresolved-revision form: `change`, `field: base-revision`; changed-target form: `change`, operation `field`, `target` |
| `PRODUCT028` | apply invocation against a non-approved change | `change`, `field: status` |
| `PRODUCT042`, `PRODUCT060`-`PRODUCT063` | citation record | cited `target`, plus payload `line` or sidecar `entry` |
| `PRODUCT064` | enumerated current consumer document with no scope declaration | `field: scope` |
| `PRODUCT065` | enumerated current consumer document declared `bound` with no citations | `field: scope` |
| `PRODUCT066` | enumerated current consumer document with one or both invalid-exemption conditions | `field: scope` |
| `PRODUCT067` | malformed payload candidate, malformed sidecar file, sidecar whose consumer is missing, or consumer using both carriers | payload `line` or sidecar `entry` when identifiable; parsed cited `target` when available |
| `PRODUCT050` | invalid configuration file | configuration `field` when it can be parsed |
| `PRODUCT051` | managed file whose bytes differ from its recorded ownership contract | none |
| `PRODUCT052` | expected managed or generated file that is missing | none; `file` is the expected path |
| `PRODUCT101`-`PRODUCT103`, `PRODUCT105`-`PRODUCT107`, `PRODUCT111` | artifact satisfying the warning condition | `artifact` |
| `PRODUCT104` | active relationship entry targeting a deprecated artifact | source `artifact`, `field`, `target` |
| `PRODUCT108` | approved Product Change containing one or more unresolved-question list items | `change`, `field: Open Questions` |

For duplicate detection, “first” is the first occurrence after sorting files by repository-relative POSIX path and, when a file can contain several documents, by one-based document order. The first occurrence is not itself diagnosed; each later occurrence is. Overlay order uses baseline files before proposed files, with each group sorted the same way.

For `PRODUCT025`, each change's overlap set is `operations.modify ∪ operations.remove`. Every target in the intersection of two active changes produces one diagnostic against each involved change. A target shared by three changes therefore produces three diagnostics, not three pairwise duplicates.

`PRODUCT066` is one diagnostic per invalid exempt document even when its reason is empty and it also contains citations. `PRODUCT067` treats a sidecar file as one carrier: multiple structural defects in that file produce one diagnostic, not one per failed schema keyword. A carrier conflict produces one diagnostic against the consumer file and suppresses citation-status diagnostics from both conflicting carriers until the conflict is resolved.

## Exit codes

| Code | Meaning                                                 |
| ---- | ------------------------------------------------------- |
| `0`  | Success; warnings allowed (unless `validation.warnings-as-errors` is `true`) |
| `1`  | Validation or conformance errors                        |
| `2`  | Invalid invocation or configuration                     |
| `3`  | Unexpected internal failure                             |

## Digests

Content digests are SHA-256 over the artifact's raw bytes, with CRLF and CR byte sequences normalized to LF, rendered as `sha256:<lowercase hex>`. The input to the hash is bytes, never decoded text: an implementation MUST NOT decode content before hashing, MUST NOT strip a byte order mark, and MUST hash a byte sequence that is not well-formed UTF-8 exactly as it appears in the file ([RFC 0038](../rfcs/0038-digest-bytes.md)). This normalization is mandatory: digests MUST be identical across operating systems and Git line-ending configurations. Citation digests use the same normalization (see the [Citation Contract](citation-contract.md)).

### What a digest proves

A digest proves byte-identity under the normalization above, and nothing more. It answers one question - is this the same content that was recorded? - and it answers it by recomputation from repository content alone, which is what makes citation statuses, baseline drift detection and the product diff reproducible on every machine ([Determinism requirements](#determinism-requirements), [manifesto](../MANIFESTO.md) principle 10).

A digest is not authentication. It carries no identity, no key and no assertion about who produced the content. A digest recorded alongside the content it covers therefore cannot establish that either one is authentic: whoever can edit the content can recompute the digest in the same commit. Digest comparison detects **drift** - content that moved while a reference to it did not - and it is silent against someone who intended a change to pass unnoticed. This holds for every use of digests in this specification, the `tampered` citation status included: that status names an embedded projection observed to diverge from the canonical text at its recorded digest, not the presence of an attacker ([Citation Contract → Statuses](citation-contract.md#statuses)).

Authority over the accepted Product Definition rests elsewhere by design. A change is approved by a human and accepted when a human merges the pull request carrying it ([Product Changes → Apply](product-changes.md#apply), [manifesto](../MANIFESTO.md) principle 5), and Git history records who changed which files and when. Where a repository needs that authority to be cryptographically verifiable, the mechanisms belong to the version control system and its host - signed commits and tags, protected branches, required reviews - and they apply to a PDaC repository exactly as to any other. This specification neither restates them nor defines a signing format of its own.

### Open directions

Not decisions, and not obligations on any implementation. They are recorded so that the boundary above reads as chosen rather than overlooked; each would need an RFC.

- **A digest over a set of files.** This section defines the digest of one artifact. Anything that fingerprints a group of files - a change directory, a model snapshot, a set of managed files - needs its own construction, including an unambiguous encoding of the paths and digests it covers, so that two implementations agree and no path content can forge an entry boundary. The [DSSE](https://github.com/secure-systems-lab/dsse) pre-authentication encoding is the standard illustration of why such constructions fail in the encoding rather than in the hash.
- **A signed attestation over an accepted change.** If a Product Definition is consumed across a trust boundary - a published definition, citations crossing a repository or an organization, an audit regime that requires non-repudiable evidence of who approved product intent - the object worth signing is the accepted change and the model state it produced, not the individual digests. An existing envelope such as DSSE carrying an [in-toto](https://in-toto.io) predicate would be the starting point, rather than a PDaC-specific format. Signature verification needs a key, a trust root and a revocation policy, none of which are repository content, so a conformance rule resting on them would not satisfy [Determinism requirements](#determinism-requirements) as written.
- **The name of the `tampered` status.** Its condition is well defined and its precedence is deliberate ([Citation Contract → Precedence](citation-contract.md#precedence)). Only the word claims more than the mechanism delivers.

## Determinism requirements

- Artifact discovery, graph compilation, traversal, product diff computation, impact analysis and diagnostic ordering MUST be deterministic and platform-independent.
- Generated outputs (`product-graph.json`, indexes, Mermaid, diagnostics JSON) MUST be byte-identical for identical input content, and `product-graph.json` MUST carry a versioned schema identifier.

Product diff determinism is semantic: the same baseline and applied result MUST yield the same set of impacted artifacts, impact kinds and resulting digests. Byte-identity of the diff report is not required while its serialization remains unfixed ([RFC 0004](../rfcs/0004-delivery-model-reset.md) open question 3).
