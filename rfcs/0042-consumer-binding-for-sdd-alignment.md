# RFC 0042: Consumer binding for SDD alignment and drift review

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-16
- **Accepted:** 2026-08-24
- **Class:** change
- **Target:** PDaC v0.2.0
- **PR:** <https://github.com/product-definition-as-code/spec/pull/42>
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/41>
- **Public comment:** seven days; completed 2026-08-23 15:59 UTC
- **Reference implementation:** <https://github.com/juangcarmona/productshape/issues/82>

## Problem

The [Citation Contract](../spec/citation-contract.md) already defines a machine-verifiable reference from an SDD specification or another consumer document to canonical product text. It also defines the deterministic states `current`, `stale`, `tampered` and `unresolved`.

That contract verifies only the citations it discovers. It does not define the population of consumer documents that was expected to contain citations. An SDD workspace may therefore contain product-bearing specifications that were never checked while a verifier reports success after discovering zero citations. The individual records are valid, but the integration has not established that it inspected the relevant surface.

The inverse overclaim is equally dangerous. A `current` citation proves that one recorded dependency still resolves at the recorded digest. It does not prove that every product-semantic statement has the right citation, that the specification covers all relevant product intent, or that the implementation satisfies either document.

SDD specifications are already the leading example in the Citation Contract and the specification index, but the complete use case remains implicit. An implementation can consequently reduce citations to link linting or claim semantic alignment that deterministic verification cannot establish.

The missing contract is not another delivery lifecycle. It is a bounded way for an integration to say which native consumer documents it inspected, which ones are bound to the Product Definition, which ones are deliberately outside that binding, and whether any recorded dependency moved.

## Proposal

### Primary use case

The specification will identify **SDD specification grounding and drift review** as a primary use case of the PDaC kernel:

> A delivery specification binds its product-semantic claims to the accepted Product Definition through citations. A consumer integration accounts for the current native documents in its framework and verifies their recorded dependencies whenever either side changes. PDaC makes possible drift visible and requires review; it does not prove semantic completeness, rewrite either side or own delivery.

This use case applies to SDD frameworks first because their specifications sit directly between accepted product intent and implementation. The contract is expressed for consumer integrations generally and does not name a particular framework.

### Conditional consumer-integration contract

A conforming PDaC implementation MAY provide no SDD or consumer-framework integration. Core repository and implementation conformance remain available without one.

When an implementation provides a consumer integration and claims population-aware PDaC verification for it, that integration MUST satisfy this RFC. The integration MUST NOT change the citation record or status semantics, which remain framework-independent.

A **consumer integration** is an adapter that knows how an external framework organises its own documents while leaving that framework in native ownership of them.

A **consumer-document population** is the deterministic set of current native documents that the integration says are subject to classification. The integration:

- MUST define and document its enumeration rule;
- MUST enumerate the same population for identical repository content and integration configuration;
- MUST distinguish current documents from archived or historical documents when the framework has that distinction;
- MUST exclude archived or historical documents by default;
- MAY expose an explicit mode that includes archived or historical documents;
- MUST report its provider identity and integration version with machine-readable results.

Framework-specific paths, lifecycle concepts and document formats belong to the adapter and MUST NOT enter the PDaC product model.

### Scope declaration

Every document in the current consumer-document population MUST carry or be associated with exactly one explicit scope declaration:

| Value | Meaning |
| --- | --- |
| `bound` | The document contains product-semantic claims that depend on the Product Definition and carries citations to the canonical text on which those claims depend. |
| `exempt` | The document contains no product-semantic dependency that requires binding. The declaration carries a non-empty reason. |

The specification fixes these semantics, not the serialization or location of the declaration. An integration MAY use native frontmatter, an inline marker, a sidecar or framework configuration, provided the declaration remains inspectable as repository data without executing code.

A document with no declaration is **unclassified**. A tool MUST NOT infer `exempt` from the absence of citations, from a file name, from generated content or from an AI assessment.

A `bound` document MUST carry at least one citation. This is an emptiness guard, not a completeness claim: the tool cannot deterministically prove that every product-semantic statement has been cited.

An `exempt` declaration MUST carry a non-empty reason and MUST NOT coexist with a citation in the same document. A tool MUST NOT create, renew or silently introduce an exemption on the user's behalf. A human-triggered operation MAY write the explicit declaration requested by that human.

### Population-aware verification

Population-aware verification MUST account for every document in the enumerated population before reporting success:

1. An unclassified current document is an error.
2. A bound document with no citations is an error.
3. An invalid exemption is an error.
4. Every citation in a bound document is evaluated under the existing Citation Contract and its existing precedence.
5. A valid exempt document passes scope verification and remains visible in results.
6. Zero discovered citations MUST NOT produce success when the population contains a bound or unclassified current document.

Text and machine-readable results MUST report:

- provider identity and integration version;
- total current documents;
- document totals by `bound`, `exempt` and `unclassified`;
- citation totals by `current`, `stale`, `tampered` and `unresolved`;
- the repository-relative path and applicable declaration or diagnostic for each non-passing document.

Results and diagnostics MUST follow the deterministic ordering rules in [Validation](../spec/validation.md).

The following stable error diagnostics are added:

| Code | Condition |
| --- | --- |
| `PRODUCT064` | Expected current consumer document has no scope declaration. |
| `PRODUCT065` | Consumer document declares `bound` but contains no citations. |
| `PRODUCT066` | Invalid exemption: its reason is empty or the exempt document contains a citation. |

