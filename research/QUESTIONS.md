# Vanta — Open Questions (ranked by how much the answer would change the vision)

Q1. **One shared Vanta history, or a Vanta protocol across many chains?**
The biggest fork. One chain = maximum network effect (cross-app portable evidence/reputation)
but a single upgrade/centralization target and a hard "why write on my chain" pitch. Many
chains (Cosmos/IBC-style, or Orbit-style app-chains) = sovereignty and fit, but history
fragments and "shared Vanta history" loses meaning — Vanta becomes a standard, not a network.
Resolving it: a concrete cross-app scenario (an agent's provider history reused across two
markets) and a concrete sovereignty need (an app that cannot accept shared governance).
Matters because: it defines what Vanta *is* (a network vs. a standard) and where the network
effect lives.

Q2. **How are disputes resolved when no evidence scheme can close the loop?**
Subjective work, colluding parties, "the output is fine but wrong" cases need a fallback:
bonded human/LLM arbitrators? Pre-agreed criteria? Sampling? If disputes are often
unresolvable, escrow degrades to a slow lockbox and trust in the system erodes.
This is the security core of the whole idea — the "optimistic" bet (assume valid, punish
provable fraud), same logic as optimistic rollups.

Q3. **Where does evidence live, and what guarantees durability?**
A hash to vanished data is a dead commitment. DA layer (Celestia-style) or content-addressed
storage is the current answer — but each is a dependency (potential centralized chokepoint).
Multi-DA from day one?

Q4. **Is the machine economy actually arriving (the "why now" question)?**
Forces: autonomous agents with wallets, stablecoins, modular blockchains, maturing ZK. The
unproven part: agents *transacting* at meaningful scale with real skin in the game. If
Vanta's first app (Stint) depends on this, the vision needs a second, human-led wedge
(inter-org service exchange? compliance/provenance?) that doesn't depend on agent commerce.

Q5. **Native asset: what would it actually do?**
Candidate functions: staking/slashing security, transaction fees (spam control), validator
set, governance. Services probably priced in stablecoins; security probably needs a native
asset (stablecoins can't be slashed). Whether Vanta mints anything, or reuses an existing
security asset, is an architecture decision — not tokenomics.

Q6. **One shared Vanta state machine (Cosmos-style sovereign protocol logic) vs. a minimal
"facts + escrow + stake" state machine with everything else off-chain?**
The thinner the on-chain state machine, the safer and more upgradeable it is — but the less
Vanta can *enforce* (whatever it can't enforce becomes a trust assumption). Where is the
right line per base fact kind?

Q7. **Should Vanta define identity, or interoperate (DIDs/VCs + key continuity)?**
Leaning: interoperate, with Vanta-specific continuity objects so stake/reputation survive key
rotation. Test: key rotation and agent delegation scenarios.

Q8. **How do we keep reputation from becoming a universal, gameable score?**
Current principle: Vanta stores evidence, apps interpret. Test: can two rival markets compute
*different* (and both useful) reputations from the same history? If the answer is always
identical, the split is fake; if they diverge badly, evidence is too thin.

## Parked (later)
- Governance of schema evolution (who approves new fact kinds / new evidence schemes)
- Privacy/deletion tension (public immutability vs. regulated data) — may force private
  channels + public verification points
- Validator set and its centralization dynamics
- Fee-market design (spam control that doesn't price out small agents)
- What Spark and ThermoCompare have to do with any of this (needs author input)