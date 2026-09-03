# Vanta — Origins of the Idea

## Thread 1: Immutable structured transactions ("Protobuf, but immutable")

The spark was not immutable *objects* in a programming language. It was immutable
*transactions* in a ledger: state changes by adding new transactions, never by rewriting old
ones. Protobuf supplied the *shape* of the idea: schemas for structured messages, typed
fields, language independence, compact deterministic serialization, schema evolution. The
deeper concept Vanta cares about: **applications communicate through structured, typed records
that become permanent, shared parts of history** — a protocol-level type system for history.

Implications carried into the vision:

- Records are typed by schemas the protocol governs (not free-form bytes).
- Deterministic serialization makes hashes meaningful across implementations ("same bytes,
  same hash, any language").
- Schema evolution is a governance question (new record types / fields without breaking old
  history — the Protobuf field-tag discipline).
- Interop without a common operator: any app can read another app's history if they share the
  record format.

Open: Protobuf itself is not sacred — it stands in for "deterministic, versioned,
schema-governed serialization" (candidates: Protobuf, CBOR+COSE, Scale, a custom canonical
form).

## Thread 2: Stint and decentralized compute

The Stint exploration introduced: providers, machines, work requests, execution, receipts,
reputation, staking, escrow, proof of execution, settlement, and autonomous agents acquiring
compute.

What Stint revealed as a *candidate general pattern* (not yet a conclusion):

> An actor expresses **intent** → another party **commits** to fulfill it (backed by stake) →
> work happens (off-chain) → **evidence** is produced → a **receipt** records the outcome →
> economic **settlement** follows.

[NOTE: Stint's actual design details are not in this repo. This thread needs author input to
stay accurate — assumptions made so far are flagged in PRIMITIVES.md.]

The test Stint sets for Vanta: if the intent/commit/receipt/settle pattern works for compute
*and* for other domains (API calls, storage, data, energy, ownership transfer), Vanta is a
general protocol. If record types must be forked per domain, Vanta was secretly a compute
protocol. (Cross-domain tests so far, in PRIMITIVES.md §5: the pattern survives for APIs and
storage — with one new requirement, recurring evidence; ownership transfer is a degenerate
case.)

## Other projects — relationship assessment (honest, not forced)

| Project | Relationship to Vanta | Note |
|---|---|---|
| Coding agents | Plausibly the *demand side* of the machine economy: agents are the buyers/actors that Vanta's primitives (bounded delegated spend authority, commitments, receipts) serve | Conceptually related, not dependent. To confirm. |
| Spark | Unknown — needs a description from the author before assessing | Input needed |
| ThermoCompare | Unknown — needs a description from the author before assessing | Input needed |

Rule: a connection must be earned, not assumed. A project belongs to Vanta's orbit only if
Vanta's primitives (enforced commitments, portable evidence/history) are genuinely
load-bearing for it.

## The intellectual path, in one breath

Immutable ledger → typed/structured transactions (the Protobuf insight) → state as append-only
shared history → work + evidence + economic commitment (Stint) → the general
commit/receipt/settle pattern → the question of who orders and enforces that history →
consensus with economic security → Vanta.