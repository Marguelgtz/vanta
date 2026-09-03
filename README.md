# Vanta — Living Vision Research

Vanta is being explored as decentralized, blockchain-native infrastructure: a protocol for
immutable, structured state transitions — promises, work, evidence, and settlement between
parties who don't trust each other, including machines and software agents.

This is a research process, not an implementation plan. The direction is allowed to evolve;
what must be preserved is continuity: when an idea changes, record what changed and why.

## Living artifacts

| File | Holds |
|---|---|
| [research/VISION.md](research/VISION.md) | Current vision, the "why blockchain" answer, hidden assumptions, competing versions |
| [research/ORIGINS.md](research/ORIGINS.md) | The intellectual path that led here (immutable-ledger/Protobuf thread, Stint, other projects) |
| [research/PRIMITIVES.md](research/PRIMITIVES.md) | Candidate core primitives under test, engagement lifecycle, evidence hierarchy, on/off-chain boundary, identity |
| [research/PRIOR_ART.md](research/PRIOR_ART.md) | Reference systems that illuminate parts of the idea (not templates) |
| [research/QUESTIONS.md](research/QUESTIONS.md) | Open questions, ranked by how much the answer would change the vision |
| [research/DECISIONS.md](research/DECISIONS.md) | Key decisions/hypotheses: position, evidence for/against, confidence, revisit triggers |
| [research/MVP_PLAN.md](research/MVP_PLAN.md) | **Base MVP living action plan** — non-negotiable vision, invariants, minimal primitives, MVP boundary, tiers, spikes, checkpoints, success criteria |

## Current one-liner (v0.1, 2026-02-09)

Vanta is a neutral, permissionless, blockchain-maintained protocol in which parties — people,
companies, machines, agents — exchange **binding promises** about work or resources and
**evidence** that those promises were kept, recorded as immutable, typed, signed transitions in
a shared canonical history; the protocol owns the facts (who promised, what evidence exists,
what value moved), and applications own the interpretations (prices, reputation, quality).

## Current phase (2026-02-09)

**Base MVP planning.** Per the author's constraint that the original vision is the
constraint, the center of gravity is re-centered from the v0.1 research lean (enforced
commitment / economic layer) to **V1 — the immutable typed-history protocol — as the trunk**,
with the economic/machine layer (V2) demoted to a branch above the base. See
[research/MVP_PLAN.md](research/MVP_PLAN.md) §1. The v0.1 one-liner above is kept as the
research state of record.

## Foundational assumptions (do not silently rewrite these)

1. Vanta is protocol/infrastructure, not a conventional company or SaaS product.
2. Blockchain is intrinsic — without it, Vanta stops being Vanta.
   *(v0.1 sharpening: what no simpler system can provide is not immutability but
   **enforced resolution** of value commitments — the argument for the economic branch.
   Re-centered 2026-02-09 for the base MVP: the base needs from blockchain
   **canonicity without an operator + permissionless contribution + indefinite liveness** of
   the shared history — see MVP_PLAN.md §1–2. Both sharpenings are retained, each scoped to
   what it argues for.)*
3. The immutable structured-transaction idea ("Protobuf, but immutable in a
   transaction-ledger sense") is one of Vanta's core origins.