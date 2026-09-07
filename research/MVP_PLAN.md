# Vanta — Base MVP: Living Action Plan (v0.2, 2026-02-09)

Status: proposed, awaiting author review at CP0. Nothing is implemented yet. This plan
supersedes the v0.1 base plan (archived: `research/archive/MVP_PLAN_v0.1.md`); diffs in §1.5.

**Rigid:** the vision (§1) and the invariants (§2). **Living:** everything about how we get
there — architecture, ordering, implementation choices, deferrals, individual primitives,
experiments, and even whether an initially proposed abstraction survives. When a finding
changes the base, run the change gate (§10) and record it. A connection must be earned, not
assumed.

**2026-09-07 research note (non-governing for this MVP):** a candidate horizontal
work/economic-provenance layer is now being tested above the base (`research/HORIZONTAL_WORK.md`),
and Cosmos/Interchain + Akash funding routes are being explored (`research/FUNDING.md`). Neither
changes the Base MVP primitives, selects a substrate, or adds economic semantics to the current
Deep Work mission. The horizontal hypothesis gets its own follow-on falsification mission.

---

## 1. The non-negotiable vision (reconstructed)

Vanta is a **blockchain-native protocol/infrastructure** — not a company, SaaS product,
marketplace, compute network, or agent-commerce product — for **shared, permanent,
structured history**:

1. Structured, typed records become permanent shared history.
2. Any actor can sign and contribute to that history; no application or company owns it.
3. Important history does not belong to the application in which it occurred; it outlives
   that application.
4. Evidence and provenance are portable: off-chain data is referenced by content hash;
   claims are signed; reference chains are reconstructible by anyone.
5. Many applications can consume the same history and interpret it differently; no
   interpretation is protocol truth.
6. Blockchain is intrinsic: canonicity of the history, permissionless contribution, and
   indefinite liveness come from a decentralized substrate, not from an operator.
7. Vanta defines the *language* of history (records, types, references, attribution);
   higher layers define domain meaning (compute, provenance, commerce…).

> **Vanta owns the evidence and the history. Applications own the interpretations.**

Origin intuition: "Protobuf, but immutable" — the value is in structured, typed,
schema-governed records becoming permanent shared history. Protobuf is a stand-in, not a
prescription.

### Re-centering note (continuity, 2026-02-09)

The v0.1 research (VISION.md) leaned toward "enforced commitment — the economic layer" as
Vanta's center of gravity (a V2 lean), and used "does it settle or lock value?" as the test
for what belongs in the base. Per the author's constraint that **the original vision is the
constraint**, this plan re-centers:

- **V1 (immutable transaction/history protocol) is the trunk** of the base MVP.
- **V3 (receipts/accountability)** is strongly aligned and reveals base properties: portable
  evidence, provenance, identity continuity, history reconstruction.
- **V4 (state layer)** is a compatible, broader branch — used to pressure-test the base's
  generality, not built as a product.
- **V2 (machine/economic layer: escrow, staking, settlement, disputes, tokens, validator
  economics)** is a branch discovered through Stint, **not the definition of Vanta**. It sits
  above the base, or extends it later. Nothing from it enters the base unless the change gate
  shows the original vision independently requires it.

