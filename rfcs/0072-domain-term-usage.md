# RFC 0072: Domain-term usage from semantic artifacts

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-24
- **Proposed target:** PDaC specification 0.2.0; additive `v1alpha1` schema evolution

## Problem

[`uses-terms`](../spec/relationships.md#canonical-vocabulary) can currently be authored only by a Use Case or Structured Behaviour. That is narrower than the meaning of the `PRODUCT106` warning, "Domain term with no usage", and narrower than the product knowledge the graph is meant to preserve.

A real adoption exposed the mismatch. `TERM-MINOR-UNITS` is needed to interpret a Business Rule that defines deterministic rounding, a Quality Requirement that requires integer money arithmetic, and another Domain Term whose definition depends on minor units. None can author the edge. A conforming implementation therefore reports the term as unused even though several artifacts substantively use it. The warning is a false positive relative to its plain-language claim, and graph inspection, impact analysis and generated projections all lose the same dependencies.

Prose mentions cannot repair this. They are not typed references, and treating them as edges would make validation dependent on natural-language matching. Nor does a path such as Use Case → Business Rule → Domain Term express the missing fact: `Use Case.governed-by` says that a rule governs behaviour; `Business Rule.uses-terms` says that interpreting the rule requires the term. Each edge carries a different fact and neither implies the other.

## Proposal

### Semantics and canonical direction

`uses-terms` is an authored relationship declaring that understanding or interpreting the source artifact requires the referenced Domain Term.

It MUST be authored in the canonical direction from the consuming artifact to one or more Domain Terms. Its only allowed target type is `domain-term`. “Used by” and all other reverse views MUST be derived and MUST NOT be authored.

The canonical relationship vocabulary adds `uses-terms` rows for these sources:

| Source | Field | Allowed targets |
| --- | --- | --- |
| Use Case | `uses-terms` | Domain Term |
| Structured Behaviour | `uses-terms` | Domain Term |
| Business Rule | `uses-terms` | Domain Term |
| Domain Term | `uses-terms` | Domain Term |
| Functional Requirement | `uses-terms` | Domain Term |
| Quality Requirement | `uses-terms` | Domain Term |
| Constraint | `uses-terms` | Domain Term |

The Use Case and Structured Behaviour rows are unchanged. The other five are added. Actors, Journeys and Bounded Contexts do not gain the field in this RFC. This RFC does not establish a distinct direct-dependency meaning for a participant, an end-to-end path or a language boundary, separate from the semantic artifacts they connect. In particular, treating a Bounded Context's owned language as usage would make `PRODUCT106` self-suppressing: `owns-terms` remains derived solely from `Domain Term.defined-in`. A later RFC MAY add one of these sources only with a concrete example and a reason that the existing semantic edges cannot express it. Product Changes do not gain the field because they are workflow records rather than Product Artifacts.

Domain Term → Domain Term is included as a definitional dependency. The same semantics apply without ambiguity: understanding one definition may require another named term. This RFC does not prohibit cycles between Domain Terms. Detecting a circular definition is a separate semantic rule requiring its own justification; a cycle is not an invalid reference merely because this edge makes it representable.

### Artifact contracts and schemas

Business Rule, Domain Term, Functional Requirement, Quality Requirement and Constraint gain optional `uses-terms` frontmatter. The artifact chapter and frontmatter reference describe it as a list of Domain Term IDs.

Each corresponding closed JSON Schema gains an optional `uses-terms` property:

```json
"uses-terms": {
  "type": "array",
  "items": {
    "$ref": "urn:product-definition-as-code:schema:common:v1alpha1#/$defs/domainTermId"
  }
}
```

This deliberately matches the existing Use Case schema. It reuses `domainTermId`, preserves `additionalProperties: false`, and introduces no new required property. Existing conformant documents therefore remain valid. As with existing relationship arrays, the schema does not add `minItems`, `uniqueItems` or an ordering rule; this RFC does not silently strengthen those common conventions for one field.

### Unused-term validation

`PRODUCT106` means: a Domain Term has no incoming canonical `uses-terms` relationship from any artifact type permitted to author that relationship.

An implementation MUST evaluate incoming edges from Use Cases, Structured Behaviours, Business Rules, Domain Terms, Functional Requirements, Quality Requirements and Constraints. A prose occurrence of a term ID or title MUST NOT count as structural usage. `defined-in`, generated reverse relationships and paths through other relationship types do not count as `uses-terms` edges.

The diagnostic wording becomes “Domain term with no incoming `uses-terms` relationship” so it states exactly what the graph checks.

### Documentation and examples

The normative examples add:

```yaml
# Business Rule
uses-terms: [TERM-MINOR-UNITS]
```

```yaml
# Quality Requirement
uses-terms: [TERM-MINOR-UNITS]
```

```yaml
# Domain Term definition
uses-terms: [TERM-MINOR-UNITS]
```

The relationship chapter will explain both the direct-edge distinction above and the single canonical direction. Generated schema and frontmatter references MUST be regenerated through the repository's documented generation workflow when one exists; generated output MUST NOT be edited as an independent source of truth.

### Conformance

The follow-up specification change adds valid fixtures with `uses-terms` on each newly permitted source: Business Rule, Domain Term, Functional Requirement, Quality Requirement and Constraint. Alongside the existing Use Case and Structured Behaviour coverage, the fixtures demonstrate that each permitted source edge resolves and prevents `PRODUCT106` for its target.

Negative coverage adds:

- a syntactically term-shaped `uses-terms` reference that is unresolved, producing the existing unknown-reference diagnostic;
- a `uses-terms` value targeting an existing non-Domain-Term artifact, producing the existing wrong-target-type diagnostic; and
- a Domain Term mentioned only in prose, still producing `PRODUCT106`.

Where the conformance output records graph or reachability projections, expected results add the new canonical edges and their effect on undirected reachability. No new diagnostic code is required: generic reference validation applies once the vocabulary and schemas admit the field, while `PRODUCT106` changes which incoming edges it considers.

## Impact

- **On existing conformant repositories:** none. Every new field is optional and existing `uses-terms` documents retain their meaning.
- **On existing implementations:** graph relationship declarations, five artifact schemas, reference validation dispatch, `PRODUCT106`, authored templates, graph projections and tests must recognize all seven permitted source kinds. Generic reference machinery may be reused, but implementations cannot claim the change needs no validation work.
- **On the conformance tests:** valid coverage is added for all five new sources, plus unresolved, wrong-target and prose-only negative coverage and graph expectations where supported.
- **On generated documentation:** artifact/frontmatter/schema references and examples are regenerated by the official workflow after their canonical sources change.

## Downstream implementation note

ProductShape should track this RFC in a separate downstream change. It must add optional `uses-terms` to the Business Rule, Domain Term, Functional Requirement, Quality Requirement and Constraint schemas; register the five source-to-Domain-Term graph relationships; make `PRODUCT106` inspect incoming canonical `uses-terms` edges from all seven permitted source kinds; expose the field in the corresponding authoring templates; update reference-target validation and graph projections; and add valid, unresolved, wrong-target, prose-only and term-to-term tests. ProductShape is not modified by this specification RFC.

## Alternatives considered

**Keep `uses-terms` on Use Cases only and infer usage through graph traversal.** Rejected. Traversal connects nodes but does not say which intermediate artifact requires a term, and it cannot represent the observed rule, requirement and definition dependencies.

**Count prose mentions as usage.** Rejected. Titles and IDs in prose are not typed, canonical references; matching them would be ambiguous, refactoring-sensitive and inconsistent across implementations.

**Introduce `references-terms` for non-behavioural artifacts.** Rejected. “Understanding this artifact requires this term” is coherent for behaviour, rules, requirements, constraints and definitions. A second edge name would create a distinction without a semantic difference and complicate reverse projections and unused-term validation.

**Exclude Domain Term → Domain Term.** Rejected. Definitions routinely depend on other defined terms, the source and target roles remain clear, and the existing canonical-direction rule handles the relationship without ambiguity. Possible circular definitions are a separate concern and are deliberately not prohibited here.

**Add the field to every artifact kind.** Rejected. This RFC establishes a direct semantic dependency for the listed source kinds only. In particular, a Bounded Context's language ownership is already derived and must not suppress `PRODUCT106`. The vocabulary should expand only where authors need to state a real semantic dependency that existing relationships cannot express.

## Consequences

The semantic decision is one coherent edge: `uses-terms` always points from an artifact whose interpretation requires a term to that Domain Term. It applies to Use Cases, Structured Behaviours, Business Rules, Domain Terms, Functional Requirements, Quality Requirements and Constraints. Reverse usage remains derived, prose remains non-structural, and no cycle rule is introduced.

This is a normative change under [CONTRIBUTING.md](../CONTRIBUTING.md). It remains public and requires maintainer consensus and resolution of substantive feedback. The temporary stabilization note suspends a fixed minimum elapsed time while the specification is pre-stable; it does not bypass review.
