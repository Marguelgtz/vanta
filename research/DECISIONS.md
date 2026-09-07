# Vanta — Decisions and Hypotheses (with reasoning)

Format: current position → evidence for → counter-evidence → alternatives → confidence →
what would cause a revisit.

D1. **Blockchain is intrinsic to Vanta, but the Base MVP does not require Vanta-owned
consensus/staking.** — *Held, corrected 2026-09-07.*
Position: the base requires a decentralized substrate that can provide canonical ordering
without an application/operator, permissionless contribution, public verification and durable
liveness. Staking/slashing/value enforcement belong to an above-base economic branch unless a
change gate proves the base itself requires them.
For: aligns with MVP_PLAN invariants I5/I6/I9 and the original requirement that important
history outlive the application/company that created it.
Against: a transparency log/federation is cheaper and may satisfy many practical users; if
permissionless contribution or indefinite liveness prove unnecessary, blockchain becomes
harder to justify.
Alternatives: transparency log; consortium/federated log; existing public chain; sovereign
app-chain.
Confidence: high that blockchain is part of the intended Vanta identity; moderate that the
Base MVP's exact substrate requirements survive measurement.
Revisit if: S1 shows a simpler decentralized/federated system satisfies the same invariants,
or the author changes the foundational assumption.

D2. **Vanta stores evidence/history, not interpretations.**
Position: the protocol stores typed attributable records, references and commitments;
reputation/prices/quality/policy are computed by applications over public history.
For: avoids a universal gameable score; preserves cross-domain reuse; matches "Vanta owns the
evidence and the history. Applications own the interpretations."
Against: some applications may need shared interpretation conventions for interoperability.
Alternatives: protocol-level scoring (rejected for the base); publish interpretations as
ordinary schemas/records above the base.
Confidence: high.
Revisit if: independent applications cannot derive useful interpretations from the same
history without a shared protocol-level state machine.

D3. **The Base MVP primitive is a type-opaque signed record envelope, not a built-in work or
economic fact family.** — *Supersedes the v0.1 intent/commitment/receipt/settlement family.*
Position: Actor / Schema / Record / History are the proposed minimum. Domain lifecycles are
expressed as schemas and references above the base.
For: Scenario A and B can exercise provenance without turning Stint or deployment concepts
into protocol ontology; keeps the original "typed shared history" vision as the trunk.
Against: application developers may prefer stronger protocol semantics; a completely opaque
base can become little more than generic signed metadata if above-base conventions fail.
Confidence: high for the current MVP, not a permanent protocol guarantee.
Revisit after: CP1/MVP evidence or the five-question change gate shows a missing semantic must
be enforced by the base.

D4. **Vanta is a general protocol, not a compute marketplace. Stint is a pressure test / first
consumer candidate, not the definition of Vanta.**
Position: Vanta-level = attributable typed history and whatever later layers earn their way in;
Stint-level = compute-specific execution, provider mechanics, telemetry and evidence.
For: the software/deployment scenario independently exercises the same base; the horizontal
work hypothesis is being tested across additional domains.
Against: generality may be speculative if the abstraction only remains useful for compute.
Confidence: moderate-to-high for the base; horizontal-work generality remains unproven.
Revisit if: non-compute scenarios require bespoke base changes or add no real value.

D5. **Economic settlement/security is an above-base branch; token design remains parked.**
Position: escrow, staking, slashing, settlement, protocol fees and any native asset are not Base
MVP requirements. If a later economic layer needs slashable security or spam resistance, define
the function before choosing an asset.
For: avoids speculative tokenomics and preserves substrate freedom.
Against: an eventual machine-work protocol may need enforceable value commitments, making the
economic branch central to its product value even if not to Vanta Core.
Confidence: high as an MVP boundary; low on eventual economic architecture.
Revisit when: a concrete settlement/dispute/security design exists.

D6. **Vanta Core is truth-agnostic; verification schemes live above the base.** — *Corrected
2026-09-07.*
Position: the base can prove attributable statements (who signed which canonical record, which
references/commitments exist, where the record sits in history). It does not prove a GPU ran, a
build was correct, an RPC answer was fresh or a human claim was true. Domain schemas may declare
verification policies and attestation schemes.
For: preserves domain neutrality and lets TEE/ZK/re-execution/human verification evolve without
base forks.
Against: without useful above-base verification conventions, a permanent history can contain
perfectly attributable nonsense.
Confidence: high for the base boundary.
Revisit if: independent verification cannot be composed without protocol-native scheme state.

D7. **Re-centering: the Base MVP is V1 (typed shared history); economic/machine layers are
branches above the base.** (2026-02-09, retained.)
Position: base MVP = immutable typed-history protocol; receipts/accountability reveal base
properties; economic enforcement sits above and is not a base requirement.
For: author's explicit constraint that the original vision is the constraint.
Against: the economic layer may ultimately provide the strongest practical "why blockchain"
and product wedge.
Confidence: high as the current governing MVP decision.
Revisit if: the Base MVP is unusable for intended consumers without economic enforcement.

D8. **Horizontal Work is a candidate above-base schema family, not a Vanta redefinition.**
(2026-09-07.)
Position: test whether obligations, performance claims, attestations and resolutions can form a
useful cross-domain economic-provenance graph while native systems retain execution semantics.
For: repeated structure appears across Stint compute, software provenance, Akash-style leases,
Lava RPC service and agent/task systems.
Against: A2A, ERC-8004, x402, SLSA/in-toto and vertical protocols already cover large parts of
the space; a generic wrapper may add no semantics beyond metadata.
Confidence: moderate enough for a falsification spike, not a product commitment.
Revisit / kill if: composition or economic consumption requires domain-specific logic in the
common layer. See `research/HORIZONTAL_WORK.md`.

D9. **Funding availability is not architecture evidence.** (2026-09-07.)
Position: pursue Cosmos/Interchain and Akash funding now, but do not choose Cosmos, Akash, IBC,
a token model or a Vanta app-chain merely because grants exist.
For: avoids grant-driven protocol contamination; preserves the MVP change gate.
Against: ecosystem fit and funding can legitimately affect implementation order and which
reference adapter is built first.
Confidence: high.
Revisit only if: a funder's constraints are explicitly accepted as product constraints by the
author.

## Change log
- 2026-02-09 — initial v0.1 research decisions; economic enforcement was the leading branch.
- 2026-02-09 (plan phase) — v0.2 Base MVP re-centered on typed shared history; economic
  primitives removed from the base.
- 2026-09-07 — reconciled stale D1/D3/D6 language with the governing v0.2 MVP; added the
  horizontal-work falsification hypothesis and the rule that funding cannot choose architecture.