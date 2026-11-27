---
id: UC-A
type: use-case
title: Draft change booking state
status: draft
primary-actor: ACT-A
governed-by:
- BR-A
uses-terms:
- TERM-A
- TERM-IDENTITY
---

## Goal

Change the draft booking state without exceeding capacity.

## Trigger

The member requests confirmation, cancellation or expiry.

## Preconditions

The aggregate invariant holds; the transition's source state and guards hold.

## Main Flow

Check guards, atomically change state and adjust used slots by the declared effect.

## Alternative Flows

Cancel or expire a confirmed booking, releasing exactly one slot.

## Failure Conditions

Refuse unavailable capacity, excessive lead time or an inapplicable source state.

## Postconditions

The invariant holds; capacity and owner identity are unchanged.
