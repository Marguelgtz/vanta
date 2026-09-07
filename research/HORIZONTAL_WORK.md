# Vanta — Horizontal Work Abstraction Research (2026-09-07)

Status: **candidate above-base protocol; not part of the Base MVP ontology.**

This document records the current hypothesis that Vanta's typed, attributable, permanent
history may support a reusable **economic provenance layer for off-chain work**. The goal is
to falsify that hypothesis before it becomes product architecture.

The Base MVP remains governed by `research/MVP_PLAN.md`: **Actor / Schema / Record / History**.
Nothing in this document adds a base primitive unless the MVP change gate is passed.

---

## 1. The hypothesis

Vertical protocols already solve specific service domains well:

- Akash: compute resource leasing and provider markets.
- Lava: RPC/data service, relay proofs, QoS and provider rewards.
- Sentinel: network/bandwidth service and usage accounting.
- A2A: agent task communication and task lifecycle.
- x402: programmatic HTTP-native payment.
- ERC-8004: agent identity, feedback/reputation and pluggable validation hooks.
- SLSA/in-toto: software-build provenance and attestations.

Vanta should **not** duplicate those systems.

The candidate horizontal abstraction is narrower:

> Different systems may be able to expose a common economic-provenance envelope linking an
> obligation to execution claims, domain-native evidence, outputs and economic resolution,
> while leaving execution and truth interpretation to the domain protocol/application.

The value, if real, is **composition and durable provenance across domains**, not replacing
vertical protocols or putting Vanta in their hot path.

---

## 2. Candidate Vanta Work vocabulary

These are **schemas above Vanta Core**, not protocol-native object types:

### `WorkObligation`
Describes what an actor accepted responsibility for.

Candidate content:
- accountable actor reference
- requester/author relation expressed through ordinary actor/reference semantics
- input commitments
- expected-output commitments or criteria references
- deadline/budget/terms as domain payload
- verification-policy reference
- parent/child work references

### `WorkPerformance`
Claims that an obligation was performed.

Candidate content:
- obligation reference
- output commitments
- domain-native execution references
- evidence references
- performer claim/signature

### `WorkAttestation`
A third party (or another participant) states something about an obligation, performance,
evidence item or output.

Candidate content:
- subject reference
- attester
- predicate / scheme identifier
- result or claim
- evidence commitment/reference

### `WorkResolution`
Records an application's resolution of a work relationship.

Candidate content:
- obligation + performance references
- accepted / rejected / challenged / superseded interpretation
- settlement/event references
- resolver actor

**Important:** payment, escrow, reputation, market matching, execution and dispute machinery
remain outside this schema family unless separately justified.

---

## 3. What would count as proof

A generic schema can always hide domain data in `metadata`. That is not proof of a useful
horizontal abstraction. The abstraction passes only if all of these hold:

1. **Domain neutrality** — Stint compute, software-build accountability, Akash-style leasing,
   Lava RPC service and at least one agent/task case fit without adding domain fields such as
   `gpu`, `rpc`, `bandwidth`, `build`, `agent`, `lease` to the common vocabulary.
2. **Semantic preservation** — native Akash leases, Lava relay proofs, SLSA provenance, etc.
   remain addressable and recoverable; Vanta does not flatten them into opaque blobs that
   destroy useful meaning.
3. **Composition** — one parent work relationship can reference child work from multiple
   domains without bespoke cross-domain protocol logic.
4. **Independent verification** — a party absent from execution can reconstruct the Vanta
   record graph, resolve referenced evidence, apply the declared policy and derive a result.
5. **Economic consumption** — some external system can act on the result (settlement,
   authorization, subsequent work, policy decision). If the output is only an audit log, the
   economic thesis is weak.
6. **No hot-path dependency** — Akash remains Akash, Lava remains Lava, software builds remain
   software builds. Vanta adds provenance/accountability rather than slowing every native
   operation.

**Kill / shrink triggers:** if composition (#3) or economic consumption (#5) cannot be shown
without domain-specific logic in the common layer, do not pitch a general work protocol.

---

## 4. Relationship to current MVP scenarios

### Scenario A — Stint compute
Already exercises:

`intent -> offer -> off-chain execution -> evidence commitments -> receipt -> interpretation`

For horizontal-work research, Stint is a **first-party concrete domain**, not the definition
of work. Vanta Core must remain unaware of Stint concepts.

### Scenario B — software/deployment accountability
Already exercises:

`source -> build -> test -> deploy -> third-party verification -> originator gone`

This is deliberately not "Spark" at the Vanta layer. Spark may later become a real consumer,
but the scenario must stay generic so it remains an independent pressure test.

### Scenario C — Lava RPC (paper/adaptor pressure test)
Use Lava because its service unit is very different from a long-running compute job. Lava
already has native relay proofs, compute-unit accounting, QoS and provider reputation. Vanta
must **reference** those semantics, not reinvent them.

### Scenario D — Akash (paper/adaptor pressure test)
Akash is a vertical compute market. The useful question is not whether Vanta can wrap a lease;
it is whether an Akash lease/provider/attestation can become evidence inside a broader work
relationship without Vanta becoming an Akash competitor or duplicating its market logic.

---

## 5. Composition test

The strongest proposed test is a parent job whose children are genuinely different:

1. obtain chain data through a Lava-backed RPC service;
2. run analysis/inference using a compute provider (Stint locally; Akash as an ecosystem
   adapter candidate);
3. produce a software/report artifact with build/provenance evidence;
4. record a parent performance/resolution that references the child evidence graph.

Vanta should only need generic record/reference/commitment mechanics plus the Work schema
family. Each child system retains its native semantics.

---

## 6. Cosmos-specific hypothesis

Cosmos is **not selected as Vanta's production substrate by this research**.

The ecosystem is relevant because it contains several vertical protocols (Akash, Lava and
others), the Cosmos SDK encourages reusable application modules, and IBC provides an
application-level interoperability substrate. A future Vanta Work reference implementation
could be a Cosmos SDK/IBC application without making Vanta Core Cosmos-specific.

Grant availability is not architectural evidence. Any Cosmos substrate decision must still
pass `MVP_PLAN.md`'s substrate/change gates.

---

## 7. Adjacent standards that constrain novelty

The novelty claim must survive these comparisons:

- **A2A** already defines generic agent task lifecycle and artifacts.
- **ERC-8004** already defines portable agent identity, feedback/reputation and generic
  validation requests/responses.
- **x402** already defines programmatic payment for HTTP resources.
- **SLSA/in-toto** already define rich software provenance/attestation patterns.
- **Sentinel-style signed service receipts** show that generic signed resource-consumption
  evidence is not new by itself.

Therefore Vanta must not claim novelty for "generic tasks", "signed receipts", "reputation",
"agent payments", or "proof of service" alone.

The candidate contribution is the **durable cross-domain economic provenance graph** built
on Vanta's shared typed history.

---

## 8. Current verdict

**Worth a formal proof spike; not yet a product commitment.**

There is repeated structure across unrelated domains, but the abstraction is only valuable if
it preserves native semantics and enables composition/economic action that the vertical
systems do not provide on their own.

Next execution artifact: `deep-work/HORIZONTAL_WORK_MISSION.md`.