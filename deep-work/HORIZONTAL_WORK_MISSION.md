# Vanta horizontal-work proof — cross-domain abstraction falsification

## Objective
Determine whether a reusable Vanta Work schema family can represent and compose genuinely
different forms of off-chain work while preserving each domain's native semantics. This is a
**post/base-MVP research mission**. It must not modify Vanta Core merely to make the hypothesis
pass.

The governing research is `research/HORIZONTAL_WORK.md`; the base contract is
`research/MVP_PLAN.md`.

The hypothesis under test is NOT "all work has a lifecycle". It is that Vanta's shared typed
history can support a durable cross-domain economic-provenance graph linking obligations,
performance claims, native evidence, attestations and resolutions.

## Success
A written `deep-work/horizontal-work-report.md` ends with exactly one verdict:

- `HORIZONTAL PASS` — all six proof conditions in HORIZONTAL_WORK §3 pass without changes to
  Vanta Core;
- `HORIZONTAL NARROW` — useful common structure exists but one or more domains/composition
  cases require narrowing the claim;
- `HORIZONTAL FAIL` — the common layer adds no meaningful semantics beyond generic metadata,
  or composition/economic-consumption requires domain logic in the common layer.

A PASS is not required. An honest FAIL is a successful research run.

## Constraints
- Do not add GPU/RPC/bandwidth/build/agent/lease fields to the common schema family.
- Do not add payment, escrow, reputation, market matching or dispute machinery to Vanta Core.
- Do not choose Cosmos, Akash or any other production substrate in this mission.
- Preserve native-domain semantics by explicit references/adapters; do not flatten evidence
  into an untyped `metadata` blob and call that interoperability.
- Scenario B remains generic software/deployment accountability; do not redefine it as Spark.
- Stint is a first-party test consumer, not Vanta's ontology.
- Akash and Lava are pressure tests/adapters, not dependencies.
- Any proposed Base MVP change must use the existing five-question change gate and be reported
  as `NEEDS_HUMAN`; do not silently make it.
- Prefer paper/spec fixtures and local deterministic tests. External network access must not be
  required for the verdict.

## Verification
bash scripts/verify-horizontal-work

## Tasks
- [ ] VANTA-H-001: Common vocabulary and falsification contract
  - acceptance: `work/spec.md` defines the minimal candidate schema family (obligation, performance, attestation, resolution or a smaller justified family), explicitly maps every field to existing Vanta Core Actor/Schema/Record/History mechanics, and copies the six pass/fail conditions from HORIZONTAL_WORK §3 into executable/testable assertions; no domain-specific common fields
  - verify: test -s work/spec.md && bash scripts/verify-horizontal-work
- [ ] VANTA-H-002: First-party cross-domain fixtures
  - acceptance: `work/fixtures/stint/` and `work/fixtures/deploy/` each express the full existing MVP pressure-test scenario using only the common work schemas + domain schemas; a report identifies what is common versus domain-native and demonstrates that Scenario B stays independent of Spark-specific concepts
  - verify: test -d work/fixtures/stint && test -d work/fixtures/deploy && bash scripts/verify-horizontal-work
- [ ] VANTA-H-003: Vertical-protocol semantic-preservation fixtures
  - acceptance: `work/fixtures/akash/` and `work/fixtures/lava/` model an Akash-style compute lease and Lava-style RPC service from documented/native concepts; every Vanta Work record contains explicit references to the native object/proof semantics needed to reconstruct meaning; no claim that Vanta replaces native metering, QoS, reputation or market logic
  - verify: test -d work/fixtures/akash && test -d work/fixtures/lava && bash scripts/verify-horizontal-work
- [ ] VANTA-H-004: Adversarial adjacent-standard comparison
  - acceptance: `work/adjacent.md` compares the proposed abstraction against A2A task lifecycle, ERC-8004 identity/reputation/validation, x402 payment and SLSA/in-toto provenance; for each, state exactly what Vanta would add, what it would not add, and one condition under which Vanta Work would be redundant
  - verify: test -s work/adjacent.md && bash scripts/verify-horizontal-work
- [ ] VANTA-H-005: Composition test
  - acceptance: `work/fixtures/composed/` expresses one parent job containing at least three child relationships from different domains (RPC/data -> compute/analysis -> artifact/build or equivalent); an independent reader can reconstruct child provenance and parent fulfillment using Vanta references without bespoke cross-domain protocol code
  - verify: test -d work/fixtures/composed && bash scripts/verify-horizontal-work
- [ ] VANTA-H-006: Economic-consumption test
  - acceptance: `work/economic-consumption.md` demonstrates at least two different external actions driven by the same Vanta Work history (for example settlement authorization and subsequent-job authorization/policy decision) while keeping payment/reputation outside Vanta Core; if this cannot be done without adding domain logic to the common layer, record the failure explicitly
  - verify: test -s work/economic-consumption.md && bash scripts/verify-horizontal-work
- [ ] VANTA-H-007: Verdict and change-gate audit
  - acceptance: `deep-work/horizontal-work-report.md` maps each of the six HORIZONTAL_WORK §3 conditions to evidence, lists all failed/awkward mappings, applies the change gate to every requested base change, records Cosmos/Akash only as ecosystem/funding implications, and ends with exactly one allowed verdict line; `bash scripts/verify-horizontal-work` passes strict mode
  - verify: test -s deep-work/horizontal-work-report.md && bash scripts/verify-horizontal-work

## Notes for human reviewers (ignored by the Stint parser; not in worker prompts)
- Run this after the current base MVP has a stable record envelope; it is intentionally a
  separate mission so funding/ecosystem ideas cannot contaminate the MVP ontology.
- H-003 should use documented shapes captured in repo research or fixtures; do not require live
  Akash/Lava access just to prove the schema mapping.
- The most important fail conditions are composition and economic consumption. A generic
  wrapper that merely stores arbitrary metadata is a FAIL/NARROW result, not success.