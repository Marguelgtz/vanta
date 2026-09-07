# Vanta — Open Questions (ranked by how much the answer would change the vision)

Q1. **Is there a useful horizontal work/economic-provenance abstraction, or only a generic
record wrapper?**
This is the immediate post-MVP falsification question. A useful abstraction must preserve
native semantics across Stint compute, software/deployment provenance, Akash-style leasing,
Lava RPC and an agent/task case; it must also compose child work and drive an external economic
or policy action. If it cannot, Vanta Work should be narrowed or killed without changing Vanta
Core. See `research/HORIZONTAL_WORK.md`.

Q2. **One shared Vanta history, or a Vanta protocol across many chains/substrates?**
One shared history maximizes cross-application provenance and network effects. A portable
standard across chains preserves sovereignty and may fit IBC/modular ecosystems better, but
fragments canonical history. This determines whether Vanta is primarily a network, a standard,
or both. Do not answer from grant availability alone.

Q3. **Which existing substrate actually satisfies Base MVP invariants at acceptable cost and
complexity?**
The current MVP plan intentionally prefers an existing public substrate before owning chain
machinery. Cosmos/IBC is newly relevant because of ecosystem fit and reusable-module funding,
but must be added to the substrate comparison as evidence, not selected by assumption.

Q4. **Where does committed evidence live, and what durability guarantee is sufficient?**
A content hash to vanished data is a dead commitment. The base currently guarantees integrity
not availability. Determine whether the survival/originator-independence test requires a minimal
availability convention or whether availability cleanly remains an above-base service.

Q5. **Is permissionless contribution a hard Vanta invariant or merely 'not controlled by the
originating application'?**
The current lean is hard permissionless append. This materially changes substrate selection,
spam/fee assumptions and the strength of the blockchain requirement.

Q6. **How much shared verification semantics are needed above the Base MVP?**
Vanta Core is truth-agnostic. Horizontal Work may need portable policy/attestation schema
conventions so independent parties can reach useful results without a universal truth engine.
Too little becomes uninterpretable metadata; too much contaminates the base with domain logic.

Q7. **Should Vanta define identity continuity beyond signing-key rotation, or interoperate with
DIDs/VCs/account systems?**
Base Actor = signing key is intentionally small. Real economic history may need organizational
continuity, delegation and recovery without turning legal identity into protocol truth.

Q8. **How should portable reputation work without becoming a universal score?**
Current principle: history/evidence is portable; scoring is typed and application-specific.
Test whether two independent applications can compute different but defensible views from the
same history. If every useful consumer needs the same score, the interpretation split may be
wrong; if scores diverge arbitrarily, evidence may be too thin.

## Parked economic-branch questions

- How are disputes resolved when evidence cannot close the loop?
- What settlement/escrow semantics belong in a Vanta Work economic layer?
- Does any native security asset have a necessary function (staking/slashing/fees), or can an
  existing asset/substrate provide it?
- Validator-set and protocol-fee design if Vanta ever owns consensus.
- Privacy/deletion tension for public immutable history.
- Governance of schema evolution.

## Project relationship notes

- **Stint:** first-party compute pressure test and likely consumer; does not define Vanta.
- **Spark:** may become a concrete software/deployment-accountability consumer later; Scenario B
  remains generic and must not be rewritten as Spark.
- **Akash:** vertical compute market and Cosmos ecosystem adapter/funding candidate; not a Base
  MVP dependency.
- **Lava:** decentralized RPC/data-service vertical and useful horizontal-abstraction stress
  test; not a Base MVP dependency.