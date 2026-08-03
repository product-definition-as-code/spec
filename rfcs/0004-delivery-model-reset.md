# RFC 0004: Delivery-model reset: accepted intent, change as PR, and the citation contract

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-03
- **Supersedes:** #1 (baseline lock file), #3 (implementation claims, applicability contracts and reconciliation states)
- **Related:** #2 (deployment topologies — remains open; scopes where cited models live and how cross-repository citations resolve)
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/4>

## Problem

The gap PDaC exists to close is re-statement: every time product knowledge is re-expressed in
natural language (in a spec, a task, a prompt, a document), it can mutate without anyone noticing.
The current specification answers this with a push pipeline (Product Change, Delivery Slice,
Product Handoff) that itself re-states knowledge into new containers, and self-hosted use has shown
the pipeline does not hold:

1. **No conforming greenfield path.** The initial baseline is authored without a Product Change
   ([`product-changes.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/product-changes.md), bootstrap exception), but every Delivery Slice must live inside a Product
   Change ([`delivery-slices.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/delivery-slices.md)) and every handoff must start from an approved slice
   ([`handoff-contract.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/handoff-contract.md), generation rule 1). There is no conforming way to deliver the initial
   baseline.
2. **Vacuous promotion gates.** Promotion rules 2 and 3 ([`product-changes.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/product-changes.md)) are satisfied
   vacuously by a change with zero slices: no slices to complete, no requirements to evidence. An
   implemented change can be promoted with no delivery evidence at all.
