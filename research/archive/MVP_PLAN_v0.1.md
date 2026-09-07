> **ARCHIVED 2026-02-09** — superseded by `research/MVP_PLAN.md` (v0.2). Kept for continuity.
> The v0.1 plan faithfully planned the v0.1 *research*, which had leaned toward the economic
> branch; it therefore baked escrow/stake/slashing, a base fact family
> (intent/commitment/receipt/settlement/dispute/transfer), a test security asset, and a
> Cosmos app-chain into the base. The v0.2 plan re-centers on the original vision (V1 trunk);
> element-by-element diff in v0.2 §1.5.

# Vanta — Base MVP: Living Action Plan (v0.1, 2026-02-09)

## 0. What this plan is — and is not

This is a **living** plan for building the **rigid base** of Vanta: the minimal, stable
protocol core everything else is built on.

- **Living:** phases, tactics, sequencing, and tooling can change at phase gates, and
  research findings (QUESTIONS.md) feed back in at every gate.
- **Rigid:** the invariants in §1 do not change except by an explicit decision recorded in
  DECISIONS.md. If a build phase reveals an invariant is wrong, that is a *vision* event,
  not a refactor — stop and discuss.
- **Strictly aligned:** every element of the base is traceable to a decision (D1–D7) or a
  named hypothesis (VISION §3). The Phase 0 deliverable includes that traceability matrix.
- The base is **not**: an application, a token, a fixed chain choice, or a company. It is a
  state machine + record format + reference SDK, demonstrated on one testnet instance.

## 1. The rigid base — invariants (the constitution)

Each invariant: statement → why (research anchor) → revisit trigger.

**I1. Facts are typed, signed, hash-linked; history is canonical and replayable.**
Every transition on the base is a signed record conforming to a protocol-governed schema,
deterministically serialized, ordered canonically. State is a function of history:
`state = fold(history)`. Anyone can recompute any past state from the public log.
*Why:* the protobuf-ledger origin thread; D3; the "history is truth, state is derived"
model. *Revisit if:* replay cost makes the model unworkable (then: state sync from a
verified snapshot + log anchoring — history still canonical).

**I2. The protocol owns only thin value state.**
Base state = identities, stakes, escrows, canonical fact order, fee accounts. No payloads,
no workloads, no outputs, no logs, no derived opinions. Everything else is off-chain, bound
by hash/proof.
*Why:* D2, D6; the evidence/interpretation split; the on/off-chain boundary rule
(PRIMITIVES §6). *Revisit if:* an enforcement need proves a fact must live in state beyond
the rule "settles/locks value or triggers one."

**I3. Enforcement is the core: value is locked, deadlines act, settlement is automatic.**
Escrow and stake are on-chain state. Missing a receipt deadline automatically slashes the
committer's stake and releases escrow. A valid receipt automatically settles. No operator,
no party, can pause or redirect these transitions.
*Why:* D1 — recording vs. enforcing is exactly what makes the blockchain intrinsic.
*Revisit if:* fully automatic resolution proves unsafe for some obligation class (then:
per-class "grace window" parameters, not manual override).

**I4. Receipts are verification-agnostic.**
A receipt commits to evidence under a *declared evidence scheme* (scheme id + commitment:
hash, co-signature, or proof). The base checks scheme conformance, not ground truth. New
schemes (L2 bonded verifiers, L3 ZK proofs) are data, not protocol upgrades.
*Why:* D6; cross-domain generality finding (PRIMITIVES §4–5). *Revisit if:* scheme
conformance checking proves to be a security hole (then: trusted scheme registry with
governed admission — a controlled relaxation).

**I5. Obligations can be one-shot or recurring.**
A commitment may require a single receipt or a schedule of evidence (periodic proofs,
liveness). Continuing obligations settle on schedule and can be terminated with a
termination receipt.
*Why:* the storage cross-domain test (PRIMITIVES §5) — retrofitting recurring evidence into
a one-shot-only base would break the "general protocol" claim.

**I6. Identity is a continuity object; agents hold bounded delegated authority.**
Stake and history survive key rotation (successive keys, each signed by its predecessor;
recovery scheme reserved). A principal may delegate a scoped authority to an agent key:
spend cap, allowed fact kinds, time window. Delegation is itself a recorded fact.
*Why:* the machine-economy center of gravity (V2); PRIMITIVES §7. *Revisit if:*
delegation semantics prove too rich for the base (then: keep caps + validity window, drop
fine-grained kind filtering to the app layer).

**I7. Canonicity without an authority.**
The base runs on decentralized consensus with permissionless participation; maintainers
secure the ordering with staked value that can be slashed. No single party can rewrite,
censor value-state transitions, or freeze escrow.
*Why:* D1 (the sharpened "why blockchain" answer). *Revisit only if:* research produces a
credible simpler secure substrate (a research-level event, not an MVP event).

