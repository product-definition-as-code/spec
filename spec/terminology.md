# Terminology

Definitions used normatively throughout this specification.

**Product Artifact.** An independently addressable unit of product knowledge with a stable immutable ID: an Actor, Journey, Use Case, Business Rule, Domain Term, Bounded Context, Functional Requirement, Quality Requirement, Constraint or Structured Behaviour.

**Product Definition (Baseline).** The accepted, versioned and validated graph of product artifacts under `docs/product/model`. It describes the product as currently defined, including behaviour that is accepted. The Product Definition is the accepted product intent on the repository's canonical branch; acceptance and implementation are distinct facts. Also called the _baseline_ when a Product Change is validated against it.

**Model repository.** The git repository holding the Product Definition, as files under the configured product root. It MAY also hold the software the definition describes (co-located topology) or hold the definition alone (dedicated topology); both conform, and co-location is the default when one repository serves the product. A model repository holds one Product Definition. See [Conformance → Topologies](conformance.md#topologies).

**Accepted.** A product artifact is accepted when it has been merged into the canonical branch by a human through a reviewed merge. Acceptance is a fact about the model, not about implementation: an accepted artifact may be unimplemented, and an implemented artifact that was never merged is not part of the Product Definition.

**Product Change.** An explicit, versioned semantic delta against the baseline: additions, modifications and removals, each represented by complete proposed future-state artifacts, plus rationale and open questions. Stored under `docs/product/changes/`. A Product Change is reviewed and accepted through a pull request, but it is not a pull request, a delivery container or an implementation state. See [Product Changes](product-changes.md).

**Overlay.** The virtual product model obtained by applying a Product Change's operations to the baseline without modifying baseline files. Validation of a Product Change compiles and validates the overlay.

**Apply.** The explicit, human-triggered operation that materializes an approved Product Change: it writes the change's operations into the proposal's model files, computes the product diff, validates the resulting model, and archives the change. Apply never merges and never commits, and it does not accept the change: the accepted Product Definition changes only when a human merges the pull request carrying the applied result.

**Product diff.** The difference between the baseline and the result of applying a Product Change: the set of artifacts that effectively changed, the kind of impact on each, and the resulting digest of each artifact added or modified. The diff is authoritative for what changed; the change's `operations` are authoritative for what was intended. Impact is computed from the diff and the citation index.

**Proposal.** The branch bearing an applied Product Change, offered for review as a pull request. The proposed tree is validated in full before merge.

**Citation.** A machine-verifiable reference from a consumer document to canonical product text: the target artifact's `id`, the content `digest` of the cited canonical text, and an optional `anchor` addressing a verification scenario by its stable `id`. See the [Citation Contract](citation-contract.md).

**Verification entry.** An entry of a Functional or Quality Requirement's `verification` list. It is exactly one inline verification scenario or one `scenario-ref` to a Structured Behaviour. PDaC does not own the verification workflow: turning an inline scenario or referenced Structured Behaviour into an executable test, running it and judging the evidence it produces belong to the delivery process ([Citation Contract → Delivery boundary](citation-contract.md#delivery-boundary)).

**Verification scenario.** The inline form of a verification entry, carrying `scenario` and an optional stable local `id`. It is a product-level acceptance criterion expressed as something observably true of the product rather than of any implementation. Its local `id` is an anchor within the containing Requirement, not an independent Product Artifact ID ([Citation Contract → Anchors](citation-contract.md#anchors)).

**Scenario reference.** The reference form of a verification entry, carrying exactly one `scenario-ref` whose value is a Structured Behaviour ID. It authors the Requirement-to-Structured-Behaviour relationship and does not create an anchor within the Requirement.

**Structured Behaviour.** A Product Artifact containing one concrete, implementation-independent example of accepted observable product behaviour, separated into optional context, one stimulus and one or more expected outcomes. It has independent identity, lifecycle, provenance, Product Change history and whole-artifact citation.

**Product Graph.** The derived directed graph whose nodes are product artifacts and whose typed edges are the canonical relationships declared in artifact frontmatter, together with derived reverse indexes. The graph is always compiled from the canonical files and is never authored.

**Canonical / Derived / Generated.** _Canonical_ files are authored by humans (possibly assisted by AI) and are the source of truth. _Derived_ or _generated_ files are produced by tooling from canonical files, are reproducible, and MUST NOT be edited by hand.

**Managed File.** A generated provider-integration file carrying a managed-file header. Managed files are regenerated by the implementation and checked for manual modification. Management covers absence as well as presence: the implementation removes a managed file that the current assets and configuration no longer produce, provided the file's content still matches what was recorded for it.

**Provenance.** The evidence behind a recovered claim: where the knowledge came from, how strongly that source supports it, and how it was recovered. Provenance is an epistemic property of an artifact's content, not a record of authorship - Git history remains the record of who changed what and when - and it is set only on artifacts recovered from an existing system. See the [Frontmatter reference](frontmatter-reference.md#provenance).

**SDD (Spec-Driven Development) framework.** A framework such as OpenSpec that owns the specification, design, task and verification workflow for one implementation increment. SDD frameworks consume canonical product knowledge through citations; they do not own canonical product semantics.

**Structural impact.** The set of artifacts reachable from a given artifact through graph edges within a stated direction and depth. Structural impact is deterministic and makes no semantic claim.

**Diagnostic.** A machine-readable validation finding with severity, stable code, message, source file and, when available, artifact ID, field and target ID.