These errors apply only during population-aware consumer verification. Plain citation verification over an explicitly supplied document or directory remains valid and continues to verify the citations it discovers without claiming population coverage.

### What the result establishes

A successful population-aware verification establishes only that:

- the integration accounted for its declared current consumer-document population;
- every document was explicitly bound or exempt;
- every bound document carried at least one citation;
- every recorded citation was evaluated under the Citation Contract;
- no embedded projection was accepted after independent editing;
- no document was silently treated as outside the Product Definition.

It does not establish that:

- every product-semantic statement has the right citation;
- all relevant product intent is covered;
- the consumer document contains no semantic contradiction;
- the implementation satisfies the consumer document or Product Definition.

Tools MAY flag suspected omissions or contradictions for human review. Those findings remain non-normative and MUST NOT be represented as deterministic PDaC conformance results.

### Review and correction

A stale citation means the consumer document requires review against the current Product Definition. A tool MUST NOT renew the recorded digest, rewrite consumer text or change the canonical Product Definition automatically.

After review:

- when the accepted Product Definition remains correct, the consumer owner revises the document where necessary and deliberately records a citation to the reviewed canonical text;
- when delivery work exposes an incorrect or incomplete product assumption, the consumer MAY propose a [Product Change](../spec/product-changes.md);
- acceptance of any Product Change remains a human decision.

The consumer framework retains native ownership of its specifications, design, tasks, implementation and verification lifecycle. Population-aware verification adds no PDaC-owned delivery state.

## Conformance cases

The conformance suite will add a framework-neutral fixture adapter or equivalent harness that supplies an explicit consumer-document population. It will cover:

1. one bound current document with a current citation;
2. the same document becoming stale after cited canonical content changes;
3. unresolved and tampered citations retaining their existing status and precedence;
4. a current document with no scope declaration reporting `PRODUCT064`;
5. a bound document with no citations reporting `PRODUCT065`;
6. exemptions with an empty reason or a citation reporting `PRODUCT066`;
7. a valid exemption passing while remaining visible in results;
8. current and archived documents, with archived documents excluded by default and included only explicitly;
9. a negative control proving that a populated workspace cannot pass through zero citation discovery;
10. deterministic text and machine-readable ordering.

The fixture harness is conformance infrastructure, not a mandated production adapter or declaration serialization.

## Impact

- **On existing conformant repositories:** none unless they opt into population-aware consumer verification. A repository using citations without an integration remains conformant under the existing Citation Contract. A repository that adopts the new capability must classify the current documents enumerated by its adapter.
- **On existing implementations:** the core citation resolver and four citation statuses do not change. Implementations may omit adapters. An adapter that claims the new capability must enumerate and classify its population, issue `PRODUCT064`–`PRODUCT066`, and report document as well as citation coverage.
- **On existing integrations:** experimental integrations such as ProductShape's OpenSpec adapter gain an enforceable second layer. Instructional configuration remains advisory; population-aware verification supplies the deterministic gate.
- **On conformance tests:** add the ten cases above and extend machine-readable result assertions. Existing citation fixtures remain valid.
- **On versioning:** this adds normative obligations and diagnostics, so it targets PDaC v0.2.0 rather than changing v0.1.0 in place.

## Alternatives considered

### Verify only discovered citations

Rejected. It validates individual records but cannot distinguish “there are no dependencies” from “the integration failed to find the documents or citations”. Zero discovery can pass vacuously.

### Require every consumer document to be bound

Rejected. SDD frameworks contain designs, notes and administrative documents that may legitimately have no product-semantic dependency. Forcing meaningless citations would create noise and teach users to cite arbitrarily.

### Infer exemptions automatically

Rejected. Missing citations are exactly the failure being guarded against. Treating absence as exemption reproduces the false green under another name. AI inference is also non-deterministic and cannot carry human accountability.

### Make semantic alignment an automated conformance claim

Rejected. Citation currentness and population coverage are mechanically testable; completeness and contradiction are semantic judgements. Collapsing them would make PDaC claim more than its evidence establishes.

### Define an OpenSpec-specific contract

Rejected. OpenSpec is the first reference integration, not part of the PDaC model. Coupling normative text to one framework would violate implementation independence and shorten the life of the product knowledge to the life of a delivery tool.

### Keep the use case non-normative

Rejected. The core failure is false success caused by an unaccounted document population. Preventing it requires testable obligations and diagnostics, not only explanatory guidance.

## Out of scope

- A mandatory SDD framework or adapter.
- A mandated serialization or location for scope declarations.
- Semantic completeness or contradiction proof.
- AI as a deterministic verifier.
- Automatic propagation between the Product Definition and consumer documents.
- Implementation, deployment or runtime verification claims.
- Cross-repository citation resolution.

## RFC classification and decision record

This RFC is a **change** under [CONTRIBUTING.md](../CONTRIBUTING.md): it adds obligations and diagnostics only for implementations claiming population-aware consumer verification. Its seven-day public comment window completed on 2026-08-23.

Accepted 2026-08-24 by the founding maintainer. No maintainer objected and no substantive public feedback remained unresolved. The accepted decision uses `bound` and accountable `exempt` declarations because they are the smallest deterministic scope model that distinguishes an intentionally out-of-scope document from a document an integration silently missed. The contract remains conditional, framework-neutral and serialization-neutral; it does not make an integration mandatory, change citation status semantics or claim semantic completeness.

The follow-up normative specification and conformance changes remain separate from this RFC acceptance and target PDaC v0.2.0.