**I8. The protocol never stores interpretations.**
No reputation scores, prices, rankings, or quality judgments exist in base state or fact
schemas. Applications compute them from the public history.
*Why:* D2. *Revisit if:* two independent apps cannot extract stable, useful interpretations
from the base history (evidence too thin — the Q8 test).

## 2. What's in the base (MVP scope)

**In:**
- Identity: continuity object, key rotation, scoped delegation (spend cap / fact kinds /
  window), fee-bearing accounts.
- Fact kinds (base family): `intent`, `commitment`, `receipt`, `settlement`, `dispute`,
  `transfer` (plain conditional value movement — the degenerate-exchange case).
  Extension of the family: design-reserved, not built (no schema governance in MVP).
- Value state: escrow, stake, automatic deadline transitions, slashing, fees (anti-spam,
  denominated in the security asset).
- Evidence: scheme registry (scheme id → conformance rules), commitments (hash /
  co-signature / proof placeholder), one-shot + recurring schedules.
- History: canonical, thin, publicly queryable, replayable; state derivable from log.
- Reference SDK: two languages (proposal: Go + TypeScript).
- Proof scenario: a Stint-shaped engagement end-to-end on testnet — agent intent, provider
  commitment with stake, off-chain "work", hash-committed receipt, settlement; plus failure
  paths (provider vanishes → deadline slash; disputed receipt → dispute window outcome).

**Out (explicitly — all have reserved extension points):**
- Native asset economics (supply, price, incentives) — the base uses a **test security
  asset** whose *roles* (stake, slash, fees) are the real design; its *economics* are
  parked (D5).
- Governance (schema/scheme admission voting) — reserved interface, manual curation in MVP.
- Reputation/interpretation services — an app-layer concern (I8).
- ZK evidence (L3) and verifiable computation — the scheme slot exists; no ZK in MVP.
- DA-layer integration — evidence storage is a pluggable interface; MVP uses simple
  off-chain storage (Q3 parked).
- DID/VC identity interop — reserved (Q7).
- Cross-chain / multi-chain deployment — the *spec* is written protocol-first so the base
  state machine is not welded to one chain (Q1 parked).

## 3. Decisions the base forces us to take now (and the answers)

An MVP cannot park every open question. These are the forced choices, made deliberately:

| # | Question | MVP answer | Why this answer | Revisit trigger |
|---|---|---|---|---|
| Q1 (partial) | One chain or many? | Build **one testnet instance**; write the spec protocol-first (state machine + schemas separable from chain implementation) | A running instance is the only way to test invariants; protocol-first spec keeps "Vanta as a standard across chains" alive | Phase 4: cross-chain strategy once two real apps exist |
| Q2 (partial) | Dispute resolution fallback? | MVP minimum: **deadline slashing + consumer verification window** (L1 two-party receipts). Bonded arbitration: interface reserved, not built | The optimistic default is the security core (assume valid, punish provable fraud); arbitration needs its own research pass | Phase 4: design bonded arbitration once dispute data exists |
| Q3 (partial) | Where does evidence live? | **Pluggable storage interface**; MVP uses simple off-chain storage; hashes committed on-chain | Keeps durability/DA as a dependency to study, not a blocker | Phase 4: multi-DA strategy |
| Q5 (partial) | Native asset? | **Test security asset** with exactly three roles: stake, slash, fees. No supply design, no incentives, no pricing of services (services can be priced in any asset the parties choose, represented in escrow) | D5 guardrail: roles are architecture, economics are parked | When slashing design is concrete enough to name what must be stakeable |
| Q6 (partial) | How thin is the state machine? | **Exactly the §2 "in" list.** Nothing else enters state. | The base must be auditable by a small team; thinness is a security feature | Only via invariant revisit (I2) |

## 4. Technology direction (pragmatic — not part of the rigid base)

Rigidity lives in §1, not in frameworks. The stack is a Phase 0 exit decision.

- **Leading candidate: Cosmos SDK (CometBFT PoS) app-chain.** Rationale: it *is* the
  origin story made literal — a sovereign, Protobuf-native state machine with modules,
  staking, and slashing built in; Akash proves the marketplace shape on it; large ecosystem
  (tooling, validators, SDKs). Cost: framework gravity — Cosmos modules are heavyweight,
  and we must guard against inheriting state bloat (anti-I2).
- **Alternatives to evaluate at the Phase 0 gate:** (a) a lighter custom state machine on
  a minimal BFT consensus (more control, more security surface we own); (b) an Orbit-style
  L2 (inherits Ethereum security, adds a dependency); (c) Avalanche-style custom L1.
- **Selection test (Phase 0 exit):** the frozen spec (fact schemas + state transition
  table) must be expressible in the candidate with *no semantic compromises*; the
  alternative that preserves I1–I8 with the least foreign state is chosen. The spec stays
  portable — if we're wrong, the base re-runs on the other substrate.