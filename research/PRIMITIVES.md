# Vanta — Candidate Core Primitives (under test)

Status: actively competing. Do not pick a term because it sounds good.

## 1. The lifecycle any primitive family must cover

```
engagement: idle → intent → committed (stake/escrow locked) → executing (off-chain)
            → receipt (evidence committed) → [dispute] → settled / closed
```

For each candidate primitive the test questions: what does it represent; who creates it; who
signs it; who verifies it; can it reference previous state; can it own or transfer value; can
it expire; can it be disputed; can other applications compose with it?

## 2. Candidates tested

### A. One "fact" / "event" primitive (the typed record)
One record type, a tagged union: every transition on Vanta is a signed, typed, hash-linked
fact. Intent/commitment/receipt/settlement/dispute are *kinds* of fact, not separate
primitives.

- Creates: the party the fact is about (commitments by the committer; receipts by the
  provider, verified by the consumer).
- Signs: the creator. Verifies: signature check + schema validation + hash linkage into
  history.
- References previous state: yes (engagement id, the commitment it answers, the evidence
  hash).
- Value: a fact doesn't *hold* value; it *triggers* value movement in protocol state.
- Expiry: deadlines carried in the fact + automatic state transitions (receipt deadline
  passes → slash).
- Disputed: the fact itself isn't disputed — claims *within* it are (a contested receipt
  opens a dispute fact).
- Composition: any app can emit and read any fact kind → cross-app interop.
- Strength: one primitive = clean data model (the Cosmos "Msg" idea); the protocol is a
  state machine over facts.
- Weakness: "fact" is a vague word; the *rules* (what a receipt must commit to) matter as
  much as the record — the primitive may really be "fact + its validation rule," i.e. the
  schema is part of the primitive.

### B. A small family: intent / commitment / receipt / settlement (+ dispute)
Each is a primitive with its own semantics.
- Strength: maps 1:1 to the lifecycle and to Stint; each has a clear creator/verifier.
- Weakness: five primitives = five rule sets; risk of overlap (a settlement is just a fact
  that moves value — separate primitive, or a flag on a fact?).
- Resolution hypothesis: the *family* is the interface apps use; underneath, the *single
  typed fact* is the ledger primitive. Family = the protocol's base record kinds.

### C. "Commitment" as the one primitive
Everything is a commitment: intent is a commitment to pay; receipt is a commitment to
evidence; settlement discharges both.
- Strength: one concept unifies demand and supply.
- Weakness: stretches the word. Receipts are *evidence*, not promises. Commitments point
  forward; evidence is a fact about the past. Forcing evidence into the commitment frame
  loses the past/future distinction that makes disputes meaningful.
  [Rejected as the single primitive; kept as one family member.]

### D. Capability (object-capability tradition: Erlang, E, IOTA lineage)
A capability = a bearer token of authority. "An agent may spend up to B on compute" is a
capability.
- Strength: clean answer to machine identity and delegated authority; capabilities compose
  and can't be used by anyone who doesn't hold one.
- Weakness: capabilities are about *authority to act*, not *history* or *value*. Vanta needs
  both; a capability model alone gives no ledger.
- Keep: as the identity/authority layer (§7), not as the ledger primitive.

## 3. Current working hypothesis [MODERATE confidence]

**The ledger primitive is one thing: a typed, signed, hash-linked fact (a "transition" in the
protobuf-ledger sense). The protocol defines a base family of fact kinds — intent,
commitment, receipt, settlement, dispute — each with a validation rule and a state-transition
rule. Applications extend the family via governed schema.**

The family is the interface; the fact is the substrate. Nothing else has survived testing so
far.

## 4. Evidence hierarchy (what "proof of work" can mean)

