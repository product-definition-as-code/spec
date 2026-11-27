# Current synthetic product intent

This is a synthetic benchmark policy for the assigned episode. Human G1 approval is required before scored execution. The rendered policy, current request and accepted predecessor history govern this session. Stable identifiers name prose decisions rather than a formal language. The fixed interface governs interchange. Flag contradictions or missing decisions; do not silently change policy. Synthetic change approvals are research controls, never human acceptance of a delivered product.

## Domain and units (BOOK-DOMAIN)

One operation considers one reservation and a shared capacity pool. `used` counts integer capacity units already occupied by all confirmed reservations, including this reservation when CONFIRMED; `capacity` is the pool's integer capacity. REQUESTED consumes no units. Each confirmed reservation consumes exactly the current footprint of {{reservation_footprint_units}} units. These are indivisible units; no rounding or conversion of supplied values occurs. Capacity and used are already measured in the current episode's units. A footprint change changes consumption per reservation, not the numerical meaning of one capacity unit. It does not migrate historical numeric states: predecessor evidence remains about its old model; new requests use states valid for the current footprint.

`days` is an externally supplied integer count of whole days until the reservation begins; zero is the start day. Subday time, time zones and elapsed time are outside this model. `due` is a trusted externally supplied eligibility flag for expiry; it is independent of days. There is no clock, timer, automatic transition, scheduling guarantee or inferred relationship between due and days. Operations are atomic and evaluated against a coherent snapshot; concurrent calls and persistent storage are outside scope.

## Total input and rejection (BOOK-INPUT)

The runtime input is a dictionary representing a JSON object. It must contain exactly the eleven interface keys, with no missing/extra keys. status, used, capacity, days, actor, owner, issuer and operation must be integers, excluding booleans, floats and strings; due, authenticated and editor must be booleans. Integers have mathematical precision, with no upper limit. status must be 0..3, operation 0..3; used, capacity, days, actor, owner and issuer must be nonnegative. used must not exceed capacity. A CONFIRMED state must have used at least the current footprint. Capacity zero is valid for REQUESTED and terminal states. No further history, owner existence or reachable-history constraint is imposed. Terminal states may coexist with any otherwise valid pool usage. Invalid input is always rejected before any business operation.

Every call returns exactly accepted, status, used and owner. accepted is boolean. Rejection, whether malformed input, invalid state, failed authorization or unmet guard, returns accepted=false and copies input status, used and owner exactly, without repairing them. If one of those keys is absent, its returned value is null. Invalid JSON values therefore may appear unchanged in these three rejection fields. The interface accepts dictionaries only; non-dictionary Python callers are outside its declared API. No error category or precedence is exposed. Unknown operations/statuses reject. Extra fields reject even if their values are otherwise harmless.

The SMT interface already types integers/booleans and has no missing/extra keys; its total relation covers every assignment of those sorts, including negative integers and out-of-range codes. Wrong runtime types/shape are runtime obligations, not an SMT proof claim. Rejects preserve state there as well.

## Identity assumptions and authorization (AUTH-TRUST, AUTH-RIGHTS)

actor and owner are stable opaque nonnegative identity numbers; equality means the same identity. The caller cannot write identity or role assertions in a real service: an external trusted authenticator supplies actor, issuer, authenticated and editor consistently. authenticated=true means identity verification succeeded; editor=true means that authenticator asserts a global trusted-editor role for this actor. The experiment assumes these assertions and tests decisions over them; it does not verify token cryptography, account existence, revocation, role issuance, network or authenticator correctness. owner is part of the trusted stored reservation snapshot. Even the owner or an editor must be authenticated by a trusted issuer. Unknown nonnegative issuer numbers are valid data but untrusted.

The current trusted issuer numbers are {{trusted_issuers}}. An editor assertion from an untrusted issuer grants nothing. CONFIRM and CANCEL allow either the reservation owner or a trusted editor. EXPIRE requires a trusted editor. The current EDIT rights setting is {{edit_rights}}. The value trusted_editor requires a trusted editor; owner_or_trusted_editor permits either the owner or a trusted editor. Both settings still require authentication by a trusted issuer. There is no administrator bypass. EDIT acknowledges authority to edit nonrepresented descriptive content; it changes none of this interface's state. This deliberately small operation makes the rights contrast observable without adding a semantic API or a new field.

## Booking operations and frame (BOOK-CONFIRM, BOOK-CANCEL, BOOK-EXPIRE, BOOK-EDIT)

These four paragraphs are stable direct use-case text. Derive their authorization from AUTH-TRUST/AUTH-RIGHTS. Keep the identity assumption in a separate source artifact so a changed assumption can leave direct use-case bytes unchanged.

CONFIRM: After BOOK-INPUT validation and AUTH-TRUST/AUTH-RIGHTS authorization, accept only from REQUESTED, with days no greater than the maximum lead window of {{maximum_lead_days}} whole days and enough unused pool units for the episode's entire footprint. On acceptance set status to CONFIRMED and increase used by the footprint. Zero days and exactly the maximum lead window are included. due does not affect this operation.

CANCEL: After BOOK-INPUT validation and AUTH-TRUST/AUTH-RIGHTS authorization, accept from REQUESTED at any valid days, or from CONFIRMED when days is at least {{confirmed_cancellation_minimum_days}}. On acceptance set status to CANCELLED; release exactly the footprint only if the old status was CONFIRMED. There is no additional due condition. The cancellation threshold is inclusive.

EXPIRE: After BOOK-INPUT validation and AUTH-TRUST/AUTH-RIGHTS authorization, accept only when due=true and the old status is among the current expiry source statuses {{expiry_source_statuses}}. On acceptance set status to EXPIRED; release exactly the footprint only if the old status was CONFIRMED. There is no days threshold. No other source status is eligible. No release occurs for REQUESTED.

EDIT: After BOOK-INPUT validation and AUTH-TRUST/AUTH-RIGHTS authorization, accept only from REQUESTED or CONFIRMED. On acceptance retain status and used. days and due add no guards. Terminal states reject every operation, including EDIT.

Every accepted operation preserves owner. It also preserves all unreturned inputs and all other reservations; only the selected reservation's status and its contribution to pool usage may change as stated. There is no transfer, creation, deletion, capacity adjustment, automatic release, repeated cancellation/expiry success or hidden write. Rejection preserves the complete state. Existing terminal state usage represents other reservations and must not be decremented.

## Independent artifact and public behaviour (AUDIT-RETENTION, SB-CAPACITY)

AUDIT-RETENTION: Retain audit records for {{audit_retention_days}} whole days. Record persistence/deletion is outside decide and Step; there is no audit input or output. This requirement has no dependency on any booking or authorization decision. It exists to test honest scope and evidence applicability without inventing an executable retention API.

SB-CAPACITY current wording: “{{sb_capacity_text}}” It refers to BOOK-CONFIRM and its complete guards/effects; this example sentence is not an alternate complete contract. Changed citation bytes and changed mathematical meaning are separate questions. Never silently renew citation pins.
