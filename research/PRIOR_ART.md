# Vanta — Prior Art (reference points, not templates)

Confidence note: entries from working knowledge unless marked. Items marked [VERIFY] should
be checked against current docs before any decision relies on them.

## Crypto / protocol systems

### Cosmos SDK
What it is: framework for application-specific blockchains — modules, Protobuf Msg types,
sovereign protocol logic, IBC for inter-chain comms.
Illuminates: the "one typed transition = one Msg" model (Vanta's single-fact primitive is
exactly this); modules ≈ Vanta's base fact kinds; Protobuf as serialization choice (the
origin thread).
Warns: app-chain sovereignty is attractive but fragments history — IBC (light clients between
sovereign chains) is the prior art for "Vanta as a protocol across many chains" (QUESTIONS Q1).

### Akash Network
What it is: decentralized compute marketplace on Cosmos: orders/bids/leases as on-chain state
objects; actual workloads run on provider off-chain Kubernetes clusters; settlement via
on-chain invoices; provider verification + staking; price oracle relayer (Pyth → Wormhole →
oracle). [2026-02 docs fetch confirmed the structure: provider verification, oracle relayer,
node architecture.]
Illuminates: the exact Stint shape — on-chain order/lease/escrow + off-chain execution +
on-chain settlement. The closest existing thing to "Vanta for compute."
Gap Vanta aims at: (1) Akash's history is about Akash only — no cross-app reuse of
evidence/reputation; (2) provider *measurement* is weak (relies on consumer + stake; no
strong proof of execution); (3) dispute handling is thin. Vanta's differentiation =
first-class evidence + shared history other apps can read. [VERIFY current state of
disputes/verification in docs]

### Bittensor
What it is: network where "miners" produce work and "validators" evaluate it; subnets are
self-governing markets; TAO settles incentives; validators set scores that determine
emissions.
Illuminates: L2 evidence (independent bonded evaluators) as a real architecture; separating
the security/settlement asset (TAO) from the work itself.
Warns: incentive gaming is real — miners/validators collude to produce worthless-but-scored
work. Lesson: **the evidence/verification design is where security lives, not the
tokenomics.**

### Celestia
What it is: modular data-availability chain — consensus + DA only; execution happens on
app-chains/rollups that publish data to Celestia and verify via DA proofs (KZG commitments,
blob sampling).
Illuminates: separating *commitments* (small, on-chain, consensus-ordered) from *data* (large,
off-chain, availability-proven) — exactly Vanta's on/off-chain boundary (PRIMITIVES §6). Also
a candidate home for evidence blobs — and a dependency to watch (a DA provider is a chokepoint
unless Vanta supports several).
[docs.celestia.io fetch failed 2026-02 — [VERIFY] current architecture details]

### Avalanche subnets / Arbitrum Orbit (app-specific chains)
What it is: infrastructure for many application-specific L1s/L2s.
Illuminates: the alternative to "one Vanta chain" — Vanta as a *protocol* (record format +
state-transition rules) deployed as many sovereign chains interop via light clients. Tradeoff:
sovereignty + upgrade freedom vs shared-history network effects (portable reputation,
cross-app evidence). This is QUESTIONS Q1, the biggest fork in the road.

## Non-crypto reference points

### Certificate Transparency / signed transparency logs
What it is: signed hash-chained logs (of TLS certs); anyone can verify an entry; monitors
detect mis-issuance.
Illuminates: the ceiling of non-blockchain design — great *detection*, no *enforcement* (no
value state, no binding resolution; trust anchor = log operator). The rung in the
"why blockchain" ladder everything below it stops at.
Lesson: Vanta can *use* log techniques (hash-chaining, anchoring, Merkle inclusion proofs)
without the log being the whole system.

### Content-addressed storage (IPFS / Arweave / CIDs) + data availability
Illuminates: a home for evidence blobs; CIDs = prior art for "commit to a hash, retrieve
content later."
Warns: durability is a dependency — a hash to data nobody stores is a dead commitment.

### Event sourcing / append-only systems
Illuminates: state as a derived view over an append-only fact stream — the "Vanta owns
history, state is derived" model.
Warns: done naively, event-sourcing everything bloats and complicates; Vanta stores only
*thin economic facts*, not a stream of everything.

### CRDTs
Illuminates (by contrast): CRDTs give convergence *without ordering* — they merge conflicts.
Economic events can't be merged ("paid $5" and "paid $7" can't both be true; one must be
canonical). CRDTs may serve Vanta's *off-chain* mergeable state (caches, views); they are not
a substitute for the ordered canonical economic log.

### DIDs / verifiable credentials
Illuminates: an identity layer Vanta should interoperate with rather than replace; selective
disclosure (SD-JWTs, ZK over credentials) as a tool for privacy in a public history.

### Object-capability systems (Erlang, E, IOTA lineage)
Illuminates: authority as a bearer object — the model for delegated, bounded authority for
agents (PRIMITIVES §7).

### Verifiable computation (ZKVMs: RISC Zero, SP1, Jolt, …; optimistic/MPC-based proofs)
Illuminates: L3 evidence (proof of execution) is becoming real; Vanta's receipts should be
verification-agnostic so L3 slots in without a protocol upgrade. [VERIFY current state of ZKVM
costs/practicality]