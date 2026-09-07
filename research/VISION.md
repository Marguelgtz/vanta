# Vanta — Current Vision (v0.1, 2026-02-09)

Status: living document. Sections marked [HYPOTHESIS] are beliefs, not conclusions.

> **Note (2026-02-09, plan phase):** this document records the v0.1 research state,
> including its lean toward enforced commitment (economic layer) as center of gravity. The
> base MVP plan re-centers on the original vision — V1 (typed shared history) as the trunk,
> economics as a branch above the base. See [MVP_PLAN.md](MVP_PLAN.md) §1. The lean is kept
> here for continuity, not as the base plan.

## 1. What Vanta is — strongest version

Vanta is a neutral, permissionless, blockchain-maintained protocol in which parties that do
not trust each other — people, companies, machines, software agents — exchange **binding
promises** (commitments backed by staked value) about work or resources, and **evidence** that
those promises were kept. Both are recorded as immutable, typed, signed transitions in a
shared canonical history.

The protocol's own state is deliberately thin: identities, stakes, escrows, and the canonical
ordering of typed events (commitments, receipts, settlements, disputes). Everything else —
workloads, outputs, logs, measurements, and interpretations such as prices and reputation —
lives off-chain, bound to the protocol only by cryptographic commitments (hashes, Merkle
roots, ZK proofs).

**Vanta owns the evidence and the history. Applications own the interpretations.**

### At each level

- **One sentence, no jargon:** Vanta is a shared, permanent, neutral record of promises,
  work, and payment between parties — including machines — that no single company controls.
- **Smart non-technical:** When an agent rents an hour of GPU time from a machine it has never
  seen, someone has to guarantee the work happens and gets paid. Today that guarantee comes
  from a company you sign up with. Vanta replaces the company with a public rulebook: the
  machine that promises stakes something real, the work is verified, payment happens
  automatically, and every step is written into a history all parties — and anyone else — can
  check but nobody can rewrite.
- **Developer:** You emit typed, signed events (intent, commitment, receipt, settlement,
  dispute) from any language. The protocol orders them canonically, enforces escrow/stake
  state transitions, and keeps the full history. Your app keeps payloads off-chain and
  commits to them by hash. You can also *read other apps' history* — which is what makes
  cross-app reputation and interop possible.
- **Economic:** Independent parties use Vanta because their promises are backed by staked
  value that can be taken if they break them, and the record is one no counterparty can
  rewrite — so you can transact with a stranger, or a machine, with the same finality you'd
  have with an intermediary you trust.
- **Protocol:** Vanta owns: identities, stakes, escrows, canonical ordered event headers
  (who, which kind, what it commits to, when), and the state transitions those trigger.
  Vanta does not own: workloads, outputs, logs, or any interpretation.

### What Vanta makes possible that is not easy today

1. An agent with no human intermediary and no KYC buys compute from a machine it has never
   seen, guaranteed by stake rather than by a company's goodwill.
2. Two organizations with no common intermediary exchange a service with settlement neither
   can renege on — no billing relationship, no payment-processor terms.
3. Track record is portable: a provider's history on one app is readable by any other app on
   Vanta. (Today reputation is trapped per-platform: your history on one marketplace exists
   nowhere else.)
4. Records outlive the company: if the marketplace disappears, the history — and the value
   state — still exists.
5. Any independent party (auditor, insurer, another agent) can verify a claim by checking the
   public record, without the originating company's cooperation.

## 2. Why blockchain is intrinsic — the sharpened answer

The naive answer is "immutability." That is wrong or incomplete: a hash-linked log is already
tamper-evident, and a signed transparency log (Certificate Transparency) already gives
*detected* tampering. Neither is a blockchain.

The precise answer, [HYPOTHESIS, high confidence]: **blockchain is intrinsic for the step
from *recording* to *enforcing*.**

| Architecture | Gives you | Breaks for Vanta because |
|---|---|---|
| Centralized DB | Shared state owned by one operator | Operator can rewrite, censor, fail, or be compelled. No shared truth. |
| Append-only DB / event sourcing (centralized) | History the operator can't easily rewrite | Operator still controls appends, forks, availability. History is only as trustworthy as the operator. |
| Hash-linked log (single operator) | Tamper-evidence: silent alteration of past entries is detectable | Operator can still mint an alternative chain or vanish. You get *detection*, not *resolution*. |
| Signed transparency log (CT-style) | Detected misbehavior + third-party monitoring | Can record facts but cannot *enforce*: no escrow, no stake, no binding resolution of conflicts. Trust anchor is still the operator. |
| Federated / consortium ledger | Canonical ordering by known operators | Membership is permissioned; the operator set can collude or be compelled; nothing economic binds them. |
| Decentralized consensus + staking (blockchain) | Permissionless participation; canonicity as a *computable* property; economic security — maintainers stake value that can be *taken* (slashed) | — |

Three properties combine, and no simpler system has all three:

1. **Canonicity without an authority.** "Which history is true" stops being a social/political
   question (who do you believe?) and becomes a cryptographic-economic one (can you produce a
   history that satisfies the fork rule?). Anyone can compute the answer; nobody has to decide
   it.
2. **A shared value state.** Not just a log of facts, but state that *moves value* (escrow,
   stake). Logs can't hold your money; value state can.
3. **Economic security on the maintainers.** The parties that keep the ordering have skin in
   the game they can lose. That turns honest ordering from a favor into a dominant strategy.
   Vanta needs the same for providers: stake that can be slashed when a provider breaks its
   commitment.