Consequence for "why blockchain": the v0.1 answer (enforcement of value commitments) is kept
as the argument for *branch* requirements. The *base* requirement is different and sufficient
on its own: **canonicity without an operator + permissionless contribution + indefinite
liveness** — properties a transparency log or federation does not provide, and which the
original vision explicitly demands (history that "does not belong to the application or
company in which it occurred").

This plan also **supersedes the v0.1 base plan** found in the repo (archived at
`research/archive/MVP_PLAN_v0.1.md`): that plan derived from the v0.1 research lean and
baked the economic layer into the base. Element-by-element diff in §1.5.

## 1.5 Diff against the v0.1 plan (superseded, archived)

The v0.1 plan was a faithful plan of the v0.1 *research* — and that research had drifted
toward the economic branch. Re-centering on the original vision changes the base as follows:

| v0.1 plan element | v0.2 treatment | Why |
|---|---|---|
| I3 "Enforcement is the core" (escrow/stake/auto-slash as base invariants) | Removed from base; becomes a V2 branch design above the base | The original vision demands shared history, not value enforcement |
| I2 base state = identities, stakes, escrows, fee accounts | Base state = the log itself + anchored schemas | Value state is branch state, not protocol state |
| Test security asset (stake/slash/fee roles) in the base | Removed entirely; fees/anti-spam are substrate concerns or later | No token/validator economics unless the base is forced to have them |
| I7 staked-validator consensus as a base requirement | I9: the substrate must provide only permissionless append, canonical ordering, verifiable inclusion, liveness | Decouples the protocol from consensus machinery; the chain is a choice, not a definition |
| Cosmos SDK app-chain as leading candidate (own L1) | An existing public substrate chosen by spike S1; own chain only if I5/I9 are infeasible | Custom chain machinery must be earned, not conventional |
| Base fact family: `intent/commitment/receipt/settlement/dispute/transfer` | No base fact family; the record envelope is type-opaque; lifecycles are application schemas | That family is one application's lifecycle (Stint's), not Vanta's ontology |
| Evidence-scheme registry in the base | `commitments[]` of content hashes in the record envelope; schemes/verification live above the base | The base references evidence; it never judges it |
| I5 recurring obligations in the base | Kept as an application-layer pattern (required by the storage cross-domain test) | A lifecycle concern, expressible with schemas + references |
| I6 spend-cap delegation in the base | Base = keys + rotation records; delegation = application schema | Spend caps are economic semantics (V2) |
| I1 state = fold(history) | Kept as a property available to stateful applications; the protocol's own state = the log | Clarification, not removal |
| I4 verification-agnostic receipts | Generalized: the base records attestations under any schema; truth is application-level (§3) | Keeps V3's power without V2's semantics |
| Proof scenario: one Stint-shaped engagement on testnet | Two substantially different consumers (Stint-shaped A + deployment accountability B), an independent third-party verifier, two divergent interpretations, an originator-gone test | One consumer cannot separate Vanta primitives from app abstractions |
| Reference SDK in two languages | Kept (S0's two-language determinism test requires it anyway) | Interop proof between independent implementations |
| Protocol-first, chain-agnostic spec | Kept — now invariant I9 | Consistent with the re-centering |

Everything else in v0.1 (rigid/living discipline, phase gates, decision traceability) is kept
in v0.2 and strengthened by the explicit change gate in §10.

## 2. Protocol invariants (rigid)

- **I1 — Append-only history.** Vanta's history is a canonically ordered sequence of
  records. No record is ever modified or deleted; corrections are new records.
- **I2 — Attribution is protocol-level.** Every record is signed by its author's key;
  anyone can verify "key K authored record R" from public data alone. What an actor is
  beyond a key (person, company, agent, machine) is interpretation/attestation, not
  protocol knowledge.
- **I3 — Typing is neutral.** Records are validated as typed bytes against
  content-addressed schemas; the protocol never interprets payload semantics; any two
  conforming implementations parse the same record identically.
- **I4 — Provenance is structural.** Records reference earlier records by content hash;
  provenance/derivation chains are reconstructible by any verifier.
- **I5 — Canonicity without an authority.** The ordering of history is fixed by a
  decentralized, permissionless substrate; no party — including the protocol's deployer —
  controls which records enter or in what order. *(Assumption to confirm with the author at
  CP0; see A8.)*
- **I6 — Survival independence.** History remains verifiable after the originating
  application/company disappears. Schema definitions are anchored in history. Off-chain data
  is referenced by content hash; its durability is a separate, above-base guarantee (not
  base truth).
- **I7 — Interpretation is application-owned.** The protocol stores no interpretations
  (scores, prices, quality, statuses). Applications derive them off-chain or publish them
  as records (attested claims). **State is protocol-owned; everything else is history.**
- **I8 — Truth is application-level.** The protocol distinguishes what it directly knows
  (K signed R; R is at position P; R references R') from what a record *claims* about the
  external world (attestations). Attested claims are never elevated to protocol truth.
- **I9 — Substrate discipline (MVP design principle).** The record format is
  chain-agnostic. The substrate is required to provide only: permissionless append,
  canonical ordering, verifiable inclusion, indefinite liveness. Nothing more.

## 3. "Facts" vs. "attestations" — the distinction the base is built on

Two tiers, kept separate everywhere:

| Tier | Examples | Protocol's relation |
|---|---|---|
| **Protocol knowledge** | "R was signed by K" · "R is at position P in history" · "R is typed by schema S" · "R references R1, R2" | Known directly; verifiable by anyone from the substrate alone |
| **Attested claims** | "this artifact was built from these sources" · "this work was executed" · "key K is operated by company X" | Stored as typed data inside a record; their truth depends on the attester's process and on above-base verification; applications choose how much weight to give them |

Consequence: Vanta never answers "is this true?" It answers "who said this, under which
schema, with which evidence commitments, at which position, and what does it reference?"
The question of truth belongs to applications — independent attestors, audits, ZK proofs,
cross-attestation. This is what lets the base stay useful for both a GPU-work receipt (Stint)
and a build-provenance attestation without the protocol understanding either domain.

## 4. Proposed minimal primitives (under test at CP1)

1. **Actor** — a public key; acts by signing. Key rotation, delegation, and organizational
   identity are *records under agreed schemas* (continuity conventions), **not** new
   protocol machinery. The base knows *who signed*; *who they are* is attested above.
2. **Schema** — a canonical, content-addressed type definition, published as a record.
   `schema_id = H(schema bytes)`. Records carry `schema_id`. Evolution = a new version (a
   new ID); older records remain parseable because the bytes are hash-bound. The protocol
   checks well-formedness and anchoring, never semantic approval.
   *(Open: anchor schemas as records in history vs. a minimal registry state — spike S2.
   Current lean: as records, which keeps the protocol's state = the log itself.)*
3. **Record** — the atomic unit of history. A canonical envelope:
   `{ schema_id, payload, author_signature, references[], commitments[] }`
   signed over its full canonical serialization; `record_id = H(canonical bytes)`.
   - `references[]` = content hashes of earlier records (provenance, dependency, reply).
   - `commitments[]` = content hashes of off-chain data (evidence, artifacts, logs). The
     base guarantees referenceability, not availability.
   The protocol validates the envelope, never the payload's meaning.
4. **History** — the append-only, canonically ordered, permissionlessly contributed log of
   records, maintained by a decentralized substrate; anyone can verify inclusion and order.
   The base protocol's entire "state" is this log (plus the view of anchored schemas).

Deliberately **not** base primitives: value/asset, escrow, stake, settlement, dispute,
intent, receipt-as-protocol-type, commitment-as-protocol-type, verifier, provider, consumer,
reputation, build, deployment, agent. Those are schemas and lifecycles that *applications*
define above the base. The `intent → commitment → receipt → settlement → dispute`
vocabulary is one useful higher-level lifecycle (Stint's) — not Vanta's ontology.

### What Vanta explicitly does not understand
Payload semantics · external-world truth · value · actor roles or relationships (beyond
signed references) · domain lifecycles · off-chain content or its availability ·
interpretations · which schemas are "good" · anything about the domain a record's schema
describes. If something is not on this "not understood" list, question why it is in the
protocol.

## 5. MVP boundary and deliberate exclusions

**In (base MVP):**
- Record format + canonical serialization + content IDs + signature envelope.
- Schema convention: publish, resolve, evolve (S2).
- Permissionless append + canonicity on one chosen substrate (A1), and the mapping of its
  ordering onto Vanta's canonical history (A6).
- Verification: a tool/library that, from public data alone, validates any record
  (signature, typing, references, inclusion/order) and reconstructs any derivation chain.
- Actor = key model + key-rotation convention (records, not machinery).
- Off-chain commitment by hash (no availability guarantee in the base).
- Two pressure-test scenarios as integration tests (both from §7), plus a third-party
  verifier implementation independent of the test consumers.

**Deliberately excluded (base MVP):**
- Value transfer, escrow, staking, slashing, settlement, protocol fees — V2 branch, above
  the base.
- Native token, validator set, custom consensus, own L1 — only if a spike shows no existing
  substrate can meet I5/I9 (A1).
- Dispute resolution — a domain process expressed in records; the base only records
  statements.
- Protocol-level reputation or any score.
- Availability/durability guarantees for off-chain data (commitment ≠ custody; above-base
  service).
- Privacy/encryption/ZK (later layer; commitment design must not preclude it).
- Formal governance protocol (schema anchoring starts as process + convention).
- Application state machines / a "bring your app's state to the chain" platform (V4 as
  product — the *property* "an app can event-source Vanta history as its authoritative
  history" comes for free and is desired; the *product* is not built).
- Cross-chain bridges / history views (later; the record format is designed to be
  substrate-portable in the meantime).
- Production decentralization, Sybil resistance, fee markets, scale engineering.

## 6. The four tiers

### Core / required now
Everything in §5 "In," plus the spikes that de-risk it (S0–S4, §9) and checkpoints CP0–CP3
(§10).

### Aligned but above the base (planned next, not built in the MVP)
- **Vanta Work (candidate; must pass falsification before adoption):** a schema-level
  vocabulary for work obligations, performance claims, attestations and resolutions that may
  link heterogeneous domain-native evidence into one provenance graph. It is not a base fact
  family and does not own execution, payment, reputation or market logic. See
  `research/HORIZONTAL_WORK.md`.
- **Stint as first full consumer**: its own schemas for the
  intent/commitment/receipt/settlement/dispute lifecycle; a value layer (escrow/stake/
  settlement on the same substrate); evidence-verification schemes for compute; market
  mechanics.
- **Deployment/software accountability as an app**: provenance schemas (SLSA/in-toto/SPDX
  shaped, as payload schemas — not protocol types), attestation policies, artifact
  availability.
- **Availability services**: DA-layer anchoring; storage-provider attestations ("this
  content is retrievable from X").
- **Verification/attestation services**: independent attestors, cross-check conventions;
  later a verifier market (V2-adjacent).
- **Interpretation frameworks**: libraries + conventions for computing reputation/pricing/
  audit from history; an "interpretation publication" schema (interpretations published as
  records, never as state).
- **Cross-substrate history view** (unified view via light clients).
- **Privacy layer**: encrypted records + ZK selective disclosure.

### Worth exploring later
- Spanning chains / a unified history across substrates (Vanta as a standard, not only a
  network).
- Vanta's own consensus/L1 — only if invariants cannot be met on existing substrates at
  acceptable cost/complexity.
- A native security asset — a V2-branch question (needed only if a staking/slashing value
  layer is built above and requires slashable value).
- ZK proofs of execution as an evidence scheme (L3 evidence from v0.1 research).
- Organizational/social key recovery (continuity beyond single rotation chains); DID/VC
  interop for real-world identity anchoring.
- Fee/anti-spam design if substrate economics require it.

### Not currently part of the vision
- Vanta as a marketplace or price-discovery system.
- Vanta as a compute network / GPU marketplace.
- Vanta as an agent framework, runtime, or wallet product.
- A protocol-level token (a V2-branch question, never a base requirement).
- Vanta as a generic decentralized database / application-state platform (V4 as product;
  the branch remains compatible).
- A universal protocol-level reputation system.
- Vanta-owned application state (balances, ownership ledgers as protocol state).

## 7. Pressure-test scenarios — how they are used

Both scenarios serve three roles: (1) **on paper** at CP1 — full record sequences written
out to expose missing capabilities; (2) **as integration tests** after the base is built —
two minimal test-consumer apps, no shared code outside the base, each computing a different
interpretation; (3) **as permanent regression** — any proposed base change must pass both
scenarios or be justified through the change gate. A primitive that only makes sense in one
of the two scenarios is challenged for base membership.

### Scenario A — Stint (compute; the domain we understand)
Domain concepts live in Stint's schemas, not in the protocol:

| Step | Base elements exercised | Above the base |
|---|---|---|
| Agent expresses a need | record (Stint's `intent` schema); actor = agent key | spend authority (delegation record), market UI |
| Provider offers | record **referencing the intent's hash** (provenance); actor = provider key | pricing, capacity claims |
| (escrow/stake) | — excluded from base | V2 value layer |
| Work executes | off-chain; the base sees nothing | execution, logging |
| Evidence | `commitments[]` = content hashes of logs/outputs | evidence-verification scheme (how to check GPU work) |
| Receipt | record (a `receipt` schema) referencing the offer + commitments | verification co-signature, dispute process |
| (settlement) | — excluded from base | V2 value layer |
| Reputation | history readable by any app | reputation computation (interpretation) |

Stress points: moderate record volume per engagement; ≥3-actor chains (an agent key acting
for a company — company-level attribution is *above* the base via a delegation record);
large/proprietary evidence (commitment only, content off-chain).

### Scenario B — software/deployment accountability (deliberately not compute)
A third party must be able to verify: source commit → build artifact (hash A) → test →
deployment to environment E, with attribution, without trusting the originating company.

| Element | Base elements exercised | Above the base |
|---|---|---|
| Source/commit | commitment to a content hash (a VCS ref) | the VCS itself |
| Build attestation | record (a `build` schema, SLSA-shaped) signed by the build-system key; references the source commitment; commitment to artifact hash A | build pipeline, reproducibility checks |
| Test attestation | record referencing the artifact; commitment to test logs | test infrastructure |
| Deployment | record (a `deploy` schema) by the deployer key; references artifact + environment | deployment tooling |
| Third-party verification | any verifier reconstructs the DAG from history, re-downloads artifact A by hash, re-checks signatures | policy decisions, audit reports |
| After the company disappears | history + schemas persist on the substrate; artifact re-verifiable if its storage survives (else: availability gap → above-base service) | — |

What B catches that A does not: **multiple actors attesting the same content** (no
uniqueness assumption — the base must tolerate this cleanly); attester ≠ performer (a
build-system key, a human-operated deployer key — no actor *types* needed); verification by
recomputation (a verifier re-hashes the artifact; no market settlement involved).

## 8. Architectural questions to answer before implementation

- **A1 — Substrate.** Which existing chain/DA meets I5/I9 at acceptable record cost?
  Spike candidates: a cheap EVM L2; Solana; Celestia (DA) + a small anchor. (A Cosmos-style
  app-chain is a *later-phase* option, not an MVP candidate — it is exactly the "own chain
  machinery" we avoid unless forced.)
- **A2 — Record addressing.** `record_id` = content-only (portable, order-independent) vs.
  content + history position (canonical Merkle identity). Current lean: **both** — content
  ID for references/portability, position for canonicity.
- **A3 — Schema anchoring.** As records in history (no protocol state) vs. a minimal
  registry state. Lean: as records. Plus the usage rule: a record may use only schemas
  anchored earlier in history (or self-describing inline schemas — byte-cost tradeoff, S2).
- **A4 — Batching.** One substrate transaction per record vs. batches (Merkle tree of a
  batch, root anchored). Driven by S1 cost data; no scale engineering before numbers exist.
- **A5 — Canonicalization + signature.** One canonical form (Protobuf canonical encoding vs.
  a compact custom form — "Protobuf" as stand-in, per the origin thread) and one signature
  scheme for the MVP (e.g., Ed25519), with an envelope that admits more later.
- **A6 — Ordering semantics.** How substrate block/transaction order maps onto Vanta's
  canonical history (batch → segment; within-batch order = deterministic serialization
  order).
- **A7 — Off-chain data.** Commitment-only in the base (availability excluded) — confirm,
  or does the survival test (I6) need a minimal availability convention? Lean: excluded,
  demonstrated above-base.
- **A8 — Permissionless contribution.** Is I5's "anyone may publish" a hard MVP
  requirement, or is "not controlled by the application" sufficient? Lean: hard — it is
  cheap on a public substrate and in the spirit of the vision. *(Confirm at CP0.)*

## 9. Experiments / spikes (only where uncertainty is real)

- **S0 — Canonicalization & identity** (1–2 days). Pick a serialization; implement record
  canonicalization, content ID, and signature envelope in **two** languages; round-trip
  tests. Kills: any ambiguity in "what exactly is signed"; interop risk between
  independent implementations.
- **S1 — Substrate probe.** On the top-2 candidates from A1: append a batch of ~100
  records, read back, verify an inclusion proof from a fresh node; measure cost/latency/
  effort. Decides A1/A4/A6.
- **S2 — Schema convention.** Publish a schema as a record; resolve it from history via an
  independent implementation; test an additive version bump (v2). Decides A3.
- **S3 — Paper scenarios** (parallel with S0/S1). Write out scenarios A and B completely as
  record sequences; list every capability used; anything not in §4 → change gate.
- **S4 — Key rotation** (small). Rotation convention as a record + verifier that follows
  rotation chains; test that attribution survives rotation. (Could fold into S3 — it is a
  convention, not machinery.)

## 10. Order of work and checkpoints

```
CP0 (author review) ──> S0 ─────────────┐
                                         ├─> CP1 ──> S1 ──────────┐
                     S3 (parallel) ──────┘                         ├─> CP2 ──> base build
                     S4 (small, optional) ─────────────────────────┘        (S2 with S1)
                                                                              │
                                                              CP3 (MVP demo) ──> CP4
```

- **CP0 — before any work.** Freeze invariants I1–I9; author confirms the re-centering
  (§1), A8 (permissionless writes), and the substrate shortlist. *Challenge here: do the
  invariants still read, to the author, as "the original Vanta"?*
- **S0 ∥ S3 → CP1.** The primitive set (§4) survives both paper scenarios; canonicalization
  proven in two languages. *Challenge: any S3 gap that tempts an addition to the base? Run
  the gate below.*
- **S1 ∥ S2 → CP2.** Substrate + batching + schema model chosen; per-record cost
  acceptable for scenario volumes (tens of records per engagement — not millions/second).
  *Challenge: is the chosen substrate a hidden V2/V4 assumption (picked for DeFi tooling,
  or for app-chain sovereignty)? Does it preclude a later own-chain path?*
- **Base build.** Protocol spec (record format, invariants, substrate mapping) + reference
  implementation (anchor + emit/verify SDK) + standalone verifier.
- **CP3 — the MVP demo (success defined in §11).** End-to-end on the substrate: both
  scenarios run as minimal test-consumer apps; a third-party verifier (independent
  implementation) checks history, signatures, references, ordering; two different
  interpretations are computed; then the originating apps are "turned off" (services
  stopped) and verification still passes. *Challenge: did any test-consumer logic leak
  into the base? Are the interpretations genuinely different?*
- **CP4 — post-MVP.** Write the above-base layer plans (value layer / Stint first;
  availability; verification services) as separate living documents.

**Change gate (for any proposed base change):**
1. Is this required by the original Vanta vision?
2. Is it merely useful for one application?
3. Is it an aligned extension that belongs above the base?
4. Is it research-driven vision drift?
5. Does adopting it make the foundation more general, or simply more complicated?

An answer of "one application" or "drift" keeps the item above the base or parks it. Any
base change requires the author's explicit sign-off and a change-log entry.

## 11. Definition of success

The MVP is successful when, on the chosen substrate, demonstrably true:

> Independent actors can create structured, typed, cryptographically attributable records
> that become part of a shared blockchain-backed history; later applications can
> independently verify that history and build their own interpretations on top of it
> without relying on the original application as the authority.

Testable sub-criteria:

1. **Attribution.** Any record is verifiable by anyone, from public data alone, as signed
   by a specific actor key — including across a key rotation.
2. **Typing.** Any record's schema resolves by ID and parses identically in two
   independent implementations sharing no code outside the base.
3. **Canonicity & sharedness.** Two independent verifiers agree on the same history
   (records + order) without trusting each other or any operator; inclusion is verifiable
   against the substrate; contribution was permissionless.
4. **Provenance.** Both scenarios' derivation chains (intent→commitment→receipt;
   source→build→test→deploy) are reconstructable by a third party from history alone.
5. **Independence from the originator.** With the originating test application stopped/gone,
   the history remains verifiable and interpretable.
6. **Interpretation freedom.** At least two independent applications compute different,
   correctly derived interpretations from the same history; neither interpretation is
   stored in the protocol.
7. **Economic neutrality.** The entire demo involves no token, escrow, stake, or value
   transfer — the foundation stands without economics.
8. **Pressure-test survival.** Both scenarios used only base primitives; all domain
   concepts lived in schemas / above the base.

**Refinements proposed** (both anchored to the original vision, not the later economic
branch): (a) key rotation included in criterion 1 — otherwise a dead key means a dead
actor, breaking the survival property the original vision demands (history outlives the
application); (b) criterion 7 added as an explicit anti-contamination test. I propose no
removals from the author's statement: it is the right definition; the sub-criteria make it
checkable.

## 12. Contamination risks (watch list)
- **Grant-driven architecture:** Cosmos/Interchain/Akash funding may influence which reference
  adapters are explored first, but may not choose Vanta's substrate, ontology or token/economic
  model without passing the same evidence/change gates as any other proposal.

| Risk | Symptoms to watch for | Mitigation |
|---|---|---|
| V2 (economic) leaks in | value fields in the record format; "provider/consumer/verifier" become actor types; escrow in the base spec; substrate picked for DeFi/staking tooling | domain concepts = schemas only; base records are type-opaque; substrate chosen on I5/I9 fit alone; no token/validator set in the base, ever |
| V3 (receipts) overreach | the protocol validates receipt *quality* (a "proof-of-work engine" in the base); protocol-level reputation; a "verifier" role in the spec | the base records attestations, never judges them; verification is above the base; no role vocabulary in the base |
| V4 (state layer) bloat | general key-value/app state in the protocol; an "app module" API in the base; upgrade coupling across unrelated apps | protocol state = the log (+ anchored schemas), nothing else; apps keep/derive their own state; no module system in the base |
| V1 over-specification | serialization/governance/privacy designed before the spikes; consensus tuned for unproven scale | spikes first; the base stays minimal until CP3; anything the scenarios don't touch is deferred |
| Process contamination | "Stint defines the protocol" — a compute-only primitive sneaks into the base | two-scenario rule: a primitive that only works for one of A/B is challenged via the gate; test consumers are separate apps |

## 13. Open questions for the author (input needed before/at CP0)

1. **A8:** hard permissionless-write requirement, or is "not controlled by the application"
   enough? (Lean: hard.)
2. **Substrate stance:** neutral, or are there preferences/constraints (ecosystem, team
   skills, a later own-chain path)?
3. **Key rotation:** base convention (lean — free, since it is "just a record") or above
   the base?
4. **Demo scope realism:** is the CP3 demo (two minimal test-consumer apps on a substrate +
   independent verifier) the right size, or should the MVP stop at "verifier + one
   scenario end-to-end"?
5. **Stint constraints:** any Stint design details that constrain scenario A (e.g., how
   evidence is shaped today)? The repo has only a research-level description.
6. **Spark / ThermoCompare:** Spark may later be a concrete consumer of Scenario B, but the
   scenario remains generic software/deployment accountability and does not constrain the base.
   ThermoCompare still needs author input before any relationship is claimed.
7. **The v0.1 plan:** the superseded plan found in the repo — anything in it you want kept
   beyond what §1.5 already preserves?

## 14. Change log
- 2026-02-09 — v0.2 plan created. Re-centered the base from the v0.1 research lean
  (enforced commitment / V2-adjacent) to V1 (typed shared history), per the author's
  constraint that the original vision is the constraint. Proposed: invariants I1–I9;
  primitives (Actor, Schema, Record, History); the fact/attestation split (§3); four
  tiers (§6); questions A1–A8; spikes S0–S4; checkpoints CP0–CP4; success criteria (§11).
  Supersedes the v0.1 base plan (archived: `research/archive/MVP_PLAN_v0.1.md`); diff in
  §1.5. Awaiting author review at CP0.
- 2026-09-07 — horizontal-work research recorded as a **separate above-base falsification
  track**; Cosmos/Interchain and Akash recorded as ecosystem/funding opportunities, not Base MVP
  architecture decisions. Current MVP missions remain substrate-agnostic.