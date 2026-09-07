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
What it is: a Cosmos-SDK decentralized compute marketplace with deployment/order/lease/provider
and escrow semantics around off-chain workloads. Providers expose infrastructure; workloads run
off-chain. Current grant program also funds open-source infrastructure/services that drive
network usage and utility.
Illuminates: a strong **vertical** protocol: compute-market semantics belong in the domain
protocol, not Vanta Core. Akash also demonstrates that Vanta must not claim novelty merely for
provider markets, leases, escrow, measurement/reputation or signed compute evidence.
Candidate Vanta relationship: an Akash lease/provider/attestation may be referenced as
domain-native evidence inside a larger Vanta Work provenance graph, if that produces value
beyond Akash's own lifecycle. Do not make Akash a Base MVP dependency.
Current references checked 2026-09-07: <https://akash.network/docs/> and
<https://akash.network/grants/>.

### Lava Network
What it is: a decentralized RPC/data-access protocol. Providers serve relays, receive
cryptographic proofs of service, accumulate compute units, and are scored on QoS/reputation
signals such as latency, availability and freshness.
Illuminates: a second strong vertical service protocol whose unit of work is very different
from a long-running compute lease. Vanta should reference Lava-native proof/QoS semantics rather
than replacing them. This is a useful hostile test for horizontal work provenance.
Current references checked 2026-09-07: <https://docs.lavanet.xyz/lava-architecture/> and
<https://docs.lavanet.xyz/provider-rewards-service/>.

### Sentinel
What it is: Cosmos-SDK decentralized bandwidth/dVPN infrastructure with session/usage and
provider economics. Earlier proof-of-bandwidth work is important prior art for signed
service-consumption evidence.
Illuminates: "signed receipt for off-chain resource use" is not itself a novel Vanta claim.
The horizontal thesis must instead survive composition, provenance and independent
interpretation across domains.
Reference: <https://docs.sentinel.co/>.

### Fetch / ASI uAgents payment protocols
What it is: agent communication/protocol tooling with an Agent Payment Protocol that
standardizes payment negotiation/finalization between agents.
Illuminates: Vanta should not claim novelty for "agents can pay each other" or for a generic
payment state machine. A candidate Vanta layer would concern durable attributable work/evidence
relationships around the payment.
Current reference checked 2026-09-07:
<https://uagents.fetch.ai/docs/guides/agent-payment-protocol>.

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

## Cross-ecosystem adjacent standards

### A2A (Agent2Agent)
What it is: an agent interoperability protocol with stateful task lifecycle, progress and
artifacts.
Illuminates: "generic work/task lifecycle" is not sufficient novelty for Vanta Work.
Current reference checked 2026-09-07: <https://a2a-protocol.org/latest/topics/life-of-a-task/>.

### ERC-8004
What it is: an Ethereum trust layer for agents with identity, reputation and generic validation
registries; validation can reference re-execution, zkML, TEE or trusted judges. Payments are
explicitly orthogonal.
Illuminates: identity + reputation + generic validation are already being standardized. Vanta
must differentiate on shared cross-domain provenance/history rather than claiming these pieces.
Current reference checked 2026-09-07: <https://eips.ethereum.org/EIPS/eip-8004>.

### x402
What it is: an HTTP-native open payment standard using `402 Payment Required` to let clients
programmatically pay for API/content resources.
Illuminates: machine payment is separable from fulfillment/economic provenance; Vanta Work
should be able to reference an external payment/settlement rail rather than own every rail.
Current reference checked 2026-09-07: <https://docs.x402.org/introduction>.

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
### SLSA / in-toto
What it is: software supply-chain provenance/attestation standards linking build definitions,
inputs, builders, outputs and verification policy.
Illuminates: Scenario B has mature prior art; Vanta's value would be durable shared provenance
and cross-domain composition, not inventing build attestations.
References: <https://slsa.dev/> and <https://in-toto.io/>.