3. **Scope loss.** A slice declares per-requirement `coverage` and `scope`, but the handoff
   `implements[]` carries bare IDs ([`frontmatter-reference.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/frontmatter-reference.md)). Partial scope is flattened before
   it reaches any consumer, and promotion unions requirement IDs.
4. **Unbounded context.** The closure rule has no budget. Real generated contexts have exceeded
   16,000 words for a single slice, which contradicts "exactly the product subgraph that increment
   needs".
5. **Reimplemented Git.** `base-revision`, `operations.add/modify/remove`, overlay validation,
   rebase-on-conflict and promotion are a branch, a diff, conflict detection and a merge, rebuilt
   as bespoke artifacts with their own lifecycle vocabulary that no adopter natively speaks.

Marking these chapters `experimental` would not close the re-statement gap. This RFC replaces the
push pipeline with two smaller contracts built on the parts of the specification that have survived
scrutiny: stable identity, typed relationships, deterministic validation and content digests.

## Proposal

### 1. Change-as-PR

- The baseline is the canonical product model on the repository's canonical branch. Normatively:
  the baseline is the accepted product intent; acceptance and implementation are distinct facts.
- `Product Change` ceases to be a normative PDaC artifact. The term now names the repository's
  native mechanism: a branch, a review, a merge (a pull request or the host's equivalent). There is
  no `change.md`, no `operations` frontmatter, no change lifecycle and no `CHG-` artifact. The
  `CHG-`, `SLI-` and `HOF-` prefixes are retired and, per [`identifiers.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/identifiers.md), never reused.
- Validation of a proposal is full structural validation of the proposed tree. This replaces
  overlay validation; the overlay is the branch.
- Tooling MUST NOT merge a proposal that fails structural validation (CI gate).
- Merging is a human decision. Tools MUST NOT merge, auto-approve or self-merge model changes.
- The bootstrap exception is deleted. The initial baseline enters through the same mechanism as
  every later change: a reviewed merge into an empty model.
- Consumers of the model MUST NOT write to it. A consumer MAY propose a revision (a PR) when
  implementation reveals a contradiction; a human decides. This is the mechanism of manifesto
  principle 9.

### 2. Citation contract

A citation is a machine-verifiable reference from any consumer document (an SDD spec, a task, an
agent prompt file, a design doc) to canonical product text.

- A citation is a record, not a block of text: target artifact `id`, content `digest` (per
  `validation.md`, LF-normalized SHA-256), and an optional `anchor`. It MAY exist as a structured
  reference inline, or in a machine-readable ledger or sidecar accompanying the consumer document.
- An anchor addresses a required body section by its heading slug, or a verification scenario by its
  stable id (see 3).
- Embedding is a projection of a citation, not its definition. A consumer MAY additionally embed
  the cited canonical text; when it does, the embedded block MUST be delimited by machine-readable
  markers carrying the citation record, MUST be byte-identical to the canonical text at the recorded
  digest, and MUST be treated as read-only and regenerable.
- A conforming tool MUST compute, deterministically, one status per citation:

  | Status | Meaning |
  | --- | --- |
  | `current` | Target resolves and its recomputed digest matches. |
  | `stale` | Target resolves; canonical content changed since citation. |
  | `tampered` | Only for embedded projections: the block differs from canonical content at the recorded digest. |
  | `unresolved` | Target id or anchor does not resolve. |

- Diagnostics: `PRODUCT060` unresolved citation (error), `PRODUCT061` stale citation (warning; a
  repository MAY escalate via its existing `warnings-as-errors` configuration, and tools MUST NOT
  apply per-artifact-type severity defaults: risk policy belongs to the repository, not the
  kernel), `PRODUCT062` tampered embedded projection (error), `PRODUCT063` anchor not found
  (error).
- Semantic contradiction between a citation and its surrounding text is explicitly non-normative:
  tools MAY flag suspected contradictions for human review; such findings are never a conformance
  criterion. Deterministic tools enforce structure, AI does semantic work, humans decide (manifesto
  principle 7).

### 3. Addressable verification scenarios

`verification[]` entries on Functional and Quality Requirements gain an optional stable `id`
(`[A-Z0-9-]+`, unique within the artifact). When present, the scenario is citable via anchor. This
makes partial scope expressible as a set of cited scenario ids instead of prose, and it is the only
schema change this RFC requires.

### 4. Retired and subsumed text

- Chapters removed from the normative spec: [`product-changes.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/product-changes.md), [`delivery-slices.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/delivery-slices.md). This
  retires the Delivery Slice artifact, not slicing: PDaC does not own delivery decomposition.
  Consumers may slice work however their process demands; PDaC only provides accepted intent and
  verifiable citations to the product model.
- [`handoff-contract.md`](https://github.com/product-definition-as-code/spec/blob/8595c9f/spec/handoff-contract.md) is replaced by the citation contract. A "handoff" remains available as a
  non-normative convenience: a generated document composed entirely of citations, with a stated size
  budget.
- Diagnostics retired, not deprecated: `PRODUCT020`–`PRODUCT027`, `PRODUCT030`–`PRODUCT032`,
  `PRODUCT040`–`PRODUCT041`, `PRODUCT043`–`PRODUCT044`, `PRODUCT108`–`PRODUCT110`. Retired codes
  are never reused, mirroring the ID immutability rule. `PRODUCT042` is generalized to citation
  digests.
- Terminology and manifesto wording updated accordingly: `terminology.md` "implemented and
  accepted" becomes "accepted"; principle 5 becomes "The baseline changes through exactly one
  operation: a human merging a validated proposed revision. Everything else is a proposal."

### Acceptance scenarios

Every clause above must be demonstrable through these six scenarios, which become conformance
fixtures:

1. **Greenfield first increment.** Empty model; a PR adds Product actors, two rules, one FR with
   scenario ids; merge; an SDD spec cites `FR-X#S1` and `BR-Y`; all citations `current`;
   implementation proceeds. No change container was ever created.
2. **Intent changes mid-flight.** A rule cited by an open SDD spec is amended on the canonical
   branch; the spec's citation reports `stale` in CI; a human updates or contests the spec. Nothing
   silent.
3. **Partial scope without loss.** A spec cites scenarios `S1` and `S2` of a five-scenario FR;
   coverage claims are checked against exactly those anchors; `S3`–`S5` remain visibly uncited.
4. **Work over existing baseline.** A spec cites baseline requirements directly, with no
   product-model change at all.
5. **Bug or refactor.** No model PR; the fix's spec cites the governing rule; citation verifies
   `current`; the model is untouched.
6. **Brownfield recovery.** Recovered draft artifacts with `provenance` enter through PRs;
   contradictory candidates collide in review, not in the baseline; `PRODUCT111` still derives the
   human-validation queue.

## Impact

- **On existing conformant repositories:** `docs/product/model/**` is untouched.
  `docs/product/changes/**` leaves the conformance surface; in-flight changes are finished as PRs
  or archived. Repositories not using Git-hosted review must provide an equivalent human-gated
  merge; PDaC already assumes Git (digests, history-as-authorship).
- **On existing implementations (ProductShape):** retire `change`, `slice`, `promote` and handoff
  generation; keep parser, graph, validation and digests unchanged; add `cite` (emit citation
  blocks) and `citations verify` (compute statuses). The retired code was the prototype that located
  the real problem.
- **On the conformance corpus:** drop change/slice/handoff fixtures (none existed); add one fixture
  per citation status, scenario-id addressing, and the six acceptance scenarios.

## Alternatives considered

- **Mark the workflow chapters `experimental`.** Honest, but closes nothing: the re-statement gap
  remains and adopters still learn a vocabulary nobody speaks.
- **Repair the handoff in place (scope fields, closure budget).** Keeps the push model; every
  handoff is still a re-statement surface and a second thing to keep in sync.
- **`implementation-status` on requirements.** Rejected: conflates intent validity, work state,
  satisfaction and deployment, which have four different owners.
- **Adopt RFC #3 as filed.** Turns PDaC into a delivery control plane; the manifesto forswears it.
  Only the obligation-realization-evidence relation is worth keeping, and it composes naturally
  with citations.

## Open questions (for the comment window)

1. Concrete citation forms per host format (inline structured reference, Markdown marker block, YAML
   sidecar ledger). The pilot will exercise all three; the follow-up normalizes.
2. Section-slug anchors and non-ASCII headings: do we need canonicalization rules, or do we restrict
   anchors to verification-scenario ids and skip the problem? **v0.1 decision:** restrict to
   scenario ids; section-slug anchors deferred to a follow-up.
