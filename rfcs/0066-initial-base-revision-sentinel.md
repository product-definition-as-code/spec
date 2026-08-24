# RFC 0066: Define the CHG-INITIAL base-revision sentinel

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-22
- **Accepted:** 2026-08-24
- **Related:** [juangcarmona/productshape#64](https://github.com/juangcarmona/productshape/issues/64)
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/46>

## Problem

The Product Change schema requires `base-revision` to match `^[0-9a-f]{7,40}$` and describes it as the baseline Git revision against which the change was created. `CHG-INITIAL` establishes a Product Definition where no accepted Product Definition exists yet, so a repository may have no revision that represents its empty baseline.

Every published `CHG-INITIAL` conformance fixture records `base-revision: '0000000'`. The specification never defines that value. An implementation reading only the normative text therefore cannot know whether it is a reserved value, whether it must be resolved through Git, or whether its failure to resolve is `PRODUCT027`.

The ambiguity also hides a second case. An ordinary `base-revision` may be syntactically valid but unavailable in a shallow clone, absent from the repository, or ambiguous. Failing closed with `PRODUCT027` is safe, but calling that failure content drift claims a comparison that never occurred.

## Proposal

Amend the `base-revision` entry in [Frontmatter reference](../spec/frontmatter-reference.md) with this text:

> `base-revision` normally names the Git revision containing the baseline against which a Product Change was created. The exact string `0000000` is the reserved **no-baseline sentinel** when it appears on `CHG-INITIAL`. It records that no Git revision names the empty Product Definition baseline. `CHG-INITIAL` MAY instead name a real Git revision at which the Product Definition baseline is empty.
>
> An implementation MUST recognize only the exact seven-character string `0000000` as the sentinel, and only on `CHG-INITIAL`. It MUST NOT resolve the sentinel against the repository. Other all-zero strings are ordinary revision values, not alternative sentinel encodings.

Amend [Product Changes, Apply](../spec/product-changes.md#apply) so the baseline compatibility rule reads:

> Apply MUST check baseline compatibility before writing. For `CHG-INITIAL` carrying the no-baseline sentinel, apply MUST skip repository resolution and baseline drift comparison, and MUST NOT emit `PRODUCT027` merely because the sentinel does not resolve.
>
> For every ordinary `base-revision`, apply MUST first resolve the value to exactly one commit. If it cannot, apply MUST fail with `PRODUCT027` and leave the working tree untouched. If it resolves, every artifact named in `operations.modify` or `operations.remove` is compared by content digest as specified below. A digest difference is also `PRODUCT027`. Diagnostic messages remain implementation-defined. An unresolved revision and a resolved revision whose artifact content changed are distinct causes of the same code.

The exception is selected by the pair `id: CHG-INITIAL` and `base-revision: '0000000'`. A non-initial Product Change carrying the same string receives no exception. At apply it follows the ordinary resolution rule and fails with `PRODUCT027` if the value cannot resolve.

Amend `base-revision` in the normative Product Change JSON Schema so its description states the same exception:

> The baseline Git revision this change was created against. The exact string `0000000` is the no-baseline sentinel only for `CHG-INITIAL`.

The schema's string shape and `gitRevision` reference do not change. The conditional semantics depend on the pair of fields and remain in the normative prose; the schema description must not continue to imply that the sentinel names a Git revision.

## Impact

- **On existing conformant repositories:** no repository needs an edit. Existing `CHG-INITIAL` fixtures already use the exact sentinel. A `CHG-INITIAL` that names a real commit containing an empty model remains valid. Validation-only fixtures for later changes may remain plain file fixtures, but the sentinel gives them no special apply behaviour.
- **On existing implementations:** no conforming behaviour changes. Implementations gain one explicit branch before repository resolution. An unavailable ordinary revision continues to fail closed with `PRODUCT027`; the diagnostic no longer needs to imply that a digest comparison occurred. Implementations that publish or copy the normative Product Change schema update its `base-revision` description.
- **On the conformance tests:** add `apply-initial-sentinel`, which applies an approved, add-only `CHG-INITIAL` carrying `0000000` and asserts no `PRODUCT027`. Add `apply-base-revision-unresolved`, which uses a non-initial change and asserts `PRODUCT027`, exit `1`, and an untouched working tree. These cases land with the planned apply-invocation case format because the current flat fixture format cannot observe apply, exit status, or repository history.

## Alternatives considered

**Allow any 7 to 40 character all-zero string.** Rejected. It creates 34 equivalent serializations and makes implementations disagree over which values receive sentinel behaviour.

**Require the sentinel on every `CHG-INITIAL`.** Rejected. A repository may already have a real commit at which the configured Product Definition is empty. That commit is a precise and useful baseline reference, so forbidding it adds no safety.

**Omit `base-revision` or use `null` on `CHG-INITIAL`.** Rejected for v0.1. It changes the closed schema and requires every parser and fixture to support a second field shape when one reserved string already exists in every published fixture.

**Use Git's empty-tree object ID.** Rejected. It is an object identifier, not a repository commit, its hash depends on the repository object format, and resolving it says nothing about the configured Product Definition root.

## Decision record

Accepted 2026-08-24 by the founding maintainer as a determination under [CONTRIBUTING.md](../CONTRIBUTING.md). It fixes undefined behaviour already represented by every published `CHG-INITIAL` fixture and requires no accepted repository or conforming implementation to change behaviour. The exact seven-character sentinel, its restriction to `CHG-INITIAL`, the fail-closed treatment of every ordinary unresolved revision and the deferred apply fixtures bound the decision without adding another field shape.

No substantive objection was raised. The fixed 72-hour minimum is suspended by the founder-led stabilization exception recorded in [Governance](../GOVERNANCE.md); publication, an explicit decision and rationale, and resolution of substantive feedback still apply.
