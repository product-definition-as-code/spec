# RFC 0081: Retrieval returns citation material

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-25

## Problem

Before a consumer can cite canonical product text, someone or something has to find it. The specification fixes what a citation is ([Citation Contract](../spec/citation-contract.md)), how drift is detected ([Validation → Digests](../spec/validation.md#digests)) and what a change obliges consumers to revisit ([Product Changes → Change impact](../spec/product-changes.md#change-impact)). It says nothing about retrieval.

At today's model sizes this is harmless: identifiers, type prefixes and text search suffice. It stops being harmless when the model outgrows what one reader, human or LLM, can hold. Implementations will then bolt on search, lexical or semantic, and an unconstrained retrieval layer is a shadow store in the making: it serves prose without ids or digests, its index drifts from the model with no way to tell, and the text an agent consumed and acted on is unverifiable. That is precisely the silent-drift failure the Citation Contract exists to make detectable, reintroduced one layer up.

The pressure is concrete, not hypothetical. Generic RAG stacks and agent session-memory systems hold derived copies of whatever they ingested, unversioned, undigested and outside any change mechanism. If product knowledge flows into an agent through such a layer, the canonical model is no longer what the agent reads; it is what the index happened to contain.

## Proposal

A new section in the [Citation Contract](../spec/citation-contract.md), **Derived retrieval**, with the following normative content.

An implementation MAY provide retrieval over the Product Definition: a facility that, given a query, returns product artifacts or locations within them. How results are found and ranked, lexically, semantically, by graph traversal or any combination, is implementation-defined and non-normative. Everything else in this section is normative.

1. A retrieval index MUST be derived: rebuildable solely from the canonical model at a named revision. It MUST NOT be treated as canonical, MUST NOT be the target of a citation, and MUST NOT live under the model root. Deleting it and rebuilding it MUST be lossless.
2. Every retrieval result that carries artifact text MUST also carry the target artifact's `id` and the whole-artifact content digest of the content actually served, and MAY carry an `anchor`, exactly the fields of a citation record. A retrieval facility MUST NOT serve canonical text without them.
3. For each result, the facility MUST recompute the target's current digest and report the result as `current` or `stale` under the statuses of [Citation Contract → Statuses](../spec/citation-contract.md#statuses). Serving content from a stale index is permitted only with that marking; an unresolvable target MUST NOT be served at all.
4. Retrieval output is citation-ready by construction: a consumer that relies on a result transcribes `id`, `digest` and optional `anchor` into a citation carrier without transformation, and the ordinary contract takes over from there.

The transport is deliberately unspecified. A CLI subcommand, an MCP server, an editor integration or a hosted API all conform if the payload contract holds. Non-normatively: exposing retrieval as an MCP server is the expected shape for agent consumers, because it puts verifiable citation material directly into the agent's tool loop instead of loose prose into its context.

## Impact

- **On existing conformant repositories:** none. No authored content changes; the section constrains a capability no repository is required to have.
- **On existing implementations:** none are required to change. ProductShape intends a `query` capability (lexical first, embeddings optional later) with its index under the implementation-managed cache, exposed over MCP; this RFC fixes the payload contract that capability must honor.
- **On the conformance tests:** one new case exercising the payload contract (query a known model, assert every result carries `id` and a digest matching the pinned artifact, assert a stale-index result is marked `stale`). Open question for review: the current suite assumes every case applies to every implementation, and retrieval is a MAY. Either the case is scoped to implementations claiming the capability, which needs a small suite mechanism, or it waits until a second implementation ships retrieval.

## Alternatives considered

**Say nothing.** Implementations add search anyway, the first mover's payload becomes the de facto contract, and nothing stops a digest-free retrieval layer from becoming the thing agents actually read. Rejected: this is the one point where a shadow store gets constrained cheaply, before it exists.

**Specify a retrieval engine in the kernel:** index format, ranking algorithm, embedding requirements. Rejected. Ranking quality is not a portability property, the kernel stays minimal by doctrine, and freezing search technology into a specification guarantees it ages badly.

**Adopt an external memory system as the store of product knowledge.** Session-memory systems for coding agents store derived, lossy observations with no revision, no digest and no change mechanism. Using one as a source of product truth creates a second store that drifts from `docs/product/**` undetectably, the exact failure PDaC exists to prevent. Rejected for truth; such systems remain fine for what they are, session memory, outside the model. A memory system MAY of course be a retrieval consumer, in which case clause 2 makes whatever it captured verifiable later.

**A full normative retrieval profile now,** with recall requirements and embedding portability. Premature. The payload contract is the part that must be right on day one; retrieval quality can compete freely behind it.