| Level | Evidence | Cost | Gameability | Status |
|---|---|---|---|---|
| L0 | Provider self-attestation ("I ran it") | ~0 | High | Usable only with strong two-sided staking |
| L1 | Two-party: consumer verifies output and co-signs the receipt | Low (consumer effort) | Consumer can falsely refuse/accept; staking makes both sides honest on average | **Pragmatic default** (optimistic, like optimistic rollups: assume valid, punish provable fraud) |
| L2 | Independent / bonded third-party verifier (Bittensor-style validator, or arbitration service) | Medium | Verifier can be bought/collude — bonds + rotation + sampling | Dispute fallback |
| L3 | Verifiable computation / ZK proof of execution (a ZKVM proves "workload W ran to completion on a machine") | High today, falling | Very low | Direction of travel; protocol must accept L3 receipts from day one |

Design rule: Vanta should be **verification-agnostic** — a receipt commits to *some* evidence
E under a *declared* evidence scheme S (hash of E, a proof, co-signatures). The protocol
checks the scheme's rules were followed, not that physics is true. This keeps Vanta general
across domains (compute, storage, and APIs have entirely different evidence schemes).

## 5. Cross-domain tests (does the pattern survive?)

- **API purchase** (agent buys 10k calls): intent = call budget; commitment = service
  provider stakes capacity; evidence = signed usage meter (per-batch request/response
  hashes); settlement per batch. **Survives** — only the evidence scheme changes (a meter,
  not a compute proof).
- **Storage** (1TB for 30 days, retrievable): pattern survives *only if* receipts can be
  **recurring** (periodic storage proofs / Merkle roots over stored data, liveness checks).
  Finding: Vanta's receipt model must support continuing obligations (scheduled evidence),
  not just one-shot delivery.
- **Ownership transfer** (digital asset between parties): lifecycle degenerates — no
  "work", just conditional value movement. Finding: Vanta needs a simpler base primitive for
  **plain conditional exchange** (a settlement with conditions), with the full work lifecycle
  as an extension on top.
- **Where the pattern breaks**: work whose quality is purely subjective (human judgment, no
  verifiable output) — no evidence scheme closes the loop; Vanta would fall back to bonded
  arbitration, reintroducing a (bonded, sampled) human element. Expect Vanta to be strongest
  where outputs are machine-checkable.

## 6. On/off-chain boundary [HYPOTHESIS, working rule]

**On-chain (protocol state/history): the minimal facts needed to settle or lock value, or to
trigger a transition that does** — identities, stakes, escrows, event headers (who, kind,
what it commits to, when), dispute outcomes, settlement transitions.
**Off-chain, hash-committed: workloads, outputs, logs, measurements, evidence payloads,
proofs (or their roots).**
**ZK / encrypted: where privacy is required — commit to properties, not content** ("this
workload satisfies spec X" without revealing the workload; "this party has ≥ N stake" without
revealing identity).

Privacy corollary: if Vanta stores only hashes and thin facts, sensitive *content* never
touches the chain — but a hash can still leak *existence*. For regulated data, design toward
on-chain verification points that reveal nothing (commit to a nonce-encrypted blob, or keep
the commitment off-chain with a signed receipt). The tension between "immutable public
history" and deletion/privacy rights is unresolved and important (QUESTIONS, parked).

"What does Vanta need to *know* vs. what it needs to be able to *verify*?": Vanta needs to
*know* only minimal economic facts (who staked/escrowed how much, canonical order, outcomes).
For everything else Vanta only needs to be able to *verify on demand* (blob matches its hash;
a proof checks; a ZK statement is true). **Vanta is a verifier of commitments, not a store
of facts.**

## 7. Identity [HYPOTHESIS, early]

- A Vanta identity = a **continuity object**: a key/identity whose history and stake survive
  key rotation (a chain of successive keys, each signed by its predecessor; or
  recovery/social/multisig schemes).
- Pseudonymous by default; optionally anchored to real-world identity by attestors
  (interoperate DIDs/VCs — Vanta should not redefine identity, only interoperate with it).
- Machines/agents act with **bounded delegated authority**: a person/company key delegates a
  scoped capability (spend cap, allowed fact kinds, time window) to an agent key — a
  corporate card with limits, not a root wallet.
- Reputation portability follows: history is public and keyed to the continuity object, so
  an app's interpretation of it travels with the identity across apps.