**Vanta requires blockchain because it doesn't just record commitments between distrusting
parties — it enforces them: it holds value, orders the events that move it, and penalizes
provable misbehavior, all without any trusted party. Recording is what transparency logs do;
enforcement without an authority is what consensus mechanisms do.**

Counter to keep alive: a well-bonded federation *might* be "good enough" for a closed set of
parties (this is what much enterprise ledger practice is). The case against it here is
composability + permissionlessness: the machine-economy use case includes parties that cannot
be vetted in advance (new machines, new agents, new companies), and a permissioned operator
set is a trust point that breaks the "no intermediary" promise.
Confidence: high that *some* decentralized consensus is required; moderate that it must be
*permissionless* (vs. large rotating bonded federation) — the machine-actor argument is the
strongest case for permissionlessness.

## 3. Hidden assumptions inside the current vision

Each is a test, not a settled fact.

1. **Enforcement is the core.** If Vanta's value were purely *recording* facts, a
   transparency log would suffice and the blockchain would be decorative. (Hypothesis: no —
   enforcement *is* the value. Test: name a Vanta customer who would pay for recording
   alone.)
2. **Staking is non-optional.** The security model assumes parties post real value. If
   staking is optional or trivial, slashing is theater.
3. **Disputes are resolvable.** For much work "was it done well" is a human judgment. Vanta
   needs a fallback (bonded arbitrators, pre-agreed objective criteria). If disputes are often
   unresolvable, escrow degrades into a slow lockbox.
4. **Evidence is re-verifiable later.** A hash pointing at data that vanished is worthless.
   Where evidence blobs live (DA layer, content-addressed storage) is a dependency — and a
   potential centralized chokepoint.
5. **The agent economy is arriving.** The first killer app (Stint / machine commerce) assumes
   autonomous agents that actually transact. If they don't, Vanta is a general protocol with
   no first mover.
6. **One shared history beats many.** A single Vanta ledger across apps vs. a Vanta *protocol*
   running on many app-chains (the Cosmos/IBC vs. Ethereum question). The biggest open
   architecture question (QUESTIONS Q1).
7. **Verification tech matures.** Strong receipts eventually need ZK / verifiable
   computation. If that's a decade away, Vanta must live on optimistic verification +
   disputes for a long time.
8. **A native security asset is needed.** Stablecoins can't be slashed (they're IOUs). If
   protocol security needs slashing, a native asset for *security* — while services are priced
   in stablecoins — may be required.

## 4. Competing versions (kept alive, not merged yet)

| Version | Center of gravity | Clearest human value | Blockchain necessity | Cleanest primitive | DX | Credible economics | Stint relationship |
|---|---|---|---|---|---|---|---|
| V1: Immutable transaction protocol ("Protobuf but immutable") | Record format + ledger | Shared, tamper-evident, structured history apps can interoperate through | Moderate (recording alone could be a log) | Typed signed hash-linked "fact" | Good (emit events, read history) | Weakest (no value flow = no fees) | Stint is one of many apps |
| V2: Autonomous machine economy | Economic primitives + non-human actors | Your agent buys/sells compute, storage, APIs with strangers, no common intermediary | Strong (enforcement, permissionless, staking) | The commitment→receipt→settle cycle | Moderate (agents need safe spend authority) | Strong (fees on real flows) | Stint is the first app, center stage |
| V3: Receipt & accountability network | Evidence as first-class objects | Proof that something happened, portable across systems (audit, provenance, compliance) | Moderate (close to a transparency log) | The receipt / attestation | Good (issue/verify receipts) | Weak (who pays for evidence alone?) | Stint's receipts are one receipt type |
| V4: Decentralized state layer | A shared state machine apps use instead of proprietary DBs for authoritative transaction history | Your app's history outlives the app; interop without a common backend | Strong | The state transition | Hardest sell (developers love Postgres) | Moderate (app-chain fees) | Stint runs *on* Vanta as an app |

Current lean [HYPOTHESIS, moderate confidence]: these are less four rival explanations than
**views on one idea** — V4 is the substrate (shared value state + consensus), V1 is the data
model (typed immutable protobuf-like transitions), V3 is the key record family bridging the
off-chain world into on-chain enforcement, and V2 is the first killer application with Stint
as its first instance. **The center of gravity is enforced commitment — the economic layer.**

Why keep them competing: if the agent economy (V2) doesn't materialize, V1+V3+V4 must carry
the value alone; if one shared ledger (V4) turns out infeasible or unwanted, Vanta may have to
become a *protocol* (record format + rules) that runs on many chains, which changes what
"Vanta" is at all.

## 5. Evidence/interpretation split — and its challenge

Principle: Vanta stores **thin facts** (typed events: commitment by identity X, receipt with
evidence hash H, settlement of amount A), not derived opinions (reputation scores, prices,
quality). Any app computes its own interpretations from the public history.

Why: a universal reputation score would be arbitrary, gameable, and politically charged
across domains; evidence is what any market can price.

Challenge: event-sourcing everything gets needlessly complicated, and some apps just want a
score. Reconciliation: Vanta does *not* event-source the world — it stores only thin economic
facts. High-frequency telemetry stays off-chain; only its *summary commitments* touch Vanta.
Working test for "does this belong in Vanta state?": **does it settle or lock value, or
trigger a transition that settles or locks value?** Yes → on-chain. No → off-chain, committed
by hash.