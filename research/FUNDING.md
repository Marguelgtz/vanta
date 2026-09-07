# Vanta — Funding Strategy (2026-09-07)

Status: **active exploration; funding must not drive protocol architecture.**

The objective is to obtain enough external funding to spend a concentrated quarter proving or
killing the Vanta thesis, without pretending the project is already a production blockchain.
The current working first-phase target is **approximately USD 25,000 for one quarter**.

That number is a scoping target, not committed income and not a valuation of Vanta.

---

## 1. Funding principle

Pitch **bounded open-source R&D deliverables**, not "fund Vanta" and not a token/network
launch.

The first funder should be buying answers to questions such as:

- Does the Vanta Core abstraction hold under independent implementations?
- Can a useful horizontal work/economic-provenance schema exist across genuinely different
  service domains?
- Is there a reusable Cosmos SDK/IBC implementation worth maintaining?
- Which pieces belong in Vanta Core, which belong in Vanta Work, and which should stay in
  vertical applications?

A negative technical result is a valid R&D outcome if it is documented and reproducible.

---

## 2. Cosmos / Interchain route

### Interchain Builders Program

Current entry point: <https://interchain.io/builders>

The program provides technical/product support and ecosystem introductions and is explicitly
intended to help organizations determine whether the Interchain Stack fits their goals. It is
**not itself presented as a guaranteed USD 25k grant program**.

Use it first to obtain technical challenge and ecosystem routing.

### Interchain Foundation

Current foundation description: <https://interchain.io/about>

ICF states that it funds organizations through grants/investments and stewards the Cosmos
technology stack. The practical funding path appears relationship-driven rather than a simple
public small-grant form.

### Proposed first ask

A one-quarter R&D phase, approximately USD 25k, centered on:

1. Vanta Core protocol/spec hardening and threat model;
2. horizontal-work falsification (`research/HORIZONTAL_WORK.md`);
3. a minimal Cosmos SDK reference implementation **only if the abstraction survives**;
4. an IBC application/schema design spike, not generic middleware;
5. cross-domain demonstrations and an independent technical report.

The pitch should explicitly state that Vanta remains substrate-neutral until the substrate
spike earns a decision.

---

## 3. Akash route

Current grant page: <https://akash.network/grants/>

Akash currently exposes three relevant funding paths:

- community contributions;
- permissionless Community Pool proposals;
- direct Core Contributor Grants from Overclock Labs for infrastructure/services that drive
  network usage and utility.

Akash should **not** be asked to fund Vanta Core research. Its incentive is Akash-specific
usage/utility.

Two plausible Akash-aligned tracks are:

1. **Stint -> Akash backend / workload tooling** — useful if it creates real Akash leases and
   improves advanced inference/agent workload UX without duplicating existing tooling.
2. **Akash -> Vanta Work adapter** — useful only if it exposes Akash-native lease/provider/
   attestation evidence to a broader outcome/accountability workflow and creates incremental
   Akash demand.

Both must be checked against existing Akash projects before a formal proposal.

---

## 4. Solo-developer positioning

Do not present the project as led by an established blockchain-protocol specialist.

The credible positioning is:

- experienced product/platform/infrastructure engineer;
- direct experience with inference and remote-compute lifecycle problems through Stint;
- new to blockchain protocol implementation;
- deliberately seeking Cosmos/Interchain technical review before making architecture claims;
- narrow first phase with measurable open-source outputs.

The knowledge gap is part of the R&D plan, not something to hide.

---

## 5. Funding gates before treating Vanta as a funded quarter

Do **not** financially plan around a grant until there is evidence in all three categories:

### Technical signal
At least one knowledgeable Cosmos/Interchain engineer agrees the problem is real enough to
investigate, or provides a concrete correction that improves the thesis.

### Ecosystem signal
At least one vertical system/project (for example Akash/Lava/agent infrastructure) can name a
specific advantage from the proposed horizontal layer rather than saying the functionality is
already native.

### Funding signal
A concrete route from conversation to funded work exists (ICF/partner grant, investment,
Akash grant/community proposal, or equivalent).

Two of three = continue aggressively but keep financial assumptions conservative.
Three of three = reasonable to structure a quarter around the funded phase.

---

## 6. Pitch order

1. Finish/verify the current Base MVP work without Cosmos contamination.
2. Run the horizontal abstraction proof mission.
3. Prepare a compact technical thesis and gap map, not a long whitepaper.
4. Enter the Interchain Builders Program / technical conversation.
5. In parallel, test an Akash-specific value proposition in the Akash community.
6. Only then turn the accepted technical scope into a milestone/budget proposal.

Do not wait for a production chain, tokenomics, full marketplace, wallet, explorer or audit
before starting the funding conversation.