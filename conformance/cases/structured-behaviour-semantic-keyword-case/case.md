# Case: structured-behaviour-semantic-keyword-case

**Verifies:** the ban on leading notation keywords in Structured Behaviour clauses is case-insensitive and word-bounded: a `given` entry opening with `Given` emits one `PRODUCT002`, while a `then` entry opening with `Givens` emits none.

**Spec references:**

- [Artifacts](../../../spec/artifacts.md#structured-behaviour-structured-behaviour-sb-) - the prohibition is case-insensitive and applies only to a complete leading word.

## Why this case exists

`structured-behaviour-semantic-keyword` covers the upper-case spelling only. An implementation matching `^(GIVEN|WHEN|THEN|AND)\b` passes it while accepting `Given a context exists`, which is the spelling an author transcribing an existing scenario actually writes. An implementation matching the keywords without a word boundary also passes it while wrongly rejecting `Givens are recorded`. This case pins both edges of the rule so neither implementation conforms.

## Expected

Exactly one `PRODUCT002`, attributed to `SB-KEYWORD-CASE`, for the mixed-case `given` entry. The single-diagnostic expectation is what proves the `then` entry accepted: an implementation that also rejects `Givens are recorded` emits a second `PRODUCT002` and fails. The fixture asserts `PRODUCT002` without fixing the instance-path notation.
